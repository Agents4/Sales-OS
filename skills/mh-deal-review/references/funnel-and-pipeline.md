---
name: funnel-and-pipeline
description: Funnel zones, which deals get which sheet, and forecast hygiene gates
---

# Funnel and pipeline discipline

Tags: **[C]** canonical, **[V]** convention, **[X]** Sales-OS extension.

## The funnel zones [C]

Strategic Selling manages the pipeline as a funnel with three zones. The point is to decide where planning effort goes.

| Zone | Meaning | Effort |
|---|---|---|
| **Above the funnel** | Suspects. Not yet qualified. | Prospecting and qualification only. No Blue Sheet. |
| **In the funnel** | Qualified and actively worked. | A light qualification card; a Blue Sheet draft once it is likely to move to Best Few. |
| **Best Few** | The opportunities closest to closing that deserve your best planning. | Full Blue Sheet, Green Sheets for every important call, weekly re-walk. |

The discipline [C, as commonly taught]: touch all three zones every week, in inverse proportion to time to close. The failure mode is working only the Best Few late in the quarter and facing an empty funnel next quarter.

An **Ideal Customer Profile** [C] built from the shared characteristics of your best existing customers (not an aspirational list) is how deals get into the funnel. Accounts that clearly miss it are disqualified, not nurtured.

## Which sheet for which deal [X]

Thresholds are defaults. A client sets its own in `workspace/context-library/sales-motion.md`.

| Situation | Planning artifact |
|---|---|
| Transactional or small deal | Qualification card only (ICP fit, need, access to decision-maker, timeline). No Blue Sheet. |
| Mid-size, 2-3 influences, short cycle | Blue Sheet "light": SSO, influences, Win-Results, red flags, actions. Skip fit and decision-process tables. |
| Complex: more than three influences, long cycle, or deal value above the client's threshold | Full Blue Sheet, Green Sheet before each key call |
| Strategic account | Gold Sheet plus Blue Sheets under it |

## Review rhythm [V]

- Best Few: re-walk weekly. A Best Few sheet older than 7 days is stale.
- In the funnel: review every 2 weeks. Stale limit 14 days.
- Above the funnel: review qualification monthly.
- Gold Sheets: every 60-90 days and on triggers.

Sales-OS lint thresholds follow these defaults (7 and 14 days) and can be changed with flags.

## Forecast hygiene gates [X]

A Blue Sheet should not support a forecast category it has not earned. These gates are Sales-OS rules, not Miller Heiman doctrine. They make forecast conversations concrete.

| Category | Minimum evidence on the Blue Sheet |
|---|---|
| **Pipeline** | SSO written; at least one influence named; ICP fit judged |
| **Best case** | Economic Buyer identified; Coach identified and tested; modes known for the EB and the main User and Technical Buyers; no high-severity red flag without a dated action |
| **Commit** | Economic Buyer met and their Win-Result known (F or I with source); Coach has delivered unwelcome news at least once; decision process and approval path known; security, legal and finance gates scheduled within the runway; Best Action Commitment accepted on the last interaction; no Economic Buyer in Even Keel or Overconfident |

Use the gates in `mh-pipeline-review` and `mh-deal-review` to challenge a forecast call. A gate failure is not a verdict; it is a specific question to answer.

## Pipeline hygiene metrics [X]

Track these weekly from the Blue Sheets (the `pipeline` command computes most of them):

- Best Few deals with an identified Economic Buyer (target 100%).
- Best Few deals with a tested Coach.
- Red flags without a dated action (target zero).
- Sheets older than the stale limit.
- Past-due actions.
- Single- or double-threaded Best Few deals.
- Win rate by whether the Economic Buyer was met before the proposal (use it to calibrate the gates over time).
