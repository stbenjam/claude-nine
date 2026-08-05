---
name: books-analyze-goodreads-export
description: Load and query a Goodreads CSV export as the Goodreads backend for the books-library skill.
user-invocable: false
---

# Goodreads backend

Use the bundled [`scripts/goodreads_lib.py`](scripts/goodreads_lib.py) helper; do not write a second CSV
parser. If the export path is not supplied, look for
`goodreads_library_export.csv` or ask the user where it is.

The helper exposes `GoodreadsLibrary` and `GoodreadsBook`, including:

- `get_read_books`, `get_tbr_books`, `get_books_by_shelf`;
- `get_books_read_in_period`, `get_books_read_in_year`, and
  `get_books_added_in_period`;
- `get_series_books`, `get_all_series`, and `get_incomplete_series`; and
- `get_author_stats`, `get_rating_distribution`, and `query`.

Important fields include `title`, `author`, `series`, `series_index`,
`my_rating`, `average_rating`, `num_pages`, `date_read`, `date_added`,
`exclusive_shelf`, `bookshelves`, `is_read`, and `is_tbr`.

Use the helper's typed properties and handle missing optional values with
defaults. The export is read-only. When running a small analysis script, add
the directory containing this skill's `scripts/` directory to `sys.path`
than guessing a separate parser or library location.
