---
name: idea-screen
description: Captures a business idea as a one-page card and scores it against the founder's own criteria, naming the riskiest assumptions and the first cheap test. Use it when someone shares a startup idea, asks "is this a good idea?", or wants to compare ideas. Not for analysing an existing company (use company-research or market-map).
license: MIT
---

# Idea screen

The point isn't to judge an idea as good or bad. It's to find out, quickly and honestly, whether it deserves the founder's scarce evenings, and what would have to be true for it to work.

## Capture the card

Write `ideas/<slug>/idea.md` with the frontmatter from the venture-lab workspace reference, then:

- **Problem:** what hurts, for whom, how often, and what they do about it today.
- **Customer:** the first specific group to sell to ("independent accountants with 2–10 staff in NL"), not a market category.
- **Who pays and why now:** the buyer, the budget it comes from, and what changed that makes this possible or urgent now.
- **The founder's edge:** why this founder, with these skills, network or insight, wins here.
- **Model guess:** how money comes in, at a guessed price.

Ask for what's missing; don't invent a customer to make the card complete.

## Score

Use the founder's criteria from `profile/criteria.md` when they exist. Otherwise use this default, each scored 0–10 with a one-line reason:

| Criterion | Weight |
|---|---|
| Founder-problem fit: they know this problem or this customer first-hand | 15 |
| Pain: frequent and costly, and the current workaround is painful | 20 |
| A buyer with budget: someone specific pays, and the budget exists | 15 |
| Market: big enough for the founder's ambition (lifestyle or venture) | 10 |
| Timing: a real "why now" | 10 |
| Edge: an unfair advantage, an insight or distribution | 15 |
| Feasibility: a small team can ship a first version in about 8 weeks | 10 |
| Path to revenue: the first paying customer within about 3 months is plausible | 5 |

The weighted total, out of 100, is the screen score. A **deal-breaker** in the founder's criteria (for example "competes with my employer") means kill, whatever the score.

## Riskiest assumptions and the first test

List the three assumptions that, if wrong, kill the idea. Usually one each for desirability (they want it), viability (they'll pay enough) and feasibility (we can build and deliver it). Rank them by how much is known about each. Propose the first test for the riskiest one: usually five problem interviews, before anything else.

## Recommend

- **Explore** (60 or more): set `stage: explore`, the `next_step`, and a `decide_by` date 2–3 weeks out.
- **Park** (45–59, or not the right time): `status: parked`, with what would make it worth reopening.
- **Kill** (under 45, or a deal-breaker): `status: killed`, with the reason in one line. A killed idea is a good outcome. Say so.
