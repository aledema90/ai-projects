# Step 2: Aggregate & link (layer 2)

**Goal:** turn the collected items into a short list of distinct requests. Each request either updates
an existing GitLab issue (log the change in its description) or creates a new issue from the template.

**Gate B:** yes, on the action list.

## Input

Approved output of step 1, `state/applied-log.md` (may be missing on the first run),
`context/template.md`, `context/issue-format.md`, config (`gitlab_groups`).

## Do

### 1. Cluster

Group items that describe the **same** request or change into one request `R#`. Merge only on explicit
evidence: the same issue ref, the same branch or MR, or the same feature named in both items (state the
shared words). Similar topic is not enough; when in doubt keep them apart. Every item belongs to exactly
one request. Items with no product content left after reading are `NOISE` with a reason.

### 2. Pick the group

Each request belongs to one group in `gitlab_groups`, by evidence: a ref or branch in a project of that
group, or a product the request names that is listed in the group's `products`. A request about a
product outside every configured group is `OUT OF SCOPE` (state the product). If the group is unclear, the request is `UNSURE`.

### 3. Find the issue

- Explicit: every issue in the request's `refs`.
- Search: open issues **anywhere in the request's group** (group-level issue search), by the request's
  keywords (at least two searches with different keywords). Read each candidate's title, state and
  description.

### 4. Verdict

For each request, one verdict:
- `LINKED <project>#<iid>`: an explicit ref to an open issue, or a candidate whose title or description
  names the same feature (state the matching words). → update action.
- `NEW <new_issue_project>`: no open issue in the group names the same feature (state the searches).
  → create action, in the group's `new_issue_project`.
- `UNSURE`: two or more plausible candidates, a weak match, or an unclear group. List the candidates with
  the reason. No action until the user decides.
- `ALREADY COVERED`: `state/applied-log.md` already has the same source item id, or the linked issue's
  current description already states the same thing (quote the line). No action.
- `OUT OF SCOPE`: the product is in no configured group. No action.
- A ref to a closed issue is reported as `LINKED (closed)` and gets no update.

### 5. Draft actions

- **Update `U#`**, one per open linked issue with at least one request left: the exact text to add,
  following `context/issue-format.md`. Several requests on the same issue go in the same action.
- **Create `C#`**, one per `NEW` request: a title (short, user-facing, English) and a description that
  follows `context/template.md` exactly: every heading, in the same order, nothing added or removed.
  Fill each section only with what the sources say. A section with no source content keeps the
  template's placeholder value (for example `n/a`), or `[to define]` when the template has none. Put the
  source links (url, who, date) under the template's resources section. The first line of the
  change-log section (named in `context/issue-format.md`) is `<today>: Created by the PO loop from
  <sources>`. No labels unless the template says so.

Write only what the sources say.

## Output format (exactly)

```
REQUESTS
| req | items | summary (English, one line) | verdict | issue / reason |
| R1 | teams:abc, meetings:x#3 | Add CSV export to report page | LINKED | grp/app#123 (title: "CSV export") |
| R2 | teams:def | Night mode for the lights | NEW | grp/backlog (searched "night mode", "brightness") |
| R3 | teams:ghi | ... | UNSURE | grp/app#12 or #40: both mention "onboarding" |
| R4 | meetings:y#1 | ... | OUT OF SCOPE | <product>, in no configured group |
| R5 | teams:jkl | ... | ALREADY COVERED | grp/app#123 description: "<line>" |
| -- | teams:mno | | NOISE | scheduling only |

ACTIONS
U1 | update description | grp/app#123 | requests: R1 | <issue url>
---
<exact text to add, and where (change-log section or end of description)>
---
C1 | create issue | grp/backlog | requests: R2
title: <title>
---
<exact description, following context/template.md>
---

COUNTS
items: N | requests: N | linked: N | new: N | unsure: N | already covered: N | out of scope: N | noise: N | actions: U N, C N
```
