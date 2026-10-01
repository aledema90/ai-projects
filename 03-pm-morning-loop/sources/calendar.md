# Source: calendar

**Purpose:** today's meetings.

## Requires

- A connected calendar tool with read access (Outlook in the default setup).
- Config keys: `prep_exclude` (titles or keywords of events that never need prep).

If not connected: `SOURCE_FAILED: calendar tool not available`.

## How to fetch (read-only)

1. List events whose start falls **today** in the user's time zone, including recurring instances.
   Skip events the user declined.
2. Map to the common format:
   - `id`: `calendar:<event id>`; `type: event`; `url`: event link if available
   - `title`, `updated` = start time `YYYY-MM-DD HH:MM`
   - `fields`: `start`, `end`, `attendees` (names), `organizer`, `description` (first 10 lines),
     `online_link`
   - `signals`: `excluded` when the title matches `prep_exclude` (keep the event, mark it)

## Output

`count_fetched: N` followed by the events in time order.
