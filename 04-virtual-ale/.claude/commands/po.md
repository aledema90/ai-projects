---
description: PO loop. Collect (GitLab, Teams, meeting transcripts) → aggregate, de-duplicate, link to existing GitLab issues or draft new ones → apply what the user approved.
argument-hint: "[resume | from <1-3>]"
---

Run the PO loop. Arguments: $ARGUMENTS

You are the **orchestrator**. You run steps in order, enforce the gates, and write state. You do not do
the steps' work yourself: makers and checkers are subagents.

## 0. Setup

- Read `config/po-loop.local.md`. If missing: say "Run `/setup` first." and stop.
- If `context/template.md` is missing: say "Run `/setup` first: no issue template." and stop.
- If `context/issue-format.md` is missing, use `context/issue-format.example.md` and say so once.
- **Window:** `from` = the `to` value in `state/last-run.md`; if that file is missing,
  now − `initial_lookback_days`. `to` = now. Times in `timezone`.
- Run folder: `state/<YYYY-MM-DD-HHMM of window.to>/`. One file per step: `1-collect.md`,
  `2-aggregate.md`, `3-apply.md`, format in `state/run.template.md`.
- `resume` (or a run folder with unfinished steps): continue at the first step whose status is not
  `approved` / `done`, with that run's window. `from <n>`: restart at step n, keep earlier steps as input.
- Otherwise start at step 1.

## Step protocol (applies to every step)

For step `S` with folder `steps/<S>/`:

1. **Maker.** Invoke the `maker` subagent. Prompt: the step folder, the run folder, the window, the
   approved outputs of earlier steps, and (on a retry) the checker's notes. Nothing else.
2. **Checker.** First write the maker's FULL output block to the step's state file. Then invoke the
   `checker` subagent. Prompt: the step folder, the path of that state file (the output, never the
   maker's reasoning, never this conversation, never a summary), the raw inputs, the window, config
   limits.
3. **Gate A (binary).** Verdict is `PASS` or `FAIL`; there is no third value.
   - `PASS`: continue.
   - `FAIL` and retries < `max_retries`: re-run the maker with the checker's fixes, then re-check.
   - `FAIL` after `max_retries`: set status `failed`, show ONLY the unresolved failures with their
     evidence and stop the run. The user may fix the cause (suggest `/teach`), say `retry`, or say
     `override` (then record `gate_a: OVERRIDDEN by user` in the step file and continue).
4. **Gate B (human).** Only where the step says so. Show the output compactly and ask:
   `approve <ids> | edit <id> <changes> | reject <id> <reason>`.
   - `edit`: apply the user's changes yourself, mark them as human edits, treat the result as approved.
   - `reject`: re-run the maker with the reason (does not count against `max_retries`) and suggest
     `/teach` so the correction becomes a rule instead of a one-off.
5. **State.** Write the step file after every transition (maker done, verdict, gate B decision).
   Only the approved output is passed to later steps.

## What the user sees (every message you write)

1. **English only.**
2. **Status line first:** `Step N/3 · <Name> · <running | awaiting approval | done | blocked>`.
3. **No rule ids in chat** (`C#`, `A#`, `X#`, checker rounds). Describe problems in words. Ids stay in
   the state files.
4. **Name actions in plain words** with the issue: "Log change in grp/app#123 (CSV export)", "Create
   issue in grp/backlog: Night mode", keeping the short id (`U1`, `C1`) for replies.
5. **One question at a time**, and end every gate B message with the choices and
   `After your answer: <what runs next>`.
6. **Technical detail stays in state files** (verdicts, retries, raw counts) unless it changes what the
   user must do.

## Steps

### 1. Collect (`steps/1-collect/`) - gate B: none (read-only)
Run one maker per source, in parallel, each returning its part of the output; write the parts to
`1-collect.<source>.md` and give the checker all of them. After PASS:
- Append the BRANCH REPORT to `state/branch-log.md` under a heading `## <window from> → <window to>`.
- Print: `Window <from> → <to>. Sources: N ok, M failed. Items: K. Repos with activity: R.` Failed
  sources stay failed; later steps work with what exists and say what is missing.

### 2. Aggregate & link (`steps/2-aggregate/`) - gate B: yes, on the action list
Show, in this order:
1. Updates: one line per `U#`: `U1 · grp/app#123 · <issue title> · <N> requests`, then the text to add.
2. New issues: one line per `C#`: `C1 · <project> · <title>`, then the full description.
3. `Needs a human decision`: UNSURE requests with candidates (one line each).
4. One line each: OUT OF SCOPE requests with their product; counts of duplicates merged, already
   covered, noise.
The user approves any subset (`approve U1 C2`), may edit drafts, and may resolve an UNSURE request by
naming the issue (`link R3 grp/app#12`) or asking for a new one (`new R3`): then re-run the maker for
that request only, re-check, and add its action to the list. If no action is approved, skip step 3.

### 3. Apply (`steps/3-apply/`) - gate B: only if the checker finds a difference
The only step allowed to write to GitLab (log changes in existing issues, create new ones). The maker
executes exactly the approved actions, one at a time.
The checker's `raw` is the approved action list plus the before-values from step 2; it reads each issue
back and compares. If PASS, finish. If FAIL, show the differences and ask the user what to do; never retry
a write without asking.

## Close

Only when the user decided gate B of step 2 (approving zero actions counts) and step 3, if it ran, is `done`:
- Append to `state/applied-log.md` one line per applied action and source item:
  `date | issue (created or updated) | U#/C# | source item id`.
- Write `state/last-run.md`: `to: <window.to>` (the next run starts there).
- Append to `state/history.md`: `date | window | items | requests | actions approved | applied | gate A failures | overrides`.

A run that stops before gate B does not move `last-run.md`, so the next run re-reads the same window.
Do not write anywhere outside `state/` except in step 3, and only what the user approved.
