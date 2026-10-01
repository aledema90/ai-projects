# Source: obsidian-todos

**Purpose:** open to-dos and recent meeting action items from an Obsidian vault.

## Requires

- Read access to the folder `vault_path` (config).
- Config keys: `vault_path`, `todo_file`, `meetings_folder`, `meetings_lookback_days`.

If `vault_path` is unset or unreadable, return `SOURCE_FAILED: vault not readable`.

## How to fetch (read-only)

1. Read `<vault_path>/<todo_file>`. Each unchecked task (`- [ ]`) is an item.
   - Parse due dates written as `📅 YYYY-MM-DD`, `due:: YYYY-MM-DD` or `due YYYY-MM-DD`.
   - Parse `#tags` and `[[links]]` into `summary`.
   - Checked tasks (`- [x]`) completed in the last 3 days are returned as `state: done`
     (needed for checker rule R2); older ones are ignored.
2. List notes in `<vault_path>/<meetings_folder>` modified in the last
   `meetings_lookback_days` days. In each, extract action items: unchecked tasks, and
   lines under headings like "Action items", "Next steps", "To do". Keep only those
   that name the user or have no owner.
3. Map to the common item format in `sources/README.md`:
   - `id`: `obsidian:<relative file path>#L<line>`
   - `type`: `todo` for the to-do file, `meeting-action` for meeting notes
   - `url`: the file path and line
   - `updated`: file modification date

## Output

A list of items in the common format. Never modify the vault during collection.
