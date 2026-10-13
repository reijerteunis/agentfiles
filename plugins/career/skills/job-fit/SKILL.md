---
name: job-fit
description: Decides whether a job is worth applying for, mapping each requirement to evidence, naming gaps and red flags, and giving a scored Go, Maybe or No-go with the winning angle. Use it when someone shares a posting and asks whether it fits or whether to apply. Not for writing a job posting for your own team (use job-description-writer).
license: MIT
---

# Job fit

Give an honest verdict before anyone spends an evening on an application. A good fit analysis is specific: it quotes the posting, cites the person's own evidence, and says no when the answer is no.

## Inputs

The posting (`jd.md`, or pasted text), `profile/master-cv.md` and `profile/preferences.md`. Without a master CV, work from the CV or profile the person gives you, and say that the verdict is provisional.

## Analysis

1. **Requirements.** Split the posting into must-haves (at most seven, read past the boilerplate to the real ones) and nice-to-haves. Note the hidden requirements a careful reader can infer: team size, stage, travel, on-call, and the reporting line.
2. **Evidence.** For each requirement, cite the master-CV IDs that prove it, and rate the match strong, partial or none. Never stretch evidence: "managed a team of 8" doesn't prove "led 50+ engineers".
3. **Gaps.** For each partial or missing requirement, say whether it's real or just wording. Say how an honest application would handle it: an adjacent strength, a learning story, or plainly not claiming it.
4. **Preferences.** Check role, company, location, compensation (if posted), timing and every deal-breaker. A deal-breaker or a never-contact company means No-go, whatever the score.
5. **Red flags.** A title inflated beyond the scope, a vague mandate, signs of high turnover, a "rockstar" laundry list, a salary below the floor, or an unclear reporting line. Quote the line that raised each one.
6. **The angle.** The single story or result from the master CV that makes this person the obvious hire for *this* job. The cover letter, CV summary and outreach all build on it.

## Score

| Part | Weight | How |
|---|---|---|
| Must-haves covered | 50 | strong = full points, partial = half, none = 0 |
| Preferences matched | 30 | role, company, location, money, timing |
| Upside | 20 | growth, mission, team, what the person said excites them |

Subtract up to 20 for red flags. **Go** at 70 or more, **Maybe** from 55 to 69, **No-go** below 55 or on any deal-breaker.

## Output

Write `fit.md`:

```markdown
# Fit: <role> at <company>

**Verdict: Go | Maybe | No-go (score/100)**: one sentence on why.
**The angle:** …

## Requirements
| Requirement | Must/Nice | Evidence | Match |
|---|---|---|---|

## Gaps and how to handle them
## Red flags
## Preferences check
```

In the reply, give the verdict, the angle and the top two reasons in three lines, then the file path.
