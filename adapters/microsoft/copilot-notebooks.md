# Copilot Notebooks

Copilot Notebooks bundle chats, files, pages and links into one grounded workspace. Sales-OS uses them the way it uses Gemini Notebook: a **Methodology coach** notebook for everyone, and an **account room** per key account.

Limits below are not confirmed by an official Microsoft page. Treat them as planning numbers and verify (see `platform-facts.md`, items 15 and 16).

## What a notebook is good for here

- Asking questions about the Miller Heiman method with answers grounded in the Sales-OS method sources.
- Holding everything about one account in one place: Blue Sheet, Green Sheets, debriefs, stakeholder profiles, meeting notes.
- Pulling in the seller's own Word, PowerPoint, Excel, PDF, Loop and OneNote content.

What it is not: a skill runner. Notebooks do not execute the Sales-OS procedures. Use Cowork or an agent for that, and use a notebook for grounded questions.

## Build the packs

```
python3 tools/sos.py build --target notebook          # static pack: Methodology coach
python3 tools/sos.py notebook-pack --account acme     # account room pack from workspace/accounts/acme
python3 tools/sos.py notebook-pack --company          # company playbook from the context library
```

Packs are folders of Markdown sources plus a `README.md`, `chat-instructions.txt` and `studio-prompts.md`. The same packs serve Gemini Notebook and Copilot Notebooks.

## Set up the Methodology coach notebook

1. In Microsoft 365 Copilot create a new notebook and name it `Sales-OS Method Coach`.
2. Add the files from `dist/notebook-packs/methodology-coach/sources/` as references. Markdown is not in the list of types the sources describe (Word, PowerPoint, Excel, PDF, Loop, pages, OneNote). Convert the sources to Word or PDF first if Markdown is rejected, or paste them into a OneNote page. Keep one file per topic.
3. Copy `chat-instructions.txt` into the notebook's custom instructions if the notebook supports them in your tenant. If not, paste it as the first message.
4. Run the starter questions from `studio-prompts.md`.

Keep the notebook under about 100 references. The only figure found for the cap (100) comes from an unverified answer on Microsoft Q&A; re-test it.

## Account rooms

1. Create a notebook per key account, for example `Account Room - Contoso`.
2. Add the account pack sources, plus the real Blue Sheet, the last three Green Sheets and debriefs, and the latest meeting notes or transcripts.
3. Share the notebook only with the account team. A notebook exposes whatever its sources expose, so match the audience to the data: do not put internal-only coaching sheets into a notebook that the customer or a partner can open.
4. Refresh the sources after each call. If the notebook references a file in SharePoint or OneDrive, update the file there. A pasted copy does not refresh itself.

## Habits

- Name sources with the date and type: `2026-10-22 call-debrief.md`.
- One notebook, one account. Do not mix accounts.
- Chat answers come back unlabeled. Ask for the F, I, A and U tags when you need them, and check any quoted fact against its source.
- Save useful chat output to a file. Notebook chat is not a system of record.
