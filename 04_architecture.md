# 04 · Architecture — <team name> · <agent name>

> Session 4 deliverable. Due **6 November** in your repo as `04_architecture.md`, with `spec.md` v2 and `evals/tickets_v0.csv` (50 rows).
> Describe the prototype you actually built, not the one you plan. Every line must match something in `/prototype`.

## 1. One-line description
*What the system does, for whom, with what output.*
Ex.: "A copilot that drafts replies to 'how do I' tickets for Paylio's tier-1 agents; the agent approves before sending."

## 2. The diagram
Draw the flow with boxes and arrows (image, Mermaid, or ASCII). Mark every human checkpoint with **⊘** and the override switch with **⏻**.

```
ticket ──▶ [1 router] ──▶ [2 routing rule] ──▶ [3 retrieve + draft] ──▶ [4 policy check] ──▶ ⊘ agent approves ──▶ sent
                                   │ low confidence / human-only                 │ block
                                   └──────────────────────▶ escalate to a person ◀┘
⏻ switch: <who can turn the copilot off, how, for whom>
```

## 3. Component table
| # | Component | Rung (1 rules · 2 classical ML · 3 pretrained model · 4 custom) | Pattern (chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer · agent) | Trust level (L1–L4) | Checkpoint ⊘ (approval · abstention · sampling · none) | Metric observed |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |

## 4. Workflow or agent?
*One paragraph.* Can you draw the path in advance (workflow), or does the model decide its own steps and tools (agent)? Why is that the right choice for your risk level? What would have to be true to move one step up?

## 5. Fallbacks
What happens when… (one line each)
- retrieval finds nothing:
- the model's confidence is below the threshold:
- the policy checker blocks the draft:
- the API is down:

## 6. The override switch ⏻
- Who can switch it off:
- Scope (one ticket · one user · everyone):
- Tested on (date, by whom):

## 7. Data
- Training / demo data (`data/`): what it is, where it comes from, synthetic or real
- Evaluation data (`evals/eval_set_v0.csv`): how many cases, who labelled them, **never used for tuning**
- Personal data present? Where is it stored, who can see it (link to `governance.md`)

## 8. Eval result v0
Copy the headline from `evals/report_v0.md`: *"<N> % of 'how do I' tickets got a draft two graders would send without editing — criterion was <X> %."*

## 9. What you would build next (3 lines max)
