# Corporate Google Workspace: Gemini app and Gemini Notebook

For a company on Google Workspace that has no Gemini Enterprise agent platform: no Workflow Builder, no custom connectors, no code to deploy. You use two standard Workspace features, the Gemini app and Gemini Notebook (formerly NotebookLM), plus Drive.

Status as of 2026-11-16. Sources and confidence are in `platform-facts.md`.

## Answer first

Run Sales-OS as a **Gem** (does the jobs) plus **Notebooks** (answer from your documents with citations). Drive holds the context and the outputs. Nothing writes back to Drive or the CRM by itself, so the seller copies outputs and sheet updates into Docs. That matches the Sales-OS approval gates: the tool drafts, the human sends.

Skills are now rolling out to Workspace accounts in the Gemini app (started 2026-10-13, due to finish in mid-November), and Gems stay until 2027-03-01 at the earliest. Check the Skills page first. If it is there and your admin has turned skills on, you can use skills (Route A). Gems (Route B) still work today and are the safer route for team sharing until you confirm that skill sharing works in your tenant.

## Step 0: Check which route you have (2 minutes)

Open the Gemini app on a corporate test account and look for the Skills page.

- **Skills page present:** Route A. Upload the zips from `dist/gemini-app/zips/` (see `gemini-app-and-workspace.md`). Before you rely on it, test that a second user can open a skill you share. Google's help page documents sharing in the web app, but the Workspace admin page lists Gemini app sharing as "coming soon" (fact 22). Until it works, each user uploads the zips themselves, or you stay on Gems.
- **No Skills page:** Route B below. The rollout may not have reached your domain yet, or your admin has not turned skills on. Gems stay until 2027-03-01 at the earliest for Workspace business and enterprise, and move into Settings on 2026-11-17.

Rehearse on a personal account only with fictional data. Never put customer data into a personal account.

## Step 1: Ask IT (one email)

1. Gemini app on for the pilot group, with access to Drive files.
2. Gem sharing on for the pilot group (Admin console, Gemini app settings, "Allow users to share Gems"). It applies per organizational unit or group, and a group setting wins. Changes take up to 24 hours.
3. Skills on for the pilot group (Workspace Studio and Gemini in Workspace settings), and whether external skill sharing is restricted. Skip this if you are staying on Gems.
4. Gemini Notebook on for the pilot group, and the edition's tier. It sets sources per notebook: 50, 100 or 300.
5. External sharing off for the Sales-OS shared drive. Gems and Notebooks follow Drive sharing.
6. A shared drive named `Sales-OS`, owned by a group rather than a person.
7. Written confirmation that Workspace is approved for customer data, and which data classes.
8. The data terms for the Gemini app on your edition (the Workspace privacy hub). For Gemini Notebook on enterprise-grade editions, Google states that files, chats and outputs are not reviewed by humans or used to improve models.

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

When the Skills page is on for your tenant, test one user first. Google converts Gems to skills in the Gemini app. Each converted skill arrives as an inactive draft that its creator must review and activate, and it keeps the name, instructions, knowledge files and Drive permissions. A converted Gem becomes one skill with the ten files attached, so compare it with `dist/gemini-app/zips/` (one skill per job) and decide which you prefer. Skills can also take files from Drive and from Notebooks, which a Gem could not. Keep under 100 active skills (per the earlier help page). Retire the Gems after the pilot group confirms. Google says migration details come at least 30 days before automated migration starts.

## Limits

| Item | Limit | Confidence |
|---|---|---|
| Gem knowledge files | 10 | Medium |
| Gem instruction length | Not published. The generated text is about 4,300 characters | Unknown |
| Notebook sources | 50, 100 or 300 by tier | High |
| Notebook source size | 500,000 words or 200 MB (earlier read; the current work-account page lists no source size) | Medium |
| Notebook chat instructions | Not documented | Unknown |
| Skills in Gemini app | 100 MB per skill. 100 active at a time per an earlier help page; the current page states no active limit | High for size; Medium for 100 active |
