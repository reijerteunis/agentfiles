---
name: agent-instructions
description: Writes and audits the instruction files agents read every session (AGENTS.md, CLAUDE.md, global instructions), keeping only checkable, always-relevant lines and moving procedures to skills and hard rules to guardrails. Use it when someone wants an AGENTS.md or CLAUDE.md for a repo, wants their instructions reviewed or shortened, or says agents ignore their rules.
license: MIT
---

# Agent instructions

Instruction files are the most expensive text in the setup: every line costs context in every session, for every task. Keep only what's true, always relevant, and checkable. Everything else goes to a lower or more specific layer.

## Create (a project AGENTS.md)

1. **Read the repo first:** README, the build and test configs (package.json, Makefile, justfile, CI), the lint config and the structure. Don't write down what an agent can infer from these in seconds.
2. **Interview:** "What do agents get wrong here? What must never happen? What does done mean in this repo?" Those answers are the most valuable lines.
3. **Write,** starting from the template in the agentfiles repo (`templates/project-AGENTS.md`) when it's available:
   - one paragraph on what the project is and what must never break,
   - the commands,
   - the layout,
   - the conventions that can't be inferred,
   - the definition of done,
   - the don'ts.
4. Add a `CLAUDE.md` containing only `@AGENTS.md`, so every tool reads the same file.

## Audit (an existing file)

Check every line against these questions:

| Question | If not |
|---|---|
| Is it true today? | Delete it, or fix it (stale paths, renamed commands) |
| Is it needed in every session? | Move it to a skill, or to a path-scoped rule (`.claude/rules/` with `paths:`) |
| Is it a procedure of more than a few steps? | Move it to a skill |
| Must it hold every time? | Move it to a guardrail (`guardrail-design`), and keep at most a one-line pointer |
| Is it checkable ("run `pnpm test` before committing"), not vague ("write good code")? | Make it concrete, or delete it |
| Does it contradict another line or file? | Keep one; agents pick at random between contradictions |

**Budgets:** keep a project file under about 200 lines, and a global file under 6,000 characters so every tool can load it. Don't generate these files automatically: research shows generated context files lower task success.

## Output

For an audit: a findings table (line, issue, where it moves) and the rewritten file, with a before and after line count. For a new file: the file, plus the three questions you'd ask the team next month to grow it from real mistakes.
