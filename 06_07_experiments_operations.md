# 06_07 — Experiments & operation · Group 5 · LabelFlow refund agent

> Five sections = the five moves of Sessions 6 + 7. Every number traces to `02_sizing.xlsx`, `05_metrics.md` or `evals/report_v0.md`. Every owner is a named role. Every threshold has a clock. Decision rule written on 21 November 2026, before any real unit.

**Read this first.** A successful test proves that the agent keeps the promise of `05_metrics.md` §4 on real traffic; it does not turn the sizing into a GO. The base case stays below do-nothing at every deflection from 30 % to 75 % (`Decision!A32:E36`); the investment decision turns on in-scope volume (`02_investment_memo.md`).

## §1 Prove the effect — hypothesis, unit, design (in words; you are not graded on statistics)

**Hypotheses** (one per business metric of `05_metrics.md §4`):

1. If we let the agent settle sub-€20 refund requests alone (L4) for merchants writing in French or English, then the **variable cost per sub-€20 refund request** moves from **€7.00** (`Inputs!D9`) to **€4.9** by the read date of §2 (day 35), without refund leakage leaving its band of **€1.5k a week** above the pre-agent baseline (`Decision!D6` ÷ 52, `governance.md` §6).
1. If the same merchants get a decision in minutes instead of ~3 days (`Inputs!G67`), then the **merchants lost after a refund request** fall from **30 a year, €12k** (`Inputs!D67`), with at most €12k retained, by 90 days after the first cohort, without wrongful refusals (overturned after a dispute) rising above the pre-agent human rate.
1. If the evidence gate and the policy check hold on real carrier records, then **refund leakage** stays within **€1.5k a week** above baseline and the cost of errors realised within **€19.2k a year** (`Upside!D40`), read weekly from launch and at the month-1 finance close. This is a no-harm hypothesis: the effect we want is none.

**Unit of randomisation:** the **merchant**, not the request, because the treatment would leak through the merchant: one who gets an instant refund changes how they write the next request and learns where the €20 line sits (eval-v0 already raised the split flag on M-1042 and M-6028, `report_v0`). Merchants are assigned once, by a hash of `merchant_id`, and keep their arm; the eval-set is split the same way (`03_product_brief.md` §4). **Design:** **shadow mode for 2 weeks** (the agent decides on every sub-€20 request, a person decides as today, nothing the agent says is executed; if agreement falls below the 55 % criterion, no A/B), **then an A/B test on merchants** (treatment at its trust levels, L4 under €20 and every refusal confirmed at L2; control keeps the human queue). What it cannot see: (1) **interference through the queue**: every request the agent settles frees a person, so the control queue gets faster than today and the speed and retention gap is under-estimated; (2) **long-run learning**: merchants splitting under €20 over months, and the 90-day churn, go to monitoring (§3); (3) **merchants outside FR and EN**: never decided by design (`language_not_covered`).

## §2 Decide before — duration and decision rule (the table below is optional: `evals/sample_size.xlsx`)

**Smallest improvement that still justifies the agent, and why:** **€7.00 → €5.5 per request**, the pessimistic sizing case at 40 % deflection (`Inputs!C22`, `05_metrics.md` §4). Below it, the agent does worse than the worst case we priced, and one point of deflection is worth only about €1.0k a year (`Decision!A32:E36`). **Slowest guardrail to read → how long we run:** the effect is huge (from no request settled without a person to 38.5 % of them), so, like P4 of `README_S6_7.md`, **the guardrail sets the duration, not the effect**. "Settled and uncontested" needs a 7-day reopen window, and leakage is only confirmed at the monthly finance reconciliation, so we run **4 weeks of requests plus the 7-day window, with one read on day 35**, after the month-end close. The churn of hypothesis 2 is read once more at day 90, as a follow-up and not as the ship decision.

| Input | Value | Source |
| --- | --- | --- |
| Baseline p₀ — an outcome that exists with and without the agent (not the offline quality rate of S4) | 0 % of sub-€20 requests settled with no human touch; €7.00 per request | `05_metrics.md` §4 · `Inputs!D9` |
| Smallest rise worth acting on | cost per request down to €5.5 (≈ 40 % deflection × 0.70 automatable ≈ 28 % settled alone) | `Inputs!C22` |
| Two risks accepted (false win · missed win) | 1 in 20 · 1 in 5 | preset in the calculator |
| **Units per group** | not computed: the effect is far larger than the minimum, and the guardrail decides the duration | `evals/sample_size.xlsx` (optional) |
| Volume per week | ≈ 1,125 sub-€20 refund requests (4,875 a month × 12 ÷ 52) | `Upside!D8` |
| **Duration actually run** | 4 weeks + 7-day reopen window, one read on day 35 | the read date of the slowest guardrail |

