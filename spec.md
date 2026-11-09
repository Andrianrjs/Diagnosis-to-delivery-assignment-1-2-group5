# spec.md — executable spec · LabelFlow refund agent · skeleton v0

Group 5 · 8 November 2026. Session 3 skeleton, completed in Session 4.
Same content as `03_product_brief.md`, with nothing left vague.

## problem

Support agents at LabelFlow (15,000 merchants, 25,000 tickets/month, ~7,500 shipping-label refund requests) spend ~9 minutes per refund request cross-referencing a long refund policy against a separate carrier-tracking system. For requests under €20 — about 65 % of them — that review costs more (~€5) than the amount refunded, and the merchant waits ~3 days. The eligibility decision has never been codified: it is tribal knowledge applied by hand, one ticket at a time. The agent codifies it, settles small claims under a hard amount ceiling, and produces a decision receipt that is both the merchant's answer and the audit record.

## user_workflow

```
- triage    : ticket text + metadata          -> refund | not-refund            (L4)
- read_policy: claim type + amount + dates    -> clause_id + clause_text        (L4)
- read_track : tracking_number                -> carrier events[] | NOT_FOUND   (L4)
- decide     : clause + events + amount       -> refund | prepare | recommend
                                                 | refuse(reason) | unknown
                                                 (L4 < €20 · L2 €20–100 · L1 > €100)
- receipt    : decision + clause + evidence   -> receipt{clause, evidence, amount}  (L4)
- execute    : receipt                        -> refund posted to billing       (L4 < €20 only)
- escalate   : case + assembled context       -> human queue                    (person only)
```

The way back to a person exists at every step, not only at the end: `escalate` is reachable from `decide`, from `execute`, and from the merchant's side of the receipt with one click.

## io_contracts

```
ticket    : {id, merchant_id, text, amount_eur, tracking_number, order_date, language}
evidence  : {tracking_number, events[{code, timestamp, location}], retrieved_at}
            | {status: "NOT_FOUND"}
decision  : {action: refund|prepare|recommend|refuse|unknown,
             amount_eur, clause_id, confidence, trust_level: L1|L2|L4}
receipt   : {decision, clause_id, clause_text, evidence, amount_eur,
             model_version, policy_version, approver_id|null, created_at}
```

Hard invariant: **no `receipt` may carry `action: refund` with `evidence.status == "NOT_FOUND"`.** This is enforced in code, before the model is called, not by prompting.

## edge_cases

- **No tracking number in the ticket** → `unknown`; ask the merchant once for it; never infer delivery from the order date.
- **Tracking returns NOT_FOUND or stale (> 72 h since last event)** → `unknown`, escalate. Never decide on partial evidence.
- **Amount ≥ €20** → never `refund`. `prepare` from €20 to €100, `recommend` above €100. Enforced on the amount field, before the model.
- **Amount missing or unparseable** → treat as above the ceiling; escalate.
- **No policy clause matches** → `unknown`, escalate, and log it as a policy-coverage gap (a documentation signal, not a model failure).
- **Two clauses conflict** → `unknown`, escalate. The agent never picks between contradictory policy.
- **Policy version changed since the last eval run** → block execution until the eval-set has been replayed.
- **Language not covered (outside FR/EN)** → escalate with the original text; never translate a policy decision.
- **Personal data in the ticket beyond what the decision needs** → excluded from the receipt (GDPR minimisation).
- **Same merchant, repeated sub-€20 claims in a short window** → decide normally, flag for the splitting monitor.
- **Duplicate request for an already-refunded order** → `refuse(already_refunded)`, with the prior receipt id as evidence.

## fallbacks

- `confidence < 0.75` → escalate with the assembled context; the agent does not guess under its own ceiling.
- Tracking API unavailable → `unknown` for every case; the queue routes to humans unchanged. The agent degrades to nothing, not to guessing.
- Policy index unavailable → same.
- Billing write fails after a decision → the receipt is written, the refund is not; the case goes to the human queue marked `execution_failed`. Never retry a money-moving write silently.
- Rolling 7-day refunded amount exceeds the pre-agent baseline by **> €2,000** → every case drops to L2 automatically (agent prepares, person approves) until a human clears it.

## done_criteria

- The success criterion from `03_product_brief.md` §7: on the 200-case eval-set, **≥ 55 % of automatable sub-€20 refund requests** receive a decision that two graders would execute without editing.
- **Zero** receipts carrying `action: refund` without tracking evidence (hard invariant, adversarial cases included).
- **Zero** refunds executed above €20 by the agent alone.
- Both counter-metrics flat or better against the human baseline: over-refund rate, wrongful-refusal rate.
- Every decision in the run produced a receipt. A decision with no receipt counts as a failure, whatever its outcome.

## out_of_scope

The WON'T column of the MoSCoW board, dated 8 Nov 2026: auto-refund above €20 · proactive refund detection · multilingual receipts · carrier-dispute auto-filing · bulk refund handling.

## eval_set

`evals/eval_set_v0.csv` — 20 cases now, growing to 200 by Session 5. Synthetic inputs, hand-labelled; origin recorded per row. Split by `merchant_id`, never by case, to prevent leakage. See `evals/README_eval_set.md` for the generation recipe.
