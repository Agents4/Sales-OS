# Security and governance

## Data classes

| Class | Examples | Where it may live |
|---|---|---|
| Public | Company websites, filings | Anywhere |
| Internal sales | Sheets, debriefs, strategy | Approved tools only (client's Workspace, approved notebook, approved CLI machines) |
| Customer confidential | Transcripts, emails, quotes, contracts | Only tools approved for customer data |
| Restricted | Credentials, personal data | Not in Sales-OS at all |

The client lists approved tools in `workspace/context-library/business-info.md` (Guardrails). Skills respect it.

## Controls built into the system

- **Never invent.** Unknown beats a plausible guess. Evidence tags and sources on claims about people and decisions.
- **Approval gates.** Drafts yes; sending, CRM writes, sharing, overwriting and promoting to the context library need explicit approval.
- **Internal versus buyer-facing boundary** with mandatory leak checks in buyer-facing skills.
- **Privacy.** Work-relevant motives only. No health, family, politics, religion or other private details in any sheet.
- **CRM contract.** Only safe summary fields go to the CRM; modes, Wins and red flag text never do.
- **Generated folders are read-only by convention**; changes go through `core/` or `local/` and the build.
- **No secrets in the repository.** `.gitignore` excludes keys and environment files.
- **Scripts are optional.** Skills contain no scripts. The Python tools use only the standard library and never make network calls.

## Governance of the skills

- Treat skills like code: change in `core/` or `local/skills/`, validate, test with eval cases, record in `CHANGELOG.md`.
- Name an owner for the shared skill set and a reviewer for client-specific skills.
- In Gemini Enterprise, enable skill sharing deliberately and approve the shared set.
- The ratchet process (`sos-ratchet`) proposes improvements for approval; it never edits shared product files itself.
- Review the lessons log on a fixed cadence.

## Access

- Sellers own their `workspace/accounts/` folders; managers get read access to the Best Few deals of their team; the context library is shared read-mostly.
- Shared notebooks that include internal-only analysis go to the deal team only.
- Agents act as the authenticated user and inherit that user's permissions.

## Incident handling

If internal analysis reaches a buyer (a leaked sheet, a CRM field, a shared doc):

1. Stop sharing and remove access; note what was exposed.
2. Tell the account owner and manager.
3. Decide whether the Coach or any named person needs a heads-up, and who gives it.
4. Record a lesson and strengthen the leak check.

## Intellectual property

The methodology names (Strategic Selling, Conceptual Selling, Large Account Management Process, LAMP, Blue, Green and Gold Sheet) belong to their owner (Miller Heiman Group, part of Korn Ferry). Sales-OS is an original synthesis and does not reproduce official workbooks or training content. Before marketing a deployment as Miller Heiman, or distributing official forms, confirm the licensing position with the client and the rights holder. Clients with their own licensed materials can substitute their wording and scales in the templates.

## Evaluation and quality

`validate` and `selftest` run before every release. `evals/` has realistic cases (invented stakeholders, personal-detail leakage, single-threaded accounts, buyer-facing leaks). Run them after any change to a skill that affects those behaviors.
