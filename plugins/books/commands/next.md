---
description: Analyze my reading patterns and suggest what to read next from my TBR
---

You are helping the user decide what to read next from their Calibre library TBR list.

## Analysis Steps

Perform the following analysis using the Calibre skill:

### 1. Analyze Recent Reading Patterns

Query the last 15 books marked as read (sorted by *dateread DESC):
- Calculate average page count of recent reads
- Identify if the user has been reading mostly long books (>600 pages)
- Look for series patterns in recent reads
- Use the `*dateread` field to determine actual reading order
- Look at `rating` field to see what books the user liked

### 2. Check for Series Continuity

For each series found in recent reads:
- Check if there are unread books in that series on the TBR
- Prioritize the next book in sequence (series_index), especially if the previous book had a high rating
- This is important for maintaining reading momentum!

### 3. Consider Reading Fatigue

Based on recent page counts:
- If average recent reads > 600 pages: Suggest shorter books (< 300 pages)
- If average recent reads < 400 pages: User might be ready for something longer
- Look for highly-rated short books as "palate cleansers"

### 4. Check Book Age in Library

Query books by timestamp (when added to library):
- Find recently added books (last 30 days) that are unread
- Find old books (added >1 year ago) that may have been forgotten
- Use `b.timestamp` field to determine when book was added

### 5. Filter by Quality

Prioritize books with:
- Goodreads rating >= 3.75 (if available)
- Consider page count relative to recent reading patterns
- Balance between series continuity and variety

## Output Format

Structure your response as a structured report with these categories:

```
# READING PATTERN SUMMARY
- Books read in last 30 days: X (use #dateread:">=30daysago")
- Average page count: Y pages
- Notable patterns: [e.g., "Completed Mistborn Era 2 series"]

# RECOMMENDATIONS BY CATEGORY

## 📚 SERIES CONTINUITY
Books that continue series you're currently reading:

- **Book Title** by Author
  Series: Series Name #X | Pages: XXX | Rating: X/5 | Added: [date/age]

## 🆕 RECENTLY ADDED
Books added to your library in the last 30 days:

- **Book Title** by Author
  Pages: XXX | Rating: X/5 | Added: [date]

## 💎 FORGOTTEN GEMS
Books added over a year ago that you may have forgotten:

- **Book Title** by Author
  Pages: XXX | Rating: X/5 | Added: [date/years ago]

## ⚡ QUICK READS
Shorter books (< 300 pages) for reading fatigue:

- **Book Title** by Author
  Pages: XXX | Rating: X/5 | Added: [age]

## 🌟 HIGHLY RATED
Top-rated unread books from your TBR:

- **Book Title** by Author
  Pages: XXX | Rating: X/5 | Added: [age]
```

## Important Notes

- Use `b.timestamp` to determine when books were added to the library
- Calculate age from timestamp (e.g., "2 days ago", "3 months ago", "2 years ago")
- Include 1-3 books per category (skip categories if no matches)
- ALWAYS check for incomplete series from recent reads first
- Balance series continuity with reading fatigue and variety
- Present data in a clean, scannable format
- Each category should help answer a different need: momentum, novelty, rediscovery, fatigue, or quality
- **IMPORTANT**: All queries should exclude archived books from recommendations
