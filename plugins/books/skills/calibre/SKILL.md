---
name: calibre
description: Search and query Calibre library databases. Use when the user asks about books, TBR (to-be-read), reading lists, Calibre library queries, book searches, or mentions Calibre. Also use for queries about book ratings, authors, reading status, or library statistics.
---

# Calibre Library Search Skill

You are helping the user search and query their Calibre library.

## Library Location

**Library Path**: `"/Users/stbenjam/Drive/Calibre Library"`

**IMPORTANT**: The directory name contains spaces and MUST be quoted in all commands.

## Database Access

- **Database**: `metadata.db` located in the library directory
- **Tool**: Use `sqlite3` command-line utility
- **Access Mode**: ALWAYS use read-only access to prevent accidental modifications

**Why Read-Only**: Using `calibredb` with containers risks database migration/upgrades if the version differs from the user's main Calibre installation. Direct SQLite access avoids this risk.

## Custom Fields Mapping

The Calibre library has these custom columns (from `custom_columns` table):

| ID | Label      | Name            | Column Table      | Values    |
|----|------------|-----------------|-------------------|-----------|
| 1  | read       | Read            | custom_column_1   | 0 or 1    |
| 2  | priority   | Priority        | custom_column_2   | (varies)  |
| 3  | goodreads  | Goodreads Rating| custom_column_3   | 0-5       |
| 4  | archived   | Archived        | custom_column_4   | 0 or 1    |
| 5  | pages      | Page count      | custom_column_5   | (integer) |
| 6  | words      | Word Count      | custom_column_6   | (integer) |

**Note**: Boolean fields (read, archived) use 0 for No/False and 1 for Yes/True.

## SQLite Query Pattern

Always use this pattern to query the database:

```bash
sqlite3 -header -column "/Users/stbenjam/Drive/Calibre Library/metadata.db" "YOUR SQL QUERY"
```

Options:
- `-header`: Include column headers in output
- `-column`: Format output in columns (better readability)

## Database Schema Overview

Key tables:
- `books` - Main book records (id, title, sort, timestamp, etc.)
- `authors` - Author records (id, name, sort)
- `books_authors_link` - Many-to-many relationship between books and authors
- `custom_column_N` - Custom field data where N is the custom column ID
- `tags` - Tag records
- `books_tags_link` - Many-to-many relationship between books and tags

## Common Queries

### To-Be-Read List
Get books that are not archived and not read:

```bash
sqlite3 -header -column "/Users/stbenjam/Drive/Calibre Library/metadata.db" "
SELECT b.title as Title,
       a.name as Author,
       c3.value as Rating,
       c5.value as Pages
FROM books b
LEFT JOIN books_authors_link bal ON b.id = bal.book
LEFT JOIN authors a ON bal.author = a.id
LEFT JOIN custom_column_1 c1 ON b.id = c1.book
LEFT JOIN custom_column_3 c3 ON b.id = c3.book
LEFT JOIN custom_column_4 c4 ON b.id = c4.book
LEFT JOIN custom_column_5 c5 ON b.id = c5.book
WHERE (c1.value = 0 OR c1.value IS NULL)
  AND (c4.value = 0 OR c4.value IS NULL)
ORDER BY b.title;
"
```

### Search by Title or Author

```bash
sqlite3 -header -column "/Users/stbenjam/Drive/Calibre Library/metadata.db" "
SELECT b.title as Title,
       a.name as Author,
       c3.value as Rating,
       c5.value as Pages,
       CASE WHEN c1.value = 1 THEN 'Yes' ELSE 'No' END as Read,
       CASE WHEN c4.value = 1 THEN 'Yes' ELSE 'No' END as Archived
FROM books b
LEFT JOIN books_authors_link bal ON b.id = bal.book
LEFT JOIN authors a ON bal.author = a.id
LEFT JOIN custom_column_1 c1 ON b.id = c1.book
LEFT JOIN custom_column_3 c3 ON b.id = c3.book
LEFT JOIN custom_column_4 c4 ON b.id = c4.book
LEFT JOIN custom_column_5 c5 ON b.id = c5.book
WHERE b.title LIKE '%SEARCH_TERM%'
   OR a.name LIKE '%SEARCH_TERM%'
ORDER BY b.title;
"
```

