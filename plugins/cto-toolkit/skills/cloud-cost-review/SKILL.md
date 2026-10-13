---
name: cloud-cost-review
description: Reviews cloud spend from billing exports with a summary script, and ranks savings by return on effort, from idle resources to commitments and unit cost. Use it when someone asks why the cloud bill went up, how to cut cloud costs, or wants a FinOps review.
license: MIT
compatibility: Runs a Python 3 script on a billing CSV export (AWS, GCP or Azure).
---

# Cloud cost review

Find the money that's being spent on nothing, then the money that's being spent inefficiently. Rank the savings by return on effort. Recommend; never change infrastructure yourself.

## Steps

1. **Get the data:** a billing export covering at least the last three months, with date, service, cost, and ideally the account or project, resource and usage type.
   - **AWS:** Cost Explorer CSV, or the CUR
   - **GCP:** the billing export
   - **Azure:** cost analysis
2. **Summarise:** `python3 scripts/cost_summary.py bill.csv --date-col <col> --service-col <col> --cost-col <col>`. This gives the monthly totals, cost per service, and the top movers.
3. **Explain the movers.** Match each big change to a cause: a launch, traffic growth, a misconfiguration, or a forgotten experiment. Mark it as a hypothesis until it's confirmed.
4. **Hunt**, in this order:
   - idle and orphaned resources: unattached volumes, old snapshots, idle load balancers, unused IPs, forgotten environments
   - oversized compute (CPU or memory below 30% for most of the period)
   - storage that should be in a cheaper tier, and log retention
   - data transfer: cross-zone traffic, NAT gateways, egress
   - commitment coverage for steady usage
   - non-production running around the clock
   - observability spend (logs, metrics cardinality)
5. **Unit economics:** cost per customer, order or request, when the business metric is available. A rising unit cost matters more than a rising bill.

## Rules

- Every saving shows its arithmetic and its assumptions. Mark estimates as estimates.
- Recommend only; the owning team makes the change. Commitments are financial decisions that go to the CTO and finance.
- Never trade reliability or security for savings without saying so explicitly.

## Output

`cloud-cost-review-YYYY-MM.md`:
- the monthly trend and the movers explained,
- a savings table (action, monthly saving with its estimate basis, effort, risk, owner),
- the unit cost trend,
- three quick wins for this week.

Have the `skeptical-cfo` agent check the estimates if it's available.
