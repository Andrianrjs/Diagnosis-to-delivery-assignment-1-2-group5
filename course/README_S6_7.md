# S6_7_templates — what to copy into your repo

| File | Where | Due |
|---|---|---|
| `06_07_experiments_operations.md` | repo root | 23 Nov (then `08_launch_memo.md` and tag `v1.0` on 26 Nov) |
| `evals/sample_size.xlsx` | `evals/` | optional — three yellow cells if you want the number |
| `governance_lines_S6_7.md` | copy the three lines into `governance.md` | 23 Nov |

**Logging in ten lines.** Langfuse: `pip install langfuse`, set the three keys from your free cloud project in `.env`, decorate your four steps with `@observe()` — one trace per draft appears in the Langfuse UI. OpenTelemetry directly: `opentelemetry-sdk` + `opentelemetry-instrumentation-fastapi`, export to Phoenix (`pip install arize-phoenix`, `phoenix serve`). Both docs have a FastAPI quick-start; copy it.

Rules: every number traces to `02_sizing.xlsx`, `05_metrics.md` or `evals/report_v0.md`; every owner is a named role; every threshold has a clock. Hosting options are on slide 19 (your laptop + tunnel for the demo; Render, Hugging Face Spaces, Vercel, Cloud Run for a pilot); the tools by layer on slide 16; the trace on slide 21; the dashboard on slide 22.

**The calculator** (`evals/sample_size.xlsx`): sheet *Proportions* for a rate (closed within an hour, resolved, approved…), sheet *Means* for an average (minutes, CSAT). Change the yellow cells only: where you are today · the smallest rise that matters · your volume per week. Read units per group and weeks. The two risks (false win 1 in 20, missed win 1 in 5) are preset — leave them.

## Six questions, one worked example per project

You are not graded on the statistics. The six questions of slide 13 — a comparison group · the unit · the smallest gain that matters · the slowest guardrail · the decision rule written before · the plan B when you cannot randomise — answered in words, are what the oral asks. Below, one worked example per project — the four columns are the headings of §1–§2 of the file.

Numbers are illustrative: replace them with yours. "n" is units per group from the calculator.

| Project | 1 · What do we claim? | 2 · What do we randomise? | 3 · How long? | 4 · Decision rule |
|---|---|---|---|---|
| **P1 HR & payroll deflection** | widget questions resolved without a ticket: 25 % → 35 % within 7 days | the question (independent; nobody learns from it) · A/B on questions | 25 % · +10 pts · 2,000 questions/week → n ≈ 330, under a week; read at 2 weeks so the 7-day tickets have arrived | ship if ≥ +10 and escalations flat; stop if one wrong payroll figure is quoted |
| **P2 fintech agent-assist** | handling time of a payment ticket: 12 min → 8 min | the ticket; agents learn from the drafts, so also watch the control tickets | sheet *Means*: spread 6 min · −2 min · 800 tickets/week → n ≈ 142, one week; run 2 | ship if −2 min and wrong-transaction links ≤ 1 %; stop on one wrong confirmation sent to a customer |
| **P3 incident communicator** | time to first status update: 25 min → 10 min | the incident — but there are ~8 a month: too few to randomise | n ≈ 16 incidents per group = months. So: shadow mode on the last 20 incidents, then before/after with the other product line as control | adopt if median ≤ 10 min on 10 incidents and zero incorrect status published |
| **P4 refund agent** | small refunds (< 20 €) decided within 5 min: 10 % → 60 % | the refund request · A/B on requests, then a 5 % holdout | the effect is huge (n ≈ 15), the **guardrail** sets the duration: to see wrong approvals go from 1 % to 3 % you need ≈ 770 approvals per group → 4 weeks at 400 requests/week | ship if ≥ +40 pts and complaints flat; stop if wrong refunds > X €/day |
| **P5 multilingual LMS support** | first-contact resolution of non-English tickets: 55 % → 65 % | the ticket · A/B on non-English tickets, segments = languages, pre-registered | 55 % · +10 pts · 300 non-English tickets/week → n ≈ 377, 3 weeks; read at 4 | ship if ≥ +10 and CSAT per language ≥ baseline − 0.1; stop for a language whose reopen rate is 1.5× the others |
| **P6 churn-prevention** | 30-day churn among flagged accounts: 20 % → 15 % | the **account**, not the chat — one account chats several times (leak) · A/B on accounts | 20 % · −5 pts · 200 flagged accounts/week → n ≈ 907 = 9 weeks. Too long: use a proxy read at week 3 (retention offer accepted) and the churn read at week 9 | ship if churn −5 pts and cost per saved account < X; cap the offers given to accounts that were not leaving |
| **P7 SLA-aware prioritisation** | P1 tickets acknowledged within SLA: 80 % → 95 % | not the ticket — re-ordering a queue changes every other ticket's wait (interference). Randomise **days** (alternate) or **teams** | 80 % · +15 pts → n ≈ 77 P1 tickets per group; at 20 P1/week that is 8 weeks → run 4 and accept you only see a large effect | ship if SLA hit ≥ 95 % on P1 and P3 waiting time not up more than 10 %; stop on one P1 classified P3 |
| **P8 voice-of-customer synthesis** | hotels that act on a theme within 30 days: 20 % → 40 % | the hotel (account) · A/B on hotels: half receive the synthesis this quarter | 20 % · +20 pts → n ≈ 83 hotels per group; with 300 hotels, one quarter | adopt if ≥ +20 pts and no factual error in the sampled reports; stop on one quote attributed to the wrong review |
| **Your own project** | an outcome that exists with and without the agent, from, to, by when, without… | the smallest unit that does not leak the treatment | three yellow cells → weeks; if too long, say so and choose before/after with control | written before the first unit; the harm that stops early |

Three patterns to recognise: **few units** (P3, P8) → months, so shadow mode and before/after; **huge effect** (P4) → the guardrail decides the duration, not the effect; **interference** (P6, P7) → randomise the account, the day or the team, and wait longer.
