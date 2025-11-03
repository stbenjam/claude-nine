#!/usr/bin/env python3
"""Library for parsing and querying Goodreads CSV exports."""

import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Callable
import re


class GoodreadsBook:
    """Represents a book from Goodreads CSV export."""

    def __init__(self, row: Dict[str, str]):
        self.book_id = row.get('Book Id', '')
        self.title = row.get('Title', '')
        self.author = row.get('Author', '')
        self.author_lf = row.get('Author l-f', '')
        self.additional_authors = row.get('Additional Authors', '')
        self.isbn = self._clean_isbn(row.get('ISBN', ''))
        self.isbn13 = self._clean_isbn(row.get('ISBN13', ''))
        self.my_rating = self._parse_int(row.get('My Rating', ''))
        self.average_rating = self._parse_float(row.get('Average Rating', ''))
        self.publisher = row.get('Publisher', '')
        self.binding = row.get('Binding', '')
        self.num_pages = self._parse_int(row.get('Number of Pages', ''))
        self.year_published = self._parse_int(row.get('Year Published', ''))
        self.original_publication_year = self._parse_int(row.get('Original Publication Year', ''))
        self.date_read = self._parse_date(row.get('Date Read', ''))
        self.date_added = self._parse_date(row.get('Date Added', ''))
        self.bookshelves = row.get('Bookshelves', '')
        self.bookshelves_with_positions = row.get('Bookshelves with positions', '')
        self.exclusive_shelf = row.get('Exclusive Shelf', '')
        self.my_review = row.get('My Review', '')
        self.spoiler = row.get('Spoiler', '')
        self.private_notes = row.get('Private Notes', '')
        self.read_count = self._parse_int(row.get('Read Count', ''))
        self.owned_copies = self._parse_int(row.get('Owned Copies', ''))

        # Parse series information from title
        self.series, self.series_index = self._parse_series()

    def _clean_isbn(self, isbn: str) -> str:
        """Remove Excel formatting from ISBN."""
        if isbn.startswith('="') and isbn.endswith('"'):
            return isbn[2:-1]
        return isbn

    def _parse_int(self, value: str) -> Optional[int]:
        """Parse integer value, return None if empty or invalid."""
        if not value or value == '':
            return None
        try:
            return int(value)
        except ValueError:
            return None

    def _parse_float(self, value: str) -> Optional[float]:
        """Parse float value, return None if empty or invalid."""
        if not value or value == '':
            return None
        try:
            return float(value)
        except ValueError:
            return None

    def _parse_date(self, value: str) -> Optional[datetime]:
        """Parse date in YYYY/MM/DD format."""
        if not value or value == '':
            return None
        try:
            return datetime.strptime(value, '%Y/%m/%d')
        except ValueError:
            return None

    def _parse_series(self) -> tuple[Optional[str], Optional[float]]:
        """Extract series name and number from title.

        Examples:
        - "An Absolutely Remarkable Thing (The Carls, #1)" -> ("The Carls", 1.0)
        - "The Three-Body Problem (Remembrance of Earth's Past, #1)" -> ("Remembrance of Earth's Past", 1.0)
        """
        # Match pattern: (Series Name, #Number)
        match = re.search(r'\(([^,]+),\s*#([\d.]+)\)$', self.title)
        if match:
            series_name = match.group(1).strip()
            try:
                series_index = float(match.group(2))
                return series_name, series_index
            except ValueError:
                return series_name, None
        return None, None

    @property
    def is_read(self) -> bool:
        """Check if book has been read."""
        return self.date_read is not None

    @property
    def is_tbr(self) -> bool:
        """Check if book is in to-be-read list."""
        return 'to-read' in self.exclusive_shelf

    @property
    def is_currently_reading(self) -> bool:
        """Check if currently reading."""
        return 'currently-reading' in self.exclusive_shelf

    def has_shelf(self, shelf_name: str) -> bool:
        """Check if book is on a specific shelf."""
        return shelf_name in self.bookshelves or shelf_name in self.exclusive_shelf

    def __repr__(self):
        return f"<GoodreadsBook: {self.title} by {self.author}>"


