# Platform adapters

Sales-OS is written once, in `core/`, in the open Agent Skills format. `python3 tools/sos.py build` compiles it for each platform. This folder explains how to use each result.

| Platform | What you use | Guide |
|---|---|---|
| Gemini app (consumer and Workspace) | One zip per skill from `dist/gemini-app/zips/` | `google/gemini-app-and-workspace.md` |
| Gemini Notebook (NotebookLM) | Source packs from `dist/notebook-packs/` | `google/gemini-notebook.md` |
| Gemini Enterprise | Skills upload, Workflow Builder, connectors | `google/gemini-enterprise.md` |
| Gemini CLI | `.agents/skills/`, `.gemini/commands/sos/`, `AGENTS.md` | `google/gemini-cli.md` |
| Antigravity CLI | The same `.agents/skills/` folder | `google/antigravity-cli.md` |
| Microsoft 365 Copilot Cowork | One zip per skill from `dist/microsoft/zips/` | `microsoft/copilot-cowork.md` |
| Copilot Agent Builder and Copilot Studio | Three 8-skill agent presets from `dist/microsoft/agent-presets/` | `microsoft/copilot-studio-and-agent-builder.md` |
| Copilot Notebooks | Source packs from `dist/notebook-packs/` | `microsoft/copilot-notebooks.md` |
| GitHub Copilot in VS Code | `.agents/skills/` | `microsoft/github-copilot-and-vscode.md` |
| Claude Code and Claude apps | `.claude/skills/`, `dist/claude-plugin/` | `claude/README.md` |
| Cursor, Codex and other Agent Skills clients | `.agents/skills/` and `AGENTS.md` | `cursor-codex/README.md` |
| Any chat tool without skills (ChatGPT, Copilot Chat, Grok, others) | `dist/portable/` prompts | `chat-only/README.md` |
| Grok | Legacy builder guide | `grok/building-sales-agents.md` |

**Start with Google.** The first client uses Google. Read `google/README.md` first: it has the three adoption tiers, a rollout order, and the facts that change fast. For a Microsoft 365 client read `microsoft/README.md`: same three tiers, Cowork as the native skills surface, and its own dated fact sheet.

## What every platform gets

The same rules, the same methodology and the same output structures. What differs is what the platform can do: files, shell, web, connectors. Skills detect this at run time (`core/shared/capabilities.md`) and degrade to chat-only output when needed.

## What not to do

Do not edit `.agents/skills`, `.claude/skills`, `.gemini/commands` or `dist/` by hand. Edit `core/` or `local/skills/` and rebuild. `python3 tools/sos.py build --check` fails if generated files have drifted.
