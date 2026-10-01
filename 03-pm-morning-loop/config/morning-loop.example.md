# Morning Loop config

Copy this file to `config/morning-loop.local.md` (git-ignored) and fill it in.
Keep the key names; commands read them by name.

## General

- max_priorities: 5          # most items the ranker may propose
- max_retries: 2             # maker/checker rounds before showing "unverified"
- daily_capacity: "6 focus hours"   # used by rubric R4 (S ≈ 1h, M ≈ 2-3h, L ≈ half day+)
- language: en

## Sources

Enabled sources, in order. Each name matches a file in `sources/`.

- tracker
- obsidian-todos

## Source settings

### tracker

- mcp_server: tracker                 # server name in .mcp.json
- scope: "assigned to me, open"       # free text, interpreted by sources/tracker.md
- project: "<project or group path>"
- lookback_days: 14                   # also fetch items updated in this window

### obsidian-todos

- vault_path: "/path/to/your/vault"
- todo_file: "Todo.md"                # relative to vault_path
- meetings_folder: "Meetings"         # relative to vault_path
- meetings_lookback_days: 7
