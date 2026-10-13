---
description: Changing an accepted decision supersedes its ADR instead of rewriting it.
tags: [adr-writer]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

Here's ADR-0007 from our decisions folder:

# ADR-0007: Use PostgreSQL as the event store
- Status: Accepted
- Date: 2025-03-04
- Deciders: Platform team

## Context
The order service emits about 200 domain events per second. Projections need an append-only log they can replay, and the team already runs PostgreSQL.

## Decision
Store events in one PostgreSQL table partitioned by month, and rebuild projections by replaying it.

## Consequences
- Easier: one database to operate; events are written in the same transaction as the order data.
- Harder: replay time grows with history.

We now emit about 6,000 events per second, and rebuilding the order projection takes nine hours. Last week the platform team agreed to move the event log to Kafka with tiered storage and keep PostgreSQL only for the projections. Please rewrite ADR-0007 so it describes what we do now, and keep the number so the links in our runbooks still work.
