# Spec template

```markdown
# <Title>

- **Status:** Draft | In review | Approved | Superseded
- **Author:** … · **Reviewers:** … (what each one checks)
- **Decision needed:** <the one-line question reviewers must answer, and by when>

## Summary
<Five lines: the problem, the proposal, the cost, the main risk.>

## Problem and context
<Who has the problem, how often, what it costs today. Link the evidence.>

## Goals
- <Measurable outcome>

## Non-goals
- <Explicitly out of scope, and why>

## Proposal
### Architecture
<Mermaid diagram plus a walkthrough.>
### Data model
<Schemas, changes, migrations, retention.>
### APIs and interfaces
<Endpoints, events, contracts, versioning.>
### Key flows
<Sequence for the main path and the main failure path.>

## Alternatives considered
1. <The simplest thing that could work>: why not.
2. …

## Rollout and rollback
<Flags, phases, backfills, the rollback at each phase, success criteria for moving on.>

## Observability
<Metrics, logs, traces, alerts, dashboards, SLOs.>

## Security and privacy
<Data classification, authorization, PII, threat model link.>

## Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## Open questions
| Question | Owner | Decide by |
|---|---|---|

## Milestones and estimate
<Ranges, with their assumptions.>
```
