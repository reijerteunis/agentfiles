#!/usr/bin/env python3
"""Go-to-market metrics from CSV exports, computed by script so they can't be wishful. Standard library only.

Usage:
  python3 gtm_metrics.py funnel funnel.csv                    columns step, count (optional: channel)
  python3 gtm_metrics.py deals deals.csv [--from 2026-07] [--to 2026-09]
  python3 gtm_metrics.py cac spend.csv deals.csv --margin 0.8 [--from …] [--to …] [--amount annual|monthly]
  python3 gtm_metrics.py retention mrr.csv --from 2025-10 --to 2026-09
  python3 gtm_metrics.py --self-test

deals.csv: id, created (YYYY-MM-DD), closed (YYYY-MM-DD, empty while open), stage (won, lost, anything else is open),
amount (first-year value, or monthly revenue with --amount monthly), source. Deal sources and spend channels must use
the same names. spend.csv: month (YYYY-MM), channel, amount. mrr.csv: month (YYYY-MM), customer, mrr.
--from and --to are inclusive months. Small samples are flagged, never hidden.
"""

from __future__ import annotations

import argparse
import csv
import io
import statistics
import sys
from datetime import date

SMALL = 30


def num(value: str) -> float:
    return float(str(value).replace(",", "").strip() or 0)


