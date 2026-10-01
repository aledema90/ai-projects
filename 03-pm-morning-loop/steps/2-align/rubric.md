# Rubric: Step 2 Align

All rules are blocking. `raw` is the approved output of step 1; strategy is `context/strategy.md`.

- **A1 Complete.** Every `backlog` item appears once in ALIGNMENT; every to-do, every chat item
  appears once in COVERAGE. The COUNTS line equals the real counts in `raw`.
- **A2 Real references.** Every `G#`, `C#`, `N#` cited exists in the strategy file. Every ticket id
  exists in `raw`. No invented ids.
- **A3 Evidence for flags.** Each OVER-/UNDER-PRIORITIZED or IMMINENT flag names the priority label,
  due date or goal that justifies it, and the values match `raw`.
- **A4 Imminent list is exact.** IMMINENT DEADLINES contains every item due within `imminent_days` or
  overdue, and nothing else. Recompute from the dates.
- **A5 COVERED is true.** For each COVERED row, the cited ticket exists and its title or description
  (`raw`) really relates to the item (shared reference or specific shared terms). A guess fails.
- **A6 UNCOVERED is true.** For each UNCOVERED row, search `raw` backlog titles and descriptions for the
  item's key terms. If a plausible match exists, the row should be COVERED or UNSURE: fail.
- **A7 PERSONAL and UNSURE justified.** Each has a one-line reason grounded in the item text.
- **A8 Non-goals.** Every ticket that serves a non-goal (`N#`) is flagged OVER-PRIORITIZED or
  explicitly noted; none is rated OK.
