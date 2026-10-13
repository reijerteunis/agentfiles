# Writing skills

The standard every skill in this repo meets. `just validate` enforces the parts a machine can check.

## Anatomy

```
plugins/<plugin>/
├── .claude-plugin/plugin.json
├── skills/<skill-name>/
│   ├── SKILL.md            required: frontmatter + instructions
│   ├── references/         optional: docs loaded only when a step needs them
│   ├── scripts/            optional: deterministic steps, run rather than read
│   └── assets/             optional: templates and files the output is built from
└── evals/<case>/           behavior tests for the plugin's skills
```

Each skill folder is self-contained. Tools that install a single skill copy only its folder, so a skill never points at files outside it. Refer to other skills by name ("load the `ruud-context` skill"), never by path.

## Frontmatter

Only the six keys from the open spec, so the skill loads everywhere: claude.ai, the API, Claude Code, Codex and the rest.

| Key | Rule |
|---|---|
| `name` | Required. Equals the folder name. 1–64 chars of `a-z`, `0-9`, single hyphens. No `claude` or `anthropic`. |
| `description` | Required. At most 1,024 chars, no XML tags. What it does and when to use it. |
| `license` | `MIT` for this repo. |
| `compatibility` | Only if it needs something unusual. At most 500 chars. |
| `metadata` | Strings only. Quote numbers: `version: "1.0"`. |
| `allowed-tools` | Avoid unless a skill really needs pre-approved tools. |

Quote any value that contains `: `. An unquoted colon breaks the YAML, and most tools then load the skill without its description, so it silently never triggers.

## The description is the trigger

It's the only part an agent sees before it decides to load the skill. Write it as:

> **What it does**, in third person, with concrete outputs. **Use it when** the situations, with the phrases people actually type, even if they don't name the skill.

- Good: "Cleans up a Jira epic and all its child issues in one pass … Use it whenever someone asks to clean up, tidy, normalise or fix the tickets under an epic, for example 'clean up PROJ-123'."
- Bad: "Helps with Jira."

Don't fit the description to your test prompts. Write it for the real requests you expect.

When another skill could plausibly answer the same request, end the description with a **routing line**: "Not for writing a job posting for your own team (use job-description-writer)." Look-alike skills are the main reason agents pick the wrong one as a library grows. Avoid colons in routing lines; they break the YAML.

## The body

1. **The outcome and its bar**, in one paragraph. Skip what the model already knows.
2. **What to read or ask first.** Say exactly when to load each reference ("Read `references/voice.md` before writing a sentence").
3. **The workflow.** Give exact commands for fragile steps and judgment for open-ended ones. One step always verifies the result.
4. **The output.** A template beats a description. Long templates go in `references/`.
5. **Gotchas.** Every correction you give an agent on this task becomes a line here.

Keep SKILL.md under 500 lines. Give any reference over 100 lines a table of contents at the top.

## Method and context

Public skills carry the method. Anything specific to a company, a client or me personally goes into a context skill in the private companion repo: identifiers, internal URLs, personas, career facts, discretion rules. The public skill loads the context skill by name when it exists, and works without it (it asks, or uses clearly marked placeholders).

## Building an agent

When a domain needs more than one skill, add an orchestrator. It follows the same standard as any other skill, plus these rules:

- **Rules that never bend** go at the top: truth, drafts only, discretion, gates.
- **A mode table** maps what people say to what the agent does, so one skill handles "what's new?", "apply to this" and "where do I stand?".
- **Specialists are called by name** ("run the `job-fit` skill"), never by path. Every specialist still works on its own.
- **State lives in files** in the person's workspace, as described in a `references/workspace.md`: the layout, templates, status values and naming. If it isn't in the workspace, it didn't happen.
- **Gates are explicit:** name every point where the agent stops for a human decision.
- **Every reply ends with the next action** and who owns it.
- **Automations** are prompts in `references/automations.md` that stand on their own, because each scheduled run starts fresh.
- **Evals** add one end-to-end case for the agent. Truthfulness and gate cases matter more than happy paths.

## Evals

Every plugin has an `evals/` suite for `claude plugin eval`. The minimum per skill:

- **One trigger case.** A realistic request that doesn't name the skill, with a `tool_used` grader that the skill fired and one grader on the output (a `regex` for long output, an `llm` rubric with concrete PASS and FAIL lines for short output).
- **One near-miss.** A related request that must *not* trigger it: `tool_used` with `min: 0`, `max: 0` and `arm: both`.

```bash
just eval cto-toolkit                 # 3 runs per case, with and without the plugin
just eval cto-toolkit --runs 1 --ablation none   # cheap pass while writing graders
```

Evals are real model calls, so run them when you change a skill, not on every commit.

What the first full run taught, the hard way:

- **The sandbox is empty.** An eval run has no repository, no workspace, no connectors and none of your instructions. A prompt like "add this to my repo" tests the sandbox, not the skill. Put everything the case needs in the prompt.
- **A case that passes without the plugin measures the model, not the skill.** Keep it as a regression guard, but to show what a skill adds, test what only the skill produces: its structure, its script's numbers, its gates.
- **Strict skills over-ask.** A skill that forbids guessing tends to answer with a questionnaire, and a plain model that just drafts beats it. Tell the skill to draft with marked placeholders and assumptions, then ask the three to five questions that would change the result.
- **Grade what the case makes possible.** A grader that wants concrete findings when the prompt gives no data fails good answers. Read the failing answer before you blame the skill.
- **One requirement per grader when it matters.** The Haiku judge waves through a requirement tacked onto the end of a PASS line: three plain answers "included a way to test the fix" without one. Give the requirement its own grader, and say what doesn't count ("a hook by itself is not a test of it").
- **Test where models slip, not where they shine.** A plain model keeps an obvious lie out of a CV, but widens a claim's scope in the summary; it writes a fine job ad, with seven must-haves and years of experience. Cases built on those traps show what a skill adds; cases it passes anyway stay as regression guards.
- **Every trigger case needs a grader on the result.** Graded only on whether the skill fired, a case always "beats" the plain model, which can't load a plugin's skill. `eval_report.py` leaves such cases out of the comparison.
- **Publish scores, never answers.** The answers reflect the account that ran them. `just eval-report` keeps only case names and pass or fail per run.

## Before you merge

- [ ] `just validate` passes
- [ ] The description says what the skill does and when to use it, in words people type
- [ ] The skill verifies its own output before delivering
- [ ] No company, client or personal specifics (those go to the private repo)
- [ ] Evals: one trigger case and one near-miss, run at least once
- [ ] `just catalog` updated the README table
