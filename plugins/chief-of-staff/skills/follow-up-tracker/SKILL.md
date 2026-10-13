---
name: follow-up-tracker
description: Keeps one list of every promise the person owes or is owed, checks due dates with a script and drafts the nudges. Use it when someone asks what they owe, who's waiting on them, or wants to track a commitment. Job-application follow-ups belong to the job-search agent.
license: MIT
compatibility: Runs a Python 3 script on the workspace's follow-ups.md.
---

# Follow-up tracker

Trust breaks on dropped promises, not on big failures. One list, in a fixed format, checked by a script, means nothing is ever forgotten.

## The list

`follow-ups.md` in the chief-of-staff workspace: one Markdown table with the columns `ID | Promise | Direction | Who | Due | Source | Status`. The format and an example are in the chief-of-staff workspace reference.

- **Direction:** `I owe` (the person promised) or `owed to me` (someone promised the person).
- **Status:** `open`, `waiting` (the ball is with someone else), `done` or `dropped`.
- **Source:** the meeting file, or the email date and sender, so anyone can check what was said.

## Capture

When a promise appears in an email, meeting or note, add a row with the next free ID (`F-NNN`). Give it a due date: the one stated, or for a vague promise ("next week", "soon") a concrete date that the person confirms. Never record a promise the person didn't actually make.

## Check

```bash
python3 scripts/followups.py <workspace>/follow-ups.md --check          # the format is valid
python3 scripts/followups.py <workspace>/follow-ups.md --due --days 2   # overdue and due within two days
```

Never compute due dates in your head. Use the script's output.

## Act

- **I owe, due or overdue:** remind the person in the brief. If it's overdue, draft the "here it is" or "need two more days" message with `email-reply`.
- **Owed to me, overdue:** draft a friendly nudge. The first nudge is gentle; the second names the impact. Always as a draft.
- **Done:** set `done` when there's evidence (the email was sent, the file delivered). Set `dropped` only when the person says so.

## Report

The overdue items first, then due this week, grouped by `I owe` and `owed to me`, with the drafted nudges listed.
