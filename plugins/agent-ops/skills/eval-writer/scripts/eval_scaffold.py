#!/usr/bin/env python3
"""Scaffold claude plugin eval cases for a skill: trigger cases and near-misses. Standard library only.

  python3 eval_scaffold.py --plugin-dir plugins/career --skill cover-letter \
      --trigger "Write me a cover letter for this job: ..." \
      --near-miss "Write a thank-you email after my interview"
  python3 eval_scaffold.py --self-test

Creates evals/<skill>-trigger-N/ (prompt.md plus a tool_used grader that the skill fired) and
evals/<skill>-near-miss-N/ (prompt.md plus a grader that it did NOT fire, scored in both arms).
Existing case folders are never overwritten. Add an output grader (llm or regex) to each trigger case by hand.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def prompt_md(description: str, tags: list[str], body: str, max_turns: int) -> str:
    return (f"---\ndescription: {description}\ntags: [{', '.join(tags)}]\nmax_turns: {max_turns}\n"
            f"allowed_tools: [Read, Glob, Grep, Skill]\n---\n\n{body.strip()}\n")


def fired(skill: str, never: bool) -> str:
    extra = "min: 0\nmax: 0\narm: both\n" if never else ""
    return (f"---\ntype: tool_used\ntool: Skill\ninput_match: '\"skill\"\\s*:\\s*\"(?:[\\w-]+:)?{skill}\"'\n{extra}---\n")


def scaffold(plugin_dir: Path, skill: str, triggers: list[str], near_misses: list[str]) -> list[Path]:
    if not NAME_RE.match(skill):
        raise ValueError("skill must be kebab-case")
    created = []
    evals = plugin_dir / "evals"
    for kind, prompts in (("trigger", triggers), ("near-miss", near_misses)):
        for n, text in enumerate(prompts, 1):
            case = evals / f"{skill}-{kind}-{n}"
            if case.exists():
                print(f"skip (exists): {case}")
                continue
            (case / "graders").mkdir(parents=True)
            if kind == "trigger":
                desc = f"A realistic request triggers {skill}."
                (case / "prompt.md").write_text(prompt_md(desc, [skill], text, 8))
                (case / "graders" / "skill-fired.md").write_text(fired(skill, never=False))
            else:
                desc = f"A near-miss request must not trigger {skill}."
                (case / "prompt.md").write_text(prompt_md(desc, ["negative", skill], text, 3))
                (case / "graders" / "not-fired.md").write_text(fired(skill, never=True))
            created.append(case)
    return created


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        made = scaffold(p, "cover-letter", ["Write my cover letter"], ["Say thanks to the interviewer"])
        again = scaffold(p, "cover-letter", ["Write my cover letter"], [])
        t = (p / "evals" / "cover-letter-trigger-1" / "prompt.md").read_text()
        g = (p / "evals" / "cover-letter-near-miss-1" / "graders" / "not-fired.md").read_text()
        checks = [len(made) == 2, again == [], "allowed_tools: [Read, Glob, Grep, Skill]" in t,
                  "Write my cover letter" in t, "min: 0" in g and "arm: both" in g and "cover-letter" in g]
        try:
            scaffold(p, "Bad Name", ["x"], [])
            checks.append(False)
        except ValueError:
            checks.append(True)
    print("eval_scaffold self-test:", "ok" if all(checks) else f"FAILED {checks}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold eval cases for a skill.")
    ap.add_argument("--plugin-dir", type=Path)
    ap.add_argument("--skill")
    ap.add_argument("--trigger", action="append", default=[], help="a realistic request that should trigger the skill")
    ap.add_argument("--near-miss", action="append", default=[], help="a related request that must not trigger it")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.plugin_dir and args.skill and (args.trigger or args.near_miss)):
        ap.error("give --plugin-dir, --skill and at least one --trigger or --near-miss")
    for case in scaffold(args.plugin_dir, args.skill, args.trigger, args.near_miss):
        print(f"created {case}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
