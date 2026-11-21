# Governance  LabelFlow refund agent

Group 5 · Raveloarimanga Rajesy Ny Andrian · Clémence Marco

## 1. What is the one job, in one sentence?

When a merchant requests a refund for a shipping label, the agent checks eligibility against the refund policy and the package-tracking evidence, then settles, prepares or recommends the refund according to its amount, producing a decision receipt in every case.

## 2. What must it never do?

Two absolute prohibitions, both testable in the eval-set:

- never refund without package-tracking evidence attached to the decision receipt;
- never refund more than €20 on its own authority.

A third, operational: never close a case without a receipt. A decision with no receipt is a decision nobody can audit, and in a money-moving flow that is the same as no control.

## 3. What is the trust level per step?

| Step | Level | What that means |
|---|---|---|
| Read the policy and the tracking evidence | L4 | Autonomous, read-only, no money moves |
| Decide and execute a refund under €20 | L4 with after-the-fact review | Acts alone; a human reviews a sample weekly |
| Decide a refund between €20 and €100 | L2 | Prepares the decision and the receipt; a human approves before execution |
| Decide a refund over €100 | L1 | Recommends only; the human decides |
| Refuse a refund, any amount | L2 | A refusal is a commercial act: prepared by the agent, confirmed by a human |

Refusals sit at L2 deliberately. An over-refund is visible in the accounts; a wrongful refusal is visible only as churn, months later.

The sizing follows these levels rather than assuming them away: `02_sizing.xlsx` prices one supervision FTE as a cost line, and the €20–100 band is entered as 0.38 ticket-equivalents rather than full deflection, because the human approval step is never removed.

## 4. Who is accountable when it is wrong?

Accountability does not move to the vendor, the model, or the agent. *Moffatt v. Air Canada* (2024 BCCRT 149) settled the point: the airline argued its chatbot was a separate legal entity responsible for its own actions, the tribunal disagreed, and LabelFlow would be in the same position. This holds under orchestration too, which is why Assignment 2 recommends renting the resolution layer while keeping the policy, the receipt and the eval-set in-house.

- Head of Support Operations: owns the agent's decisions as if they were an agent's, owns the weekly sample review, and owns the kill-switch.
- Finance: owns the refund-leakage line and the monthly reconciliation.
- Legal: owns the wording of the receipt and of any automated refusal.
- The product owner of the agent: owns the eval-set and the re-evaluation at every model change.

## 5. What is logged, and for how long?

Every decision writes a receipt: input request, policy clause applied, tracking evidence and its timestamp, amount, decision, trust level at which it was taken, model version, and the identity of the approving human where one was required. Receipts are retained for the statutory accounting period and are the evidence base for the eval-set and for any dispute. Merchant personal data in the receipt is limited to what the decision required (GDPR minimisation); the receipt is the merchant's on request.

## 6. How does a merchant reach a human, and how do we roll back?

Every agent decision carries a one-click escalation that routes to a human with the full case context, and the merchant is told the decision was automated. A merchant may not be left with no route to a person: that is the omission the Klarna case exposed, where the customers who could not reach a human had no line in the business case.

Rollback is a downgrade, not a shutdown: the kill-switch moves every case to L2 (the agent prepares, a human approves). Turning the agent off entirely returns the queue to a 3-day wait, so it is the last resort, not the first.

Rollback triggers (any one moves every case to L2):

- **Money trigger (primary):** refunded amount on agent-settled cases exceeds the pre-agent
  baseline by more than **€1,500 over a rolling 7 days** — roughly the agent's weekly net
  value (€80k/year in `02_sizing.xlsx`). Above that, leakage erases what the agent saves.
  _Guess — to be recalibrated once the 3-month refund export gives the real baseline._
- any refund executed without tracking evidence (zero tolerance);
- wrongful-refusal rate (refusals overturned after dispute) above the human baseline over
  a rolling 7 days;
- refunded amount per merchant jumping without a matching request volume (splitting signal);
- a model-version change that has not passed the eval-set replay.

---

## Assignment 1 — the six governance questions (provisional)

Status legend:  answered · 🔍 to check before launch

**1. EU AI Act risk tier — Limited risk (provisional).**
The agent decides shipping-label refunds for business customers. It is not in Annex III:
no creditworthiness scoring, no access to essential services for natural persons, no
employment decision. Transparency obligations apply: merchants are told the decision was
automated (see §6).
🔍 Some merchants are sole traders (natural persons) — confirm this does not change the
tier, and check whether GDPR Art. 22 (solely automated decisions) applies to an automated
refusal. Our design already gives a human route on every decision.

**2. Whose data, on what legal basis.**
- Merchant account and contact data, refund history → **contract** (GDPR Art. 6(1)(b)):
  processing the refund the merchant asked for.
