#!/usr/bin/env python3
"""Library for parsing and querying Goodreads CSV exports."""

import csv
import os
import re
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional


class GoodreadsBook:
    """Represents a book from a Goodreads CSV export."""

    def __init__(self, row: Dict[str, str]):
        self.book_id = row.get("Book Id", "")
        self.title = row.get("Title", "")
        self.author = row.get("Author", "")
        self.author_lf = row.get("Author l-f", "")
        self.additional_authors = row.get("Additional Authors", "")
        self.isbn = self._clean_isbn(row.get("ISBN", ""))
        self.isbn13 = self._clean_isbn(row.get("ISBN13", ""))
        self.my_rating = self._parse_int(row.get("My Rating", ""))
        self.average_rating = self._parse_float(row.get("Average Rating", ""))
        self.publisher = row.get("Publisher", "")
        self.binding = row.get("Binding", "")
        self.num_pages = self._parse_int(row.get("Number of Pages", ""))
        self.year_published = self._parse_int(row.get("Year Published", ""))
        self.original_publication_year = self._parse_int(
            row.get("Original Publication Year", "")
        )
        self.date_read = self._parse_date(row.get("Date Read", ""))
        self.date_added = self._parse_date(row.get("Date Added", ""))
        self.bookshelves = row.get("Bookshelves", "")
        self.bookshelves_with_positions = row.get("Bookshelves with positions", "")
        self.exclusive_shelf = row.get("Exclusive Shelf", "")
        self.my_review = row.get("My Review", "")
        self.spoiler = row.get("Spoiler", "")
        self.private_notes = row.get("Private Notes", "")
        self.read_count = self._parse_int(row.get("Read Count", ""))
        self.owned_copies = self._parse_int(row.get("Owned Copies", ""))
        self.series, self.series_index = self._parse_series()

    @staticmethod
    def _clean_isbn(isbn: str) -> str:
        if isbn.startswith('="') and isbn.endswith('"'):
            return isbn[2:-1]
        return isbn

    @staticmethod
    def _parse_int(value: str) -> Optional[int]:
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    @staticmethod
    def _parse_float(value: str) -> Optional[float]:
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def _parse_date(value: str) -> Optional[datetime]:
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y/%m/%d")
        except ValueError:
            return None

    def _parse_series(self) -> tuple[Optional[str], Optional[float]]:
        match = re.search(r"\(([^,]+),\s*#([\d.]+)\)$", self.title)
        if not match:
            return None, None
        series_name = match.group(1).strip()
        try:
            return series_name, float(match.group(2))
        except ValueError:
            return series_name, None

    @property
    def is_read(self) -> bool:
        return self.date_read is not None

    @property
    def is_tbr(self) -> bool:
        return "to-read" in self.exclusive_shelf

    @property
    def is_currently_reading(self) -> bool:
        return "currently-reading" in self.exclusive_shelf

    def has_shelf(self, shelf_name: str) -> bool:
        return shelf_name in self.bookshelves or shelf_name in self.exclusive_shelf

    def __repr__(self) -> str:
        return f"<GoodreadsBook: {self.title} by {self.author}>"


class GoodreadsLibrary:
    """Main class for querying a Goodreads CSV export."""

    def __init__(self, csv_path: Optional[str] = None):
        if csv_path is None:
            csv_path = os.path.expanduser(
                "~/Drive/Claude/books/goodreads_library_export.csv"
            )
        self.csv_path = csv_path
        self.books: List[GoodreadsBook] = []
        self._load_books()

    def _load_books(self) -> None:
        with open(self.csv_path, "r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                self.books.append(GoodreadsBook(row))

    def query(self, filter_func: Callable[[GoodreadsBook], bool]) -> List[GoodreadsBook]:
        return [book for book in self.books if filter_func(book)]

    def get_read_books(
        self, limit: Optional[int] = None, sort_by_date: bool = True
    ) -> List[GoodreadsBook]:
        books = [book for book in self.books if book.is_read]
        if sort_by_date:
            books.sort(key=lambda book: book.date_read or datetime.min, reverse=True)
        return books[:limit] if limit else books

    def get_tbr_books(self) -> List[GoodreadsBook]:
        return [book for book in self.books if book.is_tbr]

    def get_books_by_shelf(self, shelf_name: str) -> List[GoodreadsBook]:
        return [book for book in self.books if book.has_shelf(shelf_name)]

    def get_books_read_in_period(self, days: int) -> List[GoodreadsBook]:
        cutoff = datetime.now() - timedelta(days=days)
        return [
            book
            for book in self.books
            if book.date_read and book.date_read >= cutoff
        ]

    def get_books_read_in_year(self, year: int) -> List[GoodreadsBook]:
        return [
            book
            for book in self.books
            if book.date_read and book.date_read.year == year
        ]

    def get_books_added_in_period(self, days: int) -> List[GoodreadsBook]:
        cutoff = datetime.now() - timedelta(days=days)
        return [
            book
            for book in self.books
            if book.date_added and book.date_added >= cutoff
        ]

    def get_series_books(self, series_name: str) -> List[GoodreadsBook]:
        books = [book for book in self.books if book.series == series_name]
        books.sort(key=lambda book: book.series_index or 0)
        return books

    def get_all_series(self) -> Dict[str, List[GoodreadsBook]]:
        series: Dict[str, List[GoodreadsBook]] = {}
        for book in self.books:
            if book.series:
                series.setdefault(book.series, []).append(book)
        for books in series.values():
            books.sort(key=lambda book: book.series_index or 0)
        return series

    def get_incomplete_series(self) -> Dict[str, Dict]:
        incomplete: Dict[str, Dict] = {}
        for series_name, books in self.get_all_series().items():
            read_count = sum(book.is_read for book in books)
            if not read_count or read_count == len(books):
                continue
            next_book = next((book for book in books if not book.is_read), None)
            incomplete[series_name] = {
                "books": books,
                "read_count": read_count,
                "total_count": len(books),
                "next_book": next_book,
            }
        return incomplete

    def get_author_stats(self) -> List[tuple[str, int]]:
        counts: Dict[str, int] = {}
        for book in self.books:
            if book.is_read:
                counts[book.author] = counts.get(book.author, 0) + 1
        return sorted(counts.items(), key=lambda item: item[1], reverse=True)

    def get_rating_distribution(self) -> Dict[int, int]:
        distribution = {rating: 0 for rating in range(1, 6)}
        for book in self.books:
            if book.is_read and book.my_rating:
                distribution[book.my_rating] = distribution.get(book.my_rating, 0) + 1
        return distribution
