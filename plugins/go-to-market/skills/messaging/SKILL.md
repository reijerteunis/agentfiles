---
name: messaging
description: Turns positioning into a message house, messages per persona and buying stage, objection answers and a proof bank, with a script that flags claims without proof in any draft. Use it when someone wants a value proposition, messaging framework or elevator pitch, or wants copy checked for unsupported claims. Not for working out the positioning itself (use positioning).
license: MIT
compatibility: Runs a Python 3 script on markdown drafts.
---

# Messaging

Messaging says the positioning in the customer's words, the same way everywhere. Every claim in it is true and provable, because one claim a sophisticated buyer doesn't believe costs more than ten good ones earn.

## 1. The proof bank

Build `strategy/proof.md` first; every other asset cites it.

```markdown
- [p-1] Checkout drop-off cut from 31% to 22% at Brightcart (case study, 2026-09, permission: named, quote)
- [p-2] 14 of 15 pilot users kept using it after the trial (product analytics, 2026-10, permission: anonymous)
- [p-3] Pro plan is €49 a month (pricing.md, 2026-10, permission: public)
```

Each entry has an ID, the claim with its number, the source, the date, and the permission: `public`, `anonymous`, `named`, `logo` or `quote`. Mark retired entries `(expired)` instead of deleting them. Proof older than 18 months counts as stale.

## 2. The message house

1. **Umbrella message:** one sentence that carries the positioning: for whom, the value, the difference.
2. **Three pillars:** the value themes from positioning, each with a one-line claim and two or three proof points.
3. **Objections:** the five that buyers raise most, each with a short, honest answer and its proof.
4. **Boilerplate:** 25, 50 and 100 words.

## 3. By persona and stage

A matrix with, for each persona, what they care about, the pillar that leads, the proof they trust, and the call to action at each stage: aware of the problem, comparing options, deciding. Champions need ammunition for their boss, economic buyers need the outcome and the risk, and users need to see their day get better.

## 4. Words

- Use the customer's words from interviews and calls, not internal jargon or category buzzwords.
- Concrete beats clever: numbers, before and after, named customers where permitted.
- Taglines are optional, and come last.

## 5. Check every draft

While drafting, put the proof ID after each claim, in the same sentence: `Checkout drop-off went from 31% to 22% [p-1].` Then run:

```bash
python3 scripts/proof_check.py draft.md strategy/proof.md
```

It flags every sentence with a number or a superlative ("best", "fastest", "the only", "#1", "guaranteed", "compliant") that cites no proof, every ID that's missing, expired or stale, and every bank entry without a date or permission. Fix each flag: add proof, narrow the claim to what's true, or cut it. Mark a line that holds no claim despite a number, such as an address, with `<!-- no-claim -->`. When it passes, print the clean copy without IDs:

```bash
python3 scripts/proof_check.py draft.md strategy/proof.md --strip > final.md
```

## Gotchas

- "Up to" and best-case numbers mislead. Use the typical result, or say it's the best case.
- A result only some customers got keeps its share next to it every time it appears, paraphrases included: "checkout time halved for 3 of our 12 pilot stores", never "pilot stores halved checkout time". A proof ID isn't a qualifier, because it's stripped from the final copy. Regulators judge the impression a line leaves, and a qualifier elsewhere on the page doesn't fix it (FTC Endorsement Guides, 16 CFR 255.2; in the EU for B2B, Directive 2006/114/EC on misleading advertising).
- Quotes, names and logos need written permission, recorded in the bank. Anonymous proof stays anonymous everywhere.
- Health, financial and environmental claims are regulated in most countries; flag them for review.
- Realistic AI-generated images, audio or video of people, places or events need a disclosure under the EU AI Act (Article 50, from 2 August 2026).

## Output

`strategy/messaging.md` (the house, the matrix, the objections and the boilerplate) and `strategy/proof.md`. In the reply, show the umbrella message, the pillars, and the claims that still need proof.
