# Random selection

Use the selected backend to load the complete selection pool before choosing.
The default is non-archived Calibre TBR books or Goodreads books where
`is_tbr` is true. Honor explicit filters for author, series, genre, page count,
rating, unread books, or the entire library.

Choose uniformly at random. Report the selected title and author, relevant
series and rating metadata, the pool size, and the pool definition. Use `N/A`
for missing fields, state clearly when the pool is empty, and do not claim
randomness if the backend query failed.
