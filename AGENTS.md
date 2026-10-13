# Working in agentfiles

This repo is my AI agent setup: skills in `plugins/`, global instructions and settings in `global/`, plus the installer and its tooling. It is public. `docs/architecture.md` explains how the pieces fit together.

## Commands

- `just validate`: run before every commit. It must pass.
- `just catalog`: run after adding, renaming or re-describing a skill.
- `just new <plugin> <skill>`: scaffold a skill.
- `just try <plugin>`: open Claude Code with the local plugin loaded.
- `just eval <plugin>`: behavior tests. These are real model calls that cost usage, so ask before running them.
- `./install.sh --dry-run`: preview what the installer would change on this machine.

## Rules

- Every skill change follows `docs/writing-skills.md`: the six spec frontmatter keys only, a description that works as a trigger, under 500 lines, a self-contained folder, and evals.
- **This repo is public.** Never add company or client specifics, personal facts, internal identifiers or URLs, or secrets. Those go in a context skill in the private companion (`../agentfiles-private`).
- Never copy a third-party skill into this repo (see `docs/third-party.md`).
- `global/AGENTS.md` loads into every session of every tool. Keep it under 6,000 characters, and change it only when asked.
- Plugins have no `version` field on purpose, so installs track commits. Don't add one.
- When behavior changes, update `README.md`, `docs/` and `CHANGELOG.md` in the same change.
