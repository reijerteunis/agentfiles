---
name: engineering-metrics
description: Measures software delivery from real data, computing DORA and flow metrics by script from GitHub exports and reading them as trends with their caveats. Use it when someone asks how fast or how reliably their team ships, asks about lead time, cycle time, deploy frequency or PR numbers (also pasted ones), wants DORA or delivery metrics, or needs numbers for a weekly or board review. It keeps the numbers team-level, even when asked to rank people.
license: MIT
compatibility: Runs a Python 3 script on data exported with the gh CLI (or the equivalent from another source).
---

# Engineering metrics

Metrics are for asking better questions about the system of work, never for ranking people. Use trends over absolute values, team-level numbers over individual ones, and one or two actions over a dashboard nobody reads.

## Collect, never estimate

1. **Pull requests:**
   `gh pr list --repo ORG/REPO --state merged --limit 1000 --json number,title,createdAt,mergedAt,labels,additions,deletions > prs.json`
2. **Deploys:** the deploy workflow's runs:
   `gh run list --repo ORG/REPO --workflow <deploy-workflow> --limit 1000 --json conclusion,createdAt,updatedAt,headBranch,event > runs.json`
   The company context names the workflow. Without one, deploy frequency stays "unknown".
3. **Incidents:** start and resolution times from the postmortems, for time to restore.
4. **Compute** with `python3 scripts/delivery_metrics.py --prs prs.json --runs runs.json --weeks 12`. Save the JSON snapshot to `metrics/YYYY-Www.json` in the workspace.

If a source isn't reachable, report the metric as unavailable and say what's needed. **Never fill a gap with an estimate.**

## What the numbers mean

| Metric | From | Caveat |
|---|---|---|
| Deployment frequency | successful deploy runs per week (`deploys_ok`; `deploys` counts every finished run) | counts pipeline runs, not customer-visible releases |
| Lead time for changes | PR opened → merged (median, p90) | starts at the PR, not at the first commit or the idea |
| Change failure rate | share of merged PRs that are reverts or hotfixes | a proxy; incidents without a revert don't show up |
| Time to restore | incident start → resolved, from postmortems | only as complete as the incident records |
| PR size | median lines changed | big PRs usually mean slow reviews and more defects |

## Read it

- Compare with the last 4–12 weeks, not with industry benchmarks.
- Look for movement and its cause: a reorganisation, a release freeze, a new pipeline, holidays.
- Segment by repo or team before concluding anything. Never show per-person numbers.
- Watch for Goodhart's law: once a metric becomes a target, it stops measuring.

## Output

A short section for the weekly or board review:
1. the table,
2. three observations, each with its likely cause, marked as a hypothesis,
3. one or two actions, for example "PRs over 400 lines doubled; propose a size guideline and pair reviews",
4. the data gaps.
