# Automations

Confirm the times and the company with the CTO before creating these. Each prompt has to stand on its own, because every run starts fresh. Replace `<COMPANY>` with the company's name and `<CONTEXT>` with its context skill.

| Task id | When (local time) | Cron |
|---|---|---|
| `cto-weekly-review` | Mondays 07:00 | `0 7 * * 1` |
| `cto-friday-wrap` | Fridays 16:00 | `0 16 * * 5` |
| `cto-board-prep` | First day of each quarter, 09:00 | `0 9 1 1,4,7,10 *` |

## cto-weekly-review

> Use the cto-office skill in Weekly review mode for `<COMPANY>`; load the `<CONTEXT>` skill first. Gather signals only from sources that are actually connected (tracker, GitHub, monitoring, calendar, the workspace registers) and name the source of every number. Never estimate a metric. Write the review to the shared workspace's `reviews/weekly/` folder, team-safe, with no people notes. Update the registers. Don't change anything in the tracker, the repos or production, and don't contact anyone. Finish with the three things that need the CTO this week.

## cto-friday-wrap

> Use the cto-office skill for `<COMPANY>`; load the `<CONTEXT>` skill first. Read this week's review and the registers. List the follow-ups due next week, the decisions still waiting, the risks due for review, and the meetings on next week's calendar that need prep. Change nothing and contact no one. Keep the summary under 15 lines.

## cto-board-prep

> Use the cto-office skill in Board mode for `<COMPANY>`; load the `<CONTEXT>` skill first. Draft the quarterly technology update for the board with the board-tech-update skill, built from the last quarter's weekly reviews, metrics, decisions and risk register. Save it as a draft in the private location's `board/` folder. Don't share it with anyone. List the numbers you couldn't source, so the CTO can fill them in.
