# 03 — Product brief · LabelFlow refund agent · v2

**Team:** Raveloarimanga Rajesy Ny Andrian · Clémence Marco (group 5) · **Starting point:** P4 · **Version:** v2 — 8 November 2026
Built from `01_problem_statement.md` and `02_investment_memo.md`. Nothing here is invented where those files already answer it.

## 1. Problem, user, do-nothing *(from 01)*

- **Problem in one sentence:** Support agents at LabelFlow, a B2B e-commerce logistics SaaS (15,000 merchants, 25,000 tickets/month, of which ~7,500 are shipping-label refund requests), manually process refunds that are often under €20 — cases where the processing cost (~€5/ticket) exceeds the amount refunded; today each request waits ~3 days and is handled by a human.
- **User (persona):** Tier-1 support agent at LabelFlow — goal: close the refund queue without giving money away — pain: cross-referencing a long refund policy against a separate tracking system, hundreds of times a week, for amounts smaller than the time it takes.
- **Do-nothing baseline:** ~3-day wait, every case routed to a human. Not zero: `02_sizing.xlsx` prices the current process improving on its own at **+€60k a year** (2–5 % efficiency gain, analogy), against ~€29k of extra cost from volume growth.

## 2. The process — as-is and to-be

| # | Step | Who today | Min | Error rate | Cost of an error | Automate / augment / keep human (test it fails) | Trust level | Min after | Metric for this step |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Merchant files the refund request | Merchant | — | — | — | Keep human — it is the trigger, not work we own | person only | — | Requests per merchant per week (splitting signal) |
| 2 | Ticket triaged into the refund queue | Agent | 1 | 5 % mis-routed *(guess)* | €5 re-route | **Automate** — fails no test: bounded, labelled, feedback immediate | L4 | 0 | Mis-routing rate |
| 3 | Open the refund policy, find the applicable clause | Agent | 3 | 8 % wrong clause *(guess)* | €25 | **Automate** — fails test 6 (no clear right answer) only on policy exceptions, which route to step 6 | L4 under €20 · L2 above | 0 | Share of decisions citing the clause a grader would cite |
| 4 | Open the tracking system, check the parcel | Agent | 2 | 4 % misread *(guess)* | €25 | **Automate** — structured carrier events, fails none of the eight tests | L4 | 0 | Evidence-retrieval success rate |
| 5 | Decide and write the reply | Agent | 2 | 6 % wrong decision *(analogy, to be replaced by the eval-set)* | €25 under €20 · €55 in the €20–100 band | **Automate under €20, augment above** — above €20 it fails test 3 (the cost of an error is not bounded by a small amount) | L4 < €20 · L2 €20–100 · L1 > €100 | 0.3 (sampling) | Decision-match rate against a trained agent |
| 6 | Execute the refund in billing | Agent | 1 | 2 % wrong amount *(guess)* | €55 | **Automate under the threshold** — money moves, so the threshold is the control, not the model | L4 < €20 · person above | 0 | Over-refund rate (€ per week vs baseline) |
| 7 | Cases the agent cannot decide | — | — | — | — | **Keep human** — "I don't know" is a valid, logged outcome | person only | +0.9 | Unknown rate (a product signal, not a failure) |

**Total agent time:** ~9 minutes today → **~1.2 minutes after**, averaged across settled and escalated cases. Consistent with the ~€5/ticket in `01` (≈ €0.35 of agent time per minute).

**Where the pain sits (the two steps):** **step 3** (policy lookup, 3 min) and **step 4** (tracking lookup, 2 min). Together they are 5 of the 9 minutes, and they are exactly the root cause named in `01`: the eligibility decision was never codified, and policy and tracking live in two systems that nothing links.

**The way back to a person (designed first):** every decision carries a one-click escalation that routes to a human with the full case already assembled — request, policy clause considered, tracking evidence retrieved — so the hand-off saves work instead of duplicating it. The merchant is told the decision was automated. No case is ever closed without that route being present.

