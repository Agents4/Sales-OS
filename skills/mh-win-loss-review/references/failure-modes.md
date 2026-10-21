---
name: failure-modes
description: The mistakes that quietly break Miller Heiman in practice, with the fix and lint code for each
---

# Failure modes and fixes

Written from how the method is commonly misapplied, plus how AI assistants misapply it. The right-hand column shows where Sales-OS catches it. Tag **[X]**.

| # | Failure | Why it hurts | Fix | Catch |
|---|---|---|---|---|
| 1 | Treating a title as the Economic Buyer ("the VP signs") | You map the wrong person and the real decision-maker surprises you | Ask who can release funds and veto; confirm from two sources | BS003 |
| 2 | More than one Economic Buyer | Dilutes the plan; usually Users or Technical Buyers with strong voices | Exactly one. Re-label the others. | BS003 |
| 3 | A friendly contact called the Coach | No real intelligence or access; the map is fiction | Run the three Coach tests; ask for unwelcome news | `signals-library.md`, `mh-coach-development` |
| 4 | One Coach only | Single point of failure if they change roles or lose influence | Develop a second source | RF in Blue Sheet |
| 5 | Business result in the Personal win column | The deal looks covered but the human motive is missing | Separate Result and Win; if the Win is blank, treat as a red flag | BS006 |
| 6 | Inventing a Win to fill the cell | Manipulation risk and wrong strategy | Mark Unknown and write the question that would reveal it | BS014, evidence tags |
| 7 | Modes never updated | Plans age; a Trouble buyer becomes Even Keel after a quick fix | Re-assess after each interaction; date it | BS016 |
| 8 | Even Keel or Overconfident Economic Buyer on a Best Few deal treated as supportive | Forecast assumes a buyer who is not ready | Move the mode or move the forecast | BS013 |
| 9 | Red flags listed, no actions | A list of worries is not a plan | Every red flag gets at least one dated, owned action | BS007 |
| 10 | Actions without owner or date | Wishes | Owner and ISO date or it does not count | BS008, BS009 |
| 11 | A strength used to offset a flag on a different influence | "We have a great Coach" does not fix an unmet Economic Buyer | Pair each flag with an action on that influence | review |
| 12 | Vague Single Sales Objective | Nobody can tell if you are winning | Account, scope, value or quantity, date; apply the colleague test | BS002 |
| 13 | Two opportunities in one sheet | Muddy strategy and conflicting actions | One SSO per sheet; split | review |
| 14 | No status quo in the competition | The strongest competitor is ignored | Always add status quo and internal build | BS018 |
| 15 | Single- or double-threaded Best Few deal | Fragile to any personnel change | Map and engage User, Technical and Economic Buyers | BS012 |
| 16 | Sheet filled once, never re-walked | The map is fiction within weeks | Weekly re-walk for Best Few; stale lint | BS010 |
| 17 | Giving information before getting information | You pitch to a Concept you assumed | Plan confirmation, new-information and attitude questions first | GS003 |
| 18 | Call without a Best Action Commitment | "Let's keep in touch" | Write BAC and MAA before every important call | GS002 |
| 19 | A Gold Sheet with only things to do | A task list, not a strategy | Add at least one Stop investment | AS009 |
| 20 | Single Sponsor, no Anti-Sponsor check | The account's fate rides on one executive | Name the Critical Vulnerability; build a second Sponsor | AS002, AS005, AS006 |
| 21 | Buyer-facing material leaks internal analysis | Burns the Coach and the deal | Internal-only items never appear in buyer artifacts (`operating-rules.md`) | `mh-mutual-action-plan` gate |
| 22 | Recording private-life details as Wins | Privacy and ethics breach | Work-relevant motives only | operating rules |
| 23 | Sheet confidence higher than the evidence | Overconfident forecasts | Tag F/I/A/U; count assumptions; show confidence | evidence tags |
| 24 | AI fills blanks with plausible text | Fabricated stakeholders and numbers | "A blank field is a finding"; refuse to invent; cite sources | operating rules, evals |
| 25 | Applying the full method to a small deal | Seller backlash; sheets go stale | Use the qualification card below the client's threshold | `funnel-and-pipeline.md` |
