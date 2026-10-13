---
name: tech-spec
description: Writes technical specs, RFCs and design docs sized to the change, covering goals and non-goals, the design, alternatives, rollout and rollback, observability, security, risks and open questions. Use it when someone needs to design a feature or system before building it, or asks for a spec, RFC or design doc. Not for recording a single decision (use adr-writer) or reviewing someone else's design (use architecture-review).
license: MIT
---

# Tech spec

A spec is a tool for being wrong cheaply: on paper, before the code. Its job is to surface the hard questions early and get the right people to agree on the answer.

## Size it to the change

- **Small** (one team, under 2 weeks): one page with problem, proposal, risks and rollout.
- **Medium** (cross-team, or 2–8 weeks): the full template, 3–5 pages.
- **Large** (platform-level, or months of work): the full template plus an ADR for each one-way-door decision inside it.

## Steps

1. **Interview the author.** Ask what problem it solves, for whom, how we'll know it worked, the constraints, and the deadline. Read the code and docs that the change touches.
2. **Draft** with `references/spec-template.md`. The hard parts get the most words: data model changes, migrations, failure modes, and anything irreversible.
3. **Alternatives.** At least two, including the simplest thing that could work, each with why it lost.
4. **Rollout.** Feature flags, migration and backfill steps, how to roll back at each step, and who's on call.
5. **Open questions.** List what's undecided, with an owner and a deadline. A spec with no open questions usually hasn't been thought through.
6. **Review.** Name the reviewers and what each should check (security, data, the owning team). Have the `principal-engineer` agent challenge it if it's available. Record one-way-door choices with `adr-writer`.

## Rules

- Write for the reviewer: put the decision needed and the riskiest part at the top.
- Diagrams in Mermaid so they live in git.
- Don't hide the uncertain parts; label them. An estimate is a range with its assumptions.

## Output

`specs/YYYY-MM-<slug>.md` in the company workspace. Its status is Draft, In review, Approved or Superseded, and it lists the reviewers and the decisions needed.