**Where the governance line sits:** at €20. Below it the agent acts alone and a human reviews a sample weekly; above it a human approves before any money moves. The line is an amount, not a confidence score, because an amount is auditable and a confidence score is not.

## 3. Features — RICE and MoSCoW

Reach = sub-€20 refund requests per month from `02_sizing.xlsx` (4,875), or the affected sub-population.

| Feature | Reach / month | Impact | Confidence | Effort (p-wk) | RICE | MoSCoW |
|---|---|---|---|---|---|---|
| Tracking-evidence gate (never decide without it) | 4,875 | 2 | 100 % | 1 | **9,750** | MUST |
| Decision receipt (clause, evidence, amount) | 4,875 | 1.5 | 100 % | 2 | **3,656** | MUST |
| Eligibility decision engine (policy × tracking) | 4,875 | 3 | 80 % | 6 | **1,950** | MUST |
| One-click escalation to a human | 500 | 3 | 100 % | 1 | **1,500** | MUST |
| Auto-refund above €20 | 2,625 | 3 | 50 % | 4 | 984 | WON'T |
| Daily reconciliation of refunded amounts | 4,875 | 0.5 | 80 % | 2 | 975 | SHOULD |
| L2 approval queue for the €20–100 band | 1,875 | 1 | 80 % | 3 | 500 | SHOULD |
| Merchant-facing refund status page | 7,500 | 0.5 | 50 % | 4 | 469 | COULD |
| Proactive refund detection (before the merchant asks) | 1,000 | 2 | 50 % | 7 | 143 | WON'T |
| Multilingual decision receipts | 1,500 | 0.5 | 50 % | 5 | 75 | WON'T |
| Carrier-dispute auto-filing | 800 | 1 | 50 % | 8 | 50 | WON'T |
| Bulk refund handling | 300 | 1 | 80 % | 5 | 48 | WON'T |

- **MUST (4):** tracking-evidence gate · decision receipt · eligibility decision engine · one-click escalation
- **SHOULD:** daily reconciliation · L2 approval queue
- **COULD:** merchant-facing refund status page
- **WON'T this time (5) — the out-of-scope list, dated 8 Nov 2026:** auto-refund above €20 · proactive refund detection · multilingual receipts · carrier-dispute auto-filing · bulk refund handling

**The feature that tests our flip assumption, and why it is a MUST:** the **decision receipt**. Its RICE (3,656) is below the tracking gate's, and on its own it deflects no ticket at all — it is pure overhead in deflection terms. It is a MUST because the flip assumption is not "does the agent answer" but "does the agent decide what a trained agent would have decided on the same evidence", and that is unmeasurable without a record of the clause applied and the evidence used. Without the receipt there is no eval-set, no grading, and no way to pass or fail the threshold in section 7. It is also the artefact the whole governance case rests on (*Moffatt v. Air Canada*, 2024 BCCRT 149).

**The cut that hurt the most:** auto-refund above €20 (RICE 984, above two of our SHOULDs). It is the single largest block of value left on the table — 2,625 requests a month — and we cut it on governance grounds, not product grounds: `governance.md` sets €20 as an absolute ceiling on the agent's own authority, and an over-refund above that line is not recoverable case by case.

## 4. Data *(six-question audit in full in `governance.md`)*

Three sources: the refund policy text (internal, versioned, current), carrier tracking events (structured, via carrier APIs, fresh to the hour), and historical refund tickets with their outcomes (~7,500/month, outcome recorded but **not labelled with the reasoning** — the gap that matters). Coverage is the open risk: policy and tickets are predominantly in French and English, while LabelFlow's merchant base is wider. Legal basis is performance of the contract (GDPR art. 6(1)(b)) for the decision itself and legitimate interest (art. 6(1)(f)) for the audit log. Leakage risk is real and specific: the same merchant's earlier ticket can appear in both train and test, so splits are by merchant, not by ticket.

## 5. Model — one rung per part

