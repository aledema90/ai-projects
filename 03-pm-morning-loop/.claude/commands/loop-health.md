---
description: Review how the loop is doing and whether it still earns its place.
---

Assess the health of the loop. Read-only.

1. Read `state/history.md`, `state/feedback-log.md` and the run folders in `state/`. If there are fewer
   than 5 runs, say there is not enough data yet and stop.
2. Report for the last 14 days:
   - runs, and per step: gate A failures, retries, overrides
   - gate B decisions: approved / edited / rejected, per step (a step that is always approved untouched
     may be too easy or no longer read; a step that is always rejected has a wrong instruction file)
   - actions applied in step 4, and checker differences found
   - sources that failed in step 1, and how often
   - corrections logged and which files they changed
3. Retirement rule: if there were **no edits, rejections, corrections or applied actions** in 14 days,
   nobody is steering this loop. Do not disable or delete anything. Ask: "Nothing was edited, rejected
   or applied in 14 days. Switch the loop off, or is it noise you skim past?"
4. If one rule fails gate A repeatedly, or one gate B keeps rejecting for the same reason, propose the
   specific `/teach` edit that would fix it.
