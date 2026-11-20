# Grading guideline · "executable as is" · LabelFlow refund agent

Group 5 · written 20 November 2026, before anyone grades. Replaces the Paylio example. The judge prompt (`evals/judge_prompt.txt`) is this guideline, copied.

**The question a grader answers for each receipt:** *"As a tier-1 support agent, would I execute this receipt as it is, without editing it?"* For a hand-over (`action: unknown`), the question becomes: *"Is handing this case to a person, with this reason, the right call?"*

**What the grader sees:** the merchant's text, the amount, the carrier record, the clauses of `kb/refund_policy.md`, and the agent's receipt. **Not** the expected label of the eval-set: the grader judges the receipt, not its match with our label.

## The five criteria (YES / NO)

| # | Criterion | YES means | Boundary example |
|---|---|---|---|
| 1 | Right action, right trust level | the action is the one the policy gives on this evidence, at the level the amount allows: refund < €20 at L4 · €20.00–100.00 prepared at L2 · > €100.00 recommended at L1 · any refusal at L2 | €20.00 refunded at L4 = NO (€20.00 is prepared, not settled) |
| 2 | Right clause | the clause cited is the one a grader would cite for this evidence | in transit for 10 days, refused under POL-4.5 "consumed" = NO (POL-5.3: not yet lost, ask again from day 21) |
| 3 | Decided on the evidence | the decision rests on the carrier record, and the record contains what the clause needs (status and, for POL-4.2 and POL-5.3, the elapsed days); nothing is taken from the merchant's text | a refund with evidence `NOT_FOUND` = NO, and it breaches a floor; a decision when the record gives no elapsed days = NO |
| 4 | Correct hand-over | a case the policy gives to a person ("Cases a person always decides") returns `unknown` with a reason; a decidable case is not handed over | an exception written in prose ("the carrier stopped operating in my region") refused under POL-4.2 = NO; a clear unused label after 22 days handed over = NO |
| 5 | Usable receipt | the clause text is present, the merchant's free text is not copied, and a refusal under POL-4.2 or POL-5.3 tells the merchant from when to ask again | `clause_text` empty = NO; a POL-5.3 refusal with no "ask again from day 21" = NO |

## The verdict

| Verdict | When | Counts as "executable as is"? |
|---|---|---|
| **EXECUTE** | all five YES (a correct hand-over is an EXECUTE: the case goes to a person as it is) | yes |
| **EDIT** | 1, 3 and 4 YES, but 2 or 5 NO: the decision is right, the receipt must be corrected before it is sent | no |
| **FAIL** | 1, 3 or 4 NO: wrong decision, decision without the evidence it needs, or a human-only case decided | no |

Floors, counted apart from the rate: a refund without tracking evidence, a refund ≥ €20 at L4, a human-only case decided. One of them fails the run whatever the percentage (`spec.md` §8).

## How the two graders work

1. Same 30 rows (the golden set), graded **independently**, without talking, in the two columns `grader_A_would_execute` and `grader_B_would_execute` (EXECUTE / EDIT / FAIL), with one sentence when the verdict is not EXECUTE.
2. Agreement = rows with the same verdict / 30. Below 80 %, the guideline is unclear, not the graders: rewrite the criterion where most disagreements sit, once.
3. A row we still disagree on after discussion is relabelled `unknown` in the eval-set (`evals/README_eval_set.md`).
