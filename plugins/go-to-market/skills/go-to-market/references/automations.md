# Automations

Confirm the times first. Each prompt has to stand on its own, because every run starts fresh. Replace `<WORKSPACE>` with the absolute path of the product's workspace.

| Task id | When (local time) | Cron | Purpose |
|---|---|---|---|
| `gtm-weekly` | Mondays 08:00 | `0 8 * * 1` | Pipeline, metrics and the week's three actions |
| `gtm-followups` | Weekdays 08:30, optional | `30 8 * * 1-5` | Follow-up drafts for deals due today |
| `gtm-launch-<slug>` | Daily during a launch, optional | `0 9 * * *` | The launch checklist; delete it at T+14 days |

## gtm-weekly

> Use the go-to-market skill in Weekly review mode for the workspace at `<WORKSPACE>`. Load the person's go-to-market context skill first if it exists. Run `python3 scripts/deals.py <WORKSPACE> --write` from the go-to-market skill folder and fix what it reports. If CSV exports exist in `<WORKSPACE>/exports/`, run the gtm-metrics skill on them. Write `reviews/YYYY-Www.md` with the pipeline by stage and what moved, the deals at risk, each channel against its target in `strategy/channels.md`, and the three actions for this week with owners. Check `suppression.md`, then draft the follow-ups that are due, as Gmail drafts if the connector is available and otherwise in `drafts/`. Never send, post or change a CRM. Report what you drafted and what needs the person's decision.

## gtm-followups

> Use the go-to-market skill for the workspace at `<WORKSPACE>`. Load the person's go-to-market context skill first if it exists. Run `python3 scripts/deals.py <WORKSPACE> --write` from the go-to-market skill folder. For every open deal whose `next_step_due` is today or earlier, read the deal file and draft the follow-up its next step needs, after checking `suppression.md`: a Gmail draft if the connector is available, otherwise a file in `drafts/`. Never send. List each draft with the deal and the reason.

## gtm-launch-<slug>

> Use the go-to-market skill for the launch plan at `<WORKSPACE>/launches/<file>`. Load the person's go-to-market context skill first if it exists. List the checklist items due today or overdue, with their owners, and anything that blocks launch day. From launch day on, summarise the results so far against the launch goal from the data available. Don't publish, post or send anything.
