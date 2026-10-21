---
name: rubric-blue-sheet
description: Review rubric for a Blue Sheet, with lint codes
---

# Rubric: Blue Sheet

Score each criterion **Pass / Weak / Fail**. If a shell is available, run `python3 tools/sos.py lint <file>` first and fold the result in. The lint finds structure; this rubric judges quality.

| # | Criterion | Pass looks like | Lint |
|---|---|---|---|
| 1 | **SSO** | One account, one outcome, quantity or value, a date. A colleague could say on the date whether it was hit. | BS002 |
| 2 | **Economic Buyer** | Exactly one named, with the reason they hold funds and veto, confirmed by two sources, or an explicit red flag with an access action | BS003 |
| 3 | **Coverage** | Economic, User, Technical and Coach roles each named or flagged; Best Few is not single- or double-threaded | BS004, BS012 |
| 4 | **Coach** | Passes the three tests (credible inside, wants us to win, gives information we could not get elsewhere); has delivered unwelcome news | review |
| 5 | **Modes** | Mode per person, per issue, dated, with evidence. No Economic Buyer in Even Keel or Overconfident treated as a supporter | BS005, BS013, BS016 |
| 6 | **Support** | -5 to +5 or Unknown, never a guess; consistent with the mode | BS015 |
| 7 | **Win-Results** | Result and Win separated, work-relevant, evidenced, with confidence | BS006, BS014 |
| 8 | **Competition** | Includes status quo and internal build; buyer perception, not our opinion; a counter for each | BS018 |
| 9 | **Strengths** | Tied to an influence and used, not a list of features | review |
| 10 | **Red flags** | Honest and specific. A complex deal with none is suspect. Every strength is not offsetting a flag on a different influence | BS007 |
| 11 | **Action plan** | Every red flag has a dated, owned action; BAC and MAA stated for the next interaction | BS007, BS008, BS009, BS020 |
| 12 | **Unknowns** | Each has who can answer it and how to find out | review |
| 13 | **Decision process** | Approval path, criteria, required proof and gates, with lead times vs the runway | review |
| 14 | **Freshness** | Reviewed within the zone limit; modes verified within 60 days | BS010 |
| 15 | **Evidence discipline** | F/I/A/U tags, sources, no invented content; assumptions the plan depends on are listed | BS014 |

## Verdict

- **Ready to run:** no Fail; at most two Weak; no Weak on rows 2, 5, 7 or 11.
- **Needs work:** list the top three fixes, ordered by how much each changes the plan.
- **Not a sheet yet:** most rows Fail. Switch to interview mode.

## Review output

Verdict, the lint summary, a table of Weak/Fail rows with the specific fix for each, the three questions that would improve the sheet most, and any internal-only content that must not leave the building.
