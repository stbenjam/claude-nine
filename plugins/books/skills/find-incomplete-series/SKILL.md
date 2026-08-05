---
name: find-incomplete-series
description: Find incomplete series in a Calibre library and identify the next book to read in each series.
user-invocable: false
---

This is a supporting workflow used by `book-library` for Calibre series
analysis. It finds series where at least one book is read but the series is not
complete.

Run the bundled helper from this skill directory:

```bash
python3 __SKILL_DIR__/scripts/series.py
```

The helper will:
1. Query your Calibre library for all books that are part of a series
2. Exclude archived books
3. Identify series where you've read at least one book but haven't finished the entire series
4. Display the next unread book in each incomplete series

Do not replace the helper with a hand-written query. Report its output clearly
and say when no incomplete series are found.
