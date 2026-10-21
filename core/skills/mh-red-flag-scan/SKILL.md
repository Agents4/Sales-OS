---
name: mh-red-flag-scan
description: "Scan a Blue Sheet, notes or transcript for red flags and silent risks, link each to an influence, and propose a dated, owned action. Use when the user asks what is wrong with a deal, what they are missing, or wants a quick risk check before a call, review or forecast."
compatibility: "Any Agent Skills client. File and shell access optional; works chat-only."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "methodology/failure-modes.md, methodology/signals-library.md, rubrics/blue-sheet.md, shared/operating-rules.md, shared/capabilities.md"
---

# Red flag scan

Find what is missing, unknown, uncertain or changing. A red flag is any of these that could cost the deal. The output is a short, ranked list with actions, not a lecture.

Read `references/operating-rules.md` and `references/capabilities.md`. Use `references/failure-modes.md` for patterns, `references/signals-library.md` for what signals mean, and `references/blue-sheet.md` for coverage checks.

## When to use

- "What am I missing on this deal?"
- Before a call, a review or a forecast submission.
- After new information (a reorganization, a new procurement contact, a quiet champion).

## Inputs

A Blue Sheet, or notes or a transcript from which the gaps can be seen. If there is no sheet, scan the material and say that the scan is partial.

## Procedure

1. **Run lint** if a shell exists, and list errors and warnings as candidate flags.
2. **Walk the standard checks** against the material:
   - Economic Buyer unidentified, unmet, in Even Keel or Overconfident, or inferred from title only.
   - Any influence with unknown mode or Win, or not contacted.
   - No tested Coach, or only one source of internal information.
   - Single- or double-threaded coverage.
   - New person in role within the last 60 to 90 days, or a reorganization.
   - Decision process, criteria or gates unknown; lead times that do not fit the runway.
   - Competition unexamined, especially status quo and internal build.
   - Stale modes or support (older than 60 days); close date in the past or incompatible with the process.
   - Strengths used to offset flags on a different influence.
   - Signals that point the other way: silence after a good meeting, a new stakeholder appearing late, requests for pricing without a conversation, delegation downward.
3. **Name each flag precisely.** One sentence, linked to an influence, severity High, Medium or Low, with the evidence and source.
4. **Action.** For each High or Medium flag propose an action with an owner and an ISO due date, aimed at that influence. If the owner or date is unknown, ask rather than invent.
5. **Rank** by how much the flag could change the outcome. Keep the list to what matters, usually five or fewer.
6. **Reconcile with the sheet.** Show which flags are already recorded and which are new. Offer to add new ones through `mh-blue-sheet` update rules.

## Output

A ranked table: ID, red flag, influence, severity, evidence, proposed action, owner, due. Then one line on what you could not assess. With file access you may append to the deal's review notes, but do not edit the Blue Sheet unless asked.

## Quality gate

1. Every flag has evidence or is marked as a question to verify.
2. Every High or Medium flag has an action with an owner and a date, or a note that the owner or date is needed.
3. No invented facts. If the material is thin, say what is unknowable from it.
4. Praise nothing that is not evidenced; list real strengths briefly so the user sees the balance.
