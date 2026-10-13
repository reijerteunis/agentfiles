#!/usr/bin/env python3
"""Time audit of a calendar export: where the hours went and how much deep-work time is left. Stdlib only.

Input: a JSON list of events, as fetched from the calendar connector and saved to a file:
  [{"title": "...", "start": "2026-10-13T09:00:00+02:00", "end": "...", "attendees": 3,
    "category": "optional, e.g. 1:1 / external / recruiting / focus"}]
Usage:
  python3 time_audit.py events.json [--workday 09:00-18:00] [--deep 90]
  python3 time_audit.py --self-test

Per day: meeting hours, number of meetings, back-to-back transitions, and the free blocks of at least --deep
minutes inside the workday. Overall: hours per category (from "category", else a guess from attendee count).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta


def guess_category(ev: dict) -> str:
    if ev.get("category"):
        return ev["category"]
    n = ev.get("attendees") or 0
    title = (ev.get("title") or "").lower()
    if n <= 1 and any(w in title for w in ("focus", "deep work", "block", "hold")):
        return "focus"
    if n <= 1:
        return "solo / holds"
    if n == 2:
        return "1:1"
    return "group"


def audit(events: list[dict], workday: tuple[str, str], deep_min: int) -> dict:
    days: dict[str, list[tuple[datetime, datetime, dict]]] = defaultdict(list)
    for ev in events:
        start, end = datetime.fromisoformat(ev["start"]), datetime.fromisoformat(ev["end"])
        if end > start:
            days[start.date().isoformat()].append((start, end, ev))
    by_category: dict[str, float] = defaultdict(float)
    per_day = []
    for day in sorted(days):
        items = sorted(days[day], key=lambda t: t[0])
        meetings = [(s, e, ev) for s, e, ev in items if guess_category(ev) != "focus"]
        hours = sum((e - s).total_seconds() for s, e, _ in meetings) / 3600
        back_to_back = sum(1 for (_, e1, _), (s2, _, _) in zip(meetings, meetings[1:]) if s2 <= e1)
        for s, e, ev in items:
            by_category[guess_category(ev)] += (e - s).total_seconds() / 3600
        tz = items[0][0].tzinfo
        ws = datetime.fromisoformat(f"{day}T{workday[0]}:00").replace(tzinfo=tz)
        we = datetime.fromisoformat(f"{day}T{workday[1]}:00").replace(tzinfo=tz)
        free, cursor = [], ws
        for s, e, _ in meetings:
            if s > cursor and (s - cursor) >= timedelta(minutes=deep_min):
                free.append(f"{cursor:%H:%M}-{min(s, we):%H:%M}")
            cursor = max(cursor, e)
        if we > cursor and (we - cursor) >= timedelta(minutes=deep_min):
            free.append(f"{cursor:%H:%M}-{we:%H:%M}")
        per_day.append({"day": day, "meeting_hours": round(hours, 2), "meetings": len(meetings),
                        "back_to_back": back_to_back, "deep_blocks": free})
    return {"per_day": per_day, "by_category": {k: round(v, 2) for k, v in sorted(by_category.items())}}


def self_test() -> int:
    tz = "+02:00"
    evs = [
        {"title": "Standup", "start": f"2026-10-13T09:00:00{tz}", "end": f"2026-10-13T09:30:00{tz}", "attendees": 6},
        {"title": "1:1 Sam", "start": f"2026-10-13T09:30:00{tz}", "end": f"2026-10-13T10:00:00{tz}", "attendees": 2},
        {"title": "Focus block", "start": f"2026-10-13T10:00:00{tz}", "end": f"2026-10-13T12:00:00{tz}", "attendees": 1},
        {"title": "Client call", "start": f"2026-10-13T15:00:00{tz}", "end": f"2026-10-13T16:00:00{tz}", "attendees": 4,
         "category": "external"},
    ]
    r = audit(evs, ("09:00", "18:00"), 90)
    d = r["per_day"][0]
    checks = [d["meeting_hours"] == 2.0, d["meetings"] == 3, d["back_to_back"] == 1,
              d["deep_blocks"] == ["10:00-15:00", "16:00-18:00"],
              r["by_category"] == {"1:1": 0.5, "external": 1.0, "focus": 2.0, "group": 0.5}]
    print("time_audit self-test:", "ok" if all(checks) else f"FAILED {checks} {r}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Time audit of a calendar export.")
    ap.add_argument("events", nargs="?")
    ap.add_argument("--workday", default="09:00-18:00")
    ap.add_argument("--deep", type=int, default=90, help="minimum minutes for a deep-work block")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.events:
        ap.error("give the events JSON file")
    with open(args.events, encoding="utf-8") as f:
        events = json.load(f)
    start, end = args.workday.split("-")
    print(json.dumps(audit(events, (start, end), args.deep), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
