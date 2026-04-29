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

from docs.patcher.shared.pipeline_launcher.governance_backlog import (
    build_governance_backlog_scope_summary,
)
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")
MODULE = Path("docs/patcher/shared/pipeline_launcher/governance_backlog.py")
OFFICIAL = Path("docs/patcher/shared/pipeline_launcher/cli.py")
TMP = Path("tmp/pipeline_launcher.py")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str]) -> tuple[int, str, str]:
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

    for path in [ENGINE, MODULE, OFFICIAL, TMP]:
        full = REPO_ROOT / path
        if not full.exists():
            findings.append({"finding_id": "MISSING_FILE", "severity": "blocking", "path": str(path)})
            continue
        try:
            py_compile.compile(str(full), doraise=True)
        except Exception as exc:
            findings.append({
                "finding_id": "PY_COMPILE_FAILED",
                "severity": "blocking",
                "path": str(path),
                "detail": str(exc),
            })

    engine_text = (REPO_ROOT / ENGINE).read_text(encoding="utf-8") if (REPO_ROOT / ENGINE).exists() else ""
    module_text = (REPO_ROOT / MODULE).read_text(encoding="utf-8") if (REPO_ROOT / MODULE).exists() else ""

    # After PHASE_28D10 engine cleanup, engine.py no longer needs to import
    # governance_backlog.py directly. D2 must only ensure that governance backlog
    # helpers were extracted out of engine.py and remain available through governance_backlog.py.

    governance_defs = [
        "def build_governance_backlog_scope_summary",
        "def attach_governance_backlog_signal",
        "def compact_governance_backlog_signal",
        "def empty_governance_backlog_signal",
    ]
    for snippet in governance_defs:
        if snippet in engine_text:
            findings.append({
                "finding_id": "ENGINE_STILL_DEFINES_GOVERNANCE_HELPER",
                "severity": "blocking",
                "snippet": snippet,
            })
        if snippet not in module_text:
            findings.append({
                "finding_id": "MODULE_MISSING_GOVERNANCE_HELPER",
                "severity": "blocking",
                "snippet": snippet,
            })

    summary = build_governance_backlog_scope_summary(REPO_ROOT)
    patch_lifecycle = summary.get("patch_lifecycle", {})
    if patch_lifecycle.get("direct_open_count") != 4:
        findings.append({
            "finding_id": "UNEXPECTED_PATCH_LIFECYCLE_OPEN_COUNT",
            "severity": "blocking",
            "actual": patch_lifecycle.get("direct_open_count"),
        })

    official_rc, official_stdout, official_stderr = run([sys.executable, str(OFFICIAL)])
    engine_rc, engine_stdout, engine_stderr = run([sys.executable, str(ENGINE)])
    tmp_rc, tmp_stdout, tmp_stderr = run([sys.executable, str(TMP)])
    raw_rc, raw_stdout, raw_stderr = run([sys.executable, str(OFFICIAL), "--raw-signals-overlay"])

    for name, rc, stderr in [
        ("official", official_rc, official_stderr),
        ("engine", engine_rc, engine_stderr),
        ("tmp", tmp_rc, tmp_stderr),
        ("raw", raw_rc, raw_stderr),
    ]:
        if rc != 0:
            findings.append({
                "finding_id": "COMMAND_FAILED",
                "severity": "blocking",
                "command": name,
                "returncode": rc,
                "stderr_excerpt": stderr[:500],
            })

    if "governance_backlog_scope_summary:" not in engine_stdout:
        findings.append({"finding_id": "ENGINE_OUTPUT_MISSING_GOVERNANCE_SUMMARY", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in official_stdout:
        findings.append({"finding_id": "OFFICIAL_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in tmp_stdout:
        findings.append({"finding_id": "TMP_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in raw_stdout:
        findings.append({"finding_id": "RAW_MISSING_OVERLAY", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" in engine_stdout:
        findings.append({"finding_id": "ENGINE_SHOULD_NOT_APPEND_HUMAN_REVIEW", "severity": "blocking"})

    return {
        "pipeline_launcher_governance_backlog_extraction_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D2",
            "purpose": "Extract governance backlog launcher helpers from engine.py into governance_backlog.py.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "governance_backlog_helpers_extracted",
                "tmp_pipeline_launcher": "compatibility_wrapper_preserved",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "artifacts": {
                "governance_backlog_module": str(MODULE).replace("\\", "/"),
                "engine": str(ENGINE).replace("\\", "/"),
                "official_command": str(OFFICIAL).replace("\\", "/"),
                "tmp_wrapper": str(TMP).replace("\\", "/"),
            },
            "inputs": [
                {"ref": str(path).replace("\\", "/"), "sha256": sha256_file(REPO_ROOT / path)}
                for path in [ENGINE, MODULE, OFFICIAL, TMP]
                if (REPO_ROOT / path).exists()
            ],
            "backlog_summary_sample": {"patch_lifecycle": patch_lifecycle},
            "blocking_findings": findings,
            "result_summary": {
                "governance_backlog_module_created": (REPO_ROOT / MODULE).exists(),
                "engine_imports_governance_backlog_module": "from docs.patcher.shared.pipeline_launcher.governance_backlog import" in engine_text,
                "engine_defines_governance_backlog_functions": "def build_governance_backlog_scope_summary" in engine_text,
                "patch_lifecycle_direct_open_count": patch_lifecycle.get("direct_open_count"),
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_stdout,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_stdout and "PIPELINE_SIGNALS_REVIEW:" not in engine_stdout,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_stdout,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_stdout,
                "recommended_next_phase": "PHASE_28D3",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        default="docs/registry/reports/pipeline_launcher_governance_backlog_extraction_validation.yaml",
    )
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)

    root = report["pipeline_launcher_governance_backlog_extraction_validation"]
    summary = root["result_summary"]

    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Governance backlog module created: {summary['governance_backlog_module_created']}")
    print(f"Engine imports governance backlog module: {summary['engine_imports_governance_backlog_module']}")
    print(f"Engine defines governance backlog functions: {summary['engine_defines_governance_backlog_functions']}")
    print(f"Patch lifecycle direct open count: {summary['patch_lifecycle_direct_open_count']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
