"""Require Claude, Codex, and portable Agent Plugins metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from skillsaw import RepositoryContext, Rule, RuleViolation, Severity
from skillsaw.lint_target import PluginNode


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


class AgentPluginManifestsRequiredRule(Rule):
    """Every marketplace plugin has synchronized Claude, Codex, and portable manifests."""

    @property
    def rule_id(self) -> str:
        return "agent-plugin-manifests-required"

    @property
    def description(self) -> str:
        return "Every marketplace plugin has synchronized Claude, Codex, and Agent Plugins manifests"

    def default_severity(self) -> Severity:
        return Severity.ERROR

    def check(self, context: RepositoryContext) -> list[RuleViolation]:
        violations: list[RuleViolation] = []
        for plugin_dir in self._plugin_dirs(context):
            violations.extend(self._check_plugin(plugin_dir))
        return violations

    def _plugin_dirs(self, context: RepositoryContext) -> Iterable[Path]:
        marketplace_path = context.root_path / ".claude-plugin" / "marketplace.json"
        if marketplace_path.is_file():
            try:
                marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                marketplace = None
            if isinstance(marketplace, dict):
                plugins_root = (context.root_path / "plugins").resolve()
                paths = []
                for entry in marketplace.get("plugins", []):
                    if not isinstance(entry, dict) or not isinstance(entry.get("source"), str):
                        continue
                    source = entry["source"]
                    if not source.startswith("./plugins/"):
                        continue
                    path = (context.root_path / source[2:]).resolve()
                    if path.parent == plugins_root:
                        paths.append(path)
                if paths:
                    return sorted(set(paths))
        return sorted(node.path for node in context.lint_tree.find(PluginNode))

    def _check_plugin(self, plugin_dir: Path) -> list[RuleViolation]:
        claude_path = plugin_dir / ".claude-plugin" / "plugin.json"
        codex_path = plugin_dir / ".codex-plugin" / "plugin.json"
        portable_path = plugin_dir / "plugin.json"
        violations: list[RuleViolation] = []
        if not claude_path.is_file():
            violations.append(self.violation("Missing Claude manifest at .claude-plugin/plugin.json", file_path=claude_path))
        if not codex_path.is_file():
            violations.append(self.violation("Missing Codex manifest at .codex-plugin/plugin.json", file_path=codex_path))
        if not portable_path.is_file():
            violations.append(self.violation("Missing Agent Plugins manifest at plugin.json", file_path=portable_path))
        claude = self._load_object(claude_path)
        codex = self._load_object(codex_path)
        portable = self._load_object(portable_path)
        if claude_path.is_file() and claude is None:
            violations.append(self.violation("Claude manifest must contain a JSON object", file_path=claude_path))
        if codex_path.is_file() and codex is None:
            violations.append(self.violation("Codex manifest must contain a JSON object", file_path=codex_path))
        if portable_path.is_file() and portable is None:
            violations.append(self.violation("Agent Plugins manifest must contain a JSON object", file_path=portable_path))
        if claude is not None and codex is not None and portable is not None:
            for field in PORTABLE_METADATA_FIELDS:
                if field not in claude:
                    continue
                expected = self._portable_value(field, claude[field])
                if portable.get(field) != expected:
                    violations.append(self.violation(f"Unsynchronized '{field}' metadata", file_path=portable_path))
                if codex.get(field) != expected:
                    violations.append(self.violation(f"Unsynchronized '{field}' metadata", file_path=codex_path))
        return violations

    @staticmethod
    def _load_object(path: Path) -> dict[str, Any] | None:
        if not path.is_file():
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    @staticmethod
    def _portable_value(field: str, value: Any) -> Any:
        if field == "author" and isinstance(value, str):
            return {"name": value}
        if field == "author" and isinstance(value, dict):
            return {key: value[key] for key in ("name", "email", "url") if key in value}
        return value
