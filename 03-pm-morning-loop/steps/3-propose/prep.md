# Step 3, lane P: Meeting prep

**Goal:** a short prep note for each of today's meetings. Read-only.

## Input

Step 1 `calendar` items (skip those with signal `excluded`), `backlog`, `notes` and `teams` items,
approved step 2 output, customer material in `context/customers/`, and recent meeting notes in
`<vault_path>/<meetings_folder>` (read-only, for context).

## Do

For each non-excluded event, in time order:
1. Find related material by attendee names, title keywords and linked tickets: tickets, to-dos, chat
   messages, past meeting notes, customer files.
2. Write the note. Every statement must cite its source id or file name in brackets.
3. If you find nothing for a section, write `none found`. Do not pad.

## Output format (exactly)

One block per meeting, at most 15 lines each:

```
PREP
P1 | <HH:MM-HH:MM> | <title> | with: <attendees as in the calendar>
   goal (inferred from title/description, say "unclear" if so):
   related: <ticket ids with one-line status> [sources]
   open to-dos: <items> [sources]
   customer context: <facts> [file] | no customer material
   bring/ask: <up to 3 concrete questions or decisions>
P2 | ...
```

Number `P1..Pn`, one per meeting. Meetings skipped as excluded are listed on one line at the end.
