---
name: business-model
description: Builds the business model for a validated idea, with value-based pricing, unit economics by script, the cost structure, the path to the first milestone, and a bootstrap or venture shape. Use it when someone asks how an idea makes money, how to price it, or about its unit economics, such as LTV, CAC payback or margins. Not for the plans and price page of a product going to market (use pricing-packaging) or build-versus-buy inside a company (use build-vs-buy).
license: MIT
compatibility: Runs a Python 3 script for the unit economics.
---

# Business model

A business model is a set of linked guesses about who pays, how much, how often, and what it costs to win and serve them. Make every guess explicit, test the riskiest ones, and let a script do the arithmetic.

## Steps

1. **Who pays, for what:** the buyer (often not the user), the value they get in money or time, and the budget it comes from.
2. **Revenue model:** subscription, usage-based, per transaction, services, licence, or a hybrid. Explain why it fits how the customer already buys.
3. **Price on value:** start from the customer's cost of the problem (from the interviews) and the price of the alternatives (from the market map). Price is a hypothesis, so propose a test: say the price out loud in interviews, show it on the fake door, or pre-sell at it.
4. **Unit economics:** run

   ```bash
   python3 scripts/unit_economics.py --price <per customer per month> --margin <0-1> --churn <monthly, 0-1> --cac <cost to acquire>
   ```

   Use evidence where you have it and label every assumption. Run three scenarios (pessimistic, base, optimistic) and show them side by side.
5. **Cost structure:** the main fixed costs (people, tools, infrastructure) and variable costs per customer. The point where gross margin covers the fixed costs is break-even: how many customers is that?
6. **Path to the first milestone,** for example €10k in monthly recurring revenue, or the founder's salary: the number of customers needed, the sales per month needed, and the channel that could plausibly deliver them.
7. **Shape:** **bootstrapped** (profitable early, founder-controlled, slower) or **venture** (needs a market big enough for a large outcome, gives up ownership for speed). Say which this idea fits, and whether that matches what the founder wants from `profile/founder.md`.

## Output

`model.md`: who pays and why, the revenue model, the price hypothesis and its test, the unit economics table (from the script) in three scenarios, the cost structure and break-even, the path to the milestone, the recommended shape, and every assumption listed. Update `assumptions.md` with the viability assumptions that most need testing.
