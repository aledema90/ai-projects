# Rubric: Step 1 Collect

All rules are blocking. Verify against `raw` (the tool responses and files the maker used), not against
how complete the output looks.

- **C1 Every source accounted for.** Each source in the config appears under SOURCES as OK or FAILED
  with a reason. None missing, none silently skipped.
- **C2 Counts match.** For every OK source, `count_fetched` (or `count_kept`) equals the number of items
  listed for it, and `count_fetched`/`count_scanned` equals what the raw tool response contained.
- **C3 Windows respected.** Every `teams` item was sent yesterday (Friday to Sunday on a Monday). Every
  `calendar` item starts today. Every `backlog` item is open. Every `notes` item is an unchecked
  to-do, or a checked one completed in the last 3 days marked `done`.
- **C4 Item shape.** Every item has `id`, `source`, `title`, `url`, `type`, `updated`, `due`. Unknown
  values are written `none` or `[unknown]`, never left out.
- **C5 Backlog fields.** Every `backlog` item states `priority`, `due`, `labels`, `project`,
  `description_status` (value `none` when absent). For a project whose `rules_file` is `none` in the
  config, `description_status` may be `not-assessed`.
- **C6 No fabrication.** Pick any 3 items per source and confirm they exist in the raw data with the same
  id, title and date. Any miss fails the rule.
- **C7 Chat filter applied.** `teams` output states scanned vs kept counts, and each kept item has a
  quote of at most 2 lines and at least one signal (`mentioned-me`, `asks-me`, `has-deadline`).
