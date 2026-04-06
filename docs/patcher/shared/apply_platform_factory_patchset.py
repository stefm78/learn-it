#!/usr/bin/env python3
"""Apply a Platform Factory patchset into a sandbox root.

This script is dedicated to the Platform Factory patchset structure used by the
`platform_factory` pipeline. It does not reuse the generic constitution patcher
because the patchset model is intentionally specific.

Usage:
    python docs/patcher/shared/apply_platform_factory_patchset.py \\
        ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \\
        ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml \\
        ./docs/pipelines/platform_factory/work/05_apply/sandbox \\
        true \\
        ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any

import yaml

PATCHSET_ROOT = "PLATFORM_FACTORY_PATCHSET"
VALIDATION_ROOT = "PLATFORM_FACTORY_PATCH_VALIDATION"
ALLOWED_TARGETS = {
    "docs/cores/current/platform_factory_architecture.yaml",
    "docs/cores/current/platform_factory_state.yaml",
}
SUPPORTED_ATOMIC_OPS = {"add", "replace", "update", "remove"}

# Mapping target_artifact -> clé racine canonique du document YAML.
# Les paths du patchset sont résolus depuis ce bloc, pas depuis la racine absolue.
CANONICAL_ROOT_KEYS = {
    "docs/cores/current/platform_factory_architecture.yaml": "PLATFORM_FACTORY_ARCHITECTURE",
    "docs/cores/current/platform_factory_state.yaml": "PLATFORM_FACTORY_STATE",
}


class ApplyContext:
    def __init__(
        self,
        patchset_path: Path,
        validation_path: Path,
        sandbox_root: Path,
        dry_run: bool,
        report_path: Path,
    ) -> None:
        self.patchset_path = patchset_path
        self.validation_path = validation_path
        self.sandbox_root = sandbox_root
        self.dry_run = dry_run
        self.report_path = report_path
        self.anomalies: list[str] = []
        self.warnings: list[str] = []
        self.files_touched: set[str] = set()
        self.files_written: set[str] = set()
        self.operations_total = 0
        self.operations_applied = 0

    def fail(self, message: str) -> None:
        self.anomalies.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def status(self) -> str:
        if self.anomalies:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "PASS"


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def _parse_bool(raw: str) -> bool:
    value = raw.strip().lower()
    if value in {"true", "1", "yes", "y"}:
        return True
    if value in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Boolean value attendu, reçu: {raw}")


def _ensure_parent_mapping(root: Any, keys: list[str]) -> tuple[dict[str, Any], str] | None:
    current = root
    for key in keys[:-1]:
        if not isinstance(current, dict):
            return None
        if key not in current or current[key] is None:
            current[key] = {}
        if not isinstance(current[key], dict):
            return None
        current = current[key]
    if not isinstance(current, dict):
        return None
    return current, keys[-1]


def _apply_add(document: Any, path: str, value: Any, ctx: ApplyContext) -> None:
    keys = path.split(".")
    parent_and_key = _ensure_parent_mapping(document, keys)
    if parent_and_key is None:
        ctx.fail(f"Impossible de résoudre le parent du path `{path}` pour op=add.")
        return
    parent, leaf = parent_and_key
    if leaf not in parent:
        parent[leaf] = copy.deepcopy(value)
        return
    existing = parent[leaf]
    if isinstance(existing, list):
        if value in existing:
            ctx.warn(f"Valeur déjà présente pour add sur `{path}` ; opération ignorée.")
            return
        existing.append(copy.deepcopy(value))
        return
    ctx.fail(
        f"Opération add impossible sur `{path}` : la cible existe déjà et n'est pas une liste."
    )


def _apply_replace_or_update(document: Any, path: str, value: Any, ctx: ApplyContext) -> None:
    keys = path.split(".")
    parent_and_key = _ensure_parent_mapping(document, keys)
    if parent_and_key is None:
        ctx.fail(f"Impossible de résoudre le parent du path `{path}` pour op=replace/update.")
        return
    parent, leaf = parent_and_key
    parent[leaf] = copy.deepcopy(value)


def _apply_remove(document: Any, path: str, ctx: ApplyContext) -> None:
    keys = path.split(".")
    parent_and_key = _ensure_parent_mapping(document, keys)
    if parent_and_key is None:
        ctx.fail(f"Impossible de résoudre le parent du path `{path}` pour op=remove.")
        return
    parent, leaf = parent_and_key
    if leaf not in parent:
        ctx.warn(f"Opération remove sur `{path}` ignorée : clé absente.")
        return
    del parent[leaf]


def _apply_atomic_op(document: Any, op_item: dict[str, Any], ctx: ApplyContext) -> None:
    atomic_op = op_item.get("op")
    path = op_item.get("path")
    ctx.operations_total += 1

    if atomic_op not in SUPPORTED_ATOMIC_OPS:
        ctx.fail(f"Type d'opération non supporté par le script Stage 05: `{atomic_op}`.")
        return
    if not isinstance(path, str) or not path.strip():
        ctx.fail("Chaque opération doit déclarer un `path` non vide.")
        return

    if atomic_op == "add":
        if "value" not in op_item:
            ctx.fail(f"L'opération add sur `{path}` doit déclarer `value`.")
            return
        _apply_add(document, path, op_item["value"], ctx)
    elif atomic_op in {"replace", "update"}:
        if "value" not in op_item:
            ctx.fail(f"L'opération {atomic_op} sur `{path}` doit déclarer `value`.")
            return
        _apply_replace_or_update(document, path, op_item["value"], ctx)
    elif atomic_op == "remove":
        _apply_remove(document, path, ctx)

    if not ctx.anomalies:
        ctx.operations_applied += 1


def _build_report(ctx: ApplyContext) -> dict[str, Any]:
    return {
        "PLATFORM_FACTORY_PATCH_EXECUTION": {
            "status": ctx.status(),
            "scope": "platform_factory_patchset_apply",
            "mode": "dry_run" if ctx.dry_run else "apply",
            "patchset_path": str(ctx.patchset_path),
            "validation_path": str(ctx.validation_path),
            "sandbox_root": str(ctx.sandbox_root),
            "report_path": str(ctx.report_path),
            "files_touched": sorted(ctx.files_touched) or ["none"],
            "files_written": sorted(ctx.files_written) or ["none"],
            "operations_total": ctx.operations_total,
            "operations_applied": ctx.operations_applied,
            "anomalies_count": len(ctx.anomalies),
            "warnings_count": len(ctx.warnings),
            "anomalies": ctx.anomalies or ["none"],
            "warnings": ctx.warnings or ["none"],
        }
    }


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(
            "Usage: python apply_platform_factory_patchset.py <patchset.yaml> <patch_validation.yaml> <sandbox_root> <dry_run:true|false> <report.yaml>",
            file=sys.stderr,
        )
        return 2

    patchset_path = Path(argv[1])
    validation_path = Path(argv[2])
    sandbox_root = Path(argv[3])
    dry_run = _parse_bool(argv[4])
    report_path = Path(argv[5])

    ctx = ApplyContext(patchset_path, validation_path, sandbox_root, dry_run, report_path)

    if not patchset_path.exists():
        ctx.fail(f"Patchset introuvable: {patchset_path}")
    if not validation_path.exists():
        ctx.fail(f"Validation patch introuvable: {validation_path}")

    patchset_data: Any = {}
    validation_data: Any = {}

    if not ctx.anomalies:
        try:
            patchset_data = _load_yaml(patchset_path)
            validation_data = _load_yaml(validation_path)
        except Exception as exc:  # pragma: no cover
            ctx.fail(f"Impossible de lire les entrées YAML: {exc}")

    if not ctx.anomalies:
        validation_root = validation_data.get(VALIDATION_ROOT)
        if not isinstance(validation_root, dict):
            ctx.fail(f"La racine `{VALIDATION_ROOT}` est absente du fichier de validation.")
        else:
            status = validation_root.get("status")
            if status != "PASS":
                ctx.fail(
                    f"Le Stage 05 exige `status: PASS` dans `{validation_path}` ; reçu `{status}`."
                )

    document_cache: dict[str, Any] = {}

    if not ctx.anomalies:
        root = patchset_data.get(PATCHSET_ROOT)
        if not isinstance(root, dict):
            ctx.fail(f"La racine `{PATCHSET_ROOT}` est absente du patchset.")
        else:
            patches = root.get("patches")
            if not isinstance(patches, list) or not patches:
                ctx.fail("Le bloc `patches` doit être une liste non vide.")
            else:
                for patch in patches:
                    if not isinstance(patch, dict):
                        ctx.fail("Chaque patch doit être un mapping.")
                        continue
                    target_artifact = patch.get("target_artifact")
                    if target_artifact not in ALLOWED_TARGETS:
                        ctx.fail(f"Artefact cible non autorisé dans Stage 05: `{target_artifact}`.")
                        continue
                    sandbox_file = sandbox_root / str(target_artifact)
                    ctx.files_touched.add(str(sandbox_file))
                    if not sandbox_file.exists():
                        ctx.fail(
                            f"Fichier cible absent dans la sandbox: {sandbox_file}. Préparer la sandbox avant apply."
                        )
                        continue
                    if str(sandbox_file) not in document_cache:
                        try:
                            document_cache[str(sandbox_file)] = _load_yaml(sandbox_file)
                        except Exception as exc:  # pragma: no cover
                            ctx.fail(f"Impossible de charger {sandbox_file}: {exc}")
                            continue

                    # Auto-descente vers le bloc racine canonique.
                    # Les paths du patchset sont relatifs à ce bloc, pas à la racine YAML absolue.
                    raw_document = document_cache[str(sandbox_file)]
                    canonical_root_key = CANONICAL_ROOT_KEYS.get(target_artifact)
                    if canonical_root_key and isinstance(raw_document, dict) and canonical_root_key in raw_document:
                        document = raw_document[canonical_root_key]
                    else:
                        document = raw_document

                    operations = patch.get("operations")
                    if not isinstance(operations, list) or not operations:
                        ctx.fail(
                            f"Le patch `{patch.get('patch_id', 'UNKNOWN')}` doit contenir une liste `operations` non vide."
                        )
                        continue
                    for op_item in operations:
                        if not isinstance(op_item, dict):
                            ctx.fail("Chaque opération doit être un mapping.")
                            continue
                        _apply_atomic_op(document, op_item, ctx)

    if not ctx.dry_run and not ctx.anomalies:
        for sandbox_file_str, document in document_cache.items():
            sandbox_file = Path(sandbox_file_str)
            _save_yaml(sandbox_file, document)
            ctx.files_written.add(str(sandbox_file))

    report = _build_report(ctx)
    _save_yaml(report_path, report)

    return 0 if not ctx.anomalies else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
