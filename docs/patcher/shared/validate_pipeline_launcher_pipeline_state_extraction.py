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

from docs.patcher.shared.pipeline_launcher.pipeline_state import (
    discover_constitution,
    discover_generic_pipeline,
)
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")
MODULE = Path("docs/patcher/shared/pipeline_launcher/pipeline_state.py")
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

    if "from docs.patcher.shared.pipeline_launcher.pipeline_state import" not in engine_text:
        findings.append({"finding_id": "ENGINE_PIPELINE_STATE_IMPORT_MISSING", "severity": "blocking"})

    for snippet in [
        "def enrich_scope_maturity",
        "def sort_scopes_by_maturity",
        "def build_maturity_summary",
        "def discover_constitution",
        "def discover_generic_pipeline",
    ]:
        if snippet in engine_text:
            findings.append({"finding_id": "ENGINE_STILL_DEFINES_PIPELINE_STATE_HELPER", "severity": "blocking", "snippet": snippet})
        if snippet not in module_text:
            findings.append({"finding_id": "PIPELINE_STATE_MODULE_MISSING_SNIPPET", "severity": "blocking", "snippet": snippet})

    constitution_state = discover_constitution(REPO_ROOT)
    if constitution_state.get("pipeline_id") != "constitution":
        findings.append({"finding_id": "CONSTITUTION_STATE_PIPELINE_ID_MISMATCH", "severity": "blocking", "actual": constitution_state.get("pipeline_id")})
    if "maturity_summary" not in constitution_state:
        findings.append({"finding_id": "CONSTITUTION_STATE_MISSING_MATURITY_SUMMARY", "severity": "blocking"})
    if "published_scopes" not in constitution_state or not constitution_state.get("published_scopes"):
        findings.append({"finding_id": "CONSTITUTION_STATE_MISSING_PUBLISHED_SCOPES", "severity": "blocking"})
    if constitution_state.get("active_runs_count") != 0:
        findings.append({"finding_id": "CONSTITUTION_ACTIVE_RUN_COUNT_UNEXPECTED", "severity": "blocking", "actual": constitution_state.get("active_runs_count")})

    generic_state = discover_generic_pipeline(REPO_ROOT, "release")
    if generic_state.get("pipeline_id") != "release":
        findings.append({"finding_id": "GENERIC_STATE_PIPELINE_ID_MISMATCH", "severity": "blocking", "actual": generic_state.get("pipeline_id")})
    if "active_runs_count" not in generic_state:
        findings.append({"finding_id": "GENERIC_STATE_MISSING_ACTIVE_RUN_COUNT", "severity": "blocking"})

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

    if "PIPELINE_REGISTRY_STATE:" not in engine_out:
        findings.append({"finding_id": "ENGINE_MISSING_REGISTRY_STATE", "severity": "blocking"})
    if "PIPELINE_LAUNCH_MENU:" not in engine_out or "PIPELINE_SIGNALS_REVIEW:" in engine_out:
        findings.append({"finding_id": "ENGINE_OUTPUT_INVALID", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in official_out:
        findings.append({"finding_id": "OFFICIAL_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_REVIEW:" not in tmp_out:
        findings.append({"finding_id": "TMP_MISSING_SIGNALS_REVIEW", "severity": "blocking"})
    if "PIPELINE_SIGNALS_OVERLAY_RAW:" not in raw_out:
        findings.append({"finding_id": "RAW_MISSING_SIGNALS_OVERLAY", "severity": "blocking"})

    return {
        "pipeline_launcher_pipeline_state_extraction_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D8",
            "purpose": "Extract pipeline state discovery helpers from engine.py into pipeline_state.py without changing launch menu behavior.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "pipeline_state_helpers_extracted",
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
            "state_samples": {
                "constitution": {
                    "active_runs_count": constitution_state.get("active_runs_count"),
                    "published_scope_count": len(constitution_state.get("published_scopes") or []),
                    "recommended_action": constitution_state.get("recommended_action"),
                    "has_governance_backlog_scope_summary": "governance_backlog_scope_summary" in constitution_state,
                },
                "release": {
                    "active_runs_count": generic_state.get("active_runs_count"),
                    "recommended_action": generic_state.get("recommended_action"),
                },
            },
            "blocking_findings": findings,
            "result_summary": {
                "pipeline_state_module_created": (REPO_ROOT / MODULE).exists(),
                "engine_imports_pipeline_state_module": "from docs.patcher.shared.pipeline_launcher.pipeline_state import" in engine_text,
                "engine_defines_pipeline_state_helpers": any(
                    snippet in engine_text
                    for snippet in [
                        "def enrich_scope_maturity",
                        "def discover_constitution",
                        "def discover_generic_pipeline",
                    ]
                ),
                "constitution_active_runs_count": constitution_state.get("active_runs_count"),
                "constitution_published_scope_count": len(constitution_state.get("published_scopes") or []),
                "constitution_recommended_action": constitution_state.get("recommended_action"),
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_out,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_out and "PIPELINE_SIGNALS_REVIEW:" not in engine_out,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_out,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_out,
                "recommended_next_phase": "PHASE_28D9",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_pipeline_state_extraction_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)
    root = report["pipeline_launcher_pipeline_state_extraction_validation"]
    summary = root["result_summary"]
    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Pipeline state module created: {summary['pipeline_state_module_created']}")
    print(f"Engine imports pipeline state module: {summary['engine_imports_pipeline_state_module']}")
    print(f"Engine defines pipeline state helpers: {summary['engine_defines_pipeline_state_helpers']}")
    print(f"Constitution active runs count: {summary['constitution_active_runs_count']}")
    print(f"Constitution published scope count: {summary['constitution_published_scope_count']}")
    print(f"Constitution recommended action: {summary['constitution_recommended_action']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
