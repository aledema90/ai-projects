# Rubric: Step 3 Apply

All rules are blocking. `raw` is the approved action list plus each updated issue's description, title,
labels, assignees and milestone as read in step 2 (the before-values). The checker **re-reads each
touched or created issue from GitLab** (read-only) and compares.

- **X1 Only approved.** Every APPLIED row maps to an approved `U#` or `C#`. No extra action.
- **X2 Nothing missing.** Every approved action is either OK or ERROR in the output.
- **X3 Read-back matches.** For each OK `U#`, the live description equals the before-value with the
  approved text added in the approved place. For each OK `C#`, the live issue is in the approved project
  with exactly the approved title and description. Report any difference with both values.
- **X4 No collateral change.** For `U#`: title, labels, assignees, milestone and state equal the
  before-values. For `C#`: no labels, assignees or milestone beyond those approved.
- **X5 No duplicate creation.** For each `C#`, exactly one issue with the approved title was created in
  the window of this step (search the project).
- **X6 Links real.** Each reported url resolves to the issue named in the row.
- **X7 Errors reported.** Every ERROR row has the tool's message; none were retried or hidden.
