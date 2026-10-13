#!/usr/bin/env python3
"""Check a tailored CV against the master CV: no claim without a source. Standard library only.

Usage:
  python3 check_claims.py cv.md master-cv.md
  python3 check_claims.py --self-test

Rules:
  1. Every bullet cites at least one master-CV ID in an HTML comment: <!-- bc-2 --> or <!-- bc-2, bc-6 -->.
  2. Every cited ID exists in the master CV (bullets there look like "- [bc-2] …").
  3. Every number in a bullet appears in the master bullets it cites.
  4. Every number in other text (summary, skills, education) appears somewhere in the master CV.
  5. Every part of a role heading ("### Company · Title · Dates") appears in the matching master heading,
     so titles and dates can't be invented or upgraded. TODO parts in the master can't be used.
Exits 1 and lists every violation with its line number.
"""

from __future__ import annotations

import argparse
import re
import sys

ID_RE = re.compile(r"\[([a-z]{2,4}-\d+)\]")
CITE_RE = re.compile(r"<!--\s*([a-z]{2,4}-\d+(?:\s*,\s*[a-z]{2,4}-\d+)*)\s*-->")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
NUM_RE = re.compile(r"\d[\d,.]*\d|\d")
BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")


def numbers(text: str) -> set[str]:
    """Numbers as written, normalised: 12,500 → 12500 · 3,75 → 3.75 · 40+ → 40 · €2M → 2."""
    found = set()
    for raw in NUM_RE.findall(COMMENT_RE.sub("", text)):
        if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", raw):
            raw = raw.replace(",", "")
        elif re.fullmatch(r"\d+,\d+", raw):
            raw = raw.replace(",", ".")
        found.add(raw.rstrip(".,"))
    return found


def heading_parts(line: str) -> list[str]:
    text = re.sub(r"\s+", " ", line.lstrip("#").strip())
    text = re.sub(r"\s*[–—-]\s*", " – ", text)  # one dash style for date ranges
    return [p.strip().lower() for p in text.split("·") if p.strip()]


def parse_master(text: str) -> tuple[dict[str, str], list[list[str]], set[str]]:
    bullets, headings = {}, []
    for line in text.splitlines():
        m = BULLET_RE.match(line)
        if m and (ids := ID_RE.findall(m.group(1))):
            for i in ids:
                bullets[i] = m.group(1)
        elif line.startswith("### "):
            headings.append(heading_parts(line))
    return bullets, headings, numbers(text)


def check(cv: str, master: str) -> list[str]:
    bullets, headings, all_numbers = parse_master(master)
    problems = []
    in_frontmatter = cv.startswith("---\n")
    for n, line in enumerate(cv.splitlines(), 1):
        if in_frontmatter:
            in_frontmatter = n == 1 or line.strip() != "---"
            continue
        if not line.strip() or line.startswith(("# ", "## ")):
            continue
        if line.startswith("### "):
            parts = heading_parts(line)
            match = next((h for h in headings if parts and h and h[0] == parts[0]), None)
            if not match:
                problems.append(f"line {n}: role '{parts[0] if parts else line}' is not in the master CV")
                continue
            for p in parts[1:]:
                if p not in match or "todo" in p:
                    problems.append(f"line {n}: '{p}' is not in the master heading '{' · '.join(match)}'")
            continue
        m = BULLET_RE.match(line)
        if m:
            cited = [i.strip() for c in CITE_RE.findall(line) for i in c.split(",")]
            if not cited:
                problems.append(f"line {n}: bullet cites no master-CV ID: {m.group(1)[:70]}")
                continue
            unknown = [i for i in cited if i not in bullets]
            if unknown:
                problems.append(f"line {n}: cites IDs that aren't in the master CV: {', '.join(unknown)}")
            source = set().union(*(numbers(bullets[i]) for i in cited if i in bullets))
            invented = numbers(line) - source
            if invented:
                problems.append(f"line {n}: numbers not in the cited source ({', '.join(cited)}): {', '.join(sorted(invented))}")
            continue
        invented = numbers(line) - all_numbers
        if invented:
            problems.append(f"line {n}: numbers not found anywhere in the master CV: {', '.join(sorted(invented))}")
    return problems


def self_test() -> int:
    master = """# Master CV
### Brightcart · TODO title · 2019 – 2024
- [bc-2] Cut the nightly reporting job from 40+ minutes to 6.
- [bc-6] Grew the data team from 3 to 7 people across two offices.
### Pixelwerk · Data Engineer · 2016 – 2019
- [px-1] Moved the warehouse from MySQL to BigQuery in two months with three people.
"""
    good = """# Jane
## Experience
### Brightcart · 2019-2024
- Made reporting 10x faster, from 40 minutes to 6 <!-- bc-2 -->
- Grew the data team from 3 to 7 across two offices <!-- bc-6 -->
### Pixelwerk · Data Engineer · 2016 – 2019
- Moved the warehouse from MySQL to BigQuery <!-- px-1 -->
"""
    bad = """### Brightcart · Lead Data Engineer · 2019 – 2024
- Grew the data team from 3 to 12 <!-- bc-6 -->
- Led a platform rewrite
- Cut costs <!-- zz-9 -->
### Acme · Lead Data Engineer · 2020
Summary: 25 years of experience
"""
    good_problems = check(good.replace("10x faster, ", ""), master)
    invented_multiplier = check(good, master)  # "10x" is not in the source bullet
    bad_problems = check(bad, master)
    expected = ["'lead data engineer' is not in the master", "(bc-6): 12", "cites no master-CV ID", "zz-9",
                "'acme' is not in the master", "master CV: 25"]
    missing = [e for e in expected if not any(e in p for p in bad_problems)]
    ok = not good_problems and invented_multiplier and not missing
    print("check_claims self-test:", "ok" if ok else f"FAILED\n good: {good_problems}\n bad: {bad_problems}\n missing: {missing}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Check a tailored CV against the master CV.")
    ap.add_argument("cv", nargs="?")
    ap.add_argument("master", nargs="?")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.cv and args.master):
        ap.error("give the tailored CV and the master CV")
    with open(args.cv, encoding="utf-8") as f, open(args.master, encoding="utf-8") as g:
        problems = check(f.read(), g.read())
    for p in problems:
        print(p)
    print(f"{'FAILED' if problems else 'ok'}: {len(problems)} unsupported claim(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
