\
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from docs.patcher.shared.pipeline_launcher.yaml_io import write_yaml
from docs.patcher.shared.validate_pipeline_launcher_engine_promotion import build_report as build_engine_report


def build_report() -> dict[str, Any]:
    engine_root = build_engine_report()["pipeline_launcher_engine_promotion_validation"]
    summary = engine_root.get("result_summary", {})
    findings = list(engine_root.get("blocking_findings", []) or [])

    return {
        "pipeline_launcher_with_signals_validation": {
            "schema_version": "0.6",
            "generated_at": engine_root.get("generated_at"),
            "status": "PASS" if not findings else "FAIL",
            "phase_id": "PHASE_28C_COMPAT",
            "purpose": "Compatibility validation for pipeline_launcher_with_signals.py after engine promotion.",
            "source_validation": {
                "ref": "docs/registry/reports/pipeline_launcher_engine_promotion_validation.yaml",
                "phase_id": "PHASE_28C",
            },
            "mutation_policy": engine_root.get("mutation_policy", {}),
            "blocking_findings": findings,
            "result_summary": {
                "has_attention_signals": True,
                "wrapper_outputs_human_review": summary.get("official_command_outputs_human_review"),
                "wrapper_outputs_copyable_prompt": summary.get("official_command_outputs_human_review"),
                "raw_overlay_available_with_flag": summary.get("raw_overlay_available_with_flag"),
                "launcher_authorizes_run_from_signals": False,
                "tmp_pipeline_launcher_behavior_changed": True,
                "tmp_pipeline_launcher_new_role": "compatibility_wrapper",
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
    print(f"tmp role: {summary['tmp_pipeline_launcher_new_role']}")
    print(f"Blocking findings: {summary['blocking_finding_count']}")
    return 0 if root["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
