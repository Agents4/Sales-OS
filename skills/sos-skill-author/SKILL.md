---
name: sos-skill-author
description: "Design, write and validate a new Sales-OS skill or change an existing one, following the Agent Skills format and Sales-OS conventions. Use when the user wants to add a skill, customize one for a client, or fix a skill that is routing or behaving badly."
compatibility: "Best with file and shell access to validate and build. Without them, produces the SKILL.md text for the user to save."
metadata:
  version: "1.0.0"
  layer: system
  last_reviewed: "2026-10-17"
  includes: "shared/skill-authoring.md, shared/operating-rules.md, shared/capabilities.md"
---

# Skill author

Write skills that route well, behave predictably and run on any platform. Follow `references/skill-authoring.md` for format and conventions, and the rules in `references/operating-rules.md`. Check `references/capabilities.md` for what the target platform can do.

## When to use

- A new repeatable task deserves a skill.
- A client needs a variant (put it in `local/skills/`, not `core/`).
- An existing skill is chosen wrongly, skips steps or produces weak output.

## Inputs

The job to be done in the user's words, an example of a good output and a bad one if they have them, and the platform(s) it must run on. For a change: the current skill and what went wrong.

## Procedure

1. **Define the job.** One sentence: who uses it, when, what they get. If it is two jobs, make two skills.
2. **Check for overlap.** List existing skills. Prefer extending one to adding a near-duplicate. Prefer a lens or a reference over a new skill if only a perspective differs.
3. **Choose the home.** Client-specific: `local/skills/`. General: `core/skills/` through the maintainers.
4. **Write the description first.** It must say what the skill does and "Use when ..." with the words a seller would use. Test it by asking: given only this text, would an agent pick this skill for the right requests, and not for the wrong ones?
5. **Draft the body** in the required sections. Decide which shared files it needs (`includes`) and reference them correctly.
6. **Build in the rules:** never invent, evidence tags, approval gates, internal versus buyer-facing boundary, capability checks, chat-only output.
7. **Validate.** With a shell run `python3 tools/sos.py validate`; fix errors and warnings. Then `python3 tools/sos.py build` and `build --check`. Without a shell, walk the checklist in the authoring guide by hand.
8. **Test.** Run it on a realistic input. Compare with the good and bad examples. Add an eval case in `evals/cases/` for new behavior.
9. **Ship.** Bump the version and `last_reviewed`, add to a bundle, and note the change in `CHANGELOG.md`.

## Output

The SKILL.md (and any supporting files), the validation result, the test result, and a list of what to update (bundle, changelog, eval case).

## Quality gate

1. Validation passes with no errors.
2. The description routes correctly on a positive and a negative example.
3. The skill states its approval gates and its internal versus buyer-facing boundary where relevant.
4. No scripts in the skill folder; no secrets; no client data in `core/`.
5. The output of a test run follows the output section exactly.
