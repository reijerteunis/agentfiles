---
description: An incident write-up request triggers incident-postmortem and stays blameless.
tags: [incident-postmortem]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

Write the postmortem for yesterday. Timeline (UTC): 14:02 Mark deployed a config change that set the payment provider timeout to 1s. 14:05 checkout errors spiked to 30%. 14:19 support escalated. 14:31 we rolled back the config. 14:36 errors back to normal. There was no canary for config changes and no alert on checkout error rate.
