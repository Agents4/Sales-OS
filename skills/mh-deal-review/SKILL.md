---
name: mh-deal-review
description: "Challenge a deal against its Blue Sheet and the forecast hygiene gates, and give a green, amber or red verdict with the questions that would change it. Use when a manager or seller wants a deal review, a forecast challenge, a pre-commit check, or a second opinion on whether an opportunity is real."
compatibility: "Any Agent Skills client. File and shell access optional; works chat-only when the sheet is pasted."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/deal-review.md, rubrics/blue-sheet.md, methodology/funnel-and-pipeline.md, methodology/failure-modes.md, shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Deal review

A deal review tests the plan, not the person. It uses the Blue Sheet as evidence and the forecast gates in `references/funnel-and-pipeline.md` as the bar. The output is a verdict and a short list of specific questions and actions.

Read `references/operating-rules.md` and detect capabilities (`references/capabilities.md`). Use `assets/deal-review.md` as the output structure, `references/blue-sheet.md` as the rubric and `references/failure-modes.md` to name what is wrong.

## When to use

- A forecast call needs challenging ("is this really Commit?").
- A manager reviews a seller's Best Few deals, or the seller wants a hard look before a review.
- A deal has stalled or slipped and the user wants to know why.

For one stakeholder's view use `mh-stakeholder-review`. For scanning only risks use `mh-red-flag-scan`.

## Inputs

Needed: the Blue Sheet (or the notes to build one) and the forecast category claimed. Helpful: recent debriefs, CRM stage, amount and close date, the sales motion thresholds.

## Procedure

1. **Read the sheet** and the CRM facts if available. If they disagree, show both and do not pick silently.
2. **Run lint** if a shell exists (`python3 tools/sos.py lint <file>`). Use the findings as evidence.
3. **Apply the gates.** For the category claimed, check each gate in `references/funnel-and-pipeline.md`. Mark Met, Not met or Unknown with evidence. A failed gate is a question, not a verdict.
4. **Coverage.** Economic Buyer, User, Technical, Coach: named, met, mode known, Win known, support, gap.
5. **Find the top risks** (at most five). For each: why it matters, the evidence, and what would change it. Name the failure mode from `references/failure-modes.md` when it applies.
6. **Check consistency.** Are modes and support consistent with the claimed stage? Is the close date compatible with the decision process, lead times and the runway? Does the amount match the SSO?
7. **Verdict.** Green: category supported, no high-severity flag without an action. Amber: supportable with named gaps closed. Red: category not supported, or critical unknowns. State the category the evidence does support.
8. **Questions for the seller.** Up to three, specific, answerable. Not rhetorical.
9. **Agreed actions.** Owner and date for each, proposed for the seller to accept.

Optional depth: if the user wants perspective checks, run `mh-stakeholder-review` for the Economic Buyer and the main competitor.

## Output

Fill `assets/deal-review.md` (naming rules in `references/output-conventions.md`). With file access save to `workspace/outputs/reviews/YYYY-MM-DD-<opportunity>-deal-review.md` and reply with the verdict, category supported, the top three risks and the three questions. Chat-only: the review in one block.

## Quality gate

1. Every finding cites a field or a source in the sheet. Nothing invented.
2. No percent probabilities unless the client's motion defines them. Say what evidence is missing for the next category instead.
3. Internal-only content stays in this review; do not suggest sharing it with the buyer.
4. Tone: direct, specific, fair. Credit what is strong before listing gaps.
