---
name: mh-mutual-action-plan
description: "Create a buyer-facing mutual action plan from the internal Blue Sheet, with a mandatory leak check so no internal analysis reaches the customer. Use when the user wants a joint plan, close plan, implementation timeline or next-steps document to share with a buyer."
compatibility: "Any Agent Skills client. File access optional; works chat-only."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/mutual-action-plan.md, shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Mutual action plan

A joint plan that the buyer can read and edit. It is the one place where the internal sheet and the customer meet, so the boundary must hold.

Read `references/operating-rules.md` (especially rule 4) and `references/capabilities.md`. Use `assets/mutual-action-plan.md` for the structure. Save per `references/output-conventions.md`.

## When to use

- The buyer has agreed to a goal and the next steps need dates and owners.
- A proposal or close plan is going to the buyer.
- The user asks for an implementation or evaluation timeline to share.

## Inputs

The Blue Sheet (the action plan, decision process and timeline), the agreed goal in the buyer's words, known dates, and the buyer-side owners the buyer has named. Never assign buyer owners the buyer has not accepted; propose them as questions.

## Procedure

1. **Shared goal.** In the buyer's own words and the date they want. If the buyer has not said it, propose a draft goal and mark it for confirmation.
2. **Steps.** From the decision process: evaluation, technical review, security, legal, procurement, finance, approvals, pilot, signature, implementation. Each with a customer owner, our owner, target date and status.
3. **Dates.** Work back from the buyer's date. Flag impossible sequences; do not hide them. Use real lead times from the sheet.
4. **Decisions and approvals** needed, who decides and by when.
5. **Dependencies and assumptions** both sides must meet.
6. **Open questions** for both teams.
7. **Leak check (mandatory).** Read the draft as the buyer. Delete or rewrite anything that reveals: modes, Wins, support ratings, red flags or unknowns phrased as internal worries, Coach identity or what the Coach said, competitor assessments, pricing strategy or discount authority, forecast category, or the existence of the Blue Sheet. Convert internal risks into neutral joint questions ("Who else needs to review the security questionnaire, and how long does that usually take?").
8. **Mark as draft.** Never send. Offer the user the file or text to send themselves.

## Output

`workspace/accounts/<account>/deals/<opportunity>/map/YYYY-MM-DD-mutual-action-plan.md` with `status: draft`. Reply with the path, the five key dates, and the list of what you removed in the leak check (described generally, not quoting internal content).

## Quality gate

1. The leak check was run and reported.
2. Every step has a date and both owners, or is clearly marked for confirmation.
3. The tone is joint: "we" and "you", never "we need to get the CFO to".
4. Nothing buyer-facing was sent.
