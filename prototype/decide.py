"""Step 4 — decide (rung 1), spec §2.4. Clause rules first, then the amount band."""
import policy

UNUSED_DAYS = 14      # POL-4.2
LOST_DAYS = 21        # POL-5.3
AUTO_CEILING = 20.00
APPROVAL_CEILING = 100.00
NOT_RECEIVED = ("never received", "not received", "jamais reçu", "pas reçu")


def stop(reason):
    """A case the agent does not decide: it goes to a person with the reason."""
    return {"action": "unknown", "clause_id": None, "trust_level": "person", "reason": reason}


def clause_for(text, ev):
    """Return ('refund' | 'refuse', clause_id) or ('unknown', reason)."""
    if ev["prior_refund"]:
        return "refuse", "POL-6.3-already-refunded"
    status, days = ev["status"], ev["days"]
    if status == "DELIVERED" and (ev["disputed"] or any(p in text.lower() for p in NOT_RECEIVED)):
        return "unknown", "evidence_contradicts_merchant"

    refunds, refusals = [], []
    if ev["duplicate_charge"]:
        refunds.append("POL-6.1-duplicate-charge")
    if status == "NO_SCAN" and days is not None:
        (refunds if days >= UNUSED_DAYS else refusals).append("POL-4.2-unused-label")
    elif status == "IN_TRANSIT" and days is not None:
        if days >= LOST_DAYS:
            refunds.append("POL-5.3-lost-in-transit")
        else:
            refusals.append("POL-4.5-consumed-label")
    elif status == "DELIVERED":
        refusals.append("POL-7.2-damage-not-label" if ev["damage_claim"] else "POL-4.5-consumed-label")
    elif status == "RETURNED_TO_SENDER":
        refusals.append("POL-4.6-return-to-sender")

    # A duplicate charge overrides a status-based refusal: the claim is about the charge.
    if len(refunds) > 1:
        return "unknown", "conflicting_clauses"
    if refunds:
        return "refund", refunds[0]
    if refusals:
        return "refuse", refusals[0]
    return "unknown", "no_clause_matches"


def band(outcome, clause_id, amount):
    """The trust level comes from the amount field only, never from the merchant's text."""
    if outcome == "refuse":
        action, level = "refuse", "L2"
    elif amount < AUTO_CEILING and not policy.switch_on():
        action, level = "refund", "L4"
    elif amount <= APPROVAL_CEILING:
        action, level = "prepare", "L2"
    else:
        action, level = "recommend", "L1"
    return {"action": action, "clause_id": clause_id, "trust_level": level, "reason": outcome}


def decide(text, evidence, amount):
    outcome, value = clause_for(text, evidence)
    if outcome == "unknown":
        return stop(value)
    return band(outcome, value, amount)