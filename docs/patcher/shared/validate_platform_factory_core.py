#!/usr/bin/env python3
"""Validate patched Platform Factory core artifacts for STAGE_06.

This validator performs deterministic checks on the patched architecture/state pair.
It is intentionally lighter than the human validation step and is meant to provide
an automatic canonical trace before the human review report.

Usage:
    python docs/patcher/shared/validate_platform_factory_core.py \
      ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml \
      ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml \
      ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml \
      > ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ARCH_ROOT = "PLATFORM_FACTORY_ARCHITECTURE"
STATE_ROOT = "PLATFORM_FACTORY_STATE"
EXECUTION_ROOT = "PLATFORM_FACTORY_PATCH_EXECUTION"
EXPECTED_ARCH_ARTIFACT_TYPE = "platform_factory_architecture"
EXPECTED_STATE_ARTIFACT_TYPE = "platform_factory_state"


class ValidationContext:
    def __init__(self, arch_path: Path, state_path: Path, execution_report_path: Path) -> None:
        self.arch_path = arch_path
        self.state_path = state_path
        self.execution_report_path = execution_report_path
        self.anomalies: list[str] = []
        self.warnings: list[str] = []
        self.checks: dict[str, str] = {}

    def ok(self, key: str) -> None:
        self.checks[key] = "PASS"

    def warn(self, key: str, message: str) -> None:
        if key not in self.checks:
            self.checks[key] = "WARN"
        self.warnings.append(message)

    def fail(self, key: str, message: str) -> None:
        self.checks[key] = "FAIL"
        self.anomalies.append(message)

    def status(self) -> str:
        if self.anomalies:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "PASS"



def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)



def _is_non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""



def _require_mapping(obj: Any, key: str, ctx: ValidationContext, message: str) -> dict[str, Any]:
    if not isinstance(obj, dict):
        ctx.fail(key, message)
        return {}
    ctx.ok(key)
    return obj



def _metadata_checks(
    metadata: dict[str, Any],
    expected_artifact_type: str,
    prefix: str,
    ctx: ValidationContext,
) -> None:
    if not _is_non_empty_str(metadata.get("artifact_id")):
        ctx.fail(f"{prefix}_artifact_id", f"`{prefix}.metadata.artifact_id` doit être une chaîne non vide.")
    else:
        ctx.ok(f"{prefix}_artifact_id")

    artifact_type = metadata.get("artifact_type")
    if artifact_type != expected_artifact_type:
        ctx.fail(
            f"{prefix}_artifact_type",
            f"`{prefix}.metadata.artifact_type` doit être `{expected_artifact_type}` ; reçu `{artifact_type}`.",
        )
    else:
        ctx.ok(f"{prefix}_artifact_type")

    if not _is_non_empty_str(metadata.get("version")):
        ctx.fail(f"{prefix}_version", f"`{prefix}.metadata.version` doit être une chaîne non vide.")
    else:
        ctx.ok(f"{prefix}_version")

    if not _is_non_empty_str(metadata.get("status")):
        ctx.warn(f"{prefix}_status", f"`{prefix}.metadata.status` devrait être renseigné.")
    else:
        ctx.ok(f"{prefix}_status")



def validate_core(
    arch_doc: Any,
    state_doc: Any,
    execution_doc: Any,
    ctx: ValidationContext,
) -> dict[str, Any]:
    summary: dict[str, Any] = {}

    arch_root = _require_mapping(
        arch_doc, "arch_root_document", ctx, "Le document architecture patché doit être un mapping."
    )
    state_root_doc = _require_mapping(
        state_doc, "state_root_document", ctx, "Le document state patché doit être un mapping."
    )
    exec_root_doc = _require_mapping(
        execution_doc,
        "execution_root_document",
        ctx,
        "Le report d'exécution doit être un mapping YAML.",
    )

    arch = _require_mapping(
        arch_root.get(ARCH_ROOT),
        "arch_root_key",
        ctx,
        f"La racine `{ARCH_ROOT}` doit être présente dans l'architecture patchée.",
    )
    state = _require_mapping(
        state_root_doc.get(STATE_ROOT),
        "state_root_key",
        ctx,
        f"La racine `{STATE_ROOT}` doit être présente dans le state patché.",
    )
    execution = _require_mapping(
        exec_root_doc.get(EXECUTION_ROOT),
        "execution_root_key",
        ctx,
        f"La racine `{EXECUTION_ROOT}` doit être présente dans le report d'exécution.",
    )

    arch_metadata = _require_mapping(
        arch.get("metadata"),
        "arch_metadata",
        ctx,
        "`PLATFORM_FACTORY_ARCHITECTURE.metadata` doit être un mapping.",
    )
    state_metadata = _require_mapping(
        state.get("metadata"),
        "state_metadata",
        ctx,
        "`PLATFORM_FACTORY_STATE.metadata` doit être un mapping.",
    )

    _metadata_checks(arch_metadata, EXPECTED_ARCH_ARTIFACT_TYPE, "arch", ctx)
    _metadata_checks(state_metadata, EXPECTED_STATE_ARTIFACT_TYPE, "state", ctx)

    exec_status = execution.get("status")
    if exec_status != "PASS":
        ctx.fail(
            "execution_report_status",
            f"Le Stage 06 exige un report d'exécution Stage 05 en `PASS`; reçu `{exec_status}`.",
        )
    else:
        ctx.ok("execution_report_status")

    files_written = execution.get("files_written")
    if not isinstance(files_written, list):
        ctx.warn(
            "execution_report_files_written",
            "`files_written` devrait être une liste dans le report d'exécution.",
        )
    else:
        ctx.ok("execution_report_files_written")

    canonical_deps = arch.get("source_of_authority", {}).get("canonical_dependencies")
    if not isinstance(canonical_deps, list) or len(canonical_deps) < 3:
        ctx.fail(
            "canonical_dependencies",
            "L'architecture patchée doit déclarer explicitement ses dépendances canoniques.",
        )
    else:
        ctx.ok("canonical_dependencies")
        summary["canonical_dependencies"] = canonical_deps

    if not isinstance(arch.get("contracts"), dict):
        ctx.fail(
            "architecture_contracts",
            "L'architecture patchée doit conserver un bloc `contracts` explicite.",
        )
    else:
        ctx.ok("architecture_contracts")

    if not isinstance(state.get("validated_decisions"), list):
        ctx.fail(
            "state_validated_decisions",
            "Le state patché doit conserver une liste `validated_decisions`.",
        )
    else:
        ctx.ok("state_validated_decisions")

    if not isinstance(state.get("known_gaps"), list):
        ctx.warn(
            "state_known_gaps",
            "Le state patché devrait conserver une liste `known_gaps` explicite.",
        )
    else:
        ctx.ok("state_known_gaps")

    if not isinstance(state.get("capabilities_absent"), list):
        ctx.warn(
            "state_capabilities_absent",
            "Le state patché devrait conserver une liste `capabilities_absent`.",
        )
    else:
        ctx.ok("state_capabilities_absent")

    maturity = state.get("multi_ia_parallel_readiness_status", {}).get("status")
    if not _is_non_empty_str(maturity):
        ctx.warn(
            "multi_ia_status",
            "Le state patché devrait conserver `multi_ia_parallel_readiness_status.status`.",
        )
    else:
        ctx.ok("multi_ia_status")
        summary["multi_ia_parallel_readiness_status"] = maturity

    projection_status = state.get("derived_projection_conformity_status", {}).get("status")
    if not _is_non_empty_str(projection_status):
        ctx.fail(
            "derived_projection_status",
            "Le state patché doit conserver `derived_projection_conformity_status.status`.",
        )
    else:
        ctx.ok("derived_projection_status")
        summary["derived_projection_conformity_status"] = projection_status

    minimum_contract_status = state.get("produced_application_contract_status", {}).get("status")
    if not _is_non_empty_str(minimum_contract_status):
        ctx.fail(
            "produced_application_contract_status",
            "Le state patché doit conserver `produced_application_contract_status.status`.",
        )
    else:
        ctx.ok("produced_application_contract_status")
        summary["produced_application_contract_status"] = minimum_contract_status

    arch_invariants = arch.get("invariants")
    if not isinstance(arch_invariants, list) or not arch_invariants:
        ctx.fail(
            "architecture_invariants",
            "L'architecture patchée doit conserver une liste `invariants` non vide.",
        )
    else:
        ctx.ok("architecture_invariants")
        summary["architecture_invariants_count"] = len(arch_invariants)

    architecture_layers = arch.get("platform_layers")
    state_layers = state.get("maturity_by_layer")
    if not isinstance(architecture_layers, list) or not isinstance(state_layers, list):
        ctx.warn(
            "layer_cross_check",
            "Le contrôle croisé des couches n'a pas pu être vérifié pleinement faute de listes explicites des deux côtés.",
        )
    else:
        arch_layer_ids = {
            item.get("layer_id")
            for item in architecture_layers
            if isinstance(item, dict) and _is_non_empty_str(item.get("layer_id"))
        }
        state_layer_ids = {
            item.get("layer_id")
            for item in state_layers
            if isinstance(item, dict) and _is_non_empty_str(item.get("layer_id"))
        }
        missing_in_state = sorted(arch_layer_ids - state_layer_ids)
        if missing_in_state:
            ctx.warn(
                "layer_cross_check",
                "Certaines couches de l'architecture ne sont pas retrouvées côté state: "
                + ", ".join(missing_in_state),
            )
        else:
            ctx.ok("layer_cross_check")
        summary["layer_ids_architecture"] = sorted(arch_layer_ids)
        summary["layer_ids_state"] = sorted(state_layer_ids)

    summary["patched_architecture_path"] = str(ctx.arch_path)
    summary["patched_state_path"] = str(ctx.state_path)
    summary["execution_report_path"] = str(ctx.execution_report_path)
    return summary



def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(
            "Usage: python validate_platform_factory_core.py <patched_architecture.yaml> <patched_state.yaml> <execution_report.yaml>",
            file=sys.stderr,
        )
        return 2

    arch_path = Path(argv[1])
    state_path = Path(argv[2])
    execution_report_path = Path(argv[3])
    ctx = ValidationContext(arch_path, state_path, execution_report_path)

    for key, path in [
        ("patched_architecture_exists", arch_path),
        ("patched_state_exists", state_path),
        ("execution_report_exists", execution_report_path),
    ]:
        if not path.exists():
            ctx.fail(key, f"Fichier requis introuvable: {path}")
        else:
            ctx.ok(key)

    summary: dict[str, Any] = {}
    if not ctx.anomalies:
        try:
            arch_doc = _load_yaml(arch_path)
            state_doc = _load_yaml(state_path)
            execution_doc = _load_yaml(execution_report_path)
        except Exception as exc:  # pragma: no cover
            ctx.fail("yaml_loading", f"Impossible de lire les fichiers YAML requis: {exc}")
        else:
            summary = validate_core(arch_doc, state_doc, execution_doc, ctx)

    output = {
        "PLATFORM_FACTORY_CORE_VALIDATION": {
            "status": ctx.status(),
            "scope": "platform_factory_patched_core",
            "validator": "validate_platform_factory_core.py",
            "patched_architecture_path": str(arch_path),
            "patched_state_path": str(state_path),
            "execution_report_path": str(execution_report_path),
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
