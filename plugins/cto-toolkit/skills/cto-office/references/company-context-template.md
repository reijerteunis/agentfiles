# Company context template

The cto-office skill writes this during Onboard. Keep it in the company's own repo (`.claude/skills/<company>-context/SKILL.md` or `.agents/skills/…`), so company information stays in company systems. Keep it short: facts and pointers, not procedures.

```markdown
---
name: <company>-context
description: <Company>'s engineering context: systems and how to reach them, teams and leads, workspace locations, rhythm and board cadence. Use it whenever the cto-office agent or any cto-toolkit skill works for <Company>.
---

# <Company> engineering context

## The company
<Two lines: what it sells, to whom, stage, headcount in engineering.>

## Systems
| What | System | How to reach it |
|---|---|---|
| Tracker | Jira project ABC | Atlassian connector |
| Code | github.com/<org> | gh CLI |
| CI/CD | GitHub Actions, deploy workflow `deploy.yml` | gh CLI |
| Monitoring | Datadog | connector, or ask the CTO |
| Incidents | #incidents channel, status page <url> | read only |

## Teams
| Team | Lead | Owns |
|---|---|---|

## Workspace
- Shared: `<path in the engineering repo>`
- Private (people notes, board drafts): `<company-approved location>`

## Rhythm
- Weekly review: <day and time>
- Planning: <cycle>
- Board meetings: <dates>

## Rules
- <Anything specific: data classification, systems agents must never touch, approval chains.>
```
