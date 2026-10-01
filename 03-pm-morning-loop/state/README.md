# state/

The loop's memory. Everything here except this file and `run.template.md` is git-ignored.

| Path | Written by | Purpose |
| --- | --- | --- |
| `<date>/1-collect.md` ... `4-apply.md` | `/morning` | One file per step per day: status, retries, gate A verdict, gate B decision, output. Lets a run resume (`/morning resume`) or restart from a step (`/morning from 2`). |
| `history.md` | `/morning` | One line per run. Read by `/loop-health`. |
| `feedback-log.md` | `/teach` | Each correction and the file it changed. Read by `/loop-health`. |

Deleting a day folder is safe: the loop treats it as a fresh start for that day.
