---
name: crm-contract
description: Platform-neutral contract for reading from and writing to a CRM
---

# CRM contract

Sales-OS is CRM-agnostic. It works with any CRM an agent can reach (Salesforce, HubSpot, Dynamics, others) through a connector or export. Principle: **the CRM is the system of record for pipeline facts; the sheets are the system of reasoning for strategy.** Do not duplicate everything into the CRM, and do not let the CRM overwrite analysis.

## What lives where

| Item | System of record | Notes |
|---|---|---|
| Opportunity stage, amount, close date, owner | CRM | Read into the sheet frontmatter; flag mismatches rather than silently overwriting either side |
| Contacts and contact roles | CRM, enriched by the sheet | Roles map below |
| Activities, emails, meetings | CRM or Google Workspace | Evidence for the sheet |
| **Response modes, Win-Results, support ratings, red flags, competitive counters, Coach identity** | **The sheet only** | Internal-only (`operating-rules.md` rule 4). CRM records are widely visible; do not copy these there |
| Strategy, action plans, SSO | The sheet | A short next step may be mirrored to the CRM |
| Blue Sheet link, last-reviewed date, coverage flags | Custom CRM fields | Safe summary fields below |

## Role mapping

| Sales-OS role | Salesforce Contact Role (suggested) | Notes |
|---|---|---|
| Economic Buyer | Economic Buyer (or Decision Maker) | Exactly one per opportunity |
| User Buyer | Business User | |
| Technical Buyer | Technical Buyer (or Evaluator) | |
| Coach | A custom picklist value "Coach" | Restrict visibility if the org shares contact roles with customers or partners |

HubSpot and others: use the nearest equivalent buying-role property or a custom property.

## Suggested custom fields (safe summary only)

| Field | Type | Purpose |
|---|---|---|
| Blue Sheet link | URL | Deep link to the sheet |
| Blue Sheet last reviewed | Date | Hygiene reporting |
| Economic Buyer identified | Checkbox | Forecast gate |
| Coach identified | Checkbox | Forecast gate |
| Open red flags | Number | Count only, no text |
| Red flags without action | Number | Hygiene |
| Funnel zone | Picklist: above, in, best-few | Pipeline view |
| SSO | Long text | Optional; same text the seller is comfortable sharing internally |

## Read flows

1. **Seed a Blue Sheet:** Opportunity, Contact Roles, last N activities, Account. Fill frontmatter and the Buying Influences names. Tag everything F with source "CRM". Do not infer modes or Wins from CRM data.
2. **Pre-call:** the person's contact record, recent activity, open tasks.
3. **Hygiene:** open opportunities with no next step, past-due close dates, no Economic Buyer role, no activity in N days. Compare against sheets.

## Write flows (always approval-gated)

1. Prepare the proposed change as a list: object, field, old value, new value, reason.
2. Show it. Wait for explicit approval.
3. Write only the approved fields. Report what was written.
4. Never write: modes, Win-Results, support, red-flag text, competitive counters, Coach identity, anything marked internal-only.

## Conflict handling

If the CRM and the sheet disagree (amount, close date, stage, contact), do not pick silently. Show both with their dates and ask which is current. Default to the CRM for pipeline fields and to the sheet for strategy.

## Permissions

The agent acts as the authenticated user. Respect sharing rules and field-level security. If the CRM refuses a read, report it and continue without that data.
