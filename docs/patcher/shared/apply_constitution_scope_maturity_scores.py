#!/usr/bin/env python3
"""Publish computed Constitution scope maturity scores into policy.yaml.

PHASE_17 deterministic patcher.

Doctrine:
- score_constitution_scope_maturity.py computes and proves maturity, but remains non-mutating;
- this patcher publishes computed maturity into policy.yaml when gates are satisfied;
- default mode is dry-run; --apply is required to write policy.yaml;
- after --apply, regenerate scope catalog and rerun scoring.

Reads:
  docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
  docs/pipelines/constitution/policies/scope_generation/policy.yaml

Writes with --apply:
  docs/pipelines/constitution/policies/scope_generation/policy.yaml

Always writes:
  docs/pipelines/constitution/reports/scope_maturity_policy_patch_report.yaml
"""

from __future__ import annotations

import argparse
import copy
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


DEFAULT_SCORING = Path("docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml")
DEFAULT_POLICY = Path("docs/pipelines/constitution/policies/scope_generation/policy.yaml")
DEFAULT_REPORT = Path("docs/pipelines/constitution/reports/scope_maturity_policy_patch_report.yaml")

EXPECTED_AXES = [
    "clarity_of_scope",
    "internal_coherence",
    "inter_scope_boundaries",
    "dependency_explicitness",
    "bounded_run_executability",
    "inter_release_stability",
]

ALLOWED_SCORING_STATUSES = {"PASS", "WARN"}
SOURCE_NOTE = (
    "Maturity synchronized from docs/pipelines/constitution/reports/"
    "scope_maturity_scoring_report.yaml by PHASE_17 computed-score authority migration."
)


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)


