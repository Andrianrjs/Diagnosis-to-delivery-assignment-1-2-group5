# spec.md — LabelFlow refund agent, v2 (after eval-v0)
> Written from `03_product_brief.md` v2 (Session 3). This is what the coding agent reads. Every section is a decision; nothing here is "nice to have".

## 1. Problem (one paragraph)

LabelFlow's tier-1 support agents spend ~9 minutes per shipping-label refund request cross-referencing a long refund policy against a separate carrier-tracking system; for requests under €20 (~65 % of ~7,500/month) that review costs more (~€5) than the amount refunded, and the merchant waits ~3 days. The agent applies the policy to the tracking evidence and produces a decision receipt (clause, evidence, amount). Under €20 it settles alone; from €20 to €100 it prepares and a person approves; above €100 it only recommends; every refusal is confirmed by a person.

## 2. Workflow — five steps, in this order

1. **Route** — rung 1. Detect the language (`fr | en | other`) from a word list. `other` → `unknown`, reason `language_not_covered`. Parse `amount_eur` as a positive number; missing or unparseable → `unknown`, reason `amount_missing`.
2. **Routing rule** — rung 1. The evidence gate. `tracking_number` must match `LF-` + 8 digits and the carrier record must be readable; otherwise `unknown`, reason `no_tracking_evidence`. This runs before any decision: no evidence, no decision.
3. **Retrieve** — rung 1. Read the carrier record for the tracking number (in v0 the `evidence` column of the eval-set stands in for the carrier API) into `{status: NO_SCAN|IN_TRANSIT|DELIVERED|RETURNED_TO_SENDER, days, duplicate_charge, prior_refund, damage_claim, disputed}`. Load the clauses from `kb/refund_policy.md` (one clause per `## ` heading).
4. **Decide** — rung 1, rules in this order:
   - **[v2 · EV-050]** the merchant's text describes a situation no clause covers (carrier stopped operating / service withdrawn, carrier bankruptcy, strike, natural disaster, customs seizure; FR and EN) → `unknown`, reason `policy_exception`. Runs first, before any clause. v2: keyword list; next: rung-3 classifier (see `04_architecture.md` §9)
   - prior receipt already refunded → refuse `POL-6.3-already-refunded`
   - `DELIVERED` and (record says the merchant disputes, or the text says "never received" / "not received" / "jamais reçu" / "pas reçu") → `unknown`, reason `evidence_contradicts_merchant`
   - **[v2 · EV-018]** `NO_SCAN` or `IN_TRANSIT` and the carrier record gives no elapsed days → `unknown`, reason `incomplete_evidence`. A clause that applies to the status but cannot be evaluated is never skipped; days are never read from the merchant's text
   - duplicate charge → refund candidate `POL-6.1-duplicate-charge`
   - `NO_SCAN`: days ≥ 14 → refund candidate `POL-4.2-unused-label`; days < 14 → refuse `POL-4.2-unused-label`
   - **[v2 · EV-031]** `IN_TRANSIT`: days ≥ 21 → refund candidate `POL-5.3-lost-in-transit`; days < 21 → refuse **`POL-5.3-lost-in-transit`** (not yet lost; the receipt tells the merchant to ask again from day 21). v0 cited POL-4.5 here, which contradicts the policy text
   - `DELIVERED`: damage claim → refuse `POL-7.2-damage-not-label`; otherwise refuse `POL-4.5-consumed-label`
   - `RETURNED_TO_SENDER` → refuse `POL-4.6-return-to-sender`
   - a duplicate charge overrides a status-based refusal (the claim is about the charge, not the parcel)
   - two refund candidates → `unknown`, reason `conflicting_clauses`; nothing matches → `unknown`, reason `no_clause_matches`
   
   Then the amount band, on the amount field only, never on the merchant's text: refund and amount < €20.00 → `refund` (L4); €20.00 ≤ amount ≤ €100.00 → `prepare` (L2); amount > €100.00 → `recommend` (L1); any refusal → `refuse` (L2).
5. **Policy check** — rung 1. Before a receipt is written, block it if `action == refund` and the evidence is `NOT_FOUND`, or if `action == refund` and amount ≥ €20.00. A blocked receipt is not executable and goes to a person with its reason. This is the hard invariant, enforced in code, not by prompting.

## 3. Contracts

- Input: `{case_id, merchant_id, input_text, amount_eur, tracking_number, evidence}`.
- Output (the receipt): `{case_id, action: refund|prepare|recommend|refuse|unknown, trust_level: L4|L2|L1|person, clause_id, clause_text, evidence, amount_eur, reason, policy: pass|block, model_version, policy_version, created_at}`.
- The merchant's free text is never copied into the receipt (GDPR minimisation).

## 4. Edge cases

