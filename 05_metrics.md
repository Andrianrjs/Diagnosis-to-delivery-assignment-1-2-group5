# 05 · Metrics · Group 5 · LabelFlow refund agent

> Session 5 deliverable. Five sections, the five moves of the session. Every number traces to `02_sizing.xlsx` (sheet and cell given) or to `evals/report_v0.md` and its receipts `evals/results_v0.csv` (prototype tag `eval-v0`, run of 17 November 2026). Where a figure is derived, the arithmetic is written next to it. No new number appears here.

**Read this first.** The headline of `report_v0` (95 %, 19/20) is **not** our deflection rate. Under `governance.md` §3, every refusal is confirmed by a person (L2), so the agent settles alone only the refunds under €20. On the 20 automatable sub-€20 held-out cases, 11 are refunds and all 11 were settled correctly at L4: **11/20 = 55 % settled alone**, which is exactly the base deflection of the sizing (`Inputs!D22`). The eval therefore confirms the sizing base case; it does not improve it. And the sizing base case is a NO-GO (`Decision!D27`): no metric below changes that, only in-scope volume does (`02_investment_memo.md`).

## 1 · Place the number · the stack for our agent

There is no model in v0: level 1 measures the rule components (`decide.py`, `retrieve.py`).

| Level | Question | Our metric | Value today (or "not yet") | Produced by | Owner | Clock |
|---|---|---|---|---|---|---|
| 5 Business | does it move the P&L? | variable cost per sub-€20 refund request · refund leakage vs pre-agent baseline · churn of merchants after a refund request | not yet · baseline €7 per request (`Inputs!D9`), 30 merchants a year lost over the 3-day wait (`Inputs!G67`) | production monitoring + finance reconciliation, monthly | Finance (`governance.md` §4) | months |
| 4 Product | does the user adopt it and get the job done? | share of sub-€20 refund requests settled at L4 and not reopened, disputed or reversed within 7 days (the primary, §3) | not yet · offline proxy: 11/20 settled alone on held-out | online A/B (S6), then monitoring, weekly | agent product owner | weeks |
| 3 Guardrails & responsible AI | does it stay inside the lines, for everyone? | refunds without evidence · refunds ≥ €20 alone · decisions on human-only cases · all by language and plan | 0 · 0 · **1 (EV-050), floor broken** | offline eval-set + adversarial rows each release, then monitoring | Head of Support Operations, with Legal | days |
| 2 AI system | does the workflow complete the task? | executable as is (automatable sub-€20, held-out) · hand-over rate | **19/20 = 95 %** (criterion 55 %) · 27 % | eval-set + two graders (grader columns still empty: today the figure is the automated proxy, `report_v0` §3) | agent product owner | hours |
| 1 Model (rule components) | is the component right? | decision accuracy · clause accuracy (decided cases) | 97 % · 96 % (held-out) | offline eval-set, every commit | prototype builder | seconds |

Read bottom-up, each arrow is a hypothesis S6 tests: 96 % clause accuracy → 95 % executable → 55 % settled alone → 38.5 % of all sub-€20 requests with no human touch (0.70 automatable × 0.55, `Inputs!D18 × D22`) → €7 to €4.9 per request (§4). Read top-down, the business number moves last, and today it says NO-GO.

## 2 · Decide when to stop · the stop criterion

*We stop improving executable-as-is at **95 % (19/20)** because the level-4 metric, the share settled alone, no longer responds: the only miss (EV-031) is a refusal, which a person confirms at L2 whatever the agent cites, so fixing it adds no settled case. Above level 4, the sizing is flat: net value stays below do-nothing at every deflection from 30 % to 75 % (`Decision!A32:E36`), and one point of deflection is worth about **€1.0k a year** (−€109.5k at 30 % to −€63.5k at 75 %, i.e. €46.1k over 45 points). The next point would cost a fresh held-out slice written by someone who has not read the rules (EV-021 to EV-050 are now read), paid from an evaluation line of **€35k a year** (`Inputs!D51`).* This is the "flat" case of the session: the bottleneck is volume in scope, not the agent.

- **Component metric and value:** executable as is, 95 % (19/20, held-out); clause accuracy 96 %.
- **The level-above metric that stops responding:** share settled alone at L4, capped by governance at the refund share of the traffic (11/20 on held-out); and net annual value, below do-nothing at every deflection rate tested.
- **Cost of the next point:** labelling a fresh held-out slice (part of the €35k a year evaluation line) for ≈ €1.0k a year of value per point of deflection.
- **What is a floor, not a stop (any miss blocks the release):** zero refunds without tracking evidence, zero refunds ≥ €20 settled alone, **zero decisions on human-only cases**. The third is broken today (EV-050): the stop applies to the percentage, the release stays blocked until `spec.md` v2 passes a fresh slice.

