---
name: architecture-review
description: Reviews a design, spec, ADR or part of a codebase like a principal engineer, checking fit, simplicity, scale, failure modes, data, security, operability, cost and migration, with findings ranked from blocker to nit. Use it when someone wants an architecture or design review, a second opinion, or asks "will this scale?". Not for writing the design (use tech-spec) or an in-depth security analysis (use threat-model).
license: MIT
---

# Architecture review

Find the problems that are cheap to fix now and expensive to fix later, and say plainly what's good. A review that only lists nits missed the point; a review that only says "looks good" didn't happen.

## Inputs

The spec, ADR, diagram or code area under review, and the requirements behind it. For code, read the actual modules, configs and infrastructure definitions, not just the README.

## Lenses

1. **Requirements fit:** does it solve the stated problem, and only that?
2. **Simplicity:** what's the simplest design that meets the requirements? Name any component, layer or abstraction that doesn't earn its place.
3. **Scale:** what breaks first at 10x traffic, data or team size?
4. **Failure modes:** what happens when each dependency is slow, down or wrong? What's the blast radius, and where are the retries, timeouts, idempotency and backpressure?
5. **Data:** consistency guarantees, migrations, backups and restores, retention, and the source of truth.
6. **Security and privacy:** authentication, authorization, secrets, PII flows, and the attack surface. Use `threat-model` for depth.
7. **Operability:** observability, on-call burden, runbooks, and how you'd debug it at 3 a.m.
8. **Cost:** the main cost drivers, and how cost scales with usage.
9. **Delivery:** a migration path with rollback, incremental milestones, and whether the team can build and run it.

## Findings

| Severity | Meaning |
|---|---|
| **Blocker** | Must change before approval: correctness, data loss, security, or a design that can't meet the requirements |
| **Major** | Should change: significant risk, cost or complexity |
| **Minor** | Worth improving |
| **Nit** | Taste; take it or leave it |

Each finding gives the location (file and line, or spec section), what's wrong, why it matters, and the recommendation. Group them by severity.

## Output

`architecture-review-<slug>.md` containing:
- the verdict: **approve**, **approve with changes**, or **rework**, in one line,
- what's good (be specific),
- the findings by severity,
- the open questions for the author.

Keep it constructive: every criticism comes with a way forward.
