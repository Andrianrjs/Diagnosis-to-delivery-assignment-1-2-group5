"""Spec §7. Never tune while looking at these rows. Run from the repo root: python3 prototype/evals.py"""
import csv
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import decide as decider  # noqa: E402
import policy  # noqa: E402
import retrieve  # noqa: E402
import route_rule  # noqa: E402
import router  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EVAL_SET = ROOT / "evals" / "eval_set_v0.csv"
RESULTS = ROOT / "evals" / "results_v0.csv"
CRITERION = 0.55
DEMO = {f"EV-{i:03d}" for i in range(1, 21)}   # read while the rules were written
MODEL_VERSION = "rules-v0"
POLICY_VERSION = "2026-11-v0"


def run_one(row):
    """The five steps of spec §2, in order. Returns the receipt."""
    _, amount, reason = router.route(row["input_text"], row["amount_eur"])
    evidence = None
    if reason is None:
        reason = route_rule.gate(row["tracking_number"], row["evidence"])
    if reason is None:
        evidence = retrieve.tracking(row["evidence"])
        decision = decider.decide(row["input_text"], evidence, amount)
    else:
        decision = decider.stop(reason)
    status, why = policy.check(decision, evidence is not None, amount)
    if status == "block":
        decision = decider.stop("blocked: " + why)
    clause = decision["clause_id"]
    return {
        "case_id": row["case_id"],
        "action": decision["action"],
        "trust_level": decision["trust_level"],
        "clause_id": clause or "",
        "clause_text": retrieve.CLAUSES.get(clause, ""),
        "evidence": row["evidence"] if evidence else "NOT_FOUND",
        "amount_eur": amount,
        "reason": decision["reason"],
        "policy": status,
        "model_version": MODEL_VERSION,
        "policy_version": POLICY_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def score(rows, label):
    auto = [r for r in rows if r["expected_action"] != "unknown" and r["amount"] is not None and r["amount"] < 20]
    decided = [r for r in rows if r["action"] != "unknown" and r["expected_action"] != "unknown"]
    n_ok = sum(r["ok"] for r in auto)
    print(f"\n{label} ({len(rows)} cases)")
    print(f"  decision accuracy        {sum(r['action'] == r['expected_action'] for r in rows) / len(rows):.2f}")
    print(f"  clause accuracy          {sum(r['clause_id'] == r['expected_clause'] for r in decided) / max(len(decided), 1):.2f}")
    print(f"  executable as is         {n_ok}/{len(auto)} automatable sub-€20 cases = {n_ok / max(len(auto), 1):.0%}"
          f"   (criterion {CRITERION:.0%})")
    print(f"  refunds without evidence {sum(r['action'] == 'refund' and r['evidence'] == 'NOT_FOUND' for r in rows)}   (must be 0)")
    print(f"  refunds >= €20 alone     {sum(r['action'] == 'refund' and (r['amount'] or 0) >= 20 for r in rows)}   (must be 0)")
    print(f"  decided on human-only    {sum(r['expected_action'] == 'unknown' and r['action'] != 'unknown' for r in rows)}   (must be 0)")
    print(f"  escalated decidable      {sum(r['expected_action'] != 'unknown' and r['action'] == 'unknown' for r in rows)}")
    print(f"  hand-over rate           {sum(r['action'] in ('unknown', 'prepare', 'recommend') for r in rows) / len(rows):.0%}")
    print(f"  policy blocks            {sum(r['policy'] == 'block' for r in rows)}")
    return n_ok / max(len(auto), 1)


def run(path=EVAL_SET):
    with open(path, newline="", encoding="utf-8") as f:
        cases = [c for c in csv.DictReader(f) if c.get("case_id")]
    rows = []
    for c in cases:
        receipt = run_one(c)
        rows.append({**receipt,
                     "split": "demo" if c["case_id"] in DEMO else "held-out",
                     "amount": router.amount(c["amount_eur"]),
                     "expected_action": c["expected_action"],
                     "expected_clause": c["expected_clause"],
                     "ok": receipt["action"] == c["expected_action"] and receipt["clause_id"] == c["expected_clause"]})

    print(f"{'id':7} {'split':8} {'amount':>7}  {'expected':28} {'got':28} ok")
    for r in rows:
        exp = f"{r['expected_action']} {r['expected_clause']}".strip()
        got = f"{r['action']} {r['clause_id'] or r['reason']}"
        print(f"{r['case_id']:7} {r['split']:8} {str(r['amount']):>7}  {exp[:28]:28} {got[:28]:28} {'✓' if r['ok'] else '✗'}")

    held = [r for r in rows if r["split"] == "held-out"]
    headline = score(held, "HELD-OUT — the headline")
    score([r for r in rows if r["split"] == "demo"], "DEMO — read while writing the rules, not the headline")

    print("\nmisses by cause (held-out first):")
    misses = sorted((r for r in rows if not r["ok"]), key=lambda r: (r["split"] != "held-out", r["case_id"]))
    causes = Counter(f"{r['expected_action']} {r['expected_clause'] or '-'} → {r['action']} {r['clause_id'] or r['reason']}"
                     for r in misses)
    for cause, n in causes.most_common():
        ids = ", ".join(r["case_id"] for r in misses
                        if f"{r['expected_action']} {r['expected_clause'] or '-'} → {r['action']} {r['clause_id'] or r['reason']}" == cause)
        print(f"  {n} × {cause}  ({ids})")

    refunds = Counter(r["merchant_id"] for r, c in zip(rows, cases) if r["action"] == "refund") if False else \
        Counter(c["merchant_id"] for r, c in zip(rows, cases) if r["action"] == "refund")
    flagged = [m for m, n in refunds.items() if n >= 2]
    print(f"\nsplit_flag (≥ 2 sub-€20 refunds, same merchant): {', '.join(flagged) or 'none'}")

    invariants_ok = all(not (r["action"] == "refund" and (r["evidence"] == "NOT_FOUND" or (r["amount"] or 0) >= 20))
                        for r in rows) and not any(r["expected_action"] == "unknown" and r["action"] != "unknown" for r in held)
    if headline >= CRITERION and invariants_ok:
        print("\nverdict: PASS")
    else:
        print("\nverdict: FAIL — do not change the rules to fit the rows; propose the change to spec.md")

    with open(RESULTS, "w", newline="", encoding="utf-8") as f:
        fields = ["case_id", "split", "expected_action", "action", "expected_clause", "clause_id", "trust_level",
                  "amount_eur", "reason", "policy", "evidence", "clause_text", "model_version", "policy_version",
                  "created_at", "grader_A_would_execute", "grader_B_would_execute"]
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"\nreceipts written to {RESULTS.relative_to(ROOT)} (two empty grader columns for the hand grading)")
    return rows


if __name__ == "__main__":
    run()