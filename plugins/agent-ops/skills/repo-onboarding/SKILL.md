---
name: repo-onboarding
description: Gets a person or an agent productive in an unfamiliar codebase, read-only. It maps the structure, stack and data flow, finds the real build, test and lint commands and the conventions, and writes a one-page onboarding note plus a minimal AGENTS.md proposal. Use it when someone opens a new repository, joins a project, asks how a codebase works, or wants to brief agents on a repo.
license: MIT
---

# Repo onboarding

In 20 minutes, produce what a senior engineer would explain on day one: how it's built, how to run it, where things live, and what to be careful with. Read only. Never change files, install anything globally, or run commands with side effects without asking.

## Explore, read-only

1. **Shape:** the folder tree two or three levels deep, the languages and frameworks (from manifests and lockfiles), and the deploy targets.
2. **Commands:** from package.json scripts, the Makefile or justfile, the CI workflows and the README. Find the real install, dev, test (whole suite and a single test), lint, typecheck and build commands. Trust CI over the README when they differ.
3. **Architecture:** the entry points (main, the server, routes, handlers), the main modules and how data flows between them, the persistence layer, and the external services.
4. **Conventions:** the lint and format configs, how errors are handled, test patterns, naming, and where business logic lives. Learn these from code, not assumptions.
5. **Hotspots and history:**

   ```bash
   git log --since=3.months --name-only --format= | grep -v '^$' | sort | uniq -c | sort -rn | head -15   # most-changed files
   git log --oneline -20                                                                                  # recent activity
   git shortlog -sn --since=6.months | head                                                               # who works here
   ```

6. **Risks:** missing tests on critical paths, TODO or FIXME clusters, outdated dependencies, and generated or vendored code that shouldn't be edited.

## Output

**The onboarding note**, about a page:
- what the project is, in two lines,
- how to run it (the verified commands),
- a map of the main modules with one line each,
- the data flow,
- the conventions,
- hotspots and risks,
- open questions for the team.

**An AGENTS.md proposal:** only what an agent can't infer quickly, following `agent-instructions`. Propose it; the team decides whether to commit it.

If running the tests is safe and quick, ask before running them, and report the result. A green test suite is the best onboarding fact there is.
