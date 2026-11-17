# 05 · Metrics — <team> · <agent>

> Session 5 deliverable. Five sections = the five moves of the session. Every number must trace to a file already in the repo (`02_sizing.xlsx`, `evals/report_v0.md`) — no new numbers appear here.

## 1 · Place the number — the stack for your agent
One metric per level. "Produced by" = which evaluation type (offline eval-set · human grading · LLM judge · adversarial · online A/B · monitoring).

| Level | Question | Your metric | Value today (or "not yet") | Produced by | Owner | Clock |
|---|---|---|---|---|---|---|
| 5 Business | does it move the P&L? | | | | | months |
| 4 Product | does the user adopt it and get the job done? | | | | | weeks |
| 3 Guardrails & responsible AI | does it stay inside the lines — for everyone? | | | | | days |
| 2 AI system | does the workflow complete the task? | *your S4 number* | | eval-set + two graders | | hours |
| 1 Model | is the component right? | | | offline eval-set | | seconds |

## 2 · Decide when to stop — the stop criterion
*"We stop improving `<component metric>` at `<value>` because `<next-level metric>` stops responding — or the action no longer changes — and the next point would cost `<…>`."*

- Component metric and value:
- The level-above metric that stops responding (or the action threshold):
- Cost of the next point (weeks, tokens, labelling, latency):
- What is a **floor**, not a stop (any miss blocks the release):

## 3 · Choose what to protect — the hierarchy, by segment
| Kind | Metric | Numerator / denominator | Level | Lag | Source & owner |
|---|---|---|---|---|---|
| Primary (1) | | | | | |
| Guardrail (3) | | | | | |
| Guardrail | | | | | |
| Guardrail | | | | | |
| Counter-metric (2) | | | | | |
| Counter-metric | | | | | |

- **Segments reported** (from the S3 audit): language · plan · region · severity · …
- **Fairness metric**, named (selection-rate parity / equal error rates across segments):
- **Harm threshold** on the counter-metric, per segment, that stops the rollout — and its owner: *(copy this line into `governance.md`)*
- How it could be gamed (the other team's line) → the repair:

## 4 · Derive the business metrics — three, with expected effects (the oral)
| Business metric | Baseline (from `02_sizing.xlsx`) | Expected effect (from `evals/report_v0.md` × the cost line) | Lag | Read date | It is a hypothesis about… |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | *(at least one stated as a non-effect with a stop band)* |

The tree (component → product → business), as a picture or a list of arrows with their claimed effect sizes:

## 5 · Make the judge trustworthy — the evaluation plan
- **Eval-set v1**: `evals/eval_set_v1.csv`, 100 cases (200 in production), stratified by <segments>; synthetic inputs tagged, labels by a person; a golden set of 30 that never changes.
- **Grading guideline**: `evals/README.md` — binary criteria, boundary examples. Two graders on the same 30 rows: agreement = <xx> %.
- **Judge**: model <…>, prompt in `evals/judge_prompt.txt`; human–judge agreement on the same 30 = <xx> %; known biases; re-aligned on <date>.
- **Cadence**: eval-set + judge every change · human sample weekly.
- *Optional, not graded* — **red rows**: `evals/adversarial_v0.csv`, five attacks by OWASP line (slide 27); what passed → spec v2 lines. **Assertions** (level 1, every commit): `evals/promptfooconfig.yaml`.
