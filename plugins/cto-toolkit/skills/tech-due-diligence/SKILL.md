---
name: tech-due-diligence
description: Runs technical due diligence on a company's technology and team, or prepares a company for one, with findings by severity, red flags and a 100-day plan. Use it when someone evaluates a company to invest in or acquire, receives a due diligence questionnaire, or prepares a data room.
license: MIT
---

# Tech due diligence

Answer one question with evidence: can this technology and this team deliver the business plan, at what cost, and with what risks? Use `references/checklist.md` as the question list.

## Mode A: assessing a target

1. **Scope** with the deal team: the thesis, what would kill the deal, the time box, and what access you get (data room, repos, interviews).
2. **Request** the checklist items early; missing answers are findings in themselves.
3. **Review the evidence:**
   - **Architecture:** a walkthrough with the CTO, and the diagrams checked against the code.
   - **Code:** sample 2–3 core repos. Look at structure, tests, CI, dependency health, how secrets are handled, recent activity and the bus factor (`git shortlog -sn`).
   - **Security and compliance:** pen-test reports, incident history, certifications, GDPR records, and AI Act exposure (use `ai-act-assessment` for AI-heavy targets).
   - **Infrastructure and cost:** cost trends and unit economics (use `cloud-cost-review`).
   - **Delivery:** deployment frequency and quality metrics, if they can be shared.
   - **Team:** structure, seniority, attrition, key people and their retention, hiring.
   - **Intellectual property and licences:** ownership of code and contractors' IP assignment, open-source licences (copyleft in distributed products), and third-party dependencies.
4. **Findings** by severity:
   - **Red flag:** threatens the thesis or the valuation.
   - **Major:** needs a plan or a price adjustment.
   - **Minor.**
   - **Strength.**

   Each finding gives its evidence and the estimated cost to fix.
5. **Report:**
   - a one-page executive summary with the verdict and the top 5 findings,
   - the detailed findings,
   - the cost to remediate,
   - a 100-day plan after closing.

## Mode B: preparing your own company

Walk through the checklist as if you were the investor. For each item, prepare the evidence in a data-room folder, write a short, honest answer, and fix the cheap gaps before the process starts. Never hide a known problem: it surfaces later, at a worse price.

## Rules

- Evidence over claims: every finding cites a document, a code location or an interview.
- Everything you see is confidential under the NDA. It stays in the deal workspace, never in personal notes or public tools.
- Don't execute anything in the target's environments; read-only access only.
