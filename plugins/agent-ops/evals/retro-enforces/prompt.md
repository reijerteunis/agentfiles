---
description: A repeated violation gets an enforcement-layer fix and a test, not another instruction.
tags: [agent-retro, guardrail-design]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

My coding agent keeps committing .env files, even though our AGENTS.md clearly says never to commit secrets. Fix this properly. You don't have access to the repo, so give me the changes here.
