# Research notes

How the methodology base was built, what is verified and what is not. Reviewed 2026-10-17.

## Method

Sources were read in three groups: (1) summaries and descriptions of the three books and the official terminology for the Large Account Management Process; (2) vendor documentation that implements the sheets in CRM tools; (3) practitioner write-ups. Elements that agree across independent sources are marked canonical with high confidence; elements that vary by source are marked convention or medium/low confidence in `core/methodology/fidelity-ledger.md`.

## Verified (multiple agreeing sources)

- Blue Sheet structure: single sales objective, four buying influences with exactly one Economic Buyer, degree of influence, response modes, Win-Results, red flags, strengths, competition and position, action plan.
- Response modes Growth, Trouble, Even Keel, Overconfident; only Growth and Trouble buy.
- Coach tests: credibility, wants you to win, gives information you cannot get elsewhere.
- Conceptual Selling: Concept; getting and giving information; commitment; question types; Best Action Commitment.
- LAMP: four phases; Field of Play; Strategic Players (Sponsor, Strategic Coach, Anti-Sponsor, Additional Key Player); Strategic Strengths; Critical Vulnerability; Buy-Sell Hierarchy; Charter Statement; Relationship Goals; Focus and Stop; Revenue Targets.

## Not independently verified

- Book publication years (1985, 1987, 1991) come from secondary sources.
- The exact wording of the Minimum Acceptable Action in official materials.
- Numeric scales (-5 to +5 for support and position): used by vendor templates, not consistently defined in the sources reviewed; treated as convention.
- The seven-factor account selection rubric and review cadences: practitioner sources.
- The full text of official worksheets: not reproduced and not required.

## Decisions taken because of the research

- Gold Sheet vocabulary follows the official LAMP terms rather than Blue Sheet roles.
- Canonical elements, conventions and Sales-OS extensions are tagged separately so a client can swap in their licensed wording.
- Forecast gates, evidence tags, lint rules and buyer-facing redaction are labelled Sales-OS extensions, not doctrine.

## Platform research (Google)

Done 2026-10-17; sources and the verify list are in `adapters/google/platform-facts.md`. Key corrections made to the design: Gemini CLI transitioned to Antigravity CLI for individual accounts; Gems were replaced by skills in the Gemini app; NotebookLM appears as Gemini Notebook in Google's current documentation; skills use the open SKILL.md format so one source serves every platform.

## Platform research (Microsoft)

Done 2026-10-22; sources and the verify list are in `adapters/microsoft/platform-facts.md`. Key findings that shaped the design: Copilot Cowork is generally available and loads the same SKILL.md zips (10 MB, 100 files per archive); Agent Builder and Copilot Studio skills are preview with an 8-skill limit per agent, so Sales-OS ships three 8-skill agent presets; plain Copilot Chat has no skills, so it uses the portable prompt and Copilot Notebooks; VS Code and GitHub Copilot read `.agents/skills/` directly. Several claims (Notebook limits, federated connector dates, Anthropic region limits) rest on third-party or unverified sources and are rated low confidence.

## Open questions for the client

1. Which Google licenses and accounts do sellers hold?
2. Do they hold a Miller Heiman license, and do they want to keep official terminology and scales?
3. Which CRM, and may the Salesforce connector read opportunity data?
4. Where do meeting notes and transcripts live today?
5. What data may be loaded into notebooks?
