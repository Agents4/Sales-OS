# Microsoft 365 and Copilot playbook

How to run Sales-OS on Microsoft's stack: Microsoft 365 Copilot, Copilot Cowork, Copilot Notebooks, Agent Builder, Copilot Studio, and GitHub Copilot in VS Code. Everything product-specific is dated and listed in `platform-facts.md` with sources and a verify list. Microsoft changes these products monthly. Check that file before a client session.

## Short version

- **Copilot Cowork is the one place in Microsoft 365 Copilot where Sales-OS skills run natively.** It takes the same `SKILL.md` zips as the other Agent Skills clients. Start there.
- Plain Copilot Chat has no skills. Use the portable system prompt and Copilot Notebooks for method coaching.
- Agent Builder and Copilot Studio can carry skills too, but with limits (8 skills per agent, preview status). Sales-OS ships three 8-skill agent presets for that.
- Developers and revenue operations can use GitHub Copilot in VS Code, which reads `.agents/skills/` directly.

## What is built for you

`python3 tools/sos.py build --target microsoft` writes `dist/microsoft/`:

| Path | What it is |
|---|---|
| `dist/microsoft/zips/<skill>.zip` | One zip per skill, `SKILL.md` at the root, companion files in `references/` and `assets/`. For Cowork and Agent Builder uploads. |
| `dist/microsoft/agent-presets/<preset>/` | Up to 8 zips plus `AGENT.md` (name, description and instructions to paste). Presets: `deal-coach`, `sales-manager`, `account-planner`. |
| `dist/microsoft/INSTALL.md` | Short upload instructions and the size table. |
| `dist/portable/` | Single-file prompts for Copilot Chat with no skills. |
| `dist/notebook-packs/` | Source packs for Copilot Notebooks. |

Never edit generated files. Edit `core/` or `local/skills/` and rebuild. `python3 tools/sos.py build --check` fails on drift.

## Three adoption tiers

They stack. Pick the tier that matches the client's licenses and IT policy.

### Tier 1: no deployment (day one)

For sellers with a Microsoft 365 Copilot license and nothing else.

- **Copilot Notebooks**: load the Methodology coach pack, then one notebook per key account. Guide: `copilot-notebooks.md`.
- **Copilot Chat with the portable prompt**: paste `dist/portable/system-prompt.md` into a chat or an agent, attach the skill files you need. Guide: `../chat-only/README.md`.
- **OneDrive or SharePoint** for the context library and living sheets. Guide: `onedrive-sharepoint-setup.md`.

Outcome: method coaching, call prep and debriefs in chat. Outputs are saved by hand. Fastest to adopt, least automation.

### Tier 2: skills in Cowork (admin-light)

For companies where Cowork is switched on. Guide: `copilot-cowork.md`.

- Admin confirms Cowork access (usage-based billing and a spending policy that selects Cowork) and, if wanted, deploys the skills as a managed plugin.
- Sellers upload the `seller-core` skills (or an admin shares them), then work in Cowork: prep, debrief, deal review, Blue Sheet maintenance.
- Cowork works with the user's own Microsoft 365 content and with the connectors the admin allows (verify which in `platform-facts.md`). Sales-OS rules still apply: draft, never send; ask before changing a system of record.

Outcome: skills with Microsoft 365 data access, shared with named people, governed and audited in Purview.

### Tier 3: managed agents and power users

For revenue operations, sales engineering and managers.

- **Agent Builder or Copilot Studio agents** built from the presets: a deal-coach agent for sellers, a manager agent for inspection. Guide: `copilot-studio-and-agent-builder.md`.
- **Connectors**: a CRM connector (MCP or Copilot connector) so agents read pipeline data. Draft first, write later.
- **GitHub Copilot in VS Code** to run the Python tools (lint, pipeline report, notebook-pack builder, build). Guide: `github-copilot-and-vscode.md`.

