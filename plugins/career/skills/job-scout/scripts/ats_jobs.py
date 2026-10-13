#!/usr/bin/env python3
"""List open jobs from companies' public job boards (Greenhouse, Lever, Ashby). Standard library only.

Usage:
  python3 ats_jobs.py --greenhouse anthropic --lever spotify --ashby linear [--match REGEX] [--location REGEX]
  python3 ats_jobs.py --self-test

The board token is the company's slug in its careers URL:
  boards.greenhouse.io/<token> · jobs.lever.co/<company> · jobs.ashbyhq.com/<org>

Prints a JSON array of {source, company, title, location, url, updated}. A board that fails is reported on
stderr and skipped, so one bad token never hides the other results.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

TIMEOUT = 20
USER_AGENT = "agentfiles-job-scout/1.0 (+https://github.com/reijerteunis/agentfiles)"


def fetch(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def from_ms(ms) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d") if ms else ""


def parse_greenhouse(token: str, data: dict) -> list[dict]:
    return [{
        "source": "greenhouse", "company": token, "title": j.get("title", ""),
        "location": (j.get("location") or {}).get("name", ""),
        "url": j.get("absolute_url", ""), "updated": (j.get("updated_at") or "")[:10],
    } for j in data.get("jobs", [])]


def parse_lever(company: str, data: list) -> list[dict]:
    return [{
        "source": "lever", "company": company, "title": j.get("text", ""),
        "location": (j.get("categories") or {}).get("location", ""),
        "url": j.get("hostedUrl", ""), "updated": from_ms(j.get("createdAt")),
    } for j in data]


def parse_ashby(org: str, data: dict) -> list[dict]:
    jobs = []
    for j in data.get("jobs", []):
        if j.get("isListed") is False:
            continue
        location = j.get("location", "")
        if j.get("isRemote") and "remote" not in location.lower():
            location = f"{location} (remote)".strip()
        jobs.append({
            "source": "ashby", "company": org, "title": j.get("title", ""), "location": location,
            "url": j.get("jobUrl", ""), "updated": (j.get("publishedAt") or "")[:10],
        })
    return jobs


BOARDS = {
    "greenhouse": ("https://boards-api.greenhouse.io/v1/boards/{}/jobs", parse_greenhouse),
    "lever": ("https://api.lever.co/v0/postings/{}?mode=json", parse_lever),
    "ashby": ("https://api.ashbyhq.com/posting-api/job-board/{}?includeCompensation=true", parse_ashby),
}


def collect(boards: list[tuple[str, str]], match: str | None, location: str | None) -> list[dict]:
    title_re = re.compile(match, re.I) if match else None
    loc_re = re.compile(location, re.I) if location else None
    jobs: list[dict] = []
    for kind, slug in boards:
        url, parse = BOARDS[kind]
        try:
            found = parse(slug, fetch(url.format(slug)))
        except Exception as exc:  # report and continue: one broken board must not hide the rest
            print(f"warning: {kind} board '{slug}' failed: {exc}", file=sys.stderr)
            continue
        jobs += [j for j in found
                 if (not title_re or title_re.search(j["title"]))
                 and (not loc_re or loc_re.search(j["location"]))]
    return jobs


def self_test() -> int:
    gh = parse_greenhouse("acme", {"jobs": [{"title": "Senior Data Engineer", "location": {"name": "Amsterdam"},
                                              "absolute_url": "https://x/1", "updated_at": "2026-10-01T10:00:00Z"}]})
    lv = parse_lever("acme", [{"text": "Analytics Engineer", "categories": {"location": "Remote"}, "hostedUrl": "https://x/2",
                               "createdAt": 1790000000000}])
    ab = parse_ashby("acme", {"jobs": [{"title": "Data Platform Engineer", "location": "Berlin", "isRemote": True,
                                        "jobUrl": "https://x/3", "publishedAt": "2026-09-30T00:00:00Z"},
                                       {"title": "Hidden", "isListed": False}]})
    checks = [
        gh[0]["title"] == "Senior Data Engineer" and gh[0]["location"] == "Amsterdam" and gh[0]["updated"] == "2026-10-01",
        lv[0]["title"] == "Analytics Engineer" and lv[0]["url"] == "https://x/2" and lv[0]["updated"].startswith("2026"),
        len(ab) == 1 and ab[0]["location"] == "Berlin (remote)",
        bool(re.compile("data engineer|analytics engineer", re.I).search("Senior Data Engineer")),
    ]
    print("ats_jobs self-test:", "ok" if all(checks) else f"FAILED {checks}")
    return 0 if all(checks) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="List open jobs from public Greenhouse, Lever and Ashby boards.")
    for kind in BOARDS:
        ap.add_argument(f"--{kind}", action="append", default=[], metavar="SLUG")
    ap.add_argument("--match", help="regex the job title must match (case-insensitive)")
    ap.add_argument("--location", help="regex the location must match (case-insensitive)")
    ap.add_argument("--self-test", action="store_true", help="run offline parser tests")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    boards = [(kind, slug) for kind in BOARDS for slug in getattr(args, kind)]
    if not boards:
        ap.error("give at least one --greenhouse, --lever or --ashby board")
    json.dump(collect(boards, args.match, args.location), sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
