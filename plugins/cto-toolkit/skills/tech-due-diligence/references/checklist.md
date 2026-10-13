# Tech due diligence checklist

Request these early. "Not available" is an answer worth recording.

## Product and architecture
- [ ] Architecture diagrams (current, not aspirational) and a walkthrough with the CTO
- [ ] The main components, data stores and third-party services, and why each was chosen
- [ ] Scalability: current load, headroom, the last capacity incident
- [ ] Multi-tenancy and data isolation model

## Code and delivery
- [ ] Read access to the 2–3 core repositories
- [ ] Test strategy and coverage of the critical paths, and the CI pipeline
- [ ] Release process, deployment frequency, rollback, and the change failure rate if known
- [ ] Dependency management: outdated or end-of-life frameworks, and the update practice

## Security and compliance
- [ ] Last penetration test and the status of its findings
- [ ] Security incidents and breaches in the last 3 years, with postmortems
- [ ] Access management: SSO, MFA, offboarding, production access
- [ ] Certifications (SOC 2, ISO 27001) or the roadmap to them
- [ ] GDPR: records of processing, DPAs with processors, data residency, deletion and DSAR handling
- [ ] AI Act: an inventory of AI systems, the role per system, and any high-risk uses

## Infrastructure and cost
- [ ] Hosting setup, environments, infrastructure as code
- [ ] Cloud cost for the last 12 months by service, and unit cost per customer
- [ ] Backups and restores: tested when, and the RPO/RTO
- [ ] Monitoring, alerting and on-call

## Team and organisation
- [ ] Org chart: roles, seniority, location, contractors and agencies
- [ ] Attrition in the last 24 months, and current open roles
- [ ] Key-person risk: who holds critical knowledge, and the retention plans
- [ ] Engineering process: planning, reviews, documentation, incident handling

## Intellectual property and legal
- [ ] IP assignment from all employees and contractors
- [ ] Open-source licence inventory, with copyleft in distributed software flagged
- [ ] Third-party software licences and their limits

## Debt and roadmap
- [ ] Known tech debt, and its impact on the roadmap
- [ ] The roadmap for the next 12–18 months, and the capacity behind it
- [ ] Planned rewrites or migrations, with their rationale and status
