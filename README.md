# claude-nine

[![skillsaw grade](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fstbenjam%2Fclaude-nine%2Fmain%2F.skillsaw-badge.json)](https://skillsaw.org/)

Shared skills and plugins for Claude Code and Codex by stbenjam.

## Installation

Add the Claude marketplace:

```
/plugin marketplace add stbenjam/claude-nine
```

Add the Codex marketplace:

```
codex plugin marketplace add stbenjam/claude-nine
```

The repository has one Codex-compatible plugin catalog at
`.agents/plugins/marketplace.json`. Claude Code continues to use
`.claude-plugin/marketplace.json`; both catalogs point at the same plugin
directories and skills.

## Plugins

- **books**: Unified Calibre and Goodreads library search, recommendations, series analysis, and statistics
- **calendar**: macOS Calendar integration via icalBuddy and AppleScript
- **finances**: Manage HSA receipts and financial documents
- **git**: Git and GitHub workflows, including the pull-request review queue
- **loops**: Autonomous workflows that shepherd work to completion, such as driving a pull request to a mergeable state
- **reviews**: Multi-agent panel code review with specialist reviewers and runtime reproducers

The books plugin uses progressive disclosure: it identifies whether a request
belongs to Calibre or Goodreads, then loads only the matching backend and
workflow reference.

## Development

Lint plugins and skills with [skillsaw](https://skillsaw.org/) in strict mode:

```bash
make lint
```

Apply autofixes or regenerate the static catalog documentation with:

```bash
make lint-fix
make docs
```

## License

MIT
