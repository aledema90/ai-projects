# Backlog rules

Copy this file to `context/backlog-rules.md` (git-ignored) and describe how YOUR backlog is organised.
Steps 1 and 3 read it: the label names, which fields are required, and what counts as hygiene.
If you already have a hygiene checklist or skill, paste its rules here with the same ids.

## Labels

Use exact strings, case-sensitive.

- Priority labels, highest first: `<priority::high>`, `<priority::medium>`, `<priority::low>`
- Status labels: `<status::backlog>` (not active), `<status::doing>`, `<status::blocked>`, ...
- Type labels (one expected): `<type::story>`, `<type::bug>`, ...
- Team labels (one expected): `<team::a>`, `<team::b>`
- "Active" = any status label other than `<status::backlog>`

## Required fields

- Always: description (not empty, not the unfilled template), type label, team label, status label.
- When active: assignee, milestone or iteration.

## Hygiene rules (ids are cited by the checker)

- HY1: no labels at all
- HY2: missing type label
- HY3: missing team label
- HY4: missing status label
- HY5: active item without assignee
- HY6: active item without milestone/iteration
- HY7: empty or template description
- HY8: blocked item (needs a decision)
- HY9: open item whose status says it shipped or is done
- HY10: no update for 180+ days

## Template detection

Phrases that show the issue template was left unfilled: `<placeholder phrase 1>`, `<placeholder phrase 2>`

## New ticket template

Title: short, outcome-oriented, max 80 characters.

```markdown
## Context
<why this matters, from the source>

## Description
<what to do>

## Acceptance Criteria
- [ ] <verifiable criterion>

## Source
<where it came from + a short quote>
```

Default labels for a new ticket: `<type::story>`, `<status::backlog>`; team label must be asked, never guessed.
