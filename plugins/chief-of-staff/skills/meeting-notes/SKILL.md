---
name: meeting-notes
description: Turns raw notes or a transcript into decisions, owned action items and open questions, records the promises made, and drafts the recap. Use it when someone shares meeting notes or a transcript, asks to write up a meeting, or asks "what did we agree?".
license: MIT
---

# Meeting notes

A meeting without written decisions and owners didn't happen. Turn the raw material into a record anyone could act on next week.

## Inputs

The notes or transcript, the meeting file's `## Prep` section if there is one (compare what happened with the desired outcome), and the attendee list. If the material doesn't say who owns an action or by when, ask; never guess.

## Write

Add a `## Notes` section to `meetings/YYYY-MM-DD-<slug>.md`, or to the company workspace for an employer's meeting:

```markdown
## Notes
**Outcome vs. goal:** <did we get what we came for?>

**Decisions**
1. <Decision>: <the reason, in a few words>

**Action items**
| Action | Owner | Due |
|---|---|---|

**Open questions**
- <Question>: <who will find out>

**Context worth keeping**
- <Facts, numbers or commitments mentioned that matter later>
```

## Rules

- Decisions are things that were actually agreed. Proposals and opinions aren't decisions; record them under open questions.
- Use the names as said, and don't attribute quotes unless the person wants that. Keep sensitive remarks about people out of the record.
- Every action item has one owner. "Team" is not an owner.
- Record the person's own actions as `I owe` and other people's actions for them as `owed to me`, with `follow-up-tracker`.

## Follow-up email

Draft a short recap to the attendees, as a draft and never sent: thanks in one line, then the decisions, the action items with owners and dates, and the next meeting if there is one. Do this only when the person usually sends recaps, or asks for one.
