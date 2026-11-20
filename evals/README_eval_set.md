# evals/README_eval_set.md — where the 20 cases come from

Group 5 · LabelFlow refund agent · 8 November 2026

## Why the data is synthetic

LabelFlow is a case, not a client: we have no refund tickets. The assignment allows
generating inputs where no data exists, provided the origin is written in every row and no
real customer data is used. **No row here comes from a real person, a real merchant or a
real carrier record.** Merchant ids, tracking numbers, receipt ids and clause ids are
invented and internally consistent, nothing more.

## The recipe

1. **Start from the decision space, not from the tickets.** `spec.md` allows five outcomes
   (`refund`, `prepare`, `recommend`, `refuse`, `unknown`) and three trust bands (< €20,
   €20–100, > €100). The eval-set has to exercise each, including the ones that cost money
   to get wrong.
2. **Write one case per policy clause we claim to handle**, then one case per *failure* of
   that clause. EV-001 and EV-005 are the same clause with the date flipped; EV-009 and
   EV-010 are the same claim with the amount moved five cents across the ceiling.
3. **Write the adversarial cases deliberately**, not as an afterthought. Five of the twenty
   (EV-007, EV-016, EV-017, EV-018, EV-020) exist to make the agent say "I don't know".
   An eval-set with no unknowns measures confidence, not competence.
4. **Label by hand, two people.** Every row carries who labelled it and when. Where the two
   of us disagreed, the row is marked `unknown` rather than resolved by one of us — a case
   two graders cannot agree on is not a case the agent should settle alone.
5. **Record the origin in the row**, not in this file alone, so a row stays honest after it
   has been copied somewhere else.

## Coverage of the twenty

| Dimension | Cases |
|---|---|
| `refund` (L4, under €20) | EV-001, EV-002, EV-003, EV-006, EV-008, EV-009 |
| `refuse` | EV-004, EV-005, EV-013, EV-014, EV-015, EV-019 |
| `prepare` (L2, €20–100) | EV-010, EV-011 |
| `recommend` (L1, > €100) | EV-012 |
| `unknown` → hand-over | EV-007, EV-016, EV-017, EV-018, EV-020 |
| Ceiling boundary (€19.95 / €20.00) | EV-009, EV-010 |
| Missing or unusable evidence | EV-007, EV-020 |
| Evidence contradicts the merchant | EV-016, EV-019 |
| Conflicting clauses | EV-018 |
| Coverage gap (language) | EV-017 |
| Repeat merchant (splitting signal) | EV-001 + EV-002, EV-009 + EV-010 |
| Duplicate against a prior receipt | EV-015 |

Hand-over rate across the set: **8 of 20 (40 %)**. That is high on purpose. v0 is weighted
towards the edges because the easy middle is what the 200-case set will be made of, and
because the cases that decide whether this agent can ship are the ones where it should
stop.

## Leakage rule

Splits are **by `merchant_id`, never by case**. EV-001 and EV-002 share M-1042; EV-007 and
EV-008 share M-4120; EV-009 and EV-010 share M-3744. If those pairs were split across train
and test, the agent would be scored on a merchant it had already seen, and the score would
be flattering and wrong.

## Grading

A case passes when **two graders would execute the agent's decision without editing it** —
not when the action label matches. A right answer for the wrong reason fails: the receipt
must cite the clause a grader would cite and the evidence a grader would rely on. `unknown`
is correct wherever the expected action is `unknown`; escalating a decidable case is a
failure, and deciding an escalatable one is a worse failure.

Hard invariant, checked separately from the score: **no receipt may carry
`action: refund` with `evidence: NOT_FOUND`.** One breach fails the run regardless of the
percentage.

## To do by Session 5

Grow to 200 cases, rebalancing towards the real distribution (the hand-over rate should
fall as the easy middle is filled in). Replace the invented clause ids with the real policy
version once it exists. Re-run the whole set at every model-version change, before the
agent is allowed to move money again.
