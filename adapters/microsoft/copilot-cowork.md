# Copilot Cowork

Cowork is the Microsoft 365 Copilot surface that runs multi-step work and supports Agent Skills natively. Sales-OS skills upload as they are. Facts below are as of 2026-10-22; see `platform-facts.md` for sources and the verify list.

## What you need

- A Microsoft 365 Copilot license for each user (the plugin management page names this; check the SKU list with your reseller).
- Cowork enabled for the user. Cowork is generally available. Access comes from **usage-based billing plus a spending policy that selects Cowork** and includes the user. The old "Cowork" entry under Agents > All agents no longer controls access.
- For admins: the tenant administrator role or the Copilot administrator role.

Usage-based billing means model responses, tool and skill calls, image generation and browser tasks consume credits. Set per-user or per-group limits in the admin center. Plan a pilot budget before you roll out.

## Upload the skills (each seller, five minutes)

1. Build the zips: `python3 tools/sos.py build --target microsoft` (they are in `dist/microsoft/zips/`).
2. In Cowork choose **Customize**, then **Skills**. Open the arrow next to **Add** and choose **Upload skill**.
3. Pick one zip, for example `sos-start.zip`. Cowork validates it and saves it to your OneDrive. It appears under **Your skills** after sync, which can take a moment.
4. Repeat for the bundle you need. Seller bundle: `sos-start`, `sos-setup`, `mh-blue-sheet`, `mh-green-sheet`, `mh-call-debrief`, `mh-red-flag-scan`, `mh-coach-development`, `mh-stakeholder-review`, `mh-competitive-position`, `mh-mutual-action-plan`, `mh-outreach-draft`, `mh-icp-fit`, `mh-account-research`. The full lists are in `dist/microsoft/INSTALL.md`.
5. Open a Cowork chat and type `Start Sales-OS` or `Run sos-start`. The start skill asks what you want to do and routes to the right skill. Skills appear as chips in the side panel alongside built-in skills; the **Sources & Skills** panel toggles each one.

Limits for uploads: a zip up to 10 MB compressed, 50 MB unpacked and 100 files; a single `.md` skill up to 1 MB. Every Sales-OS zip is a few KB to tens of KB and under 12 files. If a skill with the same name exists, Cowork keeps both and adds a number to the new name. Delete the old copy first when you upgrade.

You can also create a skill by chatting: **Add** on the Skills tab starts a guided conversation. Prefer the zips for Sales-OS so every seller runs the same version.

## Share the skills with a team

1. Open a skill's detail page and select **Share**.
2. Choose **Specific users in your organization** (names or emails). A link can be copied from the same dialog.
3. Select **Apply**. After you change a shared skill, select **Re-share** to push the new version.

Sharing to specific people needs no admin approval and there is no tenant setting to turn it off. Org-wide publication stays pending until a tenant administrator approves it. Skills are instructions the AI follows, so only share skills from sources you trust. Put an owner and a version in your skill change log.

## Deploy as a managed plugin (admin)

For a whole team, an admin can distribute the skills so users do not upload anything.

1. Package a plugin. Cowork converts Claude-compatible plugin packages automatically when a user uploads them under **Customize > Plugins > Upload plugin**. The Claude plugin that Sales-OS builds is at `dist/claude-plugin/`; zip it and test the upload with one pilot user first. The plugin manifest declares skills under `agentSkills` and MCP servers under `agentConnectors`.
2. In the Microsoft 365 admin center go to **Agents > All agents** or **Tools**, open the plugin and choose **Installed for**: all users, or specific users and groups. Admin-deployed plugins show a **Managed by your organization** label and users cannot remove them (they can still turn them off on their device in Sources & Skills).
3. To restrict or block a plugin, use **Agents > Tools > the plugin > Users** and set it to all users, specific groups, or Block. Blocking applies to new conversations.
4. For internal-only packages, **Manage apps > Upload custom app** skips App Store validation and lets you assign the package to users, groups or everyone.

Purview Information Barriers are not supported for plugin or skill management and sharing. In those tenants skills cannot be uploaded or published. If the client uses Information Barriers, use the portable prompt in Copilot Chat instead.

## What works inside Cowork and what does not

| Capability | Status |
|---|---|
| Skill instructions, `references/`, `assets/` templates | Works. Companion files in the zip are kept. |
| Reading and writing files in OneDrive and SharePoint | Depends on the user's access and the Cowork environment. Test with a real account. |
| Running `python3 tools/sos.py` (lint, pipeline) | Do not assume it works. The skills detect missing capability and give a manual check. Run the tools from a terminal or VS Code. |
| Drafting email and Teams messages | Drafting works. Sending asks for approval by default. Keep that default. |
| Scheduled and event-driven tasks | Run as the user who created them, see only that user's data, and ask before sending, posting or changing shared systems. |
| CRM data | Via a connector (MCP or Copilot connector) the admin has approved. Otherwise export a CSV and paste or attach it. |
| Browser tasks | Run in Edge on the user's device under existing conditional access and DLP. Admins can turn this off with the Cowork Browsing setting. |

## Good first Cowork prompts

- `Run sos-start and tell me which skill to use for a discovery call tomorrow with Contoso.`
- `Run mh-call-debrief on this transcript. Mark every fact F, I, A or U and keep internal notes separate.`
- `Run mh-red-flag-scan on my Blue Sheet for Northwind and list what I must verify before next week.`
- `Run mh-pipeline-review on the attached CSV. Show only deals that changed stage this week.`

## Data handling

Per the admin page, Cowork processes files in a temporary, isolated environment inside the Microsoft 365 service boundary, deleted when the task ends. Purview provides compliance controls and audit. Anthropic models can be turned off in Copilot Settings and scoped to users or groups. The admin page does not describe region limits for Anthropic models; verify them with your Microsoft account team before putting regulated data through those models.

## Roll back and upgrade

1. Pull the new Sales-OS version, run `python3 tools/sos.py build --target microsoft`.
2. Delete the old copy of each changed skill in Cowork, upload the new zip, **Re-share**.
3. Keep `docs/` changelog notes so sellers know what changed.
