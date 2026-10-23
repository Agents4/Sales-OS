# Changelog

All notable changes to the Sales-OS product. Client data lives in `workspace/` and is not versioned here.

## 1.0.2 (2026-10-22)

- Microsoft 365 and Copilot implementation guide in `adapters/microsoft/`: playbook with three tiers, Copilot Cowork skills and admin deployment, Agent Builder and Copilot Studio, Copilot Notebooks, OneDrive and SharePoint setup, GitHub Copilot in VS Code, and a dated fact sheet with sources and a verify list.
- New build target `microsoft` (`dist/microsoft/`): one upload zip per skill, three 8-skill agent presets with ready-to-paste agent names, descriptions and instructions, and an install note. The build warns when a zip exceeds a Cowork upload limit.
- `core/bundles.json` gains `agent_presets`; `validate` checks that each has at most 8 skills (SK083, SK084).
- `new-instance --platforms microsoft`.

## 1.0.1 (2026-10-21)

- Gemini CLI extension published from a repository whose root is the extension (`python3 tools/sos.py export-extension <dir>`).
- Extension context explains how to call the bundled tools from a user's project folder.
- `lint`, `pipeline` and `notebook-pack` read `workspace/` from the current folder (or `--workspace`), so they work when Sales-OS is installed elsewhere.

## 1.0.0 (2026-10-17)

First robust release, replacing the original lightweight prototype (kept in `docs/legacy/`).

- Methodology knowledge base for Strategic Selling, Conceptual Selling and LAMP, with a fidelity ledger tagging each element as canonical, convention or Sales-OS extension.
- 22 skills: 15 methodology skills (Blue, Green, Gold, call debrief, deal review, red-flag scan, Coach development, stakeholder lenses, competitive position, win/loss, pipeline review, mutual action plan, outreach, ICP fit, account research) and 7 system skills (start, setup, sheet lint, CRM sync, notebook pack, skill author, ratchet).
- Templates with worked fictional examples, review rubrics, five stakeholder lenses and shared operating rules.
- `tools/sos.py`: validate, build, lint, pipeline, notebook-pack, new-instance, upgrade-instance, release, list, doctor, selftest. Python standard library only.
- Platform builds from one source: Gemini CLI, Antigravity CLI, Codex and other Agent Skills clients, Claude Code, Gemini app and Workspace zips, a Gemini CLI extension, a Claude plugin, portable prompts, and Gemini Notebook packs.
- Four skill bundles: seller-core, manager, strategic-accounts, revops.
- Evaluation cases and rubric.
