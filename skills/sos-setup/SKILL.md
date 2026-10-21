---
name: sos-setup
description: "Set up Sales-OS for a company or seller by interviewing for business info, sales motion, writing style and thresholds, and writing the context library. Use when starting a new client instance, when the context library is empty or template text, or when the user wants to update company facts."
compatibility: "Any Agent Skills client. File access recommended to write the context library; otherwise returns the files as text."
metadata:
  version: "1.0.0"
  layer: system
  last_reviewed: "2026-10-17"
  includes: "scaffold/workspace/context-library/business-info.md, scaffold/workspace/context-library/sales-motion.md, scaffold/workspace/context-library/writing-style.md, shared/interview-protocol.md, shared/operating-rules.md, shared/capabilities.md, shared/output-conventions.md"
---

# Setup

Fill the context library so every other skill speaks the client's language and uses the client's thresholds. Do it by interview, three questions at a time, and write down only what the user says.

Read `references/operating-rules.md`, `references/capabilities.md` and `references/interview-protocol.md`. The files to produce follow the structures in `references/business-info.md`, `references/sales-motion.md` and `references/writing-style.md`. Where they go is in `references/output-conventions.md`.

## When to use

- A new instance, or the context library is empty or still template text.
- The company, product, ICP or process has changed.
- The user wants to tune thresholds, stages or voice.

## Inputs

The user's answers; optionally existing documents (pitch deck, website text, playbook, sample emails). Do not research the company unless asked; setup records what the client says.

## Procedure

1. **Check state.** Read the existing context library files. Say what is filled and what is still template text.
2. **Interview in this order, three questions a turn:**
   - Business info: what the company sells, to whom, outcomes customers get, proof points, differentiators, competitors, the Ideal Customer Profile built from best existing customers.
   - Sales motion: stages and exit criteria, typical deal size and cycle, number of buying influences, the thresholds that decide Blue Sheet versus qualification card, forecast categories, tools (CRM, meeting notes), review cadence.
   - Writing style: ask for two or three examples the user is proud of, plus what to avoid; capture rules, not adjectives.
   - Guardrails: what must never be shared externally, approved tools for customer data, approval rules for outbound.
3. **Summarize after each section** in two to four lines and ask to confirm or correct.
4. **Write the files**, keeping the template headings. Mark anything unknown as Unknown rather than guessing. Use the user's own words.
5. **Mark promotion.** The context library is read-mostly: propose the files, and write them only after the user approves.
6. **Offer next steps:** build a Blue Sheet on a live deal, or load the company playbook into a Gemini Notebook (`sos-notebook-pack`).

## Output

Updated files in `workspace/context-library/` with a list of what changed, or the file contents in blocks when there is no file access. A list of the five items still unknown.

## Quality gate

1. Nothing was invented about the company. Gaps say Unknown.
2. No sensitive customer data or credentials were recorded.
3. The user approved the final text before it was written.
4. The ICP derives from best customers, not aspirations; if the user gave aspirations, they are labelled as such.
