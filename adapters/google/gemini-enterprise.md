# Gemini Enterprise

Status as of 2026-10-17 from Google's release notes and documentation. Verify with `platform-facts.md`.

## Skills

Custom skills are generally available in Gemini Enterprise. End users can create, upload and share skills. An admin turns on the skills and skill-sharing settings in Feature Management, and can approve sharing requests. Upload the zips from `dist/gemini-app/zips/` (the format is the open Agent Skills layout; if a zip is rejected, upload the folder from `.agents/skills/<name>/`). Google also publishes pre-built skill packs and describes skills as an open specification that works across Antigravity, Claude Code and other tools.

## Workflow Builder

Workflow Builder (formerly Agent Designer) is generally available. It supports scheduled and on-demand workflows, mentions of chat agents, importing A2A and ADK agents, and connectors including Drive, Gmail, Calendar, Chat, Slack, Jira, Microsoft Teams, Notion and Salesforce.

Useful Sales-OS workflows:

| Workflow | Trigger | What it does |
|---|---|---|
| Weekly pipeline hygiene | Weekly schedule | Reads Blue Sheets and the CRM, runs the `mh-pipeline-review` skill, posts the report to the manager |
| Pre-call brief | Calendar event with an external attendee | Reads the Blue Sheet and calendar entry, drafts the Green Sheet |
| Post-call debrief | Meet notes available | Drafts the debrief and a follow-up draft; waits for approval |
| Stale sheet nudge | Daily | Lists sheets past their review limit and asks the owner |

Design every workflow so it drafts and proposes. Anything outward (sending mail, writing the CRM) waits for a human approval step.

## Connectors and MCP

Custom MCP servers can be added as data stores (off by default, controlled by an organization policy). Gemini Enterprise reads tool definitions from the server. Use connectors for Drive, Calendar, Gmail and Salesforce. Follow `core/shared/crm-contract.md` for what to read and write.

## Governance

- Enable skill sharing deliberately: start with a pilot group, approve the shared set, then widen.
- Keep internal-only analysis out of shared spaces and out of CRM fields visible to customers.
- Use the audit trail and observability views to review what skills and agents did.
- Apply data protection policies to notebooks that hold deal material, where the organization uses them.
- Decide who may change shared skills. Treat skill changes like code: review, test with the eval cases, then release.

## Account fit

Gemini Enterprise, Gemini Code Assist Standard or Enterprise, and Workspace editions are different licenses. Confirm which the client holds before promising a feature; see `platform-facts.md`.
