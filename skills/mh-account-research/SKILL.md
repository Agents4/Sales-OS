---
name: mh-account-research
description: "Research a target or existing account from public sources into a sourced brief: priorities, triggers, people, ICP fit and hypotheses to test. Use when the user needs account background before a first call, a Blue Sheet, a Gold Sheet or an executive meeting."
compatibility: "Needs web search or fetch for live research. Without web access it organizes supplied material and lists what to research."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/account-research-brief.md, shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Account research

Produce a brief that a seller can use in ten minutes: what the company cares about, what is changing, who matters, and what to test in conversation. Public sources only unless the user supplies more.

Read `references/operating-rules.md` and `references/capabilities.md`. Use `assets/account-research-brief.md` for the structure and `references/output-conventions.md` for where to save.

## When to use

- Before a first call or a major meeting.
- To seed a Blue Sheet or a Gold Sheet.
- To refresh a stale account profile.

## Inputs

The account (name and, if ambiguous, location or domain), the purpose, and any known context. If the name is ambiguous, ask once before researching.

## Procedure

1. **Check capability.** If web search or fetch is available, use it. If not, say that the brief will organize supplied material only, and list what to research.
2. **Collect from primary sources first:** the company's own site, annual or investor reports and filings, press releases, leadership statements, job postings (they reveal priorities), regulatory filings, and reputable news. Prefer recent. Note dates.
3. **Capture the customer's language:** priorities and pressures in their words, with a quote and URL.
4. **Triggers and timing:** leadership changes, funding, acquisitions, reorganizations, regulatory deadlines, product launches, incidents.
5. **People:** only business-relevant, public information (name, title, role, tenure if public). Mark confidence. Do not guess titles or infer roles. Never collect personal or private information.
6. **ICP fit:** score against the client's profile from `workspace/context-library/business-info.md` if it exists.
7. **Hypotheses:** two to five statements to test in conversation, how to test each, and with whom.
8. **Not found:** list what could not be established.
9. **Sources:** numbered URLs with access dates. Every claim in the brief maps to a number.

## Output

`workspace/accounts/<account>/research/YYYY-MM-DD-<purpose>.md`. Reply with three bullets of what matters most and the sources count. Chat-only: the brief in one block.

## Quality gate

1. Every factual claim has a numbered source; claims from a single weak source are marked Low confidence.
2. No invented people, titles, numbers or quotes.
3. Recent facts are checked for freshness; anything older than 12 months is labelled with its date.
4. Respect site restrictions: if a page cannot be fetched, say so rather than working around it.
