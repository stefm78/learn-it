#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.overlay import (
    build_pipeline_signals_overlay,
    build_pipeline_signals_review,
)


def main() -> int:
    raw_overlay = "--raw-signals-overlay" in sys.argv[1:]
    launcher_args = [arg for arg in sys.argv[1:] if arg != "--raw-signals-overlay"]

    launcher = REPO_ROOT / "tmp" / "pipeline_launcher.py"

    completed = subprocess.run(
        [sys.executable, str(launcher), *launcher_args],
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

    review = build_pipeline_signals_review(REPO_ROOT)["pipeline_signals_review"]

    print()
    print("PIPELINE_SIGNALS_REVIEW:")
    print(f"status: {review['status']}")
    print(f"recommended_default: {review['recommended_default']}")
    print(f"human_summary: {review['human_summary']}")
    print(f"attention_signal_count: {review['attention_signal_count']}")
    print("attention_signals:")
    for line in review["attention_signals"]:
        print(f"  - {line}")
    print("affected_scope_keys:")
    for scope_key in review["affected_scope_keys"]:
        print(f"  - {scope_key}")
    print("recommended_actions:")
    for action in review["recommended_actions"]:
        print(f"  - {action}")
    print(f"run_opening_authorized_by_signals: {str(review['run_opening_authorized_by_signals']).lower()}")
    print(f"run_materialization_authorized_by_signals: {str(review['run_materialization_authorized_by_signals']).lower()}")
    print()
    print("recommended_prompt:")
    print("---")
    print(review["recommended_prompt"])
    print("---")

    if raw_overlay:
        overlay = build_pipeline_signals_overlay(REPO_ROOT)
        print()
        print("PIPELINE_SIGNALS_OVERLAY_RAW:")
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
