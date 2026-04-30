#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import sys

try:
    import yaml
except Exception:
    yaml = None

REPO = Path.cwd()

REQUIRED_FILES = [
    "docs/pipelines/cross_core_contract/pipeline.md",
    "docs/pipelines/cross_core_contract/state.yaml",
    "docs/pipelines/cross_core_contract/signals.yaml",
    "docs/pipelines/cross_core_contract/README.md",
    "docs/pipelines/cross_core_contract/requests/README.md",
    "docs/pipelines/cross_core_contract/schemas/cross_core_change_request.schema.yaml",
    "docs/pipelines/cross_core_contract/reports/README.md",
]

FORBIDDEN_MUTATION_TARGETS = [
    "docs/cores/current/constitution.yaml",
    "docs/cores/current/referentiel.yaml",
    "docs/cores/current/link.yaml",
    "docs/pipelines/constitution/scope_catalog/governance_backlog.yaml",
]


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def add_finding(findings: list[dict], finding_id: str, severity: str, message: str, path: str | None = None) -> None:
    item = {"finding_id": finding_id, "severity": severity, "message": message}
    if path:
        item["path"] = path
    findings.append(item)


def dump_yaml(data: dict) -> str:
    if yaml is not None:
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120)
    return repr(data)


def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/registry/reports/cross_core_contract_pipeline_validation.yaml")
    findings: list[dict] = []
    checked_files: list[dict] = []

    for rel_path in REQUIRED_FILES:
        path = REPO / rel_path
        exists = path.exists()
        checked_files.append(
            {
                "path": rel_path,
                "exists": exists,
                "sha256": sha256_file(path) if exists else None,
            }
        )
        if not exists:
            add_finding(findings, "missing_required_file", "blocking", "Missing required skeleton file", rel_path)

    registry = read(REPO / "docs/registry/pipelines.md")
    if "### cross_core_contract" not in registry:
        add_finding(findings, "registry_missing_pipeline", "blocking", "Registry does not declare cross_core_contract", "docs/registry/pipelines.md")
    if "docs/pipelines/cross_core_contract/pipeline.md" not in registry:
        add_finding(findings, "registry_missing_pipeline_path", "blocking", "Registry does not point to pipeline.md", "docs/registry/pipelines.md")

    pipeline = read(REPO / "docs/pipelines/cross_core_contract/pipeline.md")
    for marker in [
        "id: cross_core_contract",
        "STAGE_00_INTAKE_AND_SHAPE_VALIDATION",
        "STAGE_02_CROSS_CORE_ARBITRAGE",
        "STAGE_05_RELEASE_AND_PROMOTION_PLANNING",
        "CCR_PATCH_LIFECYCLE_ESCALATION_THRESHOLD_N_R01",
        "GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R01",
        "GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R02",
    ]:
        if marker not in pipeline:
            add_finding(findings, "pipeline_missing_contract_marker", "blocking", f"Missing marker: {marker}", "docs/pipelines/cross_core_contract/pipeline.md")

    signals = read(REPO / "docs/pipelines/cross_core_contract/signals.yaml")
    for marker in ["pipeline_id: cross_core_contract", "signals_provider: not_implemented", "signals: []"]:
        if marker not in signals:
            add_finding(findings, "signals_invalid", "blocking", f"Missing marker: {marker}", "docs/pipelines/cross_core_contract/signals.yaml")

    schema = read(REPO / "docs/pipelines/cross_core_contract/schemas/cross_core_change_request.schema.yaml")
    for marker in [
        "cross_core_change_request_schema:",
        "validate_multi_core_release_plan",
        "validate_multi_core_promotion_manifest",
        "backlog_closure: forbidden_until_validated_resolution",
    ]:
        if marker not in schema:
            add_finding(findings, "schema_missing_marker", "blocking", f"Missing marker: {marker}", "docs/pipelines/cross_core_contract/schemas/cross_core_change_request.schema.yaml")

    report = {
        "cross_core_contract_pipeline_validation": {
            "schema_version": "0.1",
            "generated_at": iso_now(),
            "status": "PASS" if not findings else "FAIL",
            "checked_files": checked_files,
            "forbidden_mutation_targets": FORBIDDEN_MUTATION_TARGETS,
            "blocking_findings": [item for item in findings if item["severity"] == "blocking"],
            "warning_findings": [item for item in findings if item["severity"] == "warning"],
            "result_summary": {
                "blocking_finding_count": sum(1 for item in findings if item["severity"] == "blocking"),
                "warning_finding_count": sum(1 for item in findings if item["severity"] == "warning"),
                "core_mutation_authorized": False,
                "constitution_run_opened": False,
            },
        }
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(dump_yaml(report), encoding="utf-8", newline="\n")

    status = report["cross_core_contract_pipeline_validation"]["status"]
    print(f"Status: {status}")
    print(f"Wrote {report_path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
