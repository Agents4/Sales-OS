---
name: sos-sheet-lint
description: "Check Blue, Green and Gold Sheets for structure and quality, using the lint command when a shell is available or the rubrics by hand when not. Use when the user wants a sheet checked, a quality score, a hygiene audit of a folder of sheets, or a review before sharing with a manager."
compatibility: "Best with shell access (Python 3.8+). Works without it by walking the rubrics."
metadata:
  version: "1.0.0"
  layer: system
  last_reviewed: "2026-10-17"
  includes: "rubrics/blue-sheet.md, rubrics/green-sheet.md, rubrics/gold-sheet.md, shared/operating-rules.md, shared/capabilities.md"
---

# Sheet lint

Lint finds structure problems fast and consistently. The rubrics judge quality. Use both.

Read `references/operating-rules.md` and `references/capabilities.md`. Rubrics are `references/blue-sheet.md`, `references/green-sheet.md` and `references/gold-sheet.md`.

## When to use

- The user wants a sheet checked before a call, review or hand-off.
- A manager wants a hygiene audit of many sheets.
- After editing a sheet, to confirm it still passes.

## Inputs

A sheet file or a folder; or pasted sheet text.

## Procedure

1. **If a shell exists:** run `python3 tools/sos.py lint <file-or-folder>`. With no path it checks the whole workspace. Useful flags: `--today YYYY-MM-DD`, `--stale-days N`, `--best-few-stale-days N`, `--strict`, `--json`.
2. **Read the result.** Errors must be fixed. Warnings are judgment calls: explain each in plain words, and say which you would fix first.
3. **If no shell:** identify the sheet type from its frontmatter (`type: blue-sheet`, `green-sheet`, `gold-sheet`) and walk the matching rubric row by row. State clearly that automated lint was not run.
4. **Judge beyond lint.** The rubric covers what code cannot: whether the Coach is real, whether the SSO passes the colleague test, whether the evidence supports the modes.
5. **Fix on request only.** Propose the fixes as edits (field, old, new). Apply them through the owning skill (`mh-blue-sheet`, `mh-green-sheet` or `mh-gold-sheet`) only when the user asks.
6. **For a folder:** summarize counts by error code and by sheet, and list the three sheets that most need attention.

## Output

A short report: pass or fail per sheet, errors, warnings, the top three fixes, and what lint cannot judge. With a folder, a table of sheets and codes.

## Quality gate

1. State exactly what was run (the command and the date), or that the rubric was walked by hand.
2. Do not hide warnings. Do not call a sheet good because lint passed; say what lint does not check.
3. Never modify a sheet without being asked.
4. Unreadable files (placeholder errors on Google Drive) are reported with the offline-availability fix from `references/capabilities.md`.
