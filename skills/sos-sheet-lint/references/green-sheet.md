---
name: rubric-green-sheet
description: Review rubric for a Green Sheet call plan, with lint codes
---

# Rubric: Green Sheet

Score each criterion **Pass / Weak / Fail**. Run `python3 tools/sos.py lint <file>` when a shell is available.

| # | Criterion | Pass looks like | Lint |
|---|---|---|---|
| 1 | **Best Action Commitment** | Specific, dated, something this person can actually do, and the most they are realistically ready for | GS002 |
| 2 | **Minimum Acceptable Action** | The least that still advances the sale, with a note of what failing to get it would mean | GS002 |
| 3 | **Buyer's Concept** | Hypothesis in the buyer's words, with source and confidence. If unknown, finding it is the call's objective | GS004 |
| 4 | **Known / assumed / unknown** | Facts cited; assumptions to confirm are listed; unknowns the call must close | review |
| 5 | **Confirmation questions** | Verify what we believe so the call starts from shared ground | GS003 |
| 6 | **New information questions** | Open, about Concept, criteria, process and others who matter | GS003 |
| 7 | **Attitude questions** | Reveal mode, priorities and personal stake without prying into private life | GS003 |
| 8 | **Commitment questions** | Test readiness and earn small agreements toward the BAC | GS003 |
| 9 | **Basic issue questions** | Reach the issue under the problem: cost of inaction, what is at stake | GS003 |
| 10 | **Get before give** | The give section follows from the Concept and says when each item is shown, only after it is confirmed | review |
| 11 | **Obstacles** | Likely obstacles with whose they are, a response and proof | review |
| 12 | **Recap** | Closing restatement of who does what by when | review |
| 13 | **Debrief** | Post-call section filled within 24 hours once the call has happened | GS005 |

## Verdict

- **Ready:** no Fail on rows 1 to 3; at most two Weak overall.
- **Fix before the call:** list what to change. A call without a BAC is a visit.

## Common problems to name

Giving a demo before the Concept is known; questions that lead the buyer; a BAC that is the seller's wish rather than the buyer's readiness; one question per type only; no way to tell if the call worked.
