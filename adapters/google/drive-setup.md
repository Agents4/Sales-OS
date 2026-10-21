# Google Drive setup

Sales-OS can live in a shared drive or a My Drive folder synced with Drive for desktop. The setup below prevents the most common failure: an agent that cannot read a file because it is online-only.

## The problem

Drive for desktop can stream files: the file appears in the folder but its contents download only when opened. A tool that reads the folder directly can fail with "Resource deadlock avoided", a timeout or "operation not permitted". `python3 tools/sos.py doctor` detects this.

## Fix

1. In Drive for desktop, open Preferences and check the My Drive sync option.
2. For the Sales-OS folder choose **Available offline** (right-click the folder in Finder or Explorer, then Offline access), or switch the account to **Mirror files**.
3. Wait for the sync to finish, then run `python3 tools/sos.py doctor`.

## Habits that keep it healthy

- Keep the folder to text: Markdown, JSON, CSV. Avoid binary office files that tools cannot read; export to text or paste the content.
- Do not store the product and client data in the same shared folder if different people need different access. Use the product/instance split: the product repository stays read-mostly; each client has an instance with its own `workspace/`.
- Remove `.DS_Store` and similar hidden files before uploading zips (the build already excludes them).
- Edit living sheets in place. Drive keeps revision history, so a mistaken edit is recoverable; the sheets also have a Change log.
- Do not edit generated folders. Rebuild.
- Sharing: the context library is shared read-mostly; each seller owns their `workspace/accounts/` folders. Use Drive sharing, not copies.
- Avoid two people editing the same sheet at once; Markdown merges poorly. One owner per sheet.

## Google Docs

If the team prefers Docs, keep the Markdown as the source of truth and paste or import into Docs for sharing. Notebook sources can be Docs synced from Drive, which lets a notebook refresh them. A Doc is not read by the CLI tools unless exported to text.
