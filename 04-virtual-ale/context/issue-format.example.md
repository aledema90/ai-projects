# Issue format: logging changes in existing issues

`/setup` copies this file to `context/issue-format.md` (git-ignored). Step 2 drafts every update to an
existing issue against it; step 2's checker fails drafts that break it. The structure of NEW issues is
`context/template.md`.

## Rules

- **Append only.** Never rewrite, reorder or delete existing description text.
- Change-log section: `## Change Log` (set it to the heading your `context/template.md` uses).
- If the description has the change-log section, add one line per change at the end of that section:

  ```
  YYYY-MM-DD: <what changed or was asked, in plain English> ([source](<url>), <who>)
  ```

- Otherwise add one section at the end of the description, or extend it if it already exists for the
  same date:

  ```
  ### Update YYYY-MM-DD
  - <one line per request: what changed or was asked, in plain English>
    ([source](<url>) · <who> · <date>)
  ```

- One line per request. Several sources for the same request go on the same line.
- Commits and merge requests are linked by short sha or `!iid`; chats and meetings by their url.
- No opinions, no estimates, no assignments: only what the sources say.
