# Automations

One weekly run keeps the setup improving. Confirm the time first. The prompt has to stand on its own, because every run starts fresh. Replace `<REPO>` with the skills repository path and `<WORKSPACE>` with the agent-ops workspace.

| Task id | When (local time) | Cron |
|---|---|---|
| `agent-ops-weekly` | Sundays 20:00 | `0 20 * * 0` |

## agent-ops-weekly

> Use the agent-ops skill for the skills repository at `<REPO>` and the workspace at `<WORKSPACE>`. Load the agent-ops context skill first if it exists.
> 1. Run the agent-retro skill's session-log scan for the last 7 days, and save only the counts and the short excerpts to `scans/`.
> 2. Run the library-audit skill's stats script on `<REPO>`.
> 3. Report:
>    - the top three recurring problems, each with the layer where a fix belongs,
>    - look-alike skills and skills without evals,
>    - the catalog size against the budget,
>    - one proposed fix for the week.
>
> Don't change any skill, setting or instruction, don't commit, and don't copy session content anywhere public.
