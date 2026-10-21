# Cursor, Codex and other Agent Skills clients

Any client that reads `AGENTS.md` and the shared `.agents/skills/` folder works without further setup.

1. Open the Sales-OS folder as the workspace.
2. `AGENTS.md` provides the rules and the routing table. Skills are in `.agents/skills/<name>/SKILL.md`.
3. Ask for a task in plain language; the client picks the skill from its description, or name it explicitly.
4. If your client uses a different skills folder, point it at `.agents/skills/` or copy that folder to the location your client expects. Do not edit the copies by hand; rebuild instead.

These clients usually have files and shell, so lint, pipeline and notebook-pack all work.