- Monitoring for errors, fraud and request splitting; the receipt audit log →
  **legitimate interest** (Art. 6(1)(f)).
- Receipt retention for the accounting period → **legal obligation** (Art. 6(1)(c)).
- Package-tracking data contains the **merchant's end-customers'** names and addresses:
  third-party data, used only to confirm delivery or return, and kept out of the receipt.
🔍 Confirm LabelFlow's role (controller vs. processor) for end-customer data in the
merchant contract; check the vendor's data location and sub-processor terms if we
orchestrate (Assignment 2).

**3. Who is accountable, and where is the human.** ✅
Accountability stays with LabelFlow (§4, _Moffatt v. Air Canada_). The human sits after
the decision under €20 (weekly sample), before it between €20 and €100, and decides
above €100 and on every refusal (§3).
🔍 Name the Head of Support Operations and the Legal owner before launch.

**4. What it must never do.** ✅
Refund without tracking evidence; refund more than €20 on its own; close a case without
a receipt (§2).

**5. Explainable to whom.**
- **Merchant:** the decision receipt, in plain language — clause applied, evidence, amount.
- **Support reviewer:** the same receipt plus the raw evidence, to confirm or overturn.
- **Finance:** daily reconciliation of refunded amounts against the baseline.
- **Auditor / Legal:** the full log — model version, trust level, approving human (§5).
🔍 Test receipt readability with 5–10 merchants (H3, Session 5).

**6. What happens to the people it cannot serve.**
Cases with missing or ambiguous tracking, non-standard carriers, policy exceptions, or
merchants who dispute: **missing evidence means escalation, never refusal.** These cases go
to a human with the full context — no worse than today's 3-day queue — and every merchant
has a one-click route to a person (§6).
🔍 Measure the escalation share on the 200 Session 4 tickets; if it exceeds ~30 %, the
agent serves too few cases to be worth it.



---

## Session 2 line — the cost-of-error line that is a legal or reputational risk

Of the seven cost lines in `02_sizing.xlsx`, the cost of error is the one that is not only money. It is priced at **€25 per wrong answer in the sub-€20 band and €55 in the €20–100 band**, and at base it absorbs **€19.2k a year, 22 % of the gross value the agent creates**. Both figures are guesses until the Session 5 eval-set exists, and both are labelled as such in the sheet.

**The line:** an automated refusal of a refund, or a refund executed on misread tracking evidence, where the decision receipt states a policy clause the agent applied incorrectly.

**Why it is not just money.** Priced as money, one wrong refusal is a €12 refund and a re-opened ticket. The real exposure is elsewhere. The receipt is a written statement by LabelFlow about its own policy, sent to a professional customer: if it misstates the policy, it is a representation the merchant can rely on, and *Moffatt v. Air Canada* confirms the company carries that liability whatever produced the text. A systematic misreading applied to thousands of receipts is not an incident, it is a pattern across the merchant base, discoverable in our own logs. Reputationally, a logistics SaaS that refuses small refunds automatically and wrongly loses merchants without ever receiving a complaint — the failure is silent on both sides of the ledger, which is why the sizing carries a daily reconciliation of refunded amounts rather than relying on complaints to surface it.

**Owner:** Head of Support Operations, accountable for the decision; Legal, accountable for the wording of the receipt and of any automated refusal; both named before launch, and the eval-set carries a dedicated wrongful-refusal slice reviewed at every model change.
	


---

## Session 4 — checkpoints, switch, eval data

Written against the prototype at tag `eval-v0` (`04_architecture.md`) and its eval (`evals/report_v0.md`).

### Human checkpoints ⊘

| Where | Type | Who | What they see | Evidence it holds (eval-v0) |
| --- | --- | --- | --- | --- |
| Refund under €20 settled by the agent (L4) | sampling, after the fact | Head of Support Operations, weekly sample | the receipt: clause, carrier evidence, amount | 0 refunds ≥ €20 alone, 0 refunds without evidence |
| Refund €20–100 prepared by the agent (L2) | approval, before any money moves | tier-1 support agent | the prepared receipt, Execute / Escalate | EV-010 (€20.00), EV-034 (€100.00) prepared, not settled |
| Any refusal, at any amount (L2) | approval | tier-1 support agent | the receipt and the clause cited | 11/11 held-out refusals prepared, none sent alone |
| Refund over €100 (L1) | the person decides | tier-1 support agent | the agent's recommendation only | EV-035 (€100.01) recommended |
| Cases the agent stops on | abstention → person | tier-1 support agent | the receipt with the reason (`no_tracking_evidence`, `language_not_covered`, `amount_missing`, `evidence_contradicts_merchant`, …) | 5/6 held-out human-only cases stopped; **EV-050** was decided — the miss that fails eval-v0 |

