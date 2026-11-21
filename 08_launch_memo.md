# Launch memo — <project name> — <date>

> One page. The decision on line one. Numbers, names, dates. Paylio's filled version: the S8 document, slides 4 and 5.

## 1 · Decision
**<Go / No-go / Conditional go>** — to <step and scope: e.g. "step 1 (internal users, 1 week) then step 2 (A/B on 50 % of <unit>, 4 weeks)">, from <date>. The next decision is read on <date> by <name> and <name>.

**Budget we ask for:** <amount> a year, taken from the fixed costs of `02_sizing.xlsx`. It pays for <people who supervise>, <integration>, <evaluation>, <monitoring>.

## 2 · Evidence
- Eval v1 (<n> cases, two graders on 30, judge validated — agreement <x %> / <y %>): **<result>** against the criterion **<criterion sentence>**.
- Guardrails: <0 outputs on forbidden cases> / <n>, checked <how often>.
- What the A/B will prove: <primary> from <baseline> to at least <target>; ≈ <n> <units> per arm (inputs: <baseline>, <smallest gain that pays>); duration <weeks> because <slowest guardrail>.
- Sizing: base <€> vs hurdle <€> (<next-best project>); EV <€>; do-nothing trajectory <€>.

## 3 · Rollout steps
| Step | Scope | Duration | Gate (metric · threshold · read date) | Signs the next step |
|---|---|---|---|---|
| 0 | shadow, staging | done | criterion met on eval v1 · no red row · rollback tested | <PM> |
| 1 | internal users, then a small share (<5 %>) | <duration> | 0 forbidden outputs · <metric ≥ threshold> on the weekly sample | <name> |
| 2 | the A/B, 50 % | <4 weeks> | <primary ≥ target> · guardrails green · ship / iterate / kill on <date> | <name> + <name> |
| 3 | 100 % with a <5 %> holdout | <6 months> | monthly: four layers green, drift review | <name> |

## 4 · Rollback & the switch
Trigger: <thresholds> · Who decides: <name> (at night: <name>) · Action: suggest-only → off (<how>) · Time to execute: < <15> min · What people see: <users> / <customers> · **Last tested: <date>, in <staging>, with <names>.**

## 5 · Owners — and who signs
| Decision | Owner | Written where |
|---|---|---|
| run an experiment on real users | <name> signs; <DPO / legal> reads | 06_07 §1–§2 · governance.md |
| read the weekly numbers and act | <name> | 06_07 §3 |
| press the switch | <name>; at night <name> | 06_07 §4 · governance.md |
| approve a release (prompt, model, KB) | <name>, with the eval re-run | evals/README.md |
| keep the trace, answer a customer or a regulator | <team> keeps it; <legal> answers | governance.md |

**This launch is signed by <name> and <name>.**

## 6 · What we do not know yet
- <open risk 1> — next experiment: <…>
- <open risk 2> — next experiment: <…>
- <the number we could not measure> — how we will: <…>
