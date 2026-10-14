# Source: meetings

**Purpose:** requests, decisions and changes discussed in meetings recorded by a meeting-recorder agent.

The recorder sends each attendee one email per meeting, from `meetings_sender`, with the subject
`<meetings_subject_prefix><meeting name>` and a link (text `meetings_link_text`) to the full transcript,
a `.txt` file in SharePoint/OneDrive. Only meetings the operator attended reach their mailbox.

## Requires

- A connected Microsoft 365 tool with Outlook email search, SharePoint search and resource read.
- Config keys: `meetings_sender`, `meetings_subject_prefix`, `meetings_link_text`, `meetings_exclude`.

If not connected: `SOURCE_FAILED: microsoft 365 tool not available`.

## How to fetch (read-only)

1. Search Outlook for emails **from `meetings_sender`** (filter by address, not keyword) received inside
   the window. Paginate until empty. Skip meetings named in `meetings_exclude`.
2. For each email, read the body and extract the transcript link (`meetings_link_text`), the meeting
   name (subject after `meetings_subject_prefix`), attendees (`to` recipients) and the sent time.
3. Resolve the link: a raw `https://...sharepoint.com/...` url cannot be read directly. Search SharePoint
   for the transcript file name without `.txt` (file type `txt`, created after the window start), take
   the exact name match, then read that resource. If not found, retry once with the meeting-name part of
   the file name. If still not found, use the email's summary block and set
   `fields: transcript: missing`.
4. From each transcript keep only points about the product: requests, decisions, scope or priority
   changes, bugs, deadlines, action items with an owner. One item per point.
5. Map to the common format:
   - `id`: `meetings:<transcript file stem>#<n>` (n = order in the transcript); `type: meeting-point`
   - `url`: the transcript link; `who`: the speaker (as named in the transcript)
   - `summary`: paraphrase in English plus a quote of at most 2 lines
   - `refs`: issue numbers or urls said or shown in the meeting
   - `fields`: `meeting`, `attendees`, `transcript: full | missing`
   - `signals`: `request`, `decision`, `bug`, `deadline`, `action-item`

## Output

`emails: N, transcripts_read: R, transcripts_missing: M, points_kept: K`, then the items.
