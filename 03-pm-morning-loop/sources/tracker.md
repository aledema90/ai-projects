# Source: tracker

**Purpose:** open work from an issue tracker (GitLab, GitHub, Jira, Linear...), via MCP.

## Requires

- An MCP server named by `tracker.mcp_server` in the config, declared in `.mcp.json`.
- Config keys: `scope`, `project`, `lookback_days`.

If the server is not connected or its tools are not available, return
`SOURCE_FAILED: tracker MCP not available`.

## How to fetch (read-only)

1. Use the server's read/list/search tools only. Do not call any create, update,
   comment, close or transition tool.
2. Fetch items matching `scope` in `project`: open items assigned to or mentioning
   the user, open review/merge requests awaiting the user, and anything updated in
   the last `lookback_days` days (including recently closed, for the checker).
3. For each item that looks blocked, due soon, or recently commented, read the latest
   comments to fill `signals`. Do not read comments for every item.
4. Map each result to the common item format in `sources/README.md`:
   - `id`: `tracker:<native id>`
   - `state: blocked` if labelled blocked or waiting on another person (`blocked-on:<who>`)
   - `due`: the due date field if present, else `none`

## Output

A list of items in the common format. If nothing matches, return an empty list
(that is a success, not a failure).
