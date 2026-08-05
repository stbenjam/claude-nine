# Reading statistics

Use the selected backend's read-only helpers to calculate:

- books and pages read this year and in the last 30 and 90 days;
- monthly reading velocity for the current year;
- average, longest, and shortest book length;
- personal and source rating averages and distributions;
- most-read authors and series, including series versus standalone counts; and
- unread/TBR count, pages, average rating, oldest entry, and recent additions.

Use the source's date and rating fields, skip records with missing required
values rather than failing, and report the number skipped. Return a structured
report with rounded averages, readable totals, and a few evidence-based
insights. Do not compare Calibre and Goodreads totals unless the user asks for
that comparison and the two data sets are known to represent the same library.
