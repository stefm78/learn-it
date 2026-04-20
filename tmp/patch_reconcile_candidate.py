#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


TARGET = Path("tmp/reconcile_run_contract_upgrade_candidate.py")


NEW_EXECUTION_PATH_REQUIRED_BY_CONTRACT = '''def execution_path_required_by_contract(path_key: str, required_tokens: List[str]) -> Optional[str]:
    normalized_key = normalize_token(path_key)

    def trim_suffixes(value: str) -> str:
        trimmed = value
        for suffix in PATH_KEY_SUFFIXES:
            if trimmed.endswith(suffix):
                trimmed = trimmed[: -len(suffix)]
                break
        return trimmed.strip("_")

    base_key = trim_suffixes(normalized_key)

    # Aliases explicites pour les cas réellement voulus par les skills actuels.
    explicit_aliases = {
        "sandbox_root": {
            "sandbox_or_output_tree_materialized",
            "sandbox_root_materialized",
            "sandbox_materialized",
        },
        "execution_report": {
            "patch_execution_report_materialized",
            "execution_report_materialized",
        },
    }

    allowed_tokens = {normalize_token(token) for token in explicit_aliases.get(normalized_key, set())}

    for required_token in required_tokens:
        normalized_required = normalize_token(required_token)

        # On ne dérive un execution_path comme preuve que pour un token de
        # matérialisation explicite, jamais pour un simple *_executed_for_real.
        if "materialized" not in normalized_required:
            continue

        # 1) Cas explicitement autorisés.
        if normalized_required in allowed_tokens:
            return required_token

        # 2) Fallback conservateur :
        #    on n'accepte que des correspondances quasi exactes sur le nom du
        #    chemin déclaré, après retrait du suffixe _root/_dir/_path.
        if base_key:
            if normalized_required == f"{base_key}_materialized":
                return required_token
            if normalized_required.startswith(f"{base_key}_") and normalized_required.endswith("_materialized"):
                return required_token
            if normalized_required.endswith(f"_{base_key}_materialized"):
                return required_token

    return None
'''


def replace_function(source: str, func_name: str, new_block: str) -> str:
    pattern = rf"def {func_name}\(.*?(?=^def |\Z)"
    updated, count = re.subn(
        pattern,
        new_block.rstrip() + "\\n\\n",
        source,
        flags=re.S | re.M,
    )
    if count != 1:
        raise RuntimeError(f"Remplacement impossible ou ambigu pour {func_name}: count={count}")
    return updated


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Fichier introuvable: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")
    text = replace_function(
        text,
        "execution_path_required_by_contract",
        NEW_EXECUTION_PATH_REQUIRED_BY_CONTRACT,
    )
    TARGET.write_text(text, encoding="utf-8")
    print(f"Patched: {TARGET}")


if __name__ == "__main__":
    main()