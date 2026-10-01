---
description: Execute actions on chosen priorities, only after the user approves each exact action.
argument-hint: "[priority numbers, e.g. 1 3]"
---

Act on priorities from today's run: $ARGUMENTS

1. Read `state/last-run.md`. If it is not from today or the numbers don't exist, say so and stop.
2. For each chosen priority, draft the exact action from its "first step": the tool, the
   target, and the full text of any comment, message, status change or note edit.
3. Show all drafted actions together. **Stop and wait.** Do not execute anything yet.
4. Execute only the actions the user explicitly approves in their reply, exactly as shown.
   If they change the wording, show the new version and ask again.
5. Report what was done and what failed. Never retry a failed write without asking.
6. Append one line per executed action to `state/history.md`: `date | apply | <item id> | <action>`
   (`/loop-health` counts these).

Never take an action that was not drafted and approved in this conversation.
