# stbenjam's skills

[![skillsaw grade](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fstbenjam%2Fskills%2Fmain%2F.skillsaw-badge.json)](https://skillsaw.org/)

Shared skills and plugins for Claude Code and Codex by stbenjam.

## Installation

Add the Claude marketplace:

```
/plugin marketplace add stbenjam/skills
```

Add the Codex marketplace:

```
codex plugin marketplace add stbenjam/skills
```

The repository has one Codex-compatible plugin catalog at
`.agents/plugins/marketplace.json`. Claude Code continues to use
`.claude-plugin/marketplace.json`; both catalogs point at the same plugin
directories and skills.

## Plugins

- **books**: Unified Calibre and Goodreads library search, recommendations, series analysis, and statistics
- **loops**: Autonomous workflows that shepherd work to completion, such as driving a pull request to a mergeable state
- **reviews**: Multi-agent panel code review with specialist reviewers and runtime reproducers
- **steering**: Compact skills for changing direction, explaining decisions, asking for clarity, tightening prose, executing decisively, and raising frontend quality

The books plugin uses progressive disclosure: it identifies whether a request
belongs to Calibre or Goodreads, then loads only the matching backend and
workflow reference.

The Books plugin provides these invocable skills:
`/books:next`, `/books:random`, `/books:series`, `/books:stats`, and
`/books:vibes`.

## Credits

The compact steering-skill pattern is inspired by [`bro` from dmmulroy/skills](https://github.com/dmmulroy/skills/blob/main/bro/SKILL.md).

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
