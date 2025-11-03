# Available Plugins

This document lists all available Claude Code plugins and their commands in the ai-helpers repository.

- [Books](#books-plugin)
- [Git](#git-plugin)
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

### Git Plugin

Git workflow automation and utilities

**Commands:**
- **`/git:review-queue` `[org/repo]`** - Generate a report of PRs needing reviews

See [plugins/git/README.md](plugins/git/README.md) for detailed documentation.

### Pr Automation Plugin

Automate PR workflow approvals and ok-to-test comments

**Commands:**
- **`/pr-automation:approve-workflows` `<repo-owner/repo-name>`** - Approve pending GitHub Actions workflows and add /ok-to-test comments to PRs

See [plugins/pr-automation/README.md](plugins/pr-automation/README.md) for detailed documentation.
