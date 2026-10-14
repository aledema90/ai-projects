# PO loop config

`/setup` copies this file to `config/po-loop.local.md` (git-ignored) and fills it in. You can also edit
it by hand. Keep the key names; commands, sources and steps read them by name.

## General

- max_retries: 2                 # maker/checker rounds before a step is reported as failed
- initial_lookback_days: 7       # window for the first run; later runs start at state/last-run.md
- timezone: Europe/Rome          # used for windows and dates shown to the user

## Sources (in order)

- gitlab
- teams
- meetings

## Source settings

### gitlab

- gitlab_groups:                 # every project in these groups (and subgroups) is read; issues are searched here
  - path: "<group/path>"
    products: ["<product name>", "<alias>"]       # names that place a request in this group
    new_issue_project: "<group/path/project>"     # where NEW issues for this group are created
- gitlab_ignore_branches: []     # glob patterns, e.g. "renovate/*", "dependabot/*"
- gitlab_ignore_authors: []      # bot accounts whose commits are noise

### teams

- teams_chats: all               # `all` 1:1, group and meeting chats, or a list of chat names
- teams_chat_exclude: []         # chat names to ignore
- teams_channels:                # channel posts to read; one entry each
  - team: "<team name>"
    channel: "<channel name>"
    team_id: "<group id GUID>"           # from the channel link, `groupId=`
    channel_id: "<19:...@thread.tacv2>"

### meetings

- meetings_sender: "<recorder@your-company.com>"   # address the meeting recorder sends summaries from
- meetings_subject_prefix: "Meeting Summary: "
- meetings_link_text: "View Full Transcript"
- meetings_exclude: []           # meeting names to ignore (e.g. 1:1s, socials)

## Issues (step 2)

- issue_template_file: context/template.md     # structure of every NEW issue
- issue_format_file: context/issue-format.md   # how changes are logged in EXISTING issues
