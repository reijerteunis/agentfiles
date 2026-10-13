---
name: incident-commander
description: Runs a live production incident with a severity, roles, a first-five-minutes checklist, a timeline, mitigation before root cause and updates on a fixed cadence, investigating read-only. Use it when something is broken or degraded in production, or someone says "we have an incident" or "the site is down". Once it's resolved, use incident-postmortem.
license: MIT
---

# Incident commander

In an incident, calm structure beats heroics. Your job is to make sure the right people are working on the right thing, decisions are made and written down, and everyone who needs to know is told, on time.

## Safety rule for agents

Investigate read-only: logs, dashboards, recent deploys, error trackers. **Never** execute a change on production (rollback, restart, config, data fix) yourself. Propose it with its risk, and let the human incident commander approve it and the operator run it. Record every approved action in the timeline.

## Severity

| Sev | Criteria | Updates |
|---|---|---|
| **SEV1** | Core flow down for many customers, data loss or a security breach | every 30 min |
| **SEV2** | Major degradation, or a core flow down for some customers | every 60 min |
| **SEV3** | Minor degradation with a workaround | at milestones |
| **SEV4** | Cosmetic, or internal only | none |

When in doubt, pick the higher severity; lowering it later is cheap.

## First five minutes

1. Declare the incident: severity, a one-line description, and a dedicated channel or thread.
2. Assign the roles: **incident commander** (coordinates and decides), **ops lead** (hands on keyboard), **comms lead** (updates), and **scribe** (timeline). In a small team one person holds several roles, but never IC and ops lead together for a SEV1.
3. Establish the impact: who is affected, what's broken, since when. Use dashboards, not guesses.
4. Ask what changed: deploys, config, traffic, dependencies, certificates, quotas.
5. Send the first update with `references/comms-templates.md`, within 15 minutes for SEV1 and SEV2.

## During the incident

- **Mitigate first:** roll back the last change, flip a flag, fail over, add capacity, or shed load. Root cause can wait; customers can't.
- Keep a **timeline** in UTC: what was seen, what was done, and by whom.
- Keep a **decision log** of what was decided, why, and on what evidence.
- Every 30 minutes, ask what we know now, what we're trying next, and whether we need more people.
- Send updates on the cadence even when nothing has changed. "Still investigating, next update at 14:30" is a valid update.

## Close out

1. Resolution: the impact has stopped and the metrics are back to normal for a sustained period (at least 30 minutes for SEV1).
2. Send the all-clear to the same audiences that got the updates.
3. Hand the timeline and decision log to `incident-postmortem`, and schedule the review within five working days.
4. Write down any temporary mitigation that needs a permanent fix as a follow-up with an owner.
