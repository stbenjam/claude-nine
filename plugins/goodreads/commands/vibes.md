---
description: Find similar books in your library based on genre, author, or themes
---

You are helping the user find books similar to one they specify.

## Task

When the user asks to find books with similar "vibes" or similar to a specific book:

1. Ask them what book they want to find similar books to (if not already specified)
2. Use the `analyze-goodreads-export` skill to search for that book in their library
3. Find similar books based on:
   - Same author
   - Books on the same custom shelves (genre indicators)
   - Similar series (if applicable)
   - Similar page count
   - Similar ratings

## Implementation

Write a Python script using goodreads_lib:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '__SKILL_DIR__/scripts')
from goodreads_lib import GoodreadsLibrary

lib = GoodreadsLibrary()

# Get the reference book (user should specify)
search_term = "BOOK_TITLE"  # Replace with user's input

# Find the book
matches = [b for b in lib.books if search_term.lower() in b.title.lower()]

if not matches:
    print(f"Could not find '{search_term}' in your library")
    sys.exit(1)

ref_book = matches[0]

print(f"\n# BOOKS SIMILAR TO: {ref_book.title}\n")

# Find similar books
similar = []

# 1. Same author
if ref_book.author:
    same_author = [b for b in lib.books
                   if b.author == ref_book.author
                   and b.book_id != ref_book.book_id
                   and not b.is_read]
    if same_author:
        print(f"## 📚 More by {ref_book.author}\n")
        for book in same_author[:3]:
            pages = f"{book.num_pages} pages" if book.num_pages else "? pages"
            rating = f"{book.average_rating:.2f}/5" if book.average_rating else "N/A"
            print(f"- **{book.title}** | {pages} | ⭐ {rating}")
        print()

# 2. Same shelves (genre indicators)
if ref_book.bookshelves:
    shelves = ref_book.bookshelves.split(',')
    for shelf in shelves[:2]:  # Check first 2 shelves
        shelf = shelf.strip()
        if shelf:
            same_shelf = [b for b in lib.books
                         if shelf in b.bookshelves
                         and b.book_id != ref_book.book_id
                         and not b.is_read]
            if same_shelf:
                print(f"## 🏷️ Similar (from '{shelf}' shelf)\n")
                for book in same_shelf[:3]:
                    pages = f"{book.num_pages} pages" if book.num_pages else "? pages"
                    rating = f"{book.average_rating:.2f}/5" if book.average_rating else "N/A"
                    print(f"- **{book.title}** by {book.author} | {pages} | ⭐ {rating}")
                print()

# 3. Similar series (if in a series)
if ref_book.series:
    series_books = lib.get_series_books(ref_book.series)
    unread_in_series = [b for b in series_books if not b.is_read]
    if unread_in_series:
        print(f"## 📖 More in {ref_book.series}\n")
        for book in unread_in_series[:3]:
            idx = f"#{book.series_index}" if book.series_index else ""
            pages = f"{book.num_pages} pages" if book.num_pages else "? pages"
            rating = f"{book.average_rating:.2f}/5" if book.average_rating else "N/A"
            print(f"- **{book.title}** {idx} | {pages} | ⭐ {rating}")
        print()
```

## Output Format

```
# BOOKS SIMILAR TO: Reference Book Title

## 📚 More by Author Name

- **Book Title** | XXX pages | ⭐ X.XX/5
- **Book Title** | XXX pages | ⭐ X.XX/5

## 🏷️ Similar (from 'genre' shelf)

- **Book Title** by Author | XXX pages | ⭐ X.XX/5
- **Book Title** by Author | XXX pages | ⭐ X.XX/5

## 📖 More in Series Name

- **Book Title** #X | XXX pages | ⭐ X.XX/5
```

## Important Notes

- Ask the user which book they want to find similar books to
- Search is case-insensitive for the title
- Prioritize unread books in results
- Custom shelves can indicate genres (e.g., "mental-health", "favorites")
- Limit results to 3 per category for readability
- Handle missing data gracefully
- Use the Bash tool to run your Python script
- Replace `__SKILL_DIR__` with the actual skill directory path
- Replace `BOOK_TITLE` with the user's search term
