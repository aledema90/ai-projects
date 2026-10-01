# Checker rubric

The checker applies every rule below to the ranker's output. Verify against the
raw items and the strategy, not against how convincing the output sounds.

Rules are **blocking** (any failure = FAIL) or **warning** (reported, does not fail).
Edit this file to change the checker; `/teach` does it for you.

## Blocking

- **R1 Traceability.** Every priority cites an item id that exists in the raw
  items. No id, or an id not in the raw data = fail.
- **R2 Not already done.** No priority whose item is closed, merged, done or
  checked off in the raw data.
- **R3 No repeats.** An item listed in `state/last-run.md` "Already surfaced" may
  reappear only if the raw data shows a new signal since (new comment, status
  change, nearer deadline). The reason must name that signal.
- **R4 Capacity.** Sum of efforts (S≈1h, M≈2-3h, L≈4h+) fits `daily_capacity`.
  Count at most `max_priorities` items.
- **R5 Strategy link.** Every priority names the goal, standing commitment or
  tie-breaker in `strategy.md` it serves. "General productivity" does not count.
  If strategy.md is missing (example used), this rule is downgraded to warning.
- **R6 Deadlines first.** Any raw item due today or overdue is either in the
  priorities or listed in "Not today" with a stated reason.

## Warning

- **R7 Concrete first step.** Each priority has a first step doable in under 15
  minutes ("Reply to X with Y", not "Work on X").
- **R8 One-line reason.** Reason is one line and states why *today*.
- **R9 Non-goals.** No priority serves something listed under Non-goals.
- **R10 Blocked on others.** Items waiting on someone else appear as a "ping"
  action (S effort), not as work.

## Verdict format

```
VERDICT: PASS | FAIL
BLOCKING FAILURES: R# - what, which priority, evidence from raw data
WARNINGS: R# - what
FIXES: concrete instruction for the ranker, one per failure
```
