# Rubric: Step 3 Propose

One section per lane. The checker grades only the lane it is asked about. All rules are blocking.

## Lane H: Hygiene

- **H-1 Real violation.** Every proposed action cites rule ids `HY#` that exist in `backlog-rules.md`,
  and the ticket really breaks them in `raw`.
- **H-2 Complete.** Every in-scope backlog item that breaks a rule appears. Recompute the violation
  count from `raw`; it equals "with violations" in SUMMARY.
- **H-3 Concrete fix.** Each action states an exact change (label string, field, draft text) or an
  explicit `[ask user]` / `ask:` question. Advice like "improve the description" fails.
- **H-4 Valid labels.** Every proposed label string exists in the taxonomy of `backlog-rules.md`.
- **H-5 No invented facts.** Description drafts contain only facts found in the ticket, linked sources
  or customer files; unknowns are marked `[to define]`.
- **H-6 No scope creep.** No excluded-label item, and no ticket that does not exist in `raw`.

## Lane P: Meeting prep

- **P-1 One per meeting.** One block per non-excluded calendar event today; count equals the calendar's.
- **P-2 Calendar facts exact.** Time, title and attendees match the calendar item.
- **P-3 Cited.** Every statement under related, open to-dos, customer context carries a source id or
  file name that exists in `raw` or in `context/customers/`.
- **P-4 No unsupported customer claims.** Customer context either cites a file that contains the fact,
  or says `no customer material`.
- **P-5 Shape.** Each block has goal, related, open to-dos, customer context, bring/ask (1-3 items),
  and at most 15 lines.
- **P-6 Inference marked.** A goal not stated in the event is marked "inferred" or "unclear".

## Lane T: New tickets

- **T-1 One per UNCOVERED.** Exactly one draft for each qualifying UNCOVERED row of the approved step 2
  output. No extra drafts, none missing.
- **T-2 Not a duplicate.** Search `raw` backlog titles and descriptions; no existing ticket covers the
  draft.
- **T-3 Complete.** Title (max 80 chars), description in the template, 2-4 acceptance criteria,
  labels, source with quote of at most 2 lines.
- **T-4 Valid labels.** Labels exist in the taxonomy; team label is set only if implied, else
  `[ask user]`.
- **T-5 No invented requirements.** Every requirement and criterion traces to the source text;
  ambiguity is marked `[to define]`.
- **T-6 Customer evidence.** Either a file in `context/customers/` that contains the claim, or `none`.
- **T-7 Language.** Same language as the source item.
