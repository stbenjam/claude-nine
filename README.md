# stbenjam's skills

[![skillsaw grade](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fstbenjam%2Fskills%2Fmain%2F.skillsaw-badge.json)](https://skillsaw.org/)

Shared skills and plugins for Claude Code and Codex by stbenjam.

## Installation

Choose the setup that matches your agent host. All paths below start at the
root of a checkout of this repository.

### Claude Code

From a Claude Code session, add the marketplace and install the plugin you
want:

```
/plugin marketplace add stbenjam/skills
/plugin install steering@stbenjam
```

Replace `steering` with `books`, `loops`, or `reviews` as needed, then run
`/reload-plugins`.

### Codex

Add the marketplace from a shell, then open Codex's plugin browser:

```
codex plugin marketplace add stbenjam/skills
codex
/plugins
```

Select the plugin to install, then start a new Codex session. The repository's
Codex catalog is `.agents/plugins/marketplace.json`.

### Standalone Agent Skills

Copy any skill directory into `.agents/skills`:

```
mkdir -p .agents/skills
cp -R plugins/steering/skills/nah .agents/skills/
```

Replace `steering/skills/nah` with the plugin and skill you want; each copied
directory must contain its `SKILL.md` file.

Claude Code uses `.claude-plugin/marketplace.json`, while Codex uses
`.agents/plugins/marketplace.json`; both catalogs point at the same plugin
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
