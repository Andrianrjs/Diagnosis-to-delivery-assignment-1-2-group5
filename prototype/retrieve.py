"""Step 3 — retrieve (rung 1), spec §2.3. The carrier record and the policy clauses.

In v0 the carrier API is replaced by the `evidence` column of the eval-set.
"""
import re
from pathlib import Path

POLICY_FILE = Path(__file__).resolve().parent.parent / "kb" / "refund_policy.md"
STATUSES = ("NO_SCAN", "IN_TRANSIT", "DELIVERED", "RETURNED_TO_SENDER")


def load_clauses(path=POLICY_FILE):
    """Return {clause_id: text}, one entry per '## POL-…' heading. Other headings are not clauses."""
    clauses, current = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            current = heading.split(" · ")[0].strip() if heading.startswith("POL-") else None
            if current:
                clauses[current] = []
        elif current:
            clauses[current].append(line.strip())
    return {cid: " ".join(l for l in lines if l) for cid, lines in clauses.items()}


CLAUSES = load_clauses()


def tracking(carrier_record):
    """Parse a carrier record that the routing rule has already accepted."""
    record = carrier_record.strip()
    text = record.lower()
    days = re.search(r"(\d+)\s*days?", record)
    return {
        "status": next(s for s in STATUSES if record.startswith(s)),
        "days": int(days.group(1)) if days else None,
        "duplicate_charge": "duplicate" in text,
        "prior_refund": "prior receipt" in text,
        "damage_claim": "damage claim" in text,
        "disputed": "disputes" in text,
    }