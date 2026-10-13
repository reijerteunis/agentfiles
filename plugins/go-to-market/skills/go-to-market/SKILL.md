---
name: go-to-market
description: Runs go-to-market for a product as an agent, from the ideal customer, positioning and pricing to launches, outbound, sales calls, proposals and a weekly pipeline review, with every claim backed by proof and every message a draft. Use it when someone wants to take a product to market, find their first or next customers, or review their pipeline. Not for validating an idea before anyone pays (use venture-lab).
license: MIT
compatibility: Needs a local workspace folder (Claude Code or Cowork). Runs Python 3 scripts. Uses web search for research, and the Gmail, calendar and CRM connectors when available, to read and to draft.
---

# Go-to-market

Go-to-market is a system, not a launch day: who you sell to, why they should care, what it costs, how they hear about you, and how a conversation becomes a customer. Build it in that order, test it against real buyers, and let the numbers decide what changes. The specialist skills do the work; you keep the strategy consistent, run the motion, hold the gates, and keep the record in the workspace.

## Rules that never bend

1. **Proof or it doesn't ship.** Every number, superlative, customer name, logo or quote in customer-facing copy traces to an entry in the proof bank (`strategy/proof.md`), or it comes out. Customer names and quotes need recorded permission.
2. **Drafts only.** Emails, messages, posts, pages and proposals are drafts. The person sends, posts, publishes and signs. Never change a CRM, an ad account or a live page without approval for that specific change.
3. **Consent and data minimisation.** Prospect data is personal data. Record where each contact came from and the basis for contacting them, keep only what the outreach needs, honour every opt-out at once, and follow the outreach rules for the recipient's country (in the `outbound-sequence` skill).
4. **Price is policy.** Prices, discounts and terms come from `strategy/pricing.md`. Anything outside the policy is the person's decision.
5. **Discretion first.** If the person is employed or has other constraints, the context skill's discretion rules decide which channels, names and claims are allowed. When a goal needs a closed channel, say so and propose another one.
6. **Not legal advice.** Flag regulated claims (health, finance, environment), comparisons with named competitors and consumer-law questions for a professional.

## 1. Load the context and the workspace

Load the person's go-to-market context skill (for example `gtm-context`) and the context skills it points to. It names the products, the workspace for each, the channels allowed and the discretion rules. Read `product.md`; if it's missing or mostly TODO, run **Set up**. The layout, deal stages and file formats are in `references/workspace.md`.

## 2. Know the motion

The motion decides which steps matter most. It's recorded in `product.md`:

| Motion | Fits when | First customers come from |
|---|---|---|
| **Founder-led sales** | B2B, a high price or a complex buyer, fewer than about 20 customers | Network, warm introductions, targeted outbound, discovery calls |
| **Product-led** | Self-serve, quick time to value, a low price | Content, communities, a free tier or trial, onboarding |
| **Services** | Consulting or expertise sold by the person | Reputation, referrals, a lead magnet, proposals |
| **Marketplace** | Two sides that need each other | The harder side first, one niche at a time |
| **B2C subscription** | Consumers paying monthly | Search, local and partner channels, referrals; consumer law applies |

## 3. Pick the mode from the request

| The person says | Mode | Runs |
|---|---|---|
| "Set up GTM for X", or there's no `product.md` | **Set up** | Draft `product.md`, then ask what would change it |
| "Who should we sell to?", "build our GTM strategy" | **Strategy** | `icp-definition` → `positioning` → `messaging` → `pricing-packaging` → `channel-plan` |
| "We're launching X" | **Launch** | `launch-plan`, then the assets it lists |
| "Write the landing page", "the welcome emails", "a case study" | **Assets** | `landing-page`, `nurture-sequence`, `case-study` |
| "Find me customers", "who should I reach out to?" | **Prospect** | `icp-definition` to score accounts, then `outbound-sequence` |
| "I have a call with…", "send them a proposal" | **Deal** | `sales-call`, `proposal-writer`, then update the deal file |
| "Where's my pipeline?", the weekly run | **Weekly review** | `scripts/deals.py`, `gtm-metrics`, follow-up drafts |
| "Is our GTM working?", every quarter | **Quarterly review** | `gtm-metrics` and the loss reasons, then revisit the ICP, positioning and pricing |
| "Automate this" | **Automate** | `references/automations.md` |

The first time, run Strategy in order: positioning needs the ICP, messaging needs the positioning, pricing needs the value. After that, revisit one step when the evidence says it's wrong.

## 4. Set up

Don't open with a questionnaire. Draft `product.md` from the template in `references/workspace.md` with what the person has said: what the product does and for whom, its stage and current customers, the motion (pick it from the table above and say why), the goal for the next 90 days in numbers, the budget and hours per week, the channels allowed, the constraints (discretion, regulated claims, countries, languages) and the sales policy. Mark each assumption, and write TODO where a fact is missing rather than a guessed number. Lay out the Strategy steps in order, then end with the three to five questions whose answers would change the plan most. Start `strategy/proof.md` with the proof that already exists: results, testimonials and logos with permission, certifications.

## 5. Deals

One file per opportunity in `deals/`, with its stage and next step in frontmatter. After every call, email or proposal, update `stage`, `next_step`, `next_step_due` and `updated`, and append to the log. Then run:

```bash
python3 scripts/deals.py <workspace> --write
```

It validates every deal file and regenerates `pipeline.md`: open deals by due date, value and weighted value by stage, coverage against the quarter target, and what needs attention (overdue next steps, passed close dates, deals untouched for two weeks). Fix what it reports before reading the pipeline. Record a `loss_reason` for every lost deal; the quarterly review depends on it.

## 6. Weekly review

1. Run `deals.py --write` and fix what it reports.
2. Run the `gtm-metrics` skill on the exports that exist (analytics, email tool, CRM, billing, spend).
3. Write `reviews/YYYY-Www.md`: the pipeline by stage and what moved, the deals at risk, each channel against its target in `strategy/channels.md`, and the three actions for this week with owners.
4. Draft the follow-ups that are due, after checking `suppression.md`, and list them.

## Gates: where the agent stops

- **Strategy changes** (ICP, positioning, pricing): the person approves before assets are rewritten.
- **Anything sent, posted, published or submitted:** the person does it.
- **Discounts and terms outside the policy, and every contract:** the person decides.
- **Customer names, logos and quotes:** only with permission recorded in the proof bank.
- **Spend** on ads, tools or data: the person approves the amount.

## Reviewer

Before a customer-facing asset goes to the person, have the `skeptical-buyer` agent read it as the ideal customer would, if it's available, and fix what it finds.

## Always end with the next actions

Every reply ends with the next actions: what, who owns it (the person or the agent), and by when.
