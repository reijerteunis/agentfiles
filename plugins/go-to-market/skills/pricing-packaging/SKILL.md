---
name: pricing-packaging
description: Designs pricing and packaging for a product going to market, from the value metric, plans and price points to a discount policy, the price page and price tests, with a script for Van Westendorp and Gabor-Granger surveys. Use it when someone asks how to price or package their product, how to handle discounts, or how to raise prices. Not for pricing an idea that has no customers yet (use business-model).
license: MIT
compatibility: Runs a Python 3 script on survey CSVs.
---

# Pricing and packaging

Price is the fastest lever on revenue, and the one most founders set once, by gut, and never revisit. Price on the value the customer gets, package so each segment buys what it needs, and write a policy so a discount is a decision, not a reflex.

## Inputs

The positioning and value themes, the ICP and personas, the evidence of the problem's cost from interviews and calls, the alternatives' prices (public pages, with links and dates), the cost to serve, and the `business-model` output if there is one.

## 1. Value metric

The unit the price grows with: per seat, per use (orders, documents, calls), per outcome, per location, or flat. A good metric grows with the value the customer gets, is easy to predict, and is hard to game. Compare two or three candidates on those criteria in a table.

## 2. Packaging

- **Good, better, best** for most products: an entry plan for the core job, a main plan most buyers should pick (make it the obvious choice), and a top plan for the demanding segment, often "contact us" in a sales-led motion.
- **Fences** separate the plans with usage limits or features that matter to one segment only (single sign-on, audit logs, API, support levels). Never cripple the core job.
- **Free:** a free tier or trial only when the motion is product-led and free users convert or spread the product. Otherwise, a paid pilot.
- **Services:** package consulting as fixed-scope offers with outcomes (an assessment, an implementation, a retainer), not hours. Keep a day rate for exceptions.

## 3. Price points

Start from value: what the problem costs the customer and what the outcome is worth to them. Capturing 10–20% of the value created is a common starting point; the weaker the evidence, the lower. Check the result against the alternatives' prices and the cost to serve (the gross margin target). Use clean numbers. Annual plans usually get about two months free; keep monthly available unless the motion is sales-led.

## 4. Test the price

- **In calls:** say the price and watch the reaction; ask what they'd compare it with.
- **Surveys** with at least about 30 people from the ICP per segment:
  - Van Westendorp asks four questions (too cheap, a bargain, getting expensive, too expensive) and gives a range of acceptable prices.
  - Gabor-Granger asks "would you buy at this price?" for a few prices and gives the revenue-maximising one.

  ```bash
  python3 scripts/price_research.py vw survey.csv     # columns: too_cheap, cheap, expensive, too_expensive
  python3 scripts/price_research.py gg answers.csv    # columns: price, buy (1 or 0), one row per person and price
  ```

  Surveys measure intent, which overstates willingness to pay. Treat the result as a range and trust a paid pilot or pre-sale over any survey.
- **Live:** test prices on new visitors or new deals, never on existing customers.

## 5. The policy

Write `strategy/pricing.md`:

- List prices per plan and the value metric.
- **Discounts:** the maximum without approval (for example 10% for annual prepayment), what every discount is traded for (a longer term, prepayment, a case study, a reference), and who approves exceptions.
- Payment terms, currency and VAT, and the rules for price increases (notice, grandfathering).
- **Consumers:** show the total price including taxes; a reference "was" price must be one you really charged (for goods, EU law makes it the lowest price of the previous 30 days); renewals need clear terms and an easy way to cancel; and online consumer contracts need a withdrawal function from 19 June 2026 (Directive (EU) 2023/2673). Check national rules with a lawyer.

## 6. The price page

Plans side by side with the recommended plan highlighted, the value metric in one line, what's included in plain words, an FAQ that answers the real objections (contract length, cancellation, data, support), and one call to action per plan. Write the copy with the `landing-page` skill.

## Gotchas

- Cost-plus and "a bit cheaper than the leader" both leave money on the table and signal low value.
- More than three plans plus "contact us" paralyses buyers.
- Raising prices: new customers first, existing ones with notice, a grandfathering period and the added value explained.
- Never discuss prices with competitors; that's illegal under competition law. Use public prices only.
- Only the person's numbers are data. A segment mapping ("smaller customers sit near 4 hours"), a volume band or a benchmark share of value is an assumption: label it so, next to where it's used.

## Output

`strategy/pricing.md`: the value metric decision, plans and fences, price points with their reasoning, the test plan and results, the policy and the open questions. Changing live prices is the person's decision.

In the reply, also when you can't write the file, give the recommendation itself: the value math with both ends of every range worked out and each assumption labelled; the value metric and why; the plans with prices and fences; a check of the recommended plan against that value range and the cost to serve (lower it, or name the extra value that justifies the gap); the discount policy (the standing discount, the most anyone gives without approval, what every other discount is traded for, and who approves); and how to test the price.
