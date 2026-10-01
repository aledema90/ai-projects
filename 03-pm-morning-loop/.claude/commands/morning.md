---
description: Morning loop. Runs 4 steps (collect, align, propose, apply), each with maker, checker, gate A and gate B.
argument-hint: "[resume | from <1-4>]"
---

Run the morning loop. Arguments: $ARGUMENTS

You are the **orchestrator**. You run steps in order, enforce the gates, and write state. You do not
do the steps' work yourself: makers and checkers are subagents.

## 0. Setup

- Read `config/morning-loop.local.md` (if missing: say so, point to the `.example`, stop).
- Read `context/strategy.md` (if missing, use `context/strategy.example.md` and warn once: steps 2-3
  will fail their strategy rules, so tell the user to write a real one).
- Run folder: `state/<today YYYY-MM-DD>/`. One file per step: `1-collect.md`, `2-align.md`,
  `3-propose.md`, `4-apply.md`, format in `state/run.template.md`.
- `resume` (or an existing run folder with unfinished steps): continue at the first step whose status
  is not `approved` / `done`. `from <n>`: restart at step n, keep earlier steps as input.
- Otherwise start at step 1.

## Step protocol (applies to every step)

For step `S` with folder `steps/<S>/`:

1. **Maker.** Invoke the `maker` subagent. Prompt: the step folder, the run folder, the approved
   outputs of earlier steps, the strategy path, and (on a retry) the checker's notes. Nothing else.
2. **Checker.** Invoke the `checker` subagent. Prompt: the step folder, the maker's output block ONLY
   (never its reasoning, never this conversation), the raw inputs, the strategy path, config limits.
3. **Gate A (binary).** Verdict is `PASS` or `FAIL`; there is no third value.
   - `PASS`: continue.
   - `FAIL` and retries < `max_retries`: re-run the maker with the checker's fixes, then re-check.
   - `FAIL` after `max_retries`: set status `failed`, show ONLY the unresolved failures with their
     evidence (not the maker's output as if it were a result) and stop the run. The user may:
     fix the cause (suggest `/teach`), say `retry`, or say `override` (then record
     `gate_a: OVERRIDDEN by user` in the step file and continue).
4. **Gate B (human).** Only where the step says so. Show the output compactly and ask:
   `approve | edit <changes> | reject <reason>`.
   - `edit`: apply the user's changes yourself, mark them as human edits, treat the result as approved.
   - `reject`: re-run the maker with the reason (does not count against `max_retries`) and suggest
     `/teach` so the correction becomes a rule instead of a one-off.
5. **State.** Write the step file after every transition (maker done, verdict, gate B decision).
   Only the approved output is passed to later steps.

## What the user sees (applies to every message you write)

1. **Start every message with a status line:** `Step N/4 · <Name> · <state>`, where state is one of
   `in corso`, `da approvare`, `fatto`, `bloccato`. Example: `Step 2/4 · Align · da approvare`.
2. **No rule ids in chat.** Never show `HY#`, `C#`, `A#`, `H-#`, `P-#`, `X-#` or checker round numbers.
   Describe the problem in words ("manca il team", "descrizione vuota"). Those ids stay in the state files.
3. **Name actions in plain words**, with the ticket: "Aggiungere il team a #1798", not "H1". You may keep a
   short number for the user to reply with (`approve 1 3`), shown next to the plain name.
4. **Ask one thing at a time, and say what happens next:** end every gate B message with the choices and
   a line `Dopo la tua risposta: <what runs next>`.
5. **Keep technical detail in the state files**, not in chat: checker verdicts, retries, raw counts. Mention a
   retry or a failure only if it changes what the user must do.
6. Goals and to-dos are named in words as well ("obiettivo Popcons", "to-do: Risposta a Dhairya"), never by
   `G1`/`L21`.

## Steps

### 1. Collect (`steps/1-collect/`) - gate B: none (read-only)
Sources listed in config, each per `sources/<name>.md`. Run the four source reads in parallel inside
one maker call. After PASS, print one line: `Sources: N ok, M failed. Items: K.` Failed sources stay
failed in the output; later steps work with what exists and say what is missing.

### 2. Align (`steps/2-align/`) - gate B: yes
Output: alignment of backlog vs strategy, and the coverage matrix. The user may correct (for example
"that to-do is personal, no ticket").

### 3. Propose (`steps/3-propose/`) - gate B: yes, on the action list
Three lanes run in parallel, each with its own maker, checker and gate A:
`hygiene.md`, `prep.md`, `tickets.md`. A lane that fails gate A is shown as failed; the other lanes
continue. One gate B shows all passed lanes as a numbered action list (`H1..`, `P1..`, `T1..`);
the user approves any subset (for example `approve H1 H3 T2`). Only approved actions move on.

After gate B, assemble the **Today brief** yourself (no maker or checker: it only recombines
approved content): deadlines due today or within `imminent_days`, today's meetings with their prep
note, then the approved actions. Deadlines first.

### 4. Apply (`steps/4-apply/`) - gate B: only if the checker finds a difference
The only step allowed to write to a tracker. The maker executes exactly the approved actions, one at a
time. The checker's `raw` is the approved action list plus the step 1 backlog items (the
before-values); it reads back from the tracker and compares with what was approved. If PASS, finish.
If FAIL, show the differences and ask the user what to do; never retry a write without asking.
Skip this step if nothing was approved.

## Close

- Append to `state/history.md`: `date | steps done | gate A failures | overrides | actions applied`.
- Do not write anywhere outside `state/` except in step 4, and only what the user approved.
