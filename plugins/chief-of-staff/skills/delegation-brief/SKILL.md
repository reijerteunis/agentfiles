---
name: delegation-brief
description: Writes a delegation brief with the outcome, the definition of done, context, decision rights and check-ins, and records the hand-off. Use it when someone wants to delegate or hand off a task to a colleague, an assistant or an agent. For splitting coding work across parallel agents, use parallel-agents.
license: MIT
---

# Delegation brief

Delegation fails on missing context, not on missing talent. A good brief transfers the outcome and the judgment, not just the task, so the work comes back done rather than half-done with questions.

## Steps

1. **Outcome:** what will be true when this is done, and why it matters. One or two sentences.
2. **Definition of done:** a checkable list. "A shortlist of 3 vendors with pricing, in the shared folder."
3. **Context:** the background they can't know (history, people, sensitivities, what's been tried) and the links they need.
4. **Constraints:** the deadline, the budget, the tools or vendors to use or avoid, the quality bar.
5. **Decision rights:**
   - **Decide alone:** …
   - **Decide and inform me:** …
   - **Ask me first:** … (money above X, anything external, anything irreversible)
6. **Resources and contacts:** who can help with what.
7. **Check-ins:** when, and in what form ("a 2-line update every Friday; call me if you're blocked for more than a day").

Size it to the task. A one-hour task gets three lines; a project gets a page.

## Output

`delegations/YYYY-MM-DD-<slug>.md`, plus a ready-to-send version of the brief (an email or chat message, as a draft) for the person to send. Record the hand-off in `follow-ups.md` as `owed to me`, with the due date and the check-in dates.

When the delegate is an AI agent, write the same brief as its prompt, and put every external or irreversible action under "Ask me first".
