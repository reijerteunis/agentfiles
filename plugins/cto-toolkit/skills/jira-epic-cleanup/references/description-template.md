# Description template

Every story description follows this structure. Epics keep the summary and References and drop the sections that don't apply.

```markdown
<One concise paragraph: what this ticket is and why it exists. No metadata here.>

---

## Acceptance Criteria

1. …
2. …

---

## Notes

> ⚠️ Technical constraint or gotcha.
> ℹ️ Process or executor note.
> 🎬 Media required (Loom, screencast).

---

## References

- PRD: …
- ADR: …
- Story points: …
- Executor: …
- Customer-facing: …
- Blocks: …
- Blocked by: …
- Risk: …
```

The References block stays as a readable footer even though the same data now lives in dedicated fields. It's the record for people who read the ticket, not for queries. Leave out lines that have no value.
