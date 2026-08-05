# books

Search and analyze a book library from either Calibre or a Goodreads CSV
export. The plugin is shared by Claude Code and Codex.

See the [main installation guide](../../README.md#installation) for Claude
Code, Codex, and standalone Agent Skills setup.

## Skills

<!-- BEGIN GENERATED SKILLS -->
- [`books-acquirer`](skills/books-acquirer/SKILL.md) — Acquire named books via library borrow/hold/download first, then explicit retailer purchase; use for get, hold, borrow, buy, or EPUB requests.
- [`books-analyze-goodreads-export`](skills/books-analyze-goodreads-export/SKILL.md) — Load and query a Goodreads CSV export as the Goodreads backend for the books-library skill.
- [`books-calibre`](skills/books-calibre/SKILL.md) — Supporting Calibre backend for the books-library skill; use it after that skill selects Calibre as the data source.
- [`books-find-incomplete-series`](skills/books-find-incomplete-series/SKILL.md) — Find incomplete series in a Calibre library and identify the next book to read in each series.
- [`books-library`](skills/books-library/SKILL.md) — Search, analyze, and recommend books from either a Calibre library or a Goodreads CSV export.
- [`books-next`](skills/books-next/SKILL.md) — Analyze reading patterns and recommend what to read next from a Calibre library or Goodreads export.
- [`books-random`](skills/books-random/SKILL.md) — Pick a random book from a Calibre library or Goodreads export, honoring the user's requested pool and filters.
- [`books-release-scout`](skills/books-release-scout/SKILL.md) — Read-only new-release book recommendations from Calibre ratings with current library availability and retailer pricing; use for book scouting.
- [`books-series`](skills/books-series/SKILL.md) — List unfinished book series and the next unread book from a Calibre library or Goodreads export.
- [`books-stats`](skills/books-stats/SKILL.md) — Show reading statistics from a Calibre library or Goodreads export, including pace, pages, ratings, authors, series, and TBR.
- [`books-vibes`](skills/books-vibes/SKILL.md) — Find books with similar authors, series, themes, shelves, length, or ratings in a Calibre library or Goodreads export.
<!-- END GENERATED SKILLS -->

## Skill routing

The invocable skills `/books:books-next`, `/books:books-random`,
`/books:books-series`, `/books:books-stats`, and `/books:books-vibes` are
available directly. Each one starts with the `books-library` router, asks
which data source is authoritative
when the request does not make that clear, and loads only the matching backend
and operation reference. This keeps the initial context small while preserving
the detailed workflows for recommendations, random selections, series,
statistics, and similar books.

## Data sources

- **Calibre** uses the configured Content Server and the `calibredb` helper.
  See `skills/books-calibre/SKILL.md` for the URL, custom fields, and setup.
- **Goodreads** uses a read-only `goodreads_library_export.csv`. The bundled
  `goodreads_lib.py` helper parses the export and supports TBR, series, shelf,
  rating, and reading-history queries.

## Example requests

- “Show my non-archived Calibre TBR books under 300 pages.”
- “Which Goodreads series have I started but not finished?”
- “Recommend something from my Goodreads export based on my recent reads.”
- “Find books similar to this title in my Calibre library.”

The plugin keeps the two sources separate. When a request could be answered by
both, choose the source explicitly rather than combining unrelated exports.

## Discovery and acquisition

Two optional skills extend the library queries into new-release scouting and
acquisition. They drive a browser and, for holds/loans/purchases, external
accounts, so they are separate from the read-only query skills above.

- **books-release-scout** builds a taste profile from Calibre ratings, finds
  genuinely new releases that fit, and presents current library availability
  and retailer pricing. It is strictly read-only and takes no external action.
- **books-acquirer** acquires a specific verified book: library-first
  (borrow/hold/download and Calibre import) with an explicit, price-confirmed
  retailer purchase fallback. It requires your own persistent browser profiles
  and, for purchases, your own purchase/payment workflow.

Both expect you to point them at your own library systems, retailer accounts,
and Calibre import folder — nothing is hardcoded.
