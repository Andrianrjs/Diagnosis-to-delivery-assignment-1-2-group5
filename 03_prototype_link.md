# 03 — Prototype link · LabelFlow refund agent

Group 5 · Raveloarimanga Rajesy Ny Andrian · Clémence Marco · 8 November 2026

## The link

**https://claude.ai/artifact/VStzhtuqFovQEqNkgdwgpE**

> **Sharing:** the artifact is private by default. Open it, use Share, and give access to
> anyone who needs to run the usability test or grade it — otherwise the link returns
> nothing for them.

Built with a Claude artifact (one of the tools the assignment allows), in under an hour,
as a single HTML page. No backend, no real billing call: nothing in it moves money.

## What it is

The surface named in `03_product_brief.md` §6: the decision panel the tier-1 agent sees
inside the support console, on a refund ticket they already have open. Left rail is the
refund queue; selecting a ticket shows the agent's decision receipt — the policy clause it
applied, the tracking evidence it relied on, the amount, and the trust level — with an
Execute / Escalate pair of buttons.

It is deliberately not a chat window. The agent's output is a record, not a conversation,
and the prototype exists to test whether that record reads.

## What it demonstrates, and what it deliberately does not

| Shows | Does not |
|---|---|
| The receipt as the product: clause, evidence, amount, trust level | Any real policy text or real carrier data |
| The €20 ceiling as a hard line — EV-010 at exactly €20.00 cannot settle itself | Model inference of any kind: every decision is pre-labelled |
| The evidence gate — EV-007 has no tracking number and Execute is disabled | The L2 approval queue (SHOULD, not MUST) |
| Escalation reachable from every case, including the ones it can decide | Billing, auth, merchant-facing views |
| Conflicting clauses handled by stopping, not choosing (EV-018) | Anything in the WON'T column |

## The six cases loaded

Drawn from `evals/eval_set_v0.csv`, chosen to cover one case per decision path rather than
six easy ones:

| Case | Amount | What it exercises |
|---|---|---|
| EV-001 | €12.40 | L4 happy path — settles alone |
| EV-010 | €20.00 | The ceiling, exactly on the line — prepares, person approves |
| EV-007 | €13.10 | No tracking evidence — execution blocked in code |
| EV-013 | €10.50 | A refusal, prepared at L2 because a wrongful refusal is silent |
| EV-012 | €240.00 | L1 — the agent only recommends |
| EV-018 | €11.75 | Two clauses conflict — the agent stops |

## The prompt used to build it

> Build a single-page prototype of the decision panel a tier-1 support agent sees inside
> LabelFlow's support console, on a shipping-label refund ticket. Left: the refund queue.
> Right: the agent's decision receipt for the selected ticket — policy clause applied,
> tracking evidence retrieved, amount, trust level — plus Execute and Escalate buttons.
> Enforce the governance rules visibly: under €20 the agent settles alone (L4), from €20 to
> €100 it prepares and a person approves (L2), above €100 it only recommends (L1), and with
> no tracking evidence Execute is disabled and the case can only be escalated. Load the six
> cases from our eval-set, including the €20.00 boundary case and the conflicting-clause
> case. No real data, no money moves, and label it a prototype.

## The task given to testers

> "A merchant has written in about a €12 shipping-label refund. Decide what LabelFlow
> should do about it, and tell me how you know."

Think aloud, no help. What we are watching for: whether they read the evidence block before
the verdict or after, whether they can say what would have made the answer different, and
whether they notice that EV-010 cannot be executed and understand why.

Results go in `03_user_research.md`.
