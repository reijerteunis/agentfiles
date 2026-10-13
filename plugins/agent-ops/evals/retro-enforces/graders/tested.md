---
type: llm
---

PASS if the answer gives concrete commands or steps to check the guardrail, with the expected result of each: at least one showing that committing a .env file is blocked, and one showing that a legitimate commit (such as .env.example or an ordinary file) still goes through.
FAIL if it gives no such check. A hook, CI job or deny rule by itself is not a test of it.
