# Available Plugins

This document lists all available Claude Code plugins and their commands in the ai-helpers repository.

- [Books](#books-plugin)
- [Calendar](#calendar-plugin)
- [Cc 10113 Reproducer](#cc-10113-reproducer-plugin)
- [Git](#git-plugin)
- [Goodreads](#goodreads-plugin)
- [Pr Automation](#pr-automation-plugin)

### Books Plugin

TODO: Add description

**Commands:**
- **`/books:next`** - Analyze my reading patterns and suggest what to read next from my TBR
- **`/books:random`** - Pick a random book from TBR or library
- **`/books:series`** - List unfinished series and the next book to read in each
- **`/books:stats`** - Show reading statistics (books per year/month, pages read, average rating, genre breakdown)
- **`/books:vibes`** - Find similar books in your library based on genre, author, or themes

See [plugins/books/README.md](plugins/books/README.md) for detailed documentation.

### Calendar Plugin

macOS Calendar integration via icalBuddy and AppleScript

**Commands:**
- **`/calendar:create`** - Create a new calendar event
- **`/calendar:today`** - Show today's calendar events
- **`/calendar:tomorrow`** - Show tomorrow's calendar events
- **`/calendar:week`** - Show this week's calendar events

See [plugins/calendar/README.md](plugins/calendar/README.md) for detailed documentation.

### Cc 10113 Reproducer Plugin

TODO: Add description

**Commands:**
- **`/cc-10113-reproducer:example`** - Runs an example check

See [plugins/cc-10113-reproducer/README.md](plugins/cc-10113-reproducer/README.md) for detailed documentation.

### Git Plugin

Git workflow automation and utilities

**Commands:**
- **`/git:review-queue` `[org/repo]`** - Generate a report of PRs needing reviews

See [plugins/git/README.md](plugins/git/README.md) for detailed documentation.

### Goodreads Plugin

TODO: Add description

**Commands:**
- **`/goodreads:next`** - Analyze my reading patterns and suggest what to read next from my TBR
- **`/goodreads:random`** - Pick a random book from TBR or library
- **`/goodreads:series`** - List unfinished series and the next book to read in each
- **`/goodreads:stats`** - Show reading statistics (books per year/month, pages read, average rating, genre breakdown)
- **`/goodreads:vibes`** - Find similar books in your library based on genre, author, or themes

See [plugins/goodreads/README.md](plugins/goodreads/README.md) for detailed documentation.

### Pr Automation Plugin

Automate PR workflow approvals and ok-to-test comments

**Commands:**
- **`/pr-automation:approve-workflows` `<repo-owner/repo-name>`** - Approve pending GitHub Actions workflows and add /ok-to-test comments to PRs

See [plugins/pr-automation/README.md](plugins/pr-automation/README.md) for detailed documentation.
