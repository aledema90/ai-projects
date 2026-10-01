# Rubric: Step 4 Apply

All rules are blocking. `raw` is the approved action list. The checker **re-reads each touched ticket
from the backlog tool** (read-only) and compares it with the approved content.

- **X-1 Only approved.** Every APPLIED row maps to an action id in the approved list. No extra action.
- **X-2 Nothing missing.** Every approved `H#`/`T#` action is either OK or ERROR in the output.
- **X-3 Read-back matches.** For each OK action, the live ticket has the approved labels, fields and
  description text exactly (title too for `T#`). Report any difference with both values.
- **X-4 No collateral change.** For `H#`, fields not listed in the approved action are unchanged
  (compare labels, assignee, milestone, title against `raw`'s before-values).
- **X-5 Links real.** Each reported url resolves to the ticket named in the row.
- **X-6 Errors reported.** Every ERROR row has the tool's message; none were retried or hidden.
