# Template Information

This is the **Claude Marketplace Template** - a starter repository for creating your own Claude Code plugin marketplace.

## What Gets Replaced

When you run `./setup.sh`, the following placeholders are replaced throughout the template:

| Placeholder | Example Value | Where Used |
|-------------|---------------|------------|
| `{{MARKETPLACE_NAME}}` | `my-plugins` | Docs, config files |
| `{{MARKETPLACE_TITLE}}` | `My Plugins - Claude Code Plugins` | HTML title |
| `{{MARKETPLACE_SUBTITLE}}` | `Claude Code Plugins by username` | Docs navbar |
| `{{OWNER_NAME}}` | `username` | Plugin metadata |
| `{{GITHUB_REPO}}` | `username/my-plugins` | Links, install commands |
| `{{PRIMARY_COLOR}}` | `#228B22` | CSS color scheme |
| `{{PRIMARY_DARK}}` | `#1a6b1a` | CSS color scheme |
| `{{SECONDARY_COLOR}}` | `#32CD32` | CSS color scheme |

## Template Files

Files with placeholders that get replaced:
- `docs/index.html` - Documentation site
- `.claude-plugin/marketplace.json.template` → `marketplace.json`
- `plugins/example-plugin/.claude-plugin/plugin.json`

## Configuration Storage

Your customizations are stored in `.template-config.json`:

```json
{
  "template_version": "1.0.0",
  "marketplace_name": "...",
  "owner_name": "...",
  "github_repo": "...",
  "color_scheme": {
    "primary": "...",
    "primary_dark": "...",
    "secondary": "..."
  }
}
```

This file is used by:
- `scripts/apply-branding.py` - Apply customizations to template files
- `make update-from-template` - Reapply branding after pulling updates

## Updating from Template

To get the latest features from this template:

```bash
make update-from-template
```

This:
1. Fetches latest `docs/index.html` from template repo
2. Fetches latest build scripts
3. Re-applies your branding from `.template-config.json`
4. Preserves all your plugins and customizations

## Template Maintenance

If you want to contribute improvements to the template:

1. Fork [stbenjam/claude-marketplace-template](https://github.com/stbenjam/claude-marketplace-template)
2. Make your changes to files in `docs/`, `scripts/`, or core template files
3. Test with `./setup.sh` to ensure placeholders work
4. Submit a pull request

## Files Safe to Modify

**Safe** (your changes won't be overwritten):
- `.template-config.json` - Your configuration
- `.claude-plugin/marketplace.json` - Your plugins list
- `plugins/*` - Your plugin code
- `README.md` - Your marketplace README

**Update-able** (will be replaced by `make update-from-template`):
- `docs/index.html` - Docs site (branding reapplied)
- `scripts/*.py` - Build scripts

**One-time** (deleted after setup):
- `setup.sh` - Setup script (optional to delete)

## Version Tracking

The template version is stored in `.template-config.json`:

```json
{
  "template_version": "1.0.0",
  ...
}
```

This helps you track which version of the template you're using.

## Questions?

- [Template Repository](https://github.com/stbenjam/claude-marketplace-template)
- [Claude Code Docs](https://docs.claude.com/en/docs/claude-code)
- [Report Issues](https://github.com/stbenjam/claude-marketplace-template/issues)
