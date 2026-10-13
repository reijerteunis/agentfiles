# Workspace

The job search lives in one folder (the "workspace"), as plain markdown files. Status is in YAML frontmatter; history goes in an append-only `## Log` section.

## Layout

```
<workspace>/
├── profile/
│   ├── master-cv.md       the only source of facts; every bullet has an ID like [co-1]
│   ├── stories.md         STAR stories, tagged by competency, citing master-CV IDs
│   └── preferences.md     roles, companies, location, money, timing, deal-breakers, never-contact list, watchlist
├── leads/
│   ├── .scout-state.json  {"last_scout": "YYYY-MM-DD"}, written by job-scout
│   └── YYYY-MM-DD-company-role.md
├── applications/
│   └── YYYY-MM-DD-company-role/
│       ├── application.md         status, dates, contacts, next action, log
│       ├── jd.md                  the posting, verbatim
│       ├── fit.md                 job-fit
│       ├── research.md            company-research
│       ├── cv.md, cv.pdf          cv-tailor (cv.md keeps the evidence IDs as comments)
│       ├── cover-letter.md        cover-letter
│       ├── answers.md             application-answers
│       ├── interview-prep-<stage>.md
│       └── offer.md
└── pipeline.md            regenerated dashboard
```

Names are kebab-case: `2026-10-13-acme-data-engineer`.

## Status values

- **Leads:** `new` → `shortlisted` | `rejected`
- **Applications:** `preparing` → `applied` → `screening` → `interviewing` → `offer` → `accepted` | `declined` | `rejected` | `withdrawn` | `ghosted`

## Lead template

```markdown
---
status: new
company: Acme
role: Senior Data Engineer
url: https://…
source: linkedin-alert | watchlist | referral | manual
location: Amsterdam (hybrid)
found_on: 2026-10-13
screen: pass | maybe
---

## Why it might fit
- …

## Posting
<the job description text, if it could be fetched>
```

## Application template

```markdown
---
status: preparing
company: Acme
role: Senior Data Engineer
url: https://…
source: linkedin-alert
fit_score: 78
applied_on:
contacts:
  - name: …
    role: hiring manager
    channel: email | linkedin
salary_range: "posted range, if any"
next_action: finish package
next_action_due: 2026-10-14
---

## Summary
One paragraph: the role, why it fits, the angle of the application.

## Log
- 2026-10-13 · created from lead · fit 78 (Go)
```

## Pipeline

`pipeline.md` is generated, never edited by hand: one table of active applications (company, role, status, next action, due), then leads awaiting a decision, then the counts per stage.
