---
name: mh-blue-sheet
description: "Build, update or review a Strategic Selling Blue Sheet for one B2B opportunity from notes, transcripts, CRM data or an interview. Use when the user wants an opportunity plan, to map buying influences, to capture what happened on a call, or to turn messy deal notes into a structured sheet."
compatibility: "Any Agent Skills client. File and shell access optional; works chat-only by returning the sheet in one block."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/blue-sheet.md, templates/example-blue-sheet.md, methodology/strategic-selling.md, methodology/signals-library.md, rubrics/blue-sheet.md, shared/operating-rules.md, shared/interview-protocol.md, shared/capabilities.md, shared/output-conventions.md"
---

# Blue Sheet (Strategic Selling)

Produce a Blue Sheet that a manager could challenge and a seller could act on. One sheet is one opportunity with one Single Sales Objective.

Read `references/operating-rules.md` first and follow it. Detect what you can do using `references/capabilities.md`. The method is in `references/strategic-selling.md`. Use `assets/blue-sheet.md` as the structure and `assets/example-blue-sheet.md` to see a finished one (fictional).

## When to use

- A new or poorly understood opportunity needs a plan.
- The user pastes notes, an email thread, a transcript or a CRM export and wants a sheet.
- An existing sheet needs updating after new information (use update mode).
- The user asks who the Economic Buyer is, what the red flags are, or what to do next on a deal.

Not for: a single call plan (`mh-green-sheet`), a whole-account plan (`mh-gold-sheet`), a debrief of one call (`mh-call-debrief`).

## Inputs

Needed: the account and a description of the opportunity. Helpful: notes, transcripts, email threads, CRM export, the existing sheet, `workspace/context-library/business-info.md` and `sales-motion.md`. If the user gives little, use interview mode.

## Procedure

1. **Choose the mode** and say it: *draft* (material supplied), *interview* (little supplied) or *update* (an existing sheet and new information). Follow `references/interview-protocol.md`.
2. **Check scope.** If the deal is small or transactional per `sales-motion.md` thresholds, offer a qualification card (`mh-icp-fit`) or a light sheet. Do not force the full method onto a small deal.
3. **Read everything supplied.** List the sources you received. If a file read fails, follow the file-access guidance in `references/capabilities.md`.
4. **Write the SSO.** Account, what, quantity or value, date. Apply the colleague test. If you cannot write it from the material, ask.
5. **Fill the Buying Influences.** For each role (Economic, User, Technical, Coach): name, title, degree of influence in this decision, mode per issue, support from -5 to +5 or Unknown, access, last verified. Rules:
   - Exactly one Economic Buyer. If the material suggests two, ask who can say no when the other says yes, and relabel the rest.
   - A title is not a role. Ask who can release funds and veto.
   - Mode and support need evidence. One remark is Low confidence. Use `references/signals-library.md` to read signals, and never guess.
   - If a role is empty, leave it empty, add a red flag and an action to find or reach that person.
6. **Win-Results.** Separate the business result from the personal win. Work-relevant only. If you cannot write the Win, write Unknown and the question that would reveal it.
7. **Competition.** Always include status quo and internal build. Use the buyer's perception, not ours.
8. **Strengths and red flags.** Strengths tie to an influence and are used. Red flags are specific. Check the standard list at the end of the template's red flags section. A strength does not cancel a flag on a different influence.
9. **Action plan.** Write the Best Action Commitment and Minimum Acceptable Action for the next interaction. Every red flag gets at least one action with an owner and an ISO due date.
10. **Unknowns and decision process.** For each unknown: who can answer, how to find out, owner, date.
11. **Evidence tags.** Mark claims F, I, A or U with a source. Do not upgrade without new evidence.
12. **Check.** Run the quality gate below. Save per `references/output-conventions.md`.

**Update mode:** re-read the existing sheet, change only what the new information changes, add a Change log row, update `last_reviewed`, and reply with a short list of changes (field, old, new, reason).

## Output

- With file access: write `workspace/accounts/<account>/deals/<opportunity>/blue-sheet.md`. Reply with the path, a three-line summary, the top three open questions and the lint result.
- Chat-only: return the whole sheet in one delimited block, then the summary and questions.
- Always end with the **three highest-value open questions**, ranked, with who can answer each.

## Quality gate

1. If a shell exists, run `python3 tools/sos.py lint <file>` and fix every error. Warnings are listed for the user, not hidden.
2. Without a shell, walk `references/blue-sheet.md` (the rubric) yourself and say that lint was not run.
3. Report: blanks that matter, assumptions the plan depends on, red flags without a dated action, anything you inferred that the user did not say.
4. Confirm nothing invented: every name, number and quote traces to a source you were given.
