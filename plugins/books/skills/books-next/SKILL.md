---
name: books-next
description: Analyze reading patterns and recommend what to read next from a Calibre library or Goodreads export.
user-invocable: true
---

# Recommend what to read next

Read `../books-library/SKILL.md` first to choose the authoritative backend,
then read `../books-library/references/recommendations.md`.

Analyze the last 15 books read in the selected library, using the backend's
actual reading-date field. Look for series continuity, recent page-count
fatigue, recently added books, older forgotten books, and highly rated TBR
books. Exclude archived Calibre books and keep Goodreads recommendations on
the TBR unless the user asks for a broader pool.

Return a concise reading-pattern summary followed by one to three suggestions
in each useful category: series continuity, recently added, forgotten gems,
quick reads, and highly rated books. Include the evidence behind each choice
and say when a category has no matches.
