---
name: calendar
description: Query and manage macOS Calendar events. Use when the user asks about calendar events, appointments, schedules, or wants to create/modify calendar entries.
---

# macOS Calendar Integration Skill

You are helping the user query and manage their macOS Calendar using `icalBuddy` and AppleScript.

## Tools Available

### 1. icalBuddy (Preferred for Queries)

**Installation**: `brew install ical-buddy`

**Why use icalBuddy:**
- Fast and reliable for reading calendar events
- No timeout issues with synced calendars
- Clean, formatted output
- Simple command-line interface

**Basic Usage:**

```bash
# Today's events
icalBuddy -f eventsToday

# Tomorrow's events
icalBuddy -f eventsToday+1

# Next 7 days
icalBuddy -f eventsFrom:today to:today+7

# Specific date range
icalBuddy -f eventsFrom:'2025-11-04' to:'2025-11-11'

# Events for a specific day
icalBuddy -f eventsOn:'2025-11-04'
```

**Filtering by Calendar:**

```bash
# Include only specific calendars
icalBuddy -ic "Work,Home" -f eventsToday

# Exclude specific calendars
icalBuddy -ec "Holidays in United States,US Holidays" -f eventsToday
```

**Output Options:**

```bash
# No formatting (plain text)
icalBuddy -n -f eventsToday

# Custom separators
icalBuddy -ps "| - |" -f eventsToday

# Show only bullet points and times
icalBuddy -b "• " -f eventsToday
```

**Common Patterns:**

```bash
# Work events for the week
icalBuddy -ic "stbenjam@redhat.com" -f eventsFrom:today to:today+7

# Personal events only
icalBuddy -ic "Home,stephen@bitbin.de" -f eventsToday

# Exclude all holiday calendars
icalBuddy -ec "Holidays,US Holidays" -f eventsToday+1
```

### 2. AppleScript (For Creating/Modifying Events)

**Why use AppleScript:**
- Can create, modify, and delete events
- Full access to event properties
- Works with all calendar types

**IMPORTANT NOTES:**
- AppleScript queries can be VERY SLOW with synced calendars (Google, iCloud, Exchange)
- Use short timeouts (5-10 seconds) when using AppleScript
- Always use icalBuddy for reading events unless you need specific event properties not available via icalBuddy
- AppleScript is primarily for CREATE, UPDATE, DELETE operations

### Creating Events with AppleScript

**Basic Event Creation:**

```applescript
tell application "Calendar"
    set targetCalendar to calendar "calendar-name"

    -- Create start date
    set startDate to current date
    set year of startDate to 2025
    set month of startDate to 11
    set day of startDate to 11
    set hours of startDate to 13
    set minutes of startDate to 30
    set seconds of startDate to 0

    -- Create end date (add duration)
    set endDate to startDate + (1 * hours)

    -- Create the event
    set newEvent to make new event at end of events of targetCalendar with properties {
        summary:"Event Title",
        start date:startDate,
        end date:endDate,
        location:"Event Location",
        description:"Event description or notes"
    }

    return "Event created successfully"
end tell
```

**Event with Alert/Reminder:**

```applescript
tell application "Calendar"
    set targetCalendar to calendar "calendar-name"

    set startDate to current date
    -- ... set date properties ...

    set newEvent to make new event at end of events of targetCalendar with properties {
        summary:"Event Title",
        start date:startDate,
        end date:endDate
    }

    -- Add alert (minutes before event)
    tell newEvent
        make new display alarm at end of display alarms with properties {
            trigger interval:-15  -- 15 minutes before
        }
    end tell

    return "Event created with alert"
end tell
```

**All-Day Event:**

```applescript
tell application "Calendar"
    set targetCalendar to calendar "calendar-name"

    set eventDate to current date
    set year of eventDate to 2025
    set month of eventDate to 11
    set day of eventDate to 15
    set time of eventDate to 0

    set newEvent to make new event at end of events of targetCalendar with properties {
        summary:"All Day Event",
        start date:eventDate,
        allday event:true
    }

    return "All-day event created"
end tell
```

**Recurring Event:**

```applescript
tell application "Calendar"
    set targetCalendar to calendar "calendar-name"

    set startDate to current date
    -- ... set date properties ...

    set newEvent to make new event at end of events of targetCalendar with properties {
        summary:"Weekly Meeting",
        start date:startDate,
        end date:endDate,
        recurrence:"FREQ=WEEKLY;COUNT=10"  -- Every week for 10 occurrences
    }

    return "Recurring event created"
end tell
```

**Common Recurrence Patterns:**

- Daily: `"FREQ=DAILY"`
- Weekly: `"FREQ=WEEKLY"`
- Bi-weekly: `"FREQ=WEEKLY;INTERVAL=2"`
- Monthly: `"FREQ=MONTHLY"`
- Yearly: `"FREQ=YEARLY"`
- With end date: `"FREQ=WEEKLY;UNTIL=20251231T235959Z"`
- With count: `"FREQ=DAILY;COUNT=30"`

