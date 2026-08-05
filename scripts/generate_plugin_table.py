#!/usr/bin/env python3
"""Generate the README plugin table from the marketplace catalogs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
START_MARKER = "<!-- BEGIN GENERATED PLUGIN TABLE -->"
END_MARKER = "<!-- END GENERATED PLUGIN TABLE -->"


def load_json(path: Path) -> dict:
    with path.open() as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"expected an object in {path}")
    return data


def load_claude_plugins() -> dict[str, tuple[str, str]]:
    data = load_json(CLAUDE_MARKETPLACE)
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        raise ValueError(f"expected a plugins list in {CLAUDE_MARKETPLACE}")

    discovered: dict[str, tuple[str, str]] = {}
    for plugin in plugins:
        if not isinstance(plugin, dict):
            raise ValueError(f"invalid plugin entry in {CLAUDE_MARKETPLACE}")
        name = plugin.get("name")
        source = plugin.get("source")
        description = plugin.get("description")
        if not all(isinstance(value, str) for value in (name, source, description)):
            raise ValueError(f"plugin entries need name, source, and description: {plugin}")
        if not source.startswith("./"):
            raise ValueError(f"plugin source must be relative: {source}")
        if name in discovered:
            raise ValueError(f"duplicate plugin name: {name}")
        plugin_path = ROOT / source[2:]
        if not plugin_path.is_dir():
            raise ValueError(f"plugin source does not exist: {source}")
        discovered[name] = (source[2:], description)
    return discovered


def load_codex_plugin_names() -> set[str]:
    data = load_json(CODEX_MARKETPLACE)
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        raise ValueError(f"expected a plugins list in {CODEX_MARKETPLACE}")
    names: set[str] = set()
    for plugin in plugins:
        if not isinstance(plugin, dict) or not isinstance(plugin.get("name"), str):
            raise ValueError(f"invalid plugin entry in {CODEX_MARKETPLACE}")
        names.add(plugin["name"])
    return names


def markdown_table(plugins: dict[str, tuple[str, str]]) -> str:
    lines = [START_MARKER, "", "| Plugin | Description |", "| --- | --- |"]
    for name, (source, description) in sorted(plugins.items()):
        escaped_description = " ".join(description.split()).replace("|", "\\|")
        lines.append(f"| [{name}]({source}/) | {escaped_description} |")
    lines.append(END_MARKER)
    return "\n".join(lines)


def update_readme(table: str) -> None:
    contents = README.read_text()
    if contents.count(START_MARKER) != 1 or contents.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one plugin table marker pair")
    start = contents.index(START_MARKER)
    end = contents.index(END_MARKER, start) + len(END_MARKER)
    updated = contents[:start] + table + contents[end:]
    if updated != contents:
        README.write_text(updated)
        print(f"updated {README.relative_to(ROOT)}")
    else:
        print(f"{README.relative_to(ROOT)} is up to date")


def main() -> None:
    plugins = load_claude_plugins()
    codex_names = load_codex_plugin_names()
    if set(plugins) != codex_names:
        raise ValueError("Claude and Codex marketplace plugin lists differ")
    update_readme(markdown_table(plugins))


if __name__ == "__main__":
    main()
