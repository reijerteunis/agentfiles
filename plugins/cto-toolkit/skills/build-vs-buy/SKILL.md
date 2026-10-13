---
name: build-vs-buy
description: Writes a build-versus-buy memo comparing building, vendors, open source and hybrid on three-year cost of ownership, time to value, fit, risk, lock-in and exit cost, with a recommendation. Use it when a team asks whether to build or buy, compares vendors with an in-house build, or questions what a vendor costs.
license: MIT
---

# Build vs buy

Build what differentiates you; buy what doesn't, unless buying creates a dependency you can't afford. The memo makes that judgment explicit and puts numbers on it.

## Steps

1. **Requirements.** List the must-haves and should-haves, including the non-functional ones: scale, latency, data residency (GDPR), security certifications, integrations and SLAs.
2. **Core or context?** Does this capability make customers choose you (core), or does it just have to work (context)? Context strongly favours buying.
3. **Options:** build; buy (2–3 vendors that meet the must-haves); self-host open source; hybrid (buy now, build later).
4. **Three-year TCO** for each option. Show the formula and every assumption.
   - **Build:** engineering time × loaded cost, plus 15–25% a year for maintenance, plus infrastructure and on-call.
   - **Buy:** licences at the expected scale, plus integration, vendor management, and price increases.
   - **Open source:** hosting, upgrades, security patching, and the expertise you need.

   Use vendors' published prices with links, or mark a price as an estimate to confirm. Never invent one.
5. **Time to value:** when each option is in production, honestly estimated.
6. **Risk and lock-in:** vendor viability, data export and portability, security and compliance posture, roadmap control, and the **cost to exit** after three years.
7. **Recommendation:** the option, why, and what would change the answer (for example "if volume exceeds X, building wins").

## Output

`build-vs-buy-<slug>.md`: a one-paragraph recommendation, then the requirements, a comparison table (TCO, time to value, fit, risk, exit cost), the assumptions, and what would change the decision. If the decision is a one-way door, hand it to `adr-writer`. Have the `skeptical-cfo` agent challenge the cost assumptions if it's available.
