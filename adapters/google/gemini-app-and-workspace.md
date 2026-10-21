# Gemini app and Workspace: skills

Status as of 2026-10-17. Verify against `platform-facts.md` before a client session.

## What you get

Skills in the Gemini app are reusable instruction sets that run inside any chat. Typing a slash and the skill name calls one (Google says the trigger will move to `@`), and Gemini can also apply an activated skill automatically when your request fits its description. Several skills can be combined in one chat. Skills replace Gems.

Sales-OS compiles every skill into a self-contained zip (instructions, references and templates). Upload one zip per skill.

## Where the zips are

`dist/gemini-app/zips/<skill>.zip`, with `dist/gemini-app/INSTALL.md` listing bundles. Build them with `python3 tools/sos.py build --target gemini-app`.

## Upload

1. Open the Skills page in the Gemini app (web or Mac app; file upload for creating skills is limited to those).
2. Create a skill by upload and choose a zip. `SKILL.md` sits at the root of the zip.
3. Review, then Create. Repeat for each skill in your bundle.
4. Activate the skills. Only activated skills are used automatically.
5. To update a skill, upload the whole zip again (replace skill).

## Limits to plan around

- Unlimited skills, but only **100 active at a time**. Activate a bundle, not everything.
- Uploads: plain-text-based files, 100 MB combined. Scripts cannot reach the internet. The Sales-OS zips are Markdown only.
- Remove hidden files like `.DS_Store` before uploading (the build already does).
- Skills do not yet work with some Gemini features (Canvas, Deep Research and others at the time of writing).
- Skills do not sync between the Gemini app and Workspace apps (Docs, Gmail and so on). Upload in each place you want them.

## Availability by account type (verify)

Skills reached personal accounts first. Workspace business, enterprise, nonprofit and education accounts were announced for later, and Google's Gems-to-skills transition dates differ by account type (November 2026 personal, March 2027 Workspace business and enterprise, June 2027 education). Treat Workspace availability as unconfirmed until you see it in the client's admin console and a test user account.

## How a seller uses it

- `/blue-sheet`, `/green-sheet`, `/call-debrief`: paste the material, answer three questions, copy the output to a Doc or a Markdown file.
- No file access in this surface: skills run in chat-only mode. They return the artifact in one block and remind you where to save it.
- Reference files (company facts, writing style) can be attached to a skill. Drive and Notebook file support for skills was announced as coming; check before depending on it.

## Where to be careful

- A personal Google account is not the same as a Workspace account for data handling. Do not put real customer data into a personal account unless the client's policy allows it.
- Keep internal-only analysis out of anything shared.
