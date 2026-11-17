# spec.md — Paylio support copilot, prototype v0

> Written from `03_product_brief.md` v2 (Session 3). This is what the coding agent reads. Every section is a decision; nothing here is "nice to have".

## 1. Problem (one paragraph)
Paylio's tier-1 support agents (Karim) spend ~40 % of their day searching the knowledge base and the policy to answer "how do I…" tickets, and the first answer at night takes up to 14 h. The copilot drafts a grounded reply that Karim approves, edits or escalates — nothing reaches the customer without him.

## 2. Workflow — four steps, in this order
1. **Route** — classify the ticket text into `how_do_i | payroll | billing | other`, with a confidence score. Rung 2: TF-IDF + logistic regression trained on `data/tickets_synthetic.csv`.
2. **Routing rule** — rung 1. `draft` only if category is `how_do_i` **and** confidence ≥ 0.70 **and** the text contains none of: `refund`, `price`, `pricing`, `invoice`, `subscription`, `discount`; otherwise `escalate`. `payroll`, `billing`, `other` are human-only.
3. **Retrieve + draft** — rung 3. Retrieval: split every `kb/*.md` into chunks by `## ` heading; TF-IDF cosine similarity; keep the top 3 chunks with score ≥ 0.05. Draft: a reply that uses **only** the retrieved chunks and cites each one as `[KB-xxx · Section]`. If `ANTHROPIC_API_KEY` is set, call the model with that instruction; otherwise use a **template drafter** (first sentence of the top chunk + citation) — same contract.
4. **Policy check** — rung 1. Block the draft if it matches: a price or currency amount, "refund", "credit note", "legal"/"lawyer"/"court". A blocked draft is shown with its reason and is not approvable.

## 3. Contracts
- Input: `{id, text}`.
- Output: `{category, confidence, decision: draft|escalate, draft_text|NO_DRAFT, citations: [{article, section, score}], policy: pass|block, reason}`.

## 4. Edge cases
- A ticket in French: treated like any other ticket in v0 (no translation).
- A ticket with two questions: answer the first retrieved topic only; say so in the draft.
- A ticket that mentions a refund or a price: must end as `escalate` or `block`.

## 5. Fallbacks
- No chunk above 0.05 → `NO_DRAFT`, decision `escalate`.
- Confidence < 0.70 → `escalate`, with the category shown to the agent.
- Model/API error → template drafter.

## 6. Surface (Streamlit, one file)
- **Inbox** page: list of eval tickets; selected ticket shows category + confidence, the draft, its citations, the policy line, and three buttons: *Approve & send*, *Edit*, *Escalate*. Buttons do nothing in v0 except show a toast. Caption on every draft: "Trust level L2 — nothing is sent until you approve."
- **Eval** page: runs §7 and shows the table and the headline number.

## 7. Evaluation (`evals/tickets_v0.csv`, 25 rows — never tune while looking at it)
- Columns: `id, text, expected_category, expected_outcome, expected_article, expected_section, language`.
- Metrics to print:
  - **routing accuracy** = share of rows where `category == expected_category`
  - **retrieval hit@3** = share of `draft`-expected rows whose `expected_article` is among the 3 citations
  - **sendable as is** (the proxy for two graders) = share of **how_do_i** rows where decision is `draft`, the draft cites `expected_article · expected_section`, and policy is `pass`
  - **drafts on human-only** = count of `escalate`-expected rows that got a draft (must be 0)
  - **policy blocks**
- Print the three most frequent miss causes (group by `expected_section` of the misses).

## 8. Definition of done
**At least 45 % of "how do I" tickets sendable as is, and zero drafts on human-only tickets.** Below that: do not fix the prompt — list the misses by cause and propose the change to this spec.

## 9. Out of scope (v0)
Login, database, customer-facing widget, fine-tuning, languages other than what the KB covers, any category other than `how_do_i` getting a draft.

## 10. Files
```
data/tickets_synthetic.csv   training data (synthetic)
kb/KB-214.md KB-301.md KB-318.md
evals/tickets_v0.csv         evaluation set (frozen)
prototype/                   ← build here: router.py route_rule.py retrieve.py draft.py policy.py evals.py app.py
```
Run: `python prototype/evals.py` · `streamlit run prototype/app.py`
