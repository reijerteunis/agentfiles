# Chief-of-staff workspace

Plain markdown in a private folder, for example `~/Code/life/cos`. Company work goes to the company workspace instead (see the orchestrator's rule 5).

```
<workspace>/
├── profile/
│   ├── priorities.md     quarter priorities, this week's one thing, what to say no to
│   ├── people.md         VIPs: name, relationship, how to handle (minimal, no sensitive details)
│   └── policies.md       email, calendar, focus time, response times, never-touch list
├── briefs/YYYY-MM-DD.md
├── meetings/YYYY-MM-DD-<slug>.md   prep and notes for one meeting
├── decisions/YYYY-MM-DD-<slug>.md
├── delegations/YYYY-MM-DD-<slug>.md
├── reviews/YYYY-Www.md
└── follow-ups.md                   the promise tracker (follow-up-tracker)
```

## follow-ups.md

One table, maintained by the `follow-up-tracker` skill and checked by its script:

```markdown
| ID | Promise | Direction | Who | Due | Source | Status |
|---|---|---|---|---|---|---|
| F-001 | Send the board deck | I owe | Anna (board) | 2026-10-15 | meetings/2026-10-13-board-prep.md | open |
| F-002 | Contract redlines | owed to me | Legal (Mark) | 2026-10-17 | email 2026-10-12 | open |
```

- **Direction:** `I owe` or `owed to me`.
- **Status:** `open`, `done`, `dropped` or `waiting`.
- **Due:** `YYYY-MM-DD`, or empty.

## Meeting file

```markdown
---
date: 2026-10-13
title: Board prep with Anna
attendees: [Anna (board chair)]
context: personal | <company>
---

## Prep
Goal · attendees and context · open threads · questions · desired outcome · materials

## Notes
Decisions · action items (owner, due) · open questions · follow-up drafted: yes/no
```

## Naming

Kebab-case slugs. Weeks are ISO weeks (`2026-W42`).
