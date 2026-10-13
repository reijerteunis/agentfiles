---
name: cv-tailor
description: Tailors a CV to one job without lying. It selects and rephrases master-CV results, cites the source of every bullet, runs a claim check and renders an ATS-friendly PDF. Use it when someone wants their CV or resume tailored to a job, or optimised for applicant tracking systems.
license: MIT
compatibility: Runs Python 3 scripts. Rendering the PDF needs Chrome or Chromium installed.
---

# CV tailor

A tailored CV says the same true things as the master CV, chosen and phrased for one reader. The hiring manager should recognise their own job in the first half page, and every line should survive a reference check.

## Inputs

`profile/master-cv.md` (the only source of facts, with an ID on every bullet), plus the application's `jd.md` and `fit.md` (the must-haves and **the angle**). Without a master CV, build one first with the person: the job-search skill's Onboard mode.

## What you may and may not change

| Allowed | Never |
|---|---|
| Select, drop and reorder bullets | Add a number, or change one |
| Rephrase a fact in the posting's vocabulary | Upgrade scope ("part of" → "led", "8 people" → "a large team") |
| Merge two bullets from the same role, citing both | Add a tool, skill, certificate or employer that isn't in the master CV |
| Shorten older roles to one line, or drop them | Change a title or a date, or fill in a TODO |
| Write the summary from master-CV facts | Use the job's must-haves as claims |
| Keep the summary as specific as the bullets it draws on | Widen a fact in the summary ("a team's BigQuery bill" → "cloud costs"), add a derived number such as total years, or list a skill the bullets don't show the person using themselves |

Honour notes in the master CV, such as "(keep relative unless cleared)": use the relative wording, not the absolute figure, unless the person clears it for this application. Also follow the discretion rules in the person's context skill.

When a must-have is missing from the master CV, leave it out of the CV and tell the person. If they confirm they really have it, they add it to the master CV first, with an ID, and only then can the CV use it.

## Steps

1. **Target.** From `fit.md` and `jd.md`, list the must-haves, the 10–15 key terms the posting uses, and the angle.
2. **Select.** Pick 10–16 bullets, strongest-for-this-job first within each role. Recent roles get 3–6 bullets; roles older than ten years get 0–2.
3. **Write** `cv.md` from `assets/cv-template.md`. Use the posting's terms where they describe the same fact, and put the result first: "Cut the nightly reporting job from 40 minutes to 6 by …". End every bullet with its source IDs in a comment: `<!-- bc-2 -->`.
4. **Summary.** Two or three lines that lead with the angle and name the role the person is applying for. Every number must exist in the master CV.
5. **Check the claims.** Run `python3 scripts/check_claims.py cv.md <workspace>/profile/master-cv.md`. Fix every violation by changing the CV, never the check, until it prints `ok`.
6. **Render.** Run `python3 scripts/render_pdf.py cv.md cv.pdf`. Open the PDF and check it's at most two pages, nothing is cut off, and no `<!--` text is visible. If the employer asks for Word, make a .docx from `cv.md` with the docx skill if it's available.
7. **Log.** Add one line to the application log: which results lead and why, and which must-haves were left unclaimed.

## ATS rules

One column. Standard section names (Summary, Experience, Education, Skills). Real text, no images or text boxes. The same date format throughout. Name the file `firstname-lastname-cv.pdf` when sending. Keywords appear in the bullets, not stuffed into a hidden list.

## Output

`cv.md` (with its evidence comments) and `cv.pdf` in the application folder. In the reply, give three bullets on what the CV now emphasises, any must-have you left unclaimed and why, and the claim-check result.
