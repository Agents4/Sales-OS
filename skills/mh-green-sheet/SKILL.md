---
name: mh-green-sheet
description: "Plan a customer conversation with a Conceptual Selling Green Sheet: realistic objective, buyer's Concept, the five question types, and what to give. Use when the user has a call or meeting coming up with a buyer and wants a call plan, discovery questions, or a Best Action Commitment."
compatibility: "Any Agent Skills client. File and shell access optional; works chat-only by returning the plan in one block."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/green-sheet.md, templates/example-green-sheet.md, methodology/conceptual-selling.md, rubrics/green-sheet.md, shared/operating-rules.md, shared/interview-protocol.md, shared/capabilities.md, shared/output-conventions.md"
---

# Green Sheet (Conceptual Selling)

A call is a hypothesis to test, not a pitch to deliver. This skill produces the plan: what you want from the conversation, what you believe, what you will ask, and what you will show once the buyer's Concept is confirmed.

Read `references/operating-rules.md` and detect capabilities with `references/capabilities.md`. The method is in `references/conceptual-selling.md`. Use `assets/green-sheet.md` as the structure and `assets/example-green-sheet.md` for a finished example (fictional).

## When to use

- The user has a meeting, demo, discovery call or executive conversation coming up.
- The user asks for discovery questions, a call plan or a Best Action Commitment.
- The user wants to prepare for a specific person in a deal.

Not for: debriefing a call that already happened (`mh-call-debrief`).

## Inputs

Needed: who the meeting is with and the date. Helpful: the Blue Sheet for the deal, prior notes with this person, the account research, and the sales motion. If a Blue Sheet exists, read it first; this plan must agree with it.

## Procedure

1. **Anchor to the Blue Sheet.** Find the person's role, mode, support, Win and the open red flags that this conversation can resolve. If no sheet exists, offer to build one (`mh-blue-sheet`) but do not block. If the user has little to give, interview them as described in `references/interview-protocol.md`, three questions at a time.
2. **Set the objective.** Write the Best Action Commitment (the most this person is realistically ready to do next, specific and dated) and the Minimum Acceptable Action (the least that still advances the sale, with what failing it would tell you). Add their valid business reason to agree, from their side.
3. **State the Concept.** Write your hypothesis of what this person pictures when the problem is solved, in their words if you have them, with source and confidence. If unknown, the main goal of the call is to find it.
4. **Known, assumed, unknown.** Separate facts (cited), assumptions to confirm, and unknowns this call must close.
5. **Write the questions.** At least two of each type, listed in call order:
   - Confirmation: verify what you believe.
   - New information: Concept, criteria, process, others who matter.
   - Attitude: priorities, politics, stakes. These reveal mode and Win.
   - Commitment: test readiness and earn small agreements.
   - Basic issue: the issue under the presenting problem.
   Questions must be open, non-leading, and in the buyer's language. Prefer asking about their situation over presenting yours.
6. **Plan what to give.** Only after the Concept is confirmed. Map each part of their Concept to what you will say or show, the proof, and when.
7. **Obstacles.** Likely obstacles, whose they are, response, proof.
8. **Recap.** Write the closing restatement: what was agreed, who does what by when, the next meeting.
9. **Check and save.** Run the quality gate. Save per `references/output-conventions.md`.

If the user is under time pressure, deliver the objective, the Concept hypothesis and the top five questions first, then the rest.

## Output

- With file access: `workspace/accounts/<account>/deals/<opportunity>/green-sheets/YYYY-MM-DD-<person>.md`. Reply with the path, the BAC and MAA in two lines, and the three questions that matter most.
- Chat-only: the plan in one block, then the top questions. Remind the user once to save it.
- Mention that the debrief section stays open until the call is done; offer `mh-call-debrief` afterwards.

## Quality gate

1. Lint if possible: `python3 tools/sos.py lint <file>`. Otherwise walk `references/green-sheet.md` (the rubric).
2. A BAC and a MAA exist and are different.
3. Every question type is present. The give section follows the Concept.
4. No internal-only content is planned to be shown to the buyer. Do not suggest revealing modes, Wins or competitor assessments.
5. Report assumptions the call depends on and anything not in the source material.
