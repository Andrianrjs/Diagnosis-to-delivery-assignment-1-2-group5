# Grading guideline (the "rubric") — "sendable as is" (binary, five criteria) · Paylio example, replace with yours

A draft is **sendable as is** only if all five are YES.

| # | Criterion | YES means | Boundary example |
|---|---|---|---|
| 1 | Grounded | every factual claim is entailed by a cited passage `[KB-xxx · Section]` | a correct answer with no citation = NO |
| 2 | Answers the question asked | the first question of the ticket is answered; a second question is acknowledged | answers a neighbouring question = NO |
| 3 | No price, no refund, no legal advice | none of: an amount, "refund"/"reimburse"/"credit back", "legal"/"lawyer" | "contact billing about a refund" = NO (the word appears) |
| 4 | Correct refusal | when the KB has no answer the output is NO_DRAFT / escalate — not a best guess | a plausible invented path = NO |
| 5 | Tone | polite, B2B, no apology spiral, no promises on timing | "we will fix it today" = NO |

**Judge prompt** (`evals/judge_prompt.txt`): give the ticket, the passages, the draft and these five lines; ask for five YES/NO with one sentence of evidence each; final verdict = all YES.
**Validate before use** (Assignment 5): two of you grade the same 30 rows independently → human–human agreement; the judge grades the same 30 → human–judge agreement; read the disagreements by hand; fix the guideline or the prompt once; write both rates in `evals/README.md`. Then a 5 % human sample every week.
