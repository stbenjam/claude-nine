---
name: books-random
description: Pick a random book from a Calibre library or Goodreads export, honoring the user's requested pool and filters.
user-invocable: true
---

# Pick a random book

Read `../books-library/SKILL.md` first to choose the authoritative backend,
then read `../books-library/references/random.md`.

Use the TBR as the default pool: non-archived unread Calibre books or
Goodreads books marked `is_tbr`. Honor explicit requests for the entire
library, all unread books, an author, series, shelf, genre, rating, page
range, or other filter. Load the complete matching pool and choose uniformly
at random; do not substitute a highest-rated or recently added book.

Report the title, author, useful series/page/rating/date metadata, pool size,
and pool definition. Use `N/A` for missing values, state clearly when the pool
is empty, and do not claim randomness if the backend query failed.
