# Rollout playbook

How to take Sales-OS from a folder to a habit in a sales team. Written for the first Google-based client; adjust for others. Technical setup for Google is in `adapters/google/`.

## Principles

- Start with one team and live deals. Sheets built on real deals get used; sheets built in training do not.
- Quality before volume: five good Blue Sheets beat fifty stale ones.
- Make the managers use it first. If deal reviews do not use the sheets, sellers stop updating them.
- Automate after the habit exists, not before.

## Phases

### Phase 0: Prepare (week 0)

- Confirm account types, licenses and which Google or Microsoft tier applies (`adapters/google/platform-facts.md` or `adapters/microsoft/platform-facts.md`, verify list).
- Confirm data policy: which tools may hold customer data.
- Confirm Miller Heiman licensing and terminology with the client.
- Choose the pilot team (5 to 10 sellers, 1 manager) and one executive sponsor.
- Create the client instance: `new-instance` (`--platforms google`, `microsoft` or both). Set Drive offline access, or OneDrive "Always keep on this device" (`adapters/microsoft/onedrive-sharepoint-setup.md`).

### Phase 1: Foundation (weeks 1 to 2)

- Run `sos-setup` with the sales leader: business info, ICP, sales motion, thresholds, writing style.
- Load the Methodology coach notebook. Hold a 45-minute enablement session: three sheets, four influences, modes, Win-Results, red flags.
- Each pilot seller builds one Blue Sheet on a live deal with `mh-blue-sheet`.
- Define the planning thresholds: which deals get which artifact.

### Phase 2: Habit (weeks 3 to 6)

- Call prep and debrief become routine: `mh-green-sheet` before, `mh-call-debrief` after.
- Weekly deal review uses the sheets and `mh-deal-review`.
- Run `sos-sheet-lint` weekly; the manager looks at red flags without actions and stale sheets.
- Collect lessons into `lessons.md`; review them every two weeks (`sos-ratchet`).

### Phase 3: Scale (weeks 7 to 12)

- Add the manager and strategic-account bundles: `mh-pipeline-review`, `mh-win-loss-review`, `mh-gold-sheet` for key accounts.
- Build account rooms in Gemini Notebook for the top accounts.
- Add connectors (Drive, Calendar, Gmail drafts, CRM read) if the data hygiene supports it.
- Roll to the next team.

### Phase 4: Automate and improve (quarter 2)

- Workflow Builder routines: weekly hygiene report, pre-call brief, stale sheet nudges.
- CRM summary fields (`core/shared/crm-contract.md`).
- Calibrate forecast gates against outcomes.
- Add client-specific skills in `local/skills/`.

## Roles (RACI)

| Activity | Sales leader | Manager | Seller | RevOps / admin | Consultant |
|---|---|---|---|---|---|
| Thresholds and process | A | C | C | R | R |
| Context library | A | C | C | R | R |
| Sheets on deals | I | A | R | I | C |
| Deal and pipeline reviews | I | R, A | C | C | C |
| Platform setup and access | I | I | I | R, A | R |
| Lessons and improvements | A | R | C | R | R |
| Data and security policy | A | C | I | R | C |

R responsible, A accountable, C consulted, I informed.

## Measures

Leading (weekly):
- Share of Best Few deals with a current Blue Sheet.
- Best Few deals with an identified Economic Buyer and a tested Coach.
- Red flags without a dated action (target zero).
- Share of important calls with a Green Sheet and a debrief.

Lagging (monthly and quarterly):
- Forecast accuracy by category, and by whether gates were met.
- Win rate when the Economic Buyer was met before the proposal, versus not.
- Cycle length and slippage.
- No-decision rate.

Adoption health: sheets edited in the last 14 days, active users per week, time to build a sheet.

## Client checklist

- [ ] Licenses and account types confirmed; tier chosen
- [ ] Data policy agreed; approved tools listed in the context library
- [ ] Drive or OneDrive folder set offline; doctor passes
- [ ] Instance created; build passes
- [ ] Context library filled and approved
- [ ] Enablement session held; recording or notebook shared
- [ ] Pilot team and deals chosen
- [ ] Manager review cadence in calendars
- [ ] Lessons review scheduled
- [ ] Executive sponsor named

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Sheets go stale | Weekly review uses them; lint flags stale ones; keep sheets short |
| Sellers fear surveillance | Position as the seller's tool; managers use it for coaching, not scoring |
| Over-trust in AI output | Evidence tags; review the three open questions; no invention rule |
| Internal analysis leaks | Leak checks; narrow notebook sharing; CRM contract |
| Platform change breaks setup | Dated platform facts; verify list; portable fallback |
| Licensing issue | Confirm before launch; use client's own wording where licensed |
