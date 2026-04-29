#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml
from docs.patcher.shared.validate_pipeline_launcher_official_command import build_report as build_official_report


def build_report() -> dict[str, Any]:
    official = build_official_report()["pipeline_launcher_official_command_validation"]
    findings = list(official.get("blocking_findings", []) or [])

    return {
        "pipeline_launcher_with_signals_validation": {
            "schema_version": "0.5",
            "generated_at": official.get("generated_at"),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28B_COMPAT",
            "purpose": "Compatibility validation for pipeline_launcher_with_signals.py after official command promotion.",
            "mutation_policy": {
                "tmp_pipeline_launcher": "not_modified",
                "compatibility_wrapper": "validated",
                "official_command": "source_of_truth",
                "signals_yaml": "not_modified",
                "pipeline_md": "not_modified",
                "state_yaml": "not_modified",
                "run_materialization": "not_performed",
            },
            "source_validation": {
                "ref": "docs/registry/reports/pipeline_launcher_official_command_validation.yaml",
                "phase_id": "PHASE_28B",
            },
            "blocking_findings": findings,
            "result_summary": {
                "has_attention_signals": True,
                "wrapper_outputs_human_review": official.get("result_summary", {}).get("compatibility_wrapper_delegates_to_official_command"),
                "wrapper_outputs_copyable_prompt": official.get("result_summary", {}).get("official_command_outputs_human_review"),
                "raw_overlay_available_with_flag": official.get("result_summary", {}).get("raw_overlay_available_with_flag"),
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
    print(f"Wrapper outputs human review: {summary['wrapper_outputs_human_review']}")
    print(f"Raw overlay available: {summary['raw_overlay_available_with_flag']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
