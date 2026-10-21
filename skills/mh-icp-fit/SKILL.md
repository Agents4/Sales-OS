---
name: mh-icp-fit
description: "Qualify an account or opportunity against the Ideal Customer Profile and decide whether it needs a qualification card, a light Blue Sheet or a full Blue Sheet. Use when the user asks if a lead is worth pursuing, which funnel zone a deal belongs in, or how much planning a deal deserves."
compatibility: "Any Agent Skills client. File and web access optional; works chat-only."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/qualification-card.md, methodology/funnel-and-pipeline.md, shared/operating-rules.md, shared/capabilities.md"
---

# ICP fit and qualification

Effort should follow potential. This skill decides whether an account fits the Ideal Customer Profile, which funnel zone it belongs in, and how much planning it earns.

Read `references/operating-rules.md` and `references/capabilities.md`. The zones, thresholds and artifact choices are in `references/funnel-and-pipeline.md`. Use `assets/qualification-card.md` for the card.

## When to use

- A new lead or inbound request.
- A seller wants to know if a deal deserves a Blue Sheet.
- A manager wants to disqualify or reprioritize.

## Inputs

The account and any facts about it, the client's Ideal Customer Profile from `workspace/context-library/business-info.md` and the thresholds from `sales-motion.md`. If either is missing, say so and ask. If web access exists, you may gather public facts; cite them.

## Procedure

1. **Load the ICP.** It should come from the shared characteristics of best existing customers, not an aspirational list. If it is vague, list what needs defining and offer to help (interview mode).
2. **Score fit** per criterion from -5 (major gap) to +5 (strong match), with evidence for each. Unknown is allowed.
3. **Check the basics:** a real need in their words, who decides and funds, access to that person, timing, budget exists or can be created, the alternative including do nothing.
4. **Decide the zone:** above the funnel, in the funnel or Best Few, with reasons.
5. **Choose the artifact** using the thresholds: qualification card only, light Blue Sheet, full Blue Sheet, or Gold Sheet. State the threshold used.
6. **Decide:** pursue, nurture or disqualify, with the reason and the next step, owner and date. Accounts that clearly miss the ICP are disqualified, not nurtured.
7. **Hand off:** offer `mh-blue-sheet` or `mh-account-research` as the next step.

## Output

A completed qualification card. With file access save beside the account (`workspace/accounts/<account>/`). Reply with the decision, the fit score summary and the next step.

## Quality gate

1. Each score has evidence or is marked Unknown.
2. The decision follows from the scores and the thresholds, and the user's override, if any, is recorded.
3. No private information about individuals is gathered.
