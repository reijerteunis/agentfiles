---
name: experiment-design
description: Designs cheap validation experiments on the riskiest assumption, with success and kill thresholds written before they run, and records results before interpreting them. Use it when someone wants to validate an idea, test demand before building, or make sense of experiment results.
license: MIT
---

# Experiment design

An experiment is only an experiment if it could have failed. Write down what failure looks like before you start, and pick the cheapest test that can tell you something, not the most impressive one.

## 1. Map the assumptions

In `assumptions.md`, list what must be true for the idea to work, grouped as:
- **Desirability:** they have the problem and want this solution.
- **Viability:** they'll pay enough, often enough, at an acquisition cost that works.
- **Feasibility:** we can build and deliver it, legally and with our skills.

Rate each one by importance (if wrong, the idea dies) and by evidence (none, weak or strong, citing interviews and earlier experiments). **Test the most important assumption with the least evidence first.**

## 2. Pick the cheapest test

| Method | Tests | Cost | Signal |
|---|---|---|---|
| Problem interviews | the problem exists and hurts | days | weak to medium (`customer-interview`) |
| Smoke test: a landing page with a sign-up | interest | €50–300 and a week | medium: visits and conversion |
| Fake door: a "buy" button that leads to an honest waitlist | intent to pay | a week | medium to strong |
| Concierge: deliver the outcome by hand | value, willingness to pay | weeks | strong |
| Pre-sale, deposit or letter of intent | willingness to pay | weeks | strongest |
| Prototype test | usability, feasibility | 1–2 weeks | medium |

Be honest with people. A fake door says "not ready yet, join the waitlist" right after the click. Never take money for something you won't deliver; refund deposits if you stop. Follow the founder's discretion rules for anything public.

## 3. Write it down before it runs

`experiments/NN-<slug>.md`, using the format in the venture-lab workspace reference:
- the assumption
- the method
- the audience and how they'll be reached
- the metric
- the **success threshold**
- the **kill threshold**
- the start and end dates
- the budget

Set the thresholds from what the business needs ("the model needs a 3% visit-to-paid conversion"), not from what feels achievable. **Never edit the thresholds after the start date.**

## 4. Record, then interpret

After the end date, write the raw result first: the numbers, and what happened. Only then write the learning:
- success, kill, or inconclusive (and why),
- what it means for the assumption,
- what to test next.

Update `assumptions.md`, and the idea's `next_step` and `decide_by`.

## Sample sizes

Small samples lie. Under 100 visitors, treat conversion rates as directional only. Prefer strong signals (money, signatures) from a few people over weak signals (clicks) from many.
