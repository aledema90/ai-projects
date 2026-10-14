# Step 3: Apply (layer 3)

**Goal:** execute exactly the actions the user approved at gate B of step 2. Nothing else.

**Gate B:** only if the checker reports a difference.

## Input

The approved action list from step 2 (`U#` updates, `C#` creations), with the exact text approved,
including human edits.

## Do

1. Skip this step if no action was approved.
2. Execute actions **one at a time**, in order.
   - `U#`: read the issue's current description. Add the approved text where the action says (end of the
     change-log section, or end of the description), following `context/issue-format.md`. Prefer
     a patch/append operation; if only full replacement exists, send the current description unchanged
     plus the approved text. Change nothing else: title, labels, assignees, milestone, state stay as
     they are.
   - `C#`: create the issue in the approved project with the approved title and description, type
     `issue`, no labels, assignees or milestone unless the approved action lists them.
3. After each action, record what the tool returned (issue url, iid, updated or created time).
4. On an error: stop that action, record the error, continue with the next one. Never retry a write: a
   create that may have succeeded must be checked by reading, never re-sent.
5. Never perform an action that is not in the approved list, and never alter approved content.

## Output format (exactly)

```
APPLIED
U1 | OK | grp/app#123 | <url> | appended <N> lines
C1 | OK | created grp/backlog#52 | <url>
U2 | ERROR | grp/app#88 | <error message>
SUMMARY
approved: N | applied: N | errors: N
```
