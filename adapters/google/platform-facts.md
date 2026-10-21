# Platform facts (as of 2026-10-17)

Everything product-specific in the Google guides comes from here. Google changes these products often. Before a client session, re-check the **verify list** at the bottom.

## Facts and sources

| # | Fact | Source | Confidence |
|---|---|---|---|
| 1 | Gemini CLI stopped serving Google AI Pro, Ultra and free individual accounts on 2026-06-18; the terminal experience moved to Antigravity CLI (announced 2026-05-19). | Gemini CLI GitHub discussion #27274 (maintainer announcement) | High |
| 2 | Gemini Code Assist Standard and Enterprise licenses, Google Cloud usage, and paid API keys keep Gemini CLI access. Vertex AI and Google One were not named. | Same | High for what it names; unknown otherwise |
| 3 | Antigravity CLI keeps Agent Skills, hooks and subagents. Extensions are renamed plugins. The installer imports skills, MCP configs and agent profiles. | Same, plus a third-party migration guide (June 2026) | Medium: the third-party details (paths, `agy` commands, quota) are not official |
| 4 | Workspace skills move from `.gemini/skills/` to `.agents/skills/` for Antigravity; global skills to `~/.gemini/antigravity-cli/skills/`. | Third-party migration guide | Medium |
| 5 | Gemini app: skills replace Gems. Skills are reusable instructions run inside chat, called with a slash (to move to `@`), also applied automatically. Unlimited skills, 100 active at once. | Gemini Apps Help: "About the transition from Gems to skills" and "Create and manage skills" | High |
| 6 | Skills import: a single `SKILL.md`, or a folder or zip with `SKILL.md` at the root. Plain-text-based files, rich media like PDFs and images; no Office binaries; 100 MB combined; scripts cannot reach the internet. Upload to create is limited to the Mac app and web app. | Gemini Apps Help: "Create and manage skills" | High |
| 7 | Skills may include reference files from 2026-09-30. Drive and Notebook file support for skills was announced as coming. | Gemini Apps Help | Medium |
| 8 | Gems retirement and conversion: November 2026 personal accounts; March 2027 Workspace business, enterprise and nonprofit; June 2027 education. Skills available first to adults on personal accounts; Workspace accounts later. | Gemini Apps Help: transition page | High for dates stated; Workspace skills availability must be verified |
| 9 | Gemini Enterprise: custom skills generally available (2026-08-13). Admins enable skills and skill sharing in Feature Management and can approve sharing requests. | Gemini Enterprise release notes | High |
| 10 | Workflow Builder (formerly Agent Designer) generally available (2026-09-03). Connectors include Drive, Gmail, Calendar, Chat, Slack, Jira; Teams, Notion, Salesforce added 2026-10-13. | Gemini Enterprise release notes | High |
| 11 | Custom MCP server data stores generally available (2026-08-07), off by default and gated by an organization policy. | Gemini Enterprise release notes | High |
| 12 | Gemini Notebook Enterprise integration in Gemini Enterprise: sharing, sensitive data protection policies, CMEK, quizzes and flashcards generally available. | Gemini Enterprise release notes | High |
| 13 | Google describes agent skills as reusable packages of instructions loaded by progressive disclosure, based on an open specification (SKILL.md with name and description up to 1,024 characters; optional `scripts/`, `references/`, `assets/`). Works across Antigravity CLI, Claude Code, VS Code, Cursor and others. | Google Cloud: AI agent skills | High |
| 14 | Google announced a unified Gemini agent for businesses on 2026-10-08, with skills, connectors, MCP and a tasks inbox; business first, consumers later; no general availability date or pricing stated. | TechCrunch, 2026-10-08 | Medium |
| 15 | Gemini CLI extension layout: `gemini-extension.json`, `commands/`, `skills/`, `agents/`, `hooks/`, `policies/`; extensions load from `~/.gemini/extensions`. Custom commands are TOML files, `/gcs:sync` from `gcs/sync.toml`. | geminicli.com extension reference | High |
| 16 | Gemini Notebook source and chat limits. Sales-OS assumes about 50 sources on the consumer tier and 300 sources, 500,000 words or 500 MB per source on Enterprise, and a short chat-instruction limit. | Not re-verified this session | Low: verify |
| 17 | The Miller Heiman method: books and sheet terminology are described in `core/methodology/fidelity-ledger.md`. Book publication years (1985, 1987, 1991) are not independently verified. | Secondary sources | See ledger |

## Verify list (do before a client session)

1. Which license and account type does the client hold: Workspace edition, Gemini Enterprise, Gemini Code Assist? This decides whether the CLI or the Antigravity CLI applies, and whether skills are enabled for their users (facts 2, 8, 9).
2. Are skills enabled in the client's Gemini app for Workspace users today, or only for personal accounts (fact 8)? Test with a real user account.
3. Is the Admin Feature Management setting for skills and skill sharing on, and who approves sharing (fact 9)?
4. Current Notebook limits and the chat-instruction character limit (fact 16).
5. Whether slash commands (`.gemini/commands`) still work in the client's CLI and whether Antigravity supports custom commands (fact 15 and the Antigravity notes).
6. Whether the Gemini app trigger changed from `/` to `@` (fact 5).
7. The client's data policy for consumer versus Workspace accounts.
8. Licensing: confirm with the client's counsel and the rights holder that using Miller Heiman terminology and sheet structures internally is fine (see `docs/security-and-governance.md`).

## Sources

- Gemini CLI transition announcement: github.com/google-gemini/gemini-cli/discussions/27274
- Gemini Apps Help, transition from Gems to skills: support.google.com/gemini/answer/18560919
- Gemini Apps Help, create and manage skills: support.google.com/gemini/answer/17094296
- Google Cloud, AI agent skills: cloud.google.com/discover/ai-agent-skills
- Gemini Enterprise release notes: docs.cloud.google.com/gemini/enterprise/docs/release-notes
- Gemini CLI extensions reference: geminicli.com/docs/extensions/reference/
- Third-party migration guide (unofficial): digitalapplied.com blog, June 2026
- TechCrunch, 2026-10-08, Google's agentic Gemini for businesses
