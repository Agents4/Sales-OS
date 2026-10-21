# Building Sales Agents with Grok Bots

Grok Bots are long-lived agents that share your cloud computer, keep memory across turns, and can run routines on a schedule or trigger. They are a strong fit for sales operating system work that should persist while you are away.

Because Sales-OS is plain Markdown on Google Drive, the same artifacts work with Grok Bots, Cursor, Claude Code, and other tools.

## Why Grok Bots for Sales-OS

- **Persistent memory** of account context, stakeholder relationships, and prior Blue / Green / Gold Sheet decisions.
- **Scheduled routines** for weekly deal hygiene, Blue Sheet reminders, pipeline reviews, or pre-meeting Green Sheet generation.
- **Drive / email / calendar access** when connected, so the bot can read recent activity, meeting notes, or CRM exports.
- **Tool-agnostic core** — the bot reads and writes the same Markdown files used by Cursor or other agents.
- **Deep Cursor integration** (see section below) for handing heavier multi-file or coding-style work to Cursor cloud agents.

## Recommended Bot Purposes

Create separate bots for distinct standing duties rather than one overloaded bot.

1. **Deal Coach Bot**  
   Purpose: Maintain and re-walk Blue Sheets for active opportunities. Surface red flags, missing Economic Buyers, and unowned actions.  
   Typical routines: Weekly review of open red flags; post-call update prompts.

2. **Call Prep Bot**  
   Purpose: Generate Green Sheets and mode-aware Conceptual Selling questions from the current Blue Sheet.  
   Trigger: On demand or before known meetings.

3. **Pipeline Hygiene Bot**  
   Purpose: Scan active opportunities for missing influences, stale Blue Sheets, or unowned red flags.  
   Schedule: Monday morning or Friday afternoon.

4. **Account Strategy Bot** (optional, for key accounts)  
   Purpose: Keep Gold Sheets current, track white space, and link active Blue Sheets to the longer-term account plan.

## How to Set One Up

1. In Grok, create a new bot with a clear name and description that matches the purpose above.  
2. Give it access to the Sales-OS folder on Drive (or the relevant subfolder).  
3. In the bot’s instructions (or first prompt), point it at `SALES-OS.md` and the methodology rules (Blue / Green / Gold altitudes, four influences, modes, win-results, red flags).  
4. Define the output location: always write drafts to `outputs/` and ask before promoting anything to `context-library/`.  
5. For a routine, ask the bot to save a scheduled prompt that loads the relevant sheets, runs the checks, and writes a summary.

## Example Routine Prompt (Weekly Deal Hygiene)

```
Every Monday at 8:00 AM local time:
1. List all Blue Sheets in context-library/blue-sheets/ and outputs/blue-sheets/ modified in the last 14 days.
2. For each, check:
   - Is there a named Economic Buyer?
   - Are response modes and personal win-results filled or marked Unknown?
   - Does every red flag have a linked action with an owner and date?
3. Produce a short summary of open risks and suggested next actions.
4. Write the summary to outputs/deal-reviews/YYYY-MM-DD-weekly-hygiene.md.
5. Do not modify the original Blue Sheets unless I explicitly approve the changes.
```

## Using Grok Bot with Cursor

Grok and Cursor are tightly integrated (shared ownership, native Grok models in Cursor, Grok Bot able to launch Cursor cloud agents). For Sales-OS work, the practical division of labor is:

### Shared source of truth
Keep the Sales-OS folder on Google Drive. Both Grok Bots and Cursor (via Drive sync, local clone, or MCP/Drive connector) can read and write the same Markdown files. This avoids version drift.

### When to use which

| Need | Prefer | Why |
|------|--------|-----|
| Scheduled weekly hygiene, reminders, overnight checks | Grok Bot | Persistent, runs while you’re away, memory across turns |
| Quick Green Sheet before a call, on-demand deal coaching | Grok Bot or Cursor chat | Both work; Bot is better if it already holds the account context |
| Deep multi-file analysis (many Blue Sheets, generate summary reports, build custom scripts) | Cursor (with Grok model) | Stronger multi-file editing, Composer/Agent modes, local or cloud agent execution |
| Generate or heavily revise structured templates, dashboards, or processing scripts | Cursor cloud agent (hand off from Grok Bot) | Bot can launch a Cursor cloud agent on a repo or workspace that contains the Sales-OS files |
| Interactive editing while you are in the IDE | Cursor | Inline edits, Composer, direct file system access |

