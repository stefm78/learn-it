#!/usr/bin/env python3
from datetime import UTC, datetime
from pathlib import Path
import re
import sys


def next_release_id(repo_root: Path):
    release_root = repo_root / "docs" / "cores" / "releases"
    release_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y_%m_%d")
    pattern = re.compile(rf"CORE_RELEASE_{stamp}_R(\d{{2}})")
    existing_numbers = []
    for child in release_root.iterdir():
        if child.is_dir():
            match = pattern.fullmatch(child.name)
            if match:
                existing_numbers.append(int(match.group(1)))
    next_number = max(existing_numbers, default=0) + 1
    release_id = f"CORE_RELEASE_{stamp}_R{next_number:02d}"
    release_path = f"docs/cores/releases/{release_id}/"
    return release_id, release_path


def main():
    from docs.patcher.shared.build_release_plan import main as legacy_main  # type: ignore
    return legacy_main()


if __name__ == "__main__":
    main()
