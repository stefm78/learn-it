#!/usr/bin/env python3
from __future__ import annotations

import argparse
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


def parse_args(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        prog="pipeline_launcher_with_signals.py",
        description=(
            "Run the experimental pipeline launcher and append a human-readable "
            "pipeline signals review block."
        ),
        epilog=(
            "Unknown options are forwarded to tmp/pipeline_launcher.py. "
            "Use --launcher-help to display the underlying launcher help."
        ),
    )
    parser.add_argument(
        "--raw-signals-overlay",
        action="store_true",
        help="also print the raw machine-readable PIPELINE_SIGNALS_OVERLAY_RAW block",
    )
    parser.add_argument(
        "--launcher-help",
        action="store_true",
        help="show help for the underlying tmp/pipeline_launcher.py and exit",
    )
    return parser.parse_known_args(argv)


def run_underlying_launcher(launcher_args: list[str]) -> subprocess.CompletedProcess[str]:
    launcher = REPO_ROOT / "tmp" / "pipeline_launcher.py"
    return subprocess.run(
        [sys.executable, str(launcher), *launcher_args],
        cwd=str(REPO_ROOT),
        check=False,
        text=True,
        capture_output=True,
    )


def print_completed_output(completed: subprocess.CompletedProcess[str]) -> None:
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)


def print_human_review() -> None:
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


def print_raw_overlay() -> None:
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


def main(argv: list[str] | None = None) -> int:
    args, launcher_args = parse_args(sys.argv[1:] if argv is None else argv)

    if args.launcher_help:
        completed = run_underlying_launcher(["-h"])
        print_completed_output(completed)
        return completed.returncode

    completed = run_underlying_launcher(launcher_args)
    print_completed_output(completed)

    if completed.returncode != 0:
        return completed.returncode

    print_human_review()

    if args.raw_signals_overlay:
        print_raw_overlay()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
