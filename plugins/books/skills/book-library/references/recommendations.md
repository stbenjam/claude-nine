# Recommendations

Use the selected backend skill to inspect the user's recent reading history
and unread library. Build recommendations from several independent signals:

1. series continuity from recent reads;
2. reading fatigue, using recent page counts;
3. recently added books;
4. older unread books that may have been forgotten; and
5. high ratings balanced against length and series momentum.

For Calibre, use `*dateread`, `timestamp`, `#read`, `#archived`, `*pages`, and
`*goodreads`. For Goodreads, use `date_read`, `date_added`, `is_read`, `is_tbr`,
`num_pages`, `my_rating`, and `average_rating`.

Return a short reading-pattern summary followed by one to three books in each
useful category. Explain why each recommendation fits and never invent missing
metadata. Exclude archived Calibre books and non-TBR Goodreads books unless the
user explicitly asks for a broader pool.
