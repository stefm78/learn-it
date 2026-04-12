#!/usr/bin/env python3
"""Generate constitution scope catalog deterministically from canonical policy inputs.

This script reads:
- docs/pipelines/constitution/policies/scope_generation/policy.yaml
- docs/pipelines/constitution/policies/scope_generation/decisions.yaml
- current canonical cores

It produces:
- docs/pipelines/constitution/scope_catalog/manifest.yaml
- docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml
- a generation report

The generator is deterministic:
- same inputs => same outputs
- stable fingerprinting
- stable lexical ordering for ids and scopes
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run this script.") from exc


@dataclass(frozen=True)
class ScopeSeed:
    scope_key: str
    scope_id: str
    publication_status: str
    target_files: List[str]
    target_modules: List[str]
    neighbor_files: List[str]
    watchpoints: List[str]
    maturity: Dict[str, Any]
    notes: List[str]


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Top-level YAML object must be a mapping: {path}")
    return data


def dump_yaml(data: Dict[str, Any]) -> str:
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_source_fingerprint(repo_root: Path, refs: List[str]) -> str:
    hasher = hashlib.sha256()
    for ref in refs:
        path = repo_root / ref
        if not path.exists():
            raise FileNotFoundError(f"Missing source artifact for fingerprint: {ref}")
        content = path.read_text(encoding="utf-8")
        hasher.update(ref.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(content.encode("utf-8"))
        hasher.update(b"\0")
    return hasher.hexdigest()


def sorted_unique(values: List[str]) -> List[str]:
    return sorted(dict.fromkeys(values))


def repo_relative(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def collect_scope_seeds(policy: Dict[str, Any]) -> Dict[str, ScopeSeed]:
    policy_root = policy["scope_generation_policy"]
    declared = policy_root.get("declared_scopes", [])
    seeds: Dict[str, ScopeSeed] = {}
    for entry in declared:
        seeds[entry["scope_key"]] = ScopeSeed(
            scope_key=entry["scope_key"],
            scope_id=entry["scope_id"],
            publication_status=entry["publication_status"],
            target_files=entry.get("target_files", []),
            target_modules=entry.get("target_modules", []),
            neighbor_files=entry.get("neighbor_files", []),
            watchpoints=entry.get("watchpoints", []),
            maturity=entry.get("maturity", {}),
            notes=entry.get("notes", []),
        )
    return seeds


def collect_decisions(decisions: Dict[str, Any]) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    decisions_root = decisions["scope_generation_decisions"]
    target_ids: Dict[str, List[str]] = {}
    neighbor_ids: Dict[str, List[str]] = {}

    for decision in decisions_root.get("decisions", []):
        if decision.get("status") != "approved":
            continue
        decision_type = decision["decision_type"]
        affected = decision.get("scope_keys_affected", [])
        ids = decision.get("target_ids", []) or []

        if decision_type == "assign_ids_to_scope":
            for scope_key in affected:
                target_ids.setdefault(scope_key, []).extend(ids)
        elif decision_type == "force_logical_neighbors":
            for scope_key in affected:
                neighbor_ids.setdefault(scope_key, []).extend(ids)
        else:
            raise ValueError(f"Unsupported scope generation decision_type: {decision_type}")

    return (
        {k: sorted_unique(v) for k, v in target_ids.items()},
        {k: sorted_unique(v) for k, v in neighbor_ids.items()},
    )


def build_scope_definition(
    scope_seed: ScopeSeed,
    shared_defaults: Dict[str, Any],
    source_fingerprint: str,
    target_ids: List[str],
    neighbor_ids: List[str],
) -> Dict[str, Any]:
    governance = copy.deepcopy(shared_defaults.get("governance", {}))
    provenance_defaults = shared_defaults.get("provenance", {})
    target_defaults = shared_defaults.get("target", {})
    maturity_defaults = shared_defaults.get("maturity", {})

    return {
        "scope_definition": {
            "schema_version": 0.1,
            "scope_id": scope_seed.scope_id,
            "scope_key": scope_seed.scope_key,
            "status": scope_seed.publication_status,
            "provenance": {
                "source_pipeline": provenance_defaults["source_pipeline"],
                "extraction_mode": provenance_defaults["extraction_mode"],
                "source_artifacts": provenance_defaults["source_artifacts"],
                "source_fingerprint": source_fingerprint,
            },
            "target": {
                "artifact_family": target_defaults["artifact_family"],
                "files": scope_seed.target_files,
                "modules": scope_seed.target_modules,
                "ids": target_ids,
            },
            "default_neighbors_to_read": {
                "files": scope_seed.neighbor_files,
                "ids": neighbor_ids,
            },
            "governance": governance,
            "watchpoints": scope_seed.watchpoints,
            "maturity": {
                "scoring_model_ref": maturity_defaults["scoring_model_ref"],
                "axes": scope_seed.maturity["axes"],
                "score_total": scope_seed.maturity["score_total"],
                "level": scope_seed.maturity["level"],
                "rationale": scope_seed.maturity["rationale"],
            },
            "notes": scope_seed.notes,
        }
    }


def build_manifest(
    policy: Dict[str, Any],
    source_fingerprint: str,
    scope_defs: List[Dict[str, Any]],
    scope_dir_rel: str,
) -> Dict[str, Any]:
    policy_root = policy["scope_generation_policy"]
    output_contract = policy_root["output_contract"]
    shared_defaults = policy_root["shared_defaults"]

    published_scopes = []
    for scope_def in scope_defs:
        scope_root = scope_def["scope_definition"]
        published_scopes.append(
            {
                "scope_id": scope_root["scope_id"],
                "scope_key": scope_root["scope_key"],
                "definition_ref": f"{scope_dir_rel}/{scope_root['scope_key']}.yaml",
                "maturity": {
                    "score_total": scope_root["maturity"]["score_total"],
                    "level": scope_root["maturity"]["level"],
                },
                "publication_status": scope_root["status"],
            }
        )

    return {
        "scope_catalog": {
            "schema_version": 0.1,
            "catalog_id": output_contract["catalog_id"],
            "status": output_contract["catalog_status"],
            "pipeline_id": policy_root["pipeline_id"],
            "source_state": {
                "constitution_ref": policy_root["source_state"]["constitution_ref"],
                "referentiel_ref": policy_root["source_state"]["referentiel_ref"],
                "link_ref": policy_root["source_state"]["link_ref"],
                "source_fingerprint": source_fingerprint,
            },
            "generation": {
                "mode": "deterministic_governed",
                "status": "generated",
                "validated_by": "human_plus_successive_ai",
                "notes": [
                    "Catalogue généré de manière déterministe à partir du canon courant et des politiques canonisées du pipeline constitution.",
                    "Les scope_definitions sont des outputs générés et non des fichiers source maintenus manuellement.",
                ],
            },
            "maturity_policy": {
                "scoring_model_ref": shared_defaults["maturity"]["scoring_model_ref"],
                "minimum_recommended_level_for_parallel_runs": "L2_usable_with_care",
            },
            "published_scopes": published_scopes,
            "notes": [
                "Catalogue généré par docs/patcher/shared/generate_constitution_scopes.py.",
                "Toute modification gouvernante doit entrer via les fichiers de politique et de décisions du pipeline constitution.",
            ],
        }
    }


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def current_text(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate constitution scopes deterministically.")
    parser.add_argument(
        "--policy",
        default="docs/pipelines/constitution/policies/scope_generation/policy.yaml",
        help="Path to the canonical scope generation policy file.",
    )
    parser.add_argument(
        "--decisions",
        default="docs/pipelines/constitution/policies/scope_generation/decisions.yaml",
        help="Path to the canonical scope generation decisions file.",
    )
    parser.add_argument(
        "--report",
        default="tmp/constitution_scope_generation_report.yaml",
        help="Path to write the generation report.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write generated files to the scope catalog locations.",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    policy_path = repo_root / args.policy
    decisions_path = repo_root / args.decisions
    report_path = repo_root / args.report

    policy = load_yaml(policy_path)
    decisions = load_yaml(decisions_path)
    policy_root = policy["scope_generation_policy"]
    shared_defaults = policy_root["shared_defaults"]
    output_contract = policy_root["output_contract"]

    source_refs = [
        policy_root["source_state"]["constitution_ref"],
        policy_root["source_state"]["referentiel_ref"],
        policy_root["source_state"]["link_ref"],
    ]
    source_fingerprint = compute_source_fingerprint(repo_root, source_refs)

    seeds = collect_scope_seeds(policy)
    target_ids_by_scope, neighbor_ids_by_scope = collect_decisions(decisions)

    missing_target_scopes = sorted(set(seeds) - set(target_ids_by_scope))
    if missing_target_scopes:
        raise ValueError(f"Missing assign_ids_to_scope decisions for scopes: {missing_target_scopes}")

    scope_dir = repo_root / output_contract["scope_definitions_dir"]
    scope_dir_rel = repo_relative(scope_dir, repo_root)

    scope_defs: List[Dict[str, Any]] = []
    generated_files: List[Tuple[Path, str]] = []
    changed_files: List[str] = []

    for scope_key in sorted(seeds):
        seed = seeds[scope_key]
        scope_def = build_scope_definition(
            scope_seed=seed,
            shared_defaults=shared_defaults,
            source_fingerprint=source_fingerprint,
            target_ids=target_ids_by_scope.get(scope_key, []),
            neighbor_ids=neighbor_ids_by_scope.get(scope_key, []),
        )
        scope_defs.append(scope_def)
        scope_path = scope_dir / f"{scope_key}.yaml"
        scope_text = dump_yaml(scope_def)
        generated_files.append((scope_path, scope_text))
        if current_text(scope_path) != scope_text:
            changed_files.append(repo_relative(scope_path, repo_root))

    manifest = build_manifest(policy, source_fingerprint, scope_defs, scope_dir_rel)
    manifest_path = repo_root / output_contract["catalog_manifest_path"]
    manifest_text = dump_yaml(manifest)
    generated_files.append((manifest_path, manifest_text))
    if current_text(manifest_path) != manifest_text:
        changed_files.append(repo_relative(manifest_path, repo_root))

    report: Dict[str, Any] = {
        "scope_generation_report": {
            "schema_version": 0.1,
            "pipeline_id": policy_root["pipeline_id"],
            "policy_ref": args.policy,
            "decisions_ref": args.decisions,
            "source_fingerprint": source_fingerprint,
            "apply_mode": bool(args.apply),
            "generated_scope_count": len(scope_defs),
            "generated_scope_keys": [s["scope_definition"]["scope_key"] for s in scope_defs],
            "changed_files": changed_files if changed_files else ["none"],
            "outputs": [repo_relative(path, repo_root) for path, _ in generated_files],
            "status": "PASS",
        }
    }

    if args.apply:
        for path, text in generated_files:
            write_text(path, text)

    write_text(report_path, dump_yaml(report))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
