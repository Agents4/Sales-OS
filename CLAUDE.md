@AGENTS.md

## Claude Code notes

- Skills are in `.claude/skills/` (generated from `core/skills/`). Use `/sos-start` to begin, or ask in plain language.
- Edit `core/`, then `python3 tools/sos.py build`. Do not edit generated folders. In this repository the root `GEMINI.md`, `gemini-extension.json`, `skills/` and `commands/` are generated too.
- Adding a skill: follow the checklist in `core/shared/skill-authoring.md`. `python3 tools/sos.py doctor` checks the registries in `os.manifest.json`.
- Run `python3 tools/sos.py validate` after changing a skill and `python3 tools/sos.py lint` after changing a sheet.
