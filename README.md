# Claude Marketplace Template

A template repository for creating your own Claude Code plugin marketplace with a beautiful documentation site.

## Features

- 🎨 **Customizable color schemes** - Choose from presets or define your own
- 📦 **GitHub Pages integration** - Auto-deploy docs on push
- 🔧 **Plugin scaffolding** - Create new plugins with one command
- ✅ **Linting** - Validate plugin structure with claudelint
- 🔄 **Template updates** - Pull updates from this template easily
- 📚 **Auto-generated docs** - Beautiful documentation site from plugin metadata

## Quick Start

### 1. Use This Template

Click the "Use this template" button on GitHub to create your own repository.

### 2. Clone and Setup

```bash
git clone https://github.com/your-username/your-marketplace.git
cd your-marketplace
./setup.sh
```

The setup script will ask you for:
- Marketplace name
- Owner name
- GitHub repository
- Color scheme (forest-green, ocean-blue, sunset-orange, royal-purple, crimson-red, or custom)
- Whether to keep the example plugin

### 3. Enable GitHub Pages

1. Go to your repository Settings → Pages
2. Set Source to "Deploy from a branch"
3. Select branch: `main` and folder: `/docs`
4. Click Save

Your docs will be available at: `https://your-username.github.io/your-marketplace/`

After making changes to your plugins, run `make update` to regenerate the docs, then commit and push.

## Usage

### Create a New Plugin

```bash
make new-plugin NAME=my-awesome-plugin
```

This creates:
- `plugins/my-awesome-plugin/`
  - `.claude-plugin/plugin.json` - Plugin metadata
  - `commands/example.md` - Example command
  - `README.md` - Plugin documentation

Don't forget to add the plugin to `.claude-plugin/marketplace.json`!

### Lint Your Plugins

```bash
make lint
```

Validates all plugins against claudelint standards.

### Update Documentation

```bash
make update
```

Regenerates plugin documentation and website data.

### Update from Template

Get the latest improvements from this template:

```bash
make update-from-template
```

This fetches:
- Latest `docs/index.html` (docs site)
- Latest build scripts
- Re-applies your branding from `.template-config.json`

## Project Structure

```
your-marketplace/
├── .claude-plugin/
│   ├── marketplace.json       # Marketplace metadata
│   └── settings.json          # Installed plugins
├── .github/workflows/
│   └── lint.yml               # Lint plugins on push/PR
├── .template-config.json      # Your branding configuration
├── docs/
│   ├── index.html            # Documentation site (static)
│   ├── data.json             # Generated plugin data
│   └── .nojekyll             # Disable Jekyll processing
├── plugins/
│   └── example-plugin/       # Example plugin (optional)
├── scripts/
│   ├── apply-branding.py     # Apply customizations
│   ├── build-website.py      # Generate website data
│   └── generate_plugin_docs.py
├── Makefile                   # Development commands
└── README.md
```

## Configuration

Edit `.template-config.json` to customize:

```json
{
  "template_version": "1.0.0",
  "marketplace_name": "my-plugins",
  "owner_name": "myusername",
  "github_repo": "myusername/my-plugins",
  "color_scheme": {
    "primary": "#228B22",
    "primary_dark": "#1a6b1a",
    "secondary": "#32CD32"
  }
}
```

After editing, run `make update` to apply changes.

## Color Scheme Presets

| Preset | Primary | Description |
|--------|---------|-------------|
| `forest-green` | #228B22 | Classic green |
| `ocean-blue` | #0077be | Deep blue |
| `sunset-orange` | #ff6b35 | Warm orange |
| `royal-purple` | #6a4c93 | Elegant purple |
| `crimson-red` | #dc143c | Bold red |

## Plugin Development

### Command Structure

Commands are defined in Markdown files under `plugins/{name}/commands/`:

```markdown
---
description: Brief description
argument-hint: [optional-args]
---

## Name
plugin-name:command-name

## Synopsis
```
/plugin-name:command-name [args]
```

## Description
What this command does...

## Implementation
1. Step-by-step implementation guide

## Return Value
What the command outputs

## Examples
Example usage

## Arguments
- $1: First argument description
```

See `plugins/example-plugin/commands/hello.md` for a complete example.

### Plugin Metadata

Edit `plugins/{name}/.claude-plugin/plugin.json`:

```json
{
  "name": "plugin-name",
  "description": "What this plugin does",
  "version": "0.0.1",
  "author": {
    "name": "Your Name"
  }
}
```

## Make Targets

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make lint` | Run plugin linter |
| `make lint-pull` | Pull latest linter image |
| `make update` | Update docs and website data |
| `make update-from-template` | Pull template updates |
| `make new-plugin NAME=foo` | Create a new plugin |

## Installation for Users

Users can install your marketplace in Claude Code:

```bash
# Add your marketplace
/plugin marketplace add your-username/your-marketplace

# Install a plugin
/plugin install my-plugin@your-marketplace

# Use a command
/my-plugin:hello
```

## Contributing

Contributions are welcome! Please:

1. Run `make lint` before committing
2. Update documentation when adding features
3. Follow the existing plugin structure

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Plugin Development Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [claudelint](https://github.com/stbenjam/claudelint)

## License

MIT

---

Built with ❤️ using [Claude Code](https://claude.com/claude-code)
