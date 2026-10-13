---
name: weekly-review
description: Closes the week against the person's priorities, covering time spent, promises kept and overdue, wins and lessons, and next week's one thing with protected time. Use it when someone asks for a weekly review, a Friday wrap-up or help planning next week. Not for a team's engineering review (use cto-office).
license: MIT
---

# Weekly review

Ten minutes on Friday buys a calmer Monday. The review closes loops, learns from the week, and turns intentions into time on the calendar.

## Gather

- `profile/priorities.md`: the quarter's priorities and this week's one thing.
- This week's briefs, meeting files, decisions and delegations in the workspace.
- `follow-ups.md`: use the `follow-up-tracker` skill to list overdue items and next week's (its script does the date maths).
- The time audit from `calendar-review` for this week and next.

## Write `reviews/YYYY-Www.md`

```markdown
# Week <nn>: review

## The week in three lines
<What moved, what didn't, how it felt.>

## Priorities
| Priority | Planned | What happened | Hours |
|---|---|---|---|

## Promises
- Kept: <n> · Overdue: <list> · Owed to me and overdue: <list>

## Wins
- …

## Lessons
- <What to do differently, as a rule for next week: "No meetings before 10 on Wednesdays.">

## Next week
**The one thing:** …
**Top three:** 1. … 2. … 3. …
**Protected time:** <the proposed focus blocks, waiting for approval>
**Prep needed:** <meetings next week that need prep>
**Say no to:** <what to decline or delegate>
```

## Rules

- Be honest, not cheerful. If a priority got zero hours, say so, and ask whether it's still a priority.
- At most three lessons, each phrased as a rule the person can follow.
- Propose calendar changes. Don't make them, except approved private focus blocks.
- Update `profile/priorities.md` with next week's one thing once the person confirms it.
