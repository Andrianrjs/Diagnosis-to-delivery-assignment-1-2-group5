# 06_07 — Experiments & operation · <team> · <agent>

> Five sections = the five moves of Sessions 6 + 7. Every number traces to `02_sizing.xlsx`, `05_metrics.md` or `evals/report_v0.md`. Every owner is a named role. Every threshold has a clock.
> Paylio lines are examples — replace them with yours.

## §1 Prove the effect — hypothesis, unit, design (in words; you are not graded on statistics)

**Hypotheses** (one per business metric of `05_metrics.md §4`):

1. If we <change> for <segment>, then <metric> moves from <baseline> to <target> by <read date> — without <counter-metric> leaving <band>.
   - *Paylio: if we let agents send copilot drafts on "how do I" tickets, the share of those tickets closed within one hour moves from 20 % to at least 25 % by week 2 — without CSAT leaving 4.3 ± 0.1 and without the French reopen rate exceeding 1.5× the English one. (An outcome that exists with and without the agent — the 40 % of S4 is draft quality, not an outcome.)*
2. …
3. …

**Unit of randomisation:** <ticket / user / agent / team / site> — because the treatment would leak to: <…>.
**Design:** <A/B on units · A/B on clusters · holdout · shadow mode · before/after with control> — what it cannot see: <…>.

## §2 Decide before — duration and decision rule (the table below is optional: `evals/sample_size.xlsx`)

**Smallest improvement that still justifies the agent, and why:** <…>
**Slowest guardrail to read → how long we run:** <…>

| Input | Value | Source |
|---|---|---|
| Baseline p₀ — an outcome that exists with and without the agent (not the offline quality rate of S4) | | `02_sizing.xlsx` / `05_metrics.md` |
| Smallest rise worth acting on | | the smallest effect that changes a decision (`02_sizing.xlsx`) |
| Two risks accepted (false win · missed win) | 1 in 20 · 1 in 5 | preset in the calculator |
| **Units per group** | | `evals/sample_size.xlsx` |
| Volume per week | | `02_sizing.xlsx` |
| **Duration actually run** | | the read date of the slowest guardrail |

**Pre-registered segments:** <the S5 list>.
**Decision rule, written on <date>, before the first unit:**
- Ship if …
- Iterate if …
- Kill if …
- Stop early only if … (the harm threshold of `governance.md`) — never on a good number.

## §3 Watch the four layers — monitoring and drift

| Layer | Metric (from `05_metrics.md`) | Threshold that pages someone | Clock | Owner | Tool — startup | Tool — large company |
|---|---|---|---|---|---|---|
| Infrastructure | | | real time | | <platform metrics · Sentry · Grafana Cloud> | <CloudWatch / Azure Monitor / Cloud Monitoring · Datadog> |
| Model quality | | | weekly | | <Langfuse · Phoenix> | <LangSmith · Langfuse self-hosted · Datadog LLM> |
| Product & guardrails | | | daily | | <SQL table + Metabase / Looker Studio> | <warehouse + Power BI / Tableau / Looker> |
| Business | | | weekly / monthly | | <weekly query + sheet> | <BI dashboard> |
| Paging | — | — | — | | <Slack / Teams webhook> | <PagerDuty / Opsgenie> |

**Where our FastAPI runs:** <our laptop + tunnel for the demo · Streamlit Cloud + Render / Hugging Face Space / Vercel / Cloud Run for a pilot> — why: <…>. Secrets in `.env`, never in Git.

**Release path and gates:** dev (every commit: <assertions>) → staging (every change of prompt / model / sources: eval-set + judge, shadow mode, rollback tested on <date>) → production by steps (<internal → 5 % → 50 % → 100 %>), each step guarded by <threshold of the table above>.

**First drift expected:** <data · concept · knowledge · model> — signal: <…> — what we re-run: the frozen eval-set (`evals/eval_set_v1.csv`) on every <release / model version / policy change>.

## §4 Contain the incident — trace, classes, rollback

**Trace — one OpenTelemetry trace per output, one span per step:** `request` (id · timestamp · segment · prompt / model / sources version · latency · cost) → `classify` (label · confidence) → `retrieve` (sources + scores · no-hit) → `generate` (tokens · latency) → `guardrail` (result) → `human_decision` (approved / edited / escalated · judge score · human grade if sampled). Stored in: <Langfuse / Phoenix / …>.

**Our one-page dashboard — five panels and the question each answers:** stat tiles + thresholds (am I paged?) · line over time (trend, spikes) · histogram this week vs last (drift) · bars by segment (Simpson, fairness) · worst-cases table (what to fix on Monday). Built with: <Streamlit tab / Grafana / Metabase>.

| Class | Example on our agent | Action |
|---|---|---|
| Caught | | count · weekly review · spec line if it repeats |
| Sent wrong | | |
| Harmful (above the harm threshold) | | rollback now · incident report · DPO if data |
| Outage | | fallback: humans-only, automatic |

**Rollback plan**

| Field | Ours |
|---|---|
| 1 · Trigger | |
| 2 · Who decides (day / night) | |
| 3 · The action (suggest-only · off · redeploy previous version) | |
| 4 · Time to execute | |
| 5 · What people see | |
| 6 · Last tested (date · where · who) | |

## §5 Own the system — the five owners

| Decision | Owner (role) | Written where |
|---|---|---|
| Run an experiment on real users | | this file §1–§2 · `governance.md` |
| Read the weekly numbers and act | | §3 |
| Press the switch (day / night) | | §4 · `governance.md` |
| Approve a release (prompt, model, sources) | | `evals/README.md` |
| Keep the trace; answer a customer or a regulator | | `governance.md` |

*Copied into `governance.md`:* who signs an experiment on real users · who can press the switch · where the trace lives and for how long.
