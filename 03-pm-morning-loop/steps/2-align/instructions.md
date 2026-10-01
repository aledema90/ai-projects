# Step 2: Align

**Goal:** check that the backlog matches the strategy, and that everything the user is holding
(to-dos, chat requests) is covered by a ticket. Report only; propose no fixes yet (that is step 3).

**Gate B:** yes. The user may correct ("that to-do is personal", "that ticket is already done").

## Input

Approved output of step 1 (items), `context/strategy.md`, config (`imminent_days`).

## Do

### Part A: backlog vs strategy

For each `backlog` item:
1. Link it to a goal (`G#`), a standing commitment (`C#`), or `NO GOAL`. Cite the number from the strategy.
2. Compare its priority label and due date with that link. Flag it when:
   - **under-prioritized:** serves a goal or commitment but has a low or missing priority label
   - **over-prioritized:** high priority but `NO GOAL`, or serves a non-goal (`N#`)
   - **imminent:** due within `imminent_days` (or overdue) regardless of priority
3. Items that are consistent need only a one-line entry.

### Part B: coverage

For every `notes` to-do, every `teams` item, and every `calendar` item that implies work (a meeting
action item written in the event description):
1. Find the backlog ticket that covers it: by ticket reference in the item, by matching title or
   keywords against `backlog` items. Never match on a vague similarity; if unsure, say `UNSURE` and
   explain.
2. Mark `COVERED by <ticket id>`, `UNCOVERED`, `PERSONAL` (clearly not backlog work, state why), or
   `UNSURE`.

## Output format (exactly)

```
ALIGNMENT
| ticket | priority | links to | status | note |
| backlog:12 | high | G1 | OK | |
| backlog:34 | none | NO GOAL | OVER-PRIORITIZED / UNDER-PRIORITIZED / IMMINENT / OK | evidence in one line |

IMMINENT DEADLINES
- <id> | due <date> | <title>

COVERAGE
| item | from | verdict | ticket / reason |
| notes:Todo.md#L4 | to-do | UNCOVERED | no ticket mentions "..." |
| teams:abc | message | COVERED | backlog:12 |

COUNTS
backlog items: N | to-dos: N | chat items: N | UNCOVERED: N | UNSURE: N
```

Every `backlog` item, every to-do and every chat item must appear exactly once.
