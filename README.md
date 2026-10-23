# Sales-OS: Gemini CLI extension

Miller Heiman sales skills for Gemini CLI: Blue, Green and Gold Sheets, call debriefs, deal and pipeline reviews, stakeholder lenses, Coach development, buyer-safe drafts and more. 22 skills, one source, tested rules: never invent, tag evidence, approval before anything outward, internal analysis never reaches the buyer.

## Install

```
gemini extensions install https://github.com/Agents4/Sales-OS
```

Restart the CLI, then try `/sos:start` (or just describe the deal). Then `/sos:setup` to fill in company facts, and `/sos:blue-sheet` on a live deal.

Update later with `gemini extensions update sales-os`. For development, link a local checkout: `gemini extensions link <path>`.

Notes:
- Gemini CLI serves enterprise Gemini Code Assist licenses and API-key use. Individual Google AI accounts moved to Antigravity CLI; there, import the extension with `agy plugin import gemini`, or use the skills in `.agents/skills` (see `adapters/google/`). Verify current status in `adapters/google/platform-facts.md`.
- Data stays in your project folder (`workspace/`). The extension never writes into its own folder.
- The Python tools are bundled (Python 3.8+, standard library only). Inside the extension the context file tells the agent how to call them.
- Methodology names belong to their owner; this is an original synthesis. See `core/methodology/fidelity-ledger.md` before marketing under that name.

---

# Sales-OS

An agentic operating system for complex B2B sales, built on the Miller Heiman methodology: Strategic Selling (Blue Sheet), Conceptual Selling (Green Sheet) and the Large Account Management Process (Gold Sheet).

It is a library of skills, templates, rubrics and tools that any AI assistant can use. Written once, it runs on Google first (Gemini app, Gemini Notebook, Gemini Enterprise, Gemini CLI, Antigravity CLI), on Microsoft 365 Copilot (Cowork, Agent Builder, Copilot Studio, Notebooks, GitHub Copilot in VS Code), and also on Claude, Cursor, Codex and plain chat tools.

## What a seller gets

| I want to | Skill |
|---|---|
| Turn messy notes into a deal plan | `mh-blue-sheet` |
| Prepare for a call | `mh-green-sheet` |
| Capture a call and draft the follow-up | `mh-call-debrief` |
| Plan a strategic account | `mh-gold-sheet` |
| Find what I am missing | `mh-red-flag-scan` |
| See the deal through the CFO's, IT's or a competitor's eyes | `mh-stakeholder-review` |
| Test or build a Coach | `mh-coach-development` |
| Write a buyer-safe email or joint plan | `mh-outreach-draft`, `mh-mutual-action-plan` |

Managers get deal and pipeline reviews, forecast gates and win/loss reviews. Revenue operations get linting, CRM sync, notebook packs and a way to improve the system from real deals (`sos-ratchet`). `sos-start` routes anyone to the right skill. Full list: `AGENTS.md`.

## How it works

```
core/        the product: methodology, 22 skills, templates, rubrics, lenses, shared rules
tools/       python3 tools/sos.py: validate, build, lint, pipeline, notebook-pack, new-instance, doctor
workspace/   your data: context library, accounts, outputs (never overwritten by upgrades)
adapters/    how to run it on each platform; start with adapters/google/ or adapters/microsoft/
.agents/ .claude/ .gemini/ dist/   generated for each platform. Do not edit by hand
```

Four ideas keep it trustworthy:

1. **Never invent.** Unknown is a valid answer; every claim carries an evidence tag (fact, inference, assumption, unknown) and a source.
2. **Approval gates.** The system drafts. People send, share and write to systems.
3. **Internal versus buyer-facing.** Modes, personal wins, red flags, Coach identity and competitor analysis never reach the customer.
4. **Fidelity.** Every element is tagged canonical, convention or Sales-OS extension (`core/methodology/fidelity-ledger.md`).

## Quick start

1. Set this folder to **Available offline** in Drive for desktop (`adapters/google/drive-setup.md`).
2. Run `python3 tools/sos.py doctor`, then `python3 tools/sos.py build`.
3. Pick your surface in `adapters/google/README.md` (Google) or `adapters/microsoft/README.md` (Microsoft 365 and Copilot): notebooks and app skills need nothing installed; the CLIs and VS Code unlock the tools.
4. Say "start" to `sos-start`, then run `sos-setup` to fill in your company facts.
5. Build your first Blue Sheet on a live deal.

## For consultants and administrators

- New client: `python3 tools/sos.py new-instance <folder> --client "<Name>" --platforms google`.
- Upgrade a client: `python3 tools/sos.py upgrade-instance <folder>` (keeps `workspace/` and `local/`).
- Release: `python3 tools/sos.py release`.
- Rollout plan: `docs/rollout-playbook.md`. Governance: `docs/security-and-governance.md`. Architecture: `docs/architecture.md`.

## Methodology and rights

This is an original practitioner synthesis, not official Miller Heiman material. The names and official worksheets belong to their owner (Korn Ferry). Confirm licensing before marketing a deployment under the Miller Heiman name. See `core/methodology/fidelity-ledger.md`.

Version 1.0.0. See `CHANGELOG.md`. Earlier prototype files are preserved in `docs/legacy/`.
