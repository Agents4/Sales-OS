---
name: mh-pipeline-review
description: "Review a pipeline across many opportunities using Blue Sheets and CRM data: hygiene metrics, forecast gate challenges, funnel balance and the deals that need a decision. Use when a manager, RevOps or seller needs a weekly pipeline review, a forecast call check, or a quarter-end hygiene sweep."
compatibility: "Any Agent Skills client. Best with shell access for the pipeline command; can work from pasted sheets or a CRM export."
metadata:
  version: "1.0.0"
  layer: methodology
  last_reviewed: "2026-10-17"
  includes: "templates/pipeline-report.md, methodology/funnel-and-pipeline.md, shared/crm-contract.md, shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Pipeline review

Turn many Blue Sheets into one evidence-based view. The point is to decide where attention goes this week, challenge forecast calls with the gates, and keep the funnel balanced.

Read `references/operating-rules.md` and `references/capabilities.md`. The zones, thresholds and forecast gates are in `references/funnel-and-pipeline.md`. CRM rules are in `references/crm-contract.md`. Use `assets/pipeline-report.md` as the output structure.

## When to use

- A weekly or monthly pipeline or forecast review.
- A manager preparing a 1:1 or a deal inspection session.
- A hygiene sweep before quarter end.

## Inputs

The workspace (`workspace/accounts/**/blue-sheet.md`) or a pasted set of sheets, plus the CRM export or connector for stage, amount, close date and owner. The scope: a seller, a team or a segment.

## Procedure

1. **Compute metrics.** With a shell run `python3 tools/sos.py pipeline` (add `--format csv --out <file>` for a spreadsheet export and `--today YYYY-MM-DD` for a reproducible run). Without a shell compute the metrics by hand from the sheets and say so.
2. **Reconcile with the CRM.** Differences in stage, amount, close date or contacts are findings. Show both values and do not choose silently.
3. **Challenge forecast calls.** For each Best case and Commit deal, check the gates. List the deals whose category is not supported, with the specific missing evidence. Gate failures are questions.
4. **Deals needing attention.** Stale sheets, past-due actions, red flags without actions, single- or double-threaded deals, Economic Buyer in Even Keel or Overconfident, close dates incompatible with the decision process.
5. **Funnel balance.** Count by zone. Flag a thin funnel behind a heavy Best Few, and Best Few overload.
6. **Calibrate.** If past outcomes are available, note which gates predicted wins and losses, to tune thresholds over time (suggest, do not change).
7. **Decisions requested.** The few choices that need a manager.
8. **Hygiene actions.** Propose tasks for sellers: update sheets, find the Economic Buyer, add actions. Do not write to the CRM without approval (`references/crm-contract.md`).

## Output

A pipeline report from the template (naming rules in `references/output-conventions.md`). With file access save to `workspace/outputs/reports/YYYY-MM-DD-pipeline.md` and reply with the headline, the three biggest forecast challenges and the decisions needed. Chat-only: report in one block.

## Quality gate

1. Metrics trace to sheets or CRM rows; counts are checked.
2. Each challenge names a deal and the specific missing evidence.
3. No false precision: no percent probabilities unless the client's motion defines them.
4. Internal-only content stays internal. Reports are for the team, not the customer.