## 3 · Choose what to protect · the hierarchy, by segment

| Kind | Metric | Numerator / denominator | Level | Lag | Source & owner |
|---|---|---|---|---|---|
| Primary (1) | Settled alone and uncontested | sub-€20 requests refunded at L4 and not reopened, disputed or reversed within 7 days / **all** sub-€20 refund requests received (not only the automatable ones, so escalating hard cases cannot inflate it). Expected 38.5 % at steady state | 4 | 7 days | receipt log + ticket system · agent product owner |
| Guardrail (3) | Hard invariants | refunds executed without tracking evidence, plus refunds ≥ €20 settled alone / all receipts. Must be 0 (eval-v0: 0 and 0) | 3 | seconds (`policy.py`), then daily | receipt log · Head of Support Operations |
| Guardrail | Correct abstention | human-only cases that received a decision / human-only cases. Must be 0 (eval-v0: 1 of 6 held-out, EV-050). In production: L4 decisions the weekly sample marks "should have gone to a person" | 2–3 | hours (eval) · 1 week (sample) | eval-set + weekly sample · agent product owner |
| Guardrail | A person reached | handed-over or escalated cases answered by a person within today's queue time (~3 days, `Inputs!G67`) / handed-over or escalated cases. No worse than today (`governance.md` §6). Hand-over rate on eval-v0: 27 % | 4 | 3 days | ticket system · Head of Support Operations |
| Counter-metric (2) | Refund leakage (silent over-refund) | € refunded on agent-settled cases minus the pre-agent baseline, rolling 7 days; band ≤ €1.5k (`Decision!D6` €79.7k ÷ 52 weeks), the trigger already in `governance.md` §6 | 5 | 1 week, truth at the monthly reconciliation | daily reconciliation · Finance |
| Counter-metric | Wrongful refusals and the churn behind them | refusals overturned after a dispute / refusals sent; and 90-day churn of merchants who received a refusal | 4–5 | weeks · 90 days | dispute log + billing · Head of Support Operations, with Legal |

- **Segments reported** (S3 audit, columns of the eval-set): **language** (FR · EN · other), **plan** (standard · high-volume · enterprise), **amount band** (< €20 · €20–100 · > €100), **carrier status** (NO_SCAN · IN_TRANSIT · DELIVERED · RETURNED_TO_SENDER). On eval-v0 held-out the counts are too small to compare rates (FR 7/7 executable but the one human-only miss, EV-050, is French; EN standard 9/10; high-volume 3/3; DE 0 decided, by design), so v1 is stratified to have enough cases per segment (§5).
- **Fairness metric, named:** **selection-rate parity** by language and plan (share of requests settled at L4), read together with **equal error rates** (wrongful-refusal rate and decided-on-human-only rate by segment). One gap is known and chosen: merchants writing in a language other than FR or EN are never decided (`language_not_covered`), so their selection rate is 0 by design. We report it rather than hide it, and their guardrail is "a person reached".
- **Harm threshold that stops the rollout, and its owner** *(the line to copy into `governance.md`)*: **"If, on any language or plan segment, the wrongful-refusal rate exceeds that segment's pre-agent human rate, or the abstention guardrail records a decided human-only case, over two consecutive weeks, the agent drops to L2 (prepare only) on that segment until the gap is explained. Owner: Head of Support Operations; reviewed with Legal monthly."** Note: v0 has no per-segment switch (`04_architecture.md` §6), so this line needs one in `spec.md`.
- **How it could be gamed → the repair.** (1) The primary rises if borderline cases are refunded: a merchant who is paid never reopens, so "not reopened" is blind to over-refunds → the leakage counter-metric and the daily reconciliation. (2) Merchants learn the €20 line and split requests → requests and refunded € per merchant per week; eval-v0 already raised the split flag on M-6028 and M-1042. (3) The primary falls to protect the guardrails if everything is escalated → the denominator is all sub-€20 requests, and "a person reached" shows the cost of escalation.

## 4 · Derive the business metrics · three, with expected effects (the oral)

