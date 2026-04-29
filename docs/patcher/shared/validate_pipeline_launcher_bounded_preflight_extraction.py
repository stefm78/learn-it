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

from docs.patcher.shared.pipeline_launcher.bounded_preflight import build_bounded_run_preflight_summary
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")
MODULE = Path("docs/patcher/shared/pipeline_launcher/bounded_preflight.py")
OFFICIAL = Path("docs/patcher/shared/pipeline_launcher/cli.py")
TMP = Path("tmp/pipeline_launcher.py")


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(args, cwd=str(REPO_ROOT), check=False, text=True, capture_output=True, timeout=30)
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
            findings.append({"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "path": str(path), "detail": str(exc)})

    engine_text = (REPO_ROOT / ENGINE).read_text(encoding="utf-8") if (REPO_ROOT / ENGINE).exists() else ""
    module_text = (REPO_ROOT / MODULE).read_text(encoding="utf-8") if (REPO_ROOT / MODULE).exists() else ""

    if "from docs.patcher.shared.pipeline_launcher.bounded_preflight import" not in engine_text:
        findings.append({"finding_id": "ENGINE_IMPORT_MISSING", "severity": "blocking"})
    if "def build_bounded_run_preflight_summary" in engine_text:
        findings.append({"finding_id": "ENGINE_STILL_DEFINES_PREFLIGHT_FUNCTION", "severity": "blocking"})
    if "def build_bounded_run_preflight_summary" not in module_text:
        findings.append({"finding_id": "MODULE_MISSING_PREFLIGHT_FUNCTION", "severity": "blocking"})

    summary = build_bounded_run_preflight_summary(REPO_ROOT)
    patch_lifecycle = summary.get("patch_lifecycle", {})
    acceptable_non_authorizing_statuses = {
        "PREFLIGHT_DEFER_TO_STAGE00_REVIEW",
        "PREFLIGHT_KEEP_BACKLOG_OPEN",
    }
    if patch_lifecycle.get("status") not in acceptable_non_authorizing_statuses:
        findings.append({
            "finding_id": "UNEXPECTED_PATCH_LIFECYCLE_PREFLIGHT_STATUS",
            "severity": "blocking",
            "actual": patch_lifecycle.get("status"),
            "expected_any_of": sorted(acceptable_non_authorizing_statuses),
        })
    if patch_lifecycle.get("new_bounded_run_recommended_now") is not False:
        findings.append({
            "finding_id": "PREFLIGHT_SHOULD_NOT_RECOMMEND_NEW_BOUNDED_RUN",
            "severity": "blocking",
            "actual": patch_lifecycle.get("new_bounded_run_recommended_now"),
        })
    if patch_lifecycle.get("matching_open_entry_count") != 4:
        findings.append({
            "finding_id": "UNEXPECTED_PATCH_LIFECYCLE_MATCHING_COUNT",
            "severity": "blocking",
            "actual": patch_lifecycle.get("matching_open_entry_count"),
        })
    if patch_lifecycle.get("open_new_run_authorized_by_default") is not False:
        findings.append({
            "finding_id": "PREFLIGHT_SHOULD_NOT_AUTHORIZE_OPEN_BY_DEFAULT",
            "severity": "blocking",
        })

    official_rc, official_out, official_err = run([sys.executable, str(OFFICIAL)])
    engine_rc, engine_out, engine_err = run([sys.executable, str(ENGINE)])
    tmp_rc, tmp_out, tmp_err = run([sys.executable, str(TMP)])
    raw_rc, raw_out, raw_err = run([sys.executable, str(OFFICIAL), "--raw-signals-overlay"])

    for name, rc, err in [
        ("official", official_rc, official_err),
        ("engine", engine_rc, engine_err),
        ("tmp", tmp_rc, tmp_err),
        ("raw", raw_rc, raw_err),
    ]:
        if rc != 0:
            findings.append({"finding_id": "COMMAND_FAILED", "severity": "blocking", "command": name, "returncode": rc, "stderr_excerpt": err[:500]})

    if "PIPELINE_SIGNALS_REVIEW:" not in official_out:
        findings.append({"finding_id": "OFFICIAL_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_LAUNCH_MENU:" not in engine_out or "PIPELINE_SIGNALS_REVIEW:" in engine_out:
        findings.append({"finding_id": "ENGINE_OUTPUT_INVALID", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in tmp_out:
        findings.append({"finding_id": "TMP_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in raw_out:
        findings.append({"finding_id": "RAW_MISSING_SIGNALS_OVERLAY", "severity": "blocking"})
    if "bounded_run_preflight_signal:" not in engine_out:
        findings.append({"finding_id": "ENGINE_MISSING_PREFLIGHT_SIGNAL", "severity": "blocking"})

    return {
        "pipeline_launcher_bounded_preflight_extraction_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D3",
            "purpose": "Extract bounded-run preflight launcher helpers from engine.py into bounded_preflight.py.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "bounded_preflight_helpers_extracted",
                "tmp_pipeline_launcher": "compatibility_wrapper_preserved",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "inputs": [
                {"ref": str(path).replace("\\", "/"), "sha256": sha256(REPO_ROOT / path)}
                for path in [ENGINE, MODULE, OFFICIAL, TMP]
                if (REPO_ROOT / path).exists()
            ],
            "preflight_summary_sample": {"patch_lifecycle": patch_lifecycle},
            "blocking_findings": findings,
            "result_summary": {
                "bounded_preflight_module_created": (REPO_ROOT / MODULE).exists(),
                "engine_imports_bounded_preflight_module": "from docs.patcher.shared.pipeline_launcher.bounded_preflight import" in engine_text,
                "engine_defines_bounded_preflight_functions": "def build_bounded_run_preflight_summary" in engine_text,
                "patch_lifecycle_preflight_status": patch_lifecycle.get("status"),
                "patch_lifecycle_matching_open_entry_count": patch_lifecycle.get("matching_open_entry_count"),
                "patch_lifecycle_open_authorized_by_default": patch_lifecycle.get("open_new_run_authorized_by_default"),
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_out,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_out and "PIPELINE_SIGNALS_REVIEW:" not in engine_out,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_out,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_out,
                "recommended_next_phase": "PHASE_28D4",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_bounded_preflight_extraction_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)
    root = report["pipeline_launcher_bounded_preflight_extraction_validation"]
    summary = root["result_summary"]
    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Bounded preflight module created: {summary['bounded_preflight_module_created']}")
    print(f"Engine imports bounded preflight module: {summary['engine_imports_bounded_preflight_module']}")
    print(f"Engine defines bounded preflight functions: {summary['engine_defines_bounded_preflight_functions']}")
    print(f"Patch lifecycle preflight status: {summary['patch_lifecycle_preflight_status']}")
    print(f"Patch lifecycle matching open count: {summary['patch_lifecycle_matching_open_entry_count']}")
    print(f"Open authorized by default: {summary['patch_lifecycle_open_authorized_by_default']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
