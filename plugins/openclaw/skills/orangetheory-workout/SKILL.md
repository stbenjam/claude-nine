---
name: orangetheory-workout
description: Look up Orangetheory Fitness daily workout summaries. Use when asked about today's or tomorrow's Orangetheory, OTF, or orange theory workout.
---

# Orangetheory Workout Skill

Fetches OTF workout intel from Reddit using a bundled script.

## Getting the Workout

Determine the target date (default to tomorrow unless user specifies otherwise), then run:

```bash
python3 <skill-dir>/scripts/get_workout.py [--date YYYY-MM-DD] [--format 2G|3G|Strength50]
```

The script searches Reddit's Daily Workout and Early Intel flairs, picks the best matching workout, and returns JSON:

```json
{
  "date": "Tuesday, April 21, 2026",
  "source": "Daily Workout",
  "available_formats": ["2G", "Orange 60 3G"],
  "workout": {
    "label": "2G",
    "content": "...full workout markdown..."
  }
}
```

If no workout is found, the output contains an `"error"` field instead.

## Fallback: OTFInsider

If the Reddit script returns no result (error or empty), fall back to OTFInsider in this order:

1. **Calendar** (`https://www.otfinsider.com/calendar`) — extract the template type for the target date (e.g. "Power Focused", "Strength", "Endurance"). The calendar is always available even when daily intel isn't posted.
2. **Direct intel page** (`https://www.otfinsider.com/intel/{date}-{template}.html` where date is `month-DD-YYYY` and template is lowercase, e.g. `april-27-2026-power`). This returns a 404 if full intel hasn't been posted yet — in that case, report only the template type from the calendar.

Example: for 2026-04-27 with template "Power", try:
`https://www.otfinsider.com/intel/april-27-2026-power`

When reporting, distinguish between:
- **Template type only** (calendar shows it, full intel not yet posted)
- **Full workout available** (direct intel page returns content)

## Summarizing

From the `workout.content` field, summarize in 1–2 paragraphs:

- Describe each block (Treadmill, Rower, Floor) briefly — the type of work, rep/time structure, and key exercises.
- Keep it concise and scannable, not a full copy-paste of the original.
- If the source is "Early Intel", flag that details may change slightly.
- If the requested format isn't available, list what is from `available_formats`.
- End with a short, energetic encouragement tailored to the workout type.
