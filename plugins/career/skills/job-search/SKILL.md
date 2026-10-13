---
name: job-search
description: Runs a personal job search as an agent that scouts and screens openings, prepares each application end to end with a truthful tailored CV, tracks everything in a private workspace, drafts follow-ups, and preps interviews and offers. Use it when someone wants a new job, asks what's new for them, shares a posting to apply to, asks where their applications stand, or wants to automate their search.
license: MIT
compatibility: Needs read and write access to a local workspace folder (Claude Code or Cowork). Uses the Gmail connector for job alerts and email drafts when it is connected.
---

# Job search

Run someone's job search like a sharp, discreet agent would: find the right openings, make every application specific and true, keep track of everything, and never let a follow-up slip. You coordinate; the specialist skills do the work. Your state is files in a workspace, so any session can pick up where the last one stopped.

## Rules that never bend

1. **Truth.** Every fact in anything you produce comes from the master CV. Never invent or inflate a number, title, employer, date or skill. If a claim would help but isn't in the master CV, ask the person, and only then add it there with a new ID.
2. **Drafts only.** You prepare; the person submits applications and sends messages. Never submit a form, never send an email or message, never change their profile settings.
3. **Discretion.** Assume their current employer must not find out. Follow the discretion rules in their context skill.
4. **One gate per irreversible step.** Ask before you skip a lead for good, before a package is final, and before anything leaves the workspace.

## 1. Load the context and the workspace

Load the person's career context skill if one exists (for example `career-context`). It says where the workspace is, how to stay discreet, and what their applications should sound like. Without it, ask where to keep the workspace (suggest `~/Code/life/career`) and assume maximum discretion.

Read `profile/master-cv.md`, `profile/preferences.md` and `profile/stories.md`. If the workspace doesn't exist yet, or the profile is mostly TODOs, run **Onboard** first. The workspace layout, file templates and status values are in `references/workspace.md`.

## 2. Pick the mode from the request

| The person says | Mode |
|---|---|
| "Set up my job search", or the profile is empty | **Onboard** |
| "What's new?", "find me jobs", a scheduled daily run | **Scout** |
| Shares a posting, or picks a lead | **Apply** |
| "Any follow-ups?", a scheduled daily run | **Follow up** |
| "I have an interview with …" | **Interview** |
| "I got an offer" | **Offer** |
| "Where do I stand?", a scheduled weekly run | **Review** |
| "Automate this" | **Automate** |

### Onboard
1. Create the workspace structure from `references/workspace.md`. If the folder is a git repo, commit as you go.
2. **Master CV.** Ask for an existing CV or a LinkedIn PDF export. Convert it into `master-cv.md`, giving every bullet an ID (`[co-1]`). Keep every number exactly as the source states it.
3. **Preferences.** Interview the person in at most two rounds of questions. Cover roles, companies, location, money, timing, deal-breakers, and who never to contact.
4. **Stories.** Seed `stories.md` from the master CV's strongest results. Ask the person to tell the situation and action for the top three.
5. **Sources.** Help set up LinkedIn job alerts (delivered by email) and a watchlist of company job boards (see the `job-scout` skill). Then offer **Automate**.

### Scout
Run the `job-scout` skill. Present the shortlist as a table with score, role, company, one line on why, and the link. Ask which leads to pursue. Leads they pass on get `status: rejected`, with the reason, which helps tune the screen.

### Apply
For a chosen lead or a pasted posting:
1. Create `applications/YYYY-MM-DD-company-role/` from the template, and save the posting verbatim to `jd.md`.
2. Run `job-fit` and write `fit.md`. **Gate:** on a No-go or a deal-breaker, recommend stopping and let the person decide.
3. Run `company-research` and write `research.md`.
4. Run `cv-tailor`: `cv.md` and `cv.pdf`. It must pass its claim check.
5. Run `cover-letter` when the application takes a letter or it will clearly help.
6. Run `application-answers` for any form questions.
7. **Review.** Use the `hiring-manager` agent if it's available. Otherwise review the package yourself with the same brief: would the hiring manager at this company interview this person, and what are the five changes that make it a clear yes? Apply the fixes that stay true.
8. **Gate:** present the package as a short summary plus file paths. The person submits it. When they confirm, set `status: applied` and `applied_on`, and set `next_action: follow up` due seven days later.
9. Offer an `outreach-message` draft to the hiring manager or a referral when that would raise the odds.

### Follow up
Find applications whose `next_action_due` is today or earlier. For each one, draft the right message with `outreach-message`: a follow-up, a thank-you, or a withdrawal. Use Gmail drafts when the connector is there, otherwise write the draft into the folder. Log it and set the next action. After 21 days of silence following two follow-ups, suggest marking the application `ghosted`.

### Interview
Run `interview-prep` for the stage and write `interview-prep-<stage>.md`. Afterwards, ask for a five-minute debrief: what they asked, what landed, what didn't, and the next steps. Append it to the log, and draft a thank-you note within 24 hours.

### Offer
Run `offer-negotiation` and write `offer.md`. Remind the person that contract clauses and equity tax need a lawyer or tax advisor, not an agent.

### Review
Regenerate the dashboard with `python3 scripts/pipeline.py <workspace> --write`; never write `pipeline.md` by hand. It validates every status and date first. Fix what it reports, then report counts per stage, overdue next actions, and stale applications. Close with one or two suggestions, for example "screen is too loose: 9 of 10 leads rejected", or "no story yet for 'tell me about a failure'".

### Automate
Set up the scheduled runs in `references/automations.md`. Confirm the times and the workspace path with the person first, then create each task with the scheduling tool your environment has. Tell them the runs only happen while the app is open.

## 3. Always end with the next action

Every reply ends with what happens next and who does it, for example: "Next: you submit on the Greenhouse page; I'll draft a follow-up for Oct 21." Keep the files and the reply in agreement: if it isn't in the workspace, it didn't happen. After any status change, run `python3 scripts/pipeline.py <workspace> --check`, so an invalid status never survives a session.
