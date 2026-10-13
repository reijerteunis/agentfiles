# Automations

Three scheduled runs keep a job search moving without the person having to remember it. Confirm the times and the workspace path before you create them. Each prompt must stand on its own, because every run starts fresh. Replace `<WORKSPACE>` with the absolute workspace path.

| Task id | When (local time) | Cron |
|---|---|---|
| `job-scout-daily` | Weekdays 07:30 | `30 7 * * 1-5` |
| `job-follow-ups` | Weekdays 08:00 | `0 8 * * 1-5` |
| `job-pipeline-weekly` | Sundays 18:00 | `0 18 * * 0` |

## job-scout-daily

> Use the job-search skill in Scout mode for the job-search workspace at `<WORKSPACE>`. Load the career context skill first if it exists. Find new openings since the last scout through the job-scout skill: job-alert emails in Gmail and the watchlist job boards. Never browse or search LinkedIn itself. Screen them against `profile/preferences.md` and file the survivors in `leads/`. Don't apply to anything and don't send anything. Finish with a short digest: the number of new leads, then a table of the best ones (score, role, company, why, link). If nothing new turned up, say so in one line.

## job-follow-ups

> Use the job-search skill in Follow up mode for the job-search workspace at `<WORKSPACE>`. Load the career context skill first if it exists. For every application whose `next_action_due` is today or earlier, draft the right message with the outreach-message skill (follow-up, thank-you or withdrawal). Save it as a Gmail draft if Gmail is connected, otherwise in the application folder. Never send anything. Update each application's log and next action, and commit the workspace if it is a git repo. Finish with a list of the drafts that are waiting for review.

## job-pipeline-weekly

> Use the job-search skill in Review mode for the job-search workspace at `<WORKSPACE>`. Load the career context skill first if it exists. Regenerate `pipeline.md`, then report counts and conversion per stage, overdue next actions and stale applications. Give at most two concrete suggestions to improve the search. Commit the workspace if it is a git repo. Don't contact anyone.
