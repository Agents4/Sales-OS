# GitHub Copilot and VS Code

For revenue operations, sales engineers and anyone who maintains Sales-OS. VS Code with GitHub Copilot reads Agent Skills from the same folders the other Agent Skills clients use, so Sales-OS needs no special build for it.

## Where VS Code finds skills

| Scope | Folders |
|---|---|
| Project (in the repository) | `.github/skills/`, `.claude/skills/`, `.agents/skills/` |
| Personal (home folder) | `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/` |

Each skill is a folder with a `SKILL.md`. The `name` in the frontmatter must match the folder name; Sales-OS skills already do. Names use lowercase letters, numbers and hyphens, maximum 64 characters; descriptions up to 1,024 characters.

The Sales-OS build writes `.agents/skills/` and `.claude/skills/`, so a checked-out Sales-OS folder works as soon as you open it in VS Code. In a monorepo, VS Code can also find skills in a parent repository if `chat.useCustomizationsInParentRepositories` is on.

## Use

1. Open the folder that contains your `workspace/` in VS Code with GitHub Copilot enabled.
2. In chat, type `/` and pick a skill, for example `/mh-blue-sheet`, then add context: `/mh-call-debrief for the Contoso call on Tuesday`.
3. Or just ask. Copilot matches your request to a skill description and loads it.

Set a skill to manual-only with `disable-model-invocation: true` and hide it from the menu with `user-invocable: false` in its frontmatter. Sales-OS does not set these by default.

## Run the tools

In VS Code the agent can run terminal commands. Ask:

- `Run python3 tools/sos.py lint and fix only what is wrong in workspace/accounts/contoso.`
- `Run python3 tools/sos.py pipeline --format csv --out pipeline.csv and summarize the stale deals.`
- `Run python3 tools/sos.py build --check.`

The Python tools run on your computer and have file access. This is the surface where lint, pipeline reports, notebook-pack builds and release builds all work.

## Authoring and building

1. Copy a skill from `core/skills/` or run `sos-skill-author`, edit it, then `python3 tools/sos.py validate`.
2. `python3 tools/sos.py build` rewrites all generated folders. `build --check` must pass before you commit.
3. Do not edit `.agents/skills/` by hand. Edit `core/` or `local/skills/`.

## Settings you may meet

- `chat.agentSkillsLocations` still works, but Microsoft recommends the default folders because Copilot CLI and the Copilot app do not inherit editor settings.
- Forked skill context (`context: fork`) is experimental and needs the `github.copilot.chat.skillTool.enabled` setting.
- The customization marketplace for installing skills is experimental and needs `chat.customizations.marketplace.enabled`.

Do not put client data in a public repository. The `.gitignore` shipped with Sales-OS already excludes `workspace/accounts/*` and `workspace/outputs/*`.

Visual Studio and GitHub Copilot on other surfaces also list Agent Skills support. Their discovery paths were not confirmed for this guide; check their documentation before relying on them.
