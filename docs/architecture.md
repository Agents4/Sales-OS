# Architecture

## Goals

1. One source, many platforms. Write a skill once; run it on Gemini, Claude, Cursor, Codex or plain chat.
2. Robust when capabilities differ: files, shell, web, connectors, subagents may or may not exist.
3. Product separate from client data, so upgrades never touch deal data.
4. Trustworthy: no invention, evidence tags, approval gates, privacy by default.
5. Maintainable by a small team: validation, deterministic builds, evals.

## Layers

```
core/methodology   knowledge: what the method says and how it fails
core/shared        rules every skill follows; CRM contract; capability handling
core/templates     sheet and document structures, with fictional examples
core/rubrics       review criteria tied to lint codes
core/lenses        stakeholder viewpoints for reviews
core/skills        the actions: 22 Agent Skills
core/notebook-packs  definitions for Gemini Notebook source packs
core/scaffold      starter workspace for a new client
tools/sos          python standard library: validate, build, lint, pipeline, packs, instances
adapters           per-platform guides
```

## Skill format

Skills follow the open Agent Skills format: a folder with `SKILL.md` (YAML frontmatter, Markdown body) and optional `references/` and `assets/`. This is the format Gemini, Antigravity, Claude Code and others read, so the canonical source is also the deliverable.

Skills are self-contained after build. A skill lists shared files in `metadata.includes`; the build copies them into the skill (`templates/` to `assets/`, everything else to `references/`). That is what lets a single zip carry a skill into the Gemini app, where nothing outside the zip is visible.

Progressive disclosure keeps context small: only name and description load at start, the body loads on use, references load when read.

## Capabilities and degradation

Skills never assume. They check for files, shell, web, Google, CRM and subagents, use what exists and degrade to chat-only output when not (`core/shared/capabilities.md`). The Gemini app is the strict case: no files, no shell, no network.

## Build

`python3 tools/sos.py build` reads `core/skills` and `local/skills`, validates them, and generates:

| Target | Output |
|---|---|
| agents | `.agents/skills/` for Gemini CLI, Antigravity CLI, Codex, Cursor |
| claude | `.claude/skills/` |
| gemini-cli | `.gemini/commands/sos/*.toml`, `.gemini/settings.json` (created only if missing) |
| gemini-app | `dist/gemini-app/zips/*.zip` and `INSTALL.md` |
| gemini-extension | `dist/gemini-extension/` |
| claude-plugin | `dist/claude-plugin/` |
| portable | `dist/portable/` system prompt and single-file skills |
| notebook | `dist/notebook-packs/` static packs |

Copies, not symlinks (Drive and zip friendly). Output is deterministic (zips use a fixed date), so `build --check` can detect drift in CI or in `doctor`. Each generated folder carries a manifest naming what is managed.

## Product versus instance

The product is this repository. A client instance is a copy made by `new-instance`: product files plus the client's `workspace/` and `local/skills/`. `upgrade-instance` refreshes product files and leaves `workspace/` and `local/` untouched. `release` produces a tarball without client data.

## Data flow

```
sources (notes, transcripts, CRM, Meet notes)
        |
   skills read workspace/context-library + sheets
        |
  living sheets (workspace/accounts/...)   <-- lint, pipeline report
        |
  debriefs, reviews, drafts (workspace/outputs)
        |
  lessons (context-library/lessons.md) -- approved --> rules, local skills, core changes
```

Nothing outward happens without approval: no sending, no CRM writes, no sharing.

## Trust boundaries

Internal-only: modes, Wins, support, red flags, Coach identity, competitor assessments, forecast, pricing strategy. Buyer-facing artifacts pass a leak check. The CRM gets only safe summary fields (`core/shared/crm-contract.md`).

## Testing

`validate` checks skills against the spec, resolves references, checks links and eval cases. `selftest` runs lint against fixtures. `evals/` holds realistic cases scored with a rubric, to catch behavior regressions after a skill change.
