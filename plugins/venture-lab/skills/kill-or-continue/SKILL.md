---
name: kill-or-continue
description: Runs the gate decision for an idea (continue, pivot, park or kill) against the criteria set before the evidence came in, separating evidence from opinion and logging any override. Use it when an experiment ends, or someone asks whether to keep going or pivot. Not for general decisions (use decision-memo).
license: MIT
---

# Kill or continue

Ideas rarely die of one bad result. They die slowly from never being judged. The gate makes the call on time, against the criteria the founder set when they were still objective.

## Inputs

`idea.md`, `assumptions.md`, the experiments (thresholds and results), the interview synthesis, the market and model files, and the kill criteria in `profile/criteria.md` and in each experiment.

## Steps

1. **Criteria first.** Restate the success and kill criteria that were set *before* the evidence. If none were set, say so: the decision will be weaker, and the next gate needs criteria written down now.
2. **Evidence table:** for each key assumption, the status (supported, contradicted or unknown) and the strongest piece of evidence. Rank evidence by strength: money, then signatures, then time commitments, then behaviour, then opinions.
3. **Steelman both sides:** the strongest honest case for continuing, and for stopping.
4. **Bias check:** sunk cost ("we've put in three months"), falling in love with the solution, moving the goalposts, cherry-picking the one enthusiastic interview.
5. **Decide,** following the criteria:
   - **Continue:** criteria met. Name the next riskiest assumption and its test.
   - **Pivot:** the evidence points to a different customer, problem or model that's stronger than the original. Name it, and send the idea back to Explore.
   - **Park:** promising, but not now (timing, the founder's capacity). Record what would reopen it.
   - **Kill:** the criteria missed or a deal-breaker hit. Record the lesson.
6. **Override rule:** if the founder chooses differently from what the criteria say, log it explicitly as an override, with the reason. Overrides are allowed; silent ones aren't.

## Output

Append to `decisions.md`: the date, the decision, the criteria against the evidence, the overrides, what would change the answer, and the lesson. Update the `idea.md` stage and status. A kill gets one sentence of acknowledgement: three weeks to learn an idea won't work is a win, and the founder's time just got freed up for the next one.
