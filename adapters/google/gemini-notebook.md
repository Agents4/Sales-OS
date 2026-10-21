# Gemini Notebook (NotebookLM)

Gemini Notebook is the product previously called NotebookLM. It answers only from the sources you load, with citations. It cannot run skills, so Sales-OS gives it well-structured source packs, chat instructions and a Studio prompt cookbook.

## Packs

| Pack | Built by | Use |
|---|---|---|
| Methodology coach | `python3 tools/sos.py build --target notebook` (output in `dist/notebook-packs/methodology-coach/`) | Anyone can ask method questions, paste a sheet for critique, take quizzes |
| Account room | `python3 tools/sos.py notebook-pack --account <slug>` | One account: plan, Blue and Green Sheets, call notes, research, method reference |
| Company playbook | `python3 tools/sos.py notebook-pack --company` | Positioning, objections, proof, competitors, sales motion |

Each pack folder has `sources/`, `chat-instructions.txt`, `studio-prompts.md` and a `README.md` with the upload steps.

## Steps

1. Create a notebook.
2. Add every file in `sources/`. Consider importing them as Google Docs so you can use sync with Drive when they change.
3. Open the chat settings, choose a custom conversational style and paste `chat-instructions.txt`. Keep it short; there is a character limit that has changed over time.
4. Use `studio-prompts.md` for audio overviews, reports, quizzes, flashcards, slide decks and mind maps.

## Limits (verify before relying)

About 50 sources per notebook on the consumer tier; Gemini Notebook Enterprise is documented at 300 sources, with per-source limits of 500,000 words or 500 MB. The builder splits long sources and warns on oversized chat instructions.

## Freshness

A notebook is a snapshot unless its sources are synced Google Docs or Slides. Re-run the builder after meaningful changes and replace only the changed sources. Say the build date in the notebook title.

## Privacy

Everyone with access to a notebook can read its sources. An account room that holds modes, Win-Results, red flags and Coach identity must be shared only with the deal team. Never add anything the client has not approved for this tool.

## Good uses

- Pre-call briefings from the account room ("what do we know and not know about the CFO").
- Manager pipeline questions across several account rooms (one notebook per account).
- New-seller onboarding from the company playbook plus the method coach.
