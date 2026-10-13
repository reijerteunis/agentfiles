---
name: nurture-sequence
description: Writes email sequences for people who opted in, such as welcome and download follow-ups, trial onboarding and win-back, with one goal per email, timing, stop rules and consent, as drafts. Use it when someone wants a welcome sequence, onboarding or drip emails, or follow-ups for a download or webinar. Not for cold outreach to people who haven't opted in (use outbound-sequence).
license: MIT
---

# Nurture sequence

People who gave you their email gave you permission to be useful, not to sell to them every day. A good sequence delivers what they signed up for, earns the next email, and makes one clear ask when they're ready.

## Before writing

Ask who signs up and from where (a download, a trial, the newsletter, an event), what they were promised, the one action the sequence leads to (activate, book a call, upgrade, reply), the email tool, and what the sign-up form said about consent. Read the messaging, the proof bank and the person's voice or context skill.

## Sequence types

| Type | Goal | Shape |
|---|---|---|
| Welcome or download follow-up | Deliver, then earn trust | Deliver now; a quick win on day 1–2; a story or case on day 4; the common mistake on day 7; a soft offer on day 10 |
| Trial onboarding | First value before the trial ends | Triggered by behaviour: not set up yet, a nudge with the one step; set up, the next feature; the day before it ends, a reminder and the offer |
| Newsletter to call | Readers into conversations | Regular value, plus a monthly invitation with a specific reason to talk |
| Win-back | Re-engage or clean the list | What's new; a reason to return; "should I stop emailing you?"; then remove the people who didn't respond |

## Each email

- One goal and one call to action.
- A subject line that says what's inside (no fake "Re:", no bait), and preview text that completes it.
- Short, in the person's voice, written to one reader.
- Proof IDs on every claim, checked with the `messaging` skill's proof check.
- The sender's identity, a working unsubscribe link and the company's address in the footer.

## Timing and logic

A table with each email's trigger or delay, the condition to skip it (they already did the action), its goal and its metric. The sequence stops when the reader does the action or replies.

## Rules

- Only people who opted in, and only for what they opted in to. A download covers the related emails you said you'd send, not unrelated promotions; if you plan those, say so on the form.
- Unsubscribes take effect at once, in every list and tool.
- Never add people who didn't opt in, such as bought lists, scraped addresses or event badge scans without consent.
- Measure replies, clicks and the action itself. Open rates are unreliable because mail apps load images to protect privacy.

## Output

`drafts/sequences/<slug>.md`: the logic table and every email (subject, preview text, body and call to action), ready to paste into the email tool. The person loads and activates it.
