---
type: llm
---

PASS if ADR-0007's original context, decision and consequences stay as they were, with only its status changed to say it is superseded by a new record that it points to, and the Kafka move is written as a new ADR with its own number whose context explains what changed (about 6,000 events per second, nine-hour rebuilds) and whose consequences include at least one real downside of the move. It may point out that the runbook links keep working because ADR-0007 still exists and points to the new record.
FAIL if it rewrites ADR-0007's context or decision to describe the Kafka setup, deletes the original rationale, or records the Kafka decision without linking it to ADR-0007.
