---
description: A parallel plan sequences the shared dependency first and isolates the rest.
tags: [parallel-agents]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I have four tickets for this week: add OAuth login, refactor the payments module, add a dark mode toggle, and change the users table schema (both OAuth and payments depend on that change). Set them up for parallel coding agents.
