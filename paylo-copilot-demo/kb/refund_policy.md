# LabelFlow refund policy — shipping labels

> Policy version **2026-11-v0**. Invented for the course: LabelFlow is a case, not a client.
> One clause per `## ` heading. The heading starts with the clause id the agent cites in its receipt,
> and the ids match the `expected_clause` column of `evals/eval_set_v0.csv`.
> Any change to this file is a new policy version: the eval-set must be replayed before the agent runs again.

## POL-4.2-unused-label · Unused label

A label that has received **no carrier scan 14 days after purchase** is refunded in full.
Before day 14 the label is still valid and can still be used: it is not refunded, and the merchant may ask again from day 14.
Day 14 itself is refundable.

## POL-4.5-consumed-label · Consumed label

A label that has been **scanned by the carrier** (in transit or delivered) has been consumed and is not refunded,
whatever the merchant says about it. The decision follows the carrier record, not the merchant's description.

## POL-4.6-return-to-sender · Returned to sender

A parcel **returned to sender after delivery attempts** has used its label: the carrier carried it.
The label is not refunded.

## POL-5.3-lost-in-transit · Lost in transit

A parcel with **no carrier event for 21 days after its last scan** is treated as lost, and its label is refunded.
Day 21 itself is refundable. Before day 21 the parcel is not yet considered lost: the claim is refused under
this clause and the merchant may ask again from day 21.

## POL-6.1-duplicate-charge · Duplicate charge

A label **charged twice** is refunded for the duplicate charge, whatever the delivery status of the parcel.
The claim is about the charge, not the parcel.

## POL-6.3-already-refunded · Already refunded

A label already refunded under an **earlier receipt** is not refunded again. The receipt cites the earlier receipt id.

## POL-7.2-damage-not-label · Damage is not a label refund

Damage to a **delivered** parcel is a claim against the carrier, not a label refund. The label is not refunded;
the merchant is pointed to the carrier damage-claim process.

## Thresholds and authority (not a clause — read by the agent, never cited)

- Amount **strictly below €20.00**: the agent settles alone (L4); a person reviews a weekly sample.
- **€20.00 to €100.00 inclusive**: the agent prepares the decision; a person approves before any money moves (L2).
- **Above €100.00**: the agent only recommends; a person decides (L1).
- **Any refusal**, at any amount: prepared by the agent, confirmed by a person (L2).
- **No refund without carrier tracking evidence**, ever.
- When two clauses would both grant a refund for different amounts, or no clause applies, the agent does not choose: a person decides.