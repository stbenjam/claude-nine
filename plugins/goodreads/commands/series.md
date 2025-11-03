---
description: List unfinished series and the next book to read in each
---

You are helping the user find incomplete series in their Goodreads library.

## Task

Use the `goodreads` skill to find series where:
- The user has read at least one book in the series
- There are still unread books in the series
- Display the next book to read in each series

## Implementation

Write a Python script using goodreads_lib:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '__SKILL_DIR__/scripts')
from goodreads_lib import GoodreadsLibrary

lib = GoodreadsLibrary()

# Get incomplete series
incomplete = lib.get_incomplete_series()

# Sort by series name
incomplete_sorted = sorted(incomplete.items(), key=lambda x: x[0])

# Display results
print("\n# UNFINISHED SERIES\n")
print(f"You have {len(incomplete_sorted)} incomplete series:\n")

for i, (series_name, info) in enumerate(incomplete_sorted, 1):
    read = info['read_count']
    total = info['total_count']
    next_book = info['next_book']

    print(f"{i}. **{series_name}** ({read}/{total} books read)")

    if next_book:
        title = next_book.title
        author = next_book.author
        index = next_book.series_index or '?'
        pages = next_book.num_pages or '?'
        rating = f"{next_book.average_rating:.2f}" if next_book.average_rating else "N/A"

        print(f"   Next: **{title}** by {author}")
        print(f"   Book #{index} | {pages} pages | Goodreads: {rating}/5\n")
    else:
        print(f"   Next: Unable to determine\n")
```

## Output Format

```
# UNFINISHED SERIES

You have X incomplete series:

1. **Series Name** (X/Y books read)
   Next: **Book Title** by Author
   Book #X | XXX pages | Goodreads: X.XX/5

2. **Another Series** (X/Y books read)
   Next: **Book Title** by Author
   Book #X | XXX pages | Goodreads: X.XX/5
```

## Important Notes

- Series information is parsed from book titles (e.g., "Title (Series, #1)")
- Books are sorted by series_index within each series
- Only show series where at least one book has been read
- The "next" book is the first unread book in series order
- Handle missing data gracefully (pages, ratings may be missing)
- Use the Bash tool to run your Python script
- Replace `__SKILL_DIR__` with the actual skill directory path
