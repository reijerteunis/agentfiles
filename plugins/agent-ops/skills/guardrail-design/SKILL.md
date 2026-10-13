---
name: guardrail-design
description: Turns rules that must always hold into enforcement instead of instructions, using permission rules, PreToolUse hooks, sandbox limits, connector blocks or CI checks, and tests that each one blocks the bad case and allows the good one. Use it when someone says an agent must never do something, wants to block a command, tool or file, or a retro shows an instruction wasn't enough.
license: MIT
---

# Guardrail design

Instructions are followed most of the time; guardrails are followed every time. Use them for anything that would cause harm, leak data, or break trust if it happened even once.

## Choose the mechanism

| Need | Mechanism | Example |
|---|---|---|
| Never call a tool or read a path | **Permission deny rule** | `"deny": ["Read(**/.env)", "mcp__<server>__send_message"]` |
| Ask every time | **Permission ask rule** | `"ask": ["Bash(git push:*)"]` |
| Block based on the arguments | **PreToolUse hook** | block `git commit --no-verify` and `--no-gpg-sign` |
| Run something after every edit | **PostToolUse hook** | a formatter or linter on changed files |
| Limit the filesystem or network for commands | **Sandbox** | `/sandbox`, with allowed domains |
| Block a connector tool everywhere, including chat | **Connector permission** in claude.ai | set send and delete tools to **Blocked** |
| Properties of files in a repo | **Validator or CI check** | gitleaks, frontmatter checks |

Deny always wins over allow, and a prompt can't override it. When a rule must hold for scheduled and unattended runs too, use deny, never ask. Unattended runs may auto-approve.

## Write it

- **Permission rules** go in the right settings file: user settings for everything, project `.claude/settings.json` for one repo, or a private overlay for machine-specific tool names. Rules are exact strings; add both naming forms when a connector has more than one (CLI and desktop).
- **Hooks** are a script that reads the event JSON on stdin and checks `tool_input`. A PreToolUse hook that exits with code **2** blocks the call, and its stderr is shown to the agent as the reason. Keep hooks fast, dependency-free, and readable in one screen. See `references/hook-example.md` and the tested script in `assets/block-unsafe-git.sh`.

## Test both ways

1. **Blocks:** feed the hook a sample JSON for the forbidden case and check that it exits 2. For permission rules, try the action in a session and check that it's denied.
2. **Allows:** feed the legitimate case and check that it exits 0. A guardrail that blocks normal work gets removed by frustrated people.
3. Keep the test as a script, or as an eval case with `eval-writer`.

## Document

Write one line in the settings file's repository (CHANGELOG or a comment in the hook) saying what it blocks, why, and the safe way to override it, for example "remove the line from the private overlay".
