---
name: jira-epic-cleanup
description: Cleans up a Jira epic and its child issues in one pass, with consistent descriptions, metadata moved into real custom fields, and blockers turned into real issue links. Use it when someone asks to clean up, tidy or fix the tickets under an epic, for example "clean up PROJ-123". Needs the Atlassian connector.
license: MIT
---

# Jira epic cleanup

Leave an epic and its stories in a state where a human can read any ticket in 30 seconds and every fact lives in the field built for it. Work through the Atlassian connector's Jira tools (`getJiraIssue`, `searchJiraIssuesUsingJql`, `editJiraIssue`, `createIssueLink`, `getAccessibleAtlassianResources`).

## 1. Load the project configuration

You need the cloud ID, the project key and the ID of every custom field you will write. Use the first source that has them:

1. **A project-specific cleanup skill** (for example `<project>-jira-cleanup`). It lists the IDs, typical values, aliases and known gotchas. Follow it over the defaults here.
2. **Discovery.** Get the cloud ID from `getAccessibleAtlassianResources`. Fetch the epic with `expand="names"` and `fields=["*all"]`: the `names` map translates field IDs to field names. Build the field map from that.

Never guess a field ID from a field name. If a field you need doesn't exist in the project, leave that data in the description's References block and report it.

## 2. Workflow

1. **Fetch the epic and its children in parallel.** The epic with `getJiraIssue` (`expand="names"`, `fields=["*all"]`, `responseContentFormat="markdown"`). The children with `searchJiraIssuesUsingJql` and `parent = <EPIC>` (newer projects) or `"Epic Link" = <EPIC>` (older company-managed projects), ordered by `created ASC`.
2. **Read everything first.** For each ticket, note the inline metadata: priority, estimate, executor, PRD and ADR references, customer impact, blocks and blocked-by.
3. **Rewrite each description** with the structure in `references/description-template.md`. Remove inline `**Field**: value` blobs from the body. Epics usually skip Acceptance Criteria and Notes but keep References.
4. **Write the fields and the description in one `editJiraIssue` call per ticket.** Only set fields that have a value in the original; skip empty ones instead of writing null. Built-in fields such as priority go in their own field, not in the description.
5. **Create the issue links.** Resolve every blocker reference to a real issue key first: search `project = <KEY> AND summary ~ "<words>"`. Skip references you can't resolve rather than creating a broken link. For "A blocks B", call `createIssueLink` with `inwardIssue = A`, `outwardIssue = B`, `type = "Blocks"`. One call per relationship: Jira shows the reverse ("is blocked by A") on B automatically.
6. **Verify.** Re-fetch two tickets, including one with links, and confirm the description, fields and links landed.
7. **Report** a table with one row per ticket (key, what changed, what was skipped and why), plus the references you couldn't resolve.

Work in parallel wherever steps don't depend on each other: fetching, resolving keys, and updating tickets.

## 3. Gotchas

- `editmeta` often lists only a few fields, but custom fields that aren't on the edit screen are still writable through the API by ID.
- Number fields such as story points take a number, not an object. Select fields take `{"value": "<option>"}` with an exact option name.
- Teams use aliases for tickets in descriptions ("the scaffold epic"). Resolve them by search; never guess.
- Don't create both directions of a link. Duplicates clutter the ticket and are tedious to clean up.
