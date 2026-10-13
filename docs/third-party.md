# Third-party plugins and skills

What I use that I didn't write, and the rules for bringing outside code into my agents.

## Plugins I use

| Plugin | From | What for |
|---|---|---|
| product-management, marketing, design | [Anthropic knowledge-work plugins](https://github.com/anthropics/knowledge-work-plugins) | Specs, roadmaps, research synthesis, campaign briefs, design critique |
| cowork-plugin-management | Anthropic | Creating and customizing plugins in Cowork |
| figma | [Figma](https://www.figma.com) | Design-to-code and code-to-design through the Figma connector |
| brand-voice | Tribe AI | Brand guidelines and on-brand writing |
| resume-skills | [ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills) | CV and job-search work |

I install these from their own marketplaces, so they update from their source. They aren't copied into this repo.

Turn off overlapping plugins once a domain here covers them. Two skills that both answer "write a cover letter" make the agent pick one at random. With the `career` plugin enabled, resume-skills is switched off.

Anthropic's built-in skills (docx, pdf, pptx, xlsx, skill-creator and others) come with a Claude account. They're proprietary, so they're never vendored here.

## Rules for outside skills

1. **Read every line before installing.** That covers SKILL.md, scripts and hooks. Published skills have shipped prompt injection and `curl | bash` payloads.
2. **Pin to a commit,** not a branch, for anything that doesn't come from its own vendor.
3. **Keep the license and the credit.** A vendored skill keeps its upstream LICENSE inside its folder, plus a note of where it came from and what I changed.
4. **Private by default.** A skill I didn't write never goes in this public repo. If I use it, it's vendored in the private companion until I can install it from its upstream source.
