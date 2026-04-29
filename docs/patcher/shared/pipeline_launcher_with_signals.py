#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.learnit_launcher.overlay import build_pipeline_signals_overlay


def main() -> int:
    launcher = REPO_ROOT / "tmp" / "pipeline_launcher.py"

    completed = subprocess.run(
        [sys.executable, str(launcher), *sys.argv[1:]],
        cwd=str(REPO_ROOT),
        check=False,
        text=True,
        capture_output=True,
    )

    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)

    if completed.returncode != 0:
        return completed.returncode

    overlay = build_pipeline_signals_overlay(REPO_ROOT)

    print()
    print("PIPELINE_SIGNALS_OVERLAY:")
    print(
        yaml.safe_dump(
            overlay["pipeline_signals_overlay"],
            allow_unicode=True,
            sort_keys=False,
            width=120,
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
