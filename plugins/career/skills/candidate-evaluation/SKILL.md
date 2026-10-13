---
name: candidate-evaluation
description: Turns interview notes and scorecards into an evidence-based hiring recommendation, with a bias check and reference questions, while the hiring manager decides. Use it after interviews, when someone shares feedback or asks whether to hire a candidate. This is the hiring side; to judge your own fit for a job, use job-fit.
license: MIT
---

# Candidate evaluation

Make the decision on evidence, not on the loudest voice in the debrief. Every rating points at something the candidate actually said or did.

**The hiring manager decides.** In the EU, AI used to evaluate candidates is a high-risk use under the AI Act (Annex III, employment). This skill structures the evidence for a human decision. It never replaces that decision, and the evidence trail is kept. For the company's obligations, use `ai-act-assessment`.

## Inputs

The interview loop (`interview-loop.md`, with its competencies and rubrics), each interviewer's notes or scorecard, the CV, and any work sample. If there's no rubric, derive competencies from the job description, and flag that the evaluation is less reliable.

## Steps

1. **Evidence per competency.** Collect the strongest evidence for and against from all notes, quoted or closely paraphrased, with the interviewer and stage.
2. **Score** each competency 1–4 against the rubric. Mark "no evidence" separately from a low score: a gap in the loop isn't a weakness of the candidate.
3. **Consistency.** Where interviewers disagree, find out why: a different question, a different bar, or a different signal. Say which view the evidence supports.
4. **Bias check.** Look for:
   - halo effect (one strong area inflating the others)
   - similarity ("reminds me of me")
   - contrast with the previous candidate
   - judgments on style, accent, age, gender, background, or where someone went to school
   - "culture fit" used as a reason without evidence

   Remove anything that isn't job-related evidence.
5. **Risks and references.** List what's uncertain and how to test it: reference-check questions, a follow-up conversation, or a trial project.
6. **Recommendation:** strong hire, hire, no hire, or strong no hire, with the 3 decisive reasons. A must-have scored 1 is a no hire, regardless of the rest.

## Output

Write `evaluation-<candidate>.md`: a competency table (score, evidence, interviewer), disagreements and how they resolve, the bias notes, the risks with reference questions, and a recommendation memo of under 200 words. Never infer or record protected characteristics. If the notes contain such remarks, flag them for the hiring manager instead of repeating them.
