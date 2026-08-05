---
name: books-stats
description: Show reading statistics from a Calibre library or Goodreads export, including pace, pages, ratings, authors, series, and TBR.
user-invocable: true
---

# Show reading statistics

Read `../books-book-library/SKILL.md` first to choose the authoritative
backend, then read `../books-book-library/references/statistics.md`.

Calculate reading velocity for the current year and the last 30 and 90 days,
monthly pace, total and average pages, longest and shortest books, personal
and source-rating distributions, most-read authors, series versus standalone
counts, and TBR size, pages, ratings, age, and recent additions. Use the
selected backend's date, rating, read, archive, and TBR fields rather than
assuming Calibre and Goodreads schemas are interchangeable.

Return a structured report with readable totals, rounded averages, a monthly
breakdown, and a few evidence-based insights. Skip records missing required
values, report how many were skipped, and do not compare the two backends
unless the user explicitly asks and they represent the same library.
