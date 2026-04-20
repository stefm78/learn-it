#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


TARGET = Path("tmp/reconcile_run_contract_upgrade_candidate.py")


NEW_NORMALIZE_RUN_RELATIVE_PATTERN = '''def normalize_run_relative_pattern(pattern: str, pipeline_id: str, run_id: str) -> str:
    prefixes = [
        f"docs/pipelines/{pipeline_id}/runs/<run_id>/",
        f"docs/pipelines/{pipeline_id}/runs/{run_id}/",
    ]
    normalized = pattern.strip()
    for prefix in prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix) :]
            break

    # Les placeholders skill comme <id> doivent être traités comme des globs,
    # pas comme des chemins littéraux.
    normalized = re.sub(r"<[^/<>]+>", "*", normalized)

    return normalized.strip()
'''


NEW_EXECUTION_PATH_REQUIRED_BY_CONTRACT = '''def execution_path_required_by_contract(path_key: str, required_tokens: List[str]) -> Optional[str]:
    normalized_key = normalize_token(path_key)

    candidate_fragments: Set[str] = {normalized_key}
    for fragment in split_token_fragments(path_key):
        candidate_fragments.add(fragment)

    for suffix in PATH_KEY_SUFFIXES:
        if normalized_key.endswith(suffix):
            trimmed = normalized_key[: -len(suffix)]
            if trimmed:
                candidate_fragments.add(trimmed)
                candidate_fragments.update(split_token_fragments(trimmed))

    for required_token in required_tokens:
        normalized_required = normalize_token(required_token)

        # On ne dérive un execution_path comme preuve que si le contrat parle
        # explicitement de matérialisation. Les tokens *_executed_for_real ne
        # doivent pas suffire à justifier un dossier structurel.
        if "materialized" not in normalized_required:
            continue

        required_fragments = split_token_fragments(required_token)

        for fragment in candidate_fragments:
            if not fragment:
                continue

            # Matching plus strict : on évite les collisions trop larges sur
            # "release", "report", etc.
            if fragment == normalized_required:
                return required_token
            if fragment in required_fragments:
                return required_token
            if normalized_required.startswith(fragment + "_"):
                return required_token
            if normalized_required.endswith("_" + fragment):
                return required_token

    return None
'''


def replace_function(source: str, func_name: str, new_block: str) -> str:
    pattern = rf"def {func_name}\(.*?(?=^def |\Z)"
    updated, count = re.subn(pattern, new_block.rstrip() + "\n\n", source, flags=re.S | re.M)
    if count != 1:
        raise RuntimeError(f"Remplacement impossible ou ambigu pour {func_name}: {count=}")
    return updated


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Fichier introuvable: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")

    text = replace_function(
        text,
        "normalize_run_relative_pattern",
        NEW_NORMALIZE_RUN_RELATIVE_PATTERN,
    )
    text = replace_function(
        text,
        "execution_path_required_by_contract",
        NEW_EXECUTION_PATH_REQUIRED_BY_CONTRACT,
    )

    TARGET.write_text(text, encoding="utf-8")
    print(f"Patched: {TARGET}")


if __name__ == "__main__":
    main()