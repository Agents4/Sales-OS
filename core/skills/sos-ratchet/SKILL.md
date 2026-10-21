---
name: sos-ratchet
description: "Turn lessons from real deals into proposed improvements to skills, templates, rules or the context library, for human approval. Use when a debrief or win/loss review shows a repeated mistake, when a user keeps correcting the same output, or on a periodic review of lessons."
compatibility: "Any Agent Skills client. File access recommended to read and write lessons; otherwise works from pasted material."
metadata:
  version: "1.0.0"
  layer: system
  last_reviewed: "2026-10-17"
  includes: "scaffold/workspace/context-library/lessons.md, shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Ratchet

A system improves when each mistake becomes a rule that prevents it. The ratchet turns evidence into small, reviewable proposals. It never changes the shared product on its own.

Read `references/operating-rules.md`, `references/capabilities.md` and `references/output-conventions.md`. The log format is in `references/lessons.md`.

## When to use

- A win/loss review or debrief exposed a repeatable mistake.
- A user keeps correcting the same thing in outputs.
- A monthly or quarterly improvement review.

## Inputs

Evidence: debriefs, win/loss reviews, user corrections, lint results across sheets. And `workspace/context-library/lessons.md` if it exists.

## Procedure

1. **Collect evidence.** Read the lessons log and the recent reviews. Note repeated patterns, not single events.
2. **Diagnose the layer.** Where does the fix belong?
   - A client fact or voice rule: `workspace/context-library/`.
   - A client-specific skill or threshold: `local/skills/` or `sales-motion.md`.
   - A product-wide skill, template, rubric or rule: a change request to the Sales-OS maintainers (`core/`).
3. **Write the proposal** as the smallest change that prevents the mistake: what to change, the exact text or diff, the evidence (at least two instances, or one severe), the risk of the change, and how to test it (an eval case if relevant).
4. **Check against the rules.** The change must not weaken any rule 1 to 6 in the operating rules, must not remove approval gates, and must not add private-life data collection.
5. **Record** each proposal in `lessons.md` with status `proposed`, date and evidence.
6. **Ask for approval.** Only after approval, apply context-library and local changes. For `core/` changes, produce a patch description for the maintainers; do not edit `core/` in a client instance.
7. **Close the loop.** When a change is applied, set status `applied` with the date, and note the next review date.

## Output

A short list of proposals with evidence and risk, the log entries added, and which require maintainer action.

## Quality gate

1. Each proposal cites evidence and is small enough to test.
2. No change was applied without approval.
3. No proposal asks the system to be less honest, drop approval gates, or collect private information.
4. Generated folders were not edited.
