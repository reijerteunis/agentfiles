#!/usr/bin/env python3
"""Publish eval results without publishing what the agents wrote: keep the scores, drop the transcripts.
Standard library only.

Usage:
  python3 scripts/eval_report.py import <result.json>...   trim `claude plugin eval --json` output into docs/evals/data/
  python3 scripts/eval_report.py import --merge <result.json>   replace only the re-run cases in a plugin's data
  python3 scripts/eval_report.py render [--check]          regenerate docs/evals/README.md and the results block in
                                                           README.md (--check: exit 1 if either is out of date)
  python3 scripts/eval_report.py --self-test

The raw output holds every answer in full, and the answers reflect the account that ran them. Only case names and
the score of each run are kept, so the published numbers can be regenerated without publishing a single answer.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- evals:start -->", "<!-- evals:end -->"


def kind(case: dict) -> str:
    graders = case.get("graders", [])
    tool = [g for g in graders if g.get("type") == "tool_used"]
    if any(g.get("config", {}).get("max") == 0 for g in tool):
        return "near-miss"
    if tool and len(tool) == len(graders):
        return "trigger-only"  # without the plugin no skill can fire, so the baseline fails by construction
    if tool:
        return "trigger"
    return "output"


def compared(case: dict) -> bool:
    return case["kind"] != "trigger-only" and bool(case["with"])


def trim(result: dict) -> dict:
    plugins = result.get("suite", {}).get("plugins", [])
    if len(plugins) != 1:
        raise ValueError("expected a result for exactly one plugin")
    cases = []
    for case in result["cases"]:
        with_runs, without_runs = case["arms"].get("with", []), case["arms"].get("without", [])
        fired = [next((g["passed"] for g in run["graders"] if g.get("withOnly")), None) for run in with_runs]
        if kind(case) == "trigger-only":
            fired = [run["score"] >= 1 for run in with_runs]
        cases.append({"name": case["name"], "kind": kind(case),
                      "with": [run["score"] for run in with_runs], "without": [run["score"] for run in without_runs],
                      "fired": fired if any(f is not None for f in fired) else None,
                      "errors": sum(1 for run in with_runs + without_runs if run.get("error"))})
    runs = max((len(c["with"]) for c in cases), default=0)
    return {"plugin": plugins[0]["name"], "ran": result["startedAt"][:10], "claude": result.get("claudeVersion", ""),
            "runs_per_case": runs, "cost_usd": round(result.get("costUsd", 0), 2), "cases": cases}


def merge(old: dict, new: dict) -> dict:
    """Cases in the new run replace the same cases in the old data; the rest stay. For re-running only what a change touched."""
    if old["plugin"] != new["plugin"]:
        raise ValueError(f"can't merge {new['plugin']} into {old['plugin']}")
    fresh = {c["name"]: c for c in new["cases"]}
    cases = [fresh.pop(c["name"], c) for c in old["cases"]] + list(fresh.values())
    return {**old, "ran": max(old["ran"], new["ran"]), "claude": new["claude"] or old["claude"],
            "runs_per_case": max(len(c["with"]) for c in cases),
            "cost_usd": round(old["cost_usd"] + new["cost_usd"], 2), "cases": cases}


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def pct(value: float | None) -> str:
    return "-" if value is None else f"{value:.0%}"


def summary(data: dict) -> dict:
    cases = data["cases"]
    scored = [c for c in cases if compared(c)]
    deltas = [mean(c["with"]) - mean(c["without"]) for c in scored if c["without"]]
    fired = [f for c in cases if c["kind"] in ("trigger", "trigger-only") and c["fired"] for f in c["fired"] if f is not None]
    near = [s for c in cases if c["kind"] == "near-miss" for s in c["with"]]
    return {"cases": len(cases), "with": mean([s for c in scored for s in c["with"]]),
            "without": mean([s for c in scored for s in c["without"]]),
            "better": sum(1 for d in deltas if d > 0), "same": sum(1 for d in deltas if d == 0),
            "worse": sum(1 for d in deltas if d < 0),
            "fired": mean([1.0 if f else 0.0 for f in fired]) if fired else None,
            "false_triggers": f"{sum(1 for s in near if s < 1)} of {len(near)}" if near else "-"}


def overall(datasets: list[dict]) -> str:
    """One sentence over every case with work to do: a near-miss passes trivially without the plugin, so it's left out."""
    cases = [c for d in datasets for c in d["cases"] if c["kind"] != "near-miss" and compared(c) and c["without"]]
    deltas = [mean(c["with"]) - mean(c["without"]) for c in cases]
    plain = sum(1 for c in cases if all(s >= 1 for s in c["without"]))
    plugin = sum(1 for c in cases if all(s >= 1 for s in c["with"]))
    return (f"Of the {len(cases)} cases with work to do (near-misses aside), the plain model alone passed {plain} in every run, "
            f"and {plugin} passed in every run with the plugins. The plugins did better on {sum(1 for d in deltas if d > 0)}, "
            f"the same on {sum(1 for d in deltas if d == 0)} and worse on {sum(1 for d in deltas if d < 0)}.")