| Business metric | Baseline (from `02_sizing.xlsx`) | Expected effect (`report_v0` × the cost line) | Lag | Read date | It is a hypothesis about… |
|---|---|---|---|---|---|
| Variable cost per sub-€20 refund request | €7.00, all handled by a person (`Inputs!D9`) on 4,875 requests a month (`Upside!D8`) | **€7 → €4.9 at steady state.** Settled alone 11/20 = 55 % of the automatable 70 % → 38.5 % of requests at €1.60 each (AI €0.096 + expected error €1.50, `Upside!D13:D14` ÷ `D11`), 61.5 % still at €7. €5.5 at the pessimistic 40 % (`Inputs!C22`); €6.0 averaged over year 1 with the adoption ramp (`Upside!D5` 46 %). All-in, the fixed lines (€163.7k a year, `Decision!D14`) add ≈ €2.8 per request on 58,500 sub-€20 requests a year: this is the NO-GO in one number | 1 month | end of month 2 of the A/B (S6) | two arrows: correct decision → settled alone (the refund share of real traffic matches the eval-set's 11/20) → no human touch afterwards (not reopened) |
| Merchants lost after a refund request | 30 merchants a year (15,000 × 2 % dispute × 10 % churn over the 3-day wait), €12k of revenue (`Inputs!D67`, range €6k–20k) | **at most €12k a year retained.** The sizing credits the whole line; the eval says only the settled-alone share gets an immediate answer, while the 27 % handed over still wait. We read €12k as an upper bound, not a target | 90 days | 90 days after the first cohort goes live | speed of the decision → retention, and wrongful refusals (L2, confirmed by a person) not cancelling it out |
| Refund leakage and cost of errors realised | €0 above the pre-agent baseline; cost of wrong answers priced at €19.2k a year (`Upside!D40`), €15.6k of it in the sub-€20 band | **No effect, band ≤ €1.5k a week above baseline** (€79.7k ÷ 52, the `governance.md` trigger) and cost of errors realised ≤ €19.2k a year. Eval-v0: 0 refunds without evidence, 0 refunds ≥ €20 alone, 0 wrong refunds among the 11 held-out refunds; one wrong refund on demo data (EV-018, €11.75). Above the band, the rollout stops | 1 week (daily reconciliation); truth at month end | weekly from launch; month 1 finance close | the evidence gate and the policy check hold on real carrier records, not only on synthetic ones |

The tree (component → product → business):

```
clause accuracy 96 %  ──▶  executable as is 95 %  ──▶  settled alone 55 % of automatable (11/20)
                                                         │   "+1 pt ≈ +€1.0k a year" (Decision!A32:E36)
                                                         ▼
                              38.5 % of sub-€20 requests with no human touch
                                │                          │                         │
                                ▼                          ▼                         ▼
               cost per request €7 → €4.9      decision in minutes, not      refunded € unchanged
               (−€5.40 per settled request)    ~3 days, on that share         (band ≤ €1.5k a week)
                                                │
                                                ▼
                                   ≤ €12k a year of merchants retained
abstention (0 decided human-only) ─▶ wrongful refusals ≤ human rate ─▶ churn not raised (counter-metric)
```

## 5 · Make the judge trustworthy · the evaluation plan

- **The policy text first.** Until 20 November `kb/refund_policy.md` held a Paylio help article and every `clause_text` in `results_v0.csv` was empty. The LabelFlow policy (POL-4.2, 4.5, 4.6, 5.3, 6.1, 6.3, 7.2) is now written, version `2026-11-v1`; graders and judge read it.
- **Eval-set v1:** `evals/eval_set_v1.csv`, 100 cases: the 50 of v0 plus EV-051 to EV-100, inputs and labels proposed by an AI (Claude) and tagged in `origin`; labels reviewed and validated by Clémence Marco. Stratified by language, plan, amount band and carrier status (counts in `evals/README.md`). EV-051 to EV-100 have never been run: they are the fresh slice for `spec.md` v2. Golden set: EV-021 to EV-050, never changed.
- **Grading guideline:** `evals/judge_rubric.md`, written before anyone grades. Five binary criteria: right action at the right trust level · the clause a grader would cite · decided on the evidence · correct hand-over · usable receipt. Verdict EXECUTE · EDIT · FAIL. Raveloarimanga Rajesy Ny Andrian and Clémence Marco grade the same 30 rows independently in `evals/grading_golden30.csv`: agreement = *to fill* (`evals/agreement.py`).
- **Judge:** model *to fill*, prompt in `evals/judge_prompt.txt`, the 30 filled prompts in `evals/judge_inputs_golden30.txt`, run in a fresh chat that never sees our labels; human–judge agreement on the same 30 = *to fill*; disagreements read, guideline or prompt fixed once, re-aligned on *date*. Known biases: the graders wrote the labels of the golden rows; the guideline and the prompt were drafted with an AI (Claude), so a Claude judge shares that family; the agent has no model, so no self-preference on its output.
- **Cadence:** eval-set + judge at every change of rules, policy version or model · human sample weekly (the L4 sample in `governance.md`) · the two rates re-measured at each policy change.
- *Optional, not graded:* `evals/adversarial_v0.csv` is still the Paylio file; our five red rows would come from `spec.md` §4 (instructions in the merchant text, a claim the evidence contradicts, request splitting, an exception written in prose, an amount just under €20).

*Numbers measured on 17 November 2026, prototype tag `eval-v0` (rules v0, policy version `2026-11-v0`).*
