# 04 · Architecture — Group 5 · LabelFlow refund agent

> Session 4 deliverable, with `spec.md` v2 and `evals/eval_set_v0.csv` (50 rows).
> Describes the prototype as built at tag `eval-v0` (`/prototype`, rules only, no model call). Changes decided after the eval are in `spec.md` §11 and in §9 below.

## 1. One-line description

A rules-based agent that checks LabelFlow merchants' shipping-label refund requests against the refund policy and the carrier tracking record, and produces a decision receipt (clause, evidence, amount, trust level): it settles refunds under €20 alone, prepares €20–100 refunds and every refusal for a support agent to approve, and only recommends above €100.

## 2. The diagram

```
request ──▶ [1 router] ──▶ [2 routing rule] ──▶ [3 retrieve] ──▶ [4 decide] ──▶ [5 policy check] ──┬─▶ refund < €20 (L4) ─▶ executed ─▶ ⊘ weekly sample review
            language,       tracking number      carrier record    clause rules                     │
            amount          + record readable    + policy clauses  + amount band                    ├─▶ ⊘ €20–100 or refusal (L2): a person approves ─▶ executed
               │                 │                                     │                  │ block   │
               │ other language  │ no evidence                         │ no clause /      │         └─▶ ⊘ > €100 (L1): a person decides
               │ / no amount     │                                     │ conflict /       │
               ▼                 ▼                                     ▼ dispute          ▼
            ⊘ escalate to a person, with the receipt and the reason ◀──────────────────────┘

⏻ switch: the file prototype/SWITCH_DOWNGRADE. While it exists, every refund the agent
  would settle alone becomes "prepare" (L2) — for every merchant — until a person removes it.
```

## 3. Component table

| # | Component | Rung | Pattern | Trust level | Checkpoint ⊘ | Metric observed (eval-v0, held-out) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `router.py` — language FR/EN, amount parsed | 1 rules | routing | L4 (read-only) | abstention | 2/2 stops correct (EV-033 no amount, EV-041 German) |
| 2 | `route_rule.py` — evidence gate: tracking number format + readable carrier record | 1 rules | routing | L4 (read-only) | abstention | 2/2 stops correct (EV-040 malformed number, EV-049 carrier timeout); 0 refunds without evidence |
| 3 | `retrieve.py` — carrier record parsed; clauses loaded from `kb/refund_policy.md` | 1 rules | chaining | L4 (read-only) | none | clause accuracy 96 %; missing elapsed days not detected (EV-018, demo) |
| 4 | `decide.py` — clause rules, then amount band | 1 rules | chaining | L4 < €20 · L2 €20–100 and refusals · L1 > €100 | approval (L2, L1) · sampling (L4) | decision accuracy 97 %; 19/20 executable as is; 1 human-only case decided (EV-050) |
| 5 | `policy.py` — blocks a refund without evidence or ≥ €20; kill switch | 1 rules | evaluator (hard check) | L4 (can only block) | abstention | 0 blocks needed; 0 refunds ≥ €20 alone |

## 4. Workflow or agent?

A workflow. The path is drawn in advance: five steps in a fixed order, every branch written in `spec.md` §2, and no component chooses its own next step or tool. That is the right choice for our risk level: the agent moves money, the policy is a finite list of clauses, and every decision has to be explainable clause by clause to a merchant and to an auditor, which a rule can do and a model cannot yet. To move one step up — a model in step 4 for the requests the rules escalate — three things would have to be true: the model abstains instead of guessing (zero decisions on human-only cases on a fresh held-out set), its output is still checked by `policy.py`, which stays rules-only, and it never raises the €20 ceiling.

## 5. Fallbacks

- retrieval finds nothing (no tracking evidence): no decision; `unknown`, reason `no_tracking_evidence`, escalated (EV-040).
- the model's confidence is below the threshold: there is no model in v0; the equivalent — no clause matches, or two clauses conflict, or the record contradicts the merchant — gives `unknown` with the reason (EV-042).
- the policy checker blocks the draft: nothing is executed; the case goes to a person marked `blocked` with the reason (0 blocks in eval-v0).
- the API is down (carrier endpoint timeout): `unknown`, escalated; the agent degrades to nothing, not to guessing (EV-049).

## 6. The override switch ⏻

- Who can switch it off: the Head of Support Operations, who owns the kill-switch (`governance.md` §4), by creating `prototype/SWITCH_DOWNGRADE`; only they remove it.
- Scope: everyone — every merchant, every case, until removed. v0 has no per-merchant switch.
- Tested on: 17 November 2026, by Raveloarimanga Rajesy Ny Andrian — with the file present, no case ended in `refund`.

## 7. Data

- Training / demo data: none trained — rules only. EV-001 to EV-020 are **demo data**: read while the rules were written, reported apart, excluded from the headline. The policy (`kb/refund_policy.md`) is invented: LabelFlow is a case.
- Evaluation data (`evals/eval_set_v0.csv`): 50 synthetic cases; EV-021 to EV-050 are the held-out set. Labelled by Raveloarimanga Rajesy Ny Andrian and Clémence Marco (two-annotator rule, `evals/README_eval_set.md`). **Never used for tuning**: the three misses changed the spec, not the rules (`spec.md` §11).
- Personal data present? Merchant ids and free text only, all synthetic. The receipts in `evals/results_v0.csv` do not copy the merchant's text (GDPR minimisation, `spec.md` §3). In production: merchant id, tracking number and receipt in the audit log, accessible to support and finance only — see `governance.md`, Session 4.

## 8. Eval result v0

"**95 %** of automatable sub-€20 refund requests (19/20, held-out) got a decision two graders would execute without editing — criterion was **55 %**. **Not met**: one human-only case was decided (EV-050), which the definition of done forbids." — `evals/report_v0.md`

## 9. What you would build next (3 lines max)

1. Rebuild from `spec.md` v2: a `policy_exception` stop before the clauses (EV-050), POL-5.3 for in-transit refusals before day 21 (EV-031), `incomplete_evidence` instead of skipping a clause (EV-018).
2. Replace the exception keyword list with a rung-3 classifier that only abstains — it can send a case to a person, never decide one — still behind `policy.py`.
3. Re-evaluate on the 200-case set written by someone who has not read the rules, and add a per-merchant switch.