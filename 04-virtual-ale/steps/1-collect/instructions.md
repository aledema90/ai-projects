# Step 1: Collect (layer 1)

**Goal:** read every configured source inside the run window and return normalized items plus the branch
change report. Nothing more. No merging, no linking, no advice.

**Gate B:** none (read-only step).

## Do

1. Read `config/po-loop.local.md`. For each source in `Sources`, follow `sources/<name>.md` and the common
   format in `sources/README.md`. Read the sources in parallel.
2. Window: `window.from` to `window.to`, given by the orchestrator. The same window for every source.
3. If a source fails, record `SOURCE_FAILED: <reason>` for it and continue.

## Output format (exactly)

```
WINDOW <from> → <to>

SOURCES
- gitlab: OK | PARTIAL (<failed projects>) | FAILED (<reason>) | <count line from sources/gitlab.md>
- teams:  OK | PARTIAL (<failed part>) | FAILED (<reason>) | <count line from sources/teams.md>
- meetings: OK | FAILED (<reason>) | <count line from sources/meetings.md>

ITEMS
<one block per item, in the common item format, grouped by source>

BRANCH REPORT
<as defined in sources/gitlab.md>
```
