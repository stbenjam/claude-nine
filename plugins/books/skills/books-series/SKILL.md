---
name: books-series
description: List unfinished book series and the next unread book from a Calibre library or Goodreads export.
user-invocable: true
---

# Find unfinished series

Read `../books-library/SKILL.md` first to choose the authoritative backend,
then read `../books-library/references/series.md`.

Find series with at least one read book and at least one unread book. Use the
selected backend's helper rather than writing an ad hoc parser: the Calibre
`books-find-incomplete-series` skill and the Goodreads `GoodreadsLibrary`
helper.
Sort series by name and identify the first unread book in series order only
when the source provides a usable series index.

Report each series' read/total count and next title, author, series index,
page count, and rating when available. State when no unfinished series are
found and label unknown fields instead of guessing.
