# Security

## Reporting

Found a vulnerability, or a secret that slipped into this repo? Don't open a public issue. Report it privately through GitHub's **Report a vulnerability** button on the Security tab.

## Before you install skills from anywhere, including here

Skills and hooks run with your agent's permissions. Published skills have been found with prompt injection, backdoors and `curl | bash` payloads. So:

- Read every `SKILL.md`, script and hook before you install it. This repo keeps them short so that's practical.
- Pin third-party marketplaces to a commit (`#<sha>`) instead of following a branch.
- Keep secrets out of reach of your agents. `global/claude/settings.json` shows the deny rules used here.

## What this repo does to stay clean

- CI scans the full history for secrets with gitleaks on every push and daily.
- GitHub Actions are pinned to commit SHAs and run with read-only tokens.
- Skills are validated against the Agent Skills spec, may not contain absolute home paths, and company context never enters this repo: it lives in a private companion.
