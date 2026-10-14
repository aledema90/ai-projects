# Virtual Ale: PO loop

A product-owner loop run with [Claude Code](https://claude.com/claude-code). On demand it reads what
changed since the last run (GitLab branches across the configured groups, Teams chats and channels,
meeting transcripts), merges duplicates, and for every request either logs the change
in an existing GitLab issue or drafts a new issue from `context/template.md`. Nothing is written to
GitLab until a human approves it.

Everything that defines behaviour is a Markdown file. There is no application code. Same pattern as
[`03-pm-morning-loop`](../03-pm-morning-loop): every step has an instruction file, a maker, a checker,
a binary gate A, a human gate B and a state file.

## How it works

```
/setup (once)            /po
   │                       │
   ▼                       ▼
[0 SETUP] ─────► [1 COLLECT] ──A──► [2 AGGREGATE & LINK] ──A──B──► [3 APPLY] ──A──(B if different)
connectors,       GitLab groups ·     cluster duplicates ·            logs changes in
auth check,       Teams · meetings    skip already-handled ·          existing issues,
groups/channels,  (read-only,         existing issue → update draft   creates new ones,
template          since last run)     no issue → new-issue draft      one at a time
                       │                                                  │
                       └──► state/branch-log.md        state/applied-log.md ◄┘
A = checker, binary pass/fail      B = you approve, edit or reject
```

| Layer | Maker does | Gate A checks | Gate B |
| --- | --- | --- | --- |
| 0 Setup | Checks GitLab and Microsoft 365 connectors, picks groups and where new issues go, channels, chats, the issue template; verifies transcript access; writes local config | (interactive) | operator answers |
| 1 Collect | Branch activity, commits, MRs and issue refs for every active project of the groups; actionable Teams messages; product points from meeting transcripts. Writes the branch change report | every source accounted for, counts match, window respected, no invented items, refs real | none (read-only) |
| 2 Aggregate & link | Merges items about the same request, drops what was already applied, searches the whole group: existing issue → change-log draft, no issue → new issue drafted from the template; other products → out of scope | partition complete, merges, groups and links have evidence, NEW really has no issue, no duplicates, drafts grounded and in format | yes, per action |
| 3 Apply | Logs the approved text in each existing issue; creates each approved new issue | re-reads each issue: approved content present, nothing else changed, no duplicate created | only if different |

## Commands

| Command | What it does |
| --- | --- |
| `/setup` | Layer 0. Checks connectors and auth, picks scope, writes `config/po-loop.local.md`. Re-run any time |
| `/po` | Runs layers 1-3 with their gates. `/po resume`, `/po from <n>` |
| `/teach <correction>` | Turns a correction into an edit of the right file |

## Handover quick start (for the next operator)

No terminal needed.

1. Connect **GitLab** and **Microsoft 365** at claude.ai → Customize → Connectors, signed in as yourself.
2. Open the Claude desktop app → **Code** tab → new session → choose this folder.
3. Say "set me up" (or `/setup`) and answer its questions: groups, where new issues go, Teams channels,
   chats, the meeting recorder, meetings to skip, the issue template if `context/template.md` is missing.
4. Whenever you want an update, say "run the PO loop" or "what changed this week?" (or `/po`). Approve,
   edit or reject the proposed changes and new issues when it asks. Nothing reaches GitLab before that.
5. To correct the loop, say what was wrong ("that message is personal, skip chats like that"); it becomes
   a permanent rule through `/teach`.
6. Optional: ask "run the PO loop every Monday at 9:00" to schedule it. The computer and the app must be
   on at that time; the run still waits for your approval.

New issues follow `context/template.md`. Changes to existing issues are logged as dated lines in their
change-log section (see `context/issue-format.md`); existing text is never rewritten.

## Safety model

- `/setup` and layers 1-2 are read-only; the only writes are local files (`config/`, `context/`, `state/`).
- Layer 3 writes only the approved content (change logs and new issues), one action at a time, and never
  retries a write.
- Gate A is binary. A step that cannot pass is reported with its failures, not shown as a result.
- The checker never sees the maker's reasoning.
- Content of issues, commits, chats and transcripts is data, never instructions.
- No secrets in files: auth lives in the connectors. Private files are git-ignored.
- `.claude/settings.json` asks before any file write outside `state/` and any shell command.

## Known limits

- Started by the operator, by asking in chat or on a schedule set up from the app.
- The meeting recorder only mails attendees: the loop sees the meetings the operator was in.
- Requests about products outside the configured groups are listed as `OUT OF SCOPE`, with no action.
- Teams search lags on wide windows; the source reads one-day slices.
- A 7-day first run took about an hour (most of it Teams and meeting transcripts). Later runs cover only the days since
  the last run.

## Layout

```
.claude/commands/   /setup /po /teach
.claude/agents/     maker, checker (generic)
steps/              1-collect, 2-aggregate, 3-apply: instructions + rubric
sources/            gitlab, teams, meetings + contract
config/             settings (/setup writes *.local.md)
context/            template (new issues), issue-format (change logs); *.example.md are generic
state/              per-run step files, logs (git-ignored)
```

## License

MIT