def get_mapping(doc: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = doc.get(key)
    if not isinstance(value, dict):
        raise SystemExit(f"Expected top-level mapping {key!r}.")
    return value


def as_int(value: Any, label: str) -> int:
    if not isinstance(value, int):
        raise SystemExit(f"Expected integer for {label}, got {value!r}.")
    return value


def normalize_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def level_rank(level: str) -> int:
    order = {
        "L0_experimental": 0,
        "L1_fragile": 1,
        "L2_usable_with_care": 2,
        "L3_operational": 3,
        "L4_strong": 4,
    }
    return order.get(str(level), -1)


def compute_level_delta(old_level: str, new_level: str) -> str:
    old_rank = level_rank(old_level)
    new_rank = level_rank(new_level)
    if old_rank == -1 or new_rank == -1:
        return "unknown"
    if new_rank == old_rank:
        return "none"
    if new_rank > old_rank:
        return "computed_higher_than_published"
    return "computed_lower_than_published"


def validate_scoring_report(scoring_root: Dict[str, Any]) -> List[str]:
    findings: List[str] = []

    status = scoring_root.get("status")
    if status not in ALLOWED_SCORING_STATUSES:
        findings.append(f"scoring_status_not_publishable:{status}")

    summary = scoring_root.get("summary")
    if not isinstance(summary, dict):
        findings.append("missing_summary")
    else:
        if summary.get("blocking_finding_count") not in (0, None):
            findings.append(f"blocking_finding_count:{summary.get('blocking_finding_count')}")

    blocking_findings = scoring_root.get("blocking_findings", [])
    if blocking_findings not in ([], None):
        findings.append("blocking_findings_not_empty")

    scope_results = scoring_root.get("scope_results")
    if not isinstance(scope_results, list) or not scope_results:
        findings.append("scope_results_missing_or_empty")
        return findings

    for idx, result in enumerate(scope_results):
        scope_key = result.get("scope_key")
        if not scope_key:
            findings.append(f"scope_results[{idx}].missing_scope_key")

        computed = result.get("computed_maturity")
        if not isinstance(computed, dict):
            findings.append(f"{scope_key}.missing_computed_maturity")
            continue

        if not isinstance(computed.get("score_total"), int):
            findings.append(f"{scope_key}.computed_maturity.score_total_not_int")
        if not computed.get("level"):
            findings.append(f"{scope_key}.computed_maturity.level_missing")

        axis_scores = result.get("axis_scores")
        if not isinstance(axis_scores, dict):
            findings.append(f"{scope_key}.axis_scores_missing")
            continue

        for axis in EXPECTED_AXES:
            axis_doc = axis_scores.get(axis)
            if not isinstance(axis_doc, dict):
                findings.append(f"{scope_key}.axis_scores.{axis}_missing")
            elif not isinstance(axis_doc.get("score"), int):
                findings.append(f"{scope_key}.axis_scores.{axis}.score_not_int")

        if isinstance(computed.get("score_total"), int) and isinstance(axis_scores, dict):
            axis_sum = sum(axis_scores.get(axis, {}).get("score", 0) for axis in EXPECTED_AXES)
            if axis_sum != computed.get("score_total"):
                findings.append(f"{scope_key}.axis_sum_mismatch:{axis_sum}!={computed.get('score_total')}")

    return findings


def index_policy_scopes(policy_root: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    declared = policy_root.get("declared_scopes")
    if not isinstance(declared, list):
        raise SystemExit("scope_generation_policy.declared_scopes must be a list.")
    by_key: Dict[str, Dict[str, Any]] = {}
    for scope in declared:
        if not isinstance(scope, dict):
            continue
        key = scope.get("scope_key")
        if key in by_key:
            raise SystemExit(f"Duplicate scope_key in policy: {key}")
        if key:
            by_key[str(key)] = scope
    return by_key


def build_computed_maturity(result: Dict[str, Any]) -> Dict[str, Any]:
    scope_key = str(result.get("scope_key"))
    computed = result.get("computed_maturity") or {}
    axis_scores = result.get("axis_scores") or {}

    axes = {}
    for axis in EXPECTED_AXES:
        axes[axis] = as_int(axis_scores[axis]["score"], f"{scope_key}.{axis}.score")

    return {
        "axes": axes,
        "score_total": as_int(computed["score_total"], f"{scope_key}.computed_maturity.score_total"),
        "level": str(computed["level"]),
    }


def merge_rationale(existing: Any, scope_key: str, scoring_status: str) -> List[str]:
    """Return a stable PHASE_17 rationale list.

    The note intentionally does not embed the current scoring status. Otherwise, the
    patcher would keep proposing rationale-only rewrites when the scoring report moves
    from WARN to PASS after publication and rerun.
    """

    if isinstance(existing, list):
        rationale = [str(item) for item in existing]
    elif existing:
        rationale = [str(existing)]
    else:
        rationale = []

    stable_prefix = f"{SOURCE_NOTE} Scope={scope_key};"
    rationale = [item for item in rationale if not item.startswith(stable_prefix)]

    note = f"{stable_prefix} published_by=apply_constitution_scope_maturity_scores.py; blocking_finding_count=0."
    rationale.append(note)
    return rationale


def synthesize_policy_patch(policy_doc: Dict[str, Any], scoring_root: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    policy_root = get_mapping(policy_doc, "scope_generation_policy")
    policy_scopes = index_policy_scopes(policy_root)

    scope_results = scoring_root.get("scope_results") or []
    patched_doc = copy.deepcopy(policy_doc)
    patched_root = get_mapping(patched_doc, "scope_generation_policy")
    patched_scopes = index_policy_scopes(patched_root)

    scoring_status = str(scoring_root.get("status"))
    actions = []

    seen = set()
    for result in scope_results:
        scope_key = str(result.get("scope_key"))
        seen.add(scope_key)
        if scope_key not in patched_scopes:
            raise SystemExit(f"Scoring report scope not found in policy.yaml: {scope_key}")

        policy_scope = policy_scopes[scope_key]
        patched_scope = patched_scopes[scope_key]

        old_maturity = copy.deepcopy(policy_scope.get("maturity") or {})
        new_maturity = build_computed_maturity(result)
        new_maturity["rationale"] = merge_rationale(old_maturity.get("rationale"), scope_key, scoring_status)

        patched_scope["maturity"] = new_maturity

        old_score = old_maturity.get("score_total")
        old_level = old_maturity.get("level")
        new_score = new_maturity.get("score_total")
        new_level = new_maturity.get("level")

        actions.append({
            "scope_key": scope_key,
            "old_score_total": old_score,
            "new_score_total": new_score,
            "score_delta": new_score - old_score if isinstance(old_score, int) and isinstance(new_score, int) else None,
            "old_level": old_level,
            "new_level": new_level,
            "level_delta": compute_level_delta(str(old_level), str(new_level)),
            "old_axes": old_maturity.get("axes", {}),
            "new_axes": new_maturity.get("axes", {}),
        })

    missing_from_scoring = sorted(set(policy_scopes) - seen)
    if missing_from_scoring:
        raise SystemExit(f"Policy scopes missing from scoring report: {missing_from_scoring}")

    changed_actions = [
        action for action in actions
        if action["old_score_total"] != action["new_score_total"]
        or action["old_level"] != action["new_level"]
        or action["old_axes"] != action["new_axes"]
    ]

    return patched_doc, {
        "scope_count": len(actions),
        "changed_scope_count": len(changed_actions),
        "unchanged_scope_count": len(actions) - len(changed_actions),
        "actions": actions,
    }


def make_report(
    *,
    status: str,
    apply_mode: bool,
    changed: bool,
    scoring_path: Path,
    policy_path: Path,
    scoring_sha_before: str,
    policy_sha_before: str,
    policy_sha_after: str,
    gate_findings: List[str],
    patch_summary: Dict[str, Any] | None,
) -> Dict[str, Any]:
    return {
        "scope_maturity_policy_patch_report": {
            "schema_version": "0.1",
            "phase_id": "PHASE_17",
            "generated_at": iso_now(),
            "status": status,
            "apply_mode": apply_mode,
            "changed": changed,
            "gate_findings": gate_findings,
            "inputs": {
                "scoring_report": normalize_path(scoring_path),
                "policy": normalize_path(policy_path),
            },
            "input_hashes": {
                "scoring_report_sha256": scoring_sha_before,
                "policy_sha256_before": policy_sha_before,
                "policy_sha256_after": policy_sha_after,
            },
            "mutation_policy": {
                "policy_yaml": "modified_if_apply_true_and_changed",
                "decisions_yaml": "not_modified",
                "catalog_manifest": "not_modified",
                "scope_definitions": "not_modified",
                "cores": "not_modified",
                "scoring_report": "not_modified",
                "scorer_rules": "not_modified",
            },
            "patch_summary": patch_summary or {
                "scope_count": 0,
                "changed_scope_count": 0,
                "unchanged_scope_count": 0,
                "actions": [],
            },
            "next_steps_after_apply": [
                "python docs/patcher/shared/generate_constitution_scopes.py --apply --report tmp/constitution_scope_generation_report.yaml",
                "python docs/patcher/shared/score_constitution_scope_maturity.py --report docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml",
                "rerun apply_constitution_scope_maturity_scores.py in dry-run to verify changed=false or only explicitly justified residuals",
            ] if apply_mode and changed else [],
        }
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish computed Constitution scope maturity scores into policy.yaml.")
    parser.add_argument("--scoring", default=str(DEFAULT_SCORING))
    parser.add_argument("--policy", default=str(DEFAULT_POLICY))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--apply", action="store_true", help="Write policy.yaml. Default is dry-run only.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    scoring_path = Path(args.scoring)
    policy_path = Path(args.policy)
    report_path = Path(args.report)

    scoring_sha_before = sha256_file(scoring_path)
    policy_sha_before = sha256_file(policy_path)

    scoring_doc = load_yaml(scoring_path)
    policy_doc = load_yaml(policy_path)

    scoring_root = get_mapping(scoring_doc, "scope_maturity_scoring_report")
    gate_findings = validate_scoring_report(scoring_root)

    patch_summary: Dict[str, Any] | None = None
    changed = False
    status = "PASS"

    if gate_findings:
        status = "BLOCKED"
        policy_sha_after = policy_sha_before
    else:
        patched_policy, patch_summary = synthesize_policy_patch(policy_doc, scoring_root)
        changed = patched_policy != policy_doc
        if args.apply and changed:
            write_yaml(policy_path, patched_policy)
        policy_sha_after = sha256_file(policy_path)

    report = make_report(
        status=status,
        apply_mode=bool(args.apply),
        changed=changed,
        scoring_path=scoring_path,
        policy_path=policy_path,
        scoring_sha_before=scoring_sha_before,
        policy_sha_before=policy_sha_before,
        policy_sha_after=policy_sha_after,
        gate_findings=gate_findings,
        patch_summary=patch_summary,
    )
    write_yaml(report_path, report)

    print(f"Wrote {report_path}")
    print(f"Status: {status} apply_mode={args.apply} changed={changed}")
    if patch_summary:
        print(f"Scopes: {patch_summary['scope_count']}; changed scopes: {patch_summary['changed_scope_count']}")
    if gate_findings:
        print("Gate findings:")
        for finding in gate_findings:
            print(f"- {finding}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
