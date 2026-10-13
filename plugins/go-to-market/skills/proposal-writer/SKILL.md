---
name: proposal-writer
description: Writes proposals, statements of work and quotes with the client's goals in their words, outcomes, scope, two or three options priced within the pricing policy, terms and next steps, as drafts that never offer a discount outside the policy. Use it when someone needs to send a proposal, quote, SOW or pilot offer. Not for technical design proposals (use tech-spec) or job offers (use offer-negotiation).
license: MIT
---

# Proposal writer

A proposal confirms a decision the buyer is already close to making. It holds no surprises, reads in five minutes, and makes saying yes easy.

## Inputs

The deal file and call notes (pain, impact, critical event, decision process), the pricing policy, the proof bank and the person's standard terms.

When some of these are missing, still write the draft the person asked for. Put a marked placeholder such as `[price from the pricing policy]` wherever a fact is missing, never a guess, and end with the short list of what's needed to finish it. Without a discovery call, say in the note to the person that the proposal is premature and recommend the call.

## Structure

1. **Their situation and goals,** in their words, with the impact they quantified.
2. **The outcome:** what will be true afterwards, and how both sides will measure it.
3. **The approach:** the phases or steps, and what the client gets from each.
4. **Scope:** what's included, and what's explicitly not.
5. **Options:** two or three, priced within the policy, with the middle one recommended. For services, a fixed fee per phase beats hours; for software, the plan, seats or usage, the term and onboarding.
6. **Timeline:** the start date, the milestones, and the critical event it meets.
7. **Assumptions and dependencies:** what the client provides (access, people, data, decisions) and by when.
8. **Proof:** one or two relevant results, with proof IDs.
9. **Terms:** how long the offer is valid, payment terms, which standard terms apply, and anything that needs legal review (liability, IP, data processing, service levels).
10. **Next steps:** how to accept, and what happens in the first week.

## Pricing discipline

- Prices and discounts follow `strategy/pricing.md`. Every discount is traded for something: a longer term, prepayment, a case study, a reference or a faster signature.
- Anything outside the policy is marked **NEEDS APPROVAL** with the reason, in a note to the person, and stays out of the client's draft until the person decides.
- Free extras that lower the effective price (extra services, training or support, price locks or renewal caps, longer payment terms) count as discounts: the same policy, the same trade, the same approval. A cheaper option with less scope isn't a discount.
- State VAT, the currency and the payment terms.

## Pilots

For a new or risky deal, offer a paid pilot: a fixed scope over four to eight weeks, success criteria agreed upfront, and the price of the full engagement agreed in advance for when the criteria are met.

## Check before delivering

1. Run the `messaging` skill's proof check on every claim.
2. Read it as the economic buyer: is the outcome clear, does the impact justify the price, is the risk handled?
3. If it's available, have the `skeptical-buyer` agent review it.

## Output

`drafts/proposals/<company>-<date>.md`, and a version formatted for PDF if asked. The deal moves to stage `proposal`, with the next step "review with <name>" and a date. The person sends it. Contracts and legal terms go to a lawyer.