def read(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def in_period(day: str, start: str | None, end: str | None) -> bool:
    month = day[:7]
    return bool(day) and (not start or month >= start) and (not end or month <= end)


def period(start: str | None, end: str | None) -> str:
    return f"{start or 'the start'} to {end or 'now'}"


def funnel(rows: list[dict]) -> str:
    steps: list[str] = []
    counts: dict[str, dict[str, float]] = {}
    for r in rows:
        step, channel = r["step"].strip(), (r.get("channel") or "").strip() or "all"
        if step not in steps:
            steps.append(step)
        counts.setdefault(channel, {})[step] = counts.get(channel, {}).get(step, 0) + num(r["count"])
    out = []
    for channel, by_step in counts.items():
        out += [f"## Funnel{'' if channel == 'all' else ': ' + channel}", "",
                "| Step | Count | From previous step | From first step |", "|---|---|---|---|"]
        first, prev = by_step.get(steps[0], 0), None
        for step in steps:
            c = by_step.get(step, 0)
            from_prev = f"{c / prev:.1%}" if prev else "-"
            from_first = f"{c / first:.2%}" if first and step != steps[0] else "-"
            out.append(f"| {step} | {c:,.0f}{' ⚠️ small sample' if c < SMALL else ''} | {from_prev} | {from_first} |")
            prev = c
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def closed_deals(rows: list[dict], start: str | None, end: str | None) -> tuple[list[dict], list[dict], int]:
    won, lost, undated = [], [], 0
    for r in rows:
        stage = r.get("stage", "").strip().lower()
        if stage not in ("won", "lost"):
            continue
        day = (r.get("closed") or "").strip()
        if not day:
            undated += 1
        elif in_period(day, start, end):
            (won if stage == "won" else lost).append(r)
    return won, lost, undated


def deals(rows: list[dict], start: str | None, end: str | None) -> str:
    won, lost, undated = closed_deals(rows, start, end)
    out = [f"## Deals closed from {period(start, end)}", ""]
    if not (won or lost):
        return "\n".join(out + ["No closed deals in this period."]) + "\n"
    cycles = [(date.fromisoformat(r["closed"].strip()) - date.fromisoformat(r["created"].strip())).days
              for r in won if r.get("created", "").strip()]
    out += [f"Won {len(won)}, lost {len(lost)}, win rate {len(won) / (len(won) + len(lost)):.0%}.",
            f"Average won deal: {statistics.mean(num(r['amount']) for r in won):,.0f}." if won else "No won deals.",
            f"Median sales cycle (won): {statistics.median(cycles):.0f} days." if cycles else ""]
    if len(won) + len(lost) < SMALL:
        out.append(f"⚠️ Small sample: {len(won) + len(lost)} closed deals, so treat the rates as rough.")
    if undated:
        out.append(f"{undated} won or lost deal(s) have no closed date and were left out.")
    out += ["", "| Source | Won | Lost | Win rate | Won value |", "|---|---|---|---|---|"]
    for source in sorted({r.get("source", "").strip() or "unknown" for r in won + lost}):
        w = [r for r in won if (r.get("source", "").strip() or "unknown") == source]
        l_ = [r for r in lost if (r.get("source", "").strip() or "unknown") == source]
        out.append(f"| {source} | {len(w)} | {len(l_)} | {len(w) / (len(w) + len(l_)):.0%} | {sum(num(r['amount']) for r in w):,.0f} |")
    return "\n".join(out) + "\n"


def cac(spend_rows: list[dict], deal_rows: list[dict], margin: float, start: str | None, end: str | None,
        amount: str = "annual") -> str:
    spend: dict[str, float] = {}
    for r in spend_rows:
        if in_period(r["month"].strip() + "-01", start, end):
            spend[r["channel"].strip()] = spend.get(r["channel"].strip(), 0) + num(r["amount"])
    won, _, _ = closed_deals(deal_rows, start, end)
    by_source: dict[str, list[float]] = {}
    for r in won:
        by_source.setdefault(r.get("source", "").strip() or "unknown", []).append(num(r["amount"]))

    def row(name: str, cost: float, amounts: list[float]) -> str:
        customers = len(amounts)
        if not customers:
            return f"| {name} | {cost:,.0f} | 0 | no customers | - | - |"
        avg = sum(amounts) / customers
        monthly = avg / 12 if amount == "annual" else avg
        if not cost:
            return f"| {name} | 0 | {customers} | no spend recorded | {avg:,.0f} | - |"
        per_customer = cost / customers
        return f"| {name} | {cost:,.0f} | {customers} | {per_customer:,.0f} | {avg:,.0f} | {per_customer / (monthly * margin):.1f} |"

    value_label = "Avg first-year value" if amount == "annual" else "Avg monthly revenue"
    out = [f"## CAC and payback from {period(start, end)} (gross margin {margin:.0%})", "",
           f"| Channel | Spend | New customers | CAC | {value_label} | Payback (months) |", "|---|---|---|---|---|---|"]
    out += [row(ch, spend.get(ch, 0), by_source.get(ch, [])) for ch in sorted(set(spend) | set(by_source))]
    out.append(row("**blended**", sum(spend.values()), [a for v in by_source.values() for a in v]))
    if len(won) < SMALL:
        out += ["", f"⚠️ Small sample: {len(won)} new customers. Channel CAC moves a lot with one deal."]
    return "\n".join(out) + "\n"


def retention(rows: list[dict], start: str, end: str) -> str:
    mrr: dict[tuple[str, str], float] = {}
    for r in rows:
        key = (r["month"].strip()[:7], r["customer"].strip())
        mrr[key] = mrr.get(key, 0) + num(r["mrr"])
    base = {c: v for (m, c), v in mrr.items() if m == start and v > 0}
    if not base:
        raise ValueError(f"no customers with MRR in {start}")
    later = {c: mrr.get((end, c), 0.0) for c in base}
    total = sum(base.values())
    churned = sorted(c for c, v in later.items() if v == 0)
    new = {c: v for (m, c), v in mrr.items() if m == end and v > 0 and c not in base}
    out = [f"## Revenue retention from {start} to {end}", "",
           f"Customers in {start}: {len(base)}, MRR {total:,.0f}.",
           f"Net revenue retention: {sum(later.values()) / total:.1%} (expansion minus contraction and churn).",
           f"Gross revenue retention: {sum(min(later[c], v) for c, v in base.items()) / total:.1%} (churn and contraction only).",
           f"Logo churn: {len(churned) / len(base):.1%} ({len(churned)} of {len(base)}).",
           f"New customers by {end}: {len(new)}, MRR {sum(new.values()):,.0f}."]
    if churned and len(churned) <= 10:
        out.append("Churned: " + ", ".join(churned) + ". Record why for each.")
    if len(base) < SMALL:
        out.append(f"⚠️ Small sample: {len(base)} customers. List the reasons per customer rather than trusting the percentages.")
    return "\n".join(out) + "\n"


def self_test() -> int:
    def rows(text: str) -> list[dict]:
        return list(csv.DictReader(io.StringIO(text)))

    deal_csv = rows("id,created,closed,stage,amount,source\n1,2026-07-01,2026-08-10,won,12000,outbound\n"
                    "2,2026-07-15,2026-09-01,lost,8000,outbound\n3,2026-08-01,2026-09-20,won,6000,referral\n"
                    "4,2026-09-01,,open,5000,inbound\n5,2026-06-01,2026-06-30,won,4000,inbound\n")
    f = funnel(rows("step,count\nvisitors,1200\nsign-ups,48\nactivated,9\npaid,2\n"))
    d = deals(deal_csv, "2026-07", "2026-09")
    c = cac(rows("month,channel,amount\n2026-07,outbound,1000\n2026-08,outbound,1000\n2026-09,outbound,1000\n"
                 "2026-08,content,600\n2026-06,outbound,5000\n"), deal_csv, 0.8, "2026-07", "2026-09")
    r = retention(rows("month,customer,mrr\n2025-10,A,100\n2025-10,B,200\n2025-10,C,100\n"
                       "2026-09,A,150\n2026-09,B,150\n2026-09,D,300\n"), "2025-10", "2026-09")
    checks = {
        "funnel": all(s in f for s in ("| sign-ups | 48 | 4.0% | 4.00% |", "| activated | 9 ⚠️ small sample | 18.8% | 0.75% |",
                                       "| paid | 2 ⚠️ small sample | 22.2% | 0.17% |")),
        "deals": all(s in d for s in ("Won 2, lost 1, win rate 67%.", "Average won deal: 9,000.",
                                      "Median sales cycle (won): 45 days.", "| outbound | 1 | 1 | 50% | 12,000 |",
                                      "| referral | 1 | 0 | 100% | 6,000 |")),
        "cac": all(s in c for s in ("| outbound | 3,000 | 1 | 3,000 | 12,000 | 3.8 |",
                                    "| referral | 0 | 1 | no spend recorded | 6,000 | - |",
                                    "| content | 600 | 0 | no customers | - | - |",
                                    "| **blended** | 3,600 | 2 | 1,800 | 9,000 | 3.0 |")),
        "retention": all(s in r for s in ("Net revenue retention: 75.0%", "Gross revenue retention: 62.5%",
                                          "Logo churn: 33.3% (1 of 3)", "New customers by 2026-09: 1, MRR 300", "Churned: C.")),
    }
    ok = all(checks.values())
    print("gtm_metrics self-test:", "ok" if ok else f"FAILED {checks}\n{f}\n{d}\n{c}\n{r}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Go-to-market metrics from CSV exports.")
    ap.add_argument("command", nargs="?", choices=["funnel", "deals", "cac", "retention"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--from", dest="start", help="first month, YYYY-MM")
    ap.add_argument("--to", dest="end", help="last month, YYYY-MM")
    ap.add_argument("--margin", type=float, help="gross margin as 0-1 (cac)")
    ap.add_argument("--amount", choices=["annual", "monthly"], default="annual", help="what a deal's amount means (cac)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    needed = {"funnel": 1, "deals": 1, "cac": 2, "retention": 1}
    if not args.command or len(args.files) != needed[args.command]:
        ap.error("see the usage at the top of this script")
    try:
        if args.command == "funnel":
            print(funnel(read(args.files[0])))
        elif args.command == "deals":
            print(deals(read(args.files[0]), args.start, args.end))
        elif args.command == "cac":
            if args.margin is None or not 0 < args.margin <= 1:
                ap.error("cac needs --margin between 0 and 1")
            print(cac(read(args.files[0]), read(args.files[1]), args.margin, args.start, args.end, args.amount))
        else:
            if not (args.start and args.end):
                ap.error("retention needs --from and --to")
            print(retention(read(args.files[0]), args.start, args.end))
    except (KeyError, ValueError) as e:
        print(f"error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
