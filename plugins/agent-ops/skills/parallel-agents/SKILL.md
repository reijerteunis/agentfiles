---
name: parallel-agents
description: Splits a batch of coding work across agents running in parallel without collisions. It checks which tasks are truly independent, sequences shared foundations first, and gives each agent its own worktree, brief and tests, plus a review and merge order. Use it when someone wants to run several agents at once, parallelise a backlog, or use worktrees with Claude Code, Codex or Herdr. Not for delegating to people (use delegation-brief).
license: MIT
---

# Parallel agents

Parallel agents multiply output only when the work is really independent and the human can review it all. Plan the split like a tech lead: independent tasks, clear briefs, separate worktrees, and a merge order decided up front.

## 1. Check independence

For each task, list the files and modules it will touch, the interfaces it changes, and whether it needs a migration or a shared configuration change. Two tasks are independent only if they touch no file in common and neither changes an interface the other uses.
- Shared foundations (a new interface, a migration, a shared component) go **first**, done by one agent, merged, and then the dependents start.
- Never run two agents on the same file, the same migration sequence, or the same lockfile change.

## 2. Size the batch

Run as many agents as the person can review well, usually 3–5. Unreviewed parallel output is a backlog, not progress.

## 3. Set up the worktrees

One worktree and branch per task:
- **Claude Code:** `claude -w <task>`.
- **Any tool:** `git worktree add ../<repo>-worktrees/<task> -b <task>`.

Install dependencies in each worktree. Run each agent in its own terminal pane (for example a Herdr pane), so its status is visible.

## 4. Brief each agent

Use one brief per agent:
- **Goal:** the outcome in one sentence, and why.
- **Scope:** the files and modules it may change, and the ones it must not touch.
- **Acceptance criteria:** checkable.
- **Verification:** the exact test, lint and type commands it must run green before it reports.
- **Constraints:** the conventions, no new dependencies without asking, and no pushing.
- **Report:** what changed, how it was verified, and open questions.

When a task is unclear, the agent asks instead of guessing. Brief Claude Code and Codex the same way.

## 5. Review and merge

- Review each diff as it finishes. A second agent can do a first review pass, but a human approves.
- Merge in the planned order. Rebase the later branches onto main before merging, and rerun their tests after the rebase.
- Clean up the merged worktrees (`git worktree remove`).

## Output

A plan table (task, agent and tool, worktree, depends on, files, acceptance, verify command, merge order) plus one brief per agent, ready to paste.
