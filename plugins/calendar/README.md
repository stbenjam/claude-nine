# Calendar Plugin for Claude Code

Integrate macOS Calendar with Claude Code using `icalBuddy` and AppleScript.

## Installation

### Prerequisites

1. **Install icalBuddy** (required):
   ```bash
   brew install ical-buddy
   ```

2. **Grant Calendar Access** (if prompted):
   - macOS may ask for permission to access Calendar
   - Go to System Settings > Privacy & Security > Calendar
   - Enable access for Terminal or your terminal app

## Features

- ✅ **Query calendar events** using fast icalBuddy commands
- ✅ **Create new events** with AppleScript
- ✅ **Modify existing events**
- ✅ **Delete events**
- ✅ **Filter by calendar** (personal, work, etc.)
- ✅ **Date range queries** (today, tomorrow, this week, custom ranges)
- ✅ **Recurring events support**
- ✅ **Location and notes**
- ✅ **Reminders/alerts**

## Available Commands

Use these slash commands for quick access:

- `/calendar:today` - Show today's events
- `/calendar:tomorrow` - Show tomorrow's events
- `/calendar:week` - Show this week's events
- `/calendar:create` - Create a new event (interactive)

## Skills

The `calendar` skill is automatically invoked when you ask about calendar events or scheduling.

**Example prompts:**
- "What's on my calendar today?"
- "Show me my work meetings this week"
- "Add a dentist appointment on Friday at 3pm"
- "When is my next workout?"
- "Cancel my 2pm meeting"

## Quick Reference

### icalBuddy Commands

#### Basic Queries

```bash
# Today's events
icalBuddy -f eventsToday

# Tomorrow's events
icalBuddy -f eventsToday+1

# Next 7 days
icalBuddy -f eventsFrom:today to:today+7

# Specific date
icalBuddy -f eventsOn:'2025-11-15'

# Date range
icalBuddy -f eventsFrom:'2025-11-01' to:'2025-11-30'
```

#### Filtering

```bash
# Exclude holiday calendars
icalBuddy -ec "Holidays in United States,US Holidays" -f eventsToday

# Include only work calendar
icalBuddy -ic "stbenjam@redhat.com" -f eventsToday

# Multiple calendars
icalBuddy -ic "Home,Work" -f eventsToday+7
```

#### Output Formatting

```bash
# Plain text (no colors/formatting)
icalBuddy -n -f eventsToday

# Custom bullet points
icalBuddy -b "• " -f eventsToday

# Custom separators
icalBuddy -ps " | " -f eventsToday
```

### AppleScript Event Creation

#### Basic Event

```applescript
tell application "Calendar"
    set targetCalendar to calendar "Home"

    set startDate to current date
    set year of startDate to 2025
    set month of startDate to 11
    set day of startDate to 15
    set hours of startDate to 14
    set minutes of startDate to 30
    set seconds of startDate to 0

    set endDate to startDate + (1 * hours)

    make new event at end of events of targetCalendar with properties {
        summary:"Event Title",
        start date:startDate,
        end date:endDate,
        location:"Event Location",
        description:"Event notes go here"
    }
end tell
```

#### Event with Reminder

```applescript
tell application "Calendar"
    set targetCalendar to calendar "Home"

    -- Set up dates...

    set newEvent to make new event at end of events of targetCalendar with properties {
        summary:"Appointment",
        start date:startDate,
        end date:endDate
    }

    -- Add 15-minute reminder
    tell newEvent
        make new display alarm at end of display alarms with properties {
            trigger interval:-15
        }
    end tell
end tell
```

#### All-Day Event

```applescript
tell application "Calendar"
    set targetCalendar to calendar "Home"

    set eventDate to current date
    set year of eventDate to 2025
    set month of eventDate to 11
    set day of eventDate to 15
    set time of eventDate to 0

    make new event at end of events of targetCalendar with properties {
        summary:"Birthday Party",
        start date:eventDate,
        allday event:true
    }
end tell
```

#### Recurring Event

```applescript
tell application "Calendar"
    set targetCalendar to calendar "Work"

    -- Set up dates...

    make new event at end of events of targetCalendar with properties {
        summary:"Weekly Team Meeting",
        start date:startDate,
        end date:endDate,
        recurrence:"FREQ=WEEKLY;COUNT=52"
    }
end tell
```

