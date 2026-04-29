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

from docs.patcher.shared.pipeline_launcher.consolidation import (
    build_bootstrap_command,
    detect_abnormal_state,
    detect_consolidation_ready,
    probe_integration_gate,
)
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")
MODULE = Path("docs/patcher/shared/pipeline_launcher/consolidation.py")
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

    if "from docs.patcher.shared.pipeline_launcher.consolidation import" not in engine_text:
        findings.append({"finding_id": "ENGINE_IMPORT_MISSING", "severity": "blocking"})

    for snippet in [
        "def probe_integration_gate",
        "def detect_consolidation_ready",
        "def detect_abnormal_state",
        "def build_bootstrap_command",
    ]:
        if snippet in engine_text:
            findings.append({"finding_id": "ENGINE_STILL_DEFINES_CONSOLIDATION_HELPER", "severity": "blocking", "snippet": snippet})
        if snippet not in module_text:
            findings.append({"finding_id": "MODULE_MISSING_CONSOLIDATION_HELPER", "severity": "blocking", "snippet": snippet})

    cmd = build_bootstrap_command(
        pipeline_id="constitution",
        run_id="CONSTITUTION_RUN_TEST",
        stage_id="STAGE_01_CHALLENGE",
        run_status="blocked",
        anomaly={"code": "run_status_abnormal", "reason": "run_status=blocked"},
    )
    for snippet in ["update_run_tracking.py", "--pipeline constitution", "--run-id CONSTITUTION_RUN_TEST"]:
        if snippet not in cmd:
            findings.append({"finding_id": "BOOTSTRAP_COMMAND_MISSING_SNIPPET", "severity": "blocking", "snippet": snippet})

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

    return {
        "pipeline_launcher_consolidation_extraction_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D6",
            "purpose": "Extract consolidation and anomaly helpers from engine.py into consolidation.py.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "consolidation_helpers_extracted",
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
            "bootstrap_command_sample": cmd,
            "blocking_findings": findings,
            "result_summary": {
                "consolidation_module_created": (REPO_ROOT / MODULE).exists(),
                "engine_imports_consolidation_module": "from docs.patcher.shared.pipeline_launcher.consolidation import" in engine_text,
                "engine_defines_consolidation_helpers": "def detect_consolidation_ready" in engine_text or "def detect_abnormal_state" in engine_text,
                "bootstrap_command_contains_update_run_tracking": "update_run_tracking.py" in cmd,
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_out,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_out and "PIPELINE_SIGNALS_REVIEW:" not in engine_out,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_out,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_out,
                "recommended_next_phase": "PHASE_28D7",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_consolidation_extraction_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)
    root = report["pipeline_launcher_consolidation_extraction_validation"]
    summary = root["result_summary"]
    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Consolidation module created: {summary['consolidation_module_created']}")
    print(f"Engine imports consolidation module: {summary['engine_imports_consolidation_module']}")
    print(f"Engine defines consolidation helpers: {summary['engine_defines_consolidation_helpers']}")
    print(f"Bootstrap command contains update_run_tracking: {summary['bootstrap_command_contains_update_run_tracking']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
