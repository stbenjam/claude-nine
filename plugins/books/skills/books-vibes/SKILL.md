---
name: books-vibes
description: Find books with similar authors, series, themes, shelves, length, or ratings in a Calibre library or Goodreads export.
user-invocable: true
---

# Find similar books

Ask for a reference title when it is missing. Read
`../books-book-library/SKILL.md` to choose the authoritative backend, then
read `../books-book-library/references/similarity.md`.

Find unread matches in descending confidence: same author, same or related
series, shared tags or Goodreads shelves, similar page count, and similar
rating. Search the selected library first and distinguish matches already in
the user's library from outside community recommendations. Use web search for
community suggestions only when useful and label those suggestions clearly.

For every recommendation, explain the evidence for the match and be
transparent about limited metadata. Exclude archived Calibre books and
non-TBR Goodreads books unless the user requests a broader search.
