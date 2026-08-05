#!/usr/bin/env python3
"""Keep the root skills/ directory linked to every plugin skill."""

from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN_SKILLS = ROOT / "plugins"
ROOT_SKILLS = ROOT / "skills"


def discover_skills() -> dict[str, Path]:
    discovered: dict[str, Path] = {}
    for skill_file in sorted(PLUGIN_SKILLS.glob("*/skills/*/SKILL.md")):
        skill_dir = skill_file.parent
        name = skill_dir.name
        previous = discovered.get(name)
        if previous is not None and previous != skill_dir:
            raise ValueError(
                f"duplicate skill name {name!r}: {previous} and {skill_dir}"
            )
        discovered[name] = skill_dir
    return discovered


def sync_skills() -> None:
    discovered = discover_skills()
    ROOT_SKILLS.mkdir(exist_ok=True)

    for entry in sorted(ROOT_SKILLS.iterdir()):
        if entry.is_symlink():
            entry.unlink()
        elif entry.name not in discovered:
            raise ValueError(
                f"refusing to remove non-symlink from {ROOT_SKILLS}: {entry.name}"
            )

    for name, skill_dir in sorted(discovered.items()):
        link = ROOT_SKILLS / name
        link.symlink_to(os.path.relpath(skill_dir, ROOT_SKILLS), target_is_directory=True)

    print(f"linked {len(discovered)} plugin skills into {ROOT_SKILLS.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        sync_skills()
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
