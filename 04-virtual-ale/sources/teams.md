# Source: teams

**Purpose:** Teams messages inside the window that ask for, decide or report a change to the product.

## Requires

- A connected Microsoft 365 / Teams tool that can search or list chat messages and list channel messages.
- Config keys: `teams_chats`, `teams_chat_exclude`, `teams_channels`.

If not connected: `SOURCE_FAILED: teams tool not available`. If chats work but channels do not (or the
reverse), return what works and state the part that failed.

## How to fetch (read-only)

Search in **one-day slices** (and split a day further if it returns more than ~200 results): a single
search over a wide window misses the newest messages (index lag), narrow slices do not. De-duplicate by
message id.

1. **Chats.** 1:1, group and meeting chats with messages inside the window (`teams_chats: all`, or only the listed
   chats). Skip `teams_chat_exclude`. Paginate.
2. **Channels.** For each entry in `teams_channels`, list posts and their replies inside the window,
   using `team_id` and `channel_id` (listing teams by name may be refused by the tenant; the ids are
   enough).
3. Keep only actionable messages: a feature request, a change of scope or priority, a decision, a bug or
   customer problem, a deadline or date, a question to the user that needs a product answer. Drop
   greetings, reactions, scheduling and small talk. A thread with one request is one item, not one item
   per reply; cite the message that states the request.
4. Map to the common format:
   - `id`: `teams:<message id>`; `type`: `message` (chat) or `channel-post`; `url`: message link if given
   - `summary`: a quote of at most 2 lines
   - `refs`: issue numbers or GitLab issue urls written in the message
   - `fields`: `chat` or `team/channel`, `thread` (root message id)
   - `signals`: `request`, `decision`, `bug`, `deadline`, `mentioned-me`

## Output

`chats: scanned N / kept K, channel_posts: scanned N / kept K`, then the kept items. State how many were
dropped as non-actionable, so the checker can see the filter was applied.
