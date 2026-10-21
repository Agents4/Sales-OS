---
name: capabilities
description: How skills adapt to what the current platform can actually do
---

# Capabilities and graceful degradation

Skills are written once and run in very different places: a terminal agent with a file system, the Gemini app with only chat, an enterprise agent with a CRM connector. Do not assume. **Detect what you can do, use it, and degrade gracefully.**

## Detect before you promise

Check your actual tool list and test with a harmless call. Do not claim access you have not verified. If a call fails, report the path and the error text.

| Capability | Means | If present | If absent |
|---|---|---|---|
| **FILES** | Read and write files in the workspace | Read context and sheets from `workspace/`; write outputs there | Ask the user to paste or attach what you need; return outputs in chat in the exact output structure so they can save them |
| **SHELL** | Run commands | Run `python3 tools/sos.py lint` and `pipeline`; use scripts | Walk the rubric by hand; say lint was not run |
| **WEB** | Search or fetch public pages | Research accounts and people from public sources, cite URLs | Work only from supplied material; list what should be researched |
| **GOOGLE** | Drive, Docs, Sheets, Gmail, Calendar, Meet notes | Pull meeting notes and transcripts, read shared docs, create drafts (never send) | Ask the user to paste or attach |
| **CRM** | A connected CRM (for example Salesforce) | Read opportunity, contact roles and activity; propose write-backs | Work from sheets and ask the user for current stage, amount, dates |
| **SUBAGENTS** | Run parallel agents with isolated context | Run stakeholder lenses in parallel, then synthesize | Run the lenses one after another yourself, in separate headed sections |
| **SCHEDULE** | Run on a schedule | Offer to set up the weekly routine | Give the user the prompt to schedule elsewhere |

## Chat-only mode

Many sellers will use the Gemini app or a similar chat. In chat-only mode:

1. Ask for the minimum inputs (paste the Blue Sheet, the notes or the transcript) instead of looking for files.
2. Produce the artifact in a single code block or clearly delimited section using the template structure, so it can be copied into a Google Doc or saved as `.md`.
3. Remind the user once, briefly, where to save it. Do not nag.
4. Ask at most three questions at a time (see `interview-protocol.md`).

## File access problems

If a read fails with "Resource deadlock avoided", a timeout, or "operation not permitted", the file is most likely a cloud-only placeholder in a Google Drive for desktop folder. Tell the user: set the Sales-OS folder to *Available offline* (or use Mirror files), then retry. Meanwhile ask them to paste the content you need. Do not guess at contents you could not read.

## Paths

Paths in skills are relative to the workspace root (the folder that contains `AGENTS.md`). `references/` and `assets/` are relative to the skill's own folder. If your platform runs skills from a different working directory, resolve accordingly and say so.

## Never rely on

- Memory of earlier conversations. Reload the sheet.
- A tool you have not verified exists.
- Network access from scripts in a skill. The Gemini app blocks it; assume none.
- Binary Office files. Convert or ask for text.
