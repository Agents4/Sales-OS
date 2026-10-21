---
name: sos-crm-sync
description: "Read opportunity, contact and activity data from a connected CRM to seed or reconcile Blue Sheets, and prepare approval-gated write-backs of safe summary fields. Use when the user wants to import a deal from the CRM, check sheets against the CRM, or update CRM fields from a sheet."
compatibility: "Needs a CRM connector, MCP server or an export file. Without one, works from pasted CRM data and produces change lists."
metadata:
  version: "1.0.0"
  layer: system
  last_reviewed: "2026-10-17"
  includes: "shared/crm-contract.md, shared/operating-rules.md, shared/capabilities.md"
---

# CRM sync

The CRM owns pipeline facts. The sheets own strategy. This skill moves the safe fields between them and never moves the internal-only ones.

Read `references/operating-rules.md` and `references/capabilities.md`. All field mappings, role mappings and write rules are in `references/crm-contract.md`; follow it.

## When to use

- Seed a Blue Sheet from an opportunity.
- Reconcile stage, amount, close date or contacts between the CRM and the sheet.
- Push the Blue Sheet link, review date and coverage flags to the CRM.
- Find opportunities with no Economic Buyer role or no next step.

## Inputs

An opportunity ID or name, or an export. The connector the user has approved. The sheet if it exists.

## Procedure

1. **Verify access.** Test the connector with a harmless read. If none exists, say so and ask for an export or a paste. Do not claim access you have not verified.
2. **Read** the opportunity, contact roles, account and recent activity. Respect the permissions of the authenticated user.
3. **Seed or reconcile.** For a new sheet, fill the frontmatter and Buying Influences names from the CRM, tagging them F with source "CRM". Do not infer modes, Wins or support from CRM data. For an existing sheet, compare each shared field and list differences: field, CRM value, sheet value, dates.
4. **Never choose silently.** Show conflicts and ask which is current. Default to the CRM for pipeline fields and the sheet for strategy.
5. **Prepare write-backs** as a list of: object, field, old value, new value, reason. Only the safe summary fields in the contract. Never modes, Win-Results, support, red flag text, competitive counters, Coach identity.
6. **Ask for explicit approval** before any write. Write only what was approved. Report exactly what was written, or that nothing was.
7. **Log.** Add a Change log row to the sheet for any change made to it.

## Output

A sync report: what was read, differences found, proposed changes, what was approved and written. Include the list of fields intentionally not copied and why, once.

## Quality gate

1. No write occurred without approval.
2. No internal-only content moved to the CRM.
3. Every conflict is shown with both values and dates.
4. Errors from the connector are reported verbatim and not retried blindly.
