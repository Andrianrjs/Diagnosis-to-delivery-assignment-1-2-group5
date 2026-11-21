# Launch memo — LabelFlow refund agent — Group 5 · 26 November 2026

> One page. The decision on line one. Every number traces to `02_sizing.xlsx`, `02_investment_memo.md`, `05_metrics.md`, `06_07_experiments_operations.md` or `evals/`.

## 1 · Decision

**Conditional go — to step 0 only: shadow mode on sub-€20 refund requests from FR and EN merchants, 2 weeks, orchestrated with a vendor, no refund executed by the agent**, from 7 December 2026. The next decision is read on 21 December 2026 by the Head of Support Operations and Finance. Step 1 opens only if (a) `spec.md` v3 passes the fresh slice of eval v1 (EV-051 to EV-100) with zero hard-invariant breaches, and (b) the three-month refund-amount export shows in-scope volume heading to ~33,000 deflected tickets a year (`02_investment_memo.md`). Without (b), the answer stays NO-GO: a better agent does not rescue the case, scope does.

**Budget we ask for:** €35k a year, the evaluation line of the fixed costs (`Inputs!D51`), not the €164k full fixed base (`Decision!D14`). It pays for the eval v1 runs, the graders' time on the golden 30, the shadow-mode comparison and the weekly L4 sample. The rest of the fixed base is asked for at the step-2 gate, not before.

## 2 · Evidence

- Eval v0, held-out (20 automatable sub-€20 cases): **19/20 = 95 % executable as is** against the criterion **55 %**, but **FAIL** on one floor: one human-only case decided (EV-050, a policy exception written in prose). `spec.md` v2 adds the stop; not yet re-evaluated. Eval v1: 100 cases built, golden 30 graded by two graders and a judge, agreement **97 % / 97 %** (`evals/README.md`); EV-051 to EV-100 never run.
- Guardrails: **0** refunds without tracking evidence / **0** refunds ≥ €20 settled alone / **1** decision on a human-only case, checked 17 November 2026 (`report_v0`).
- What the A/B will prove: variable cost per sub-€20 request from **€7.00** to at most **€5.5** (expected €4.9); ≈ **2,250 requests per arm** (≈ 1,125 a week, `Upside!D8`, over 4 weeks, randomised by merchant); duration **4 weeks + the 7-day reopen window**, because "settled and uncontested" and the monthly leakage reconciliation are the slowest guardrails (`06_07` §2).
- Sizing: base **−€84k** a year vs hurdle **+€180k** (the self-serve refund-status page); EV **−€73k** (scenarios −€273k / −€84k / +€148k, weighted 0.25 / 0.50 / 0.25); do-nothing **+€84k**. Below do-nothing at every deflection from 30 % to 75 % (`Decision!A32:E36`).

## 3 · Rollout steps

| Step | Scope | Duration | Gate (metric · threshold · read date) | Signs the next step |
| --- | --- | --- | --- | --- |
| 0 | shadow, staging: the agent decides, a person decides as today, nothing executed | 2 weeks, from 7 Dec 2026 | eval v1 fresh slice: 0 invariant breaches and ≥ 55 % executable · shadow agreement ≥ 55 % · rollback tested (17 Nov 2026) · export shows the volume · read 21 Dec 2026 | Head of Support Operations + Finance |
| 1 | 5 % of FR and EN merchants | 1 week | 0 refunds without evidence · 0 refunds ≥ €20 alone · 0 "should have gone to a person" in the weekly L4 sample | Head of Support Operations |
| 2 | the A/B, 50 % of merchants | 4 weeks + 7 days | cost per request ≤ €5.5 · leakage ≤ €1.5k every week · a person reached no worse than control · ship / iterate / kill on day 35 (`06_07` §2) | Head of Support Operations + Finance, Legal reads |
| 3 | 100 % with a 5 % holdout of merchants | 6 months | monthly: four layers green (`06_07` §3), drift review at each policy change, 90-day churn read | agent product owner |

## 4 · Rollback & the switch

Trigger: refunded € over 7 days more than €1.5k above baseline, any hard invariant broken, or the segment harm threshold · Who decides: Head of Support Operations (at night: the automatic trigger, confirmed the next morning) · Action: suggest-only (every refund prepared at L2, `SWITCH_DOWNGRADE`) → off (every case to the human queue) · Time to execute: < 15 min · What people see: support agents get every case in their approval queue with the receipt prepared / merchants get the same answer, approved by a person, so slower · **Last tested: 17 November 2026, on the prototype (our laptop, eval-v0), with Raveloarimanga Rajesy Ny Andrian: 17 of 17 refunds became "prepare".**

## 5 · Owners — and who signs

| Decision | Owner | Written where |
| --- | --- | --- |
| run an experiment on real users | Head of Support Operations signs; Legal reads | 06_07 §1–§2 · governance.md |
| read the weekly numbers and act | agent product owner; Finance for leakage and cost | 06_07 §3 |
| press the switch | Head of Support Operations; the automatic trigger at night | 06_07 §4 · governance.md |
| approve a release (rules, policy version, KB) | agent product owner, with the eval re-run; plus the Head of Support Operations for a new policy version | evals/README.md |
| keep the trace, answer a customer or a regulator | Finance keeps the receipt log; Legal answers | governance.md |

**This launch is signed by the Head of Support Operations and Finance** (people named before step 0, `governance.md` A1 Q3). Prepared by Raveloarimanga Rajesy Ny Andrian and Clémence Marco.

## 6 · What we do not know yet

- **The share of refund requests under €20** is a guess (65 %, `Inputs!D14`), and it moves the whole case — next experiment: the three-month refund-amount export, before step 0 ends.
- **Whether spec v3 generalises**: EV-051 to EV-100 have never been run; the policy and the spec are now aligned on EV-047 (`2026-11-v2`) but the judge has not been re-run on it — next experiment: build v3, run eval v1 on the fresh slice and re-run the judge on EV-046 and EV-047, before step 1.
- **The pre-agent wrongful-refusal rate per segment**, which the harm threshold compares against, and the €1.5k trigger, which is a guess (`governance.md` §6) — how we will: measure both from the dispute log and the refund export of the last three months, before step 1.