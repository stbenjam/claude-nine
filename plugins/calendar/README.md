# calendar

Integrate macOS Calendar with Claude Code and Codex using `icalBuddy` and
AppleScript.

## Skills

- `calendar`: shared query and mutation guidance
- `calendar-today`: today's events, grouped by calendar
- `calendar-tomorrow`: tomorrow's events, grouped by calendar
- `calendar-week`: the next seven days with conflicts highlighted
- `calendar-create`: create an event after confirming its details

Ask for calendar information in natural language, such as “What is on my
calendar tomorrow?” or “Create a dentist appointment on Friday at 3pm.” Query
events with `icalBuddy` and use AppleScript only for writes.

## Setup

Install the query tool with `brew install ical-buddy` and grant the terminal
Calendar access in macOS Privacy & Security settings when prompted.
