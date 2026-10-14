# Rubric: Step 2 Aggregate & link

All rules are blocking. `raw` is the approved step 1 output plus `state/applied-log.md`. Re-read issues
from GitLab (read-only) where a rule needs it.

- **A1 Complete partition.** Every step 1 item appears in exactly one request row or one `NOISE` row.
  Counts add up.
- **A2 Merges have evidence.** For every request with 2+ items, the shared ref, branch, MR or named
  feature is present in each merged item's raw text, and the items describe the same request.
- **A3 Group right.** Each request's group (from its issue or target project) is supported by a ref,
  branch or named product in its items. `OUT OF SCOPE` names a product that is in no configured group.
- **A4 Links real.** Every `LINKED` issue exists, is in a project of its group, and its state matches
  (open, or marked `closed`). For a non-explicit link, the stated matching words appear in the issue
  title or description.
- **A5 NEW is real.** For each `NEW`, search open issues of the group with the request's main keyword:
  no open issue clearly names the same feature. The target is the group's `new_issue_project`.
- **A6 No duplicates.** No action repeats a source item id already recorded in `applied-log.md` (for the
  same issue, or as an issue already created), and no update line repeats a line already in the issue's
  current description. Each `ALREADY COVERED` row quotes text that really exists. No two `C#` actions
  create the same feature.
- **A7 One action per issue.** No issue has more than one `U#`; no action targets a closed issue or an
  `UNSURE`, `OUT OF SCOPE` or `NOISE` request. Every `NEW` request has exactly one `C#`.
- **A8 Drafts grounded.** Every line of every `U#` and every filled section of every `C#` is supported by
  a source item of its requests, and states nothing absent from those items. Each `C#` lists its sources'
  urls.
- **A9 Format followed.** Every `U#` follows `context/issue-format.md` (append only, no edit to existing
  text). Every `C#` description has exactly the headings of `context/template.md`, in the same order.
- **A10 English.** Summaries, titles and drafts are in English (quotes may keep their language).
