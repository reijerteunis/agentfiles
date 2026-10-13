# CTO workspace

Two locations with a hard boundary between them.

## Shared: in the company's engineering repo, visible to the engineering team

```
<shared>/
├── decisions/
│   ├── 0001-<slug>.md          ADRs, numbered, written by adr-writer
│   └── README.md               the index, regenerated
├── specs/YYYY-MM-<slug>.md     tech specs and RFCs (tech-spec)
├── postmortems/YYYY-MM-DD-<slug>.md
├── plans/YYYY-Qn.md            quarter plans
├── reviews/weekly/YYYY-Www.md  weekly reviews, team-safe
├── registers/
│   ├── risks.md
│   ├── decisions.md            two-way-door decisions, plus links to ADRs
│   ├── follow-ups.md           action items from postmortems, reviews and ADRs
│   └── tech-debt.md            (tech-debt-register)
└── metrics/YYYY-Www.json       raw snapshots from engineering-metrics
```

## Private: company-approved, CTO-only

Never a personal repo, never a shared folder.

```
<private>/
├── people/<person>/
│   ├── 1on1-YYYY-MM-DD.md
│   └── review-<cycle>.md
└── board/YYYY-Qn-update.md     drafts until they're shared with the board
```

## Register formats

All registers are Markdown tables, one row per item, newest first. Rows are updated in place; closed items keep their row with `status: done` and the date.

**risks.md**

| ID | Risk | Likelihood (1–5) | Impact (1–5) | Owner | Mitigation | Review on | Status |
|---|---|---|---|---|---|---|---|

**decisions.md**

| Date | Decision | Type (two-way / ADR-nnnn) | Owner | Revisit on |
|---|---|---|---|---|

**follow-ups.md**

| ID | Action | Source (postmortem, review or ADR) | Owner | Due | Status |
|---|---|---|---|---|---|

## Naming

Kebab-case slugs. Weeks are ISO weeks: `2026-W42`. Dates are `YYYY-MM-DD` in the company's time zone.
