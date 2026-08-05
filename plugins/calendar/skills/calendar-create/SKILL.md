---
name: calendar-create
description: Create a macOS Calendar event after collecting its calendar, title, time, duration, and optional details.
user-invocable: true
---

# Create a calendar event

Use the `calendar` skill and AppleScript for mutations. Before writing,
collect or confirm:

1. the calendar (for example Home, Work, `stephen@bitbin.de`, or
   `stbenjam@redhat.com`);
2. event title;
3. date and start time;
4. duration, defaulting to one hour when the user agrees;
5. optional location and notes; and
6. whether to add a reminder.

Ask follow-up questions for ambiguous dates or times. Create the event only
after the details are clear, then report the calendar, title, time, and any
reminder that was added. Respect Calendar permissions and report AppleScript
errors without claiming success.