def summary_table(datasets: list[dict]) -> list[str]:
    lines = ["| Plugin | Cases | Runs per case | Score with the plugin | Without it | Better / same / worse with it "
             "| Right skill fired | False triggers |", "|---|---|---|---|---|---|---|---|"]
    for d in sorted(datasets, key=lambda d: (-d["runs_per_case"], d["plugin"])):
        s = summary(d)
        lines.append(f"| [`{d['plugin']}`](docs/evals/README.md#{d['plugin']}) | {s['cases']} | {d['runs_per_case']} "
                     f"| {pct(s['with'])} | {pct(s['without'])} | {s['better']} / {s['same']} / {s['worse']} "
                     f"| {pct(s['fired'])} | {s['false_triggers']} |")
    return lines


def render_details(datasets: list[dict]) -> str:
    claude = sorted({d["claude"] for d in datasets if d["claude"]})
    lines = ["# Eval results", "", "<!-- Generated by scripts/eval_report.py from docs/evals/data/. Don't edit by hand. -->", "",
             "Every case runs in two arms: with the plugin, and without it (the same model and settings, no plugin). "
             "LLM graders are judged by Claude Haiku with three votes. The runs happen on the author's machine"
             + (f" with Claude Code {', '.join(claude)}" if claude else "") + ". Only scores are published: the answers "
             "themselves stay on that machine, because they reflect the account that ran them.", "",
             "- **Score:** the average, over all runs, of the share of scored graders that passed. In the per-case tables, "
             "**2/3** means two of three runs passed every grader.",
             "- **Better / same / worse:** cases whose average score is higher, equal or lower with the plugin than without it. "
             "A case that also passes without the plugin shows what the model already does well; it still guards against regressions.",
             "- **Right skill fired:** in trigger cases, the share of runs where the expected skill loaded. A trigger-only case "
             "checks nothing else, and is left out of the comparison because the plain model can't load a plugin's skill.",
             "- **False triggers:** near-miss runs where one of the plugin's skills loaded although it shouldn't have.", "",
             "Run them yourself with `just eval <plugin>`, then `just eval-report <result.json>`.", "",
             "## Summary", ""]
    lines += [line.replace("](docs/evals/README.md#", "](#") for line in summary_table(datasets)] + ["", overall(datasets)]
    for d in sorted(datasets, key=lambda d: (-d["runs_per_case"], d["plugin"])):
        lines += ["", f"## {d['plugin']}", "",
                  f"Run on {d['ran']}, {d['runs_per_case']} run{'s' if d['runs_per_case'] != 1 else ''} per case and arm.", "",
                  "| Case | Type | With the plugin | Without it | Δ | Right skill fired |", "|---|---|---|---|---|---|"]
        for c in d["cases"]:
            w, wo = (mean(c["with"]), mean(c["without"])) if compared(c) else (None, None)
            delta = "-" if w is None or wo is None else f"{w - wo:+.2f}"
            fired = "-" if not c["fired"] else f"{sum(1 for f in c['fired'] if f)}/{len(c['fired'])}"
            passed = lambda runs: "-" if not runs or not compared(c) else f"{sum(1 for s in runs if s >= 1)}/{len(runs)}"
            note = f" ({c['errors']} run error{'s' if c['errors'] != 1 else ''})" if c.get("errors") else ""
            lines.append(f"| {c['name']}{note} | {c['kind']} | {passed(c['with'])} | {passed(c['without'])} | {delta} | {fired} |")
    return "\n".join(lines) + "\n"


def load(data_dir: Path) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(data_dir.glob("*.json"))]


def render(root: Path, check: bool) -> int:
    datasets = load(root / "docs" / "evals" / "data")
    if not datasets:
        print("no data in docs/evals/data; run `import` first")
        return 1
    details_path, readme_path = root / "docs" / "evals" / "README.md", root / "README.md"
    details = render_details(datasets)
    readme = readme_path.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        print(f"README.md has no {START} … {END} block")
        return 1
    head, rest = readme.split(START, 1)
    block = "\n".join([START] + summary_table(datasets) + ["", overall(datasets), END])
    new_readme = head + block + rest.split(END, 1)[1]
    stale = [p.name for p, new in ((details_path, details), (readme_path, new_readme))
             if not p.exists() or p.read_text(encoding="utf-8") != new]
    if check:
        for name in stale:
            print(f"error: {name} is out of date: run `just eval-report`")
        return 1 if stale else 0
    details_path.write_text(details, encoding="utf-8")
    readme_path.write_text(new_readme, encoding="utf-8")
    print(f"wrote {details_path.relative_to(root)} and the results block in README.md")
    return 0


