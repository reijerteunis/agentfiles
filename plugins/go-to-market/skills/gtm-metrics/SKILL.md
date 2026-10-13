---
name: gtm-metrics
description: Measures go-to-market performance from exports, computing funnel conversion, win rate, sales cycle, CAC payback and revenue retention by script, with sample sizes and caveats. Use it when someone asks whether their marketing or sales is working, or wants funnel metrics, CAC, payback or NRR. Not for engineering delivery metrics (use engineering-metrics) or projecting an idea's unit economics (use business-model).
license: MIT
compatibility: Runs a Python 3 script on CSV exports from analytics, CRM, billing and accounting tools.
---

# GTM metrics

Metrics decide where the next hour and the next euro go. Compute them by script from real exports so they can't be wishful, look at trends and cohorts rather than single numbers, and always say how small the sample is.

## Exports

Ask for CSV exports, or read them through connectors when available, into `exports/`:

| File | Columns | From |
|---|---|---|
| `funnel.csv` | step, count, optionally channel | Analytics and the email tool, for one period |
| `deals.csv` | id, created, closed, stage, amount, source | The CRM, or the workspace's deal files |
| `spend.csv` | month (YYYY-MM), channel, amount | Accounting, ad accounts and tools; add people's time at a cost if it's significant |
| `mrr.csv` | month (YYYY-MM), customer, mrr | The billing system |

Use the same names for spend channels and deal sources, so the script can match them.

## Run

```bash
python3 scripts/gtm_metrics.py funnel exports/funnel.csv
python3 scripts/gtm_metrics.py deals exports/deals.csv --from 2026-07 --to 2026-09
python3 scripts/gtm_metrics.py cac exports/spend.csv exports/deals.csv --margin 0.8 --from 2026-07 --to 2026-09
python3 scripts/gtm_metrics.py retention exports/mrr.csv --from 2025-10 --to 2026-09
```

`cac` treats a deal's amount as its first-year value; pass `--amount monthly` when it's monthly revenue. Every command flags small samples.

## Read them

- **Funnel:** the step with the steepest drop is where to work, unless the sample explains it. A drop after sign-up isn't automatically an onboarding problem: poorly matched traffic activates poorly too. Split by channel before naming a cause.
- **Deals:** the win rate by source shows which channels bring buyers, not just leads. A long sales cycle on a short runway is a risk to name.
- **CAC and payback** per channel, against the targets in `strategy/channels.md`.
- **Retention:** net revenue retention above 100% means existing customers grow on their own; gross retention shows the leak. With few customers, list who churned and why instead of trusting a percentage.

## Rules

- Never fill a gap with an estimate presented as data. When an export is missing, say which numbers can't be computed.
- State the period, the sample size, and anything that distorts it, such as one large deal or a launch spike.
- Say what the numbers suggest, not what they prove. Name a cause only when the data rules out the alternatives; otherwise give the candidates and the split that would tell them apart. A projection such as "fixing this doubles revenue" says what has to be true.
- Compare with the previous period and the targets, not with benchmarks from the internet.

## Output

A metrics section for the weekly or quarterly review in `reviews/`: the commands and exports used, the numbers, and the two or three things they suggest doing.
