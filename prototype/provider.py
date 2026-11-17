"""promptfoo custom provider: runs the starter's four steps and returns the draft (or NO_DRAFT).
Place next to the starter's prototype/ files. promptfoo calls call_api(prompt, options, context)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import router, route_rule, retrieve, draft as drafter, policy


def call_api(prompt, options, context):
    ticket = context["vars"].get("ticket") or context["vars"].get("input_the_agent_receives") or prompt
    cat, conf = router.predict(ticket)
    decision = route_rule.decide(cat, conf, ticket)
    passages = retrieve.top_k(ticket) if decision == "draft" else []
    text = drafter.draft(ticket, passages) if decision == "draft" else "NO_DRAFT"
    status, reason = policy.check(text)
    if status == "block":
        text = "NO_DRAFT"
    return {"output": text, "metadata": {"category": cat, "confidence": conf, "decision": decision, "policy": status, "reason": reason}}
