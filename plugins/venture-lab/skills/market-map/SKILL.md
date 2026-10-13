---
name: market-map
description: Maps the market around an idea with bottom-up sizing by script, the real alternatives, a competitor teardown, positioning and why now. Use it when someone asks how big a market is, who the competitors are, or how to position an idea before it has customers. Not for positioning a product going to market (use positioning) or researching an employer (use company-research).
license: MIT
compatibility: Uses web search for research and runs a Python 3 sizing script.
---

# Market map

A good market map answers three questions: is there enough money here for the founder's ambition, what do customers do today instead, and where is the gap a newcomer can win? Use evidence and sources, not big top-down numbers.

## Size it bottom-up

1. Define the segments from the idea card: specific customer types in specific places.
2. For each, find the **number of customers** (statistics offices, industry associations, registries, LinkedIn counts) and a **price per year** (competitors' public pricing, or interview evidence). Every number gets a source, or is labelled as an assumption.
3. Put them in a `market.json` and run `python3 scripts/sizing.py market.json`. It computes:
   - **TAM:** everyone in the segments, paying full price.
   - **SAM:** the share you can actually serve with this product and these channels.
   - **SOM:** a realistic share in 3–5 years. For a newcomer that's usually a few percent of SAM.
4. Sanity-check the SOM: how many customers is that, and how many sales would it take per month to get there?

Never use "the global X market is $50B, we only need 1%". Investors and founders both stop listening at that sentence.

## Map the alternatives

Customers already solve the problem somehow. List the real alternatives, including **spreadsheets and email, an agency or freelancer, an in-house tool, a big suite's add-on, and doing nothing**, with why customers put up with each one today.

## Tear down competitors

For the top 3–5, using public sources only:

| | Who they serve | Pricing | Positioning | Strengths | Weaknesses | Recent moves |
|---|---|---|---|---|---|---|

Check reviews (G2, Capterra, app stores, Reddit) for the complaints that point to gaps.

## Position and timing

- **The gap:** the segment or job that's underserved, and why the incumbents won't fix it (their incentives, not just their roadmap).
- **The position,** in one sentence: "For <customer> who <need>, <product> is the <category> that <key benefit>, unlike <alternative>."
- **Why now:** the shift that makes this possible or urgent now, such as regulation, technology, behaviour or a cost change.

## Output

`market.md`: the sizing table (from the script) with its sources, the alternatives, the competitor teardown, and the position and why-now. Mark each assumption the market map supports or weakens in `assumptions.md`.
