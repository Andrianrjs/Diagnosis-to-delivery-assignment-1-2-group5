# Eval report v0 — Group 5 · LabelFlow refund agent

**Date:** 17 November 2026   **Eval-set:** `evals/eval_set_v0.csv`, 50 cases (30 held-out + 20 demo)   **Prototype commit:** `eval-v0`
**Run:** `python3 prototype/evals.py` · receipts in `evals/results_v0.csv`

## 1. The number against the criterion

| | Value |
|---|---|
| Success criterion (from the brief, Session 3) | *"On our eval-set, at least 55 % of automatable sub-€20 refund requests receive a decision that two graders would execute without editing, and no decision executes a refund without tracking evidence attached to its receipt."* |
| Decisions produced (action ≠ unknown), held-out | 22 / 30 = 73 % |
| **Executable as is** — action **and** clause match the label, automatable sub-€20 held-out cases | **19 / 20 = 95 %** |
| Decisions on human-only cases (should be 0) | **1** (EV-050) |
| Refunds without tracking evidence (should be 0) | 0 |
| Refunds ≥ €20 settled alone (should be 0) | 0 |
| Policy blocks | 0 |
| Decision accuracy (action matches the label), held-out | 97 % |
| Clause accuracy (clause matches the label, decided cases), held-out | 96 % |
| Hand-over rate, held-out | 27 % |
| Splitting flag raised | M-6028 (EV-038 + EV-039) and M-1042 (EV-001 + EV-002), as designed |

**Verdict:** **criterion not met.** The percentage clears 55 % by a wide margin, but the definition of done (`spec.md` §8) also requires zero decisions on human-only cases, and EV-050 was decided. Following the method: we do not change the rules to make the row pass; the miss becomes a line in `spec.md` v2.

## 2. The three most frequent misses

Each cause occurred once; together they are every miss in the run (held-out and demo).

| # | What went wrong (one line) | Example ticket id | Which component | What it becomes in `spec.md` v2 |
|---|---|---|---|---|
| 1 | A policy exception written in prose ("the carrier has stopped operating in my region") was read as an ordinary too-early unused label and **refused**; a person should have decided | EV-050 | `decide.py` (rules read fields, not prose) | Before the clause rules, detect merchant text that describes a situation no clause covers → `unknown`, reason `policy_exception`. v0: keyword list; v1: rung-3 classifier |
| 2 | A parcel in transit for 10 days was refused under **POL-4.5** (consumed) instead of **POL-5.3** (not yet lost, ask again at day 21): right action, wrong reason sent to the merchant | EV-031 | `decide.py` / `spec.md` §2.4 | `IN_TRANSIT` and days < 21 → refuse citing **POL-5.3-lost-in-transit**, as the policy text says. The spec v0 rule was wrong, not the code |
| 3 | The carrier record gave no elapsed days, so POL-4.2 could not be evaluated and was **skipped silently**; only the duplicate-charge clause remained and the agent refunded instead of escalating the conflict | EV-018 | `retrieve.py` + `decide.py` | A clause that applies to the status but cannot be evaluated because a field is missing → `unknown`, reason `incomplete_evidence`. Never skip a clause for lack of data |

## 3. Who graded, and how

The figure above is the **automated proxy**: a case counts only if both the action and the clause match the label two of us agreed on when writing the eval-set (`evals/README_eval_set.md`). The hand grading — two graders, independently, "would I execute this receipt without editing?" yes/no — is done in the two empty columns of `evals/results_v0.csv` by Raveloarimanga Rajesy Ny Andrian and Clémence Marco. Disagreements: *to fill after grading* — resolved by discussion; a case we still disagree on is relabelled `unknown`, as the eval-set README requires.

## 4. What is demo data and what is eval data

**EV-001 to EV-020 are demo data.** We read them while writing the rules in `spec.md`, so they are reported apart (12/12 = 100 %, one miss: EV-018) and excluded from the headline. **EV-021 to EV-050 are the held-out set**, written after the rules and never used to change them.

Two honest limits on the 95 %. The held-out cases were written by the same team, in the same session as the rules, so they share our blind spots. And all 50 cases are synthetic: there is no real ticket in the set. The number says the rules do what the spec says; it does not yet say the spec matches real merchants.

## 5. Next step (one line)

Apply the three lines to `spec.md` v2, rebuild from the spec, and re-run on a **fresh** held-out slice written by someone who has not read the rules — the 200-case set planned for Session 5.