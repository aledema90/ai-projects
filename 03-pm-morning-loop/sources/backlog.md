# Source: backlog

**Purpose:** open work items from the issue/backlog tool, with deadlines and priority labels.

## Requires

- A connected backlog tool with read access (list, search, get).
- Config keys: `backlog_projects` (list of `path`, `rules_file`, `serves_goal`), `backlog_types`, `backlog_exclude_labels`.
- Rules for labels and required fields: `context/backlog-rules.md` (read it, you need the priority
  label names).

If the tool is not connected: `SOURCE_FAILED: backlog tool not available`.

## How to fetch (read-only)

1. For EACH entry of `backlog_projects`: list **open** items of the types in `backlog_types` in its `path`
   (a project or a group). Tag every item with its project in `fields: project`. Paginate until the last
   page. Skip items carrying any label in `backlog_exclude_labels`, and report how many you skipped.
2. For each item capture: id, title, url, state, labels, assignee(s), milestone/iteration, due date,
   created and updated dates, parent epic or group if the tool gives it cheaply, and a description
   status: `empty | template | filled` (write `not-assessed` for a project whose `rules_file` is `none`). Keep the description text only for items you need it for in
   step 3 hygiene (the checker will have access via `raw`).
3. Map to the common format:
   - `fields`: `labels`, `assignees`, `milestone`, `priority` (from the priority label, or `none`),
     `epic`, `description_status`
   - `due`: the due date, else the milestone due date marked `(milestone)`, else `none`
   - `signals`: `overdue`, `due-today`, `imminent` (due within `imminent_days`), `blocked` when the
     blocked label from `backlog-rules.md` is present

## Output

`count_fetched: N, count_skipped: M` followed by the items. An empty backlog is a success; say so.
