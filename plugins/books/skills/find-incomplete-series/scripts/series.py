#!/usr/bin/env python3
import subprocess
import json
from collections import defaultdict

# Query Calibre for all books in series
result = subprocess.run([
    '/Applications/calibre.app/Contents/MacOS/calibredb', 'list',
    '--with-library=http://killington.home.bitbin.de:8454/#',
    '--username=calibre',
    '--password=calibre',
    '--fields=title,authors,series,series_index,*read,*archived',
    '--search=series:true',
    '--for-machine'
], capture_output=True, text=True)

books = json.loads(result.stdout)

# Group books by series, excluding archived books
series_dict = defaultdict(list)
for book in books:
    if book.get('series') and not book.get('*archived'):
        series_dict[book['series']].append(book)

# Sort books in each series by series_index
for series in series_dict:
    series_dict[series].sort(key=lambda x: float(x.get('series_index', 0)))

# Find series with at least one read book but not all read
incomplete_series = []
for series, books_list in series_dict.items():
    read_count = sum(1 for b in books_list if b.get('*read') == True)
    total_count = len(books_list)

    if read_count > 0 and read_count < total_count:
        # Find the next unread book
        next_unread = None
        for book in books_list:
            if not book.get('*read'):
                next_unread = book
                break

        incomplete_series.append({
            'series': series,
            'read': read_count,
            'total': total_count,
            'next_book': next_unread
        })

# Sort by series name
incomplete_series.sort(key=lambda x: x['series'])

# Output results
print(f"\n# UNFINISHED SERIES\n")
print(f"You have {len(incomplete_series)} incomplete series:\n")

for i, s in enumerate(incomplete_series, 1):
    print(f"{i}. **{s['series']}** ({s['read']}/{s['total']} books read)")
    if s['next_book']:
        authors = s['next_book'].get('authors', 'Unknown')
        title = s['next_book'].get('title', 'Unknown')
        index = s['next_book'].get('series_index', 0)
        print(f"   Next: **{title}** by {authors} (Book #{index})\n")
    else:
        print(f"   Next: Unable to determine\n")
