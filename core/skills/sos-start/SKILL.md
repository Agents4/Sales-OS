---
name: sos-start
description: "Orient a user to Sales-OS and route them to the right skill for their situation. Use when the user is new, asks what Sales-OS can do, says help, or describes a sales task without naming a skill."
compatibility: "Any Agent Skills client. No files or tools needed."
metadata:
  version: "1.0.0"
  layer: system
  last_reviewed: "2026-10-17"
  includes: "shared/operating-rules.md, shared/capabilities.md"
---

# Start here

Sales-OS is a library of skills for complex B2B sales, built on the Miller Heiman methodology: Strategic Selling (Blue Sheet, one opportunity), Conceptual Selling (Green Sheet, one conversation) and the Large Account Management Process (Gold Sheet, one strategic account).

Read `references/operating-rules.md` for the rules every skill follows. Check `references/capabilities.md` to see which abilities are available in this session, so you offer only what works.

## When to use

- The user is new and asks what this can do.
- The user describes a sales situation but not a skill.
- The user is unsure which sheet or review they need.

## Procedure

1. **Ask one question** if the situation is unclear: "What are you trying to get done: prepare for a call, understand a deal, review a deal, plan an account, or something else?" If it is clear, skip it and route.
2. **Route** using this table. Name the skill and what it will produce. Offer to start it.

| Situation | Skill |
|---|---|
| New or messy opportunity; who is the Economic Buyer; what are the risks | `mh-blue-sheet` |
| A call or meeting is coming up | `mh-green-sheet` |
| A call just happened; update the deal; draft the follow-up | `mh-call-debrief` |
| Plan or review a strategic account | `mh-gold-sheet` |
| "What am I missing?" before a call or review | `mh-red-flag-scan` |
| Challenge a forecast or review a deal | `mh-deal-review` |
| How will the CFO, IT or a competitor see this | `mh-stakeholder-review` |
| Is this contact a real Coach; no Coach yet | `mh-coach-development` |
| A competitor or no-decision risk | `mh-competitive-position` |
| Deal closed; learn from it | `mh-win-loss-review` |
| Weekly pipeline or forecast hygiene | `mh-pipeline-review` |
| Joint plan to share with the buyer | `mh-mutual-action-plan` |
| Write an email or note to a buyer | `mh-outreach-draft` |
| Is this lead worth pursuing; how much planning | `mh-icp-fit` |
| Background on a company before outreach | `mh-account-research` |
| Set up Sales-OS for a company | `sos-setup` |
| Check a sheet for quality | `sos-sheet-lint` |
| Build a Gemini Notebook source pack | `sos-notebook-pack` |
| Sync with CRM | `sos-crm-sync` |
| Add or change a skill | `sos-skill-author` |
| Propose improvements from experience | `sos-ratchet` |

3. **Say what you need** to start (for example "paste your notes on the deal"), and what you will produce. Offer a short path: draft first, then three questions.
4. **State the limits honestly.** If you have no file access, say that outputs will come as text for the user to save. If a skill needs a capability you lack, name it and offer the closest alternative.

## Output

A short reply: the recommended skill, why, what you need from the user, and what they will get. No long explanations. If the user is brand new, add three lines on what the three sheets are.

## Quality gate

1. You routed to a skill that exists in this installation.
2. You did not promise a tool or a file action you cannot perform.
3. You asked at most one question.
