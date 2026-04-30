#!/usr/bin/env python3
"""Validate the generic pipeline hardening reference artifacts."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Dict, List

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required.") from exc


REQUIRED_FILES = [
    "docs/specs/pipeline_hardening_model.md",
    "docs/specs/pipeline_hardening_checklist.md",
    "docs/pipelines/_templates/hardened_pipeline/pipeline.md",
    "docs/pipelines/_templates/hardened_pipeline/AI_PROTOCOL.yaml",
    "docs/pipelines/_templates/hardened_pipeline/entry_actions/OPEN.action.yaml",
    "docs/pipelines/_templates/hardened_pipeline/entry_actions/MATERIALIZE.action.yaml",
    "docs/pipelines/_templates/hardened_pipeline/entry_actions/CONTINUE.action.yaml",
    "docs/pipelines/_templates/hardened_pipeline/entry_actions/RECONCILE.action.yaml",
    "docs/pipelines/_templates/hardened_pipeline/stages/STAGE_00_INTAKE.skill.yaml",
    "docs/pipelines/_templates/hardened_pipeline/stages/STAGE_01_VALIDATION.skill.yaml",
]

REQUIRED_TERMS = {
    "docs/specs/pipeline_hardening_model.md": [
        "L1",
        "L2",
        "L3",
        "L4",
        "Constitution pipeline is the reference L4 pipeline",
        "forbidden_direct_writes",
        "baseline_capture",
        "pre_release_preview",
        "final_closeout_score",
    ],
    "docs/specs/pipeline_hardening_checklist.md": [
        "L1",
        "L2",
        "L3",
        "L4",
        "can_release",
        "can_promote",
        "can_close",
    ],
    "docs/pipelines/_templates/hardened_pipeline/AI_PROTOCOL.yaml": [
        "forbidden_direct_writes",
        "deterministic_script_policy",
        "anti_patterns",
    ],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Dict:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def validate(repo_root: Path) -> Dict:
    findings: List[Dict] = []
    files = []

    for rel in REQUIRED_FILES:
        path = repo_root / rel
        exists = path.exists()
        files.append({
            "path": rel,
            "exists": exists,
            "sha256": sha256(path) if exists else None,
        })
        if not exists:
            findings.append({"severity": "blocking", "path": rel, "message": "required file missing"})

    for rel, terms in REQUIRED_TERMS.items():
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            if term not in text:
                findings.append({"severity": "blocking", "path": rel, "message": f"required term missing: {term}"})

    for rel in REQUIRED_FILES:
        if not rel.endswith((".yaml", ".yml")):
            continue
        path = repo_root / rel
        if not path.exists():
            continue
        data = load_yaml(path)
        if not data:
            findings.append({"severity": "blocking", "path": rel, "message": "YAML file is empty or not a mapping"})

    blocking = [item for item in findings if item["severity"] == "blocking"]
    return {
        "pipeline_hardening_reference_validation": {
            "schema_version": 0.1,
            "status": "PASS" if not blocking else "FAIL",
            "validated_scope": "reference_model_and_template",
            "required_file_count": len(REQUIRED_FILES),
            "present_file_count": sum(1 for item in files if item["exists"]),
            "files": files,
            "blocking_findings": blocking,
            "blocking_finding_count": len(blocking),
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report", default="docs/registry/reports/pipeline_hardening_reference_validation.yaml")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if not (repo_root / "docs").exists():
        raise SystemExit("ERROR: run from repository root or pass --repo-root")

    report = validate(repo_root)
    report_path = repo_root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")

    status = report["pipeline_hardening_reference_validation"]["status"]
    print(f"Wrote {report_path.relative_to(repo_root).as_posix()}")
    print(f"status: {status}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
