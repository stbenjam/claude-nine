# books

Search and analyze a book library from either Calibre or a Goodreads CSV
export. The plugin is shared by Claude Code and Codex.

See the [main installation guide](../../README.md#installation) for Claude
Code, Codex, and standalone Agent Skills setup.

## Skill routing

The invocable skills `/books:books-next`, `/books:books-random`,
`/books:books-series`, `/books:books-stats`, and `/books:books-vibes` are
available directly. Each one starts with the `books-book-library` router, asks
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
