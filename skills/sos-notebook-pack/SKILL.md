---
name: sos-notebook-pack
description: "Prepare source packs and instructions for a Gemini Notebook (NotebookLM) so a team can chat with an account room, a company playbook or the methodology. Use when the user wants to set up a notebook, load deal material into a notebook, or refresh one with new notes."
compatibility: "Best with shell access to run the pack builder. Without a shell, produces a manual checklist of sources and the chat instructions."
metadata:
  version: "1.0.0"
  layer: system
  last_reviewed: "2026-10-17"
  includes: "shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Notebook packs

A notebook is a grounded workspace: it answers only from the sources you load. A good pack is small, current and clearly named. The builder compiles packs from the workspace so you do not hand-copy files.

Read `references/operating-rules.md`, `references/capabilities.md` and `references/output-conventions.md`.

## Pack types

| Pack | Contents | Use |
|---|---|---|
| Methodology coach | Method references and the three templates | A coach anyone can ask about Miller Heiman |
| Account room | One account's profile, Gold Sheet, Blue Sheets, latest debriefs and research | Preparing for calls and reviews on that account |
| Company playbook | Context library: business info, sales motion, competitors, proof points, objections | Messaging and enablement |

## When to use

- A team wants a notebook for an account, a company playbook or the method.
- New notes or sheets should be added to an existing notebook.
- The user asks what to upload and what to leave out.

## Procedure

1. **Confirm what may be loaded.** Only material the client has approved for this tool. Exclude credentials, personal data, and anything internal the client does not want in a shared notebook. Remind that internal-only analysis (modes, Wins, red flags, Coach identity) in a notebook is visible to everyone who can open it.
2. **Build with a shell:**
   - Account room: `python3 tools/sos.py notebook-pack --account <slug>`
   - Company playbook: `python3 tools/sos.py notebook-pack --company`
   - Static packs (methodology coach) are produced by `python3 tools/sos.py build --target notebook`.
   Output goes under `dist/notebook-packs/`. Add `--out <dir>` to change it, `--no-method` to skip the method sources.
3. **Without a shell:** list the exact files to upload from the workspace, in order, and give the chat instructions text from the pack's `chat-instructions.txt` with the account and date filled in.
4. **Respect limits.** Notebooks cap the number and size of sources; the builder splits long sources and writes a README. Chat instructions have a character limit; keep them short.
5. **Tell the user the steps in the Notebook interface:** create the notebook, add the sources, paste the chat instructions into the custom chat settings, and try the studio prompts from the pack.
6. **Refresh.** Sources in a notebook do not auto-update from files. Re-run the builder and replace changed sources. Say when the pack was built.

## Output

The pack folder path (or the manual list), the chat instructions, and the studio prompts to try. A one-line statement of what was left out and why.

## Quality gate

1. No source was added that the client has not approved for this tool.
2. The user knows the pack is a snapshot with a build date.
3. If the builder reported a problem (unreadable file, source too large), it is reported with the fix.