def self_test() -> int:
    def run(score: float, fired: bool | None = None, error: str | None = None) -> dict:
        graders = [{"name": "rubric", "passed": score >= 1, "withOnly": False}]
        if fired is not None:
            graders.append({"name": "skill-fired", "passed": fired, "withOnly": True})
        return {"score": score, "passed": score >= 1, "graders": graders, "error": error,
                "evidence": "SECRET ANSWER", "tracePath": "/tmp/x/trace.jsonl"}

    raw = {"startedAt": "2026-10-13T07:11:11.769Z", "claudeVersion": "2.1.296", "costUsd": 1.2842,
           "suite": {"plugins": [{"name": "demo", "path": "/home/someone/demo"}]},
           "cases": [
               {"name": "does-the-job", "graders": [{"type": "llm"}, {"type": "tool_used", "config": {"tool": "Skill"}}],
                "arms": {"with": [run(1, True), run(1, True), run(0, False)], "without": [run(0), run(0), run(0)]}},
               {"name": "stays-quiet", "graders": [{"type": "tool_used", "config": {"tool": "Skill", "max": 0}}],
                "arms": {"with": [run(1), run(0), run(1)], "without": [run(1), run(1), run(1)]}},
               {"name": "already-fine", "graders": [{"type": "llm"}],
                "arms": {"with": [run(1), run(1), run(1, error="timeout")], "without": [run(1), run(1), run(1)]}},
               {"name": "only-fires", "graders": [{"type": "tool_used", "config": {"tool": "Skill"}}],
                "arms": {"with": [run(1), run(1), run(0)], "without": [run(0), run(0), run(0)]}}]}
    data = trim(raw)
    text = json.dumps(data)
    s = summary(data)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "docs" / "evals" / "data").mkdir(parents=True)
        (root / "docs" / "evals" / "data" / "demo.json").write_text(text)
        (root / "README.md").write_text(f"# x\n{START}\nold\n{END}\ntail\n")
        first = render(root, check=False)
        fresh = render(root, check=True)
        readme = (root / "README.md").read_text()
        details = (root / "docs" / "evals" / "README.md").read_text()
    checks = [
        "SECRET" not in text and "/tmp/" not in text and "/home/" not in text,
        [c["kind"] for c in data["cases"]] == ["trigger", "near-miss", "output", "trigger-only"],
        data["runs_per_case"] == 3 and data["cost_usd"] == 1.28 and data["cases"][2]["errors"] == 1,
        (s["better"], s["same"], s["worse"]) == (1, 1, 1),
        s["false_triggers"] == "1 of 3" and abs(s["fired"] - 4 / 6) < 1e-9,
        first == 0 and fresh == 0,
        "| [`demo`](docs/evals/README.md#demo) | 4 | 3 | 78% | 67% | 1 / 1 / 1 | 67% | 1 of 3 |" in readme,
        readme.endswith("tail\n") and "old" not in readme,
        "| does-the-job | trigger | 2/3 | 0/3 | +0.67 | 2/3 |" in details,
        "| already-fine (1 run error) | output | 3/3 | 3/3 | +0.00 | - |" in details,
        "| only-fires | trigger-only | - | - | - | 2/3 |" in details,
        overall([data]) == "Of the 2 cases with work to do (near-misses aside), the plain model alone passed 1 in every run, "
                           "and 1 passed in every run with the plugins. The plugins did better on 1, the same on 1 and worse on 0.",
        overall([data]) in readme and overall([data]) in details,
    ]
    rerun = {**data, "ran": "2026-10-14", "cost_usd": 0.5,
             "cases": [{**data["cases"][0], "with": [1, 1, 1]},
                       {"name": "new-case", "kind": "output", "with": [1], "without": [0], "fired": None, "errors": 0}]}
    merged = merge(data, rerun)
    checks += [
        [c["name"] for c in merged["cases"]] == ["does-the-job", "stays-quiet", "already-fine", "only-fires", "new-case"],
        merged["cases"][0]["with"] == [1, 1, 1] and merged["cases"][1] == data["cases"][1],
        merged["ran"] == "2026-10-14" and merged["cost_usd"] == 1.78 and merged["runs_per_case"] == 3,
    ]
    print("eval_report self-test:", "ok" if all(checks) else f"FAILED {checks}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish eval scores without the transcripts.")
    ap.add_argument("command", nargs="?", choices=["import", "render"])
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--check", action="store_true", help="render: exit 1 if the generated files are out of date")
    ap.add_argument("--merge", action="store_true", help="import: replace only the re-run cases in the plugin's existing data")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_intermixed_args()  # so `import --merge <files>` works as documented
    if args.self_test:
        return self_test()
    if args.command == "import":
        if not args.files:
            ap.error("give one or more result.json files from `claude plugin eval --json`")
        out = ROOT / "docs" / "evals" / "data"
        out.mkdir(parents=True, exist_ok=True)
        for f in args.files:
            data = trim(json.loads(f.read_text(encoding="utf-8")))
            target = out / f"{data['plugin']}.json"
            if args.merge:
                if not target.exists():
                    ap.error(f"--merge: no data for {data['plugin']} yet; import a full run first")
                rerun = [c["name"] for c in data["cases"]]
                data = merge(json.loads(target.read_text(encoding="utf-8")), data)
                print(f"merged {data['plugin']}: re-ran {', '.join(rerun)}")
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            print(f"imported {data['plugin']}: {len(data['cases'])} cases, {data['runs_per_case']} runs per case")
        return render(ROOT, check=False)
    if args.command == "render":
        return render(ROOT, check=args.check)
    ap.error("give a command: import or render")
    return 2


if __name__ == "__main__":
    sys.exit(main())
