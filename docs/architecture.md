# Architecture

How the repo turns into a working setup, and why each piece lives where it does.

## Three repos: method, context, state

| Repo | Visibility | Holds |
|---|---|---|
| `agentfiles` | public | **Method:** global instructions, Claude settings, the installer, and the skills anyone can use |
| `agentfiles-private` | private | **Context:** context skills (company and personal facts and rules), private plugins, and third-party skills I use but didn't write |
| `life` | private | **State:** the workspace agents read and write: profile, pipelines, drafts and logs, all as markdown |

Both have the same layout: a `.claude-plugin/marketplace.json` at the root and plugins under `plugins/`. The private repo can also add `global/AGENTS.md` (imported into Claude's instructions) and `global/claude/settings.json` (merged on top of the public settings). The installer finds it at `../agentfiles-private`, or wherever `AGENTFILES_PRIVATE` points.

## Agents

An agent here is not a separate program. It's a set of skills with a job, a memory and a boss:

| Part | What it is | Example: chief of staff |
|---|---|---|
| **Orchestrator** | A skill that runs the end-to-end workflow, picks a mode from the request, and calls the specialists by name | `chief-of-staff` |
| **Specialists** | Skills that each do one step well, and also work on their own | `daily-brief`, `inbox-triage`, `email-reply`, `meeting-prep`, … |
| **Reviewers** | Subagents that critique the work from a specific point of view, in Claude Code and Cowork | the `draft-reviewer` agent |
| **Context** | A private skill with the person's rules and pointers | `cos-context` |
| **State** | Markdown files in the `life` workspace, with status in frontmatter and append-only logs | `life/cos/follow-ups.md`, `life/cos/briefs/…` |
| **Gates** | Points where the agent stops for a human decision. It drafts; people send and submit | "the person sends every reply" |
| **Automations** | Scheduled runs of the orchestrator in a given mode | a morning brief, follow-up drafts, a Friday review |

Because the state lives in files rather than in a conversation, any session can pick up where the last one stopped: a scheduled run at 07:30, Cowork in the afternoon, Claude Code in the evening. Because people send and submit everything, an agent can work unattended without being able to do harm.

Automations are defined in the orchestrator's `references/automations.md`, so they're versioned with the method. The agent's Automate mode creates them with the environment's scheduling tool, after the person confirms the times.

## Where everything lands

| What | How it gets there | Lands in |
|---|---|---|
| Skills for Claude (chat, Cowork, Claude Code) | Plugin marketplaces, added once in claude.ai | Synced by Claude to every surface and machine you sign in to |
| Skills for every other agent | `install.sh` links each skill folder | `~/.agents/skills/<name>` (Codex, Cursor, Zed, Copilot, Gemini, OpenCode, Amp, Goose) |
| Global instructions for Claude | `install.sh` writes the contents of `global/AGENTS.md` into it | `~/.claude/CLAUDE.md` |
| Global instructions for other agents | `install.sh` links `global/AGENTS.md` for each installed tool, or writes the same copy as Claude's when the private companion adds lines | `~/.codex/AGENTS.md`, `~/.config/zed/AGENTS.md`, … |
| Claude settings | `install.sh` merges `global/claude/settings.json` | `~/.claude/settings.json` |
| Status line | `install.sh` links it | `~/.claude/statusline.sh` |
| Codex config | `install.sh` copies it once; Codex owns it after that | `~/.codex/config.toml` |

### Why some files are linked and others aren't

- **Linked** when a tool only reads the file: edits in the repo apply immediately.
- **Generated** for `~/.claude/CLAUDE.md`: Cowork skips a symlinked one, and also skips `@imports` that point outside the session's folder. So the installer writes the instructions in full. After editing `global/AGENTS.md`, run `./install.sh` again; `./install.sh --check` reports when the two have drifted.
- **Merged** for `~/.claude/settings.json`: Claude Code writes to it itself (plugin installs, `/model`, other tools' hooks). Merging keeps those local changes out of the repo while the repo's keys always win. Lists such as deny rules are unioned, so removing a rule from the repo doesn't remove it locally; delete it in both places.
- **Copied once** for the Codex config: Codex writes trusted folders and preferences into it, so the repo only seeds it.

## Why Claude gets skills through the marketplace

A marketplace added in claude.ai syncs its plugins to chat, Cowork and Claude Code, on every machine you sign in to, and updates them when you push. Linking the same skills into `~/.claude/skills` as well would load every skill twice. So `install.sh` never touches Claude's skills folder; it only makes sure `~/.claude/skills`, `agents`, `commands` and `hooks` are real folders, because Claude and other tools write into them.

## Keep the enabled catalog small

Skill selection gets less accurate as the number of enabled skills grows. The biggest cause is look-alikes: two skills that both seem to fit a request. Research puts the drop at around 30 skills, and Anthropic advises reviewing anything above 20–50. Three habits keep it accurate:

- **Plugins are packs.** Enable a domain when you need it. For example, `career` is on during a job search and off otherwise.
- **Routing lines.** Every skill with a look-alike says what it's *not* for and which skill to use instead, for example "Not for writing a job posting for your own team (use job-description-writer)".
- **Self-explanatory names.** When the catalog is over budget, Claude Code drops descriptions before names.

## Drafts only is enforced, not requested

Scheduled runs can approve their own actions, and connector approval settings have had bugs. So "the agent never sends" isn't left to skill text:

- `global/claude/settings.json` denies the Gmail connector's send, reply and forward tools in Claude Code. A deny always wins and can't be overridden by a prompt. The private overlay adds the same rules under the tool names the desktop app uses for its connectors.
- The calendar's respond and delete tools are denied the same way. Accepting an invite notifies the organiser, and deleting an event cancels it for everyone.
- In claude.ai, set the same Gmail and calendar tools to **Blocked** under the connectors' permissions.
- Scheduled tasks only ever create drafts and files. People send, submit and publish.

## Versions and updates

Plugins have no `version` field, so each install tracks the latest commit. Marketplaces added in claude.ai auto-update; the running session keeps its version until `/reload-plugins` or a restart.

## The development loop

```bash
just new cto-toolkit adr-writer   # scaffold
just validate                     # spec, plugins, evals, catalog, shell, secrets
just try cto-toolkit              # a Claude session with the local plugin loaded
just eval cto-toolkit             # behavior against a no-plugin baseline (costs usage)
git push                          # CI, then every machine picks it up
```
