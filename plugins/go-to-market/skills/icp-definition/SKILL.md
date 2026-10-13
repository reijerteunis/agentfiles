---
name: icp-definition
description: Defines the ideal customer profile and buyer personas from evidence (the best and worst customers, interviews, lost deals), with triggers, disqualifiers, tiers and a scoring script for account lists. Use it when someone asks who to sell to, wants buyer personas, or wants to prioritise prospects. Not for user personas in product planning (use product-planning).
license: MIT
compatibility: Runs a Python 3 script on a CSV of accounts.
---

# ICP definition

An ideal customer profile is a bet on where you win fastest and keep customers longest, not a description of everyone who could buy. Build it from evidence, write down who you won't sell to, and make it sharp enough that two people would score the same account the same way.

## 1. Evidence first

- **With customers:** list the best ones (fastest to close, quickest to value, highest retention or expansion, happiest) and the worst (churned, painful, heavily discounted). What do the best have in common that the worst don't?
- **Without customers yet:** use the problem interviews, the venture-lab evidence if there is any, and stalled or lost conversations. Mark the ICP as a hypothesis and name what it rests on.
- Give each statement its source. "We think" is fine when it's labelled.
- Only what the person gave or a file shows counts as evidence. Anything you add, such as an industry, a size cutoff or a typical buyer, is labelled a hypothesis.

## 2. The profile

Write `strategy/icp.md`:

- **Firmographics** (B2B): industry, size, geography, business model, growth stage. **Situation** (B2C): life stage, location, and the event that creates the need.
- **Environment:** the tools, processes or regulations that make the product fit, or not.
- **Triggers:** events that create urgency now, such as new funding, a new leader, a migration, a failed audit, a new regulation or growth past a threshold. Timing and outbound come from triggers.
- **Pains and outcomes** in the customer's own words, from interviews and calls.
- **Buying committee** (B2B): the economic buyer, the champion, the users and the blockers (IT, security, legal, procurement), and what each needs before saying yes.
- **Disqualifiers:** accounts not worth pursuing even when they ask: too small to pay, the wrong stack, a use case you can't serve, a regulatory blocker.
- **Tiers:** A (pursue actively), B (respond and nurture), C (don't pursue).

## 3. Personas

One short card per role in the buying committee: goals, the pains this product touches, the objections they raise, the proof they trust, where they spend attention (channels, communities, events), and the words they use. Base every card on interviews and calls. Leave out invented detail such as names, ages and hobbies.

## 4. The scoring rubric

Turn the profile into `strategy/icp.json`, so lists are scored consistently:

```json
{
  "tiers": {"A": 70, "B": 40},
  "criteria": [
    {"field": "employees", "op": "between", "value": [50, 500], "points": 30, "why": "big enough to pay, small enough to move fast"},
    {"field": "country", "op": "in", "value": ["NL", "BE", "DE"], "points": 20, "why": "markets we serve"},
    {"field": "platform", "op": "eq", "value": "shopify", "points": 30, "why": "the integration we have"},
    {"field": "trigger", "op": "nonempty", "points": 20, "why": "a reason to buy now"}
  ],
  "disqualify": [
    {"field": "employees", "op": "lt", "value": 10, "why": "can't pay the minimum plan"}
  ]
}
```

Score a CSV of accounts whose columns match the fields:

```bash
python3 scripts/score_accounts.py accounts.csv strategy/icp.json --out scored.csv
```

It writes each account's score, tier and reasons, and prints the counts and the top ten. Check the top and bottom ten by hand: when the rubric ranks an account where you wouldn't, fix the rubric, not the list.

## Gotchas

- Too broad is the usual failure. "SMBs in Europe" isn't an ICP. If the A-tier has more than a few hundred accounts for a founder-led motion, narrow it.
- Lists come from lawful sources with a recorded source: public company information, your own CRM, people who engaged. Don't buy or scrape personal data.
- Revisit the ICP every quarter against the won and lost deals.

## Output

`strategy/icp.md` (the profile, personas, tiers, evidence and open questions) and `strategy/icp.json`. In the reply, name the three statements the ICP rests on most and the cheapest way to test each.
