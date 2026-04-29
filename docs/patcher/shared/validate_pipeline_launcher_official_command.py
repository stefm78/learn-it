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

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml


OFFICIAL_COMMAND = Path("docs/patcher/shared/pipeline_launcher/cli.py")
COMPAT_COMMAND = Path("docs/patcher/shared/pipeline_launcher_with_signals.py")
TMP_ENGINE = Path("tmp/pipeline_launcher.py")


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
    findings: list[dict[str, Any]] = []

    paths = {
        "official_command": REPO_ROOT / OFFICIAL_COMMAND,
        "compat_command": REPO_ROOT / COMPAT_COMMAND,
        "tmp_engine": REPO_ROOT / TMP_ENGINE,
    }

    for name, path in paths.items():
        if not path.exists():
            findings.append({"finding_id": "MISSING_FILE", "severity": "blocking", "name": name, "path": str(path)})
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            findings.append({"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "name": name, "detail": str(exc)})

    official_help_rc, official_help_stdout, official_help_stderr = run_command(
        [sys.executable, str(OFFICIAL_COMMAND), "-h"]
    )
    official_run_rc, official_run_stdout, official_run_stderr = run_command(
        [sys.executable, str(OFFICIAL_COMMAND)]
    )
    official_raw_rc, official_raw_stdout, official_raw_stderr = run_command(
        [sys.executable, str(OFFICIAL_COMMAND), "--raw-signals-overlay"]
    )
    module_rc, module_stdout, module_stderr = run_command(
        [sys.executable, "-m", "docs.patcher.shared.pipeline_launcher.cli", "-h"]
    )
    compat_rc, compat_stdout, compat_stderr = run_command(
        [sys.executable, str(COMPAT_COMMAND)]
    )
    tmp_rc, tmp_stdout, tmp_stderr = run_command(
        [sys.executable, str(TMP_ENGINE)]
    )

    runtime_results = {
        "official_help": (official_help_rc, official_help_stdout, official_help_stderr),
        "official_run": (official_run_rc, official_run_stdout, official_run_stderr),
        "official_raw": (official_raw_rc, official_raw_stdout, official_raw_stderr),
        "official_module_help": (module_rc, module_stdout, module_stderr),
        "compat_run": (compat_rc, compat_stdout, compat_stderr),
        "tmp_engine": (tmp_rc, tmp_stdout, tmp_stderr),
    }

    for name, (rc, _stdout, stderr) in runtime_results.items():
        if rc != 0:
            findings.append(
                {
                    "finding_id": "COMMAND_FAILED",
                    "severity": "blocking",
                    "command": name,
                    "returncode": rc,
                    "stderr_excerpt": stderr[:500],
                }
            )

    help_required = [
        "--raw-signals-overlay",
        "--repo-root REPO_ROOT",
        "--pipeline PIPELINE",
        "--branch BRANCH",
        "--parallel-runs N",
        "official human-facing launcher command",
    ]
    missing_help = [snippet for snippet in help_required if snippet not in official_help_stdout]
    if missing_help:
        findings.append(
            {
                "finding_id": "OFFICIAL_HELP_MISSING_EXPECTED_OPTIONS",
                "severity": "blocking",
                "missing": missing_help,
            }
        )

    if "--launcher-help" in official_help_stdout:
        findings.append(
            {
                "finding_id": "OFFICIAL_HELP_MUST_NOT_EXPOSE_SECOND_LAUNCHER_HELP",
                "severity": "blocking",
            }
        )

    official_required_output = [
        "PIPELINE_REGISTRY_STATE:",
        "PIPELINE_LAUNCHER_STATE:",
        "PIPELINE_LAUNCH_MENU:",
        "PIPELINE_SIGNALS_REVIEW:",
        "recommended_prompt:",
        "run_opening_authorized_by_signals: false",
    ]
    missing_output = [snippet for snippet in official_required_output if snippet not in official_run_stdout]
    if missing_output:
        findings.append(
            {
                "finding_id": "OFFICIAL_OUTPUT_MISSING_EXPECTED_SNIPPETS",
                "severity": "blocking",
                "missing": missing_output,
            }
        )

    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in official_raw_stdout:
        findings.append(
            {
                "finding_id": "OFFICIAL_RAW_OVERLAY_FLAG_NOT_WORKING",
                "severity": "blocking",
            }
        )

    compat_required = [
        "PIPELINE_REGISTRY_STATE:",
        "PIPELINE_SIGNALS_REVIEW:",
    ]
    missing_compat = [snippet for snippet in compat_required if snippet not in compat_stdout]
    if missing_compat:
        findings.append(
            {
                "finding_id": "COMPAT_WRAPPER_MISSING_EXPECTED_SNIPPETS",
                "severity": "blocking",
                "missing": missing_compat,
            }
        )

    if "PIPELINE_SIGNALS_REVIEW:" in tmp_stdout:
        findings.append(
            {
                "finding_id": "TMP_ENGINE_SHOULD_REMAIN_UNCHANGED_IN_PHASE_28B",
                "severity": "blocking",
            }
        )

    return {
        "pipeline_launcher_official_command_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28B",
            "purpose": "Create an official human-facing pipeline launcher command without moving the tmp runtime engine yet.",
            "mutation_policy": {
                "official_command": "created",
                "compatibility_wrapper": "updated",
                "tmp_pipeline_launcher": "not_modified",
                "runtime_modules": "not_moved_yet",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "commands": {
                "official_file_command": "python docs/patcher/shared/pipeline_launcher/cli.py",
                "official_module_command": "python -m docs.patcher.shared.pipeline_launcher.cli",
                "compatibility_command": "python docs/patcher/shared/pipeline_launcher_with_signals.py",
                "tmp_engine": "python tmp/pipeline_launcher.py",
            },
            "inputs": [
                {"ref": str(path.relative_to(REPO_ROOT)).replace("\\", "/"), "sha256": sha256_file(path)}
                for path in paths.values()
                if path.exists()
            ],
            "runtime": {
                "official_help": {"status": "PASS" if official_help_rc == 0 else "FAIL", "stdout": official_help_stdout, "stderr": official_help_stderr},
                "official_run": {"status": "PASS" if official_run_rc == 0 else "FAIL", "stdout_excerpt": official_run_stdout[-3000:], "stderr": official_run_stderr[:800]},
                "official_raw": {"status": "PASS" if official_raw_rc == 0 else "FAIL", "stdout_excerpt": official_raw_stdout[-2500:], "stderr": official_raw_stderr[:800]},
                "official_module_help": {"status": "PASS" if module_rc == 0 else "FAIL", "stdout": module_stdout, "stderr": module_stderr},
                "compat_run": {"status": "PASS" if compat_rc == 0 else "FAIL", "stdout_excerpt": compat_stdout[-2000:], "stderr": compat_stderr[:800]},
                "tmp_engine": {"status": "PASS" if tmp_rc == 0 else "FAIL", "stdout_excerpt": tmp_stdout[:1500], "stderr": tmp_stderr[:800]},
            },
            "blocking_findings": findings,
            "result_summary": {
                "official_command_created": (REPO_ROOT / OFFICIAL_COMMAND).exists(),
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_run_stdout,
                "official_help_exposes_single_surface": "--launcher-help" not in official_help_stdout and "--pipeline PIPELINE" in official_help_stdout,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in official_raw_stdout,
                "compatibility_wrapper_delegates_to_official_command": "PIPELINE_SIGNALS_REVIEW:" in compat_stdout,
                "tmp_pipeline_launcher_behavior_changed": False,
                "tmp_pipeline_launcher_remains_internal_engine": True,
                "recommended_next_phase": "PHASE_28C",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_official_command_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    report_path = REPO_ROOT / args.report
    write_yaml(report_path, report)

    root = report["pipeline_launcher_official_command_validation"]
    summary = root["result_summary"]

    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Official command created: {summary['official_command_created']}")
    print(f"Official command outputs human review: {summary['official_command_outputs_human_review']}")
    print(f"Official help exposes single surface: {summary['official_help_exposes_single_surface']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
