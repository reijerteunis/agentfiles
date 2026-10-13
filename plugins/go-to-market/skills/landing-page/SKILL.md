---
name: landing-page
description: Writes conversion copy for a landing page, homepage or pricing page aimed at one audience and one action, with proof from the proof bank, objection answers, search and accessibility basics, and one test to run. Use it when someone wants a landing page, homepage or sign-up page written or improved, or asks why their page doesn't convert. Not for blog posts or articles.
license: MIT
---

# Landing page

A landing page has one audience and one job: get the right visitor to take one action. Everything on it either moves that visitor toward the action or comes off.

## Before writing

Read `strategy/positioning.md`, `strategy/messaging.md` and `strategy/proof.md`. Ask for the audience (one persona or segment), where the traffic comes from (search, an ad, a post, an email, outbound), the one action (sign up, book a call, start a trial, download) and what visitors already know when they arrive.

## Structure

1. **Hero:** a headline with the outcome for this audience (not the category, not a slogan), a subheadline that says how, one call to action, and an image of the product or the result. It passes the five-second test: who is it for, what does it do, why should I care.
2. **The problem** in the customer's words, and what the alternatives cost them.
3. **How it works:** three steps or the three pillars, concretely.
4. **Proof:** numbers, a customer story, quotes and logos with permission, certifications. Everything from the proof bank.
5. **Objections:** the real ones from calls (price, effort to switch, data, lock-in, "we tried this before"), answered plainly. An FAQ works.
6. **Offer and call to action:** what they get, what it costs or that it's free, what happens next, and only the guarantees you'll honour.
7. **Footer:** the company's identity and contact details, the privacy notice and the terms.

Match the page to the traffic: an ad that promises a checkout audit lands on that promise, not on the homepage.

## Basics that cost nothing

- **Search:** one main query per page, a title of about 60 characters and a meta description of about 155 written to be clicked, one H1, a descriptive URL, a fast page.
- **AI assistants:** answer the core questions plainly in the text, add structured data (Organization, Product, FAQ) where it's true, and keep facts identical wherever they appear.
- **Accessibility:** headings in order, alt text, enough contrast, labelled form fields, buttons that say what they do ("Book a 20-minute call", not "Submit").
- **Forms:** ask only what's needed. Marketing consent is a separate, unticked checkbox with a link to the privacy notice.
- **Tracking:** one conversion event, UTM sources, and no non-essential cookies before consent where the law requires it.

## Check before delivering

1. Run the `messaging` skill's proof check (`proof_check.py` with the proof bank) on the copy and fix every flag. When it can't run, check by hand: every number, comparison (faster, cheaper, more accurate) and promise of time saved, including in the title and meta description, has a proof ID or a [to verify] marker; without proof, say what the product does instead. Sample data in screenshots and alt text is labelled as an example.
2. Read it as the visitor: does the hero pass the five-second test, and is there one main action?
3. If it's available, have the `skeptical-buyer` agent review it.

## One test

Propose the test with the most leverage (usually the headline or the offer), its metric and the sample it needs. With little traffic, test big differences only, or show the page to five people from the ICP instead.

## Output

`drafts/pages/<slug>.md`: the copy section by section (a version with proof IDs for review and a clean one), the title and meta description, alt texts, structured data suggestions, the form fields and the test. Publishing is the person's call.
