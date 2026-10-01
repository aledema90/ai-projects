# Step 3, lane H: Hygiene

**Goal:** find tickets that break the hygiene rules and propose the exact fix. Read-only: you propose,
step 4 applies after approval.

## Input

Step 1 `backlog` items, approved step 2 output, `context/backlog-rules.md` (read it: rule ids, labels,
required fields, template phrases), customer material in `context/customers/` (optional context).

## Do

1. Apply each rule `HY#` in `backlog-rules.md` to every in-scope backlog item. An item can break several.
2. For each violation, propose a concrete fix:
   - missing label: the exact label string from the taxonomy (never invent one)
   - missing assignee/milestone: name the value only if the data gives it; otherwise `[ask user]`
   - empty/template description: write a draft description in the project's template, built ONLY from
     the ticket's title, existing text, linked sources and customer material. Mark gaps `[to define]`.
   - blocked, shipped-but-open, stale: the fix is a question for the user, not a change
     (`ask: unblock decision?`, `ask: close?`).
3. Order the actions so tickets from step 2 flagged UNDER-PRIORITIZED come first among those that break
   a rule.
4. Tickets flagged IMMINENT in step 2 (for example an overdue due date) that break no `HY#` rule are
   NOT actions: gate A rule H-1 requires every numbered action to cite an `HY#` rule. List them on
   ONE line right after the `note:` line, in the form
   `FYI from step 2 (no HY rule, not an action): <id> <due date> <overdue|imminent>, <status>; ... ask: is the due date still valid?`
   They are not counted in `with violations` or `proposed fixes`.

## Output format (exactly)

```
HYGIENE
note: <limits, for example rules that could not be assessed>
FYI from step 2 (no HY rule, not an action): <only if step 2 flagged IMMINENT items with no HY violation>
H1 | <ticket id> | <url> | rules: HY2, HY7
   fix: add label `<x>`; description draft below
   description draft:
   <markdown, only if HY7>
H2 | ...
SUMMARY
in scope: N | with violations: N | proposed fixes: N | questions for user: N
```

Number actions `H1..Hn`; one action per ticket (several field changes in one action).
