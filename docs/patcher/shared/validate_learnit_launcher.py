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

# Allow execution as `python docs/patcher/shared/validate_learnit_launcher.py`
# while importing the local docs.* namespace from the repository root.
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.learnit_launcher.pipeline_signals import (
    build_launcher_signal_summary,
    build_next_best_action_slot,
    build_pipeline_signal_slots,
    build_review_action_slot,
    compact_prompt_binding,
)
from docs.patcher.shared.learnit_launcher.registry import discover_pipelines
from docs.patcher.shared.learnit_launcher.yaml_io import write_yaml


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report(repo_root: Path) -> dict[str, Any]:
    registry_path = repo_root / "docs" / "registry" / "pipelines.md"
    launcher_path = repo_root / "tmp" / "pipeline_launcher.py"

    pipelines = discover_pipelines(registry_path)
    pipeline_ids = [str(pipeline.get("pipeline_id", "")) for pipeline in pipelines if pipeline.get("pipeline_id")]

    signal_slots = build_pipeline_signal_slots(repo_root, pipeline_ids)
    signal_summary = build_launcher_signal_summary(signal_slots)
    review_action = build_review_action_slot(signal_summary)
    next_best_action = build_next_best_action_slot(signal_summary)
    prompt_binding = compact_prompt_binding(signal_summary)

    findings: list[dict[str, Any]] = []

    if len(pipeline_ids) != 4:
        findings.append(
            {
                "finding_id": "UNEXPECTED_PIPELINE_COUNT",
                "severity": "blocking",
                "expected": 4,
                "actual": len(pipeline_ids),
            }
        )

    provider_by_pipeline = {slot["pipeline_id"]: slot["provider"] for slot in signal_slots}
    if provider_by_pipeline.get("constitution") != "implemented":
        findings.append(
            {
                "finding_id": "CONSTITUTION_SIGNALS_PROVIDER_NOT_IMPLEMENTED",
                "severity": "blocking",
                "actual": provider_by_pipeline.get("constitution"),
            }
        )

    if signal_summary.get("has_attention_signals") is not True:
        findings.append(
            {
                "finding_id": "NO_ATTENTION_SIGNAL_FOUND",
                "severity": "blocking",
                "detail": "Expected constitution backlog attention signal.",
            }
        )

    if signal_summary.get("recommended_default_hint") != "review_pipeline_signals":
        findings.append(
            {
                "finding_id": "UNEXPECTED_RECOMMENDED_DEFAULT_HINT",
                "severity": "blocking",
                "actual": signal_summary.get("recommended_default_hint"),
            }
        )

    if signal_summary.get("run_opening_authorized_by_signals") is not False:
        findings.append(
            {
                "finding_id": "SIGNALS_MUST_NOT_AUTHORIZE_RUN_OPENING",
                "severity": "blocking",
            }
        )

    if "attention_signal_must_be_acknowledged" not in prompt_binding.get("pipeline_signals_handling", ""):
        findings.append(
            {
                "finding_id": "PROMPT_BINDING_MISSING_ATTENTION_ACK",
                "severity": "blocking",
            }
        )

    compile_status = "PASS"
    try:
        py_compile.compile(str(launcher_path), doraise=True)
    except Exception as exc:
        compile_status = "FAIL"
        findings.append(
            {
                "finding_id": "TMP_PIPELINE_LAUNCHER_COMPILE_FAILED",
                "severity": "blocking",
                "detail": str(exc),
            }
        )

    launcher_runtime_status = "not_run"
    launcher_runtime_excerpt = ""
    if compile_status == "PASS":
        completed = subprocess.run(
            [sys.executable, str(launcher_path)],
            check=False,
            text=True,
            capture_output=True,
            timeout=30,
        )
        launcher_runtime_status = "PASS" if completed.returncode == 0 else "FAIL"
        launcher_runtime_excerpt = (completed.stdout or completed.stderr or "")[:2500]
        if completed.returncode != 0:
            findings.append(
                {
                    "finding_id": "TMP_PIPELINE_LAUNCHER_RUNTIME_FAILED",
                    "severity": "blocking",
                    "returncode": completed.returncode,
                }
            )

    module_files = [
        repo_root / "docs" / "patcher" / "shared" / "learnit_launcher" / "__init__.py",
        repo_root / "docs" / "patcher" / "shared" / "learnit_launcher" / "yaml_io.py",
        repo_root / "docs" / "patcher" / "shared" / "learnit_launcher" / "registry.py",
        repo_root / "docs" / "patcher" / "shared" / "learnit_launcher" / "pipeline_signals.py",
        repo_root / "docs" / "patcher" / "shared" / "validate_learnit_launcher.py",
    ]

    return {
        "learnit_launcher_modularization_validation": {
            "schema_version": "0.2",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_27A",
            "purpose": "Bootstrap a modular launcher runtime without changing tmp/pipeline_launcher.py behavior.",
            "mutation_policy": {
                "tmp_pipeline_launcher": "not_modified",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "modules": [
                {"ref": str(path.relative_to(repo_root)).replace("\\", "/"), "sha256": sha256_file(path)}
                for path in module_files
                if path.exists()
            ],
            "registry_pipeline_count": len(pipeline_ids),
            "pipeline_ids": pipeline_ids,
            "provider_by_pipeline": provider_by_pipeline,
            "signal_summary": signal_summary,
            "review_action_slot": review_action,
            "next_best_action_slot": next_best_action,
            "prompt_binding": prompt_binding,
            "tmp_pipeline_launcher_compile_status": compile_status,
            "tmp_pipeline_launcher_runtime_status": launcher_runtime_status,
            "tmp_pipeline_launcher_runtime_excerpt": launcher_runtime_excerpt,
            "blocking_findings": findings,
            "result_summary": {
                "has_attention_signals": signal_summary.get("has_attention_signals"),
                "recommended_default_hint": signal_summary.get("recommended_default_hint"),
                "launcher_authorizes_run_from_signals": False,
                "tmp_pipeline_launcher_behavior_changed": False,
                "blocking_finding_count": len(findings),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="docs/registry/reports/learnit_launcher_modularization_validation.yaml")
    args = parser.parse_args()

    repo_root = Path(".")
    report_path = Path(args.report)

    report = build_report(repo_root)
    write_yaml(report_path, report)

    root = report["learnit_launcher_modularization_validation"]
    summary = root["result_summary"]

    print(f"Status: {root['status']}")
    print(f"Wrote {report_path}")
    print(f"Registry pipelines: {root['registry_pipeline_count']}")
    print(f"Recommended default hint: {summary['recommended_default_hint']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
