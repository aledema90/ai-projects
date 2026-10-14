# Source: gitlab

**Purpose:** what changed on every branch of every project in the configured groups in the window, and
which issues it touches.

## Requires

- A connected GitLab tool with read access (list group projects, list branches, list commits, list
  merge requests).
- Config keys: `gitlab_groups`, `gitlab_ignore_branches`, `gitlab_ignore_authors`.

If the tool is not connected: `SOURCE_FAILED: gitlab tool not available`. If one group or project fails,
mark it failed and continue with the others.

## How to fetch (read-only)

1. For EACH group in `gitlab_groups`: list its projects including subgroups, not archived, ordered by
   last activity (newest first). Keep projects whose last activity is inside the window; stop paging at
   the first older one.
2. For each kept project:
   1. List branches. Keep branches whose last commit is inside the window and that do not match
      `gitlab_ignore_branches`.
   2. For each kept branch, list commits inside the window (paginate). Drop commits by
      `gitlab_ignore_authors` and merge commits that only merge another branch (count them as dropped).
      A commit present on several branches is listed once, on the first branch it was found, with the
      other branches in `fields: also_on`.
   3. List merge requests created, updated or merged inside the window.
3. Extract issue references, keep them in `refs` as `<project>#<iid>`:
   - branch name starting with a number (`123-fix-login` → `<project>#123`),
   - `#123` or `<group/project>#123` or a full issue url in commit messages,
   - `Closes|Fixes|Resolves|Related to #123` in merge request title or description.
4. Map to the common format:
   - commits: `id: gitlab:<project>@<short sha>`, `type: commit`, `title`: first line of the message,
     `fields`: `group`, `branch`, `also_on`
   - merge requests: `id: gitlab:<project>!<iid>`, `type: merge-request`,
     `fields`: `group`, `source_branch`, `target_branch`, `state` (opened | merged | closed), `draft`
   - `signals`: `change` always; `bug` if the message says fix/bug/hotfix

## Branch change report

After the items, write a report per group, then per project, then per branch:

```
BRANCH REPORT <window from> → <window to>
<group>
  <project>
    <branch> | commits: N | authors: a, b | MRs: !12 (merged → main) | issues: #123, #456
      - <short sha> <first line of message> (<author>, <date>)
  (no activity)                          # when a group had no project with activity
```

## Output

Per group: `projects_scanned: N, projects_active: P`; per active project: `branches_kept: K,
commits_kept: C, commits_dropped: D, mrs: M`. Then the items, then the branch report.
