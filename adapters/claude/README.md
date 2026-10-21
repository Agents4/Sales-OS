# Claude

## Claude Code

1. Open the Sales-OS folder. `CLAUDE.md` imports `AGENTS.md`.
2. Skills are in `.claude/skills/` (generated). Ask in plain language or call a skill by name.
3. For a shareable install across projects, use `dist/claude-plugin/` as a local plugin or publish it to a plugin marketplace. Plugin skills are namespaced `sales-os:<skill>`.
4. Claude Code has files, shell and often web access, so the Python tools and research skills work fully.

## Claude apps (web, desktop, mobile)

Skills can be uploaded as zips from `dist/gemini-app/zips/` (the same self-contained layout) where your plan supports skills. Otherwise use the portable prompts (`chat-only/README.md`) or a Claude Project with `dist/portable/system-prompt.md` as the instructions and skill files as knowledge.

## Tips

- Run `python3 tools/sos.py validate` after changing a skill and `build` to regenerate the folders.
- Subagents let `mh-stakeholder-review` run lenses in parallel.
