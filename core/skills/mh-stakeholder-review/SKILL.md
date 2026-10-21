---
name: mh-stakeholder-review
description: "Stress-test a deal plan, proposal or message from the viewpoint of the Economic Buyer, User Buyer, Technical Buyer, Coach or the strongest competitor. Use when the user wants to see how a stakeholder would react, prepare for objections, or check a plan from several perspectives before a meeting or review."
compatibility: "Any Agent Skills client. Uses parallel subagents when available, otherwise runs the lenses one after another."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "lenses/economic-buyer.md, lenses/user-buyer.md, lenses/technical-buyer.md, lenses/coach.md, lenses/competitor.md, shared/operating-rules.md, shared/capabilities.md"
---

# Stakeholder review

Look at the same plan through different eyes. Each lens is a short brief in `references/`. Choose the lens or lenses, apply them to the plan using only the evidence provided, and return a plain verdict and the action that helps most.

Read `references/operating-rules.md` and `references/capabilities.md`.

## Lenses

| Lens | File | Use for |
|---|---|---|
| Economic Buyer | `references/economic-buyer.md` | Business case, risk, timing, why now, personal stake |
| User Buyer | `references/user-buyer.md` | Daily impact, adoption, fear, involvement |
| Technical Buyer | `references/technical-buyer.md` | Requirements, integration, security, process, lead times |
| Coach | `references/coach.md` | Coach strength, intel gaps, protection |
| Competitor | `references/competitor.md` | How the strongest alternative, including status quo, would beat us |

## When to use

- Before an executive meeting, a proposal, a deal review or a forecast call.
- When the user asks "how will the CFO see this", "what will IT say" or "how would the competitor attack us".
- When the user wants a quick whole-deal read from every viewpoint.

## Inputs

The plan, proposal, message or Blue Sheet to review, and which lens or lenses. If none is named, default to Economic Buyer, Technical Buyer and Competitor, and offer the others.

## Procedure

1. **Pick lenses** and say which. Use all five only when asked.
2. **Gather evidence.** Read the Blue Sheet and anything about the people. Do not invent what a person thinks. Where the evidence is thin, say what the lens can and cannot conclude.
3. **Run each lens.** If subagents are available, run each lens in parallel with only the plan and its brief, then synthesize. Otherwise run them one after another, each under its own heading. Keep them independent: do not let the first lens bias the next.
4. **For each lens return** the verdict, the three questions they would ask first, missing proof or risk, and the one action that most helps.
5. **Synthesize.** Where lenses conflict, say so. Rank the actions by effect on the deal. Note any red flag the review reveals and offer to add it to the sheet.

## Output

One section per lens, then a synthesis with the ranked actions. With file access save to `workspace/outputs/reviews/YYYY-MM-DD-<opportunity>-stakeholder-review.md`. Chat-only: return in one block.

## Quality gate

1. Each lens is grounded in evidence from the material and says so; guesses are labeled as assumptions.
2. The review is critical, not flattering.
3. Nothing in the review is meant for the buyer. Keep it internal.
4. Never speculate about private-life matters; work-relevant motives only.
