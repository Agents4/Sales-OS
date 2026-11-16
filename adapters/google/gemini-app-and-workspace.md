# Gemini app and Workspace: skills

Status as of 2026-11-16. Verify against `platform-facts.md` before a client session.

> **Corporate accounts:** Google's transition page (updated 2026-11-09) says skills are available in the Gemini app to all Workspace editions, with the rollout started on 2026-10-13 and due to finish in mid-November. Admins must turn skills on. Gems stay, and move into Settings on 2026-11-17, until 2027-03-01 at the earliest (Business and Enterprise). If your corporate account has no Skills page yet, use `corporate-workspace.md` (Gems plus Notebooks). Check the Skills page on a test account first.

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
- Uploads: plain-text-based files plus `.docx`, `.pdf`, `.md`, `.csv`, `.xlsx`, `.pptx` and common images, 100 MB combined. Legacy `.doc`, `.xls`, `.ppt`, audio, video and archives are not supported. Scripts cannot reach the internet. The Sales-OS zips are Markdown only.
- Remove hidden files like `.DS_Store` before uploading (the build already does).
- Skills do not yet work with some Gemini features (Canvas, Deep Research and others at the time of writing).
- Skills do not sync between the Gemini app and Workspace apps (Docs, Gmail and so on). Upload in each place you want them.

## Availability by account type (verify)

Skills began rolling out in the Gemini app on 2026-10-13 to all Workspace editions, and Workspace apps (Studio, Docs) followed from 2026-11-09. Gems are removed no sooner than 2027-03-01 (Business and Enterprise) and 2027-06-01 (Education). The page does not address nonprofit accounts. Skills built in the Gemini app are not available in Workspace apps or Gemini Enterprise, and the reverse. Confirm in the client's admin console and a test user account that skills are on.

**Sharing:** Google's help page documents sharing in the Gemini web app (owner and Editors share, Viewer or Editor access, optional expiry, files shared separately), but the Workspace admin page lists Gemini app sharing as "coming soon". Test it with a second user before you plan a team rollout. If it does not work, each user uploads the zips.

## How a seller uses it

- `/blue-sheet`, `/green-sheet`, `/call-debrief`: paste the material, answer three questions, copy the output to a Doc or a Markdown file.
- No file access in this surface: skills run in chat-only mode. They return the artifact in one block and remind you where to save it.
- Reference files (company facts, writing style) can be attached to a skill. Files can also be added from Google Drive and from Notebooks, and they keep their live link (they are left out of a downloaded zip). A Gem could not take a Notebook as a source. Check it in the client's tenant before depending on it.

## Where to be careful

- A personal Google account is not the same as a Workspace account for data handling. Do not put real customer data into a personal account unless the client's policy allows it.
- Keep internal-only analysis out of anything shared.
