#!/usr/bin/env python3
"""Score a list of accounts against an ICP rubric, so two people would tier the same account the same way.
Standard library only.

Usage:
  python3 score_accounts.py accounts.csv icp.json [--out scored.csv]
  python3 score_accounts.py --self-test

icp.json:
  {"tiers": {"A": 70, "B": 40},
   "criteria":   [{"field": "employees", "op": "between", "value": [50, 500], "points": 30, "why": "can pay, moves fast"}],
   "disqualify": [{"field": "employees", "op": "lt", "value": 10, "why": "can't pay the minimum plan"}]}

Operators: eq, ne, in, not_in, lt, lte, gt, gte, between (inclusive), contains, nonempty, empty. Comparisons are
numeric when both sides are numbers, otherwise case-insensitive text. Empty cells only match `empty`.
Every account gets a score, a tier (A, B, C, or X when a disqualifier matches) and the reasons.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys

OPS = {"eq", "ne", "in", "not_in", "lt", "lte", "gt", "gte", "between", "contains", "nonempty", "empty"}


def num(value) -> float | None:
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return None


def matches(cell: str, op: str, value) -> bool:
    cell = (cell or "").strip()
    if op == "empty":
        return not cell
    if op == "nonempty":
        return bool(cell)
    if not cell:
        return False
    if op in ("lt", "lte", "gt", "gte", "between"):
        c = num(cell)
        if c is None:
            return False
        if op == "between":
            return num(value[0]) <= c <= num(value[1])
        v = num(value)
        return {"lt": c < v, "lte": c <= v, "gt": c > v, "gte": c >= v}[op]
    low = cell.lower()
    if op == "contains":
        return str(value).lower() in low
    if op in ("in", "not_in"):
        hit = low in {str(v).lower() for v in value}
        return hit if op == "in" else not hit
    c, v = num(cell), num(value)
    same = c == v if (c is not None and v is not None) else low == str(value).lower()
    return same if op == "eq" else not same


def check_rubric(rubric: dict, header: list[str]) -> list[str]:
    problems = []
    tiers = rubric.get("tiers", {})
    if not (isinstance(tiers.get("A"), (int, float)) and isinstance(tiers.get("B"), (int, float)) and tiers["A"] > tiers["B"]):
        problems.append('tiers needs numbers with A > B, for example {"A": 70, "B": 40}')
    if not rubric.get("criteria"):
        problems.append("criteria is empty")
    for kind in ("criteria", "disqualify"):
        for i, c in enumerate(rubric.get(kind, [])):
            where, op = f"{kind}[{i}]", c.get("op")
            if op not in OPS:
                problems.append(f"{where}: op '{op}' not in {sorted(OPS)}")
            if c.get("field") not in header:
                problems.append(f"{where}: field '{c.get('field')}' is not a column in the CSV")
            if kind == "criteria" and not isinstance(c.get("points"), (int, float)):
                problems.append(f"{where}: points must be a number")
            if op == "between" and not (isinstance(c.get("value"), list) and len(c["value"]) == 2):
                problems.append(f"{where}: between needs a [low, high] value")
            if op in ("in", "not_in") and not isinstance(c.get("value"), list):
                problems.append(f"{where}: {op} needs a list value")
    return problems


def score(row: dict, rubric: dict) -> tuple[float, str, list[str]]:
    for d in rubric.get("disqualify", []):
        if matches(row.get(d["field"], ""), d["op"], d.get("value")):
            return 0, "X", [f"disqualified: {d.get('why') or d['field'] + ' ' + d['op']}"]
    total, reasons = 0.0, []
    for c in rubric["criteria"]:
        if matches(row.get(c["field"], ""), c["op"], c.get("value")):
            total += c["points"]
            reasons.append(f"+{c['points']:g} {c.get('why') or c['field']}")
    tiers = rubric["tiers"]
    return total, "A" if total >= tiers["A"] else "B" if total >= tiers["B"] else "C", reasons


def run(csv_text: str, rubric: dict) -> tuple[list[dict], list[str]]:
    reader = csv.DictReader(io.StringIO(csv_text))
    header = reader.fieldnames or []
    problems = check_rubric(rubric, header)
    if problems:
        return [], problems
    scored = []
    for row in reader:
        total, tier, reasons = score(row, rubric)
        scored.append({**row, "score": f"{total:g}", "tier": tier, "reasons": "; ".join(reasons)})
    scored.sort(key=lambda r: ("ABCX".index(r["tier"]), -float(r["score"])))
    return scored, []


def self_test() -> int:
    rubric = {"tiers": {"A": 70, "B": 40},
              "criteria": [{"field": "employees", "op": "between", "value": [50, 500], "points": 30},
                           {"field": "country", "op": "in", "value": ["NL", "BE", "DE"], "points": 20},
                           {"field": "uses_shopify", "op": "eq", "value": "yes", "points": 30},
                           {"field": "trigger", "op": "nonempty", "points": 20, "why": "a reason to buy now"}],
              "disqualify": [{"field": "employees", "op": "lt", "value": 10, "why": "too small to pay"}]}
    accounts = ("company,employees,country,uses_shopify,trigger\n"
                "Brightcart,120,NL,yes,raised seed\n"
                "Pixelwerk,60,FR,Yes,\n"
                "Tiny,5,NL,yes,new CEO\n"
                'Acme,"2,000",nl,no,\n')
    scored, problems = run(accounts, rubric)
    by_name = {r["company"]: r for r in scored}
    _, bad = run(accounts, {**rubric, "criteria": rubric["criteria"] + [{"field": "revenue", "op": "gt", "value": 1, "points": 5}]})
    checks = [not problems,
              (by_name["Brightcart"]["score"], by_name["Brightcart"]["tier"]) == ("100", "A"),
              (by_name["Pixelwerk"]["score"], by_name["Pixelwerk"]["tier"]) == ("60", "B"),
              by_name["Tiny"]["tier"] == "X" and "too small to pay" in by_name["Tiny"]["reasons"],
              (by_name["Acme"]["score"], by_name["Acme"]["tier"]) == ("20", "C"),
              [r["company"] for r in scored] == ["Brightcart", "Pixelwerk", "Acme", "Tiny"],
              "+20 a reason to buy now" in by_name["Brightcart"]["reasons"],
              any("'revenue' is not a column" in p for p in bad)]
    print("score_accounts self-test:", "ok" if all(checks) else f"FAILED {checks}\n{scored}\n{problems}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Score accounts against an ICP rubric.")
    ap.add_argument("accounts", nargs="?")
    ap.add_argument("rubric", nargs="?")
    ap.add_argument("--out", help="write the scored accounts to this CSV")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.accounts and args.rubric):
        ap.error("give the accounts CSV and the rubric JSON")
    with open(args.accounts, encoding="utf-8-sig") as f, open(args.rubric, encoding="utf-8") as g:
        scored, problems = run(f.read(), json.load(g))
    for p in problems:
        print(f"error: {p}")
    if problems:
        return 1
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(scored[0].keys()) if scored else ["score", "tier", "reasons"])
            writer.writeheader()
            writer.writerows(scored)
        print(f"wrote {args.out}")
    counts = {t: sum(1 for r in scored if r["tier"] == t) for t in "ABCX"}
    print(f"{len(scored)} accounts: A {counts['A']}, B {counts['B']}, C {counts['C']}, disqualified {counts['X']}")
    for r in scored[:10]:
        print(f"  {r['tier']} {r['score']:>5}  {next(iter(r.values()))}  ({r['reasons']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
