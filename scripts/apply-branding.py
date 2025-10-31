#!/usr/bin/env python3
"""
Apply branding customizations to template files.

This script reads configuration from .template-config.json and applies
the branding (colors, names, repo info) to template files.
"""

import json
import os
import sys
from pathlib import Path

# Color scheme presets
COLOR_PRESETS = {
    "forest-green": {
        "primary": "#228B22",
        "primary_dark": "#1a6b1a",
        "secondary": "#32CD32",
    },
    "ocean-blue": {
        "primary": "#0077be",
        "primary_dark": "#005a8e",
        "secondary": "#4db8ff",
    },
    "sunset-orange": {
        "primary": "#ff6b35",
        "primary_dark": "#d94f1f",
        "secondary": "#ff9966",
    },
    "royal-purple": {
        "primary": "#6a4c93",
        "primary_dark": "#4a3369",
        "secondary": "#9d84b7",
    },
    "crimson-red": {
        "primary": "#dc143c",
        "primary_dark": "#a0102a",
        "secondary": "#ff6b7a",
    },
}


def load_config():
    """Load configuration from .template-config.json"""
    config_path = Path(".template-config.json")
    if not config_path.exists():
        print("Error: .template-config.json not found")
        print("Run setup.sh first to configure your marketplace")
        sys.exit(1)

    with open(config_path) as f:
        return json.load(f)


def apply_to_file(file_path, replacements):
    """Apply replacements to a file"""
    if not Path(file_path).exists():
        print(f"Warning: {file_path} not found, skipping")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    for key, value in replacements.items():
        placeholder = f"{{{{{key}}}}}"
        content = content.replace(placeholder, value)

    with open(file_path, 'w') as f:
        f.write(content)

    print(f"✓ Applied branding to {file_path}")


def main():
    config = load_config()

    # Extract owner and repo name from github_repo
    github_repo = config["github_repo"]
    if "/" in github_repo:
        owner, repo = github_repo.split("/", 1)
        github_pages_url = f"{owner}.github.io/{repo}"
    else:
        github_pages_url = f"{github_repo}.github.io"

    # Build replacements dict
    replacements = {
        "MARKETPLACE_NAME": config["marketplace_name"],
        "MARKETPLACE_TITLE": f"{config['marketplace_name']} - Claude Code Plugins",
        "MARKETPLACE_SUBTITLE": f"Claude Code Plugins by {config['owner_name']}",
        "OWNER_NAME": config["owner_name"],
        "GITHUB_REPO": config["github_repo"],
        "GITHUB_PAGES_URL": github_pages_url,
        "PRIMARY_COLOR": config["color_scheme"]["primary"],
        "PRIMARY_DARK": config["color_scheme"]["primary_dark"],
        "SECONDARY_COLOR": config["color_scheme"]["secondary"],
    }

    # Apply to all template files
    files_to_update = [
        "docs/index.html",
        ".claude-plugin/marketplace.json",
        "plugins/example-plugin/.claude-plugin/plugin.json",
        "README.md",
    ]

    for file_path in files_to_update:
        apply_to_file(file_path, replacements)

    print("\n✓ Branding applied successfully!")


if __name__ == "__main__":
    main()
