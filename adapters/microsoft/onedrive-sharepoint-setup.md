# OneDrive and SharePoint setup

Sales-OS can live in a OneDrive folder or a SharePoint document library. The setup below prevents the most common failure: a tool or agent that cannot read a file because it is cloud-only, or that can read files people were never meant to see.

## Layout

Use two places, one for the product and one for the data.

```
SharePoint: Sales-OS Product (read-mostly)        OneDrive or SharePoint: Sales-OS Workspace
  core/ docs/ adapters/ tools/ dist/                 workspace/context-library/   shared read-mostly
  (the product repository or a release tarball)      workspace/accounts/<slug>/   one owner per account
                                                     workspace/outputs/           drafts and reports
```

Why split: the product changes by release, the workspace changes daily. Different people need different access. This is the same product and instance split as in `docs/architecture.md`.

## Files On-Demand (the cloud-only problem)

OneDrive can keep files online-only: the file appears but its content downloads when opened. A tool that reads the folder directly (a terminal, VS Code) can fail with a timeout or "operation not permitted". `python3 tools/sos.py doctor` detects this.

Fix:

1. In File Explorer or Finder, right-click the Sales-OS folder and choose **Always keep on this device**.
2. Wait for sync to finish, then run `python3 tools/sos.py doctor`.
3. Keep the folder mostly to text: Markdown, JSON, CSV. Cowork and agents read Office files; the Python tools do not.

Cowork and agents read through Microsoft 365 and do not need local sync. Only tools you run on your own computer do.

## Permissions

- The context library: read for all sellers, edit for sales operations.
- Each account folder: edit for the account team only. Use SharePoint groups, not individual shares.
- Do not store the product and client data in the same library if the audience differs.
- Cowork tasks and agents see only what the signed-in user can open. If a seller can open another team's account folder, so can their Cowork.
- Keep internal-only coaching sheets in a folder that no buyer, partner or guest can open. Do not share it with external guests.

## Versions and change control

- SharePoint and OneDrive keep version history. A mistaken edit is recoverable.
- The living sheets have a Change log; keep it up.
- One owner per sheet. Markdown merges poorly with two simultaneous editors.
- Never edit `.agents/skills`, `.claude/skills`, `.gemini/commands` or `dist/`. Rebuild.

## Word and Excel versus Markdown

Markdown is the source of truth because the tools lint and compile it. If the team prefers Word, keep the Markdown as the master and export or paste into Word for sharing. Copilot Notebooks accept Word, PowerPoint, Excel and PDF. Convert on the way in. A Word copy is not read by the Python tools unless exported to text.

## Run the tools from your own computer

```
cd "<your Sales-OS workspace folder>"
python3 <product folder>/tools/sos.py lint
python3 <product folder>/tools/sos.py pipeline --format csv --out pipeline.csv
```

Python 3.8 or later, standard library only. Both commands read `workspace/` from the current folder, or take `--workspace <folder>`.
