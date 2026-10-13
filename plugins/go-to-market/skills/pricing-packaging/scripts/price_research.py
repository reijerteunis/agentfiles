#!/usr/bin/env python3
"""Analyse price research surveys with Van Westendorp and Gabor-Granger. Standard library only.

Usage:
  python3 price_research.py vw survey.csv    columns too_cheap, cheap, expensive, too_expensive (one row per respondent)
  python3 price_research.py gg answers.csv   columns price, buy (1 or 0, one row per respondent and price)
                                             or price, share (0-1, already aggregated)
  python3 price_research.py --self-test

Van Westendorp curves at price p: too cheap = share answering too_cheap >= p · cheap = share answering cheap >= p ·
expensive = share answering expensive <= p · too expensive = share answering too_expensive <= p.
Intersections, interpolated linearly between observed prices:
  lower bound of the acceptable range (PMC) = too cheap × not cheap (1 − cheap)
  optimal price point (OPP)                 = too cheap × too expensive
  indifference price point (IPP)            = cheap × expensive
  upper bound of the acceptable range (PME) = too expensive × not expensive (1 − expensive)
Some practitioners take the bounds from "expensive" and "cheap" instead; say which convention you report.
Respondents whose answers aren't in order (too cheap ≤ cheap ≤ expensive ≤ too expensive) are dropped and counted.
Numbers may carry a currency sign; a comma is read as a decimal separator.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys

VW_COLUMNS = ["too_cheap", "cheap", "expensive", "too_expensive"]


def num(value: str) -> float:
    return float(str(value).strip().lstrip("€$£").replace(",", ".").strip())


def crossing(xs: list[float], f: list[float], g: list[float]) -> float | None:
    """First price where f and g meet. A run of equal values gives its midpoint."""
    d = [a - b for a, b in zip(f, g)]
    for i, di in enumerate(d):
        if abs(di) < 1e-12:
            j = i
            while j + 1 < len(d) and abs(d[j + 1]) < 1e-12:
                j += 1
            return (xs[i] + xs[j]) / 2
        if i + 1 < len(d) and di * d[i + 1] < 0:
            return xs[i] + (xs[i + 1] - xs[i]) * di / (di - d[i + 1])
    return None


def van_westendorp(rows: list[dict]) -> tuple[int, int, dict[str, float | None]]:
    answers, dropped = [], 0
    for row in rows:
        try:
            a = [num(row[c]) for c in VW_COLUMNS]
        except (KeyError, ValueError):
            dropped += 1
            continue
        if a == sorted(a):
            answers.append(a)
        else:
            dropped += 1
    if len(answers) < 2:
        raise ValueError(f"need at least 2 consistent respondents with columns {VW_COLUMNS}")
    n, grid = len(answers), sorted({x for a in answers for x in a})
    too_cheap = [sum(a[0] >= p for a in answers) / n for p in grid]
    cheap = [sum(a[1] >= p for a in answers) / n for p in grid]
    expensive = [sum(a[2] <= p for a in answers) / n for p in grid]
    too_expensive = [sum(a[3] <= p for a in answers) / n for p in grid]
    points = {
        "lower bound (PMC)": crossing(grid, too_cheap, [1 - v for v in cheap]),
        "optimal price point (OPP)": crossing(grid, too_cheap, too_expensive),
        "indifference price point (IPP)": crossing(grid, cheap, expensive),
        "upper bound (PME)": crossing(grid, too_expensive, [1 - v for v in expensive]),
    }
    return n, dropped, points


def gabor_granger(rows: list[dict]) -> list[tuple[float, float, int | None, float]]:
    """(price, share willing to buy, respondents or None, revenue index), sorted by price."""
    if rows and "share" in rows[0]:
        table = [(num(r["price"]), num(r["share"]), None) for r in rows]
        table = [(p, s / 100 if s > 1 else s, n) for p, s, n in table]
    else:
        tally: dict[float, list[int]] = {}
        for r in rows:
            tally.setdefault(num(r["price"]), []).append(1 if str(r["buy"]).strip().lower() in ("1", "yes", "true", "y") else 0)
        table = [(p, sum(v) / len(v), len(v)) for p, v in tally.items()]
    return sorted((p, s, n, p * s) for p, s, n in table)


def report_vw(rows: list[dict]) -> str:
    n, dropped, points = van_westendorp(rows)
    lines = [f"Respondents: {n} used, {dropped} dropped (answers missing or out of order)."]
    if n < 30:
        lines.append("Small sample: fewer than 30 respondents, so treat the points as a rough range.")
    lines += [f"{name}: {value:.2f}" if value is not None else f"{name}: no crossing (sample too small or inconsistent)"
              for name, value in points.items()]
    lo, hi = points["lower bound (PMC)"], points["upper bound (PME)"]
    if lo is not None and hi is not None:
        lines.append(f"Acceptable range: {lo:.2f} to {hi:.2f}")
    return "\n".join(lines)


def report_gg(rows: list[dict]) -> str:
    table = gabor_granger(rows)
    best = max(table, key=lambda t: t[3])
    lines = ["| Price | Would buy | Respondents | Revenue index |", "|---|---|---|---|"]
    lines += [f"| {p:g} | {s:.0%} | {n if n is not None else '-'} | {r:.2f}{' ← highest' if (p, s, n, r) == best else ''} |"
              for p, s, n, r in table]
    lines.append(f"\nRevenue-maximising price among those tested: {best[0]:g}. Stated intent overestimates real buying; "
                 "confirm with a paid pilot or a live test.")
    return "\n".join(lines)


def self_test() -> int:
    # 100 respondents with too cheap = a, cheap = a+10, expensive = a+20, too expensive = a+30, a = 0..99.
    # Worked by hand: PMC 55, OPP 64.5, IPP 64.5, PME 74.
    rows = [dict(zip(VW_COLUMNS, map(str, (a, a + 10, a + 20, a + 30)))) for a in range(100)]
    rows.append(dict(zip(VW_COLUMNS, ("50", "40", "60", "70"))))  # out of order: dropped
    n, dropped, points = van_westendorp(rows)
    expected = {"lower bound (PMC)": 55, "optimal price point (OPP)": 64.5,
                "indifference price point (IPP)": 64.5, "upper bound (PME)": 74}
    vw_ok = n == 100 and dropped == 1 and all(points[k] is not None and abs(points[k] - v) < 1e-9 for k, v in expected.items())
    answers = "price,buy\n" + "".join(f"{p},{int(i < k)}\n" for p, k in ((10, 8), (20, 6), (30, 3)) for i in range(10))
    table = gabor_granger(list(csv.DictReader(io.StringIO(answers))))
    shares = gabor_granger(list(csv.DictReader(io.StringIO("price,share\n10,80\n20,0.6\n"))))
    gg_ok = ([(p, s, r) for p, s, _, r in table] == [(10, 0.8, 8.0), (20, 0.6, 12.0), (30, 0.3, 9.0)]
             and max(table, key=lambda t: t[3])[0] == 20 and [s for _, s, _, _ in shares] == [0.8, 0.6]
             and num("€12,50") == 12.5)
    ok = vw_ok and gg_ok
    print("price_research self-test:", "ok" if ok else f"FAILED vw={vw_ok} {n} {dropped} {points} gg={gg_ok} {table}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyse Van Westendorp or Gabor-Granger price surveys.")
    ap.add_argument("method", nargs="?", choices=["vw", "gg"])
    ap.add_argument("csv", nargs="?")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.method and args.csv):
        ap.error("give the method (vw or gg) and the CSV")
    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    try:
        print(report_vw(rows) if args.method == "vw" else report_gg(rows))
    except (KeyError, ValueError) as e:
        print(f"error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
