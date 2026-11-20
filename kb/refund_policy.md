# LabelFlow · Shipping-label refund policy

Version 2026-11-v1 · 20 November 2026 · invented for the course: LabelFlow is a case, not a client.
First written text of the policy. The eval-v0 receipts cite policy version `2026-11-v0`, which had no text in the repository.

Only the headings that start with `POL-` are clauses; the prototype loads them one per heading (`prototype/retrieve.py`). The other sections say who decides and how clauses combine.

## Scope and authority

This policy covers refunds of shipping labels bought on LabelFlow. It does not cover compensation for the goods inside the parcel, which is a claim against the carrier. Every decision rests on the carrier record of the tracking number; the merchant's own account of events is read, never used as evidence. Below €20.00 the refund agent may settle a refund alone. From €20.00 to €100.00 it prepares the decision and a support agent approves it. Above €100.00 it recommends and a support agent decides. Every refusal, at any amount, is confirmed by a support agent before it is sent.

## Cases a person always decides

A support agent decides, and the refund agent hands the case over with its reason, when: the carrier record is missing, unreadable or lacks the elapsed days a clause needs; the record contradicts the merchant (delivered, but the merchant says it never arrived); the merchant describes a situation no clause covers (carrier stopped operating in the region, carrier bankruptcy, strike, natural disaster, customs seizure); the request is written in a language other than French or English; the amount is missing; or two clauses would each refund the same request.

## POL-4.2-unused-label · Unused label

A label that the carrier has never scanned is refunded in full once 14 days have passed since its purchase with no carrier event. Before day 14 the label can still be used and is not refunded; the merchant may ask again from day 14. Evidence: carrier status NO_SCAN and the number of days since purchase.

## POL-4.5-consumed-label · Consumed label

A label that the carrier scanned and delivered has been used: the shipping service was provided and the label is not refunded. Evidence: carrier status DELIVERED.

## POL-4.6-return-to-sender · Return to sender

A parcel returned to the sender after the carrier's delivery attempts has used its label: the attempts were made and the label is not refunded. Shipping the parcel again requires a new label. Evidence: carrier status RETURNED_TO_SENDER.

## POL-5.3-lost-in-transit · Lost in transit

A parcel with no carrier event for 21 days or more after its last in-transit event is considered lost, and its label is refunded in full. Before day 21 the parcel is not yet considered lost: the label is not refunded and the merchant may ask again from day 21. Compensation for the goods is a carrier claim outside this policy. Evidence: carrier status IN_TRANSIT and the number of days since the last event.

## POL-6.1-duplicate-charge · Duplicate charge

When the same label was charged twice on the same order, the duplicate charge is refunded, whatever the status of the parcel: the claim is about the charge, not the delivery. Evidence: two charges for the same label on the order.

## POL-6.3-already-refunded · Already refunded

A label already refunded under a previous receipt is not refunded again. The reply cites the previous receipt. Evidence: the earlier refund receipt for the same label.

## POL-7.2-damage-not-label · Damage is not a label refund

Damage to the goods is claimed from the carrier through its damage-claim process. The label was used to carry the parcel and is not refunded. Evidence: carrier status DELIVERED and a damage claim on file.
