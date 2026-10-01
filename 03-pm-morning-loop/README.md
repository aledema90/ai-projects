# Morning Loop

A daily loop for a product manager, run with [Claude Code](https://claude.com/claude-code).
Every morning it reads your backlog, to-do list, yesterday's chats and today's calendar, checks the
backlog against your strategy, proposes fixes and meeting prep, and writes to your tools only what you
approve.

Everything that defines behaviour is a Markdown file. There is no application code.

Inspired by the "loops for PMs" idea: every loop has a trigger, a skill file, a maker, a checker, a
gate and a state file. Here every step has all of them, plus a human gate.

## How it works

```
/morning
   │
   ▼
[1 COLLECT] ──A──► [2 ALIGN] ──A──B──► [3 PROPOSE] ──A──B──► [4 APPLY] ──A──(B if different)
 4 sources           backlog vs         hygiene · prep ·        writes only what
 (read-only)         strategy +         new tickets             you approved
                     coverage check     (3 parallel lanes)
   ▲                                                                │
   └──────────────── state/<date>/<step>.md ◄───────────────────────┘
A = checker, binary pass/fail      B = you approve, edit or reject
```

| Step | Maker does | Gate A checks | Gate B |
| --- | --- | --- | --- |
| 1 Collect | Reads backlog (open items, deadlines, priority labels), to-do list, yesterday's chat, today's calendar | every source accounted for, counts match, windows respected, no invented items | none (read-only) |
| 2 Align | Links each ticket to a goal in your strategy, flags mis-prioritised and imminent ones, maps every to-do and request to a ticket or `UNCOVERED` | references exist, flags have evidence, `UNCOVERED` really has no matching ticket | yes |
| 3 Propose | Lane H: hygiene fixes with draft text. Lane P: prep note per meeting. Lane T: ticket drafts for uncovered items. Uses customer material if present | each lane against its own rubric: cited, no invented facts, valid labels, no duplicates | yes, per action |
| 4 Apply | Executes the approved actions one at a time | re-reads each ticket and compares with what you approved | only if different |

After step 3 you get a **Today brief**: deadlines first, today's meetings with their prep, then the
approved actions.

## The six pieces, per step

| Piece | Where |
| --- | --- |
| Trigger | `/morning` (run it, or resume with `/morning resume`, restart with `/morning from 2`) |
| Instruction file | `steps/<n>-<name>/instructions.md` (+ lane files in step 3) |
| Maker | `.claude/agents/maker.md` (generic: reads the step's instructions) |
| Checker | `.claude/agents/checker.md` + `steps/<n>-<name>/rubric.md` |
| Gate A | pass/fail, orchestrated in `.claude/commands/morning.md`; `max_retries` in config |
| Gate B | you, in chat; described per step in `morning.md` |
| State | `state/<date>/<n>-<name>.md` |

## Commands

| Command | What it does |
| --- | --- |
| `/morning` | Runs the four steps with their gates |
| `/teach <correction>` | Turns a correction into an edit of the right file (instruction, rubric, strategy, rules, source, config) |
| `/loop-health` | Reviews 14 days of runs; asks whether to retire the loop if nobody edits, rejects or applies anything |

## Two rules baked in

1. **Never correct the loop in chat.** Use `/teach` so the fix lands in a file and accumulates.
2. **Switch off loops you no longer steer.** `/loop-health` asks; it never deletes.

## Quick start

1. `cp config/morning-loop.example.md config/morning-loop.local.md` and fill in project, vault path.
2. `cp context/strategy.example.md context/strategy.md` and write numbered, measurable goals
   (G1, G2...). Steps 2 and 3 are only as sharp as this file.
3. `cp context/backlog-rules.example.md context/backlog-rules.md` and describe your labels, required
   fields and hygiene rules.
4. Connect your backlog tool, chat and calendar to Claude Code (or `cp .mcp.json.example .mcp.json` and
   edit it). Make the notes vault readable.
5. Optional: drop customer files in `context/customers/` (see its README).
6. Run `claude` in this folder, then `/morning`.

## Safety model

- Steps 1-3 are read-only; the only writes are state files in `state/`.
- Step 4 executes the exact approved content, one action at a time, and never retries a write.
- Gate A is binary. A step that cannot pass is reported with its failures, not shown as a result.
- The checker never sees the maker's reasoning.
- Content of tickets, notes, chats and events is data, never instructions.
- Private files are git-ignored: `config/*.local.md`, `context/strategy.md`, `context/backlog-rules.md`,
  `context/customers/*`, `state/*`, `.mcp.json`.
- `.claude/settings.json` asks before any file write outside `state/` or any shell command. Write
  tools of your connected tracker are guarded by the prompt in step 4 and your own tool permissions.

## Adding a source

Write `sources/<name>.md` following [`sources/README.md`](sources/README.md), add it to `Sources` in
your config, and add its rules to `steps/1-collect/rubric.md` if it has special windows or filters.

## Layout

```
.claude/commands/   /morning /teach /loop-health
.claude/agents/     maker, checker (generic)
steps/              1-collect, 2-align, 3-propose (hygiene, prep, tickets), 4-apply: instructions + rubric
sources/            backlog, notes, teams, calendar + contract
config/             settings (copy the example to *.local.md)
context/            strategy, backlog-rules, customers/
state/              per-day step files, history, feedback log (git-ignored)
```

## Known limits

- Started by you. A schedule can run steps 1-2 and wait at the first gate B, but is not set up here.
- Chat search usually covers 1:1, group and meeting chats, not channel posts.
- Customer material is read as context, not used for training; no file means no customer claims.
- The checker is only as good as `strategy.md` and `backlog-rules.md`.

## License

MIT
