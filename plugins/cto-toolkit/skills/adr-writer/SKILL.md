---
name: adr-writer
description: Writes architecture decision records with context, honest options including doing nothing, the drivers, the decision and its consequences, numbered and superseded rather than rewritten. Use it when a team makes or debates a hard-to-reverse technical choice, or asks for an ADR or decision record. Not for full design documents (use tech-spec) or reviewing a design (use architecture-review).
license: MIT
---

# ADR writer

An ADR exists so that someone in two years understands why, not just what. Write the options honestly, especially the ones that lost, because that's what stops the same debate from happening again.

## Is it ADR-worthy?

Write an ADR for a **one-way door**: hard or expensive to reverse, touching several teams, constraining future choices, or likely to be questioned later. For a cheap, reversible choice, a single line in the decision log is enough. Say so instead of writing an ADR.

## Steps

1. **Context.** Read the relevant code, docs, specs and earlier ADRs, and talk to the person deciding. State the problem in two or three sentences that someone outside the team understands.
2. **Decision drivers.** List the 3–6 criteria that matter, in order: for example cost, time to value, team skills, scalability, lock-in, compliance.
3. **Options.** At least two real options plus **do nothing**. Steelman each one: write it the way its strongest advocate would. Score each option against the drivers, with evidence, not adjectives.
4. **Reversibility.** For each option, what would it cost to undo it in a year? Use the `build-vs-buy` skill when the question is about sourcing.
5. **Outcome.** The recommended option, and why it beats the runner-up on the drivers that matter most.
6. **Consequences.** What becomes easier, what becomes harder, and what new risks or work the decision creates. Include the bad ones.
7. **Confirmation.** How we'll know the decision is working (a metric, a milestone), and the date to revisit it.

Write it with `references/adr-template.md`. The status starts as **Proposed**; the decision-maker accepts it.

## Numbering and history

- Number sequentially in `decisions/`: the next free `NNNN`, with a kebab-case slug.
- Never rewrite an accepted ADR's decision. A new ADR **supersedes** it, and the old one gets `Status: Superseded by ADR-NNNN`.
- Update `decisions/README.md` (the index) and the decision log.

## Before delivering

Can a newcomer understand the context without asking anyone? Does every option have its real downside? Is the "do nothing" option honestly evaluated? Is the revisit date set?
