"""Step 2 — the routing rule (rung 1), spec §2.2. No evidence, no decision."""
import re

from retrieve import STATUSES

TRACKING_FORMAT = re.compile(r"^LF-\d{8}$")


def gate(tracking_number, carrier_record):
    """Return None if the case may be decided, otherwise the reason it goes to a person."""
    if not TRACKING_FORMAT.match((tracking_number or "").strip()):
        return "no_tracking_evidence"
    if not (carrier_record or "").strip().startswith(STATUSES):
        return "no_tracking_evidence"
    return None