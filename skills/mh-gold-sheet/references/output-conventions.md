---
name: output-conventions
description: Where files live, how they are named, and how outputs are presented
---

# Output conventions

## Workspace layout

```
workspace/
├── context-library/            curated company truths; agents read, humans promote
│   ├── business-info.md        company, product, ICP, value props
│   ├── sales-motion.md         process, stages, thresholds, tools, cadence
│   ├── writing-style.md        voice rules for outbound prose
│   ├── competitors/  proof/  objections/  playbooks/
│   └── lessons.md              proposed rule changes awaiting approval (see sos-ratchet)
├── accounts/
│   └── <account-slug>/
│       ├── profile.md          short account profile
│       ├── gold-sheet.md       LAMP plan, if a strategic account
│       ├── research/           dated research briefs
│       └── deals/
│           └── <opportunity-slug>/
│               ├── blue-sheet.md          the living sheet (edit in place)
│               ├── green-sheets/YYYY-MM-DD-<person>.md
│               ├── call-notes/YYYY-MM-DD-<topic>.md
│               └── map/YYYY-MM-DD-mutual-action-plan.md   (buyer-facing)
└── outputs/                    drafts and reports that are not living sheets
    ├── reviews/  debriefs/  reports/  drafts/
```

## Rules

- Slugs are lowercase with hyphens: `halcyon-logistics`, `route-platform`.
- Dates are ISO `YYYY-MM-DD` everywhere (frontmatter, filenames, tables).
- **Living sheets** (Blue, Green, Gold) are edited in place and carry a Change log. Google Drive keeps revision history, so in-place edits are recoverable; still, summarize every change you make.
- **Everything else** is a new dated file under `outputs/` or the account's folders. Never overwrite a dated output; create a new one.
- Every artifact has YAML frontmatter with at least `type`, `account`, and a date, so tools can find it. Sheets use the schemas in the templates (`type: blue-sheet`, `green-sheet`, `gold-sheet`).
- Drafts of customer-facing text are saved under `outputs/drafts/` and marked `status: draft`. They are never sent by an agent.
- `workspace/context-library/` is read-mostly. Propose changes in `lessons.md` or as a diff for the user to approve.
- Do not write into generated folders (`.agents/skills`, `.claude/skills`, `.gemini/commands`, `dist/`).

## Presenting results

Lead with what matters: the finding, the gap or the decision. Then the artifact. Then the open questions and next actions.

**With file access:** write the file, then reply with the path, a three-line summary of what changed or what you found, the top open questions, and the lint result. Do not paste the whole file back unless asked.

**Chat-only:** return the artifact in one delimited block using the template's structure, then the summary and questions. Include a one-line reminder of where to save it.

**Changes to an existing sheet:** reply with a short "what changed" list (field, old, new, reason) rather than the whole sheet.

## Citing sources

Cite as `(F: call 2026-10-12)`, `(F: email from Priya 2026-10-14)`, `(F: CRM)`, `(I: from F above)`. In research briefs use numbered URLs. For files, give the workspace-relative path.
