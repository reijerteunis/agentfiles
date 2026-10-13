---
name: ai-act-assessment
description: Assesses an AI system against the EU AI Act, covering scope, role, prohibited practices, high-risk classification, transparency and general-purpose AI duties, with dated obligations and an evidence plan. Use it when someone asks what the AI Act means for a product or tool, whether a system is high-risk, or what to do by when. Not for technical security threats (use threat-model).
license: MIT
---

# AI Act assessment

Turn "does the AI Act apply to us?" into a reasoned classification, a dated list of obligations, and a plan to produce the evidence as you go.

This is an orientation, not legal advice. Cite the article for every conclusion, and recommend legal review for anything borderline or high-risk.

**Dates moved in 2026.** Before stating any deadline, read `references/timeline.md`, which is dated, and check it against the official text on EUR-Lex when the assessment drives real decisions. Never quote a deadline from memory.

## Steps

1. **Describe the system:**
   - what it does and the decisions or outputs it influences
   - who uses it and who is affected
   - the model or models (own, fine-tuned, a third-party API)
   - where it's offered or used (in the EU, or affecting people in the EU)
2. **Is it an AI system?** Apply the definition in Article 3(1). Fixed rule-based software usually isn't. Record your reasoning.
3. **Role, under Article 3 and Article 25:**
   - **Provider:** develops it, or has it developed, and places it on the market under its own name.
   - **Deployer:** uses it under its own authority.
   - **Importer** or **distributor:** brings it onto the EU market or passes it on.

   A deployer becomes a provider by putting its name on a high-risk system, substantially modifying one, or changing its intended purpose so that it becomes high-risk.
4. **Prohibited practices** (Article 5): for example manipulative techniques, social scoring, emotion recognition at work or in education, and untargeted scraping of facial images. Prohibited means stop, not mitigate. The list grew in 2026: check `references/timeline.md`.
5. **High-risk?**
   - **Annex I:** the system is a safety component of, or is itself, a product under listed EU product legislation (machinery, medical devices, toys and others).
   - **Annex III:** it's used in a listed area:
     - biometrics
     - critical infrastructure
     - education
     - **employment and worker management**: recruitment, screening, evaluating candidates, promotion and termination decisions, task allocation, monitoring and evaluating performance
     - access to essential services, including credit scoring and insurance pricing
     - law enforcement
     - migration
     - justice and democratic processes
   - **Article 6(3):** an Annex III system isn't high-risk when it performs a narrow procedural task, improves the result of a completed human activity, detects patterns without replacing human assessment, or does preparatory work. **Profiling of natural persons is always high-risk.** Document the exception: providers must keep that documentation.
6. **Transparency** (Article 50): tell people they're interacting with an AI unless it's obvious, mark synthetic content in a machine-readable way, inform people about emotion recognition and biometric categorisation, and label deepfakes.
7. **General-purpose AI models** (Articles 53 and 55): these duties apply only when you *provide* a GPAI model. Using one through an API makes you a downstream provider or deployer of your own system, not a GPAI provider.
8. **AI literacy** (Article 4): applies to every provider and deployer. Staff who operate or oversee AI need appropriate training.

## Obligations

From the classification, list the obligations that apply:

- **High-risk providers:**
  - risk management (Article 9)
  - data governance (Article 10)
  - technical documentation (Article 11)
  - logging (Article 12)
  - instructions for deployers (Article 13)
  - human oversight (Article 14)
  - accuracy, robustness and cybersecurity (Article 15)
  - a quality management system (Article 17)
  - conformity assessment, registration and post-market monitoring
- **High-risk deployers** (Article 26): use the system as instructed, assign competent human oversight, monitor it, keep logs, and inform affected workers. Some deployers, such as public bodies and certain credit and insurance uses, must also do a fundamental rights impact assessment (Article 27).

## Evidence plan

For each obligation, name the artefact that proves it and the engineering practice that produces it as a by-product. For example, logging produces the Article 12 records, evals produce the Article 15 accuracy evidence, the model and data cards produce the Article 11 documentation, and the review queue produces the Article 14 oversight. Compliance that comes out of the delivery process stays current; compliance written up as a separate document goes stale.

## Output

Write `ai-act-<system>.md`:

- the classification in one line, for example "High-risk (Annex III, employment), we are the deployer"
- the reasoning for each step, with articles
- the obligations, with their application dates from the timeline
- the gaps, ranked
- the evidence plan
- the open questions for legal review
- an "as of" date, and the timeline version used
