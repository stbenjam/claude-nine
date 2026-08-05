# Incomplete series

Use the selected backend's series helper rather than writing an ad hoc parser.
Find series with at least one read book and at least one unread book, sort by
series name, and identify the first unread book in series order.

For Calibre, use the bundled `books-find-incomplete-series` skill and its
`series.py` helper. For Goodreads, use `GoodreadsLibrary.get_incomplete_series()` from the
bundled `goodreads_lib` helper.

Report the series read/total count and the next title, author, series index,
page count, and rating when available. State when no incomplete series are
found and do not infer a series order when the source lacks an index.