**Pre-registered segments:** language (FR · EN · other) · plan (standard · high-volume · enterprise) · amount band (< €20 · €20–100 · > €100) · carrier status (NO_SCAN · IN_TRANSIT · DELIVERED · RETURNED_TO_SENDER), as listed in `05_metrics.md` §3. No segment is added after the read. **Decision rule, written on 21 November 2026, before the first unit:**

- Ship if cost per request ≤ €5.5 in treatment **and** zero hard-invariant breaches **and** leakage within €1.5k every week **and** "a person reached" no worse than control.
- Iterate if cost per request is between €5.5 and €7.00, or one segment breaks its guardrail while the others hold: back to L2 on that segment, change `spec.md`, re-run the frozen eval-set, new test.
- Kill if cost per request ≥ €7.00, or the same invariant is broken twice.
- Stop early only if a refund goes out without tracking evidence, a refund ≥ €20 is settled alone, or the harm threshold of `governance.md` is crossed (on any language or plan segment, wrongful refusals above that segment's pre-agent human rate, or a decided human-only case, over two consecutive weeks). Never on a good number.

## §3 Watch the four layers — monitoring and drift

| Layer | Metric (from `05_metrics.md`) | Threshold that pages someone | Clock | Owner | Tool — startup | Tool — large company |
| --- | --- | --- | --- | --- | --- | --- |
| Infrastructure | decision latency · carrier API up · share of "cannot decide, evidence unavailable" | p95 decision above 30 s (`03_product_brief.md` §6) · evidence unavailable on more than 27 % of requests (eval-v0 hand-over rate) | real time | prototype builder | Cloud Run metrics · Sentry | Cloud Monitoring · Datadog |
| Model quality (rule components; no model in v0) | clause accuracy and executable as is on the frozen eval-set · L4 weekly sample marked "should have gone to a person" | any drop below eval-v0 (96 % clause, 95 % executable) · any sampled case marked | weekly, and at every commit | agent product owner | Phoenix (traces) + `evals.py` / promptfoo | Langfuse self-hosted |
| Product & guardrails | the 3 hard invariants · settled alone and uncontested · a person reached | any invariant breach (must be 0) · settled alone below 38.5 % of sub-€20 requests (0.70 × 0.55) for 2 weeks · a hand-over not answered within ~3 days | daily (invariants in seconds, in `policy.py`) | Head of Support Operations | SQL table of receipts + Metabase | warehouse + Looker |
| Business | refund leakage · cost per sub-€20 request · churn after a refusal | leakage above €1.5k a week above baseline · cost per request above €5.5 for a month | weekly (leakage) / monthly (cost, finance close) / 90 days (churn) | Finance | weekly query + sheet | finance reconciliation in the warehouse + Looker |
| Paging | — | — | — | Head of Support Operations | Slack webhook | PagerDuty |

**Where our FastAPI runs:** our laptop + tunnel for the demo, **Cloud Run in an EU region for a pilot**. Why: receipts hold merchant data under GDPR, so the data stays in the EU, and the agent is rules only, so there is no GPU and no model to host. Secrets in `.env`, never in Git.

**Release path and gates:** dev (every commit: `python3 prototype/evals.py`, zero invariant breaches, no drop on the golden 30) → staging (every change of rules, policy version or sources: eval-set v1 + judge with every EDIT and FAIL read by a person, shadow mode, rollback tested on 17 November 2026) → production by steps (**shadow → 5 % of merchants for 1 week → 50 % of merchants, the A/B test of §1, 4 weeks → 100 %**), each step guarded by zero invariant breaches and leakage within €1.5k a week, signed by the agent product owner.

**First drift expected:** **knowledge** — the refund policy changes (a window, a clause) and the agent keeps citing the retired text (`03_product_brief.md` §8). Signal: a receipt whose `policy_version` differs from the live `kb/refund_policy.md`, or a clause id that no longer exists. What we re-run: the frozen eval-set (`evals/eval_set_v1.csv`) and the golden 30, with the judge, on every **policy change**, before it reaches production. Next in line: data drift (a carrier adds a status outside the four in `retrieve.py`, so "no tracking evidence" spikes) and concept drift (merchants learn the €20 line, so the split flag rises per merchant per week).

## §4 Contain the incident — trace, classes, rollback

**Trace — one OpenTelemetry trace per output, one span per step:** `request` (case_id · timestamp · segment: language, plan, amount band · experiment arm · rules version `rules-v0` · policy version · latency; cost ≈ 0, no model call) → `router` (language · amount · stop_reason) → `routing_rule` (tracking-number format · carrier record found · gate result) → `retrieve` (carrier status · elapsed days · duplicate charge · prior refund · clause ids loaded, or no-hit) → `decide` (outcome · clause_id · trust level · reason) → `policy_check` (evidence present · amount below €20 · switch state · passed or blocked) → `human_decision` (approved / edited / escalated at L2 · judge verdict · human grade if in the weekly sample). Stored in: Phoenix for the pilot; the decision receipt itself is written to the receipt log.

**Our one-page dashboard — five panels and the question each answers:** stat tiles + thresholds (am I paged? the 3 invariants, leakage this week against €1.5k) · line over time (trend, spikes: settled alone and uncontested against 38.5 %) · histogram this week vs last (drift: carrier statuses and cited clauses, so a new status or a retired clause shows) · bars by segment (Simpson, fairness: wrongful refusals and decided human-only cases by language and plan) · worst-cases table (what to fix on Monday: reversed refunds, overturned refusals, sampled cases marked "should have gone to a person"). Built with: Metabase on the receipt table.

| Class | Example on our agent | Action |
| --- | --- | --- |
| Caught | a policy exception (the carrier stopped operating) refused by the agent, stopped at L2 because every refusal is confirmed by a person (EV-050) | count · weekly review · spec line if it repeats |
| Sent wrong | a refusal sent with the wrong clause, so the merchant is not told to ask again from day 21 (EV-031); or a wrong sub-€20 refund (EV-018, €11.75 on demo data) | correct the answer or reverse the refund · add the case to the eval-set · spec line |
| Harmful (above the harm threshold) | leakage above €1.5k in 7 days, a refund without tracking evidence, or one segment above its human wrongful-refusal rate for two weeks | rollback now · incident report · Legal, and the DPO if merchant data is involved |
| Outage | the carrier API is down, so no evidence can be read | fallback: humans-only, automatic ("cannot decide, evidence unavailable"), the queue goes back to the ~3-day wait |

**Rollback plan**

| Field | Ours |
| --- | --- |
| 1 · Trigger | refunded € over a rolling 7 days more than €1.5k above the pre-agent baseline (`governance.md` §6) · any hard invariant broken · the segment harm threshold of §2 |
| 2 · Who decides (day / night) | day: Head of Support Operations · night: the leakage and invariant triggers fire automatically, nobody has to decide; the Head of Support Operations confirms the next morning |
| 3 · The action (suggest-only · off · redeploy previous version) | **suggest-only first**: the file `prototype/SWITCH_DOWNGRADE` turns every refund into "prepare" (L2), the agent prepares and a person approves · **off** if the prepared receipts themselves are wrong: every case to the human queue · **redeploy the previous version** (git tag) if a release caused it |
| 4 · Time to execute | one file, seconds; under 15 minutes from the alert to confirmation |
| 5 · What people see | support agents: every case lands in their approval queue with the receipt already prepared · merchants: the same answer, approved by a person, so slower |
| 6 · Last tested (date · where · who) | **17 November 2026 · the prototype on our laptop (our staging), on eval-v0 · Raveloarimanga Rajesy Ny Andrian**: 17 of 17 refunds became "prepare" (`04_architecture.md` §6) |

## §5 Own the system — the five owners

| Decision | Owner (role) | Written where |
| --- | --- | --- |
| Run an experiment on real users | Head of Support Operations, read by Legal before it starts (deployer obligations, EU AI Act art. 26) | this file §1–§2 · `governance.md` |
| Read the weekly numbers and act | agent product owner; Finance for leakage and cost | §3 |
| Press the switch (day / night) | Head of Support Operations by day; the automatic trigger by night | §4 · `governance.md` |
| Approve a release (rules, policy version, sources) | agent product owner after the staging gate; plus the Head of Support Operations for a new policy version | `evals/README.md` |
| Keep the trace; answer a customer or a regulator | Legal, with Finance for the refund records | `governance.md` |

_Copied into `governance.md`:_ who signs an experiment on real users · who can press the switch · where the trace lives and for how long. The company answers for what the agent decides (_Moffatt v. Air Canada_, 2024 BCCRT 149): the receipt is how we answer.