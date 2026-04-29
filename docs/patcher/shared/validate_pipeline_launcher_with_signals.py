#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import py_compile
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.overlay import (
    build_pipeline_signals_overlay,
    build_pipeline_signals_review,
)
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        args,
        cwd=str(REPO_ROOT),
        check=False,
        text=True,
        capture_output=True,
        timeout=30,
    )
    return completed.returncode, completed.stdout or "", completed.stderr or ""


def build_report() -> dict[str, Any]:
    paths = {
        "tmp_launcher": REPO_ROOT / "tmp" / "pipeline_launcher.py",
        "wrapper": REPO_ROOT / "docs" / "patcher" / "shared" / "pipeline_launcher_with_signals.py",
        "overlay": REPO_ROOT / "docs" / "patcher" / "shared" / "pipeline_launcher" / "overlay.py",
        "pipeline_signals": REPO_ROOT / "docs" / "patcher" / "shared" / "pipeline_launcher" / "pipeline_signals.py",
    }

    findings: list[dict[str, Any]] = []

    for name, path in paths.items():
        if not path.exists():
            findings.append({"finding_id": "MISSING_FILE", "severity": "blocking", "name": name, "path": str(path)})
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            findings.append(
                {"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "name": name, "detail": str(exc)}
            )

    tmp_rc, tmp_stdout, tmp_stderr = run_command([sys.executable, str(paths["tmp_launcher"])])
    wrapper_rc, wrapper_stdout, wrapper_stderr = run_command([sys.executable, str(paths["wrapper"])])
    raw_rc, raw_stdout, raw_stderr = run_command([sys.executable, str(paths["wrapper"]), "--raw-signals-overlay"])
    help_rc, help_stdout, help_stderr = run_command([sys.executable, str(paths["wrapper"]), "-h"])
    launcher_help_rc, launcher_help_stdout, launcher_help_stderr = run_command(
        [sys.executable, str(paths["wrapper"]), "--launcher-help"]
    )

    if tmp_rc != 0:
        findings.append({"finding_id": "TMP_LAUNCHER_RUNTIME_FAILED", "severity": "blocking", "returncode": tmp_rc})
    if wrapper_rc != 0:
        findings.append(
            {"finding_id": "SIGNALS_WRAPPER_RUNTIME_FAILED", "severity": "blocking", "returncode": wrapper_rc}
        )
    if raw_rc != 0:
        findings.append(
            {"finding_id": "SIGNALS_WRAPPER_RAW_RUNTIME_FAILED", "severity": "blocking", "returncode": raw_rc}
        )
    if help_rc != 0:
        findings.append(
            {"finding_id": "SIGNALS_WRAPPER_HELP_FAILED", "severity": "blocking", "returncode": help_rc}
        )
    if launcher_help_rc != 0:
        findings.append(
            {"finding_id": "UNDERLYING_LAUNCHER_HELP_FAILED", "severity": "blocking", "returncode": launcher_help_rc}
        )

    overlay = build_pipeline_signals_overlay(REPO_ROOT)
    review = build_pipeline_signals_review(REPO_ROOT)

    overlay_root = overlay.get("pipeline_signals_overlay", {})
    review_root = review.get("pipeline_signals_review", {})
    summary = overlay_root.get("signal_summary", {})
    prompt = review_root.get("recommended_prompt", "")

    if overlay_root.get("recommended_default_hint") != "review_pipeline_signals":
        findings.append(
            {
                "finding_id": "UNEXPECTED_RECOMMENDED_DEFAULT_HINT",
                "severity": "blocking",
                "actual": overlay_root.get("recommended_default_hint"),
            }
        )

    if summary.get("has_attention_signals") is not True:
        findings.append({"finding_id": "MISSING_ATTENTION_SIGNAL", "severity": "blocking"})

    if review_root.get("status") != "attention":
        findings.append({"finding_id": "HUMAN_REVIEW_STATUS_NOT_ATTENTION", "severity": "blocking"})

    if review_root.get("recommended_default") != "review_pipeline_signals":
        findings.append({"finding_id": "HUMAN_REVIEW_RECOMMENDED_DEFAULT_INVALID", "severity": "blocking"})

    if review_root.get("run_opening_authorized_by_signals") is not False:
        findings.append({"finding_id": "REVIEW_MUST_NOT_AUTHORIZE_RUN_OPENING", "severity": "blocking"})

    if "n'ouvre pas de run" not in prompt:
        findings.append({"finding_id": "PROMPT_MISSING_NO_RUN_CONSTRAINT", "severity": "blocking"})

    if "STAGE_00" not in prompt:
        findings.append({"finding_id": "PROMPT_MISSING_STAGE00_REFERENCE", "severity": "blocking"})

    if "OPEN_NEW_RUN" not in prompt:
        findings.append({"finding_id": "PROMPT_MISSING_OPEN_NEW_RUN_REFERENCE", "severity": "blocking"})

    runtime_required = [
        "PIPELINE_SIGNALS_REVIEW:",
        "status: attention",
        "recommended_default: review_pipeline_signals",
        "recommended_prompt:",
        "n'ouvre pas de run",
        "STAGE_00",
        "OPEN_NEW_RUN",
        "run_opening_authorized_by_signals: false",
    ]
    missing_runtime = [snippet for snippet in runtime_required if snippet not in wrapper_stdout]
    if missing_runtime:
        findings.append(
            {
                "finding_id": "WRAPPER_OUTPUT_MISSING_EXPECTED_HUMAN_SNIPPETS",
                "severity": "blocking",
                "missing": missing_runtime,
            }
        )

    if "signal_summary: &" in wrapper_stdout or "open_new_run_prompt_binding_addition:" in wrapper_stdout:
        findings.append(
            {
                "finding_id": "WRAPPER_DEFAULT_OUTPUT_STILL_TOO_RAW",
                "severity": "blocking",
            }
        )

    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in raw_stdout:
        findings.append(
            {
                "finding_id": "RAW_OVERLAY_OPTION_MISSING",
                "severity": "blocking",
            }
        )

    help_required = [
        "--raw-signals-overlay",
        "--launcher-help",
        "Unknown options are forwarded to tmp/pipeline_launcher.py",
    ]
    missing_help = [snippet for snippet in help_required if snippet not in help_stdout]
    if missing_help:
        findings.append(
            {
                "finding_id": "WRAPPER_HELP_MISSING_EXPECTED_OPTIONS",
                "severity": "blocking",
                "missing": missing_help,
            }
        )

    if "--raw-signals-overlay" in launcher_help_stdout:
        findings.append(
            {
                "finding_id": "UNDERLYING_LAUNCHER_HELP_SHOULD_NOT_INCLUDE_WRAPPER_ONLY_OPTION",
                "severity": "blocking",
            }
        )

    if "--pipeline PIPELINE" not in launcher_help_stdout:
        findings.append(
            {
                "finding_id": "UNDERLYING_LAUNCHER_HELP_NOT_FORWARDED",
                "severity": "blocking",
            }
        )

    return {
        "pipeline_launcher_with_signals_validation": {
            "schema_version": "0.3",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_27E",
            "purpose": "Expose wrapper-specific CLI help while preserving human-readable pipeline signal review output.",
            "mutation_policy": {
                "tmp_pipeline_launcher": "not_modified",
                "wrapper": "updated",
                "overlay_module": "not_modified",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "inputs": [
                {
                    "ref": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                    "sha256": sha256_file(path),
                }
                for path in paths.values()
                if path.exists()
            ],
            "overlay": overlay_root,
            "human_review": review_root,
            "tmp_launcher_runtime": {
                "status": "PASS" if tmp_rc == 0 else "FAIL",
                "stdout_excerpt": tmp_stdout[:1200],
                "stderr_excerpt": tmp_stderr[:800],
            },
            "wrapper_runtime": {
                "status": "PASS" if wrapper_rc == 0 else "FAIL",
                "stdout_excerpt": wrapper_stdout[-3500:],
                "stderr_excerpt": wrapper_stderr[:800],
            },
            "raw_wrapper_runtime": {
                "status": "PASS" if raw_rc == 0 else "FAIL",
                "stdout_excerpt": raw_stdout[-2500:],
                "stderr_excerpt": raw_stderr[:800],
            },
            "wrapper_help_runtime": {
                "status": "PASS" if help_rc == 0 else "FAIL",
                "stdout": help_stdout,
                "stderr": help_stderr,
            },
            "underlying_launcher_help_runtime": {
                "status": "PASS" if launcher_help_rc == 0 else "FAIL",
                "stdout_excerpt": launcher_help_stdout[:1800],
                "stderr_excerpt": launcher_help_stderr[:800],
            },
            "blocking_findings": findings,
            "result_summary": {
                "has_attention_signals": summary.get("has_attention_signals"),
                "recommended_default_hint": overlay_root.get("recommended_default_hint"),
                "wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in wrapper_stdout,
                "wrapper_outputs_copyable_prompt": "recommended_prompt:" in wrapper_stdout and "n'ouvre pas de run" in wrapper_stdout,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_stdout,
                "wrapper_help_exposes_raw_overlay_flag": "--raw-signals-overlay" in help_stdout,
                "wrapper_help_exposes_launcher_help_flag": "--launcher-help" in help_stdout,
                "launcher_authorizes_run_from_signals": False,
                "tmp_pipeline_launcher_behavior_changed": False,
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_with_signals_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    report_path = REPO_ROOT / args.report
    write_yaml(report_path, report)

    root = report["pipeline_launcher_with_signals_validation"]
    summary = root["result_summary"]

    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Recommended default hint: {summary['recommended_default_hint']}")
    print(f"Human review output: {summary['wrapper_outputs_human_review']}")
    print(f"Copyable prompt output: {summary['wrapper_outputs_copyable_prompt']}")
    print(f"Wrapper help exposes raw flag: {summary['wrapper_help_exposes_raw_overlay_flag']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
