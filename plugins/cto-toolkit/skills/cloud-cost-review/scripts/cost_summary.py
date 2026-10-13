#!/usr/bin/env python3
"""Summarise a cloud billing export: cost per service per month and the biggest movers. Stdlib only.

Works with any CSV that has a date, a service and a cost column (AWS Cost Explorer or CUR, GCP billing
export, Azure cost analysis). Point it at the right columns:
  python3 cost_summary.py bill.csv --date-col "UsageStartDate" --service-col "ProductName" --cost-col "UnblendedCost"
  python3 cost_summary.py --self-test

Prints the monthly totals, cost per service for the last two months with the change, and the top movers.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import defaultdict


def parse_amount(raw: str) -> float:
    raw = (raw or "").strip().replace("$", "").replace("€", "").replace(" ", "")
    if raw.count(",") and raw.count("."):
        raw = raw.replace(",", "")          # 1,234.56
    elif raw.count(",") == 1:
        raw = raw.replace(",", ".")         # 1234,56
    try:
        return float(raw)
    except ValueError:
        return 0.0


def summarise(rows: list[dict], date_col: str, service_col: str, cost_col: str) -> dict:
    by_month: dict[str, float] = defaultdict(float)
    by_service: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in rows:
        month = (row.get(date_col) or "")[:7]
        if len(month) != 7:
            continue
        cost = parse_amount(row.get(cost_col, ""))
        by_month[month] += cost
        by_service[row.get(service_col) or "(unknown)"][month] += cost
    months = sorted(by_month)
    last, prev = (months[-1], months[-2]) if len(months) >= 2 else (months[-1] if months else None, None)
    services = []
    for svc, per in by_service.items():
        now_c, before = per.get(last, 0.0), per.get(prev, 0.0) if prev else 0.0
        services.append({"service": svc, "last": round(now_c, 2), "previous": round(before, 2),
                         "change": round(now_c - before, 2),
                         "change_pct": round(100 * (now_c - before) / before, 1) if before else None})
    services.sort(key=lambda s: s["last"], reverse=True)
    movers = sorted(services, key=lambda s: abs(s["change"]), reverse=True)[:5]
    return {"months": {m: round(by_month[m], 2) for m in months}, "last": last, "previous": prev,
            "services": services, "movers": movers}


def report(s: dict) -> str:
    lines = ["## Monthly total", "| Month | Cost |", "|---|---|"]
    lines += [f"| {m} | {c:,.2f} |" for m, c in s["months"].items()]
    lines += ["", f"## By service ({s['previous']} → {s['last']})", "| Service | Previous | Last | Change | % |",
              "|---|---|---|---|---|"]
    for v in s["services"][:15]:
        pct = "-" if v["change_pct"] is None else f"{v['change_pct']}%"
        lines.append(f"| {v['service']} | {v['previous']:,.2f} | {v['last']:,.2f} | {v['change']:+,.2f} | {pct} |")
    lines += ["", "## Top movers"] + [f"- {v['service']}: {v['change']:+,.2f}" for v in s["movers"]]
    return "\n".join(lines)


def self_test() -> int:
    data = io.StringIO("date,service,cost\n2026-08-03,EC2,100\n2026-08-20,S3,10\n"
                       "2026-09-02,EC2,160\n2026-09-15,S3,\"9,50\"\n2026-09-20,NAT Gateway,40\n")
    s = summarise(list(csv.DictReader(data)), "date", "service", "cost")
    ec2 = next(v for v in s["services"] if v["service"] == "EC2")
    checks = [s["months"] == {"2026-08": 110.0, "2026-09": 209.5}, s["last"] == "2026-09",
              ec2["change"] == 60.0 and ec2["change_pct"] == 60.0,
              s["movers"][0]["service"] == "EC2", parse_amount("1,234.50") == 1234.5]
    print("cost_summary self-test:", "ok" if all(checks) else f"FAILED {checks}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Summarise a cloud billing CSV.")
    ap.add_argument("csv", nargs="?")
    ap.add_argument("--date-col", default="date")
    ap.add_argument("--service-col", default="service")
    ap.add_argument("--cost-col", default="cost")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.csv:
        ap.error("give the billing CSV")
    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    missing = [c for c in (args.date_col, args.service_col, args.cost_col) if rows and c not in rows[0]]
    if missing:
        print(f"columns not found: {missing}; available: {list(rows[0])}", file=sys.stderr)
        return 1
    print(report(summarise(rows, args.date_col, args.service_col, args.cost_col)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
