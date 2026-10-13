#!/usr/bin/env python3
"""Check customer-facing copy against a proof bank: no claim without a source. Standard library only.

Usage:
  python3 proof_check.py draft.md proof.md            list unsupported claims, exit 1 if there are any
  python3 proof_check.py draft.md proof.md --strip    if the check passes, print the copy without proof IDs
  python3 proof_check.py --self-test

The proof bank has one entry per line:  - [p-1] <claim> (<source>, YYYY-MM, permission: public)
Permissions: public, anonymous, named, logo, quote (combine them: "permission: named, quote"). Mark retired entries
"(expired)". In a draft, cite entries in the same sentence as the claim: "Checkout drop-off fell to 22% [p-1]."

Rules:
  1. A sentence with a number or a superlative ("best", "fastest", "the only", "#1", "guaranteed", "compliant", …)
     cites at least one proof ID. Years on their own, list numbering, URLs and code don't count. A line that holds
     no claim despite a number (an address, a step count) can be marked <!-- no-claim -->.
  2. Every cited ID exists in the bank, isn't marked expired, and isn't older than --max-age months.
  3. Every bank entry has a date and a known permission.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date

ENTRY_RE = re.compile(r"^\s*[-*]\s+\[(p-\d+)\]\s+(.*)$")
CITE_RE = re.compile(r"\s?\[(p-\d+(?:\s*,\s*p-\d+)*)\]")
DATE_RE = re.compile(r"\b(\d{4})-(\d{2})(?:-\d{2})?\b")
PERMISSION_RE = re.compile(r"permission:\s*([a-z][a-z ,+/]*)", re.I)
PERMISSIONS = {"public", "anonymous", "named", "logo", "quote"}
SUPERLATIVE_RE = re.compile(
    r"\b(best|fastest|cheapest|leading|unbeatable|unmatched|world-class|industry-leading|award-winning|"
    r"guaranteed?|proven|certified|compliant|number one)\b|#1\b|\bthe (only|first|largest|biggest)\b", re.I)
URL_RE = re.compile(r"https?://\S+|www\.\S+")
CODE_RE = re.compile(r"`[^`]*`")
COMMENT_RE = re.compile(r"<!--.*?-->")
YEAR_RE = re.compile(r"\b(?:19\d\d|20\d\d)\b")
LIST_NUM_RE = re.compile(r"^\s*(?:#+\s*)?\d+[.)]\s+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(“‘€$£#])")
NO_CLAIM = "no-claim"


def parse_bank(text: str) -> tuple[dict[str, dict], list[str]]:
    entries, problems = {}, []
    for n, line in enumerate(text.splitlines(), 1):
        m = ENTRY_RE.match(line)
        if not m:
            continue
        pid, rest = m.groups()
        dates = DATE_RE.findall(rest)
        perm = PERMISSION_RE.search(rest)
        perms = {p for p in re.split(r"[ ,+/]+", perm.group(1).lower()) if p} if perm else set()
        if not dates:
            problems.append(f"proof bank line {n}: {pid} has no date (YYYY-MM)")
        if not perms:
            problems.append(f"proof bank line {n}: {pid} has no permission")
        elif perms - PERMISSIONS:
            problems.append(f"proof bank line {n}: {pid} has an unknown permission {sorted(perms - PERMISSIONS)}")
        entries[pid] = {"date": tuple(map(int, dates[-1])) if dates else None, "expired": "(expired)" in rest.lower()}
    return entries, problems


def months_since(year_month: tuple[int, int], today: date) -> int:
    return (today.year - year_month[0]) * 12 + today.month - year_month[1]


def claim_text(sentence: str) -> str:
    for pattern in (COMMENT_RE, CODE_RE, URL_RE, CITE_RE, YEAR_RE):
        sentence = pattern.sub(" ", sentence)
    return sentence


def check(draft: str, bank: str, today: date, max_age: int = 18) -> tuple[int, list[str]]:
    entries, problems = parse_bank(bank)
    claims, in_code, in_front = 0, False, draft.startswith("---\n")
    for n, line in enumerate(draft.splitlines(), 1):
        if in_front:
            in_front = n == 1 or line.strip() != "---"
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.strip() or NO_CLAIM in line:
            continue
        for sentence in SENTENCE_RE.split(LIST_NUM_RE.sub("", line)):
            cited = [i.strip() for c in CITE_RE.findall(sentence) for i in c.split(",")]
            for pid in cited:
                entry = entries.get(pid)
                if entry is None:
                    problems.append(f"line {n}: cites {pid}, which isn't in the proof bank")
                elif entry["expired"]:
                    problems.append(f"line {n}: cites {pid}, which is marked expired")
                elif entry["date"] and months_since(entry["date"], today) > max_age:
                    problems.append(f"line {n}: cites {pid}, which is older than {max_age} months")
            text = claim_text(sentence)
            if re.search(r"\d", text) or SUPERLATIVE_RE.search(text):
                claims += 1
                if not cited:
                    problems.append(f"line {n}: claim without proof: {sentence.strip()[:90]}")
    return claims, problems


def strip(draft: str) -> str:
    return re.sub(r"[ \t]*<!--\s*no-claim\s*-->", "", CITE_RE.sub("", draft))


def self_test() -> int:
    bank = """# Proof bank
