"""Step 4 — the policy checker (rung 1: rules). TODO: complete the patterns; return (status, reason)."""
import re

RULES = [
    (r"(€|\$|£)\s?\d|\d+\s?(€|euros|dollars)|\bprice\b|\bpricing\b", "mentions a price"),
    (r"\brefund(ed|s)?\b|\bcredit note\b", "promises a refund"),
    (r"\blegal(ly)?\b|\blawyer\b|\bcourt\b", "gives legal advice"),
]


def check(draft_text):
    """Return ('pass', '') or ('block', reason)."""
    if draft_text == "NO_DRAFT":
        return "pass", ""
    for pat, reason in RULES:
        if re.search(pat, draft_text, flags=re.I):
            return "block", reason
    return "pass", ""
