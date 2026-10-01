---
description: Turn a correction into a permanent edit of the right loop file instead of fixing it in chat.
argument-hint: "<what was wrong / what you want instead>"
---

Correction from the user: $ARGUMENTS

Do not just adjust today's answer. Make the correction compound.

1. Pick the single file the correction belongs in:
   - what a step does or how its output looks -> `steps/<n>-<name>/instructions.md` (or the lane file)
   - a pass/fail rule -> `steps/<n>-<name>/rubric.md`
   - goals, non-goals, tie-breakers -> `context/strategy.md`
   - ticket labels, hygiene rules -> `context/backlog-rules.md`
   - how a system is read -> `sources/<name>.md`
   - limits, paths, exclusions -> `config/morning-loop.local.md`
   - how every maker or checker behaves -> `.claude/agents/maker.md` / `checker.md`
2. Draft the smallest precise edit and show it as before/after. Prefer a testable rule ("a ticket with
   no `priority` label and due within 3 days fails A3") over a preference ("be more careful").
3. Apply it only after the user says yes.
4. Append to `state/feedback-log.md`: `date | file changed | correction in one line`.
5. Offer to re-run the affected step (`/morning from <n>`) to confirm.
