#!/usr/bin/env python3
"""Weekly delivery metrics from GitHub exports. Standard library only.

Export the data with the gh CLI, then compute:
  gh pr list --repo ORG/REPO --state merged --limit 1000 \
     --json number,title,createdAt,mergedAt,labels,additions,deletions > prs.json
  gh run list --repo ORG/REPO --workflow deploy.yml --limit 1000 \
     --json conclusion,createdAt,updatedAt,headBranch,event > runs.json     (optional)
  python3 delivery_metrics.py --prs prs.json [--runs runs.json] [--weeks 12] [--branch main]
  python3 delivery_metrics.py --self-test

Per ISO week: merged PRs, median and p90 lead time (PR opened to merged, hours), median PR size
(lines changed), the share of merged PRs that are reverts or hotfixes (a change-failure proxy), deploy
runs, the successful ones (deployment frequency) and their success rate. Prints a Markdown table plus a JSON snapshot. Numbers come only from the
exports: a week without data shows "-".
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

FAILURE_RE = re.compile(r"\b(revert|hotfix|rollback|roll back)\b", re.I)


def ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def week(dt: datetime) -> str:
    year, wk, _ = dt.isocalendar()
    return f"{year}-W{wk:02d}"


def pct(values: list[float], p: float) -> float:
    ordered = sorted(values)
    k = (len(ordered) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (k - lo)


def compute(prs: list[dict], runs: list[dict], weeks: int, branch: str, now: datetime) -> list[dict]:
    start = now - timedelta(weeks=weeks)
    by_week: dict[str, dict] = defaultdict(lambda: {"lead": [], "size": [], "fail": 0, "deploys": 0, "deploy_ok": 0})
    for pr in prs:
        if not pr.get("mergedAt"):
            continue
        merged = ts(pr["mergedAt"])
        if merged < start:
            continue
        w = by_week[week(merged)]
        w["lead"].append((merged - ts(pr["createdAt"])).total_seconds() / 3600)
        w["size"].append((pr.get("additions") or 0) + (pr.get("deletions") or 0))
        labels = " ".join(l.get("name", "") for l in pr.get("labels") or [])
        if FAILURE_RE.search(pr.get("title", "")) or FAILURE_RE.search(labels):
            w["fail"] += 1
    for run in runs:
        created = ts(run["createdAt"])
        if created < start or (branch and run.get("headBranch") not in (branch, None)):
            continue
        if run.get("conclusion") in ("cancelled", "skipped", None, ""):
            continue
        w = by_week[week(created)]
        w["deploys"] += 1
        w["deploy_ok"] += run.get("conclusion") == "success"
    rows = []
    for wk in sorted(by_week):
        d = by_week[wk]
        merged = len(d["lead"])
        rows.append({
            "week": wk,
            "merged_prs": merged,
            "lead_time_median_h": round(statistics.median(d["lead"]), 1) if merged else None,
            "lead_time_p90_h": round(pct(d["lead"], 0.9), 1) if merged else None,
            "pr_size_median": int(statistics.median(d["size"])) if merged else None,
            "revert_hotfix_pct": round(100 * d["fail"] / merged, 1) if merged else None,
            "deploys": d["deploys"] if runs else None,
            "deploys_ok": d["deploy_ok"] if runs else None,
            "deploy_success_pct": round(100 * d["deploy_ok"] / d["deploys"], 1) if runs and d["deploys"] else None,
        })
    return rows


def table(rows: list[dict]) -> str:
    cols = ["week", "merged_prs", "lead_time_median_h", "lead_time_p90_h", "pr_size_median",
            "revert_hotfix_pct", "deploys", "deploys_ok", "deploy_success_pct"]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join("-" if r[c] is None else str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def self_test() -> int:
    now = datetime(2026, 10, 12, tzinfo=timezone.utc)
    prs = [
        {"title": "Add search", "createdAt": "2026-10-05T08:00:00Z", "mergedAt": "2026-10-05T18:00:00Z", "additions": 120, "deletions": 30},
        {"title": "Revert search", "createdAt": "2026-10-06T08:00:00Z", "mergedAt": "2026-10-06T09:00:00Z", "additions": 30, "deletions": 120},
        {"title": "Old", "createdAt": "2025-01-01T08:00:00Z", "mergedAt": "2025-01-02T08:00:00Z"},
        {"title": "Open PR", "createdAt": "2026-10-07T08:00:00Z", "mergedAt": None},
    ]
    runs = [{"conclusion": "success", "createdAt": "2026-10-05T19:00:00Z", "headBranch": "main"},
            {"conclusion": "failure", "createdAt": "2026-10-06T10:00:00Z", "headBranch": "main"},
            {"conclusion": "success", "createdAt": "2026-10-06T11:00:00Z", "headBranch": "feature"}]
    rows = compute(prs, runs, 12, "main", now)
    r = rows[0] if rows else {}
    checks = [len(rows) == 1, r.get("merged_prs") == 2, r.get("lead_time_median_h") == 5.5,
              r.get("revert_hotfix_pct") == 50.0, r.get("deploys") == 2, r.get("deploys_ok") == 1,
              r.get("deploy_success_pct") == 50.0,
              r.get("pr_size_median") == 150]
    print("delivery_metrics self-test:", "ok" if all(checks) else f"FAILED {checks} {rows}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Weekly delivery metrics from gh exports.")
    ap.add_argument("--prs", help="JSON from gh pr list (merged)")
    ap.add_argument("--runs", help="JSON from gh run list for the deploy workflow")
    ap.add_argument("--weeks", type=int, default=12)
    ap.add_argument("--branch", default="main", help="deploy branch to count runs for ('' for all)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.prs:
        ap.error("--prs is required")
    with open(args.prs, encoding="utf-8") as f:
        prs = json.load(f)
    runs = []
    if args.runs:
        with open(args.runs, encoding="utf-8") as f:
            runs = json.load(f)
    rows = compute(prs, runs, args.weeks, args.branch, datetime.now(timezone.utc))
    print(table(rows))
    print("\n```json")
    print(json.dumps(rows, indent=2))
    print("```")
    return 0


if __name__ == "__main__":
    sys.exit(main())
