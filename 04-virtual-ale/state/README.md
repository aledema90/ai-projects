# state/

The loop's memory. Everything here except this file and `run.template.md` is git-ignored.

| Path | Written by | Purpose |
| --- | --- | --- |
| `<YYYY-MM-DD-HHMM>/1-collect.md` ... `3-apply.md` | `/po` | One file per step per run: status, retries, gate A verdict, gate B decision, output. Lets a run resume (`/po resume`) or restart from a step (`/po from 2`). |
| `last-run.md` | `/po` | End of the last completed window. The next run starts here. |
| `branch-log.md` | `/po` step 1 | Persistent log of branch changes, one section per window. |
| `applied-log.md` | `/po` close | Every source item already written to an issue. Step 2 uses it to avoid duplicates. |
| `history.md` | `/po` close | One line per run. |
| `feedback-log.md` | `/teach` | Each correction and the file it changed. |

Deleting a run folder is safe. Deleting `last-run.md` makes the next run re-read `initial_lookback_days`;
`applied-log.md` still prevents duplicate updates.
