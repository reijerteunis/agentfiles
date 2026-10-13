---
name: tech-debt-register
description: Builds a tech debt register from code hotspots, incidents and team pain, with the interest and principal of each item, priorities, and a paydown plan with a capacity budget. Use it when someone asks what their tech debt is, what to fix first, or how to justify refactoring time to the business.
license: MIT
---

# Tech debt register

Debt isn't bad; unmanaged debt is. The register makes debt visible in the language the business understands: what it costs every sprint, what it costs to fix, and what happens if you wait.

## Find it

1. **Hotspots:** the files that change most often and are hardest to change. Change frequency over six months:

   ```bash
   git log --since=6.months --name-only --format= | grep -v '^$' | sort | uniq -c | sort -rn | head -30
   ```

   Cross that with size or complexity. A hotspot that's also complex is where debt costs real time.
2. **Incidents and postmortems:** recurring contributing factors.
3. **Slowness:** areas where changes take longest or need the most rework (the PR lead time and review rounds from `engineering-metrics`).
4. **People:** ask the team what slows them down most, ideally in a short survey: "if you could fix one thing…".
5. **Decisions:** consequences recorded in ADRs ("harder: …") and known shortcuts.

## Describe each item

| Field | Meaning |
|---|---|
| Debt | What it is, where it lives (paths, systems) |
| Type | Deliberate or accidental × prudent or reckless |
| Interest | The ongoing cost: hours per sprint, incidents, slower onboarding, security exposure |
| Principal | The effort to fix, as a range |
| Cost of delay | What gets worse if we wait (it grows, blocks a roadmap item, a deadline) |
| Owner | The team that would fix it |

## Prioritise and plan

- Rank by **interest ÷ principal**, then move cost-of-delay items up.
- **Capacity:** reserve a share of every sprint (typically 15–20%) for the top of the register, plus a scheduled slot for the one or two big items per quarter.
- Use the boy-scout rule for small items: fix it when you touch it.
- Business framing: "This costs about X engineer-days a month and caused N incidents; fixing it takes Y days and pays back in Z months."
- Use only the numbers the person gave or the data shows. Where you illustrate a row or a calculation, use placeholders (X days, N PRs), not made-up figures: example numbers tend to end up in the real document.

## Output

`registers/tech-debt.md` with one row per item, sorted by priority. Then a summary for the quarter plan: the total interest, the top five items with their payback, and the capacity requested. Review it monthly; close items with a date, and record what the fix actually cost.