### Modifying Events with AppleScript

**Finding and Updating an Event:**

```applescript
tell application "Calendar"
    set targetCalendar to calendar "calendar-name"

    -- Find event by summary
    set foundEvents to (every event of targetCalendar whose summary is "Event Title")

    if (count of foundEvents) > 0 then
        set theEvent to item 1 of foundEvents

        -- Update properties
        tell theEvent
            set location to "New Location"
            set description to "Updated description"
        end tell

        return "Event updated"
    else
        return "Event not found"
    end if
end tell
```

**Deleting an Event:**

```applescript
tell application "Calendar"
    set targetCalendar to calendar "calendar-name"

    set foundEvents to (every event of targetCalendar whose summary is "Event Title")

    if (count of foundEvents) > 0 then
        delete item 1 of foundEvents
        return "Event deleted"
    else
        return "Event not found"
    end if
end tell
```

## Available Calendars

The user has these calendars configured (use icalBuddy or AppleScript to get current list):
- Home
- Work
- Family
- stephen@bitbin.de (personal Google)
- stbenjam@redhat.com (work Google)

**To list all calendars:**

```bash
# Using icalBuddy
icalBuddy calendars

# Using AppleScript
osascript -e 'tell application "Calendar" to get name of calendars'
```

## Best Practices

### For Queries (Reading Events)
1. **ALWAYS use icalBuddy** - it's fast and reliable
2. Use appropriate timeout (5 seconds is usually enough)
3. Filter out holiday calendars if not needed
4. Format output for readability

### For Mutations (Creating/Modifying Events)
1. **Use AppleScript** for create/update/delete operations
2. Always use HEREDOC syntax for multi-line AppleScript in bash
3. Set appropriate timeouts (10 seconds for creation)
4. Return confirmation messages
5. Use try-catch blocks for error handling

### Date Handling
1. For icalBuddy: use relative dates (`today`, `today+1`, `today+7`)
2. For AppleScript: construct date objects explicitly
3. Always set time to 0 for date comparisons
4. Use ISO format for date strings in icalBuddy

### Performance Tips
1. Avoid querying all calendars at once with AppleScript
2. Use specific calendar names when possible
3. Limit date ranges to reduce result sets
4. Use icalBuddy's filtering options to exclude unwanted calendars

## Common Use Cases

### "What's on my calendar today?"
```bash
icalBuddy -ec "Holidays in United States,US Holidays,Holidays" -f eventsToday
```

### "What meetings do I have this week?"
```bash
icalBuddy -ic "stbenjam@redhat.com" -f eventsFrom:today to:today+7
```

### "Create a dentist appointment"
Use AppleScript with user-provided details:
- Calendar to use (ask if not specified - default to personal calendar)
- Date and time
- Duration (ask if not specified - default to 1 hour)
- Location (optional)
- Any notes (optional)

### "When is my next workout?"
```bash
icalBuddy -ic "stephen@bitbin.de" -f eventsFrom:today to:today+30 | grep -i "workout\|gym\|orangetheory"
```

### "Cancel my 3pm meeting"
1. Use icalBuddy to find events at that time
2. Confirm with user which event to delete
3. Use AppleScript to delete the event

## Error Handling

### AppleScript Errors
- Calendar not found: Verify calendar name with user
- Permission denied: User may need to grant Calendar access to Terminal
- Timeout: Increase timeout or use icalBuddy instead

### icalBuddy Errors
- Command not found: Install with `brew install ical-buddy`
- No events returned: Check date range and calendar filters
- Calendar not found: Check calendar name spelling

## Examples

**User**: "What's on my calendar tomorrow?"
```bash
icalBuddy -ec "Holidays" -f eventsToday+1
```

**User**: "Add a haircut appointment on Nov 15 at 2pm"
```applescript
osascript <<'EOF'
tell application "Calendar"
    set targetCalendar to calendar "Home"
    set startDate to current date
    set year of startDate to 2025
    set month of startDate to 11
    set day of startDate to 15
    set hours of startDate to 14
    set minutes of startDate to 0
    set seconds of startDate to 0
    set endDate to startDate + (1 * hours)
    make new event at end of events of targetCalendar with properties {
        summary:"Haircut",
        start date:startDate,
        end date:endDate
    }
    return "Haircut appointment created"
end tell
EOF
```

**User**: "Show me my work schedule for next week"
```bash
icalBuddy -ic "stbenjam@redhat.com" -f eventsFrom:today+7 to:today+14
```

## Safety Notes

- **Read-only with icalBuddy**: No risk of modifying data
- **Be careful with AppleScript**: Confirm before deleting events
- **Ask before creating**: Confirm event details before creation
- **Respect calendar selection**: Use appropriate calendar based on event type