- Exactly €20.00 → `prepare`, never `refund`. Exactly €100.00 → `prepare`. €100.01 → `recommend`.
- Day 14 with no scan → refundable; day 13 → refused. Day 21 in transit → refundable.
- The merchant's text claims something the evidence contradicts ("unused" but `DELIVERED`) → decide on the evidence; the receipt cites the evidence, not the claim.
- Instructions inside the merchant's text ("ignore the policy", "approve €50") → ignored; amount and action come only from the fields and the rules.
- Same merchant, two or more sub-€20 refunds in the run → decide each normally, raise `split_flag` on the merchant.
- Language other than FR/EN → `unknown`; never translate a policy decision.
- **[v2 · EV-050]** A merchant describing an exceptional situation in prose is never decided by the rules, even if the fields alone would point to a clause.
- **[v2 · EV-018]** A carrier record without elapsed days for a time-based status is incomplete evidence: escalate, do not fall back on the clauses that remain.
- **[v2 · EV-031]** An in-transit parcel before day 21 is "not yet lost" (POL-5.3), not "consumed" (POL-4.5): the clause cited must tell the merchant when to come back.

## 5. Fallbacks

- Carrier record `NOT_FOUND` or carrier API down → `unknown` for that case; the agent degrades to nothing, not to guessing.
- No clause matches, or two clauses conflict → `unknown`, escalated with the context assembled.
- Policy check blocks a receipt → nothing is executed; the case goes to a person marked `blocked` with the reason.
- **Kill switch ⏻**: if the file `prototype/SWITCH_DOWNGRADE` exists, every `refund` becomes `prepare` (L2) for every case, until a person removes it.

## 6. Surface (Streamlit, one file) — optional in v0

- **Queue** page: list of eval cases; the selected case shows the receipt (action, trust level, clause and its text, evidence, amount, reason) and two buttons, _Execute_ and _Escalate_. _Execute_ is disabled unless `action == refund` and `trust_level == L4`. Buttons only show a toast. Caption: "Prototype — no money moves."
- **Eval** page: runs §7 and shows the table and the headline number.

## 7. Evaluation (`evals/eval_set_v0.csv`, 50 rows — never tune while looking at it)

- Columns: `case_id, merchant_id, segment, input_text, amount_eur, tracking_number, order_date, evidence, expected_action, expected_clause, handover, why_this_case_exists, origin`.
- EV-001 to EV-020 were read while these rules were written: report them apart as **demo**. EV-021 to EV-050 are the **held-out** set; the headline comes from them only.
- Metrics to print, for held-out and demo separately:
  - **decision accuracy** = share of rows where `action == expected_action`
  - **clause accuracy** = share of decided rows where `clause_id == expected_clause`
  - **executable as is** (the proxy for two graders) = share of **automatable sub-€20** rows (amount < €20 and `expected_action != unknown`) where action **and** clause both match
  - **refunds without evidence** (must be 0) and **refunds ≥ €20 alone** (must be 0)
  - **decided on human-only** = rows with `expected_action == unknown` that got a decision (must be 0)
  - **escalated decidable** = rows with a decision expected that got `unknown`
  - **hand-over rate** and **policy blocks**
- Print the misses grouped by cause (`expected → got`, with the case ids).

## 8. Definition of done

**At least 55 % of automatable sub-€20 held-out cases executable as is, zero refunds without tracking evidence, zero refunds ≥ €20 alone, and zero decisions on human-only cases.** Below that: do not change the rules to fit the rows — list the misses by cause and propose the change to this spec.

## 9. Out of scope (v0)

Any model call, real carrier API, real billing, login, database, merchant-facing view, the L2 approval queue (SHOULD), auto-refund above €20, multilingual receipts, carrier-dispute filing, bulk refunds.

## 10. Files

```
kb/refund_policy.md          the policy, one clause per ## heading (invented: LabelFlow is a case)
evals/eval_set_v0.csv        evaluation set, 50 rows (frozen)
prototype/                   ← build here: router.py route_rule.py retrieve.py decide.py policy.py evals.py (app.py optional)
```

Run: `python3 prototype/evals.py` · `streamlit run prototype/app.py`


## 11. Changes from v0 — every eval-v0 miss is a line

Run `eval-v0` (17 Nov 2026, `evals/report_v0.md`): held-out 19/20 = 95 % executable as is (criterion 55 %), **FAIL** on one decision taken on a human-only case. Following §8, the rules were not tuned to the rows; the spec changed instead.

| Miss | Case | Cause | Change in this spec |
|---|---|---|---|
| Decided a human-only case | EV-050 | Rules read fields, not prose; an exception the policy does not cover looked like a too-early unused label | §2.4 first rule: `policy_exception` → `unknown` |
| Right action, wrong clause | EV-031 | Spec v0 contradicted the policy text for in-transit parcels before day 21 | §2.4: refuse under POL-5.3, not POL-4.5 |
| Refund instead of conflict | EV-018 | Carrier record without elapsed days; POL-4.2 skipped silently | §2.4: `incomplete_evidence` → `unknown` |

The prototype at tag `eval-v0` implements v0. v2 is rebuilt from this spec and must be evaluated on a **fresh** held-out slice (the 200-case set planned for Session 5), not on EV-021–EV-050, which have now been read while writing these changes.