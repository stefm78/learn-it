#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import yaml


TARGET = Path("docs/pipelines/constitution/stages/STAGE_02_ARBITRAGE.skill.yaml")


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def save_yaml(path: Path, data: dict) -> None:
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Missing target file: {TARGET}")

    data = load_yaml(TARGET)
    expected_outputs = data.setdefault("expected_outputs", {})

    replacements = {
        "bounded_local_run": "docs/pipelines/constitution/runs/<run_id>/work/02_arbitrage/arbitrage*.md",
        "nominal_global": "docs/pipelines/constitution/work/02_arbitrage/arbitrage*.md",
        "bounded_transition": "docs/pipelines/constitution/work/02_arbitrage/arbitrage*.md",
    }

    changed = False
    for mode, new_pattern in replacements.items():
        mode_block = expected_outputs.setdefault(mode, {})
        if not isinstance(mode_block, dict):
            raise ValueError(f"expected_outputs.{mode} must be a mapping")
        old_value = mode_block.get("report_path_pattern")
        if old_value != new_pattern:
            mode_block["report_path_pattern"] = new_pattern
            changed = True

    migration_note = data.get("migration_note")
    note_suffix = (
        " Fix (2026-04-20): alignement expected_outputs sur le consommateur aval "
        "STAGE_03_PATCH_SYNTHESIS et sur les artefacts réellement matérialisés "
        "du run ; report_path_pattern passe à arbitrage*.md."
    )
    if isinstance(migration_note, str) and note_suffix.strip() not in migration_note:
        data["migration_note"] = migration_note + note_suffix
        changed = True

    if changed:
        save_yaml(TARGET, data)
        print(f"Patched: {TARGET}")
    else:
        print(f"No change needed: {TARGET}")


if __name__ == "__main__":
    main()