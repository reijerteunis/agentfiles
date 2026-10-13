---
name: email-reply
description: Drafts an email reply in the person's voice that leads with the answer, stays short and flags what it commits them to, saved as a draft only. Use it when someone asks to reply to or answer an email, or to say yes, no or not now politely. Not for job-search messages (use outreach-message).
license: MIT
compatibility: Uses the Gmail connector to read the thread and create the draft; otherwise drafts in the chat.
---

# Email reply

A good reply is shorter than the email it answers, says the decision in the first line, and sounds like the person on a good day.

## Before drafting

1. Read the **whole thread**, not just the last message: who's on it, what's been agreed, and what's actually being asked.
2. Load the person's voice from their context skill. Match the thread's language (reply in Dutch to Dutch) and its formality.
3. If the reply needs a decision the person hasn't made, such as a date, a price or a yes or no, ask first, or draft two short alternatives and let them pick.

## Write

- **First line:** the answer or the decision. "Yes, Thursday 14:00 works." "I'll pass on this one."
- **Then** only what the other person needs to act: the details, the next step, the owner and the date.
- **Length:** most replies are 2–6 lines. Use more only if the question really needs it.
- **No-filler rule:** no "I hope this email finds you well", no "Please don't hesitate to reach out", no restating their email.
- Saying no: be kind, clear and brief. Give a reason only if it helps the relationship, and offer an alternative only if the person wants one.
- Keep the recipients the thread needs. Point out when someone should be removed or added, but don't change it yourself.

## Commitments check

Before saving, list everything the draft commits the person to: deadlines, deliverables, money, meetings, confidential information. Each one goes into `follow-ups.md` as `I owe` once the person sends it. If the draft promises something the person didn't confirm, rewrite it as a question to them instead.

## Output

Save it as a Gmail draft in the thread when the connector is available; otherwise show it in the chat. Say plainly that it's a draft and hasn't been sent. Give the draft, then the commitments line: "Commits you to: sending the deck by Friday."
