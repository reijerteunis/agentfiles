---
name: incident-postmortem
description: Writes blameless postmortems with a sourced timeline, measured impact, contributing factors instead of a guilty person, and at most seven owned, dated action items. Use it after an incident, or when someone asks for a postmortem, incident report or RCA. Not while the incident is still live (use incident-commander).
license: MIT
---

# Incident postmortem

The purpose is learning, not blame. If the postmortem names a person as the cause, the organisation learns to hide incidents. Ask how the system made the mistake easy, not who made it.

## Gather the facts first

Collect the evidence before you write: alerts and monitoring graphs, the incident channel, the deploy and config history, commits, tickets, customer reports, and the incident commander's timeline and decision log. Interview the responders about what they saw and why each choice made sense at the time.

## Write it

Use `references/postmortem-template.md`.

1. **Summary** in five lines: what happened, the impact, the duration, the fix, and the main lesson.
2. **Impact** from data only: the duration, customers and requests affected, SLO budget burned, and revenue if it can be measured. Mark estimates as estimates.
3. **Timeline** in UTC: detection, escalation, key decisions, mitigation and resolution. Highlight **time to detect** and **time to mitigate**.
4. **Contributing factors:** usually several, across technology (missing guard, weak test, single point of failure), process (deploy without canary, missing runbook) and organisation (ownership gap, overload). Write each as a condition, not a person: "the deploy pipeline allowed…", not "Alex deployed…".
5. **What went well**, and **where we got lucky**. Luck is the next incident.
6. **Action items:** at most 7, each **prevent**, **detect** or **mitigate**, with an owner, a due date and a tracking link. Prefer items that remove a whole class of failure. Put each one in the follow-ups register. When nobody has named the owners and dates yet, propose them: the owning team or role, and a date counted from today (sooner for detect items), each marked *proposed* for the review meeting to confirm.

## Rules

- Blameless language throughout: no names in the causes, no "should have", no "human error" as a cause.
- Treat every number as a claim that needs a source.
- Hold the review meeting within five working days, and finalise the document after it.
- An action item without an owner and a date is a wish. Don't list wishes, and never leave either as TBD: propose one and mark it.

## Output

`postmortems/YYYY-MM-DD-<slug>.md` in the company workspace, plus new rows in `registers/follow-ups.md`. In the reply, give the summary, the top contributing factor, and the action items.
