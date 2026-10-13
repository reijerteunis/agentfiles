# Automations

One scheduled run keeps ideas from drifting. Confirm the time first. The prompt has to stand on its own, because every run starts fresh. Replace `<WORKSPACE>` with the absolute workspace path.

| Task id | When (local time) | Cron |
|---|---|---|
| `venture-lab-weekly` | Sundays 19:00 | `0 19 * * 0` |

## venture-lab-weekly

> Use the venture-lab skill in Portfolio mode for the workspace at `<WORKSPACE>`. Load the founder's venture context skill first if it exists. Run `python3 scripts/lab.py <WORKSPACE> --write` from the venture-lab skill folder, and fix what it reports. For each active idea, report: the stage, the evidence gathered this week, experiments whose end date has passed and need their result recorded, and gate decisions due. Recommend the single most valuable test for next week, and which idea deserves the founder's limited hours. Don't contact anyone or publish anything. Draft interview outreach only if the founder asked for it.
