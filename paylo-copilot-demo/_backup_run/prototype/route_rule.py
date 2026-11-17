"""Step 2 — the routing rule (rung 1), spec §2.2."""
import re
THRESHOLD = 0.70
HUMAN_ONLY = {"payroll", "billing", "other"}
MONEY_WORDS = re.compile(r"\b(refund|price|pricing|invoice|subscription|discount)\b", re.I)


def decide(category, confidence, text=""):
    if MONEY_WORDS.search(text or ""):
        return "escalate"
    if confidence < THRESHOLD or category in HUMAN_ONLY:
        return "escalate"
    return "draft"
