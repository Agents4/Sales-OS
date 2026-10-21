# Antigravity CLI

Antigravity CLI is Google's terminal agent that replaced Gemini CLI for individual accounts (announced 2026-05-19; Gemini CLI stopped serving those accounts 2026-06-18). It keeps Agent Skills, hooks and subagents. Status as of 2026-10-17; verify with `platform-facts.md`.

## What Sales-OS provides

| Item | Notes |
|---|---|
| Skills | `.agents/skills/` in the workspace is the shared location Antigravity reads. Global skills live under `~/.gemini/antigravity-cli/skills/` |
| Context | `AGENTS.md` at the folder root. Memory files from Gemini CLI (`GEMINI.md`) are still read per reports; confirm in your install |
| Extensions | Gemini CLI extensions are called plugins in Antigravity. Convert the Sales-OS extension with `agy plugin import gemini` |
| Config | Settings and MCP configuration moved under `~/.gemini/antigravity-cli/`; MCP uses a separate file and the remote server key is `serverUrl` (a leftover `url` key may fail silently) |

## Setup

1. Install with the official installer for your platform, or Homebrew where available. Verify with `agy doctor` and see what it discovered with `agy inspect`.
2. Open the Sales-OS folder in a terminal and start the CLI.
3. Confirm the `mh-` and `sos-` skills are discovered. Run `sos-start`.
4. If you use the extension, import it with `agy plugin import gemini`.

## Differences to expect

- Slash commands from `.gemini/commands/sos/` are a Gemini CLI feature. In Antigravity rely on skills (activate by name or by matching request). Re-check whether custom commands are supported in your version.
- Quota moved from a daily request count to a weekly compute-based cap on some plans; plan long runs accordingly.
- Scripts or cron jobs that called `gemini` must be changed to `agy`.

## Notes

The official migration guide and the installer commands change; use the links in `platform-facts.md`. Keep customer data on approved machines.
