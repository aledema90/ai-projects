# Morning Loop config

Copy this file to `config/morning-loop.local.md` (git-ignored) and fill it in.
Keep the key names; commands, sources and steps read them by name.

## General

- max_retries: 2              # maker/checker rounds before a step is reported as failed
- imminent_days: 3            # "imminent" deadline window
- language: en                # language of the output; drafts keep the language of their source

## Sources (in order)

- backlog
- notes
- teams
- calendar

## Source settings

### backlog

- backlog_project: "<project or group path in your backlog tool>"
- backlog_types: ["issue"]
- backlog_exclude_labels: []           # items with any of these labels are out of scope
- rules_file: context/backlog-rules.md

### notes

- vault_path: "/path/to/your/vault"
- todo_file: "Todo.md"                 # relative to vault_path
- meetings_folder: "Meetings"          # used as customer/meeting context in step 3

### teams

- chat_lookback: yesterday             # fixed by design; do not widen
- chat_exclude: []                     # chat names to ignore

### calendar

- prep_exclude: ["Focus", "Lunch", "OOO"]   # event titles that never get a prep note

## Customer material (step 3)

- customers_dir: context/customers     # transcripts, digests, notes about customers. Optional.
