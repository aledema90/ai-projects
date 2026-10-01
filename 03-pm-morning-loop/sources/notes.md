# Source: notes

**Purpose:** the user's personal to-do list, kept in a notes tool (Obsidian vault in the default setup).

## Requires

- Read access to the folder `vault_path`.
- Config keys: `vault_path`, `todo_file`.

If unset or unreadable: `SOURCE_FAILED: notes not readable`.

## How to fetch (read-only)

1. Read `<vault_path>/<todo_file>`. Every unchecked task (`- [ ]`) is an item.
   - Due dates: `📅 YYYY-MM-DD`, `due:: YYYY-MM-DD` or `due YYYY-MM-DD`.
   - `#tags` and `[[links]]` go into `fields`.
   - Checked tasks completed in the last 3 days: return as `state: done` (so step 2 does not propose
     tickets for finished work). Ignore older ones.
2. Map to the common format:
   - `id`: `notes:<file>#L<line>`; `type: todo`; `url`: file path and line
   - `updated`: the file's modification date
   - `fields`: `tags`, `links`, `ticket_ref` if the line already contains a ticket id or link
     (important for coverage in step 2)

## Output

`count_fetched: N` followed by the items. Never modify the vault.
