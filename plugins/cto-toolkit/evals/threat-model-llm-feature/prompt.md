---
description: A security review of an LLM feature triggers threat-model and covers prompt injection.
tags: [threat-model]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

Threat model our new feature: customers upload supplier invoices (PDF), an LLM extracts the bank details and amounts, and our system then schedules the payment.
