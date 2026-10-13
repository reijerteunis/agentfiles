#!/usr/bin/env python3
"""Bottom-up market sizing: TAM, SAM and SOM from customer counts and prices. Standard library only.

Input: a JSON file describing segments, with every number sourced or labelled as an assumption:
  {"currency": "EUR",
   "segments": [{"name": "Accounting firms 2-10 staff, NL", "customers": 9000,
                 "price_per_year": 600, "serviceable_share": 0.6, "obtainable_share": 0.03,
                 "source": "CBS 2025 + own assumption on shares"}]}
  customers × price_per_year              = TAM (everyone in the segment pays the full price)
  TAM × serviceable_share                 = SAM (the part you can reach with this product and these channels)
  SAM × obtainable_share                  = SOM (what you could realistically win in 3–5 years)
Usage:
  python3 sizing.py market.json
  python3 sizing.py --self-test
"""

from __future__ import annotations

import argparse
import json
import sys


def size(spec: dict) -> dict:
    rows = []
    for s in spec["segments"]:
        tam = s["customers"] * s["price_per_year"]
        sam = tam * s.get("serviceable_share", 1.0)
        som = sam * s.get("obtainable_share", 0.0)
        rows.append({"segment": s["name"], "customers": s["customers"], "price_per_year": s["price_per_year"],
                     "tam": round(tam), "sam": round(sam), "som": round(som),
                     "som_customers": round(s["customers"] * s.get("serviceable_share", 1.0) * s.get("obtainable_share", 0.0)),
                     "source": s.get("source", "UNSOURCED")})
    total = {k: sum(r[k] for r in rows) for k in ("tam", "sam", "som", "som_customers")}
    return {"currency": spec.get("currency", ""), "segments": rows, "total": total}


def report(r: dict) -> str:
    c = r["currency"]
    lines = ["| Segment | Customers | Price/yr | TAM | SAM | SOM | SOM customers | Source |", "|---|---|---|---|---|---|---|---|"]
    for s in r["segments"]:
        lines.append(f"| {s['segment']} | {s['customers']:,} | {c} {s['price_per_year']:,} | {c} {s['tam']:,} | "
                     f"{c} {s['sam']:,} | {c} {s['som']:,} | {s['som_customers']:,} | {s['source']} |")
    t = r["total"]
    lines.append(f"| **Total** | | | **{c} {t['tam']:,}** | **{c} {t['sam']:,}** | **{c} {t['som']:,}** | **{t['som_customers']:,}** | |")
    unsourced = [s["segment"] for s in r["segments"] if s["source"] == "UNSOURCED"]
    if unsourced:
        lines.append(f"\n⚠️ Unsourced segments: {', '.join(unsourced)}. Every number needs a source or an 'assumption' label.")
    return "\n".join(lines)


def self_test() -> int:
    r = size({"currency": "EUR", "segments": [
        {"name": "A", "customers": 9000, "price_per_year": 600, "serviceable_share": 0.6, "obtainable_share": 0.03, "source": "x"},
        {"name": "B", "customers": 1000, "price_per_year": 1200}]})
    a, b = r["segments"]
    checks = [a["tam"] == 5_400_000, a["sam"] == 3_240_000, a["som"] == 97_200, a["som_customers"] == 162,
              b["sam"] == 1_200_000 and b["som"] == 0, r["total"]["tam"] == 6_600_000,
              "Unsourced segments: B" in report(r)]
    print("sizing self-test:", "ok" if all(checks) else f"FAILED {checks} {r}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Bottom-up TAM/SAM/SOM.")
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.spec:
        ap.error("give the market JSON file")
    with open(args.spec, encoding="utf-8") as f:
        print(report(size(json.load(f))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
