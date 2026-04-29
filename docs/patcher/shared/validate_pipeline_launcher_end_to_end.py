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

from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml

PY_FILES = [
    Path("docs/patcher/shared/pipeline_launcher/__init__.py"),
    Path("docs/patcher/shared/pipeline_launcher/cli.py"),
    Path("docs/patcher/shared/pipeline_launcher/engine.py"),
    Path("docs/patcher/shared/pipeline_launcher/overlay.py"),
    Path("docs/patcher/shared/pipeline_launcher/pipeline_signals.py"),
    Path("docs/patcher/shared/pipeline_launcher/maturity.py"),
    Path("docs/patcher/shared/pipeline_launcher/governance_backlog.py"),
    Path("docs/patcher/shared/pipeline_launcher/bounded_preflight.py"),
    Path("docs/patcher/shared/pipeline_launcher/entry_actions.py"),
    Path("docs/patcher/shared/pipeline_launcher/run_context.py"),
    Path("docs/patcher/shared/pipeline_launcher/consolidation.py"),
    Path("docs/patcher/shared/pipeline_launcher/registry.py"),
    Path("docs/patcher/shared/pipeline_launcher/pipeline_state.py"),
    Path("docs/patcher/shared/pipeline_launcher/launch_menu.py"),
    Path("docs/patcher/shared/pipeline_launcher/yaml_io.py"),
    Path("docs/patcher/shared/pipeline_launcher_with_signals.py"),
    Path("tmp/pipeline_launcher.py"),
]

VALIDATOR_FILES = [
    Path("docs/patcher/shared/validate_pipeline_launcher.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_official_command.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_engine_promotion.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_maturity_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_governance_backlog_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_bounded_preflight_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_entry_actions_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_run_context_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_consolidation_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_registry_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_pipeline_state_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_launch_menu_extraction.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_engine_cleanup.py"),
    Path("docs/patcher/shared/validate_pipeline_launcher_with_signals.py"),
    Path("docs/patcher/shared/validate_pipeline_signals.py"),
]

REPORTS = [
    ("pipeline_signals", Path("docs/registry/reports/pipeline_signals_validation.yaml"), "pipeline_signals_validation", None),
    ("modularization", Path("docs/registry/reports/pipeline_launcher_modularization_validation.yaml"), "pipeline_launcher_modularization_validation", None),
    ("with_signals", Path("docs/registry/reports/pipeline_launcher_with_signals_validation.yaml"), "pipeline_launcher_with_signals_validation", None),
    ("official_command", Path("docs/registry/reports/pipeline_launcher_official_command_validation.yaml"), "pipeline_launcher_official_command_validation", "PHASE_28C_COMPAT"),
    ("engine_promotion", Path("docs/registry/reports/pipeline_launcher_engine_promotion_validation.yaml"), "pipeline_launcher_engine_promotion_validation", "PHASE_28D_COMPAT"),
    ("D1_maturity", Path("docs/registry/reports/pipeline_launcher_maturity_extraction_validation.yaml"), "pipeline_launcher_maturity_extraction_validation", "PHASE_28D1"),
    ("D2_governance_backlog", Path("docs/registry/reports/pipeline_launcher_governance_backlog_extraction_validation.yaml"), "pipeline_launcher_governance_backlog_extraction_validation", "PHASE_28D2"),
    ("D3_bounded_preflight", Path("docs/registry/reports/pipeline_launcher_bounded_preflight_extraction_validation.yaml"), "pipeline_launcher_bounded_preflight_extraction_validation", "PHASE_28D3"),
    ("D4_entry_actions", Path("docs/registry/reports/pipeline_launcher_entry_actions_extraction_validation.yaml"), "pipeline_launcher_entry_actions_extraction_validation", "PHASE_28D4"),
    ("D5_run_context", Path("docs/registry/reports/pipeline_launcher_run_context_extraction_validation.yaml"), "pipeline_launcher_run_context_extraction_validation", "PHASE_28D5"),
    ("D6_consolidation", Path("docs/registry/reports/pipeline_launcher_consolidation_extraction_validation.yaml"), "pipeline_launcher_consolidation_extraction_validation", "PHASE_28D6"),
    ("D7_registry", Path("docs/registry/reports/pipeline_launcher_registry_extraction_validation.yaml"), "pipeline_launcher_registry_extraction_validation", "PHASE_28D7"),
    ("D8_pipeline_state", Path("docs/registry/reports/pipeline_launcher_pipeline_state_extraction_validation.yaml"), "pipeline_launcher_pipeline_state_extraction_validation", "PHASE_28D8"),
    ("D9_launch_menu", Path("docs/registry/reports/pipeline_launcher_launch_menu_extraction_validation.yaml"), "pipeline_launcher_launch_menu_extraction_validation", "PHASE_28D9"),
    ("D10_engine_cleanup", Path("docs/registry/reports/pipeline_launcher_engine_cleanup_validation.yaml"), "pipeline_launcher_engine_cleanup_validation", "PHASE_28D10"),
]


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(args, cwd=str(REPO_ROOT), check=False, text=True, capture_output=True, timeout=45)
    return completed.returncode, completed.stdout or "", completed.stderr or ""


