# state/

This folder is the loop's memory. Everything here except this file and the
template is git-ignored, so your data never ends up in the public repository.

| File | Written by | Purpose |
| --- | --- | --- |
| `last-run.md` | `/morning` | Yesterday's priorities and which items were already surfaced, so the loop does not repeat itself. |
| `history.md` | `/morning` | One line per run: date, verdict, retries, sources that worked. Used by `/loop-health`. |
| `feedback-log.md` | `/teach` | Every correction you made and which file it changed. Used by `/loop-health`. |

The files are created automatically on the first run. To see the expected format
of `last-run.md`, open `last-run.template.md`.

Deleting a file here is safe: the loop treats it as a fresh start.
