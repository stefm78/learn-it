#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

import yaml

# Support both:
#   python docs/patcher/shared/pipeline_launcher/cli.py
#   python -m docs.patcher.shared.pipeline_launcher.cli
REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.overlay import (
    build_pipeline_signals_overlay,
    build_pipeline_signals_review,
)


def parse_args(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        prog="pipeline_launcher",
        description=(
            "Run the pipeline launcher and append a human-readable pipeline signals review block. "
            "This is the official human-facing launcher command."
        ),
    )

    parser.add_argument(
        "--raw-signals-overlay",
        action="store_true",
        help="also print the raw machine-readable PIPELINE_SIGNALS_OVERLAY_RAW block",
    )
    parser.add_argument("--repo-root", help="repository root passed to the pipeline launcher")
    parser.add_argument("--pipeline", help="pipeline id to inspect, for example constitution")
    parser.add_argument("--branch", help="branch name used when rendering prompts")
    parser.add_argument("--parallel-runs", type=int, metavar="N", help="parallel run display limit")

    args, unknown_args = parser.parse_known_args(argv)

    forwarded_args: list[str] = []
    if args.repo_root:
        forwarded_args.extend(["--repo-root", args.repo_root])
    if args.pipeline:
        forwarded_args.extend(["--pipeline", args.pipeline])
    if args.branch:
        forwarded_args.extend(["--branch", args.branch])
    if args.parallel_runs is not None:
        forwarded_args.extend(["--parallel-runs", str(args.parallel_runs)])

    # Keep pass-through for future engine options during the compatibility period.
    forwarded_args.extend(unknown_args)
    return args, forwarded_args


def effective_repo_root(args: argparse.Namespace) -> Path:
    if args.repo_root:
        return Path(args.repo_root).resolve()
    return REPO_ROOT


def run_pipeline_engine(repo_root: Path, launcher_args: list[str]) -> subprocess.CompletedProcess[str]:
    engine = repo_root / "tmp" / "pipeline_launcher.py"
    return subprocess.run(
        [sys.executable, str(engine), *launcher_args],
        cwd=str(repo_root),
        check=False,
        text=True,
        capture_output=True,
    )


def print_completed_output(completed: subprocess.CompletedProcess[str]) -> None:
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)


def print_human_review(repo_root: Path) -> None:
    review = build_pipeline_signals_review(repo_root)["pipeline_signals_review"]

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


def print_raw_overlay(repo_root: Path) -> None:
    overlay = build_pipeline_signals_overlay(repo_root)
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
    repo_root = effective_repo_root(args)

    completed = run_pipeline_engine(repo_root, launcher_args)
    print_completed_output(completed)

    if completed.returncode != 0:
        return completed.returncode

    print_human_review(repo_root)

    if args.raw_signals_overlay:
        print_raw_overlay(repo_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
