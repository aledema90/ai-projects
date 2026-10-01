# Step 3, lane T: New tickets

**Goal:** draft a ticket for every item step 2 marked UNCOVERED and the user approved as needing one.
Read-only: you draft, step 4 creates after approval.

## Input

Approved step 2 output (COVERAGE rows with verdict UNCOVERED; ignore PERSONAL, COVERED; UNSURE only if
the user turned it into UNCOVERED at gate B), the source items they came from, `context/backlog-rules.md`
(template, labels, default labels), customer material in `context/customers/` (optional context).

## Do

For each UNCOVERED row, one draft:
1. **Title:** short, outcome-oriented, max 80 characters, same language as the source.
2. **Description:** use the "New ticket template" in `backlog-rules.md`. Context and Description come
   from the source text only. Expand wording, never requirements.
3. **Acceptance criteria:** 2-4 verifiable criteria that follow from the source. Where the source is
   ambiguous, write `[to define]`.
4. **Labels:** only strings from the taxonomy. Team label: set only if the data implies it, otherwise
   `[ask user]`.
5. **Source:** the original item id and a quote of at most 2 lines.
6. **Customer evidence:** cite the file in `context/customers/` if relevant, else `none`.
7. If one source item clearly holds several distinct topics, propose splitting and say so.

## Output format (exactly)

```
TICKETS
T1 | from <item id> | in <project>
   title: ...
   labels: ...
   description:
   <markdown>
   customer evidence: <file + one line> | none
T2 | ...
SUMMARY
drafts: N | needs user input: N
```

Number `T1..Tn`, one per UNCOVERED item. No extras.
