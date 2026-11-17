# Session 5 files — what goes where

| File | Where in your repo | Due |
|---|---|---|
| `05_metrics.md` | repo root — the five moves, sections 1–5, written at home (slide 21 = your checklist for §1–4) | 22 Nov |
| `evals/eval_set_v1.csv` | your 50 cases → 100 (200 is the production standard, optional), stratified by segment, synthetic rows tagged (same columns as `eval_set_v0.csv`) | 22 Nov |
| `evals/adversarial_v0.csv` | *optional, not graded* — red rows, one OWASP code each (slide 29) | — |
| `evals/judge_rubric.md` + `evals/judge_prompt.txt` | the grading guideline (the rubric — Paylio example to replace), the judge prompt, and in `evals/README.md` the two agreement rates on 30 cases (human–human, human–judge) | 22 Nov |
| `evals/promptfooconfig.yaml` + `prototype/provider.py` | *optional* — the level-1 assertions; adapt them to your own "never" list | — |
| `governance.md` — Session 5 line | counter-metrics, segments reported, harm threshold, owner | 22 Nov |

## Running the tools on the Paylio starter (or your agent)

**promptfoo — assertions (no API key needed with the mock drafter)**
```
npm install -g promptfoo          # or npx promptfoo@latest …
cd support-copilot-starter
cp <S5_templates>/evals/promptfooconfig.yaml evals/ ; cp <S5_templates>/prototype/provider.py prototype/
npx promptfoo@latest eval -c evals/promptfooconfig.yaml
npx promptfoo@latest view
```
**promptfoo — red team** (generates attacks with a model: set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`)
```
npx promptfoo@latest redteam run -c evals/promptfooconfig.yaml
npx promptfoo@latest redteam report
```
**Giskard scan on the drafter** (Python; needs a model key for the detectors)
```python
import giskard, pandas as pd
from prototype import retrieve, draft as drafter
def predict(df: pd.DataFrame):
    return [drafter.draft(t, retrieve.top_k(t)) for t in df["ticket"]]
model = giskard.Model(model=predict, model_type="text_generation",
                      name="Paylio copilot drafter", description="Drafts KB-grounded replies to how-do-I tickets; never prices, refunds, legal advice or other customers' data.",
                      feature_names=["ticket"])
dataset = giskard.Dataset(pd.read_csv("evals/eval_set_v1.csv").rename(columns={"input_the_agent_receives": "ticket"}), target=None)
report = giskard.scan(model, dataset)      # prompt injection, hallucination, harmful, disclosure, stereotypes, sycophancy, formatting
report.to_html("evals/giskard_scan.html")
```
**RAGAS on retrieval + drafting** (needs a model key)
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
# build a dataset with columns: question, answer, contexts, ground_truth  (from eval_set_v1 + your prototype's outputs)
```
Write the numbers you get in `05_metrics.md` §5 — with the date and the version of the prototype they were measured on.
