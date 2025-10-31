# Available Plugins

This document lists all available Claude Code plugins and their commands in the ai-helpers repository.

- [Git](#git-plugin)
- [Potato](#potato-plugin)
- [Pr Automation](#pr-automation-plugin)

### Git Plugin

Git workflow automation and utilities

**Commands:**
- **`/git:review-queue` `[org/repo]`** - Generate a report of PRs needing reviews

See [plugins/git/README.md](plugins/git/README.md) for detailed documentation.

### Potato Plugin

TODO: Add description

**Commands:**
- **`/potato:example`** - Example command

See [plugins/potato/README.md](plugins/potato/README.md) for detailed documentation.

### Pr Automation Plugin

Automate PR workflow approvals and ok-to-test comments

**Commands:**
- **`/pr-automation:approve-workflows` `<repo-owner/repo-name>`** - Approve pending GitHub Actions workflows and add /ok-to-test comments to PRs

See [plugins/pr-automation/README.md](plugins/pr-automation/README.md) for detailed documentation.
