# Gemini CLI

Status as of 2026-10-17. Google moved its terminal experience to Antigravity CLI. Gemini CLI stopped serving individual accounts (Google AI Pro, Ultra and free tier) on 2026-06-18. It remains available for enterprise users with Gemini Code Assist Standard or Enterprise licenses and for API-key authentication. Check `platform-facts.md` and the client's license before choosing this path. If the client's users are individuals or on a Workspace plan without those licenses, use Antigravity CLI instead (`antigravity-cli.md`). The skills are the same.

## What Sales-OS provides

| Item | Location |
|---|---|
| Context file | `AGENTS.md` (Gemini CLI reads it through `.gemini/settings.json`, created by the build if missing) |
| Skills | `.agents/skills/<name>/SKILL.md` (workspace scope) |
| Slash commands | `.gemini/commands/sos/<name>.toml`, called as `/sos:blue-sheet`, `/sos:green-sheet` and so on |
| Extension | `dist/gemini-extension/` for sharing across projects |

## Setup

1. Put the Sales-OS folder (or a client instance) on the machine, offline-available if on Drive (`drive-setup.md`).
2. Run `python3 tools/sos.py build` once. It writes the generated folders.
3. Open a terminal in the folder and start the CLI. It loads `AGENTS.md`. List skills with the skills command and confirm the `mh-` and `sos-` names appear.
4. Start with `/sos:start` or ask in plain language. Skills activate by name or when the request matches their description.

## Using the Python tools from the CLI

The CLI can run shell commands, so skills call `python3 tools/sos.py lint <file>` and `pipeline` directly. Python 3.8 or later, standard library only.

## Install as an extension from GitHub

```
gemini extensions install https://github.com/Agents4/Sales-OS
```

The repository root is the extension (`gemini-extension.json`, `GEMINI.md`, `skills/`, `commands/sos/`) next to the full source. Update with `gemini extensions update sales-os`. Maintainers regenerate it with `python3 tools/sos.py export-extension <folder>` and push the result.

## Sharing as an extension (local)

Install `dist/gemini-extension/` with the CLI's extensions install command, or link it while developing, then restart. The extension carries the skills, the commands and a context file built from `AGENTS.md`.

## Notes

- Project commands reference the skill by path so they work without activation; extension commands activate by name.
- Keep customer data on approved machines. A terminal agent can read everything in the folder.
