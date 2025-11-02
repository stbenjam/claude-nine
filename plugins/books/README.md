# books

A Claude Code plugin for managing and exploring your Calibre library. Query your reading list, get personalized recommendations, and track your reading patterns - all from the command line.

## Features

### Skills

#### `calibre` Skill

Search and query your Calibre library database using natural language:

- Search books by title, author, series, or rating
- Query your to-be-read (TBR) list
- Find books by custom fields (read status, date read, Goodreads ratings, page count)
- Get reading statistics and patterns
- Filter by highly-rated books, quick reads, or specific authors

**Usage:**
```
Ask Claude about your books, and the skill will automatically activate:
- "Show me my to-be-read list"
- "Find books by Brandon Sanderson"
- "What books did I read in October?"
- "Show me highly rated unread books under 300 pages"
```

### Commands

#### `/books:next`

Get personalized reading recommendations based on your reading patterns.

Analyzes:
- Recent reading history (last 15 books)
- Series continuity (suggests next books in series you're reading)
- Reading fatigue (balances long/short books)
- Book age in library (finds recently added and forgotten gems)
- Quality ratings (prioritizes highly-rated books)

**Usage:**
```
/books:next
```

Generates a categorized report with:
- 📚 Series continuity recommendations
- 🆕 Recently added books
- ⏰ Forgotten gems
- ⚡ Quick reads
- 🌟 Top-rated books

## Setup

### Prerequisites

1. **Calibre**: Install [Calibre](https://calibre-ebook.com/) desktop application
2. **Calibre Content Server**: The plugin connects to a Calibre Content Server instance

### Configuration

The plugin is configured to connect to a Calibre Content Server. Edit `skills/calibre/SKILL.md` to set:

- **Library URL**: Your Calibre Content Server URL
- **Authentication**: Username and password (if required)
- **calibredb Location**: Path to the `calibredb` command

**Current configuration:**
```
Library URL: http://killington.home.bitbin.de:8454/#
Username: calibre
Password: calibre
calibredb: /Applications/calibre.app/Contents/MacOS/calibredb
```

### Custom Fields

The plugin supports these custom Calibre fields:

| Field     | Search Name | Type     | Purpose                          |
|-----------|-------------|----------|----------------------------------|
| read      | #read       | Boolean  | Mark books as read/unread        |
| dateread  | #dateread   | Datetime | Track when you finished books    |
| archived  | #archived   | Boolean  | Archive books from TBR           |
| goodreads | #goodreads  | Float    | Goodreads rating (0.0-5.0)      |
| pages     | #pages      | Integer  | Page count                       |
| priority  | #priority   | Text     | Reading priority                 |
| words     | #words      | Integer  | Word count                       |

## Examples

### Query your library
```
"What books did I read in the last 30 days?"
"Show me unread books in the Mistborn series"
"Find highly rated books under 400 pages"
```

### Get recommendations
```
/books:next
```

Generates analysis like:
```
READING PATTERN SUMMARY
- Books read in last 30 days: 7
- Average page count: 461 pages
- Notable patterns: Completed Mistborn: Wax & Wayne series

SERIES CONTINUITY (TOP PRIORITY!)
- Fevered Star by Rebecca Roanhorse
  Series: Between Earth and Sky #2 | 401 pages | Rating: 4.08/5
```

## How It Works

The plugin uses `calibredb` to query your Calibre library via the Content Server API. It:

1. Fetches book metadata (title, author, series, ratings, custom fields)
2. Analyzes reading patterns using date-read and completion data
3. Generates intelligent recommendations based on multiple factors
4. Presents results in readable, categorized formats

All queries are read-only - the plugin never modifies your library.

## Troubleshooting

### Authentication errors
If you see "A username and password is required", update the credentials in `skills/calibre/SKILL.md`.

### Connection errors
Ensure your Calibre Content Server is running and accessible at the configured URL.

### Missing custom fields
If custom fields aren't working, verify they exist in your Calibre library with the exact names listed above.

## Version

**v0.0.1** - Initial release
