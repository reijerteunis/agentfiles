#!/usr/bin/env python3
"""Scan local Claude Code session logs for signs that agents went wrong. Standard library only.

  python3 transcript_scan.py [--root ~/.claude/projects] [--days 7] [--excerpts 10]
  python3 transcript_scan.py --self-test

Counts, per project: sessions, failed tool calls (by tool), permission denials, and moments where the person
corrected the agent ("no, …", "that's wrong", "stop", "why did you…"). Prints a Markdown summary with a few
short excerpts. Everything stays on this machine. Never paste the excerpts anywhere public.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

CORRECTION_RE = re.compile(
    r"^(no[,.! ]|nope\b|wrong\b|that'?s not\b|that is not\b|stop\b|don'?t\b|do not\b|why did you\b|"
    r"you didn'?t\b|not what i\b|undo\b|revert\b|you broke\b|that broke\b)", re.I)
DENIAL_RE = re.compile(r"deny|denied|reject", re.I)


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def scan(root: Path, days: int, excerpts: int) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    stats: dict[str, Counter] = defaultdict(Counter)
    sessions: dict[str, set[str]] = defaultdict(set)
    tool_errors: Counter = Counter()
    samples: list[tuple[str, str, str]] = []
    for path in root.glob("*/*.jsonl"):
        if path.stat().st_mtime < time.time() - days * 86400:
            continue
        tool_names: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = rec.get("timestamp")
            if not ts:
                continue
            try:
                when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                continue
            if when < cutoff:
                continue
            project = short_project(rec.get("cwd") or path.parent.name)
            content = (rec.get("message") or {}).get("content")
            if rec.get("type") == "assistant" and isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        tool_names[b.get("id", "")] = b.get("name", "?")
            if rec.get("type") != "user":
                continue
            if rec.get("sessionId"):
                sessions[project].add(rec["sessionId"])
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error") is True:
                        stats[project]["tool_errors"] += 1
                        tool_errors[tool_names.get(b.get("tool_use_id", ""), "?")] += 1
            decision = rec.get("permissionDecision")
            if decision and DENIAL_RE.search(json.dumps(decision)):
                stats[project]["denials"] += 1
            said = text_of(content).strip()
            if said and not said.startswith("<") and CORRECTION_RE.match(said):
                stats[project]["corrections"] += 1
                if len(samples) < excerpts:
                    samples.append((when.strftime("%Y-%m-%d"), project, said[:140].replace("\n", " ")))
    for project, ids in sessions.items():
        stats[project]["sessions"] = len(ids)
    return {"stats": stats, "tool_errors": tool_errors, "samples": samples, "days": days}


def short_project(cwd: str) -> str:
    """~/Code/app stays as is; long paths keep their last two parts, so the table stays readable."""
    path = cwd.replace(str(Path.home()), "~")
    parts = path.split("/")
    return path if len(path) <= 40 else "…/" + "/".join(parts[-2:])


def report(r: dict) -> str:
    lines = [f"## Agent signals, last {r['days']} days", "", "| Project | Sessions | Tool errors | Denials | Corrections |", "|---|---|---|---|---|"]
    for project, c in sorted(r["stats"].items(), key=lambda kv: -(kv[1]["corrections"] + kv[1]["tool_errors"])):
        lines.append(f"| {project} | {c['sessions']} | {c['tool_errors']} | {c['denials']} | {c['corrections']} |")
    if r["tool_errors"]:
        lines += ["", "**Failing tools:** " + ", ".join(f"{t} ({n})" for t, n in r["tool_errors"].most_common(8))]
    if r["samples"]:
        lines += ["", "**Corrections (excerpts, local only):**"] + [f"- {d} · {p} · \"{s}\"" for d, p, s in r["samples"]]
    if not r["stats"]:
        lines += ["", "No sessions in this period."]
    return "\n".join(lines)


def self_test() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    old = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    recs = [
        {"type": "assistant", "timestamp": now, "cwd": "/w/app", "sessionId": "s1",
         "message": {"content": [{"type": "tool_use", "id": "t1", "name": "Bash"}]}},
        {"type": "user", "timestamp": now, "cwd": "/w/app", "sessionId": "s1",
         "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "is_error": True}]}},
        {"type": "user", "timestamp": now, "cwd": "/w/app", "sessionId": "s1", "message": {"content": "No, that's the wrong file"}},
        {"type": "user", "timestamp": now, "cwd": "/w/app", "sessionId": "s1", "message": {"content": "<system-reminder>no</system-reminder>"}},
        {"type": "user", "timestamp": now, "cwd": "/w/app", "sessionId": "s1", "permissionDecision": {"behavior": "deny"},
         "message": {"content": "ok"}},
        {"type": "user", "timestamp": old, "cwd": "/w/app", "sessionId": "s0", "message": {"content": "stop that"}},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "proj"
        d.mkdir()
        (d / "a.jsonl").write_text("\n".join(json.dumps(r) for r in recs) + "\nnot json\n")
        r = scan(Path(tmp), 7, 5)
        c = r["stats"]["/w/app"]
        checks = [c["tool_errors"] == 1, c["corrections"] == 1, c["denials"] == 1, c["sessions"] == 1,
                  r["tool_errors"]["Bash"] == 1, "wrong file" in report(r)]
    print("transcript_scan self-test:", "ok" if all(checks) else f"FAILED {checks} {dict(c)}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Scan Claude Code session logs for agent problems.")
    ap.add_argument("--root", type=Path, default=Path(os.path.expanduser("~/.claude/projects")))
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--excerpts", type=int, default=10)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    print(report(scan(args.root, args.days, args.excerpts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
