---
type: llm
---

PASS if the threat model treats the uploaded PDF as untrusted input (hidden instructions, altered figures or a forged invoice), recognises that the model can extract a fraudster's bank details perfectly and the money still goes to the wrong account, and puts a check outside the model before any payment is scheduled: the extracted account is compared with the supplier's verified account on file, and a new or changed account is confirmed through a channel the invoice doesn't control, such as a call to a known contact, and approved by a person.
FAIL if its main protection against a diverted payment is the model itself (prompt instructions, input filtering or a second model checking the first), or if it lets the system schedule a payment to bank details nobody has verified.
