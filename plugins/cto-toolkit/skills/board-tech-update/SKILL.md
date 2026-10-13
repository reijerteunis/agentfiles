---
name: board-tech-update
description: Writes the quarterly technology update for a board or investors, as one page with the status, progress, consistent metrics, risks and asks, built from sourced data. Use it when a CTO needs a board update, an investor update or a quarterly technology summary.
license: MIT
---

# Board tech update

The board reads it in five minutes and should come away knowing three things: are we on track, what could hurt us, and what do you need from us. Write for smart people who aren't engineers.

## Inputs

The quarter's weekly reviews, `engineering-metrics` snapshots, the risk and decision registers, the plan for the quarter, cost data, and the hiring pipeline. Every number has a source. A number you can't source becomes a gap to fill, never an estimate.

## The one-pager

1. **Headline:** one line with the status and why. For example: "On track: checkout rebuild shipped; reliability slipped in August, now recovered."
2. **Progress against plan:** 3–5 outcomes tied to business goals ("faster checkout: conversion +x%"), plus what slipped and why.
3. **Metrics:** a small table with the same metrics every quarter, so trends are visible:
   - deployment frequency and lead time
   - availability against its SLO, and major incidents
   - security posture (open critical findings)
   - cloud cost and unit cost
   - engineering headcount, attrition and open roles
4. **Risks:** the top three, each with its likelihood, impact, mitigation and owner. Name them before the board finds them.
5. **Asks:** the decisions, budget or introductions you need from the board, each with its rationale.
6. **Next quarter:** three priorities and how you'll know they worked.

Put the detail in an appendix: architecture changes, the incident summary, AI and compliance status, and team changes.

## Rules

- No jargon without a one-line translation. Give outcomes before activities.
- Keep the same structure and metric definitions every quarter, so the board can compare.
- Be honest about misses. Boards forgive bad news delivered early, not surprises.
- Save drafts only to the private `board/` folder. The CTO decides when to share.

## Output

`board/YYYY-Qn-update.md`: the one-pager, the appendix, and a list of numbers that still need a source.
