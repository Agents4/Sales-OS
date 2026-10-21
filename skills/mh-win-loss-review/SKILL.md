---
name: mh-win-loss-review
description: "Review a closed opportunity (won, lost or no-decision) by comparing what the Blue Sheet said with what happened, and extract lessons that change practice. Use when a deal has closed, a loss needs a post-mortem, or the team wants to calibrate its sheets and forecasts against outcomes."
compatibility: "Any Agent Skills client. File and shell access optional; works chat-only."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/win-loss-review.md, methodology/failure-modes.md, shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Win/loss review

Learn, do not blame. The most valuable comparison is between what the sheet claimed and what actually happened, because that exposes where the method or the seller's evidence was weak.

Read `references/operating-rules.md` and `references/capabilities.md`. Use `assets/win-loss-review.md` as the structure and `references/failure-modes.md` to name patterns. File locations are in `references/output-conventions.md`.

## When to use

- A deal has been won, lost or ended in no decision.
- The team wants a quarterly look at outcomes versus forecast.
- A loss needs an honest explanation for a manager or coach.

## Inputs

The final Blue Sheet and its Change log, debriefs and call notes, the CRM outcome and stated reason, and any customer feedback. Ask for what is missing. If the buyer gave a reason, record it separately from your analysis.

## Procedure

1. **Outcome.** What was decided, by whom, when. Separate the stated reason from the likely real reason, and label each.
2. **Compare sheet to reality.** Economic Buyer, modes, support, competition, decision process, timeline. Use the Change log to see what the sheet said at each point.
3. **Turning points.** The few events that decided it: date, event, effect, and whether the sheet could have shown it.
4. **What worked** and **what was missed or late.** Be specific. Tie to roles and evidence.
5. **Name the failure modes** from `references/failure-modes.md` that apply, with evidence. Do not force a match.
6. **Lessons.** Each lesson is a concrete change: a question to ask, a gate to add, a template field, a rule, a practice. For each: evidence, where it applies, the proposed change.
7. **Route the lessons.** Put proposed changes to skills, templates or rules in `workspace/context-library/lessons.md` for approval via `sos-ratchet`. Do not change shared files yourself.
8. **Closing.** Update the Blue Sheet status and Change log if asked. Do not delete the sheet.

## Output

`workspace/outputs/reviews/YYYY-MM-DD-<opportunity>-win-loss.md` from the template. Reply with the outcome in one line, the top three lessons and the proposed changes. Chat-only: one block.

## Quality gate

1. Every claim cites the sheet, a debrief or a customer statement. No hindsight stories without evidence.
2. Wins get the same scrutiny as losses: a win can hide luck and weak process.
3. Customer data stays within approved tools. No private-life details about any person.
4. Lessons are actionable and small enough to try.
