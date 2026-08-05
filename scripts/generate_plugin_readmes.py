#!/usr/bin/env python3
"""Generate each plugin README's skill list from SKILL.md frontmatter."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
START = "<!-- BEGIN GENERATED SKILLS -->"
END = "<!-- END GENERATED SKILLS -->"


def frontmatter_value(contents: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", contents)
    if match is None:
        raise ValueError(f"missing {key!r} in skill frontmatter")
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def generated_list(plugin: Path) -> str:
    entries = []
    for skill_file in sorted(plugin.glob("skills/*/SKILL.md")):
        contents = skill_file.read_text()
        name = frontmatter_value(contents, "name")
        description = frontmatter_value(contents, "description")
        relative = skill_file.relative_to(plugin).as_posix()
        entries.append(f"- [`{name}`]({relative}) — {description}")
    if not entries:
        raise ValueError(f"no skills found in {plugin.relative_to(ROOT)}")
    return "\n".join((START, *entries, END))


def update_readme(plugin: Path) -> bool:
    readme = plugin / "README.md"
    contents = readme.read_text()
    if contents.count(START) != 1 or contents.count(END) != 1:
        raise ValueError(
            f"{readme.relative_to(ROOT)} must contain exactly one skill marker pair"
        )
    before, remainder = contents.split(START, 1)
    _, after = remainder.split(END, 1)
    updated = before + generated_list(plugin) + after
    if updated == contents:
        print(f"{readme.relative_to(ROOT)} is up to date")
        return False
    readme.write_text(updated)
    print(f"updated {readme.relative_to(ROOT)}")
    return True


def main() -> None:
    for plugin in sorted(path for path in PLUGINS.iterdir() if path.is_dir()):
        update_readme(plugin)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"error: {error}")
