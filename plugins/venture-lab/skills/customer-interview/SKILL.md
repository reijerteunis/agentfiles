---
name: customer-interview
description: Runs Mom Test problem discovery, from recruiting and past-behaviour interview guides to capturing each interview and synthesising across them by commitments. Use it when someone wants to talk to potential customers, validate a problem or write interview questions. Not for sales calls (use sales-call) or job interviews (use interview-prep).
license: MIT
---

# Customer interview

People lie to be nice about your idea, but they don't lie about what they did last Tuesday. Ask about their life and their past behaviour, never about your idea. Compliments are noise; commitments are signal.

## Recruit

- Target the specific customer from the idea card. Five to ten conversations per segment are enough to see patterns.
- Find people through the founder's network, communities, LinkedIn searches, and second-degree introductions. Never approach the founder's employer's customers, partners or colleagues; follow the founder's discretion rules.
- Draft the outreach, as drafts only: short, honest, about learning ("I'm researching how small accounting firms handle supplier invoices; 20 minutes, no pitch"). Never claim a product exists when it doesn't.

## The guide

Write a 20-minute guide with 6–8 questions from `references/question-bank.md`, in this order:

1. Their context and role.
2. The last time the problem happened: walk through it step by step.
3. What they did about it, and what it cost (time, money, risk).
4. What they've tried or bought already, and why that didn't fully work.
5. How they decide about tools or services like this, and who has the budget.
6. Whether it's even a priority this quarter, compared with everything else.
7. Who else to talk to (the introduction ask).

**Never ask:** "Would you use…?", "Would you pay…?", "Do you think this is a good idea?" Don't pitch until the very end, if at all.

## Capture each interview

Write `interviews/YYYY-MM-DD-<who>.md`:
- who they are (role and segment, no unnecessary personal data)
- facts about past behaviour
- pains, ranked by intensity
- current workarounds and spend
- buyer and budget
- quotes (verbatim, short)
- commitments offered: time, an introduction, a pilot, money
- surprises

## Synthesise, after every 3–5 interviews

- **Patterns:** pains mentioned by most interviewees without prompting, and how often and how intense each is.
- **Willingness to pay:** evidence of money already spent on workarounds or tools. Opinions don't count.
- **Commitments:** count them. Zero commitments after 8 conversations is a strong signal.
- **Assumptions:** mark each one supported, contradicted or still unknown, citing the interviews. Update `assumptions.md`.
- **Surprises and pivots:** problems that came up which are bigger than the one assumed.
