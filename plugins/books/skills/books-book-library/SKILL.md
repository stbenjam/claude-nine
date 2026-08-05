---
name: books-book-library
description: Search, analyze, and recommend books from either a Calibre library or a Goodreads CSV export.
user-invocable: true
---

# Book library workflow

This plugin supports two book-library backends. Use progressive disclosure so
the conversation only loads the instructions and data source it needs.

## Choose a backend first

1. Choose **Calibre** when the user mentions Calibre, `calibredb`, the content
   server, or the configured custom fields such as `#read` and `#archived`.
2. Choose **Goodreads** when the user mentions Goodreads, a Goodreads export,
   CSV, shelves, or fields such as `date_read` and `exclusive_shelf`.
3. If the request is ambiguous and both sources could answer it, ask which
   library to use. Do not silently query both or present one as authoritative.

After choosing, read only the matching backend skill:

- Calibre: `../books-calibre/SKILL.md`
- Goodreads: `../books-analyze-goodreads-export/SKILL.md`

## Choose an operation second

Read only the matching reference under `references/`:

- recommendations: `recommendations.md`
- random selection: `random.md`
- incomplete series: `series.md`
- reading statistics: `statistics.md`
- similar books: `similarity.md`

For a simple title, author, series, TBR, or shelf lookup, use the selected
backend skill directly without loading an operation reference.

Keep queries read-only unless the user explicitly requests a change, preserve
the selected backend's field semantics, and say when required metadata or the
library itself is unavailable.
