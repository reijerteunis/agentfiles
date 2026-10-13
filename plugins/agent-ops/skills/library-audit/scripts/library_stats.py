#!/usr/bin/env python3
"""Audit a skills repository: size, budget, look-alikes, routing lines and eval coverage. Stdlib only.

  python3 library_stats.py <repo> [--budget 8000] [--similarity 0.30]
  python3 library_stats.py --self-test

<repo> has a .claude-plugin/marketplace.json listing plugins with ./relative sources (the agentfiles layout).
Reports per plugin: skills, description characters, skills without an eval case. Library-wide: the total
description size against the listing budget, and pairs of skills whose descriptions overlap strongly without a
routing line ("use <other-skill>") pointing between them: the look-alikes that make agents pick wrong.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
import tempfile
from pathlib import Path

STOP = set("""a an and are as at be by for from has have in into is it its of on or that the their them they this
to was were when which while who will with use used using it's them your you skill skills someone asks wants
when also more less other than then what how does about over under each every only like such""".split())


def description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ""
    fm = text[4:].split("\n---", 1)[0].splitlines()
    for i, line in enumerate(fm):
        if line.startswith("description:"):
            value = line[len("description:"):].strip()
            if value in (">", "|", ">-", "|-"):
                block = []
                for nxt in fm[i + 1:]:
                    if nxt.startswith((" ", "\t")):
                        block.append(nxt.strip())
                    else:
                        break
                return " ".join(block)
            return value.strip('"').strip("'")
    return ""


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z-]{3,}", text.lower()) if w not in STOP}


def audit(repo: Path, budget: int, threshold: float) -> dict:
    market = json.loads((repo / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    skills, plugins = [], []
    for entry in market.get("plugins", []):
        pdir = repo / entry["source"]
        eval_text = " ".join(p.read_text(encoding="utf-8", errors="ignore") for p in pdir.glob("evals/**/*.md"))
        names = []
        for sdir in sorted(d for d in (pdir / "skills").glob("*") if (d / "SKILL.md").exists()):
            desc = description(sdir / "SKILL.md")
            skills.append({"plugin": entry["name"], "name": sdir.name, "desc": desc,
                           "tested": re.search(rf"(?<![\w-]){re.escape(sdir.name)}(?![\w-])", eval_text) is not None})
            names.append(sdir.name)
        mine = [s for s in skills if s["plugin"] == entry["name"]]
        plugins.append({"plugin": entry["name"], "skills": len(names), "chars": sum(len(s["desc"]) for s in mine),
                        "untested": [s["name"] for s in mine if not s["tested"]]})
    lookalikes = []
    for a, b in itertools.combinations(skills, 2):
        wa, wb = words(a["desc"]), words(b["desc"])
        if not wa or not wb:
            continue
        sim = len(wa & wb) / len(wa | wb)
        routed = f"use {b['name']}" in a["desc"] or f"use {a['name']}" in b["desc"]
        if sim >= threshold and not routed:
            lookalikes.append({"a": a["name"], "b": b["name"], "similarity": round(sim, 2)})
    lookalikes.sort(key=lambda x: -x["similarity"])
    total = sum(p["chars"] for p in plugins)
    return {"plugins": plugins, "skills": len(skills), "total_chars": total, "budget": budget,
            "lookalikes": lookalikes, "no_description": [s["name"] for s in skills if not s["desc"]]}


def report(r: dict) -> str:
    lines = ["| Plugin | Skills | Description chars | Without evals |", "|---|---|---|---|"]
    for p in r["plugins"]:
        lines.append(f"| {p['plugin']} | {p['skills']} | {p['chars']:,} | {', '.join(p['untested']) or '-'} |")
    over = r["total_chars"] > r["budget"]
    lines += ["", f"**Catalog:** {r['skills']} skills, {r['total_chars']:,} description characters. Claude Code's skill "
              f"listing gets about 1% of the context window (~{r['budget']:,} characters at 200k tokens)"
              + (". Over budget with everything enabled: the least-used skills lose their descriptions and stop "
                 "triggering reliably. Shorten descriptions, and enable plugins as packs." if over else ".")]
    if r["lookalikes"]:
        lines += ["", "**Look-alikes without routing lines:**"]
        lines += [f"- {x['a']} ↔ {x['b']} (overlap {x['similarity']})" for x in r["lookalikes"][:15]]
    if r["no_description"]:
        lines += ["", "**Missing descriptions:** " + ", ".join(r["no_description"])]
    return "\n".join(lines)


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / ".claude-plugin").mkdir()
        (repo / ".claude-plugin" / "marketplace.json").write_text(json.dumps(
            {"name": "t", "owner": {"name": "t"}, "plugins": [{"name": "p", "source": "./plugins/p"}]}))
        def skill(name: str, desc: str) -> None:
            d = repo / "plugins" / "p" / "skills" / name
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {desc}\n---\nBody\n")
        skill("cover-letter", "Writes tailored cover letters for job applications using the candidate's master resume.")
        skill("motivation-letter", "Writes tailored motivation letters for job applications using the candidate's master resume.")
        skill("routed-letter", "Writes tailored cover letters for job applications using the candidate resume (use cover-letter).")
        (repo / "plugins" / "p" / "skills" / "folded").mkdir()
        (repo / "plugins" / "p" / "skills" / "folded" / "SKILL.md").write_text("---\nname: folded\ndescription: >\n  Plans trips\n  and packing.\n---\n")
        (repo / "plugins" / "p" / "evals" / "c1").mkdir(parents=True)
        (repo / "plugins" / "p" / "evals" / "c1" / "prompt.md").write_text("checks cover-letter fires")
        r = audit(repo, 100, 0.5)
        pairs = {(x["a"], x["b"]) for x in r["lookalikes"]}
        checks = [r["skills"] == 4, ("cover-letter", "motivation-letter") in pairs,
                  ("cover-letter", "routed-letter") not in pairs,
                  r["plugins"][0]["untested"] == ["folded", "motivation-letter", "routed-letter"],
                  "Over budget" in report(r), description(repo / "plugins/p/skills/folded/SKILL.md") == "Plans trips and packing."]
    print("library_stats self-test:", "ok" if all(checks) else f"FAILED {checks} {r}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit a skills repository.")
    ap.add_argument("repo", nargs="?", type=Path)
    ap.add_argument("--budget", type=int, default=8000, help="approximate listing budget in characters")
    ap.add_argument("--similarity", type=float, default=0.30, help="word-overlap threshold for look-alikes (0-1)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.repo:
        ap.error("give the repository path")
    print(report(audit(args.repo, args.budget, args.similarity)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
