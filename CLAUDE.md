@AGENTS.md

## Claude Code notes

- Skills are in `.claude/skills/` (generated from `core/skills/`). Use `/sos-start` to begin, or ask in plain language.
- Edit `core/`, then `python3 tools/sos.py build`. Do not edit generated folders.
- Run `python3 tools/sos.py validate` after changing a skill and `python3 tools/sos.py lint` after changing a sheet.
