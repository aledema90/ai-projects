---
description: Layer 0. Checks connectors and authentication, picks repos, chats and channels, writes the local config. Safe to re-run.
---

Set up the PO loop for the person running this session (the **operator**). Arguments: $ARGUMENTS

You do this yourself, in the conversation (not through a subagent): it needs the operator's answers.
Everything here is **read-only** except writing the two local files in step 5. Never ask for, print or
store a token, key or password: authentication lives in the MCP connectors.

Start every message with `Setup · <stage> · <running | needs you | done | blocked>`.

## 1. Connectors

Two connectors are required. For each, find its tools (search the available or deferred tools by the
keywords given) and call one read-only identity tool:

| Connector | Keywords to find it | Identity check | Used by |
| --- | --- | --- | --- |
| GitLab | `gitlab`, `whoami`, `list_projects` | `whoami` (or get current user) | gitlab source, steps 2-3 |
| Microsoft 365 | `outlook_email_search`, `teams`, `sharepoint_search`, `get_me` | `get_me` (or get current user) | teams, meetings |

- Tool missing → the connector is not installed. Tell the operator: "Connect <name> at claude.ai →
  Customize → Connectors (or run `/mcp` in a terminal session), then re-run `/setup`." Use
  `.mcp.json.example` only if they run their own MCP servers.
- Tool present but the call fails with an auth error → same message, "re-authenticate".
- Show who each connector is signed in as. Ask the operator to confirm it is **their own** account. Stop
  here until both connectors pass.

## 2. GitLab scope

1. If `config/po-loop.local.md` exists, read it and show the current `gitlab_groups`; ask keep / change.
2. Otherwise ask for the GitLab groups to cover and, for each, the product names that belong to it
   (`products`). Every project in these groups is read, and issues are searched across the whole group.
3. For each group, show its 5 projects with the most open issues and ask which one receives NEW issues
   (`new_issue_project`).
4. Ask for branch patterns and bot authors to ignore (suggest `renovate/*`, `dependabot/*` if such
   branches exist).
5. For each group, check you can list its projects and search its issues, and that each
   `new_issue_project` exists. Mark ✓ / ✗.

## 3. Teams scope

1. List the operator's joined teams and their channels, numbered. The operator picks channels to read.
   If listing teams is refused (some tenants do not grant the connector `Team.ReadBasic.All`), ask the
   operator to paste each channel's link (channel `...` → **Copy link**). Take the team id from the
   `groupId=` parameter and the channel id from the path segment `19:...@thread.tacv2` (url-decode it),
   then list that team's channels to confirm the name. Reading channel messages needs only the ids.
2. Ask: all 1:1, group and meeting chats, or only some (list recent chats if they want to pick)? Any chat to
   exclude?
3. Read one recent message from one chosen channel and one chat to confirm access. Mark ✓ / ✗. If channel
   reading fails, say so: the loop then reads chats only.

## 4. Meeting transcripts

Ask for the meeting recorder's sender address, the subject prefix and the transcript link text (keys
`meetings_*`). Search Outlook for emails from that sender in the last 14 days (one page). Report the
count and the three most recent meeting names. If one exists, resolve and read its transcript once (see
`sources/meetings.md`) to confirm SharePoint access. Zero results is a warning, not a failure: the
recorder only mails attendees, so the operator may not be on those meetings yet. Ask which meeting names
to exclude.

## 5. Write local files

1. Build `config/po-loop.local.md` from `config/po-loop.example.md` with the answers. Show the diff of
   changed keys (not the whole file) and write it after the operator says yes.
2. If `context/issue-format.md` does not exist, copy `context/issue-format.example.md` to it.
3. **Issue template.** If `context/template.md` does not exist, ask the operator for the template every
   NEW issue must follow: a file path to copy, the text pasted in chat, or `context/template.example.md`
   as a starting point. Write it to
   `context/template.md` after they confirm. If it exists, show its headings and ask keep / replace.
   The loop cannot create issues without it.
4. Never touch `state/`.

## 6. Checklist

```
Setup · Checklist · done
✓ GitLab      signed in as <user> · groups: <paths> · new issues → <projects>
✓ Teams       <N> channels · chats: <all | N> · <excluded>
✓ Meetings    <N> summaries in the last 14 days · transcript read ✓
✓ Template    context/template.md · <N> sections
Next: /po
```

Use ✗ with the reason for anything that failed, and do not suggest `/po` while a required connector is ✗.