Outcome: scheduled and on-demand flows, agents the whole team can open, and the full tool set for the people who maintain it.

## Which surface for which job

| Job | Best surface | Why |
|---|---|---|
| Learn and ask about the method | Copilot Notebooks | Grounded in the method sources; no setup |
| Prepare a call, debrief, update a Blue Sheet | Cowork with skills | Reads mail, meetings and files; skills hold the procedure |
| Inspect a deal or the pipeline | Cowork, or the manager agent | Needs several sheets and the CRM view |
| Same workflow for a whole team, with a fixed set of skills | Agent Builder or Copilot Studio agent | One agent to open, controlled skills |
| Lint sheets, build packs, build skills | VS Code with GitHub Copilot, or a terminal | Python tools need a shell |
| No skills available at all | Copilot Chat with the portable prompt | Works anywhere |

## Recommended rollout order

1. Admin: confirm licenses, Cowork access, the plugin and skill sharing settings, and whether the tenant uses Purview Information Barriers (they block custom skills and plugin sharing). See the verify list in `platform-facts.md`.
2. `onedrive-sharepoint-setup.md`: put the Sales-OS folder on OneDrive or a SharePoint library with the right sync settings.
3. Load the **Methodology coach** notebook and run a 45-minute enablement session.
4. Pick one pilot team and one live deal per seller. Upload the seller-core skills in Cowork. Run `sos-setup`, then `mh-blue-sheet`.
5. Add call prep and debrief to the weekly routine (`mh-green-sheet`, `mh-call-debrief`).
6. Add a manager cadence (`mh-deal-review`, `mh-pipeline-review`).
7. Add the preset agents and a CRM connector once the data hygiene is good enough to automate.

See `docs/rollout-playbook.md` for the full plan, roles and KPIs.

## Governance specific to Microsoft

- **Who can see what.** Cowork tasks run as the user who created them and see only that user's data. Do not rely on a skill to hide data; fix permissions in SharePoint.
- **Sensitivity labels.** The skill sandbox for agents retains and honors sensitivity labels. Do not label the methodology files "Confidential" unless you want to restrict who can use them.
- **Audit.** Cowork and plugin interactions appear under Copilot activities in Purview audit logs.
- **Approval gates.** Cowork asks before it sends mail, posts messages or changes shared systems. Keep that default. Do not pre-authorize sending for sales outreach.
- **Models.** Cowork can use Anthropic models. Admins can turn the Anthropic model family on or off in Copilot Settings. Check what your data-residency and compliance reviewers have approved.
- **Internal-only boundary.** Sales-OS output marked internal-only (motives, red flags, coaching) must never go into a buyer-facing email, a Teams message to the customer or a shared mutual action plan. The skills enforce this; reviewers should still check.
- **Trademark and licensing.** Confirm internal use of Miller Heiman terminology and sheet structure with the rights holder. See `docs/security-and-governance.md`.

## What not to do

- Do not paste real customer data into a surface that your policy has not approved.
- Do not upload the whole product folder as a single skill. One skill per zip.
- Do not edit generated folders or `dist/`. Edit the source and rebuild.
- Do not expect Python tools to run inside Cowork, Agent Builder or Copilot Chat. Skills fall back to chat-only output and say so. Run the tools from a terminal or VS Code.
- Do not treat third-party blog claims about Copilot as fact. Every claim in `platform-facts.md` carries a source and a confidence rating.

## Files in this folder

| File | Contents |
|---|---|
| `copilot-cowork.md` | Skill upload, sharing, admin deployment, billing, approval gates |
| `copilot-studio-and-agent-builder.md` | The three agent presets, limits, connectors |
| `copilot-notebooks.md` | Source packs and the account room pattern |
| `onedrive-sharepoint-setup.md` | Folder layout, sync, permissions |
| `github-copilot-and-vscode.md` | Skill folders, running the tools |
| `platform-facts.md` | Dated facts, sources, verify list |
