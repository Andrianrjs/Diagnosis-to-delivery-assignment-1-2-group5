# LabelFlow refund agent — Group 5

**Team:** Raveloarimanga Rajesy Ny Andrian (Git: Andrianrjs) · Clémence Marco (Git: clemencemarco-prog)

**Company:** LabelFlow — a SaaS platform for e-commerce logistics (shipping labels + returns).
15,000 merchants, 25,000 tickets/month, 30 % about shipping-label refunds.

**The agent's job, in one sentence:** When a merchant requests a refund for a shipping label,
the agent checks eligibility against the refund policy and the package-tracking evidence,
then settles, prepares or recommends the refund according to its amount, producing a
decision receipt (policy clause, evidence, amount) that is both the merchant's answer and
the audit log.

**Trust level per step:**

| Step | Level | What it means |
| --- | --- | --- |
| Read policy + tracking evidence | L4 | Autonomous, read-only, no money moves |
| Refund under €20 | L4 | Acts alone; a human reviews a sample weekly |
| Refund €20–100 | L2 | Prepares the decision; a human approves before execution |
| Refund over €100 | L1 | Recommends only; the human decides |
| Refuse a refund (any amount) | L2 | Prepared by the agent, confirmed by a human |

**What it must never do:** refund without package-tracking evidence, or refund more than
€20 on its own.

**Rollback:** if refunded amounts exceed the pre-agent baseline by more than €1,500 over
7 days (or any refund goes out without tracking evidence), every case drops to L2 —
the agent prepares, a human approves.

## Files

| File | Content |
| --- | --- |
| `01_problem_statement.md` | Assignment 1 — problem, 5 Whys, AI fit, selection check, press release, hypotheses, do-nothing baseline |
| `governance.md` | Assignments 1–4 — the six governance questions, trust levels, rollback; Session 2 cost-of-error line; Session 4 checkpoints, switch, eval data |
| `02_sizing.xlsx` | Assignment 2 — sizing model |
| `02_investment_memo.md` | Assignment 2 — investment memo (build / buy / orchestrate) |
| `03_product_brief.md` · `03_ai_lean_canvas.md` · `03_user_research.md` · `03_prototype_link.md` | Assignment 3 — product brief, lean canvas, user research, clickable preview |
| `spec.md` | Assignment 4 — spec v2 (after eval-v0); §11 lists every eval miss and the change it caused |
| `kb/refund_policy.md` | The refund policy the agent reads, one clause per heading (invented: LabelFlow is a case) |
| `prototype/` | Assignment 4 — rules-only prototype: `router` → `route_rule` → `retrieve` → `decide` → `policy`; `evals.py`; `app.py` (optional Streamlit) |
| `evals/` | Eval-set (50 cases), eval README, `results_v0.csv`, `report_v0.md` (95 % vs 55 %, FAIL on EV-050) |
| `04_architecture.md` | Assignment 4 — diagram, components, workflow vs agent, fallbacks, switch, data, eval result |
| `05_metrics.md` | Assignment 5 — to do |
| `course/` | Course instructions (Sessions 4 and 5), for reference |
| `paylo-copilot-demo/` | The instructor's Paylio demo, kept for reference only — not our prototype |

Run the eval from the repo root: `python3 prototype/evals.py`