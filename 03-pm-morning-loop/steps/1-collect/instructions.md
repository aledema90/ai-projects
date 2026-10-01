# Step 1: Collect

**Goal:** read every configured source and return normalized items. Nothing more. No ranking, no advice.

**Gate B:** none (read-only step).

## Do

1. Read `config/morning-loop.local.md`. For each source in `Sources`, follow `sources/<name>.md`
   and the common format in `sources/README.md`.
2. Windows: backlog = all open (in scope); notes = open to-dos; teams = yesterday only;
   calendar = today only.
3. If a source fails, record `SOURCE_FAILED: <reason>` for it and continue.

## Output format (exactly)

```
SOURCES
- backlog: OK | FAILED (<reason>) | count_fetched: N | count_skipped: M
- notes:   OK | FAILED (<reason>) | count_fetched: N
- teams:   OK | FAILED (<reason>) | count_scanned: N | count_kept: K
- calendar: OK | FAILED (<reason>) | count_fetched: N

ITEMS
<one block per item, in the common item format, grouped by source>
```
