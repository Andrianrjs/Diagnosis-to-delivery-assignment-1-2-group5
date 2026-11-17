"""Step 3 — the drafter. API if ANTHROPIC_API_KEY is set, else the template drafter (spec §2.3)."""
import os
from dotenv import load_dotenv
load_dotenv()

PROMPT = """You are a support copilot for Paylio (HR & payroll SaaS). Reply to the ticket using ONLY the passages below.
Cite every passage you use as [article · section]. If the passages do not answer the question, reply exactly NO_DRAFT.
Never quote a price, never promise a refund, never give legal advice. If the ticket asks two things, answer the first retrieved topic and say so.

Ticket: {ticket}

Passages:
{passages}
"""


def template_draft(ticket, passages):
    if not passages:
        return "NO_DRAFT"
    p = passages[0]
    first = p["text"].split(". ")[0].rstrip(".") + "."
    return f"Hi, here is how to do it: {first} [{p['article']} · {p['section']}] Let me know if that works."


def draft(ticket, passages):
    if not passages:
        return "NO_DRAFT"
    if not os.getenv("ANTHROPIC_API_KEY"):
        return template_draft(ticket, passages)
    try:
        import anthropic
        client = anthropic.Anthropic()
        ptxt = "\n\n".join(f"[{p['article']} · {p['section']}]\n{p['text']}" for p in passages)
        msg = client.messages.create(model=os.getenv("MODEL", "claude-sonnet-4-5"), max_tokens=400,
                                     messages=[{"role": "user", "content": PROMPT.format(ticket=ticket, passages=ptxt)}])
        return msg.content[0].text.strip()
    except Exception:
        return template_draft(ticket, passages)
