#!/usr/bin/env python3
"""Validate a Platform Factory patchset structure for STAGE_04 pre-apply validation.

This validator is intentionally dedicated to the Platform Factory patchset shape.
It does not try to force the generic constitution patch DSL on top of this pipeline.

Usage:
    python docs/patcher/shared/validate_platform_factory_patchset.py \
        ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \
        > ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT_KEY = "PLATFORM_FACTORY_PATCHSET"
ALLOWED_TARGET_ARTIFACTS = {
    "docs/cores/current/platform_factory_architecture.yaml",
    "docs/cores/current/platform_factory_state.yaml",
}
ALLOWED_TOP_LEVEL_PATCH_OPERATIONS = {
    "add",
    "update",
    "replace",
    "remove",
    "move",
    "split",
    "normalize",
    "reclassify",
    "clarify_wording",
    "align_state_with_architecture",
}
ALLOWED_ATOMIC_OPS = {
    "add",
    "update",
    "replace",
    "remove",
    "move",
    "normalize",
    "reclassify",
    "clarify_wording",
}
ALLOWED_EXCLUSION_REASONS = {
    "deferred",
    "rejected",
    "out_of_scope",
    "validator_or_tooling",
    "pipeline_work",
    "release_governance",
    "clarification_required",
}
EXPECTED_ARBITRAGE_PATH = (
    "docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md"
)


def _is_non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


class ValidationContext:
    def __init__(self, patchset_path: Path) -> None:
        self.patchset_path = patchset_path
        self.anomalies: list[str] = []
        self.warnings: list[str] = []
        self.checks: dict[str, str] = {}

    def fail(self, key: str, message: str) -> None:
        self.checks[key] = "FAIL"
        self.anomalies.append(message)

    def warn(self, key: str, message: str) -> None:
        if key not in self.checks:
            self.checks[key] = "WARN"
        self.warnings.append(message)

    def ok(self, key: str) -> None:
        self.checks[key] = "PASS"

    def status(self) -> str:
        if self.anomalies:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "PASS"



def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)



def validate_patchset(data: Any, ctx: ValidationContext) -> dict[str, Any]:
    declared_targets: list[str] = []
    used_targets: list[str] = []
    patch_count = 0

    if not isinstance(data, dict):
        ctx.fail("root_document", "Le document YAML racine doit être un mapping.")
        return {
            "patch_count": patch_count,
            "target_artifacts_declared": declared_targets,
            "target_artifacts_used": used_targets,
        }
    ctx.ok("root_document")

    if ROOT_KEY not in data:
        ctx.fail("root_key", f"La clé racine obligatoire `{ROOT_KEY}` est absente.")
        return {
            "patch_count": patch_count,
            "target_artifacts_declared": declared_targets,
            "target_artifacts_used": used_targets,
        }
    ctx.ok("root_key")

    patchset = data.get(ROOT_KEY)
    if not isinstance(patchset, dict):
        ctx.fail("root_payload", f"`{ROOT_KEY}` doit contenir un mapping.")
        return {
            "patch_count": patch_count,
            "target_artifacts_declared": declared_targets,
            "target_artifacts_used": used_targets,
        }
    ctx.ok("root_payload")

    metadata = patchset.get("metadata")
    if not isinstance(metadata, dict):
        ctx.fail("metadata", "Le bloc `metadata` est obligatoire et doit être un mapping.")
        metadata = {}
    else:
        ctx.ok("metadata")

    patchset_id = metadata.get("patchset_id")
    if not _is_non_empty_str(patchset_id):
        ctx.fail("patchset_id", "`metadata.patchset_id` doit être une chaîne non vide.")
    else:
        ctx.ok("patchset_id")

    target_artifacts = metadata.get("target_artifacts")
    if not isinstance(target_artifacts, list) or not target_artifacts:
        ctx.fail(
            "target_artifacts",
            "`metadata.target_artifacts` doit être une liste non vide.",
        )
        target_artifacts = []
    else:
        invalid_targets = [
            item for item in target_artifacts if item not in ALLOWED_TARGET_ARTIFACTS
        ]
        if invalid_targets:
            ctx.fail(
                "target_artifacts",
                "`metadata.target_artifacts` contient des cibles non autorisées: "
                + ", ".join(sorted(invalid_targets)),
            )
        else:
            ctx.ok("target_artifacts")
    declared_targets = [str(item) for item in target_artifacts if isinstance(item, str)]

    source_decision_record = metadata.get("source_decision_record")
    if not _is_non_empty_str(source_decision_record):
        ctx.fail(
            "source_decision_record",
            "`metadata.source_decision_record` doit être une chaîne non vide.",
        )
    else:
        if str(source_decision_record) != EXPECTED_ARBITRAGE_PATH:
            ctx.warn(
                "source_decision_record",
                "`metadata.source_decision_record` ne pointe pas vers le record d'arbitrage canonique attendu.",
            )
        else:
            ctx.ok("source_decision_record")

    if not _is_non_empty_str(metadata.get("scope")):
        ctx.warn("scope", "`metadata.scope` devrait être renseigné comme chaîne non vide.")
    else:
        ctx.ok("scope")

    notes = metadata.get("notes")
    if notes is None:
        ctx.warn("notes", "`metadata.notes` est absent ; une note de portée est recommandée.")
    elif not isinstance(notes, list) or any(not _is_non_empty_str(item) for item in notes):
        ctx.warn(
            "notes",
            "`metadata.notes` devrait être une liste de chaînes non vides.",
        )
    else:
        ctx.ok("notes")

    patches = patchset.get("patches")
    if not isinstance(patches, list) or not patches:
        ctx.fail("patches", "Le bloc `patches` doit être une liste non vide.")
        patches = []
    else:
        ctx.ok("patches")

    seen_patch_ids: set[str] = set()
    patch_artifact_hits: dict[str, int] = {artifact: 0 for artifact in ALLOWED_TARGET_ARTIFACTS}

    for index, patch in enumerate(patches, start=1):
        patch_prefix = f"patch_{index}"
        if not isinstance(patch, dict):
            ctx.fail(patch_prefix, f"Le patch #{index} doit être un mapping.")
            continue

        patch_count += 1

        patch_id = patch.get("patch_id")
        if not _is_non_empty_str(patch_id):
            ctx.fail(f"{patch_prefix}_id", f"Le patch #{index} doit déclarer `patch_id`.")
        else:
            if patch_id in seen_patch_ids:
                ctx.fail(
                    f"{patch_prefix}_id",
                    f"`patch_id` dupliqué détecté: `{patch_id}`.",
                )
            else:
                seen_patch_ids.add(str(patch_id))
                ctx.ok(f"{patch_prefix}_id")

        if not _is_non_empty_str(patch.get("source_decision")):
            ctx.fail(
                f"{patch_prefix}_source_decision",
                f"Le patch `{patch_id or index}` doit déclarer `source_decision`.",
            )
        else:
            ctx.ok(f"{patch_prefix}_source_decision")

        target_artifact = patch.get("target_artifact")
        if target_artifact not in ALLOWED_TARGET_ARTIFACTS:
            ctx.fail(
                f"{patch_prefix}_target_artifact",
                f"Le patch `{patch_id or index}` cible un artefact non autorisé: `{target_artifact}`.",
            )
        else:
            patch_artifact_hits[str(target_artifact)] += 1
            used_targets.append(str(target_artifact))
            ctx.ok(f"{patch_prefix}_target_artifact")

        operation = patch.get("operation")
        if operation not in ALLOWED_TOP_LEVEL_PATCH_OPERATIONS:
            ctx.fail(
                f"{patch_prefix}_operation",
                f"Le patch `{patch_id or index}` déclare une opération de haut niveau non autorisée: `{operation}`.",
            )
        else:
            ctx.ok(f"{patch_prefix}_operation")

        for required_field in ["change_type", "rationale", "effect", "risk_avoided"]:
            if not _is_non_empty_str(patch.get(required_field)):
                ctx.fail(
                    f"{patch_prefix}_{required_field}",
                    f"Le patch `{patch_id or index}` doit déclarer `{required_field}` comme chaîne non vide.",
                )
            else:
                ctx.ok(f"{patch_prefix}_{required_field}")

        location_hint = patch.get("location_hint")
        if not isinstance(location_hint, dict):
            ctx.fail(
                f"{patch_prefix}_location_hint",
                f"Le patch `{patch_id or index}` doit déclarer un `location_hint` mapping.",
            )
        else:
            if not _is_non_empty_str(location_hint.get("section")):
                ctx.fail(
                    f"{patch_prefix}_location_hint_section",
                    f"Le patch `{patch_id or index}` doit déclarer `location_hint.section`.",
                )
            else:
                ctx.ok(f"{patch_prefix}_location_hint_section")
            if not _is_non_empty_str(location_hint.get("granularity")):
                ctx.warn(
                    f"{patch_prefix}_location_hint_granularity",
                    f"Le patch `{patch_id or index}` devrait déclarer `location_hint.granularity`.",
                )
            else:
                ctx.ok(f"{patch_prefix}_location_hint_granularity")
            keys_to_update = location_hint.get("keys_to_update")
            if keys_to_update is not None and (
                not isinstance(keys_to_update, list)
                or any(not _is_non_empty_str(item) for item in keys_to_update)
            ):
                ctx.warn(
                    f"{patch_prefix}_location_hint_keys_to_update",
                    f"Le patch `{patch_id or index}` devrait déclarer `location_hint.keys_to_update` comme liste de chaînes non vides.",
                )
            elif keys_to_update is not None:
                ctx.ok(f"{patch_prefix}_location_hint_keys_to_update")

        operations = patch.get("operations")
        if not isinstance(operations, list) or not operations:
            ctx.fail(
                f"{patch_prefix}_operations",
                f"Le patch `{patch_id or index}` doit contenir une liste `operations` non vide.",
            )
            continue
        ctx.ok(f"{patch_prefix}_operations")

        for op_index, op_item in enumerate(operations, start=1):
            op_prefix = f"{patch_prefix}_op_{op_index}"
            if not isinstance(op_item, dict):
                ctx.fail(op_prefix, f"L'opération #{op_index} du patch `{patch_id or index}` doit être un mapping.")
                continue

            atomic_op = op_item.get("op")
            if atomic_op not in ALLOWED_ATOMIC_OPS:
                ctx.fail(
                    f"{op_prefix}_op",
                    f"L'opération #{op_index} du patch `{patch_id or index}` utilise un type non autorisé: `{atomic_op}`.",
                )
            else:
                ctx.ok(f"{op_prefix}_op")

            if not _is_non_empty_str(op_item.get("path")):
                ctx.fail(
                    f"{op_prefix}_path",
                    f"L'opération #{op_index} du patch `{patch_id or index}` doit déclarer `path`.",
                )
            else:
                ctx.ok(f"{op_prefix}_path")

            if atomic_op != "remove" and "value" not in op_item:
                ctx.fail(
                    f"{op_prefix}_value",
                    f"L'opération #{op_index} du patch `{patch_id or index}` doit déclarer `value` pour `op={atomic_op}`.",
                )
            else:
                ctx.ok(f"{op_prefix}_value")

        validation_focus = patch.get("validation_focus")
        if validation_focus is None:
            ctx.warn(
                f"{patch_prefix}_validation_focus",
                f"Le patch `{patch_id or index}` devrait déclarer `validation_focus`.",
            )
        elif not isinstance(validation_focus, list) or any(
            not _is_non_empty_str(item) for item in validation_focus
        ):
            ctx.warn(
                f"{patch_prefix}_validation_focus",
                f"Le patch `{patch_id or index}` devrait déclarer `validation_focus` comme liste de chaînes non vides.",
            )
        else:
            ctx.ok(f"{patch_prefix}_validation_focus")

    undeclared_targets = sorted(set(used_targets) - set(declared_targets))
    if undeclared_targets:
        ctx.fail(
            "declared_vs_used_targets",
            "Des artefacts cibles sont utilisés dans `patches` sans être déclarés dans `metadata.target_artifacts`: "
            + ", ".join(undeclared_targets),
        )
    else:
        ctx.ok("declared_vs_used_targets")

    unused_declared_targets = [
        artifact for artifact in declared_targets if patch_artifact_hits.get(artifact, 0) == 0
    ]
    if unused_declared_targets:
        ctx.warn(
            "unused_declared_targets",
            "Des artefacts sont déclarés dans `metadata.target_artifacts` mais non utilisés dans `patches`: "
            + ", ".join(unused_declared_targets),
        )
    else:
        ctx.ok("unused_declared_targets")

    exclusions = patchset.get("exclusions")
    if exclusions is None:
        ctx.warn(
            "exclusions",
            "Le bloc `exclusions` est absent ; une liste explicite des sujets hors patchset est recommandée.",
        )
    elif not isinstance(exclusions, dict):
        ctx.fail("exclusions", "Le bloc `exclusions` doit être un mapping.")
    else:
        items = exclusions.get("items")
        if items is None:
            ctx.warn(
                "exclusions_items",
                "Le bloc `exclusions.items` est absent ; une liste explicite est recommandée.",
            )
        elif not isinstance(items, list):
            ctx.fail("exclusions_items", "`exclusions.items` doit être une liste.")
        else:
            for item_index, item in enumerate(items, start=1):
                item_prefix = f"exclusion_{item_index}"
                if not isinstance(item, dict):
                    ctx.fail(item_prefix, f"L'exclusion #{item_index} doit être un mapping.")
                    continue
                if not _is_non_empty_str(item.get("id")):
                    ctx.fail(
                        f"{item_prefix}_id",
                        f"L'exclusion #{item_index} doit déclarer `id`.",
                    )
                else:
                    ctx.ok(f"{item_prefix}_id")
                reason = item.get("reason")
                if reason not in ALLOWED_EXCLUSION_REASONS:
                    ctx.warn(
                        f"{item_prefix}_reason",
                        f"L'exclusion #{item_index} utilise un `reason` non standard: `{reason}`.",
                    )
                else:
                    ctx.ok(f"{item_prefix}_reason")
                if not _is_non_empty_str(item.get("note")):
                    ctx.warn(
                        f"{item_prefix}_note",
                        f"L'exclusion #{item_index} devrait déclarer `note` comme chaîne non vide.",
                    )
                else:
                    ctx.ok(f"{item_prefix}_note")

    return {
        "patch_count": patch_count,
        "target_artifacts_declared": sorted(set(declared_targets)),
        "target_artifacts_used": sorted(set(used_targets)),
    }



def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "Usage: python validate_platform_factory_patchset.py <patchset.yaml>",
            file=sys.stderr,
        )
        return 2

    patchset_path = Path(argv[1])
    ctx = ValidationContext(patchset_path)

    if not patchset_path.exists():
        ctx.fail("input_file", f"Fichier introuvable: {patchset_path}")
        output = {
            "PLATFORM_FACTORY_PATCH_VALIDATION": {
                "status": ctx.status(),
                "scope": "platform_factory_patchset",
                "validator": "validate_platform_factory_patchset.py",
                "patchset_path": str(patchset_path),
                "anomalies_count": len(ctx.anomalies),
                "warnings_count": len(ctx.warnings),
                "checks": ctx.checks,
                "summary": {},
                "anomalies": ctx.anomalies or ["none"],
                "warnings": ctx.warnings or ["none"],
            }
        }
        yaml.safe_dump(output, sys.stdout, sort_keys=False, allow_unicode=True)
        return 1

    try:
        data = _load_yaml(patchset_path)
        summary = validate_patchset(data, ctx)
    except Exception as exc:  # pragma: no cover - defensive guard
        ctx.fail("validator_runtime", f"Erreur interne du validateur: {exc}")
        summary = {}

    output = {
        "PLATFORM_FACTORY_PATCH_VALIDATION": {
            "status": ctx.status(),
            "scope": "platform_factory_patchset",
            "validator": "validate_platform_factory_patchset.py",
            "patchset_path": str(patchset_path),
            "anomalies_count": len(ctx.anomalies),
            "warnings_count": len(ctx.warnings),
            "checks": ctx.checks,
            "summary": summary,
            "anomalies": ctx.anomalies or ["none"],
            "warnings": ctx.warnings or ["none"],
        }
    }
    yaml.safe_dump(output, sys.stdout, sort_keys=False, allow_unicode=True)
    return 0 if not ctx.anomalies else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
