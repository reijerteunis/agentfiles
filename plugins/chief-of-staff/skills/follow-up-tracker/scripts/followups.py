#!/usr/bin/env python3
"""Check the promise tracker (follow-ups.md) and list what's due. Standard library only.

Usage:
  python3 followups.py follow-ups.md --check          validate rows, exit 1 on errors
  python3 followups.py follow-ups.md --due [--days 2] list open items overdue or due within N days
  python3 followups.py --self-test

The tracker is one Markdown table with the columns:
  ID | Promise | Direction | Who | Due | Source | Status
Direction is "I owe" or "owed to me"; Status is open, waiting, done or dropped; Due is YYYY-MM-DD or empty.
Date maths happens here, not in the model, so nothing slips through.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta

COLUMNS = ["ID", "Promise", "Direction", "Who", "Due", "Source", "Status"]
DIRECTIONS = {"I owe", "owed to me"}
STATUSES = {"open", "waiting", "done", "dropped"}


def parse(text: str) -> tuple[list[dict], list[str]]:
    rows, errors, header = [], [], None
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            if header != COLUMNS:
                errors.append(f"line {n}: header must be {' | '.join(COLUMNS)}")
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if len(cells) != len(COLUMNS):
            errors.append(f"line {n}: expected {len(COLUMNS)} columns, got {len(cells)}")
            continue
        row = dict(zip(COLUMNS, cells), line=n)
        if row["Direction"] not in DIRECTIONS:
            errors.append(f"line {n}: Direction '{row['Direction']}' must be one of {sorted(DIRECTIONS)}")
        if row["Status"] not in STATUSES:
            errors.append(f"line {n}: Status '{row['Status']}' must be one of {sorted(STATUSES)}")
        if row["Due"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["Due"]):
            errors.append(f"line {n}: Due '{row['Due']}' must be YYYY-MM-DD or empty")
        rows.append(row)
    ids = [r["ID"] for r in rows]
    errors += [f"duplicate ID {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    return rows, errors


def due(rows: list[dict], today: date, days: int) -> list[dict]:
    horizon = (today + timedelta(days=days)).isoformat()
    items = [r for r in rows if r["Status"] in ("open", "waiting") and r["Due"] and r["Due"] <= horizon]
    return sorted(items, key=lambda r: r["Due"])


def self_test() -> int:
    text = """| ID | Promise | Direction | Who | Due | Source | Status |
|---|---|---|---|---|---|---|
| F-001 | Send deck | I owe | Anna | 2026-10-12 | meeting | open |
| F-002 | Redlines | owed to me | Mark | 2026-10-15 | email | waiting |
| F-003 | Old thing | I owe | Bo | 2026-10-01 | email | done |
| F-004 | Bad | maybe | Cy | 13-10-2026 | email | pending |
"""
    rows, errors = parse(text)
    items = due(rows, date(2026, 10, 13), 2)
    checks = [len(rows) == 4, len(errors) == 3, [r["ID"] for r in items] == ["F-001", "F-002"]]
    print("followups self-test:", "ok" if all(checks) else f"FAILED {checks} {errors} {items}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Check follow-ups.md and list what's due.")
    ap.add_argument("tracker", nargs="?")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--due", action="store_true")
    ap.add_argument("--days", type=int, default=0, help="also include items due within N days")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.tracker:
        ap.error("give the path to follow-ups.md")
    with open(args.tracker, encoding="utf-8") as f:
        rows, errors = parse(f.read())
    for e in errors:
        print(f"error: {e}")
    if args.due:
        today = date.today()
        for r in due(rows, today, args.days):
            when = "OVERDUE" if r["Due"] < today.isoformat() else "due"
            print(f"{when} {r['Due']} · {r['ID']} · {r['Direction']} · {r['Who']} · {r['Promise']}")
    print(f"{'FAILED' if errors else 'ok'}: {len(rows)} items, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
