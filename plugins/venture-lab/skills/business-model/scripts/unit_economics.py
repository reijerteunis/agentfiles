#!/usr/bin/env python3
"""Unit economics for a subscription or repeat-purchase business. Standard library only.

  python3 unit_economics.py --price 49 --margin 0.8 --churn 0.03 --cac 300 [--currency EUR]
  python3 unit_economics.py --self-test

price  = revenue per customer per month · margin = gross margin (0-1) · churn = monthly churn (0-1)
cac    = cost to acquire one customer
Outputs: lifetime (months) = 1 / churn · LTV = price × margin / churn · LTV:CAC · CAC payback (months)
= cac / (price × margin). Rules of thumb shown for orientation only: LTV:CAC ≥ 3, payback ≤ 12 months.
"""

from __future__ import annotations

import argparse
import sys


def compute(price: float, margin: float, churn: float, cac: float) -> dict:
    if not (0 < churn <= 1 and 0 < margin <= 1 and price > 0):
        raise ValueError("need price > 0, 0 < margin ≤ 1 and 0 < churn ≤ 1")
    monthly_gross = price * margin
    ltv = monthly_gross / churn
    return {"lifetime_months": round(1 / churn, 1), "monthly_gross_profit": round(monthly_gross, 2),
            "ltv": round(ltv, 2), "ltv_to_cac": round(ltv / cac, 2) if cac else None,
            "payback_months": round(cac / monthly_gross, 2) if cac else 0.0}


def report(r: dict, cur: str) -> str:
    verdict = []
    if r["ltv_to_cac"] is not None:
        verdict.append("LTV:CAC healthy (≥ 3)" if r["ltv_to_cac"] >= 3 else "LTV:CAC below 3: acquisition is too expensive or churn too high")
    verdict.append("payback within 12 months" if r["payback_months"] <= 12 else "payback longer than 12 months: cash-hungry")
    return (f"| Metric | Value |\n|---|---|\n"
            f"| Customer lifetime | {r['lifetime_months']} months |\n"
            f"| Gross profit per customer per month | {cur} {r['monthly_gross_profit']:,} |\n"
            f"| LTV | {cur} {r['ltv']:,} |\n"
            f"| LTV:CAC | {r['ltv_to_cac']} |\n"
            f"| CAC payback | {r['payback_months']} months |\n\n"
            + " · ".join(verdict) + " (rules of thumb, not laws)")


def self_test() -> int:
    r = compute(49, 0.8, 0.03, 300)
    checks = [r["ltv"] == 1306.67, r["payback_months"] == 7.65, r["ltv_to_cac"] == 4.36, r["lifetime_months"] == 33.3]
    try:
        compute(49, 0.8, 0, 300)
        checks.append(False)
    except ValueError:
        checks.append(True)
    print("unit_economics self-test:", "ok" if all(checks) else f"FAILED {checks} {r}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Unit economics: LTV, LTV:CAC and payback.")
    ap.add_argument("--price", type=float, help="revenue per customer per month")
    ap.add_argument("--margin", type=float, help="gross margin, 0-1")
    ap.add_argument("--churn", type=float, help="monthly churn, 0-1")
    ap.add_argument("--cac", type=float, default=0.0, help="customer acquisition cost")
    ap.add_argument("--currency", default="EUR")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if None in (args.price, args.margin, args.churn):
        ap.error("--price, --margin and --churn are required")
    print(report(compute(args.price, args.margin, args.churn, args.cac), args.currency))
    return 0


if __name__ == "__main__":
    sys.exit(main())
