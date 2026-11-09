# 03 — AI Lean Canvas · LabelFlow refund agent

Group 5 · Raveloarimanga Rajesy Ny Andrian · Clémence Marco · 8 November 2026
Every box reuses `01_problem_statement.md` or `02_sizing.xlsx`. Source types are carried over, not re-invented.

## 1. Problem

Shipping-label refund requests under €20 cost more to process (~€5/ticket, *analogy*) than the amount refunded, and merchants wait ~3 days (*measured*). ~7,500 refund requests a month, of which ~65 % under €20 (*guess — the unmeasured number that moves the whole case*). The root cause is not volume: the eligibility decision was never codified, so a human cross-references a long policy against a separate tracking system, every time.

## 2. Customer segments

Primary: LabelFlow tier-1 support agents (the people doing the 9 minutes). Secondary: the 15,000 merchants waiting three days. Early adopter segment: merchants on the standard plan shipping under 500 parcels a month, where sub-€20 claims concentrate.

## 3. Unique value proposition

A refund decision in under an hour instead of three days, with a receipt that names the policy clause and the tracking evidence it rests on — so the merchant knows why, and LabelFlow can prove why.

## 4. Solution

An agent with three tools (read policy · read tracking · execute refund) and four outcomes (refund · prepare for approval · recommend only · refuse with a reason), bounded by an amount: L4 under €20, L2 from €20 to €100, L1 above €100. Deterministic rules hold the ceiling and the evidence gate; a pretrained model handles the ambiguous slice and writes the receipt.

## 5. What the AI must predict or generate

Not a prediction of merchant behaviour. Two things only: **which policy clause applies to this case given this tracking evidence**, and **a receipt a merchant can read and an auditor can check**. Everything else in the flow is a rule.

## 6. Data

| | |
|---|---|
| **Sources** | Refund policy text (internal, versioned) · carrier tracking events (structured, hourly) · historical refund tickets with outcomes (~7,500/month) |
| **Volume & labels** | Outcomes are recorded; **the reasoning is not labelled**. This is the real gap: we can see what was decided, not why. |
| **Coverage** | Predominantly FR/EN policy and tickets against a wider merchant base — the known gap by segment |
| **Rights** | GDPR art. 6(1)(b) for the decision, art. 6(1)(f) for the audit log. Never real customer data in the eval-set. |
| **Leakage** | Split by merchant, not by ticket: the same merchant's earlier case can otherwise appear in both train and test |
| **Freshness** | Tracking fresh to the hour; policy versioned — a retired clause cited is a defect, not a drift |

## 7. Key metrics

**Primary:** share of automatable sub-€20 requests decided as a trained agent would decide them (threshold 55 %, from `02_sizing.xlsx` Inputs row 22).
**Counter-metric 1:** over-refund rate — money leaving without a valid claim.
**Counter-metric 2:** wrongful-refusal rate — refusals overturned after a merchant disputes them.
**Business:** refund cost per case (processing + leakage), target −50 %; time to resolution, target < 1 hour.

## 8. Cost structure *(from `02_sizing.xlsx`)*

€164k a year of fixed lines at base — integration amortised (€37k), evaluation (€35k), one supervision FTE (€48k), monitoring (€20k), re-evaluation at model changes (€24k) — against €43k of net variable contribution in year 1. Tokens are the smallest line (~€1.2k); the human in the loop is the largest.

## 9. Revenue / value capture

Internal cost avoided, not revenue: €3.38 net per deflected ticket, 12,592 tickets in year 1. Plus a small, deliberately under-claimed retention line (€12k, *guess*) from faster refunds.

## 10. Unfair advantage

The refund policy and the tracking history are LabelFlow's, and so is the decision receipt. A competitor can rent the same model; it cannot rent fifteen thousand merchants' refund history or the policy the decisions are made against. This is also why Assignment 2 recommends orchestrating rather than buying outright.

## 11. Channels

Inside the existing support console, as a decision panel on the ticket the agent already has open. No new surface, no new login, no new habit.

## 12. Risk and governance line

The agent can lose money silently (over-refund) or lose merchants silently (wrongful refusal). Neither generates a complaint, so neither is caught by listening to customers — which is why the control is a euro amount on a rolling 7-day window (€2,000) and a daily reconciliation, not a satisfaction score. Liability stays with LabelFlow whatever the architecture (*Moffatt v. Air Canada*, 2024 BCCRT 149).

## 13. The one assumption that decides everything

That at least 55 % of automatable sub-€20 cases can be decided from policy text plus tracking data alone, well enough that two graders would execute the decision unedited. Tested on 200 historical tickets with the Session 4 prototype.

**And the one Assignment 2 added:** that in-scope volume is large enough to carry the fixed costs. It is not, at refund-only scope — 12,592 deflected tickets a year against a break-even of 50,000–63,000. The agent passing its threshold and the project being worth building are two different questions, and only the first is settled by the prototype.
