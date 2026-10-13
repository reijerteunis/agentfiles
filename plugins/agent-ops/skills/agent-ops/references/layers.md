# The layers

Put every rule, fact and procedure in the lowest layer that works. Lower layers are more reliable and cost less context.

| Layer | Holds | Reliability | Context cost | Where (Claude Code) |
|---|---|---|---|---|
| **Permission** | Things an agent must never do (read secrets, send email, run destructive commands) | Always enforced | None | `permissions.deny` in settings |
| **Hook** | Checks that must run every time (format on edit, block a command pattern, verify before stop) | Always runs | None | `hooks` in settings or a plugin's `hooks/hooks.json` |
| **Sandbox** | Filesystem and network limits for commands | Enforced by the OS | None | `sandbox` settings |
| **Validator or test** | Properties of files that must hold (frontmatter, formats, no secrets) | Enforced in CI | None | scripts and CI |
| **Global instructions** | How to work with this person, in every session | Usually followed | Every session | `~/.claude/CLAUDE.md`, `AGENTS.md` |
| **Project instructions** | Stack, commands, conventions for one repo | Usually followed | Every session in that repo | the repo's `AGENTS.md` |
| **Skill** | A procedure, loaded when relevant | Followed when triggered | Only when used, plus its description | `skills/<name>/SKILL.md` |
| **Context skill** | Facts and specifics (people, IDs, preferences) | Loaded by name | Only when used | private repo |
| **Memory** | Things learned in passing | Unreliable | Small | auto memory |

## How to choose

- Could it cause harm or leak data if ignored even once? → **permission or hook**.
- Is it a property of files? → **validator**.
- Does it apply to every task in every repo? → **global instructions**, if it fits the budget.
- Does it apply only in one repo? → **project instructions**.
- Is it a multi-step procedure? → **skill**.
- Is it a fact about a person, company or system? → **context skill**.
- Did an agent get it wrong once? → first add a **gotcha** to the skill that was running, then an **eval case** that reproduces it.
