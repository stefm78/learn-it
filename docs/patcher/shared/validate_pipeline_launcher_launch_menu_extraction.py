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

from docs.patcher.shared.pipeline_launcher.launch_menu import (
    build_menu,
    build_open_new_actions,
    build_parallel_slots,
)
from docs.patcher.shared.pipeline_launcher.pipeline_state import discover_constitution
from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

ENGINE = Path("docs/patcher/shared/pipeline_launcher/engine.py")
MODULE = Path("docs/patcher/shared/pipeline_launcher/launch_menu.py")
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

    if "from docs.patcher.shared.pipeline_launcher.launch_menu import" not in engine_text:
        findings.append({"finding_id": "ENGINE_LAUNCH_MENU_IMPORT_MISSING", "severity": "blocking"})

    for snippet in [
        "def _scope_choice_entry",
        "def build_continue_actions",
        "def build_open_new_actions",
        "def build_disambiguation_actions",
        "def build_consolidate_actions",
        "def build_menu",
        "def build_parallel_slots",
    ]:
        if snippet in engine_text:
            findings.append({"finding_id": "ENGINE_STILL_DEFINES_LAUNCH_MENU_HELPER", "severity": "blocking", "snippet": snippet})
        if snippet not in module_text:
            findings.append({"finding_id": "LAUNCH_MENU_MODULE_MISSING_SNIPPET", "severity": "blocking", "snippet": snippet})

    state = discover_constitution(REPO_ROOT)
    menu = build_menu(REPO_ROOT, "feat/core-modularization-bootstrap", state, "docs/pipelines/constitution/pipeline.md")
    if "decision_summary" not in menu or "next_best_actions" not in menu:
        findings.append({"finding_id": "BUILD_MENU_SHAPE_INVALID", "severity": "blocking"})
    if menu.get("next_best_actions", {}).get("new_run", {}).get("run_opening_authorized") is not False:
        findings.append({"finding_id": "BUILD_MENU_SHOULD_NOT_AUTHORIZE_NEW_RUN", "severity": "blocking"})

    registry_pipelines = [
        {
            "pipeline_id": "constitution",
            "path": "docs/pipelines/constitution/pipeline.md",
            "goal": "test",
            "canonical_state": "docs/pipelines/constitution/state.yaml",
        }
    ]
    slots = build_parallel_slots(REPO_ROOT, "feat/core-modularization-bootstrap", registry_pipelines, {"constitution": state}, 1)
    if "slots" not in slots or "parallel_slots_requested" not in slots:
        findings.append({"finding_id": "BUILD_PARALLEL_SLOTS_SHAPE_INVALID", "severity": "blocking"})

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
        "pipeline_launcher_launch_menu_extraction_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28D9",
            "purpose": "Extract launch menu and parallel slot builders from engine.py into launch_menu.py.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "launch_menu_helpers_extracted",
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
            "menu_sample": {
                "recommended_default": menu.get("decision_summary", {}).get("recommended_default"),
                "new_run_status": menu.get("next_best_actions", {}).get("new_run", {}).get("status"),
                "new_run_authorized": menu.get("next_best_actions", {}).get("new_run", {}).get("run_opening_authorized"),
            },
            "parallel_slots_sample": {
                "parallel_slots_requested": slots.get("parallel_slots_requested"),
                "parallel_slots_available": slots.get("parallel_slots_available"),
            },
            "blocking_findings": findings,
            "result_summary": {
                "launch_menu_module_created": (REPO_ROOT / MODULE).exists(),
                "engine_imports_launch_menu_module": "from docs.patcher.shared.pipeline_launcher.launch_menu import" in engine_text,
                "engine_defines_launch_menu_helpers": any(
                    snippet in engine_text
                    for snippet in [
                        "def build_menu",
                        "def build_parallel_slots",
                        "def build_open_new_actions",
                    ]
                ),
                "build_menu_returns_next_best_actions": "next_best_actions" in menu,
                "build_menu_keeps_new_run_non_authorizing": menu.get("next_best_actions", {}).get("new_run", {}).get("run_opening_authorized") is False,
                "build_parallel_slots_returns_slots": "slots" in slots,
                "official_command_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in official_out,
                "engine_outputs_raw_launcher_without_human_review": "PIPELINE_LAUNCH_MENU:" in engine_out and "PIPELINE_SIGNALS_REVIEW:" not in engine_out,
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in tmp_out,
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in raw_out,
                "recommended_next_phase": "PHASE_28D10",
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_launch_menu_extraction_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)
    root = report["pipeline_launcher_launch_menu_extraction_validation"]
    summary = root["result_summary"]
    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Launch menu module created: {summary['launch_menu_module_created']}")
    print(f"Engine imports launch menu module: {summary['engine_imports_launch_menu_module']}")
    print(f"Engine defines launch menu helpers: {summary['engine_defines_launch_menu_helpers']}")
    print(f"Build menu returns next_best_actions: {summary['build_menu_returns_next_best_actions']}")
    print(f"Build menu keeps new_run non-authorizing: {summary['build_menu_keeps_new_run_non_authorizing']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
