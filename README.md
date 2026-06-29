# claude-nine

[![skillsaw grade](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fstbenjam%2Fclaude-nine%2Fmain%2F.skillsaw-badge.json)](https://skillsaw.org/)

Claude Code Plugins by stbenjam

## Installation

Add the marketplace to Claude Code:

```
/plugin marketplace add stbenjam/claude-nine
```

Install a specific plugin:

```
/plugin install books@claude-nine
```

## Plugins

- **books**: Query a Calibre library (TBR, series, stats, recommendations)
- **calendar**: macOS Calendar integration via icalBuddy and AppleScript
- **finances**: Manage HSA receipts and financial documents
- **git**: Git and GitHub workflows, including the PR review queue
- **goodreads**: Query a Goodreads CSV export
- **loops**: Autonomous loops that shepherd work to completion, such as driving a PR to a mergeable state
- **reviews**: Multi-agent panel code review with specialist reviewers and runtime reproducers

## Development

Lint plugins and skills with [skillsaw](https://skillsaw.org/) (strict mode):

```bash
make lint
```

Apply autofixes:

```bash
make lint-fix
```

## License

MIT
