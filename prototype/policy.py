"""Step 5 — the policy check (rung 1), spec §2.5 and §5. Enforced in code, before anything is executed.

The ceiling is defined here again, independently of decide.py, on purpose: a bug in the
decision rules must not be able to move the line that blocks it.
"""
from pathlib import Path

SWITCH_FILE = Path(__file__).resolve().parent / "SWITCH_DOWNGRADE"
AUTO_CEILING = 20.00


def switch_on():
    """Kill switch ⏻: while this file exists, every refund is downgraded to prepare (L2)."""
    return SWITCH_FILE.exists()


def check(decision, evidence_found, amount):
    """Return ('pass', '') or ('block', reason)."""
    if decision["action"] != "refund":
        return "pass", ""
    if not evidence_found:
        return "block", "refund without tracking evidence"
    if amount is None or amount >= AUTO_CEILING:
        return "block", "refund at or above €20 without a person"
    return "pass", ""