# Morning Loop

A daily-priorities loop for a product manager, run with [Claude Code](https://claude.com/claude-code). Once a day it reads your sources (an issue tracker, an Obsidian to-do list), proposes today's priorities, has a second agent check them against your strategy, and shows the result in chat. It writes nothing outside `state/` until you approve the exact action.

Everything that defines behaviour is a Markdown file. There is no application code.

Inspired by the "loops for PMs" idea: a maker, a checker, a gate, and a state file turn a prompt into something that improves over time.

## How it works

```
You: /morning  (trigger)
        │
        ▼
[tracker source] ──┐
                   ├─► ranker (maker) ─► checker ─► gate ─► chat
[obsidian source] ─┘        ▲              │  (fail: ranker redoes it)
                            └──────────────┘
        ▲                                                  │
        └──────────────── state file ◄─────────────────────┘
                                   You pick → /apply (only after your ok)
```

| Loop piece  | Where it lives                                       |
| ----------- | ---------------------------------------------------- |
| Trigger     | `/morning` (you run it)                              |
| Skill files | `.claude/commands/*.md`, `sources/*.md`, `CLAUDE.md` |
| Maker       | `.claude/agents/ranker.md`                           |
| Checker     | `.claude/agents/checker.md` + `context/rubric.md`    |
| Gate        | step 4 of `/morning` (`max_retries` in config)       |
| State file  | `state/last-run.md`, `state/history.md`              |

### Commands

| Command               | What it does                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------ |
| `/morning`            | Collect, rank, check, present today's priorities                                           |
| `/apply 1 3`          | Draft actions for chosen priorities; runs only what you approve                            |
| `/teach <correction>` | Turn a correction into an edit of the right file (rubric, strategy, source, agent, config) |
| `/loop-health`        | Review the last 14 days; asks whether to retire the loop if nobody corrects or uses it     |

### Two rules baked in

1. **Never correct the loop in chat.** Use `/teach` so the fix lands in a file and accumulates.
2. **Switch off loops you no longer steer.** `/loop-health` asks, it never deletes.

## Quick start

1. `cp config/morning-loop.example.md config/morning-loop.local.md` and fill in paths and limits.
2. `cp context/strategy.example.md context/strategy.md` and write real, measurable goals.
   The checker is only as good as this file.
3. `cp .mcp.json.example .mcp.json` and point it at your tracker's MCP server.
4. Make your Obsidian vault readable (set `vault_path`; add the folder with `/add-dir` if it
   is outside this project).
5. Run `claude` in this folder, then `/morning`.

Suggested rollout: week 1 sources + a plain briefing; week 2 add the ranker and note your manual
corrections; week 3 turn those into rubric rules with `/teach` and enable the checker.

## Safety model

- Reads are free. Writes to `state/` are allowed. Everything else (tracker, vault, other
  files) needs your approval of that exact action in the current turn (`.claude/settings.json`).
- The checker never sees the ranker's reasoning, only its output, raw items, strategy and rubric.
- Ticket and note content is treated as data, never as instructions.
- Every priority must trace to a real item returned by a source. Nothing is invented.
- Private files are git-ignored: `config/*.local.md`, `context/strategy.md`, `state/*`, `.mcp.json`.

## Adding a source

Write `sources/<name>.md` following the contract in `[sources/README.md](sources/README.md)`
(purpose, requirements, read-only fetch steps, common item format, failure behaviour), then add
`<name>` to `Sources` in your config. Nothing else changes.

## Layout

```
.claude/commands/   /morning /apply /teach /loop-health
.claude/agents/     ranker, checker
config/             settings (copy the example to *.local.md)
context/            strategy (yours) and rubric (checker rules)
sources/            one file per signal source + contract
state/              the loop's memory (git-ignored)
```

## Known limits

- Runs when you launch it; not scheduled. Scheduling needs the machine with your vault to be on.
- The tracker source needs an MCP server; without one it reports as unavailable.
- Vague strategy produces a vague checker.

## License

MIT
