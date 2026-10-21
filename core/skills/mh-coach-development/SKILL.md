---
name: mh-coach-development
description: "Test whether a contact is a real Coach and plan how to develop one, including a second source of internal information. Use when the user says they have a champion or friendly contact, has no Coach, wants to prepare a Coach conversation, or the Coach is leaving or untested."
compatibility: "Any Agent Skills client. File and shell access optional; works chat-only."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "lenses/coach.md, methodology/signals-library.md, templates/stakeholder-profile.md, shared/operating-rules.md, shared/capabilities.md"
---

# Coach development

A Coach is credible inside the organization, wants you to win, and gives you information you cannot get elsewhere. Friendliness is not enough. This skill tests the candidate, protects them, and plans the next conversation.

Read `references/operating-rules.md` and `references/capabilities.md`. Use `references/coach.md` for the coach lens and `references/signals-library.md` for signals. Use `assets/stakeholder-profile.md` to record the person.

## When to use

- The user names a champion and wants to know whether they are a Coach.
- There is no Coach or only one, and the user needs a plan.
- A Coach conversation is coming up.
- The Coach changes role, goes quiet or is at risk.

## Inputs

The candidate's name and role, how the user knows them, and what they have told the user so far. The Blue Sheet if there is one.

## Procedure

1. **Apply the three tests** with evidence:
   - Credible: do others inside respect them? How do you know? Do they have access to the decision?
   - Wants you to win: what do they gain? Is their Win linked to our success? Is it work-relevant and honest to serve?
   - Gives information you cannot get elsewhere: what have they told you that you could not have learned from the public, from a website or from sales material? Have they delivered unwelcome news?
2. **Classify.** Strong Coach, developing, untested, or not a Coach (a friendly contact, a Sponsor or an information source). Say why in two lines with evidence.
3. **Intel gaps.** What do you need that a Coach could provide: the real decision process, modes of the Economic Buyer and others, politics, timing, competitor position, the Economic Buyer's priorities.
4. **Plan the Coach conversation.** Three to five questions, in order, that move from confirmation to candor: for example how a decision like this is normally made, who else needs to be comfortable, what has gone wrong on similar projects, what would make them hesitate to recommend us, how we could be seen differently by the Economic Buyer. Never ask the Coach to decide your strategy or pricing, or to act beyond their influence.
5. **Test candor.** If they have not yet given unwelcome news, include one question that invites it, and plan to reward honesty rather than argue.
6. **Protect the Coach.** No attribution in anything the buyer could see. Agree how to communicate. Do not put their identity in CRM fields visible beyond the team.
7. **Second source.** Name a backup (another Coach candidate, a partner, a former employee, an adjacent leader) and one action to build it.
8. **Record.** Update the stakeholder profile and propose Blue Sheet changes through `mh-blue-sheet`.

## Output

Verdict (strong, developing, untested, not a Coach), evidence for each test, intel gaps, the Coach conversation plan, the backup plan, and proposed sheet updates. With file access write the profile to the deal folder; otherwise return it in one block.

## Quality gate

1. Evidence for every test. A "yes" without evidence is a "not yet".
2. Absence of a tested Coach is called out as a red flag with an action.
3. Work-relevant motives only. Nothing about their private life.
4. The Coach's identity and what they said stay internal.