### Highly Rated Unread Books

```bash
sqlite3 -header -column "/Users/stbenjam/Drive/Calibre Library/metadata.db" "
SELECT b.title as Title,
       a.name as Author,
       c3.value as Rating,
       c5.value as Pages
FROM books b
LEFT JOIN books_authors_link bal ON b.id = bal.book
LEFT JOIN authors a ON bal.author = a.id
LEFT JOIN custom_column_1 c1 ON b.id = c1.book
LEFT JOIN custom_column_3 c3 ON b.id = c3.book
LEFT JOIN custom_column_5 c5 ON b.id = c5.book
WHERE (c1.value = 0 OR c1.value IS NULL)
  AND c3.value >= 4
ORDER BY c3.value DESC, b.title;
"
```

### Books by Specific Author

```bash
sqlite3 -header -column "/Users/stbenjam/Drive/Calibre Library/metadata.db" "
SELECT b.title as Title,
       a.name as Author,
       c3.value as Rating,
       c5.value as Pages,
       CASE WHEN c1.value = 1 THEN 'Yes' ELSE 'No' END as Read
FROM books b
LEFT JOIN books_authors_link bal ON b.id = bal.book
LEFT JOIN authors a ON bal.author = a.id
LEFT JOIN custom_column_1 c1 ON b.id = c1.book
LEFT JOIN custom_column_3 c3 ON b.id = c3.book
LEFT JOIN custom_column_5 c5 ON b.id = c5.book
WHERE a.name LIKE '%AUTHOR_NAME%'
ORDER BY b.title;
"
```

### Count Books by Status

```bash
sqlite3 -header -column "/Users/stbenjam/Drive/Calibre Library/metadata.db" "
SELECT
  COUNT(*) as Total,
  SUM(CASE WHEN c1.value = 1 THEN 1 ELSE 0 END) as Read,
  SUM(CASE WHEN c1.value = 0 OR c1.value IS NULL THEN 1 ELSE 0 END) as Unread,
  SUM(CASE WHEN c4.value = 1 THEN 1 ELSE 0 END) as Archived
FROM books b
LEFT JOIN custom_column_1 c1 ON b.id = c1.book
LEFT JOIN custom_column_4 c4 ON b.id = c4.book;
"
```

## Usage Instructions

When the user asks to search their Calibre library:

1. Determine what they're looking for (to-be-read, specific book, by rating, etc.)
2. Construct the appropriate SQL query based on the examples above
3. **Always quote the library path** due to spaces in the directory name
4. Execute the query using the Bash tool with `sqlite3`
5. Present the results in a readable format

## Query Tips

- Use `LIKE '%term%'` for case-insensitive substring matching
- Use `IS NULL` checks for custom fields that may not be set
- Use `CASE` statements to convert boolean 0/1 values to Yes/No for readability
- Join `custom_column_N` tables using `LEFT JOIN` to include books without custom field values
- The `books_authors_link` table may have multiple entries per book (multiple authors)

## Examples

**User**: "Show me my to-be-read list"
→ Query books where read=0/NULL and archived=0/NULL

**User**: "Find books by Sanderson"
→ Query with `WHERE a.name LIKE '%Sanderson%'`

**User**: "Show highly rated unread books"
→ Query with `WHERE c1.value = 0 AND c3.value >= 4`

**User**: "How many books do I have?"
→ Use count query to show total, read, unread, and archived counts

## Safety Notes

- SQLite read operations are always safe
- Never use `UPDATE`, `INSERT`, `DELETE`, or `ALTER` statements
- If the user asks to modify data, politely decline and suggest they use Calibre GUI
- The database is accessed directly without locking concerns since we're read-only