class GoodreadsLibrary:
    """Main class for querying Goodreads library from CSV."""

    def __init__(self, csv_path: Optional[str] = None):
        """Initialize library from CSV file.

        Args:
            csv_path: Path to goodreads_library_export.csv
                     Defaults to ~/Drive/Claude/books/goodreads_library_export.csv
        """
        if csv_path is None:
            csv_path = os.path.expanduser('~/Drive/Claude/books/goodreads_library_export.csv')

        self.csv_path = csv_path
        self.books: List[GoodreadsBook] = []
        self._load_books()

    def _load_books(self):
        """Load books from CSV file."""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.books.append(GoodreadsBook(row))

    def query(self, filter_func: Callable[[GoodreadsBook], bool]) -> List[GoodreadsBook]:
        """Query books with a custom filter function."""
        return [book for book in self.books if filter_func(book)]

    def get_read_books(self, limit: Optional[int] = None,
                       sort_by_date: bool = True) -> List[GoodreadsBook]:
        """Get all read books, optionally sorted by date read."""
        books = [book for book in self.books if book.is_read]
        if sort_by_date:
            books.sort(key=lambda b: b.date_read or datetime.min, reverse=True)
        if limit:
            books = books[:limit]
        return books

    def get_tbr_books(self) -> List[GoodreadsBook]:
        """Get all to-be-read books."""
        return [book for book in self.books if book.is_tbr]

    def get_books_by_shelf(self, shelf_name: str) -> List[GoodreadsBook]:
        """Get all books on a specific shelf."""
        return [book for book in self.books if book.has_shelf(shelf_name)]

    def get_books_read_in_period(self, days: int) -> List[GoodreadsBook]:
        """Get books read in the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        return [book for book in self.books
                if book.date_read and book.date_read >= cutoff]

    def get_books_read_in_year(self, year: int) -> List[GoodreadsBook]:
        """Get books read in a specific year."""
        return [book for book in self.books
                if book.date_read and book.date_read.year == year]

    def get_books_added_in_period(self, days: int) -> List[GoodreadsBook]:
        """Get books added to library in the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        return [book for book in self.books
                if book.date_added and book.date_added >= cutoff]

    def get_series_books(self, series_name: str) -> List[GoodreadsBook]:
        """Get all books in a series, sorted by series index."""
        books = [book for book in self.books if book.series == series_name]
        books.sort(key=lambda b: b.series_index or 0)
        return books

    def get_all_series(self) -> Dict[str, List[GoodreadsBook]]:
        """Get all series with their books."""
        series_dict = {}
        for book in self.books:
            if book.series:
                if book.series not in series_dict:
                    series_dict[book.series] = []
                series_dict[book.series].append(book)

        # Sort books within each series
        for series in series_dict:
            series_dict[series].sort(key=lambda b: b.series_index or 0)

        return series_dict

    def get_incomplete_series(self) -> Dict[str, Dict]:
        """Get series where at least one book is read but not all."""
        all_series = self.get_all_series()
        incomplete = {}

        for series_name, books in all_series.items():
            read_count = sum(1 for b in books if b.is_read)
            total_count = len(books)

            if read_count > 0 and read_count < total_count:
                # Find next unread book
                next_unread = None
                for book in books:
                    if not book.is_read:
                        next_unread = book
                        break

                incomplete[series_name] = {
                    'books': books,
                    'read_count': read_count,
                    'total_count': total_count,
                    'next_book': next_unread
                }

        return incomplete

    def get_author_stats(self) -> List[tuple[str, int]]:
        """Get author statistics (author, book count) sorted by count."""
        author_counts = {}
        for book in self.books:
            if book.is_read:
                author_counts[book.author] = author_counts.get(book.author, 0) + 1

        return sorted(author_counts.items(), key=lambda x: x[1], reverse=True)

    def get_rating_distribution(self) -> Dict[int, int]:
        """Get distribution of user ratings."""
        dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for book in self.books:
            if book.is_read and book.my_rating:
                dist[book.my_rating] = dist.get(book.my_rating, 0) + 1
        return dist
