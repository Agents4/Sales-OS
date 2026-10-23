# Platform facts (as of 2026-10-22)

Everything product-specific in the Microsoft guides comes from here. Microsoft changes these products often. Before a client session, re-check the **verify list** at the bottom.

## Facts and sources

| # | Fact | Source | Confidence |
|---|---|---|---|
| 1 | Cowork is generally available. Access is by usage-based billing plus a spending policy that selects Cowork and includes the user. The Cowork entry under Agents > All agents no longer controls access. | Microsoft Learn: Manage Cowork for your organization (admin summary) | High |
| 2 | Cowork usage (model responses, tool and skill calls, images, browser tasks) consumes credits; admins set per-user or per-group limits and monitor usage in the admin center and the Consumption Dashboard. | Same | High |
| 3 | Cowork skill upload: Customize > Skills > Add arrow > Upload skill. Accepts a single `SKILL.md` as `.md` (up to 1 MB), or a `.zip` or `.skill` archive with `SKILL.md` at the root plus companion files (up to 10 MB compressed, 50 MB unpacked, 100 files). Frontmatter needs `name` and `description`. Duplicate names are kept and numbered. Skills are saved to the user's OneDrive. | Microsoft Learn: Customize Cowork | High |
| 4 | Cowork can create a skill through a guided chat (Add > Create new). Sharing: Only you, or specific users in the organization; copy a link; Re-share after changes. | Same | High |
| 5 | Cowork plugin upload takes a `.zip`. Claude-compatible plugin packages are converted automatically, including bundled skills and external connectors. | Microsoft Learn: Cowork plugins | High |
| 6 | Admins deploy plugins from the admin center (Agents > All agents or Tools > Installed for): everyone, specific groups, or available in the store. There is no single tenant setting that turns off sharing. Org-wide publication needs tenant admin approval. Blocking a plugin blocks it for everyone in the tenant, including recipients of a share. | Microsoft Learn: Admin management of Cowork plugins | High |
| 7 | Purview Information Barriers are not supported for plugin or skill management and sharing; in those tenants embedded knowledge uploads are blocked, so skills and plugins cannot be uploaded or published. | Same; Learn: declarative agent skills | High |
| 8 | Plugin manifests declare skills under `agentSkills` and MCP servers under `agentConnectors`; auth types are `None`, `OAuthPluginVault`, `ApiKeyPluginVault`. Users complete each connector's own consent flow. | Admin management of Cowork plugins | High |
| 9 | Cowork scheduled and event-driven tasks run as the user who created them. By default Cowork asks before it sends email, posts messages or changes shared systems. Files are processed in a temporary isolated environment inside the Microsoft 365 service boundary. Interactions appear in Purview audit logs (Audit Standard includes them). | Manage Cowork for your organization; Admin management of Cowork plugins | High |
| 10 | Admins can turn the Anthropic model family on or off in Copilot Settings, scoped to users or groups. Turning it off changes the models shown; it does not block Cowork. The page does not describe region restrictions for Anthropic models. | Manage Cowork for your organization | High for what it states; region limits unknown |
| 11 | Agent Builder custom skills are in preview for the Frontier Program, not available with Purview Information Barriers, not yet publishable through Partner Center. Package: `.zip` with `SKILL.md` (instructions under 20,000 characters). Limits: 8 skills per agent, 50 MB zip, 25 MB per file, 350 files, depth 3. Skills and embedded files cannot be combined yet. Scripts run in a sandbox with no network and no package install. | Microsoft Learn: Skills in Agent Builder; Custom skills in declarative agents | High |
| 12 | Agent Builder agent limits: instructions up to 8,000 characters, name up to 30, description up to 1,000. | Microsoft Learn (Agent Builder), retrieved earlier in this work | Medium (not re-fetched in this pass) |
| 13 | Copilot Studio: the Skills component applies to agents built on the GitHub Copilot harness. Upload a `.md` file or a `.zip` with `SKILL.md`. Size and count limits and GA status are not stated; the creation article is labeled preview. Use can consume Copilot Credits. | Microsoft Learn: add an existing skill (Copilot Studio) | Medium: limits unknown |
| 14 | VS Code and GitHub Copilot read skills from `.github/skills/`, `.claude/skills/`, `.agents/skills/` (project) and `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/` (personal). `name` must match the folder name. Slash-command invocation and automatic matching. | code.visualstudio.com: Agent Skills | High |
| 15 | Copilot Notebooks reference limit is reported as 100 references used for grounding; supported types include docx, pptx, xlsx, pdf, loop, page and OneNote. | Microsoft Q&A, an AI-generated answer that cites support articles | Low: verify |
| 16 | Copilot Notebooks sharing, licensing and availability are not confirmed in this guide. | Not verified | Unknown: verify |
| 17 | Federated Copilot Connectors (MCP-based) were announced to reach general availability; one summary dates it 2026-09-23. | Microsoft message center items summarized by third parties | Medium: verify in the client's Message center |
| 18 | Classic Copilot Chat has no native skills outside Cowork and Agent Builder. | Third-party articles | Low: verify with a real account |
| 19 | The Miller Heiman method terms and sheet structure are described in `core/methodology/fidelity-ledger.md`. | Secondary sources | See ledger |

## Verify list (do before a client session)

1. Which licenses does the client hold: Microsoft 365 Copilot, Copilot Studio capacity, GitHub Copilot? Is Cowork enabled for the pilot users, and is a spending policy that selects Cowork in place (facts 1, 2)?
2. Does the tenant use Purview Information Barriers? If yes, skills and plugin sharing are blocked and the fallback is the portable prompt (fact 7).
3. Upload `sos-start.zip` in Cowork with a real pilot account. Does it validate, appear under Your skills and trigger from a chat (fact 3)? Test a skill that uses `references/` and `assets/`, for example `mh-blue-sheet`.
4. Is the Frontier Program active for Agent Builder skills? Test the `deal-coach` preset (facts 11, 12).
5. Does Copilot Studio in the client's environment offer GitHub Copilot harness agents and the Skills tab, and what limits apply (fact 13)?
6. Can Cowork read and write the Sales-OS workspace in OneDrive or SharePoint, and does it run the Python tools? The guides assume it may not (copilot-cowork.md).
7. Which CRM connector exists and who approves it (fact 17)? Confirm Dynamics connector defaults.
8. Anthropic models: are they allowed for this client's data, and where are they processed (fact 10)? Ask the Microsoft account team.
9. Copilot Notebooks: current reference limits, accepted file types (is Markdown accepted?), sharing options and licensing (facts 15, 16).
10. Sensitivity labels and sharing policy on the Sales-OS libraries.
11. Licensing: confirm with the client's counsel and the rights holder that using Miller Heiman terminology and sheet structures internally is fine (see `docs/security-and-governance.md`).

## Sources

- Manage Cowork for your organization: learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-admin-governance
- Customize Cowork (upload a skill): learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-customize
- Cowork plugins: learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugins
- Admin management of Cowork plugins: learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-manage-plugins
- Skills in Agent Builder (preview): learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-skills
- Custom skills in declarative agents (preview): learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills
- Copilot Studio, add an existing skill: learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing
- VS Code, Agent Skills: code.visualstudio.com/docs/agent-customization/agent-skills
- Copilot Notebooks reference limits (unverified): learn.microsoft.com/en-us/answers/a/12638742
- Federated Copilot Connectors summaries (third party): m365admin.handsontek.net, mc.merill.net/message/RM501120