def load_yaml(path: Path) -> dict[str, Any]:
    import yaml
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def report_status(path: Path, root_key: str) -> tuple[str | None, str | None, int | None]:
    doc = load_yaml(REPO_ROOT / path)
    root = doc.get(root_key) if isinstance(doc, dict) else None
    if not isinstance(root, dict):
        return None, None, None
    summary = root.get("result_summary") or {}
    return root.get("status"), root.get("phase_id"), summary.get("blocking_finding_count")


def build_report() -> dict[str, Any]:
    findings: list[dict[str, Any]] = []

    # Compile runtime modules and validators.
    for path in [*PY_FILES, *VALIDATOR_FILES]:
        full = REPO_ROOT / path
        if not full.exists():
            findings.append({"finding_id": "MISSING_PY_FILE", "severity": "blocking", "path": str(path)})
            continue
        try:
            py_compile.compile(str(full), doraise=True)
        except Exception as exc:
            findings.append({"finding_id": "PY_COMPILE_FAILED", "severity": "blocking", "path": str(path), "detail": str(exc)})

    # Validate reports.
    report_summaries: list[dict[str, Any]] = []
    for label, path, root_key, expected_phase in REPORTS:
        full = REPO_ROOT / path
        if not full.exists():
            findings.append({"finding_id": "MISSING_REPORT", "severity": "blocking", "label": label, "path": str(path)})
            continue
        status, phase_id, blocking_count = report_status(path, root_key)
        report_summaries.append({
            "label": label,
            "path": str(path).replace("\\", "/"),
            "status": status,
            "phase_id": phase_id,
            "blocking_finding_count": blocking_count,
        })
        if status != "PASS":
            findings.append({"finding_id": "REPORT_STATUS_NOT_PASS", "severity": "blocking", "label": label, "status": status})
        if expected_phase is not None and phase_id != expected_phase:
            findings.append({
                "finding_id": "REPORT_PHASE_MISMATCH",
                "severity": "blocking",
                "label": label,
                "expected": expected_phase,
                "actual": phase_id,
            })
        if blocking_count not in (0, None):
            findings.append({
                "finding_id": "REPORT_HAS_BLOCKING_FINDINGS",
                "severity": "blocking",
                "label": label,
                "blocking_finding_count": blocking_count,
            })

    # Runtime smoke tests.
    smoke_commands = {
        "official_cli": [sys.executable, "docs/patcher/shared/pipeline_launcher/cli.py"],
        "official_module": [sys.executable, "-m", "docs.patcher.shared.pipeline_launcher.cli"],
        "engine_direct": [sys.executable, "docs/patcher/shared/pipeline_launcher/engine.py"],
        "engine_parallel": [sys.executable, "docs/patcher/shared/pipeline_launcher/engine.py", "--parallel-runs", "2"],
        "tmp_wrapper": [sys.executable, "tmp/pipeline_launcher.py"],
        "compat_wrapper": [sys.executable, "docs/patcher/shared/pipeline_launcher_with_signals.py"],
        "raw_overlay": [sys.executable, "docs/patcher/shared/pipeline_launcher/cli.py", "--raw-signals-overlay"],
        "unsupported_pipeline": [sys.executable, "docs/patcher/shared/pipeline_launcher/engine.py", "--pipeline", "release"],
    }

    smoke_results: dict[str, dict[str, Any]] = {}
    for name, cmd in smoke_commands.items():
        rc, out, err = run(cmd)
        markers = [
            marker for marker in [
                "PIPELINE_REGISTRY_STATE:",
                "PIPELINE_LAUNCHER_STATE:",
                "PIPELINE_LAUNCH_MENU:",
                "PIPELINE_PARALLEL_SLOTS:",
                "PIPELINE_SIGNALS_REVIEW:",
                "PIPELINE_SIGNALS_OVERLAY_RAW:",
            ]
            if marker in out
        ]
        smoke_results[name] = {
            "returncode": rc,
            "markers": markers,
            "stderr_excerpt": err[:500],
        }
        if rc != 0:
            findings.append({"finding_id": "SMOKE_COMMAND_FAILED", "severity": "blocking", "command": name, "stderr_excerpt": err[:500]})

    expected_markers = {
        "official_cli": ["PIPELINE_REGISTRY_STATE:", "PIPELINE_LAUNCH_MENU:", "PIPELINE_SIGNALS_REVIEW:"],
        "official_module": ["PIPELINE_REGISTRY_STATE:", "PIPELINE_LAUNCH_MENU:", "PIPELINE_SIGNALS_REVIEW:"],
        "engine_direct": ["PIPELINE_REGISTRY_STATE:", "PIPELINE_LAUNCH_MENU:"],
        "engine_parallel": ["PIPELINE_REGISTRY_STATE:", "PIPELINE_PARALLEL_SLOTS:"],
        "tmp_wrapper": ["PIPELINE_REGISTRY_STATE:", "PIPELINE_LAUNCH_MENU:", "PIPELINE_SIGNALS_REVIEW:"],
        "compat_wrapper": ["PIPELINE_REGISTRY_STATE:", "PIPELINE_LAUNCH_MENU:", "PIPELINE_SIGNALS_REVIEW:"],
        "raw_overlay": ["PIPELINE_SIGNALS_OVERLAY_RAW:"],
        "unsupported_pipeline": ["PIPELINE_REGISTRY_STATE:", "PIPELINE_LAUNCH_MENU:"],
    }
    for name, markers in expected_markers.items():
        got = smoke_results.get(name, {}).get("markers", [])
        for marker in markers:
            if marker not in got:
                findings.append({"finding_id": "SMOKE_MARKER_MISSING", "severity": "blocking", "command": name, "marker": marker, "markers": got})

    # Key semantic checks from command output.
    official_out = run(smoke_commands["official_cli"])[1]
    if "run_opening_authorized: false" not in official_out and "run_opening_authorized_by_signals: false" not in official_out:
        findings.append({"finding_id": "OFFICIAL_OUTPUT_DOES_NOT_SHOW_NON_AUTHORIZATION", "severity": "warning"})

    engine_text = (REPO_ROOT / "docs/patcher/shared/pipeline_launcher/engine.py").read_text(encoding="utf-8")
    forbidden_engine_imports = [
        "from docs.patcher.shared.pipeline_launcher.maturity import",
        "from docs.patcher.shared.pipeline_launcher.governance_backlog import",
        "from docs.patcher.shared.pipeline_launcher.bounded_preflight import",
        "from docs.patcher.shared.pipeline_launcher.entry_actions import",
        "from docs.patcher.shared.pipeline_launcher.run_context import",
        "from docs.patcher.shared.pipeline_launcher.consolidation import",
        "from docs.patcher.shared.pipeline_launcher.yaml_io import load_yaml",
        "Still experimental: kept in tmp/",
    ]
    for snippet in forbidden_engine_imports:
        if snippet in engine_text:
            findings.append({"finding_id": "ENGINE_FORBIDDEN_SNIPPET_PRESENT", "severity": "blocking", "snippet": snippet})

    return {
        "pipeline_launcher_end_to_end_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not [f for f in findings if f.get("severity") == "blocking"] else "FAIL",
            "phase_id": "PHASE_28D11",
            "purpose": "Validate the promoted modular pipeline launcher end-to-end after PHASE_28D10 cleanup.",
            "mutation_policy": {
                "official_command": "preserved",
                "internal_engine": "no_functional_change",
                "tmp_pipeline_launcher": "compatibility_wrapper_preserved",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "runtime_artifacts": [
                {"ref": str(path).replace("\\", "/"), "sha256": sha256(REPO_ROOT / path)}
                for path in PY_FILES
                if (REPO_ROOT / path).exists()
            ],
            "validated_reports": report_summaries,
            "smoke_results": smoke_results,
            "blocking_findings": [f for f in findings if f.get("severity") == "blocking"],
            "warnings": [f for f in findings if f.get("severity") == "warning"],
            "result_summary": {
                "compiled_runtime_file_count": sum(1 for path in PY_FILES if (REPO_ROOT / path).exists()),
                "compiled_validator_file_count": sum(1 for path in VALIDATOR_FILES if (REPO_ROOT / path).exists()),
                "validated_report_count": len(report_summaries),
                "all_historical_reports_pass": all(r.get("status") == "PASS" and r.get("blocking_finding_count") in (0, None) for r in report_summaries),
                "official_cli_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in smoke_results.get("official_cli", {}).get("markers", []),
                "official_module_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in smoke_results.get("official_module", {}).get("markers", []),
                "engine_direct_outputs_raw_launcher": "PIPELINE_LAUNCH_MENU:" in smoke_results.get("engine_direct", {}).get("markers", []),
                "engine_parallel_slots_work": "PIPELINE_PARALLEL_SLOTS:" in smoke_results.get("engine_parallel", {}).get("markers", []),
                "tmp_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in smoke_results.get("tmp_wrapper", {}).get("markers", []),
                "compat_wrapper_outputs_human_review": "PIPELINE_SIGNALS_REVIEW:" in smoke_results.get("compat_wrapper", {}).get("markers", []),
                "raw_overlay_available_with_flag": "PIPELINE_SIGNALS_OVERLAY_RAW:" in smoke_results.get("raw_overlay", {}).get("markers", []),
                "unsupported_pipeline_fails_closed": "PIPELINE_LAUNCH_MENU:" in smoke_results.get("unsupported_pipeline", {}).get("markers", []),
                "engine_cleanup_preserved": not any(snippet in engine_text for snippet in forbidden_engine_imports),
                "recommended_next_phase": "STOP_OR_TARGETED_FUNCTIONAL_TESTS",
                "blocking_finding_count": len([f for f in findings if f.get("severity") == "blocking"]),
                "warning_count": len([f for f in findings if f.get("severity") == "warning"]),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/pipeline_launcher_end_to_end_validation.yaml")
    args = parser.parse_args()

    report = build_report()
    write_yaml(REPO_ROOT / args.report, report)
    root = report["pipeline_launcher_end_to_end_validation"]
    summary = root["result_summary"]
    print(f"Status: {root['status']}")
    print(f"Wrote {args.report}")
    print(f"Historical reports pass: {summary['all_historical_reports_pass']}")
    print(f"Official CLI outputs human review: {summary['official_cli_outputs_human_review']}")
    print(f"Official module outputs human review: {summary['official_module_outputs_human_review']}")
    print(f"Engine parallel slots work: {summary['engine_parallel_slots_work']}")
    print(f"TMP wrapper outputs human review: {summary['tmp_wrapper_outputs_human_review']}")
    print(f"Raw overlay available: {summary['raw_overlay_available_with_flag']}")
    print(f"Recommended next phase: {summary['recommended_next_phase']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    print(f"Warnings: {summary['warning_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
