#!/usr/bin/env python3
"""Validate a Platform Factory patchset YAML.

This script validates the structural and operational conformance of a patchset
before it is applied in Stage 05. It supports an optional --check-paths mode
that loads the actual source artifacts and verifies that each operation path is
resolvable and compatible with the target structure.

Usage (structure only):
    python docs/patcher/shared/validate_platform_factory_patchset.py \\
        ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \\
        > ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml

Usage (with path checking against real artifacts):
    python docs/patcher/shared/validate_platform_factory_patchset.py \\
        ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \\
        --check-paths \\
        --arch ./docs/cores/current/platform_factory_architecture.yaml \\
        --state ./docs/cores/current/platform_factory_state.yaml \\
        > ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

PATCHSET_ROOT = "PLATFORM_FACTORY_PATCHSET"

REQUIRED_METADATA_KEYS = [
    "patchset_id",
    "target_artifacts",
    "source_decision_record",
    "scope",
    "notes",
]

REQUIRED_PATCH_KEYS = [
    "patch_id",
    "source_decision",
    "target_artifact",
    "operation",
    "change_type",
    "rationale",
    "effect",
    "risk_avoided",
    "location_hint",
    "operations",
]

REQUIRED_LOCATION_HINT_KEYS = ["section", "granularity", "keys_to_update"]

REQUIRED_OP_KEYS = ["op", "path"]

SUPPORTED_OPS = {"add", "replace", "update", "remove",
                 "list_remove_item", "list_remove_mapping", "list_replace_mapping"}

ALLOWED_TARGETS = {
    "docs/cores/current/platform_factory_architecture.yaml",
    "docs/cores/current/platform_factory_state.yaml",
}

CANONICAL_ROOT_KEYS = {
    "docs/cores/current/platform_factory_architecture.yaml": "PLATFORM_FACTORY_ARCHITECTURE",
    "docs/cores/current/platform_factory_state.yaml": "PLATFORM_FACTORY_STATE",
}

REQUIRED_EXCLUSION_KEYS = ["id", "reason", "note"]


class ValidationContext:
    def __init__(self) -> None:
        self.checks: dict[str, str] = {}
        self.anomalies: list[str] = []
        self.warnings: list[str] = []
        self.patch_count = 0
        self.target_artifacts_declared: list[str] = []
        self.target_artifacts_used: set[str] = set()

    def record(self, key: str, passed: bool, message: str = "") -> bool:
        self.checks[key] = "PASS" if passed else "FAIL"
        if not passed:
            self.anomalies.append(message or key)
        return passed

    def warn(self, key: str, message: str) -> None:
        self.checks[key] = "WARN"
        self.warnings.append(message)

    def status(self) -> str:
        if self.anomalies:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "PASS"


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _resolve_path(document: Any, path: str) -> tuple[bool, Any, str]:
    """Resolve a dot-separated path in a document.

    Returns (found, value, error_message).
    document is the canonical root block (already descended).
    """
    keys = path.split(".")
    current = document
    for i, key in enumerate(keys):
        if isinstance(current, dict):
            if key not in current:
                return False, None, f"Clé `{key}` absente à la position {i} du path `{path}`."
            current = current[key]
        else:
            return False, None, (
                f"Impossible de descendre dans `{key}` à la position {i} "
                f"du path `{path}` : la valeur parente n'est pas un mapping."
            )
    return True, current, ""


def _resolve_parent(document: Any, path: str) -> tuple[bool, Any, str, str]:
    """Resolve the parent mapping of a dot-separated path.

    Returns (found, parent_dict, leaf_key, error_message).
    """
    keys = path.split(".")
    if len(keys) == 1:
        return True, document, keys[0], ""
    parent_path = ".".join(keys[:-1])
    found, parent, err = _resolve_path(document, parent_path)
    if not found:
        return False, None, "", err
    if not isinstance(parent, dict):
        return False, None, "", (
            f"Le parent de `{path}` n'est pas un mapping."
        )
    return True, parent, keys[-1], ""


def _check_path_compatibility(
    document: Any,
    op_item: dict[str, Any],
    patch_id: str,
    ctx: ValidationContext,
    check_key: str,
) -> None:
    """Check that a path is compatible with the target document structure."""
    op = op_item.get("op", "")
    path = op_item.get("path", "")

    if op == "add":
        found_parent, parent, leaf, err = _resolve_parent(document, path)
        if not found_parent:
            ctx.warn(
                check_key,
                f"[check-paths] patch `{patch_id}` op=add path=`{path}` : "
                f"parent non résolvable ({err}). La clé sera créée si le parent existe à l'apply.",
            )
            return
        if leaf in parent:
            existing = parent[leaf]
            if not isinstance(existing, list):
                ctx.record(
                    check_key,
                    False,
                    f"[check-paths] patch `{patch_id}` op=add path=`{path}` : "
                    f"la cible existe déjà et n'est pas une liste → FAIL garanti à l'apply. "
                    f"Utiliser `replace` ou `list_replace_mapping` à la place.",
                )

    elif op in {"replace", "update"}:
        # replace/update are always safe — just warn if path doesn't exist yet (new key).
        found_parent, parent, leaf, err = _resolve_parent(document, path)
        if not found_parent:
            ctx.warn(
                check_key,
                f"[check-paths] patch `{patch_id}` op={op} path=`{path}` : "
                f"parent non résolvable ({err}). Nouvelle clé sera créée.",
            )

    elif op == "remove":
        found, value, err = _resolve_path(document, path)
        if not found:
            ctx.warn(
                check_key,
                f"[check-paths] patch `{patch_id}` op=remove path=`{path}` : "
                f"clé absente dans l'artefact source → WARN garanti à l'apply ({err}).",
            )
            return
        if isinstance(value, list):
            ctx.record(
                check_key,
                False,
                f"[check-paths] patch `{patch_id}` op=remove path=`{path}` : "
                f"la cible est une liste. Utiliser `list_remove_item` ou `list_remove_mapping` "
                f"pour retirer un élément, ou `replace` pour réécrire la liste entière.",
            )

    elif op == "list_remove_item":
        found, value, err = _resolve_path(document, path)
        if not found:
            ctx.warn(
                check_key,
                f"[check-paths] patch `{patch_id}` op=list_remove_item path=`{path}` : "
                f"cible absente dans l'artefact source → WARN probable à l'apply ({err}).",
            )
            return
        if not isinstance(value, list):
            ctx.record(
                check_key,
                False,
                f"[check-paths] patch `{patch_id}` op=list_remove_item path=`{path}` : "
                f"la cible n'est pas une liste (type={type(value).__name__}).",
            )

    elif op == "list_remove_mapping":
        found, value, err = _resolve_path(document, path)
        if not found:
            ctx.warn(
                check_key,
                f"[check-paths] patch `{patch_id}` op=list_remove_mapping path=`{path}` : "
                f"cible absente dans l'artefact source → WARN probable à l'apply ({err}).",
            )
            return
        if not isinstance(value, list):
            ctx.record(
                check_key,
                False,
                f"[check-paths] patch `{patch_id}` op=list_remove_mapping path=`{path}` : "
                f"la cible n'est pas une liste (type={type(value).__name__}).",
            )
            return
        match_key = op_item.get("match_key")
        match_value = op_item.get("match_value")
        if not match_key or match_value is None:
            ctx.record(
                check_key,
                False,
                f"[check-paths] patch `{patch_id}` op=list_remove_mapping path=`{path}` : "
                f"`match_key` et `match_value` sont obligatoires.",
            )
            return
        found_item = any(
            isinstance(item, dict) and item.get(match_key) == match_value
            for item in value
        )
        if not found_item:
            ctx.warn(
                check_key,
                f"[check-paths] patch `{patch_id}` op=list_remove_mapping path=`{path}` : "
                f"aucun item avec {match_key}={match_value} trouvé → WARN probable à l'apply.",
            )

    elif op == "list_replace_mapping":
        found, value, err = _resolve_path(document, path)
        if not found:
            ctx.record(
                check_key,
                False,
                f"[check-paths] patch `{patch_id}` op=list_replace_mapping path=`{path}` : "
                f"cible absente dans l'artefact source → FAIL garanti à l'apply ({err}).",
            )
            return
        if not isinstance(value, list):
            ctx.record(
                check_key,
                False,
                f"[check-paths] patch `{patch_id}` op=list_replace_mapping path=`{path}` : "
                f"la cible n'est pas une liste (type={type(value).__name__}).",
            )
            return
        match_key = op_item.get("match_key")
        match_value = op_item.get("match_value")
        if not match_key or match_value is None:
            ctx.record(
                check_key,
                False,
                f"[check-paths] patch `{patch_id}` op=list_replace_mapping path=`{path}` : "
                f"`match_key` et `match_value` sont obligatoires.",
            )
            return
        found_item = any(
            isinstance(item, dict) and item.get(match_key) == match_value
            for item in value
        )
        if not found_item:
            ctx.record(
                check_key,
                False,
                f"[check-paths] patch `{patch_id}` op=list_replace_mapping path=`{path}` : "
                f"aucun item avec {match_key}={match_value} trouvé → FAIL garanti à l'apply.",
            )


def _validate_op(op_item: Any, patch_idx: int, op_idx: int, ctx: ValidationContext) -> None:
    prefix = f"patch_{patch_idx}_op_{op_idx}"
    if not isinstance(op_item, dict):
        ctx.record(f"{prefix}_structure", False, f"L'opération {op_idx} du patch {patch_idx} doit être un mapping.")
        return
    for key in REQUIRED_OP_KEYS:
        ctx.record(
            f"{prefix}_{key}",
            key in op_item,
            f"Champ obligatoire `{key}` absent dans op {op_idx} du patch {patch_idx}.",
        )
    op = op_item.get("op", "")
    ctx.record(
        f"{prefix}_op_supported",
        op in SUPPORTED_OPS,
        f"Op `{op}` non supportée dans op {op_idx} du patch {patch_idx}. Ops supportées : {sorted(SUPPORTED_OPS)}.",
    )
    if op in {"add", "replace", "update", "list_replace_mapping"}:
        ctx.record(
            f"{prefix}_value_present",
            "value" in op_item,
            f"Champ `value` obligatoire pour op `{op}` dans op {op_idx} du patch {patch_idx}.",
        )
    if op in {"list_remove_mapping", "list_replace_mapping"}:
        ctx.record(
            f"{prefix}_match_key_present",
            "match_key" in op_item,
            f"Champ `match_key` obligatoire pour op `{op}` dans op {op_idx} du patch {patch_idx}.",
        )
        ctx.record(
            f"{prefix}_match_value_present",
            "match_value" in op_item,
            f"Champ `match_value` obligatoire pour op `{op}` dans op {op_idx} du patch {patch_idx}.",
        )
    if op == "list_remove_item":
        ctx.record(
            f"{prefix}_value_present",
            "value" in op_item,
            f"Champ `value` obligatoire pour op `list_remove_item` dans op {op_idx} du patch {patch_idx}.",
        )


def _validate_patch(
    patch: Any,
    patch_idx: int,
    ctx: ValidationContext,
    artifact_documents: dict[str, Any],
    check_paths: bool,
) -> None:
    prefix = f"patch_{patch_idx}"
    if not isinstance(patch, dict):
        ctx.record(f"{prefix}_structure", False, f"Le patch {patch_idx} doit être un mapping.")
        return
    for key in REQUIRED_PATCH_KEYS:
        ctx.record(
            f"{prefix}_{key}",
            key in patch,
            f"Champ obligatoire `{key}` absent dans patch {patch_idx}.",
        )
    if "target_artifact" in patch:
        ctx.target_artifacts_used.add(patch["target_artifact"])
    location_hint = patch.get("location_hint")
    if isinstance(location_hint, dict):
        for key in REQUIRED_LOCATION_HINT_KEYS:
            ctx.record(
                f"{prefix}_location_hint_{key}",
                key in location_hint,
                f"Champ obligatoire `{key}` absent dans location_hint du patch {patch_idx}.",
            )
    operations = patch.get("operations")
    if isinstance(operations, list):
        for op_idx, op_item in enumerate(operations, start=1):
            _validate_op(op_item, patch_idx, op_idx, ctx)
            if check_paths and isinstance(op_item, dict):
                target = patch.get("target_artifact", "")
                document = artifact_documents.get(target)
                if document is not None:
                    check_key = f"{prefix}_op_{op_idx}_path_check"
                    patch_id = patch.get("patch_id", f"patch_{patch_idx}")
                    _check_path_compatibility(document, op_item, patch_id, ctx, check_key)
    if "validation_focus" in patch:
        ctx.record(
            f"{prefix}_validation_focus",
            isinstance(patch["validation_focus"], list),
            f"`validation_focus` du patch {patch_idx} doit être une liste.",
        )


def _validate_exclusion(excl: Any, excl_idx: int, ctx: ValidationContext) -> None:
    prefix = f"exclusion_{excl_idx}"
    if not isinstance(excl, dict):
        ctx.record(f"{prefix}_structure", False, f"L'exclusion {excl_idx} doit être un mapping.")
        return
    for key in REQUIRED_EXCLUSION_KEYS:
        ctx.record(
            f"{prefix}_{key}",
            key in excl,
            f"Champ obligatoire `{key}` absent dans exclusion {excl_idx}.",
        )


def _build_report(ctx: ValidationContext, patchset_path: str, check_paths: bool) -> dict[str, Any]:
    unused = [
        t for t in ctx.target_artifacts_declared
        if t not in ctx.target_artifacts_used
    ]
    ctx.record("declared_vs_used_targets", True)
    ctx.record("unused_declared_targets", not unused,
               f"Artefacts déclarés mais non utilisés dans les patches : {unused}." if unused else "")
    return {
        "PLATFORM_FACTORY_PATCH_VALIDATION": {
            "status": ctx.status(),
            "scope": "platform_factory_patchset",
            "check_paths_enabled": check_paths,
            "validator": "validate_platform_factory_patchset.py",
            "patchset_path": patchset_path,
            "anomalies_count": len(ctx.anomalies),
            "warnings_count": len(ctx.warnings),
            "checks": ctx.checks,
            "summary": {
                "patch_count": ctx.patch_count,
                "target_artifacts_declared": ctx.target_artifacts_declared,
                "target_artifacts_used": sorted(ctx.target_artifacts_used),
            },
            "anomalies": ctx.anomalies or ["none"],
            "warnings": ctx.warnings or ["none"],
        }
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("patchset", help="Chemin vers le patchset YAML")
    parser.add_argument("--check-paths", action="store_true",
                        help="Vérifier la compatibilité des paths avec les artefacts sources réels")
    parser.add_argument("--arch", default="docs/cores/current/platform_factory_architecture.yaml",
                        help="Chemin vers platform_factory_architecture.yaml")
    parser.add_argument("--state", default="docs/cores/current/platform_factory_state.yaml",
                        help="Chemin vers platform_factory_state.yaml")
    args = parser.parse_args(argv[1:])

    patchset_path = Path(args.patchset)
    ctx = ValidationContext()

    ctx.record("root_document", patchset_path.exists(),
               f"Patchset introuvable : {patchset_path}")
    if not patchset_path.exists():
        report = _build_report(ctx, str(patchset_path), args.check_paths)
        print(yaml.dump(report, sort_keys=False, allow_unicode=True), end="")
        return 1

    raw = _load_yaml(patchset_path)
    ctx.record("root_key", isinstance(raw, dict) and PATCHSET_ROOT in raw,
               f"Clé racine `{PATCHSET_ROOT}` absente.")
    if not (isinstance(raw, dict) and PATCHSET_ROOT in raw):
        report = _build_report(ctx, str(patchset_path), args.check_paths)
        print(yaml.dump(report, sort_keys=False, allow_unicode=True), end="")
        return 1

    root = raw[PATCHSET_ROOT]
    ctx.record("root_payload", isinstance(root, dict),
               "La valeur sous la clé racine doit être un mapping.")

    # Metadata
    metadata = root.get("metadata", {})
    ctx.record("metadata", isinstance(metadata, dict), "`metadata` doit être un mapping.")
    for key in REQUIRED_METADATA_KEYS:
        ctx.record(f"metadata_{key}", key in metadata,
                   f"Champ obligatoire `{key}` absent dans metadata.")
    if "target_artifacts" in metadata:
        ta = metadata["target_artifacts"]
        ctx.record("metadata_target_artifacts_list",
                   isinstance(ta, list) and len(ta) > 0,
                   "`target_artifacts` doit être une liste non vide.")
        ctx.target_artifacts_declared = ta if isinstance(ta, list) else []

    # Load artifact documents for path checking
    artifact_documents: dict[str, Any] = {}
    if args.check_paths:
        for artifact_key, canonical_root_key in CANONICAL_ROOT_KEYS.items():
            path_arg = args.arch if "architecture" in artifact_key else args.state
            artifact_path = Path(path_arg)
            if artifact_path.exists():
                raw_doc = _load_yaml(artifact_path)
                if isinstance(raw_doc, dict) and canonical_root_key in raw_doc:
                    artifact_documents[artifact_key] = raw_doc[canonical_root_key]
                else:
                    artifact_documents[artifact_key] = raw_doc
            else:
                ctx.warn(
                    f"artifact_load_{artifact_key}",
                    f"[check-paths] Artefact source introuvable : {artifact_path}. "
                    f"Les vérifications de path pour cet artefact seront ignorées.",
                )

    # Patches
    patches = root.get("patches")
    ctx.record("patches", isinstance(patches, list) and len(patches) > 0,
               "`patches` doit être une liste non vide.")
    if isinstance(patches, list):
        ctx.patch_count = len(patches)
        for patch_idx, patch in enumerate(patches, start=1):
            _validate_patch(patch, patch_idx, ctx, artifact_documents, args.check_paths)

    # Exclusions
    exclusions = root.get("exclusions", {})
    if isinstance(exclusions, dict):
        items = exclusions.get("items", [])
        if isinstance(items, list):
            for excl_idx, excl in enumerate(items, start=1):
                _validate_exclusion(excl, excl_idx, ctx)

    report = _build_report(ctx, str(patchset_path), args.check_paths)
    print(yaml.dump(report, sort_keys=False, allow_unicode=True), end="")
    return 0 if ctx.status() == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