The checkpoint that failed is the abstention before the clause rules: the rules read fields and missed an exception written in prose. `spec.md` v2 adds a `policy_exception` stop; until it is built and re-evaluated, the agent stays a prototype.

### The switch ⏻

- **Owner:** the Head of Support Operations (§4). The agent's product owner may also trigger it on a failed eval replay; only the Head of Support Operations clears it.
- **What it does:** every refund the agent would settle alone becomes `prepare` (L2) — the agent prepares, a person approves. It is a downgrade, not a shutdown, consistent with §6: switching the agent off entirely would return the queue to a three-day wait.
- **Scope:** every merchant, every case. v0 has no per-merchant switch (`04_architecture.md` §9).
- **When it must be pulled:** the triggers in §6 — refunded amount on agent-settled cases more than **€1,500** above the pre-agent baseline over a rolling 7 days (this figure supersedes the €2,000 in `03_product_brief.md` §8); any refund without tracking evidence; wrongful-refusal rate above the human baseline; a splitting signal; a model or policy version that has not passed the eval-set replay.
- **Tested:** 17 November 2026 (`04_architecture.md` §6).

### Where the eval data is stored, and who sees it

- `evals/eval_set_v0.csv` — 50 synthetic cases, in this repository, readable by the team and the course staff. No real merchant, end-customer or carrier data; tracking numbers and receipt ids are invented.
- `evals/results_v0.csv` — the receipts of the eval-v0 run, with two grader columns. Receipts never copy the merchant's free text (GDPR minimisation, `spec.md` §3).
- **Frozen at tag `eval-v0`.** EV-021 to EV-050 have now been read while writing `spec.md` v2, so they are no longer held-out for v2: the next eval needs a fresh slice (the 200-case set, Session 5).
- **In production** (not built): the eval-set would be drawn from real tickets, pseudonymised (merchant id hashed, end-customer names and addresses removed from tracking events), stored with the receipt audit log, access limited to Support Operations and the agent's product owner, and owned by the product owner (§4), who replays it at every model or policy change.


---

## Session 5 — counter-metrics, segments, harm threshold

Written against `05_metrics.md` §3.

- **Counter-metrics:** refund leakage (€ refunded on agent-settled cases minus the pre-agent baseline, rolling 7 days, band ≤ €1.5k, owner Finance); wrongful refusals (refusals overturned after a dispute / refusals sent) and the 90-day churn of merchants who received a refusal (owner Head of Support Operations, with Legal).
- **Segments reported:** language (FR · EN · other), plan (standard · high-volume · enterprise), amount band (< €20 · €20–100 · > €100), carrier status. Fairness metric: selection-rate parity by language and plan, read with equal error rates. Known gap, chosen: requests outside FR and EN are never decided, and are protected by the "person reached" guardrail.
- **Harm threshold that stops the rollout:** "If, on any language or plan segment, the wrongful-refusal rate exceeds that segment's pre-agent human rate, or the abstention guardrail records a decided human-only case, over two consecutive weeks, the agent drops to L2 (prepare only) on that segment until the gap is explained. Owner: Head of Support Operations; reviewed with Legal monthly."
- **Prerequisite:** v0 has no per-segment switch (`04_architecture.md` §6); the threshold above needs one in `spec.md`.

## Sessions 6-7 — experiments and operation

- **Experiments on real users.** Any experiment on real merchants is signed by the Head of Support Operations and read by Legal before it starts; the decision rule and the harm threshold are written before the first unit (`06_07_experiments_operations.md` §2).
- **The switch.** The Head of Support Operations can move the system to suggest-only (`SWITCH_DOWNGRADE`, every refund prepared at L2) or off, by day; the automatic leakage and invariant triggers by night. Last tested 17 November 2026, next test before the first real merchant enters shadow mode.
- **The trace.** One line per output, kept 10 years at the receipt log (an accounting record, Code de commerce art. L123-22); full step traces 90 days in Phoenix, to cover the 90-day churn read. Proposed, to be confirmed by Finance and Legal. Legal answers a customer or a regulator from it.

## Session 8 — who signs the launch

- This launch (conditional go to step 0, shadow mode on sub-€20 FR and EN requests, from 7 December 2026) is signed by the Head of Support Operations and Finance; Legal has read the protocol.
- Merchants receive the agent's decision directly when it settles a refund under €20 alone (L4), so they are told it was automated: the first line of every receipt reads "This decision was made automatically by LabelFlow's refund assistant. Reply or click 'Talk to a person' to reach our team." (EU AI Act art. 50, from 2 August 2026). Refusals and refunds from €20 are approved by a person before they are sent.
- The rollback plan (06_07 §4) was last tested on 17 November 2026 by Raveloarimanga Rajesy Ny Andrian; next test: before shadow mode starts, 7 December 2026.