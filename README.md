# stbenjam's skills

[![skillsaw report card](https://raw.githubusercontent.com/stbenjam/skills/main/.skillsaw-card.svg)](https://skillsaw.org/)

Shared skills and plugins for Claude Code and Codex by stbenjam.

## Contents

- [Plugins](#plugins)
- [Installation](#installation)
  - [Claude Code](#claude-code)
  - [Codex](#codex)
  - [Standalone Agent Skills](#standalone-agent-skills)
- [Development](#development)
- [License](#license)

## Plugins

- **[books](plugins/books/)**: Book library workflows
- **[loops](plugins/loops/)**: Autonomous workflows that shepherd work to completion, such as driving a pull request to a mergeable state
- **[reviews](plugins/reviews/)**: Multi-agent panel code review with specialist reviewers and runtime reproducers
- **[rules](plugins/rules/)**: Context-specific rules for safe Git operations and rigorous test-failure investigation
- **[steering](plugins/steering/)**: Compact skills for changing direction, explaining decisions, asking for clarity, tightening prose, executing decisively, and raising frontend quality

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

The root `skills/` directory contains symlinks to every plugin skill. Refresh it
after adding or removing plugin skills with:

```
make sync-skills
```

Then copy any skill directory into `.agents/skills`:

```
mkdir -p .agents/skills
cp -RL skills/git-rules .agents/skills/
```

Each symlink points to a plugin skill directory containing its `SKILL.md` file.

Claude Code uses `.claude-plugin/marketplace.json`, while Codex uses
`.agents/plugins/marketplace.json`; both catalogs point at the same plugin
directories and skills.

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

Refresh the root standalone-skill symlinks with:

```bash
make sync-skills
```

## License

MIT
