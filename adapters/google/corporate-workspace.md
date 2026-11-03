# Corporate Google Workspace: Gemini app and Gemini Notebook

For a company on Google Workspace that has no Gemini Enterprise agent platform: no Workflow Builder, no custom connectors, no code to deploy. You use two standard Workspace features, the Gemini app and Gemini Notebook (formerly NotebookLM), plus Drive.

Status as of 2026-11-03. Sources and confidence are in `platform-facts.md`.

## Answer first

Run Sales-OS as a **Gem** (does the jobs) plus **Notebooks** (answer from your documents with citations). Drive holds the context and the outputs. Nothing writes back to Drive or the CRM by itself, so the seller copies outputs and sheet updates into Docs. That matches the Sales-OS approval gates: the tool drafts, the human sends.

If the Skills page exists on the corporate account, use skills instead of Gems (Route A). If not, use Gems (Route B). Check first.

## Step 0: Check which route you have (2 minutes)

Open the Gemini app on a corporate test account and look for the Skills page.

- **Skills page present:** Route A. Upload the zips from `dist/gemini-app/zips/` (see `gemini-app-and-workspace.md`).
- **No Skills page:** Route B below. Google's transition page says skills are available to personal accounts only and that work and school accounts come "soon". It also says Gems are removed from Workspace business, enterprise and nonprofit accounts in March 2027.

Rehearse on a personal account only with fictional data. Never put customer data into a personal account.

## Step 1: Ask IT (one email)

1. Gemini app on for the pilot group, with access to Drive files.
2. Gem sharing on for the pilot group (Admin console, Gemini app settings, "Allow users to share Gems"). It applies per organizational unit or group, and a group setting wins. Changes take up to 24 hours.
3. Gemini Notebook on for the pilot group, and the edition's tier. It sets sources per notebook: 50, 100 or 300.
4. External sharing off for the Sales-OS shared drive. Gems and Notebooks follow Drive sharing.
5. A shared drive named `Sales-OS`, owned by a group rather than a person.
6. Written confirmation that Workspace is approved for customer data, and which data classes.
7. The data terms for the Gemini app on your edition (the Workspace privacy hub). For Gemini Notebook on enterprise-grade editions, Google states that files, chats and outputs are not reviewed by humans or used to improve models.

## Step 2: Build the files (one person, once)

Run on a computer with Python:

```
python3 tools/sos.py build --target portable
python3 tools/sos.py build --target notebook
```

Outputs in `dist/portable/`: `gem-seller-instructions.md`, `gem-manager-instructions.md`, `gem-kits.md`, and `skills/<name>.md`. Outputs in `dist/notebook-packs/methodology-coach/`.

Create the company context Doc in Drive from `business-info.md`, `sales-motion.md` and `writing-style.md` (run `sos-setup` first, or write them by hand). Keep it as a native Google Doc so edits flow through.

## Step 3: Create the Gems (Route B)

1. gemini.google.com, signed in with the work account, Explore Gems, New Gem.
2. Name it from `gem-kits.md` (`Sales-OS | Seller`, `Sales-OS | Manager`).
3. Paste the matching `gem-*-instructions.md`. Replace `[COMPANY]`.
4. Add the ten knowledge files in the order `gem-kits.md` lists. Rename each `skills/<name>.md` to `.txt`, or import it into Google Docs. A Gem holds at most 10 files.
5. Save before closing the preview. Test with `Run mh-blue-sheet` and a fictional deal.
6. Share with the pilot group as viewers.

## Step 4: Create the Notebooks

| Notebook | Sources | Who sees it |
|---|---|---|
| Methodology coach | The 11 files in `dist/notebook-packs/methodology-coach/sources/` | Everyone |
| Company playbook | `python3 tools/sos.py notebook-pack --company` | Sellers and managers |
| Account room, one per account | `python3 tools/sos.py notebook-pack --account <slug>` | The deal team only |

Import sources as Google Docs so Drive sync keeps them current. Paste `chat-instructions.txt` from the pack into the chat settings. Keep it short: the character limit is not documented. An account room holds modes, Win-Results, red flags and Coach identity, and everyone with access can read every source.

## Step 5: The working loop

1. Ask the account room: what do we know and not know about the CFO? Answers cite sources.
2. Run the job in the Gem: `Run mh-green-sheet` for the call.
3. Copy the output into the account's Doc. Follow the FILING NOTE.
4. Paste the SHEET UPDATES into the Blue Sheet Doc. The Notebook source refreshes from Drive.
5. Weekly, 15 minutes: managers run `Run mh-pipeline-review` on pasted sheets.

Lint does not run in the Gem. The Gem walks the rubric by hand and says so. RevOps can run `python3 tools/sos.py lint` on exported sheets from a laptop.

## Step 6: Moving to skills

When the Skills page appears for your tenant, test one user first. Google converts Gems to skills automatically ahead of removal. Compare the result with `dist/gemini-app/zips/`, upload the zips for the bundle, and keep under 100 active skills. Retire the Gems after the pilot group confirms.

## Limits

| Item | Limit | Confidence |
|---|---|---|
| Gem knowledge files | 10 | Medium |
| Gem instruction length | Not published. The generated text is about 4,300 characters | Unknown |
| Notebook sources | 50, 100 or 300 by tier | High |
| Notebook source size | 500,000 words or 200 MB | High |
| Notebook chat instructions | Not documented | Unknown |
| Skills in Gemini app | 100 active, 100 MB per skill | High |
