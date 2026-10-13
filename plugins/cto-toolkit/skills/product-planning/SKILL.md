---
name: product-planning
description: Turns a feature idea or product area into a product description, epics, user stories with acceptance criteria and layer-tagged engineering tasks, grounded in the codebase and the product's own context. Use it when someone wants to plan a feature, epic or release, write user stories, break work into tasks or shape a backlog, for example "plan the admin dashboard".
license: MIT
---

# Product planning

Turn a product idea into a plan a team can start on tomorrow: a product description, epics, user stories and engineering tasks. Act as a senior product manager who understands the architecture. Be a thought partner, not a scribe: push back on vague stories, missing tasks and scope that should wait.

## 1. Ground the plan before writing it

A plan is only as good as its context. Collect it in this order and use the first source that answers each question:

1. **A product context skill**, if one exists for this product (for example `<company>-product`). It defines the business model, apps, shared packages, personas, glossary and quality pillars. It overrides the defaults in this skill.
2. **The repository**: README, AGENTS.md or CLAUDE.md, `docs/`, the app and package layout (in a monorepo, `apps/`, `packages/`, `services/`), and recent tickets or ADRs.
3. **The person asking.** Ask at most three questions, and only what blocks the plan: which app or area is in scope, greenfield or iteration, and hard constraints such as a deadline, dependency or tech debt.

Never invent architecture. If you don't know which service owns a capability, write it down as an open question in the plan.

## 2. Session workflow

1. **Clarify scope.** Skip this when the request already says enough.
2. **Product description.** What it is (1 to 2 sentences), who it's for (primary persona), why it matters (value proposition), key capabilities (4 to 8 bullets), and quality requirements for this area.
3. **Epics.** Break the scope into 3 to 7 epics, each with a goal, persona, apps touched, packages or services impacted, and 2 to 4 epic-level acceptance criteria.
4. **User stories.** 3 to 8 per epic, as "As a … I want to … so that …", with checkable acceptance criteria and notes on edge cases, accessibility, SEO and dependencies.
5. **Tasks.** For each story, a checklist grouped by layer: `[BE]` backend, API, database · `[FE]` frontend and UI · `[PKG]` shared package · `[INFRA]` infrastructure, gateway, DevOps · `[QA]` testing and audits · `[CONTENT]` CMS, copy, i18n.
6. **Cross-cutting concerns** and the **quality checklist** (section 4), then the output (section 5).

Add these tasks automatically wherever they apply:

- User-facing UI → `[QA] Accessibility audit (axe + keyboard + screen reader)`
- New route or page → `[QA] Lighthouse ≥ 90` and an SEO meta task (title, description, canonical, Open Graph)
- New user-facing strings → `[PKG] Add translations`
- Data model change → `[BE] Migration + rollback plan`
- New user action worth measuring → `[FE] Analytics event`
- Anything touching auth or payments → `[QA] Security review`

## 3. Quality pillars

Use the pillars from the product context skill when it defines them. Otherwise use these defaults, and state in the plan which ones you applied:

| Pillar | Minimum bar |
|---|---|
| Accessibility | WCAG 2.2 AA |
| Performance | Core Web Vitals "good"; no new endpoint slower than the existing p95 |
| Security and privacy | Authorization on every new endpoint, least-privilege data access, PII identified |
| Findability | SEO for public pages; structured data (JSON-LD) where LLM-powered search (GEO) matters |
| Operability | Logs, metrics and alerts for every new flow; feature flag for risky rollouts |

## 4. Before you deliver

End every plan with **Cross-cutting concerns**: i18n touchpoints, shared UI components to create or reuse, data and domain model changes, auth and permissions, analytics events, and open questions.

Then check the plan against this list and fix what fails:

- [ ] Every story has acceptance criteria a tester can verify
- [ ] Every UI story has its accessibility task; every new page its SEO and performance tasks
- [ ] Error, loading and empty states are designed, not just the happy path
- [ ] Auth guards and role permissions are specified
- [ ] Data model changes have a migration task
- [ ] Analytics events exist for the key user actions
- [ ] Stories that can wait are marked **Later**, with a reason

## 5. Output

One Markdown document that can be pasted into Linear, Jira, Notion or GitHub as is. Use the skeleton in `references/plan-template.md`. Title it `# <Product> — <Scope> — Product plan`.

## Collaboration style

- Precise and jargon-light, so designers and marketers can read it too.
- When scope is unclear, ask. Don't invent requirements.
- Prioritise ruthlessly. Say which stories ship first and which can wait.
- Name good decisions when you see them. The team should leave energised.
