---
name: agent-retro
description: Turns agent mistakes into durable fixes. It scans local session logs for failed tool calls, denials and corrections, finds the real cause, places the fix at the lowest layer that works (permission, hook, validator, instruction, skill or context), adds a regression test and records the retro. Use it when someone says an agent keeps making the same mistake, ignored an instruction or did something it shouldn't have.
license: MIT
compatibility: Runs a Python 3 script on local Claude Code session logs (~/.claude/projects), with the person's agreement.
---

# Agent retro

When an agent makes the same mistake twice, the setup is wrong, not the agent. Find the cause, fix it where the fix is cheapest and most reliable, and prove it with a test.

## 1. Find the problems

- **Reported:** what the person saw, with an example. Ask for the prompt, what the agent did, and what should have happened.
- **Scanned:** with the person's agreement, run

  ```bash
  python3 scripts/transcript_scan.py --days 7 --excerpts 10
  ```

  It counts failed tool calls (by tool), permission denials and the moments the person corrected the agent, per project, with short excerpts. The excerpts stay on this machine. Look for repetition: the same tool failing, the same correction, the same project.

## 2. Find the cause

For each recurring problem, ask why until you reach something in the setup:

| Cause | Typical sign | Typical fix layer |
|---|---|---|
| Missing guardrail | It did something it must never do | Permission or hook |
| Missing fact or context | It guessed a name, a path or a convention | Project AGENTS.md or a context skill |
| Unclear or conflicting instruction | It followed one rule and broke another | Rewrite or remove one rule (`agent-instructions`) |
| Skill didn't trigger | It improvised instead of using the procedure | The skill's description and routing lines (`eval-writer` to prove it) |
| Wrong skill triggered | A look-alike won | Routing lines, or merge the look-alikes (`library-audit`) |
| Skill gap | No procedure existed for a recurring task | A new skill (`skill-author`) |
| Environment | A tool, path or permission is missing | Install, configure, or fix the shell setup |

The layers and how to choose between them are in the agent-ops skill's layer guide. Use the lowest layer that reliably prevents the problem.

## 3. Fix and test

1. Make the smallest fix at that layer. For permissions and hooks, use `guardrail-design`.
2. Add the test that would have caught it:
   - an eval case that reproduces the original prompt (`eval-writer`),
   - a validator rule,
   - or a hook test.
3. If a skill was involved, add a line to its **Gotchas** section, written as a rule.
4. Run the validation and the new test.

## 4. Record

Write `retros/YYYY-MM-DD-<slug>.md` in the agent-ops workspace, using the template in its workspace reference: what happened, the cause, the fix and its layer, the test, and a one-line lesson. A lesson that's free of personal and company details can later go into the public playbook or a skill's gotchas.
