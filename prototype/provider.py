"""promptfoo custom provider (Session 5): runs the five steps of spec §2 on one case and returns the receipt."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import evals  # noqa: E402


def call_api(prompt, options, context):
    v = context.get("vars", {})
    case = {
        "case_id": v.get("case_id", "adhoc"),
        "input_text": v.get("input_text") or v.get("ticket") or prompt,
        "amount_eur": v.get("amount_eur", ""),
        "tracking_number": v.get("tracking_number", ""),
        "evidence": v.get("evidence", ""),
    }
    receipt = evals.run_one(case)
    return {"output": json.dumps(receipt, ensure_ascii=False), "metadata": receipt}