- [p-1] Checkout drop-off cut from 31% to 22% at Brightcart (case study, 2026-09, permission: named, quote)
- [p-2] 14 of 15 pilot users kept using it after the trial (product analytics, 2024-01, permission: anonymous)
- [p-3] SOC 2 Type II report issued (auditor report, 2026-06)
- [p-4] Rated best in class by a trade magazine (review, 2026-05, permission: public) (expired)
"""
    draft = """---
title: Home 2026
---
# Checkout in under a second
## 1. How it works
Brightcart cut checkout drop-off from 31% to 22% [p-1]. Founded in 2019, we work with Shopify stores.
Our pilot users stayed [p-2].
We are the fastest checkout on the market.
Trusted by 200 stores.
It works with every theme [p-9].
Award-winning support [p-4].
Read more at https://example.com/2024/report-42.
Keizersgracht 123, Amsterdam <!-- no-claim -->
```
const x = 42;
```
"""
    claims, problems = check(draft, bank, date(2026, 10, 13))
    expected = ["p-3 has no permission", "cites p-2, which is older than 18 months",
                "claim without proof: We are the fastest", "claim without proof: Trusted by 200",
                "cites p-9, which isn't", "cites p-4, which is marked expired"]
    missing = [e for e in expected if not any(e in p for p in problems)]
    noise = [p for p in problems if any(w in p for w in ("Founded", "How it works", "Read more", "Keizersgracht", "const", "Home"))]
    clean = strip("Fast [p-1]. Cheap [p-1, p-2]. Office 12 <!-- no-claim -->")
    ok = not missing and not noise and len(problems) == len(expected) and clean == "Fast. Cheap. Office 12"
    print("proof_check self-test:", "ok" if ok else f"FAILED\n missing: {missing}\n noise: {noise}\n all: {problems}\n strip: {clean!r}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Check copy against a proof bank.")
    ap.add_argument("draft", nargs="?")
    ap.add_argument("bank", nargs="?")
    ap.add_argument("--strip", action="store_true", help="print the copy without proof IDs if the check passes")
    ap.add_argument("--max-age", type=int, default=18, help="months before a proof point counts as stale (default 18)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.draft and args.bank):
        ap.error("give the draft and the proof bank")
    with open(args.draft, encoding="utf-8") as f, open(args.bank, encoding="utf-8") as g:
        draft = f.read()
        claims, problems = check(draft, g.read(), date.today(), args.max_age)
    out = sys.stderr if args.strip else sys.stdout
    for p in problems:
        print(p, file=out)
    print(f"{'FAILED' if problems else 'ok'}: {claims} claim(s), {len(problems)} problem(s)", file=out)
    if args.strip and not problems:
        sys.stdout.write(strip(draft))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
