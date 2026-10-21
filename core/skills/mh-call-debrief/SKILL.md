---
name: mh-call-debrief
description: "Debrief a customer call from a transcript, recording summary or notes: result against plan, new facts, buyer Concept, mode and Win-Results changes, red flags, commitments, Blue Sheet updates and a buyer-safe follow-up draft. Use when a call or meeting has just happened and the user wants to capture it, update the deal, or draft a follow-up."
compatibility: "Any Agent Skills client. File and shell access optional. Can read meeting notes from Google Workspace when connected; otherwise ask the user to paste them."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/call-debrief.md, rubrics/debrief.md, methodology/signals-library.md, shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Call debrief

Turn a call into evidence. The debrief separates what was said from what you infer, updates the Blue Sheet with sourced changes, and drafts a follow-up that contains nothing internal.

Read `references/operating-rules.md` and detect capabilities (`references/capabilities.md`). Use `assets/call-debrief.md` as the structure, `references/debrief.md` as the quality rubric and `references/signals-library.md` to interpret modes and signals.

## When to use

- A call, meeting or demo has happened and there is a transcript, notes or the user's recollection.
- The user asks "what did I learn", "update the sheet", "draft the follow-up" or "did we get the commitment".

## Inputs

Needed: the call content and the opportunity. Helpful: the Green Sheet for the call, the Blue Sheet, and the attendee list. If Google meeting notes or a transcript are reachable (GOOGLE capability), offer to read them. Otherwise ask for the paste.

## Procedure

1. **Gather.** Read the call content, the Green Sheet and the Blue Sheet. State what you received.
2. **Result against plan.** Was the Best Action Commitment achieved, the Minimum Acceptable Action, or neither? Quote the evidence. Do not mark success on friendly sounds alone.
3. **Extract facts.** New facts only, each with a source (timestamp or short quote) and what it affects. Keep quotes exact and short.
4. **Concept.** Record the buyer's Concept in their words and how it differs from your hypothesis.
5. **Influence changes.** For each person: mode (per issue), support, Win, access. Show old, new, evidence and confidence. One remark is Low confidence. Do not change a mode on one ambiguous remark; record it as an inference and add a question to confirm.
6. **New people, process, timing.** Any new stakeholder, approval step, security or legal gate, reorganization or procurement involvement becomes an unknown or a red flag with an action.
7. **Red flags.** List created and resolved. Every new flag gets an owned, dated action.
8. **Commitments.** What we owe, what they owe, by when.
9. **Blue Sheet diff.** List proposed edits: section, field, old, new, reason. If the user asked you to update the sheet, apply them with `mh-blue-sheet` update rules (Change log row, `last_reviewed`). Otherwise present and wait.
10. **Follow-up draft.** Restate agreed next steps only. Buyer-safe, in the user's voice (`workspace/context-library/writing-style.md` if present). Mark it a draft. Do not send.
11. **Honest note.** Say where the call went worse than hoped.
12. **Leak check.** Read the follow-up as the buyer. Remove modes, Wins, flags, competitor assessments, Coach references and forecast.

## Output

File locations and naming follow `references/output-conventions.md`.

- With file access: `workspace/accounts/<account>/deals/<opportunity>/call-notes/YYYY-MM-DD-<topic>.md` for the raw notes if supplied, and the debrief in `workspace/outputs/debriefs/YYYY-MM-DD-<account>.md`.
- Reply: the result in one line, the top three learnings, sheet changes proposed or applied, the follow-up draft, open questions.
- Chat-only: the debrief in one block plus the follow-up in a second block.

## Quality gate

1. Walk `references/debrief.md`. Fail conditions: any invented quote, any mode change presented as fact on a single remark, any internal-only item in the follow-up, a BAC marked achieved without evidence.
2. If the Blue Sheet was changed and a shell exists, run `python3 tools/sos.py lint <file>`.
3. Report assumptions, unknowns created, and anything you inferred that the user did not say.
