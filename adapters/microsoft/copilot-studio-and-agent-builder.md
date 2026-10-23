# Agent Builder and Copilot Studio

Use these when a team wants one agent to open, with a fixed set of skills, instead of every seller uploading skills in Cowork. Both are skills-in-preview as of 2026-10-22. Read the limits before you design anything.

## The three presets

Each preset is one agent with at most 8 skills. They are generated into `dist/microsoft/agent-presets/<preset>/` with an `AGENT.md` that has the name, description and instructions to paste.

| Preset | For | Skills |
|---|---|---|
| `deal-coach` | A seller qualifying, preparing, debriefing and protecting a deal | `sos-start`, `mh-blue-sheet`, `mh-green-sheet`, `mh-call-debrief`, `mh-red-flag-scan`, `mh-stakeholder-review`, `mh-competitive-position`, `mh-mutual-action-plan` |
| `sales-manager` | Deal inspection, forecast challenge, coaching | `sos-start`, `mh-blue-sheet`, `mh-gold-sheet`, `mh-deal-review`, `mh-red-flag-scan`, `mh-pipeline-review`, `mh-win-loss-review`, `mh-coach-development` |
| `account-planner` | Strategic-account research, targeting and outreach | `sos-start`, `mh-gold-sheet`, `mh-blue-sheet`, `mh-account-research`, `mh-icp-fit`, `mh-stakeholder-review`, `mh-competitive-position`, `mh-outreach-draft` |

Presets live in `core/bundles.json` under `agent_presets`. `python3 tools/sos.py validate` fails if a preset has more than 8 skills or names an unknown skill.

## Agent Builder (Microsoft 365 Copilot)

**Status.** Custom skills in declarative agents are in preview, for organizations in the Microsoft Frontier Program. They are not available in tenants that use Purview Information Barriers. Partner Center publishing of agents with skills is not supported yet.

**Create the agent.**

1. In Copilot, choose **Agents & Skills > New agent**. Name it with the name from `AGENT.md` (max 30 characters) and paste the description (max 1,000 characters).
2. Paste the instructions from `AGENT.md` into the instructions field (max 8,000 characters).
3. Open the **Configure** tab, expand **Skills**, select **Add** and upload a zip from the preset folder. Repeat for each zip. Review the name, description and files each time.
4. Use **Try it** to test. Ask for something that should trigger one skill, for example a call debrief on a pasted transcript.
5. Share the agent with named people. Governance for agents is in the admin center.

**Limits (Agent Builder).**

| Item | Limit |
|---|---|
| Skills per agent | 8 |
| Skill instructions (`SKILL.md`) | under 20,000 characters (Sales-OS skills are 2,800 to 5,400 characters) |
| Zip | up to 50 MB; the package must be a `.zip` with `SKILL.md` at the root |
| File size | 25 MB per file |
| Files per package | 350 across all skills |
| Folder depth | 3 |
| Reuse across agents | not supported in preview: upload again per agent |
| Skills plus embedded files | not supported together yet |

Supported resource types include Markdown, text, JSON, YAML, CSV, Office files, PDF and images. Supported scripts: `.py`, `.js`, `.mjs`, `.cjs`, `.ts`, `.mts`, `.sh`, `.bash`. Scripts run in a sandbox with no network and no package install. Sales-OS ships no scripts in its zips, so this does not affect you.

**Do not combine** skills with uploaded knowledge files in the same agent until Microsoft lifts that limit. Put reference material in the skills (`references/`) or in a Notebook, and keep customer data in the user's own files.

## Copilot Studio

**Status.** The Skills component in Copilot Studio applies to agents built on the GitHub Copilot harness, which the creation article labels preview. The skills page does not state limits, so assume the Agent Builder limits and test.

**Upload.**

1. Open the agent in Copilot Studio, go to **Build**, then **Skills**.
2. In **Add skill** choose **Upload a skill** and drop a zip (or a single `.md` file). The system validates the file.
3. To update, edit the skill locally and replace the uploaded skill from the skills management page.

Using, building, testing and evaluating these agents can consume Copilot Credits. Set a budget before a pilot.

## Connectors for CRM data

Agents read pipeline data through connectors, not through the Python tools.

- **MCP servers and Federated Copilot Connectors.** Federated connectors reached general availability on 2026-09-23 (third-party summary of Microsoft message center items; verify in your Message center). A CRM vendor that offers an MCP server can connect this way. Cowork plugin manifests declare MCP servers under `agentConnectors` with `None`, `OAuthPluginVault` or `ApiKeyPluginVault` authentication.
- **Dynamics 365 Sales and Customer Service connectors** are enabled by default in Cowork and can be disabled in Power Platform Copilot Dataverse settings.
- **Salesforce and others.** Confirm with the client which connector exists for their CRM and who owns the sign-in. Each user completes the connector's own consent flow; nobody can sign in on behalf of users.

Rules that do not change: read first, draft second, write third, and only with approval. See `core/shared/crm-contract.md`.

## When not to use these

- If the client has no Frontier access and no GitHub Copilot harness agents, use Cowork skills (`copilot-cowork.md`) or the portable prompt in a plain agent. A plain Agent Builder agent with `dist/portable/system-prompt.md` as instructions and no skills works everywhere.
- If more than 8 skills are needed in one place, use Cowork. It has no stated skill-count limit (the 100-file limit applies per archive).
