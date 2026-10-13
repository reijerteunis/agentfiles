# Agent-ops workspace

Retros and audits about the setup itself, kept private, for example `agentfiles-private/ops`. Sanitised lessons can later be published as skill gotchas or playbook notes.

```
<workspace>/
├── retros/YYYY-MM-DD-<slug>.md      one per problem fixed (agent-retro)
├── audits/YYYY-MM-DD-library.md     library audits (library-audit)
├── scans/YYYY-Www.md                weekly session-log scan summaries (counts and short excerpts only)
└── blueprints/<domain>.md           agent designs (agent-blueprint)
```

## Retro file

```markdown
---
date: 2026-10-13
problem: Agent committed a .env file
layer: permission + validator      # where the fix landed
tested_by: evals/no-env-commit, gitleaks in CI
status: fixed | monitoring | open
---

## What happened
## Why (the cause, not the symptom)
## The fix, and why at this layer
## The test that would have caught it
## Lesson (one line, could be shared publicly once sanitised)
```
