# stbenjam's skills

[![skillsaw report card](https://raw.githubusercontent.com/stbenjam/skills/main/.skillsaw-card.svg)](https://skillsaw.org/)

Shared skills and plugins for Claude Code and Codex by stbenjam.

## Contents

  - [Plugins](#plugins)
  - [Installation](#installation)
  - [Claude Code](#claude-code)
  - [Codex](#codex)
  - [Other Agents](#other-agents)
- [Development](#development)
- [License](#license)

## Plugins

<!-- BEGIN GENERATED PLUGIN TABLE -->

| Plugin | Description |
| --- | --- |
| [books](plugins/books/) | Search and analyze a Calibre library or Goodreads export |
| [loops](plugins/loops/) | Autonomous loops that shepherd work to completion, such as driving a PR to a mergeable state |
| [openclaw](plugins/openclaw/) | A grab-bag of miscellaneous OpenClaw skills (pollen forecasts, Orangetheory lookups, narrated video reels) with no unifying theme. |
| [reviews](plugins/reviews/) | Multi-agent panel code review with specialist reviewers and runtime reproducers |
| [rules](plugins/rules/) | Context-specific rules for safe Git operations and rigorous test-failure investigation. |
| [steering](plugins/steering/) | Compact conversation-steering skills for changing direction, explaining decisions, asking for clarity, tightening prose, executing decisively, and raising frontend quality. |
<!-- END GENERATED PLUGIN TABLE -->

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

### Agent Plugins

Each plugin also includes a portable Agent Plugins v1 manifest at
`plugins/<name>/plugin.json`. Agent Plugins exposes the plugin's directly
packaged skills; Claude-specific commands, agents, hooks, and dependency
bundles remain in `.claude-plugin/plugin.json`. Shared name, version,
description, and author metadata is synchronized across the Claude, Codex,
and portable manifests.

Run `make sync-agent-plugins` after changing plugin metadata, or
`make check-agent-plugins` in validation-only workflows.

### Other Agents

Use the `skills` CLI to select skills:

```
npx skills install stbenjam/skills
```

Or copy one into `.agents/skills`:

```
mkdir -p .agents/skills
cp -RL skills/git-rules .agents/skills/
```

Run `make update` after adding or removing plugin skills to refresh links and docs.

## Development

Run `make update` to regenerate the documentation, this plugin table, and the
root `skills/` symlinks. Then lint plugins and skills with
[skillsaw](https://skillsaw.org/) in strict mode:

```bash
make update
make lint
```

Apply autofixes with:

```bash
make lint-fix
```

## License

MIT