**Recurrence patterns:**
- `"FREQ=DAILY"` - Every day
- `"FREQ=WEEKLY"` - Every week
- `"FREQ=WEEKLY;INTERVAL=2"` - Every 2 weeks
- `"FREQ=MONTHLY"` - Every month
- `"FREQ=YEARLY"` - Every year
- `"FREQ=WEEKLY;COUNT=10"` - 10 occurrences
- `"FREQ=DAILY;UNTIL=20251231T235959Z"` - Until specific date

### Finding and Modifying Events

```applescript
tell application "Calendar"
    set targetCalendar to calendar "Home"

    -- Find event by title
    set foundEvents to (every event of targetCalendar whose summary is "Dentist")

    if (count of foundEvents) > 0 then
        set theEvent to item 1 of foundEvents

        -- Update properties
        tell theEvent
            set location to "New Address"
            set description to "Updated notes"
        end tell
    end if
end tell
```

### Deleting Events

```applescript
tell application "Calendar"
    set targetCalendar to calendar "Home"

    set foundEvents to (every event of targetCalendar whose summary is "Cancelled Meeting")

    if (count of foundEvents) > 0 then
        delete item 1 of foundEvents
    end if
end tell
```

## Performance Notes

### Use icalBuddy for Reading ✅
- **Fast** - No timeout issues
- **Reliable** - Works with all calendar types
- **Clean output** - Easy to parse
- Use for: Querying events, listing calendars, date ranges

### Use AppleScript for Writing ⚠️
- Can be **slow** with synced calendars (Google, iCloud)
- Always use **short timeouts** (5-10 seconds)
- Use for: Creating, modifying, deleting events
- Avoid for: Large date range queries

## Tips & Best Practices

1. **Filter out noise**: Exclude holiday calendars with `-ec "Holidays"`
2. **Use relative dates**: `today`, `today+1`, `today+7` instead of specific dates
3. **Confirm deletions**: Always confirm before deleting events
4. **Choose right calendar**: Ask user which calendar for new events
5. **Default duration**: Use 1 hour if user doesn't specify
6. **Add reminders**: Ask if user wants a reminder (default: no)
7. **Format output**: Present events in an organized, readable format

## Troubleshooting

### icalBuddy not found
```bash
brew install ical-buddy
```

### AppleScript timeout
- Increase timeout parameter
- Use icalBuddy instead for queries
- Check internet connection (for synced calendars)

### Permission denied
- Go to System Settings > Privacy & Security > Calendar
- Enable access for Terminal

### Calendar not found
- List calendars: `icalBuddy calendars`
- Use exact calendar name (case-sensitive)

### No events showing
- Check date range
- Verify calendar filters
- Try without filters to see all events

## Examples

### Show today's work meetings
```bash
icalBuddy -ic "stbenjam@redhat.com" -f eventsToday
```

### Show personal events this week
```bash
icalBuddy -ic "Home,stephen@bitbin.de" -f eventsFrom:today to:today+7
```

### Create doctor appointment
```bash
osascript <<'EOF'
tell application "Calendar"
    set targetCalendar to calendar "Home"
    set startDate to current date
    set year of startDate to 2025
    set month of startDate to 11
    set day of startDate to 20
    set hours of startDate to 10
    set minutes of startDate to 0
    set seconds of startDate to 0
    set endDate to startDate + (1 * hours)
    make new event at end of events of targetCalendar with properties {
        summary:"Doctor Appointment",
        start date:startDate,
        end date:endDate,
        location:"Medical Center",
        description:"Annual checkup"
    }
end tell
EOF
```

### Find next gym session
```bash
icalBuddy -ic "stephen@bitbin.de" -f eventsFrom:today to:today+30 | grep -i "orangetheory\|gym\|workout"
```

## Reference Links

- [icalBuddy Documentation](https://hasseg.org/icalBuddy/)
- [AppleScript Calendar Suite](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/reference/ASLR_cmds.html)
- [iCalendar Recurrence Rules](https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html)

## License

MIT

## Author

Stephen Benjamin
