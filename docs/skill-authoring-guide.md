# Skill authoring guide

The full conventions live with the skills so every build can include them: `core/shared/skill-authoring.md`. In short:

- Folder name equals `name`; `mh-` for methodology, `sos-` for system skills.
- The `description` routes the skill; say what it does and "Use when ...".
- Sections: When to use, Inputs, Procedure, Output, Quality gate. Under 500 lines.
- List shared files in `metadata.includes`; reference them as `references/<file>` or `assets/<file>`.
- State the rules that matter: never invent, approval gates, internal versus buyer-facing, capability fallbacks, chat-only output.
- No scripts inside skills. Code lives in `tools/`.
- Test: `python3 tools/sos.py validate`, run an eval case, `build`, `build --check`.

The `sos-skill-author` skill walks through the process interactively.