| Part | Rung | Why the rung below fails |
|---|---|---|
| Triage into the refund queue | **1 — rules** | Nothing below rules. Keyword and metadata routing already works; a model here would be over-engineering. |
| Tracking-evidence retrieval | **1 — rules** | Carrier events are structured. Classical ML would add variance to a lookup that is deterministic. |
| Clear-cut eligibility (amount + window + delivery confirmed) | **1 — rules** | Nothing below rules, and this is the ~70 % the agent must *not* use a model for. A rule is auditable; a model is not. |
| Ambiguous eligibility (policy exceptions, non-standard evidence) | **3 — pretrained model** | Rules fail: the exception space is long-tailed and written in prose. Classical ML fails: there are no labels for the *reasoning*, only for the outcome. |
| Decision receipt writing | **3 — pretrained model** | Templates fail on the ambiguous slice — the clause and the evidence vary per case, and a template that cannot say why produces a receipt nobody can audit. |
| Orchestration (which tool, which trust level, when to stop) | **4 — hybrid** | A pure model fails: the €20 ceiling and the evidence gate must hold deterministically, not probabilistically. Rules alone fail: they cannot decide when a case is ambiguous enough to escalate. |

## 6. Where it lives (integration surface)

Inside the existing support console, as a decision panel on the refund ticket the agent already has open — no new tool to learn. Speed: under 30 seconds per decision, because the agent is waiting on it. Format: the decision receipt (clause, evidence, amount, trust level) plus an Execute / Escalate pair of buttons. Fallback: if the tracking API or the policy index is unavailable, the agent returns "cannot decide — evidence unavailable" and the ticket routes to the human queue unchanged; it never decides on partial evidence. Who sees the log: Support Operations daily, Finance monthly in the reconciliation, Legal on any dispute.

## 7. Success criterion — one sentence

> By **30 January 2027**, on our **200-case eval-set** (v0 of 20 cases committed with this brief), at least **55 % of automatable sub-€20 refund requests — about 38 % of all sub-€20 requests — receive a decision that two graders would execute without editing**, and **no decision executes a refund without tracking evidence attached to its receipt**.

The 55 % is the Base deflection assumption on category 1 in `02_sizing.xlsx` (Inputs row 22), which the sensitivity table on the Decision tab varies from 30 % to 75 %. The 38 % is 0.70 × 0.55 — the automatable share times the deflection rate.

**One honest caveat, carried from Assignment 2.** The sensitivity table reads "below do-nothing" at *every* deflection rate from 30 % to 75 %, so hitting 55 % does not by itself make the project worth building. What flips our case is in-scope volume (50,000–63,000 deflected tickets a year against 12,592 at base), not agent quality. The 55 % is the right threshold for the *prototype* — it tells us whether the agent works at all, and therefore whether orchestrating with a vendor is viable — but the investment decision turns on scope. We state this rather than quietly reusing a threshold that no longer decides anything.

## 8. Risks and rollback trigger

- **Over-refunding, silently.** Nobody opens a ticket to complain about being paid. This is the failure mode the daily reconciliation exists to catch.
- **Merchants learning the €20 line** and splitting requests under it.
- **Policy drift** — the refund policy changes and the agent keeps citing a retired clause.
- **A wrongful refusal pattern** that shows up as churn months later, not as complaints.
- **Rollback trigger (one line):** if the refunded amount over a rolling 7 days exceeds the pre-agent baseline by more than **€2,000** (~15 % of a normal week's sub-€20 refunds), every case drops to L2 automatically — the agent prepares, a person approves. Rollback is a downgrade, not a shutdown: switching the agent off returns the queue to a three-day wait.

---

## 9. What the users changed

> **PENDING — the design loop has not been run.** This section is filled only from real conversations and one usability test, per the assignment's explicit rule. See `03_user_research.md` for the guide, the task and the empty evidence tables, which are ready to run.

| Change | Evidence (who said / did what) |
|---|---|
| | |

## 10. What they could not decide

> **PENDING for the same reason.** The questions we already know users cannot settle for us, and who settles them instead: the €20 threshold (Finance and Legal, from the three-month refund-amount export), the EU AI Act risk tier (Legal), and the retention period for decision receipts (Finance and Legal). Users can tell us whether the receipt is readable; they cannot tell us where the money line sits.
