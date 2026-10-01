# Source: teams

**Purpose:** find messages from **yesterday only** that may need action today.

## Requires

- A connected chat tool with message search or list (Microsoft Teams in the default setup).
- Config keys: `chat_lookback`, `chat_exclude`.

Known limitation: chat search usually covers 1:1, group and meeting chats, not channel posts.
State this in the output when it applies. If not connected: `SOURCE_FAILED: chat tool not available`.

## How to fetch (read-only)

1. Fetch messages sent or received **yesterday** (the single previous calendar day; on Monday, use
   Friday through Sunday). Ignore chats listed in `chat_exclude`.
2. Keep only messages that look actionable: a request or question to the user, a deadline or date, a
   decision that affects work, a mention of the user, a bug or customer problem. Drop greetings,
   reactions and small talk. Do not summarize the whole conversation.
3. Map to the common format:
   - `id`: `teams:<message id>`; `type: message`; `url`: message link if the tool provides one
   - `summary`: a quote of at most 2 lines
   - `fields`: `from`, `chat`, `sent_at`
   - `signals`: `mentioned-me`, `asks-me`, `has-deadline`

## Output

`count_scanned: N, count_kept: K` followed by the kept items. Say how many messages were dropped as
non-actionable, so the checker can see the filter was applied and not skipped.
