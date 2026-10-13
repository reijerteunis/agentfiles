---
name: library-audit
description: Audits a skill library so agents keep picking the right skill. A script measures descriptions against the listing budget, eval coverage and look-alike pairs without routing lines, then it proposes what to prune, merge and fix. Use it when someone has many skills, says an agent picks the wrong skill or ignores one, or wants their skills reviewed or cleaned up.
license: MIT
compatibility: Runs a Python 3 script on a skills repository with a .claude-plugin/marketplace.json.
---

# Library audit

Skill selection gets worse as a library grows. Look-alikes compete, long descriptions crowd each other out of the listing, and untested skills drift. An audit keeps the library sharp.

## Measure

```bash
python3 scripts/library_stats.py <repo>
```

It reports:
- per plugin: the number of skills, the description characters, and the skills without an eval case,
- the whole catalog against the listing budget (about 1% of the context window),
- pairs of skills whose descriptions overlap strongly with no routing line between them.

Also run `/skill-doctor` in Claude Code, if available, for usage: skills never invoked in recent weeks.

## Judge

| Finding | Fix |
|---|---|
| Over budget | Shorten descriptions to what plus when plus routing (aim for 300–500 characters), and enable plugins as packs instead of everything at once |
| A look-alike pair | Add routing lines to both ("Not for … (use X)"), or merge them if they really do the same job |
| No evals | One trigger case and one near-miss with `eval-writer` |
| Never used | Ask whether it's still needed: delete it, or fix its description if it should have triggered |
| A third-party skill overlapping an own skill | Turn one off |
| A skill over 500 lines | Move detail into `references/` |

## Output

Write `audits/YYYY-MM-DD-library.md` in the agent-ops workspace: the stats table, the findings, and a ranked fix plan with an owner and an effort for each. Apply fixes only after the person agrees. Every change goes through the repository's validation, and the evals of the skills touched.
