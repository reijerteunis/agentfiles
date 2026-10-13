---
name: eval-writer
description: Writes and runs behaviour evals for a skill or plugin with claude plugin eval, covering trigger cases in real words, near-misses that must not trigger, output graders and regression cases, then tunes the description until the skill triggers reliably. Use it when someone wants evals or tests for a skill, asks whether a skill triggers, or needs a regression test after an agent mistake.
license: MIT
compatibility: Runs a Python 3 scaffolding script; running the evals needs Claude Code with claude plugin eval (real model calls that cost usage).
---

# Eval writer

A skill without evals is a hope. Evals show three things: does it trigger when it should, does it stay quiet when it shouldn't, and is the output better than no skill at all?

## 1. Collect prompts

For the skill, write prompts the way real people type them. Never use the skill's name, and never paraphrase its description.
- **Triggers:** 3–10 realistic requests, from direct ("write my cover letter") to indirect ("they want a motivation letter by Friday").
- **Near-misses:** 2–5 related requests that belong to a sibling skill or need no skill at all. Use the routing lines in the description: each "Not for … (use X)" is a near-miss to test.
- **Regressions:** the exact prompt from any past mistake, for example one found by `agent-retro`.

## 2. Scaffold

```bash
python3 scripts/eval_scaffold.py --plugin-dir <plugin> --skill <name> \
  --trigger "<request 1>" --trigger "<request 2>" --near-miss "<related request>"
```

It writes each case's `prompt.md`, and a `tool_used` grader for "fired" or "did not fire". Near-misses are scored in both arms. Existing cases are never overwritten.

## 3. Add output graders by hand

Give each trigger case one grader on the result:
- **regex** for long or structured output: a required section, a forbidden phrase (`match: not_contains`), a number.
- **llm** for short output, with concrete lines: "PASS if … FAIL if …". Judge outcomes, not formatting.
- **file_exists** when the skill writes a file.

Keep the steps a case needs in the prompt itself (each run starts in an empty folder), and grant only the tools it needs in `allowed_tools`.

## 4. Run and read

```bash
claude plugin eval <plugin> --case '<skill>-*'                     # 3 runs per arm, with Δ against no plugin
claude plugin eval <plugin> --case '<skill>-*' --runs 1 --ablation none   # a cheap pass while writing graders
```

- **Trigger rate** below about 90% on triggers: rewrite the description's "Use it when" part with the words from the failing prompts.
- **Fires on near-misses:** add or sharpen routing lines.
- **Δ near zero:** the skill isn't adding much. Strengthen what it does that the model wouldn't do alone, or delete it.
- **Negative Δ with the skill firing:** read both answers before anything else. If the skill asked questions where the plain model drafted, fix the skill. If the answers are equally good, suspect the judge: rerun with `--judge-model sonnet` and tighten the rubric.

Change one thing at a time, and rerun only the affected cases. Evals cost usage, so say so before running a full suite.

## Gotchas

- **The sandbox is empty:** no repository, workspace, connectors or user instructions. "Fix this in my repo" tests the sandbox, not the skill. Say in the prompt what the agent has, and what to deliver in the reply.
- **A case that passes without the plugin measures the model.** Keep it as a regression guard, but to show what the skill adds, grade what only the skill produces: its structure, its script's numbers, its gates.
- **Grade what the prompt makes possible.** A grader that wants findings the prompt gives no data for fails good answers.
- **One requirement per grader when it matters.** The Haiku judge waves through a requirement tacked onto the end of a PASS line. Give it its own grader and say what doesn't count.
- **Test where models slip.** Plain models pass the obvious case; the skill shows its worth on the trap: a claim's scope widened, a free extra outside the discount policy, a best-case number without its share.
- **Every trigger case needs a grader on the result.** A case graded only on whether the skill fired can't be compared with the plain model, which has no plugin skill to load.
- **Publish scores, never answers.** The answers reflect the account that ran them.
