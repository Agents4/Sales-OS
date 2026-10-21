# Google playbook

How to run Sales-OS on Google's stack. Facts about Google products change quickly. Everything product-specific here is dated and listed in `platform-facts.md` with its sources and a verify list. Check that file before a client session.

## Three adoption tiers

Pick the tier that matches the client's appetite and IT policy. They stack: each tier adds to the one before.

### Tier 1: no install (day one)

For sellers who only have a browser. Nothing for IT to deploy.

- **Gemini Notebook** (the product formerly called NotebookLM): load the Methodology coach pack, then an account room per key account. Chat with grounded sources, generate briefings and quizzes. Guide: `gemini-notebook.md`.
- **Gemini app skills**: upload the skill zips for the seller bundle. Skills run inside any Gemini chat. Guide: `gemini-app-and-workspace.md`. Check availability for the client's account type first: skills reached personal accounts before Workspace business accounts.
- **Google Docs and Drive** for the living sheets (as `.md` or pasted into Docs) and the context library.

Outcome: sellers get method coaching, call prep and debriefs in chat, with outputs saved by hand. Fastest to adopt, least automation.

### Tier 2: managed (admin-enabled)

For companies on Gemini Enterprise or Workspace with an admin.

- **Gemini Enterprise skills**: admin enables skills and skill sharing, then the team uploads or shares the skill set. Guide: `gemini-enterprise.md`.
- **Workflow Builder** for scheduled or on-demand flows, for example a weekly pipeline hygiene report from the sheets, with connectors to Drive, Gmail, Calendar and Salesforce.
- **Connectors** to Drive, Calendar, Gmail, Meet notes and the CRM so skills can read real data and draft, never send.

Outcome: skills with data access, shared and governed, with audit.

### Tier 3: power users (terminal)

For revenue operations, sales engineering and managers who like a terminal.

- **Gemini CLI** (enterprise and API-key accounts) or **Antigravity CLI** (everyone else): both read `.agents/skills/` and `AGENTS.md`. Guides: `gemini-cli.md`, `antigravity-cli.md`.
- Run the Python tools: lint, pipeline report, notebook-pack builder, build and release.
- Generate account rooms and company playbooks for the notebooks.

Outcome: automated hygiene, packs, builds, and the full tool set.

## Recommended rollout order

1. Admin: confirm which of the three tiers the client's accounts allow today (`platform-facts.md`, verify list).
2. `drive-setup.md`: put the Sales-OS folder on Drive with the right offline settings.
3. Load the **Methodology coach** notebook and run a 45-minute enablement session.
4. Pick one pilot team and one live deal per seller. Run `sos-setup`, then `mh-blue-sheet`.
5. Add call prep and debrief to the weekly routine (`mh-green-sheet`, `mh-call-debrief`).
6. Add a manager cadence (`mh-deal-review`, `mh-pipeline-review`).
7. Add connectors and workflows when the data hygiene is good enough to automate.

See `docs/rollout-playbook.md` for the full plan, KPIs and roles.

## Choosing the surface for a task

| Task | Best surface |
|---|---|
| Learn or coach on the method | Gemini Notebook (method coach) |
| Prepare for a call | Gemini app skill `mh-green-sheet`, or the account room notebook |
| Debrief a call from Meet notes | Gemini Enterprise skill with Meet/Drive access, or paste into the Gemini app skill |
| Weekly pipeline report | Workflow Builder or a CLI run of `pipeline` |
| Edit and lint a sheet | CLI with the Python tools, or the rubric in chat |
| Share an account room with a team | Gemini Notebook sharing |

## Data and privacy on Google

- Use only the Google surfaces the client's security team has approved for customer data. Account type decides data handling and retention for the consumer apps; check this before loading real deal data into a personal account.
- Internal-only analysis (modes, Win-Results, red flags, Coach identity) inside a shared notebook is visible to everyone with access. Share notebooks narrowly.
- A skill never sends mail. At most it creates a draft when a Gmail connector is present and the user asked.

## Files in this folder

| File | Contents |
|---|---|
| `drive-setup.md` | Drive for desktop settings that avoid read failures |
| `gemini-app-and-workspace.md` | Skills in the Gemini app, zips, limits |
| `gemini-notebook.md` | Notebook packs, chat instructions, studio prompts |
| `gemini-enterprise.md` | Enterprise skills, Workflow Builder, connectors, governance |
| `gemini-cli.md` | Gemini CLI setup and commands |
| `antigravity-cli.md` | Antigravity CLI setup and migration notes |
| `platform-facts.md` | Dated facts, sources and the verify list |
