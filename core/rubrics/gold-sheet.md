---
name: rubric-gold-sheet
description: Review rubric for a Gold Sheet (LAMP account plan), with lint codes
---

# Rubric: Gold Sheet

Score each criterion **Pass / Weak / Fail**. Run `python3 tools/sos.py lint <file>` when a shell is available.

| # | Criterion | Pass looks like | Lint |
|---|---|---|---|
| 1 | **Field of Play** | A segment of the account that acts independently and where we can contribute significantly; scope and exclusions stated | AS001 |
| 2 | **Sponsor** | At least one named, with evidence that they promote us and counter competitors. Preferably two | AS002, AS005 |
| 3 | **Strategic Coach** | Named; helps us understand how the Field of Play decides | AS003 |
| 4 | **Anti-Sponsor** | Named, or "None identified" with how we checked | AS004 |
| 5 | **Relationships vs org chart** | Players have strength, an internal owner and the next action; not a list of titles | review |
| 6 | **Trends and KPIs** | The customer's own priorities in their language, not our product language | review |
| 7 | **Strategic Strengths** | What the Field of Play values and competitors cannot easily match | review |
| 8 | **Critical Vulnerability** | One real weakness that would cripple our position, with a plan. Single-sponsor dependency is common | AS006 |
| 9 | **Buy-Sell Hierarchy** | Customer's view and ours (1-5) with evidence; a desired level; the customer decides the level | AS008 |
| 10 | **Charter Statement** | Mutual, measurable, time-bound. Benefit to them and to us | AS007 |
| 11 | **Relationship Goals** | Tied to Strategic Players, opportunities and strengths | review |
| 12 | **Focus and Stop** | At least one of each; investments categorised. A plan with only things to do is a task list | AS009 |
| 13 | **Revenue targets** | Basis and confidence stated | AS010 |
| 14 | **SSOs linked** | Each linked to a Blue Sheet by path | AS011 |
| 15 | **Action plan** | Owners, dates, the customer purpose and completion evidence | review |
| 16 | **Cadence** | Reviewed within 60 to 90 days; next review set; trigger events defined | AS012 |

## Verdict

- **Ready:** no Fail on 2, 8, 10, 12; at most two Weak.
- **Otherwise:** list the top three fixes. For a single-threaded plan, the first fix is always a second Sponsor.
