#!/usr/bin/env python3
"""Synchronize Claude, Codex, and portable Agent Plugins metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
PORTABLE_METADATA_FIELDS = (
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)
STDIO_FIELDS = ("command", "args", "env", "cwd")
REMOTE_FIELDS = ("url", "headers")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def marketplace_plugin_dirs(repo_root: Path) -> list[Path]:
    marketplace = load_json(repo_root / ".claude-plugin" / "marketplace.json")
    plugins_dir = (repo_root / "plugins").resolve()
    result: list[Path] = []
    for entry in marketplace.get("plugins", []):
        if not isinstance(entry, dict):
            continue
        source = entry.get("source")
        if not isinstance(source, str) or not source.startswith("./plugins/"):
            continue
        plugin_dir = (repo_root / source[2:]).resolve()
        if plugin_dir.parent != plugins_dir:
            raise ValueError(f"Marketplace source escapes plugins directory: {source}")
        result.append(plugin_dir)
    return sorted(set(result))


def normalize_author(value: Any) -> Any:
    if isinstance(value, str):
        return {"name": value}
    if isinstance(value, dict):
        return {key: value[key] for key in ("name", "email", "url") if key in value}
    return value


def portable_manifest_from_claude(claude: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(claude.get("name"), str) or not claude["name"]:
        raise ValueError("Claude manifest must define a non-empty name")
    portable: dict[str, Any] = {"$schema": PLUGIN_SCHEMA}
    for field in PORTABLE_METADATA_FIELDS:
        if field in claude:
            portable[field] = normalize_author(claude[field]) if field == "author" else claude[field]
    return portable


def claude_manifest_from_portable(portable: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(portable.get("name"), str) or not portable["name"]:
        raise ValueError("Agent Plugins manifest must define a non-empty name")
    return {field: portable[field] for field in PORTABLE_METADATA_FIELDS if field in portable}


def codex_manifest_from_claude(claude: dict[str, Any]) -> dict[str, Any]:
    """Build a minimal Codex manifest while leaving existing UI metadata intact."""
    portable = portable_manifest_from_claude(claude)
    portable.pop("$schema")
    author = portable.get("author", {})
    developer = author.get("name", "stbenjam") if isinstance(author, dict) else "stbenjam"
    name = portable["name"]
    description = portable.get("description", f"Use the {name} plugin.")
    portable.update(
        {
            "skills": "./skills/",
            "interface": {
                "displayName": name.replace("-", " ").title(),
                "shortDescription": description,
                "longDescription": description,
                "developerName": developer,
                "category": "Productivity",
                "capabilities": [],
                "defaultPrompt": f"Help me use the {name} plugin.",
            },
        }
    )
    return portable


def portable_mcp_from_claude(claude_mcp: dict[str, Any]) -> dict[str, Any]:
    servers = claude_mcp.get("mcpServers")
    if not isinstance(servers, dict):
        raise ValueError("Claude MCP configuration must define an mcpServers object")

    portable_servers: dict[str, Any] = {}
    for name, server in servers.items():
        if not isinstance(server, dict):
            raise ValueError(f"MCP server {name!r} must be a JSON object")
        source_type = server.get("type")
        if source_type in (None, "stdio"):
            server_type, fields = "stdio", STDIO_FIELDS
        elif source_type == "http":
            server_type, fields = "streamable-http", REMOTE_FIELDS
        elif source_type == "sse":
            server_type, fields = "sse", REMOTE_FIELDS
        else:
            raise ValueError(f"Unsupported Claude MCP transport {source_type!r} for {name!r}")
        translated: dict[str, Any] = {"type": server_type}
        for field in fields:
            if field in server:
                translated[field] = server[field]
        portable_servers[name] = translated
    return {"$schema": MCP_SCHEMA, "mcpServers": portable_servers}


def sync_manifest(plugin_dir: Path, check: bool) -> list[str]:
    claude_path = plugin_dir / ".claude-plugin" / "plugin.json"
    codex_path = plugin_dir / ".codex-plugin" / "plugin.json"
    portable_path = plugin_dir / "plugin.json"
    errors: list[str] = []
    try:
        claude = load_json(claude_path) if claude_path.is_file() else None
        codex = load_json(codex_path) if codex_path.is_file() else None
        portable = load_json(portable_path) if portable_path.is_file() else None
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"{plugin_dir.name}: {exc}"]

    if claude is None and portable is None and codex is None:
        return [f"{plugin_dir.name}: missing all plugin manifests"]
    if check:
        for path, value in ((claude_path, claude), (codex_path, codex), (portable_path, portable)):
            if value is None:
                errors.append(f"{plugin_dir.name}: missing {path}")
        return errors

    if claude is None:
        source = portable if portable is not None else codex
        assert source is not None
        write_json(claude_path, claude_manifest_from_portable(source))
        claude = load_json(claude_path)
        print(f"created {claude_path}")
    if portable is None:
        assert claude is not None
        write_json(portable_path, portable_manifest_from_claude(claude))
        portable = load_json(portable_path)
        print(f"created {portable_path}")
    if codex is None:
        assert claude is not None
        codex_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(codex_path, codex_manifest_from_claude(claude))
        codex = load_json(codex_path)
        print(f"created {codex_path}")

    assert claude is not None and codex is not None and portable is not None
    expected = portable_manifest_from_claude(claude)
    for field in PORTABLE_METADATA_FIELDS:
        if field not in expected:
            continue
        if portable.get(field) != expected[field]:
            errors.append(f"{plugin_dir.name}: {portable_path} differs in {field!r}")
        if codex.get(field) != expected[field]:
            errors.append(f"{plugin_dir.name}: {codex_path} differs in {field!r}")
    return errors


def sync_mcp(plugin_dir: Path, check: bool) -> list[str]:
    claude_path = plugin_dir / ".mcp.json"
    portable_path = plugin_dir / "mcp.json"
    if not claude_path.is_file():
        return []
    try:
        expected = portable_mcp_from_claude(load_json(claude_path))
        existing = load_json(portable_path) if portable_path.is_file() else None
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"{plugin_dir.name}: {exc}"]
    if existing is None:
        if check:
            return [f"{plugin_dir.name}: missing {portable_path}"]
        write_json(portable_path, expected)
        print(f"created {portable_path}")
        return []
    if existing != expected:
        return [f"{plugin_dir.name}: {portable_path} differs from {claude_path}"]
    return []


def sync_agent_plugins(repo_root: Path, check: bool) -> int:
    try:
        plugin_dirs = marketplace_plugin_dirs(repo_root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    errors: list[str] = []
    for plugin_dir in plugin_dirs:
        errors.extend(sync_manifest(plugin_dir, check))
        errors.extend(sync_mcp(plugin_dir, check))
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    action = "validated" if check else "synchronized"
    print(f"Agent Plugins: {action} {len(plugin_dirs)} first-party plugins")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without creating files")
    args = parser.parse_args()
    return sync_agent_plugins(Path(__file__).resolve().parent.parent, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
