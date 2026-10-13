---
name: threat-model
description: Threat-models a feature or system with a data-flow diagram, STRIDE per element, AI and agent threats such as prompt injection and excessive agency, mitigations, residual risk and tests. Use it when designing or reviewing something security-sensitive, adding an LLM or agent to a product, or when someone asks for a threat model. For legal or regulatory questions about AI, use ai-act-assessment.
license: MIT
---

# Threat model

Ask four questions, in this order: what are we building, what can go wrong, what are we doing about it, and did we do a good enough job? Keep it concrete enough that every mitigation turns into a ticket or a test.

## Steps

1. **Scope.** The feature or system, its users, and what's explicitly out of scope.
2. **Assets.** What an attacker wants: data (PII, credentials, payment data, IP), money, availability, reputation, and the AI's capabilities and permissions.
3. **Diagram.** A Mermaid data-flow diagram with external entities, processes, data stores and flows, and the **trust boundaries** marked. Most threats sit on boundary crossings.
4. **STRIDE** for each element and boundary crossing:

   | Threat | Question |
   |---|---|
   | Spoofing | Can someone pretend to be another user or service? |
   | Tampering | Can data or code be changed in transit or at rest? |
   | Repudiation | Can someone deny an action because it isn't logged? |
   | Information disclosure | Can data leak to the wrong party? |
   | Denial of service | Can someone exhaust the system or its budget? |
   | Elevation of privilege | Can someone gain rights they shouldn't have? |

5. **AI and agent threats**, when an LLM or agent is in the flow:
   - **prompt injection** from user input and from retrieved content (web pages, documents, emails, tickets)
   - **sensitive data disclosure** in outputs or logs
   - **excessive agency:** tools and permissions beyond what the task needs
   - **insecure output handling:** model output executed or rendered without validation
   - **training-data or retrieval poisoning**
   - **supply-chain risk** in models, plugins and skills
   - **runaway cost**
6. **Rate** each threat for likelihood and impact (1–5), with its existing mitigations, missing ones, and the residual risk after the planned controls.
7. **Tests:** for each mitigation, the test or monitor that proves it works: unit, integration, or a red-team prompt for AI flows.

## Output

`threat-model-<slug>.md`: scope, assets, the diagram, a threat table (ID, element, STRIDE or AI category, threat, likelihood, impact, existing, missing, residual, owner), and the top five actions. For EU systems that process personal data, note where a DPIA (data protection impact assessment) may be required. Hand AI regulation questions to `ai-act-assessment`.
