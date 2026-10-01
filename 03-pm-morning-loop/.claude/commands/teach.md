---
description: Turn a correction into a permanent edit of the right loop file instead of fixing it in chat.
argument-hint: "<what was wrong / what you want instead>"
---

Correction from the user: $ARGUMENTS

Do not just adjust today's answer. Make the correction compound.

1. Decide which single file the correction belongs in:
   - a checking rule or threshold -> `context/rubric.md`
   - goals, non-goals, tie-breakers -> `context/strategy.md` (create from the example if missing)
   - how items are fetched or parsed -> `sources/<name>.md`
   - how ranking or output is written -> `.claude/agents/ranker.md`
   - how checking is done -> `.claude/agents/checker.md`
   - limits and paths -> `config/morning-loop.local.md`
2. Draft the smallest precise edit (show the diff as before/after text). Prefer a concrete,
   testable rule over a vague preference.
3. Ask the user to approve the edit. Apply it only after a yes.
4. Append to `state/feedback-log.md`: `date | file changed | correction in one line`.
5. Offer to re-run `/morning` to confirm the correction works.
