---
name: decision-memo
description: Turns a hard personal or business decision into a one-page memo with the options (including doing nothing), weighted criteria, risks, a pre-mortem and a recommendation. Use it when someone is torn between options, or asks "should I…?" about a big choice. Not for technical architecture decisions (use adr-writer) or job offers (use offer-negotiation).
license: MIT
---

# Decision memo

Most hard decisions are hard because the question is fuzzy, the criteria are unspoken, or one option is a hidden "do nothing". The memo makes all three explicit and fits on a page.

## Steps

1. **The real question:** restate it in one sentence, including the deadline. "Do I accept the board seat at X, which starts in January?" Ask until it's sharp.
2. **Reversibility:** a two-way door gets a fast decision with a one-paragraph memo. A one-way door gets the full page.
3. **Options:** 2–4 real options, plus **do nothing or decide later**, with what each really means in practice.
4. **Criteria:** 3–6 things that matter, weighted by the person ("time with family 30%, learning 25%, money 20%…"). If they haven't given weights, propose weights from what they've told you, mark them as assumed, and ask them to correct them at the end. Don't hold the memo back to wait for weights.
5. **Score** each option on each criterion from 1 to 5, with a line of evidence. Show the weighted totals, but treat them as a conversation starter, not the answer.
6. **Risks:** what could go wrong with each option, its likelihood, and the cost to reverse.
7. **Pre-mortem** on the favourite: "It's a year later and this was a mistake. Why?" The two most plausible stories, and what would guard against them.
8. **Recommendation:** the option, in one paragraph on why, and the signals that would change the answer.

## Output

Write the whole memo in the first reply, including the pre-mortem and a recommendation, even when facts are missing: mark each gap as an assumption, say which ones would flip the recommendation, and end with at most five questions. Never answer a "should I…?" with only questions.

`decisions/YYYY-MM-DD-<slug>.md`: the question, the options, a criteria table with weights and scores, the risks, the pre-mortem, the recommendation and the decide-by date. The person decides; record what they decided and why. A short note on the reasoning is worth more than the scores.

For major money, legal or health decisions, say that the memo organises the thinking and that a professional (an accountant, lawyer or doctor) should check the specifics.
