---
description: An instructions audit catches a contradiction and moves procedures and must-hold rules to the right layer.
tags: [agent-instructions]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Review our AGENTS.md:

- Always use npm for installs.
- We use pnpm; never run npm install.
- To deploy: 1) bump the version 2) build the Docker image 3) push to the registry 4) update the Helm chart 5) run the smoke tests 6) post in #releases.
- Never push to main.
- Write clean, high-quality code.
