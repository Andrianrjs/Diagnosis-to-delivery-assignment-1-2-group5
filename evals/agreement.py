"""Agreement rates on the golden 30 (Assignment 5 §5). Run from the repo root: python3 evals/agreement.py

Reads evals/grading_golden30.csv once the three verdict columns are filled (EXECUTE / EDIT / FAIL).
"""
import csv
from pathlib import Path

SHEET = Path(__file__).resolve().parent / "grading_golden30.csv"
VERDICTS = {"EXECUTE", "EDIT", "FAIL"}

rows = list(csv.DictReader(open(SHEET, encoding="utf-8")))
for col in ("grader_A_verdict", "grader_B_verdict", "judge_verdict"):
    bad = [r["case_id"] for r in rows if r[col].strip().upper() not in VERDICTS]
    if bad:
        print(f"{col}: {len(bad)} rows not graded yet ({', '.join(bad[:5])}{'…' if len(bad) > 5 else ''})")

done = [r for r in rows if all(r[c].strip().upper() in VERDICTS
                               for c in ("grader_A_verdict", "grader_B_verdict", "judge_verdict"))]
if not done:
    raise SystemExit("nothing to compare yet")

v = lambda r, c: r[c].strip().upper()
hh = [r for r in done if v(r, "grader_A_verdict") == v(r, "grader_B_verdict")]
print(f"\nhuman–human agreement : {len(hh)}/{len(done)} = {len(hh) / len(done):.0%}")
hj = [r for r in hh if v(r, "judge_verdict") == v(r, "grader_A_verdict")]
print(f"human–judge agreement : {len(hj)}/{len(hh)} = {len(hj) / max(len(hh), 1):.0%}  (on the rows where the two humans agree)")
for g in ("grader_A_verdict", "grader_B_verdict"):
    n = sum(v(r, "judge_verdict") == v(r, g) for r in done)
    print(f"judge vs {g[:8]}     : {n}/{len(done)} = {n / len(done):.0%}")

print("\ndisagreements to read by hand:")
for r in done:
    a, b, j = v(r, "grader_A_verdict"), v(r, "grader_B_verdict"), v(r, "judge_verdict")
    if len({a, b, j}) > 1:
        print(f"  {r['case_id']}  A={a:7} B={b:7} judge={j:7}  {r['clause_id'] or r['reason']}")
