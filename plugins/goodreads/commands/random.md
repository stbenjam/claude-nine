---
description: Pick a random book from TBR or library
---

You are helping the user pick a random book from their Goodreads library.

## Task

Use the `analyze-goodreads-skill` skill to pick a random book from their TBR list.

## Implementation

Write a Python script using goodreads_lib:

```python
#!/usr/bin/env python3
import sys
import random
sys.path.insert(0, '__SKILL_DIR__/scripts')
from goodreads_lib import GoodreadsLibrary

lib = GoodreadsLibrary()

# Get TBR books
tbr = lib.get_tbr_books()

if not tbr:
    print("No books in your TBR!")
    sys.exit(0)

# Pick random book
book = random.choice(tbr)

# Display
print("\n# 🎲 RANDOM TBR PICK\n")
print(f"**{book.title}**")
print(f"by {book.author}\n")

if book.series and book.series_index:
    print(f"📚 Series: {book.series} #{book.series_index}")

if book.num_pages:
    print(f"📖 Pages: {book.num_pages}")

if book.average_rating:
    print(f"⭐ Goodreads Rating: {book.average_rating:.2f}/5")

if book.date_added:
    from datetime import datetime
    days_ago = (datetime.now() - book.date_added).days
    if days_ago < 30:
        print(f"🆕 Added: {days_ago} days ago")
    elif days_ago < 365:
        months = days_ago // 30
        print(f"📅 Added: {months} months ago")
    else:
        years = days_ago // 365
        print(f"📅 Added: {years} years ago")

print(f"\nTotal TBR books: {len(tbr)}")
```

## Output Format

```
# 🎲 RANDOM TBR PICK

**Book Title**
by Author Name

📚 Series: Series Name #X
📖 Pages: XXX
⭐ Goodreads Rating: X.XX/5
📅 Added: X months/years ago

Total TBR books: XX
```

## Important Notes

- Pick from books where `is_tbr` is True
- Display relevant metadata (series, pages, rating, date added)
- Show 'N/A' for any missing series, page-count, rating, or date-added field
- Use the Bash tool to run your Python script
- Replace `__SKILL_DIR__` with the actual skill directory path
