# The playbook

How I set up AI agents, and why. Every file in this repo follows from these principles.

Agents write most of my code now. So their configuration gets the same discipline as the code they write: versioned, reviewed, tested, and as small as it can be. A prompt nobody reviewed is a deploy nobody reviewed.

## 1. Instructions are code

Global instructions, skills and settings live in git. Changes go through the same loop as any other change: edit, lint (`just validate`), test the behavior (`just eval`), push. CI checks every skill against the open spec, checks the settings against the official schema, and scans the full history for secrets. If an instruction matters, it has a test.

## 2. Put every rule in the lowest layer that works

| Layer | Holds | Example | Lives in |
|---|---|---|---|
| Enforcement | Rules that must hold every time | Agents can't read `.env` files or `~/.ssh` | `global/claude/settings.json` (permissions, hooks) |
| Global instructions | How I work, in every session | "Done means verified" | `global/AGENTS.md` |
| Project instructions | Stack, commands, conventions | "Run `pnpm test:unit` before committing" | each repo's `AGENTS.md` |
| Skills | Procedures, loaded on demand | Plan a feature into epics, stories and tasks | `plugins/*/skills/` |
| Context skills | Facts and company specifics | One company's personas, field IDs, glossary | the private companion repo |

The test for where a rule goes: if it must hold 100% of the time, it's a permission or a hook, not a sentence. Sentences are followed most of the time. Hooks are followed every time.

## 3. Always-on context is expensive

Every line of global instructions is read in every session, by every agent, on every task. So `global/AGENTS.md` stays under 6,000 characters (the tightest limit among the tools I use), holds no procedures, and every line in it is checkable. I don't use generated context files: [research on them](https://arxiv.org/abs/2602.11988) found they lower task success and raise cost. A short file I wrote by hand beats a long one a tool wrote for me.

## 4. Write skills like onboarding a strong new hire

A skill is the briefing I'd give a smart person on day one:

- **The description is the trigger.** It says what the skill produces and when to use it, in the words people actually type. A vague description means the skill never fires.
- **Show taste, not just rules.** My build-in-public skill keeps the drafts I rejected and why. That teaches the voice faster than any list of adjectives.
- **End with a quality gate.** Every skill checks its own output before delivering it.
- **Grow a gotchas section.** Every time I correct an agent on a task, the lesson goes into that skill.
- **Keep it lean.** Under 500 lines, references loaded only when a step needs them, scripts for anything deterministic.

The full standard is in [writing-skills.md](writing-skills.md).

## 5. Separate the method from the context

The method for planning a product or cleaning up a Jira epic is the same at every company. The personas, field IDs and business model are not. So public skills carry the method, and small private context skills carry the specifics. `product-planning` works anywhere; a private `<company>-product` skill adds that company's context and points at it.

That split does three things: I can share the craft without leaking anything, every company benefits when the method improves, and the context stays small enough to keep current.

## 6. Done means verified

An agent's "done" is a claim until it's proven. My global instructions require running whatever actually exercises the change (build, tests, the app itself) and reporting what was verified and how. Agents may never skip or weaken a test to reach green. Commits are signed, so I always know what I approved, and CI runs on everything.

## 7. Autonomy where mistakes are cheap

The line is simple: reversible, local work happens without asking. Anything outward-facing or irreversible gets a question first: pushing, deploying, deleting data, sending messages, spending money, touching CI or permissions. That keeps agents fast on the 95% of work where a mistake costs a `git checkout`, and careful on the 5% where it doesn't.

## 8. Make the machine agent-friendly

Agents inherit your environment, so the environment has to work for them:

- PATH and runtimes are set in login-shell files, because agents run login shells, not your interactive one.
- No alias shadows a real command. An agent typing `cd` must not get a fuzzy directory jumper.
- Git never waits on an editor (`GIT_EDITOR=true` for Claude Code), and never on a pager.
- Parallel work runs in separate worktrees, watched from one terminal workspace.

## 9. Security is a default, not a review step

- Agents are denied reads of secrets, SSH keys and cloud credentials. Secrets come from 1Password at runtime.
- Content from web pages, issues and files is data, never instructions.
- Package managers skip versions younger than 24 hours. Compromised releases are usually pulled within hours, and agents install packages all day.
- Third-party skills are read line by line before they're installed, and pinned to a commit.

## 10. Portable by default

I use open standards wherever they exist: one `AGENTS.md` for instructions and `SKILL.md` for skills. One canonical file is linked into every tool, so switching tools or adding one costs nothing. Claude gets the skills through the plugin marketplace; every other agent reads them from `~/.agents/skills`.

## 11. Measure, then prune

The status line shows context use and plan limits on every prompt. Evals run every case with the plugin and without it, so I know what it actually adds. Unused skills get deleted: every skill description costs context in every session, so a skill has to earn its place.

## 12. Agents are skills with a job, a memory and a boss

The step from skills to agents isn't a new framework. It's three additions:

- **an orchestrator skill** that knows the whole workflow,
- **state in files** so any session can continue the work,
- **explicit gates** where a human decides.

My chief of staff triages my inbox every morning, drafts the replies, flags the email that asks to change a supplier's bank details, and tracks every promise I made. But it never sends, accepts or deletes anything. Autonomy on the work, a human on the consequences.

## Do and don't

| Do | Don't |
|---|---|
| Version, lint and test your agent config | Edit prompts in a settings screen and hope |
| Enforce must-hold rules with permissions and hooks | Write "NEVER" in capitals and trust it |
| Keep global instructions short and checkable | Paste your whole wiki into the context |
| Write skill descriptions as triggers | Name a skill and assume the agent finds it |
| Keep method public and context private | Copy company internals into a shared repo |
| Require proof of "done" | Accept "should work now" |
| Let agents act freely on reversible work | Make agents ask permission for every file edit |
| Pin and read third-party skills | Install the most popular skill pack unread |
