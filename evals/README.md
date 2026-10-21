# Evals

Realistic cases to test skills after a change. Each case has `input.md` (what the user supplies, fictional) and `expected.md` (what a good response must and must not do). Score with `rubric.md`.

| Case | Skill | What it tests |
|---|---|---|
| 01 | `mh-blue-sheet` | Messy notes with an unknown Economic Buyer and an untested Coach: no invention, red flags with actions |
| 02 | `mh-call-debrief` | Transcript with a personal detail, an Overconfident executive, a new stakeholder and a reorganization rumor |
| 03 | `mh-gold-sheet` | Single-threaded sponsor account: Critical Vulnerability, second Sponsor, Stop investment |
| 04 | `mh-outreach-draft` | Buyer-facing text built from a sheet full of internal analysis: leak check |

## How to run

1. Give the skill the `input.md` content as the user would (paste or attach), in the platform you care about, including chat-only mode.
2. Score the response with `rubric.md` against `expected.md`.
3. Record the result and date in your change notes. A change that regresses a "must" is not ready to ship.

Run at least cases 01 and 04 after any change to shared rules, and the matching case after a skill change. Add a case when a real failure appears.
