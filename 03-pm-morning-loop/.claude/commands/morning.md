---
description: Morning loop. Collect signals, propose today's priorities, verify them, show in chat.
---

Run the morning loop. Follow these steps in order. Be brief in your own narration.

## 0. Load context

- Read `config/morning-loop.local.md`. If missing, read `config/morning-loop.example.md`,
  warn that the user has not configured the loop, and stop.
- Read `context/strategy.md`. If missing, use `context/strategy.example.md` and warn
  once that the checker will be weak until a real strategy exists.
- Read `context/rubric.md`.
- Read `state/last-run.md` if it exists (else treat as a fresh start).

## 1. Collect signals

For each source listed in the config, follow `sources/<name>.md` and `sources/README.md`.
Run them in parallel when possible. Collect items in the common format.
If a source returns `SOURCE_FAILED`, record the reason and continue with the others.
If every source failed, report that and stop.

## 2. Rank (maker)

Invoke the `ranker` subagent. Pass in the prompt: all items, the strategy, `max_priorities`,
`daily_capacity`, and `last_run`. Nothing else.

## 3. Check

Invoke the `checker` subagent. Pass in the prompt: the ranker's output block only, all items,
the strategy, config limits, and `last_run`. Do NOT pass the ranker's reasoning or this
conversation.

## 4. Gate

- If `VERDICT: PASS`, continue.
- If `FAIL` and retries used < `max_retries`: invoke `ranker` again with the same input plus
  `checker_notes` (the checker's failures and fixes), then re-run step 3.
- If `FAIL` after `max_retries`: continue, but mark the result **UNVERIFIED** and show the
  unresolved failures.

## 5. Present

Show in chat, in this order:

1. **Today** - the priorities, each: title (linked), why today, first step, effort.
2. **Not today** - one line each.
3. **Loop health** - one line: sources ok/failed, checker verdict, retries, warnings.
4. Offer: "Tell me which to act on and I'll propose the exact action (`/apply`). If something
   looks wrong, use `/teach` instead of correcting me here."

## 6. Save state

Write only inside `state/`:

- `state/last-run.md` in the format of `state/last-run.template.md`. Carry over "Already
  surfaced" entries from the previous run for 7 days.
- Append one line to `state/history.md`: `date | verdict | retries | sources ok | sources failed`.

Do not write anywhere else.