### Practical handoff patterns

1. **Grok Bot → Cursor cloud agent**  
   Ask the Bot:  
   “Hand this to a Cursor cloud agent. Use the Sales-OS workspace. Read all active Blue Sheets in outputs/blue-sheets/, produce a single deal-review summary Markdown with open red flags and recommended actions, and open a pull request or write the file to outputs/deal-reviews/.”  
   The Bot launches the agent; you review the result.

2. **Cursor → Grok Bot**  
   From a Cursor session (or via the `cursor-grokbot-agents` BDK extension), consult a named sales Bot for account context or methodology guidance, then bring the reply back into the Cursor conversation.

3. **Local Cursor + Drive-synced Sales-OS**  
   Sync or clone the Sales-OS folder locally. Open it as a Cursor project. Use Grok models inside Cursor for interactive work. Let Grok Bots continue to run scheduled routines against the Drive copy. Promote finalized outputs from `outputs/` into `context-library/` as the shared source of truth.

4. **MCP / connectors**  
   If you have Google Drive or other sales tools connected in Cursor (or via AnythingMCP-style bridges), the Cursor agent can query live data while the Grok Bot maintains the long-lived planning documents.

### Best practices for the combined workflow

- Treat `SALES-OS.md` and the templates as the contract both tools must follow.  
- Grok Bot owns the “always-on” harness (schedules, memory, notifications).  
- Cursor owns heavy interactive or multi-file generation when you are present or when you explicitly hand off.  
- Always re-load the current Blue / Green / Gold Sheet at the start of a session rather than relying solely on memory.  
- Human review remains required for customer-facing output or forecast-impacting changes.  
- When either tool proposes a methodology improvement, promote the rule into `SALES-OS.md` so both benefit.

## Salesforce MCP Options (when available)

If the Grok Bot (or Cursor) has Salesforce MCP access (Salesforce Hosted MCP Servers — SObject reads/mutations, SOQL, etc.), use it to ground planning in live CRM data.

**Common patterns:**
- **Seed Blue Sheets:** Query Opportunity + OpportunityContactRoles + recent Activities to pre-populate influences, amount, close date, and stage.
- **Hygiene routines:** “Find open Opportunities over $50K with no next step or last activity > 14 days; flag those missing an Economic Buyer mapping.”
- **Green Sheet prep:** Pull the specific Contact’s role, recent interactions, and open Tasks before generating questions.
- **Gold Sheet context:** Pull Account hierarchy, all related open Opportunities, and key Contacts for multi-year planning.
- **Write-back (after approval):** Update Opportunity stage, close date, description, or a custom field after the human reviews the Markdown draft.

**Example routine addition (with Salesforce):**
```
Also query Salesforce for open Opportunities owned by me with Amount > 25000 and LastActivityDate < LAST_N_DAYS:14.
Cross-reference against Blue Sheets. Flag any Opportunity without a corresponding recent Blue Sheet or with mismatched close date/amount.
```

**Guardrails:**
- Prefer read operations by default. Require explicit confirmation before any create/update.
- Markdown sheets stay the methodology source of truth; Salesforce stays the pipeline system of record.
- Run as the authenticated user so sharing and field-level security are respected.
- If MCP is unavailable, fall back cleanly to Drive files and note the gap.

## Best Practices (Grok Bot specific)

- Keep the bot’s standing purpose narrow. A bot that only does deal hygiene stays more reliable than one that also writes emails and does research.  
- Use the verification prompt from the prompt engineering guide as part of the bot’s routine.  
- Start with one bot (Deal Coach or Pipeline Hygiene). Expand only after the first routine is producing reliable, low-noise output.

## Limitations

Grok Bots excel at persistent, scheduled, file-aware work and memory. Cursor (especially with cloud agents and Composer) is stronger for deep multi-file editing, code-like processing of the Markdown artifacts, and interactive IDE workflows. Use both: the Bot for the ongoing operating rhythm, Cursor for intensive sessions or handoffs.
