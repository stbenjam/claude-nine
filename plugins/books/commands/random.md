---
description: Pick a random book from TBR or library
---

You are helping the user pick a random book from their Calibre library.

## Selection Process

Use the Calibre skill to select a random book:

### 1. Determine Selection Pool

By default, select from TBR list, but check if user specified:
- **TBR** (default): `#read:No and #archived:No`
- **All unread**: `#read:No`
- **Entire library**: no filter
- **Specific criteria**: by author, series, genre, rating, page count, etc.

### 2. Query the Pool

Query all books matching the criteria:
```bash
--fields='title,authors,series,series_index,*goodreads,*pages,timestamp'
--search='[appropriate search based on user criteria]'
--for-machine
```

### 3. Random Selection

From the results:
- Count total books in pool
- Select one at random
- Present it with full details

### 4. Context About the Selection

Provide helpful context:
- When it was added to library (from `timestamp`)
- Why it might be interesting to read now
- How it fits current reading patterns
- Series context if applicable

## Output Format

Present the random selection:

```
# 🎲 RANDOM BOOK SELECTION

**[Book Title]** by [Author]

## Details
- **Series**: [Series Name #X] or "Standalone"
- **Pages**: XXX pages
- **Rating**: X.X / 5 (Goodreads)
- **Added to Library**: [date or "X months/years ago"]

## Why Read This Now?

[Provide 2-3 reasons why this might be a good choice, such as:]
- Fits your recent reading pattern of [genre/length/style]
- Next book in [Series Name] series
- Highly rated on Goodreads
- Been in your TBR for [time], might be a good time to revisit
- Quick read at XXX pages if you're between longer books
- This author is similar to [recent author] you enjoyed

## Pool Information
Selected randomly from **X books** in your [TBR/unread books/library/specified criteria]

---
Not feeling it? Run /books:random again for another suggestion!
Or try /books:vibes to find books with similar themes to one you enjoyed.
```

## Advanced Options

If the user specifies additional criteria, combine them:

**Examples:**
- "Random book under 300 pages": Add `#pages:"<300"`
- "Random unread Sanderson": Add `authors:"Sanderson"`
- "Random highly rated book": Add `#goodreads:">4"`
- "Random from series": Add `not series:""`
- "Random standalone": Add `series:""`
- "Random book added this year": Add `timestamp:">YYYY-01-01"`

## Implementation Notes

- Use Python or similar to select random index from JSON array results
- Handle edge cases (empty pool, pool of 1)
- If pool is small (< 10 books), mention all options
- Exclude archived books by default unless user specifically asks
- Make selection truly random - don't bias toward highest rated or recently added
- If user runs command multiple times, try to avoid repeating recent suggestions

## Example Python Snippet for Randomization

```python
import json
import random
import sys

data = json.load(sys.stdin)
if data:
    book = random.choice(data)
    print(json.dumps(book, indent=2))
```

You can pipe calibredb output through this to get random selection.
