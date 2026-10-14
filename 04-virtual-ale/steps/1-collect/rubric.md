# Rubric: Step 1 Collect

All rules are blocking. Verify against `raw` (the tool responses the maker used), not against how complete
the output looks.

- **C1 Every source accounted for.** Each source in the config appears under SOURCES as OK, PARTIAL or
  FAILED with a reason. Each group in `gitlab_groups` and each entry in `teams_channels` is either
  covered or named as failed.
- **C2 Counts match.** For every source, the kept counts equal the number of items listed for it, and the
  scanned counts equal what the raw tool responses contained. For `teams`, re-run the search for the
  newest 2 hours of the window and one other 2-hour slice: every chat message returned is classified.
  For `gitlab`, re-list each group's projects by last activity: every project active in the window is
  covered.
- **C3 Window respected.** Every item's `when` is inside the window. No item from outside it.
- **C4 Item shape.** Every item has `id`, `source`, `title`, `url`, `type`, `when`, `who`, `summary`,
  `repo`, `refs`. Unknown values are written `none`, `[]` or `[unknown]`, never left out.
- **C5 No fabrication.** Pick any 3 items per source and confirm they exist in the raw data with the same
  id, author and date (for `meetings`, the quote appears in the transcript). Any miss fails the rule.
- **C6 Refs real.** Every `refs` entry appears literally in the item's raw text (branch name, message,
  MR description, chat message or transcript).
- **C7 Filters applied.** `teams` and `meetings` state scanned vs kept counts; each kept item has a quote of
  at most 2 lines and at least one signal. Ignored branches and authors from config are absent.
- **C8 Branch report consistent.** Every commit and MR item appears in the branch report under its
  project and branch, and the report lists nothing that is not an item.
- **C9 English.** Titles and summaries are in English (quotes may keep their language).
