# Eval report v0 — <team name> · <agent name>

**Date:** <30 October 2026>   **Eval-set:** `evals/eval_set_v0.csv` (your agent) or `evals/tickets_v0.csv` (the Paylio starter), <N> cases   **Prototype commit:** `eval-v0`

## 1. The number against the criterion
| | Value |
|---|---|
| Success criterion (from the brief, Session 3) | *"By 30 October, on our eval-set, at least 45 % of 'how do I' tickets get a draft that two graders would send without editing — and no draft quotes a price or promises a refund."* |
| Drafts produced (grounded + policy pass) | <k> / <N> = <xx> % |
| **Drafts two graders would send without editing** (graded by hand) | <k'> / <N> = **<xx> %** |
| Drafts on human-only tickets (should be 0) | <n> |
| Policy blocks | <n> |
| Routing accuracy | <xx> % |
| Retrieval hit@3 | <xx> % |

**Verdict:** criterion met / not met.

## 2. The three most frequent misses
| # | What went wrong (one line) | Example ticket id | Which component | What it becomes in `spec.md` v2 |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## 3. Who graded, and how
Two graders, independently, "would I send this without editing?" yes/no. Disagreements: <n> — resolved by <discussion / a third person>.

## 4. What is demo data and what is eval data
State it plainly: which tickets did you look at while tuning the prompt or the threshold? Those are demo data now and are excluded above.

## 5. Next step (one line)
