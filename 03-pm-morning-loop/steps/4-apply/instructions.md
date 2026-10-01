# Step 4: Apply

**Goal:** execute exactly the actions the user approved at gate B of step 3. Nothing else.

**Gate B:** only if the checker reports a difference.

## Input

The approved action list from step 3 (ids `H#`, `T#`; `P#` prep notes need no execution), with the exact
content approved, including human edits.

## Do

1. Skip this step entirely if no `H#` or `T#` action was approved.
2. Execute actions **one at a time**, in order. For each:
   - `H#`: update the ticket: add the approved labels, set the approved fields, replace the description
     with the approved draft. Change nothing else on the ticket.
   - `T#`: create the ticket with the approved title, labels and description in the project named on the approved draft (one of the `backlog_projects` paths).
3. After each action, record what the tool returned (ticket id and url).
4. On an error: stop that action, record the error, continue with the next action. Never retry a write.
5. Never perform an action that is not in the approved list, and never alter approved content.

## Output format (exactly)

```
APPLIED
H1 | OK | <ticket id> | <url> | changes: <what was changed>
T1 | OK | created <ticket id> | <url>
H2 | ERROR | <ticket id> | <error message>
SUMMARY
approved: N | applied: N | errors: N
```
