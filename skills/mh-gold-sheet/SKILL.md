---
name: mh-gold-sheet
description: "Build or review a Large Account Management Process (LAMP) Gold Sheet for a strategic account: Field of Play, Strategic Players, strengths, Critical Vulnerability, Buy-Sell Hierarchy, Charter Statement, Focus and Stop investments. Use when the user is planning a key or strategic account, an account review, or long-term growth rather than one deal."
compatibility: "Any Agent Skills client. File and shell access optional; works chat-only by returning the plan in one block."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/gold-sheet.md, templates/example-gold-sheet.md, methodology/lamp.md, rubrics/gold-sheet.md, shared/operating-rules.md, shared/interview-protocol.md, shared/capabilities.md, shared/output-conventions.md"
---

# Gold Sheet (LAMP)

An account plan for a strategic account or a clearly defined part of it. LAMP moves through four phases: Data Gathering, Situation Appraisal, Strategy Planning and Action Planning. The Gold Sheet captures the result.

Read `references/operating-rules.md` and `references/capabilities.md`. The method and vocabulary are in `references/lamp.md`. Use `assets/gold-sheet.md` as the structure and `assets/example-gold-sheet.md` for an example (fictional).

## When to use

- A strategic or key account needs a plan, an annual review or a restart.
- The user asks about Sponsors, Anti-Sponsors, account strategy, relationship goals or what to stop doing.
- Several Blue Sheets sit under one account and need a coherent strategy.

Not for: one opportunity (`mh-blue-sheet`). Apply the funnel guidance: do not build a Gold Sheet for an account that is not strategic.

## Inputs

Needed: the account and which Field of Play to plan. Helpful: Blue Sheets, account research, revenue history, executive contacts, delivery and support history, `business-info.md` and `sales-motion.md`.

## Procedure

1. **Mode.** Draft, interview or update per `references/interview-protocol.md`. Say which.
2. **Data gathering.** List what you have and what is missing: customer, industry, competitors, history, people. Offer `mh-account-research` for gaps. Do not guess.
3. **Field of Play.** The part of the account that acts independently and where you can contribute significantly. State scope and exclusions.
4. **Strategic Players.** Sponsor, Strategic Coach, Anti-Sponsor, Additional Key Players. For each: influence, relationship strength, internal owner, evidence gap, next action. At least one Sponsor, ideally two. Record "None identified" for Anti-Sponsor only with how you checked. An org chart is not a relationship map.
5. **Trends, opportunities, KPIs.** In the customer's language. Source them.
6. **Strategic Strengths** the Field of Play values and competitors cannot easily match.
7. **Critical Vulnerability.** One weakness that would cripple the position if left alone. Single-Sponsor dependency is common. Pair it with a plan.
8. **Buy-Sell Hierarchy.** Customer's current view, our view, desired level, with evidence. The customer decides the level.
9. **Charter Statement.** Where you and the customer agree the relationship should go, measurable and time-bound, with benefit to both.
10. **Relationship Goals** per Strategic Player, tied to opportunities and strengths.
11. **Focus and Stop.** Name at least one thing to stop. A plan with only additions is a task list.
12. **Revenue targets, SSOs, actions, red flags.** Link each SSO to a Blue Sheet. Every action has owner, date and a customer purpose with completion evidence.
13. **Cadence.** Set `next_review` within 60 to 90 days and list trigger events (executive change, acquisition, Sponsor departure, competitive entry, delivery incident).

## Output

File locations and naming follow `references/output-conventions.md`.

- With file access: `workspace/accounts/<account>/gold-sheet.md`. Reply with the path, the Charter in one line, the Critical Vulnerability, and the top three open questions.
- Chat-only: the plan in one block then the summary.

## Quality gate

1. Lint if possible: `python3 tools/sos.py lint <file>`. Otherwise walk `references/gold-sheet.md` (the rubric).
2. At least one Sponsor, a named Critical Vulnerability, a Charter Statement, and at least one Focus and one Stop.
3. Single-threaded? Say so and make a second Sponsor the first action.
4. Report assumptions the plan relies on and anything the user did not say.
