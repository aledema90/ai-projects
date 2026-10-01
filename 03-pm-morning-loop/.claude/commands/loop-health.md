---
description: Review how the loop is doing and whether it still earns its place.
---

Assess the health of the loop. Read-only.

1. Read `state/history.md` and `state/feedback-log.md`. If they are missing or have fewer
   than 5 runs, say there is not enough data yet and stop.
2. Report for the last 14 days:
   - runs, and how many were PASS / FAIL / UNVERIFIED
   - average retries
   - how often each source failed
   - number of corrections in `feedback-log.md` and which files they touched
   - how many `/apply` actions were taken (if recorded)
3. Apply the retirement rule: if there were **no corrections and no actions** in 14 days,
   nobody is steering or using this loop. Do not delete or disable anything. Ask the user:
   "Nothing was corrected or acted on in 14 days. Should this loop be switched off, or has it
   become noise you skim past?"
4. If one source fails often, or the same rule fails repeatedly, suggest the specific
   `/teach` correction that would fix it.
