from pathlib import Path

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"[ERREUR] Bloc introuvable pour {label}")
    return text.replace(old, new, 1)

path = Path("docs/patcher/shared/reconcile_run.py")
text = path.read_text(encoding="utf-8")

# -------------------------------------------------------------------
# 1) Renommer la table hardcodée en fallback
# -------------------------------------------------------------------
text = replace_once(
    text,
    "STAGE_EVIDENCE: Dict[str, List[str]] = {\n",
    "STAGE_EVIDENCE_FALLBACK: Dict[str, List[str]] = {\n",
    "rename STAGE_EVIDENCE to STAGE_EVIDENCE_FALLBACK",
)

# -------------------------------------------------------------------
# 2) Remplacer matches_any_glob + stage_evidence_status
# -------------------------------------------------------------------
old_block = """def matches_any_glob(base: Path, pattern: str) -> bool:
    return any(base.glob(pattern))


def stage_evidence_status(run_root: Path, stage_id: str) -> Tuple[bool, List[str]]:
    missing: List[str] = []
    for pattern in STAGE_EVIDENCE.get(stage_id, []):
        if "*" in pattern or "?" in pattern or "[" in pattern:
            if not matches_any_glob(run_root, pattern):
                missing.append(pattern)
        else:
            if not (run_root / pattern).exists():
                missing.append(pattern)
    return len(missing) == 0, missing
"""

new_block = """def matches_any_glob(base: Path, pattern: str) -> bool:
    return any(base.glob(pattern))


def stage_skill_path(repo_root: Path, pipeline_id: str, stage_id: str) -> Path:
    return repo_root / "docs" / "pipelines" / pipeline_id / "stages" / f"{stage_id}.skill.yaml"


def normalize_run_relative_pattern(pattern: str, pipeline_id: str, run_id: str) -> str:
    prefixes = [
        f"docs/pipelines/{pipeline_id}/runs/<run_id>/",
        f"docs/pipelines/{pipeline_id}/runs/{run_id}/",
    ]
    for prefix in prefixes:
        if pattern.startswith(prefix):
            return pattern[len(prefix):]
    return pattern


def derive_stage_evidence_patterns(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    stage_id: str,
    mode: str,
) -> List[str]:
    skill_path = stage_skill_path(repo_root, pipeline_id, stage_id)
    skill_data = load_yaml_optional(skill_path)
    expected_outputs = skill_data.get("expected_outputs", {})
    if not isinstance(expected_outputs, dict):
        expected_outputs = {}

    mode_outputs = expected_outputs.get(mode, {})
    if not isinstance(mode_outputs, dict):
        mode_outputs = {}

    derived_patterns: List[str] = []

    for key in ("report_path_pattern", "primary_output_path_pattern"):
        value = mode_outputs.get(key)
        if isinstance(value, str) and value.strip():
            derived_patterns.append(value.strip())

    raw_artifacts = mode_outputs.get("required_raw_artifacts", [])
    if isinstance(raw_artifacts, list):
        for value in raw_artifacts:
            if isinstance(value, str) and value.strip():
                derived_patterns.append(value.strip())

    normalized: List[str] = []
    for pattern in derived_patterns:
        normalized_pattern = normalize_run_relative_pattern(pattern, pipeline_id, run_id)
        if normalized_pattern:
            normalized.append(normalized_pattern)

    if normalized:
        return sorted(set(normalized))

    return STAGE_EVIDENCE_FALLBACK.get(stage_id, [])


def stage_evidence_status(run_root: Path, evidence_patterns: List[str]) -> Tuple[bool, List[str]]:
    missing: List[str] = []
    for pattern in evidence_patterns:
        if "*" in pattern or "?" in pattern or "[" in pattern:
            if not matches_any_glob(run_root, pattern):
                missing.append(pattern)
        else:
            if not (run_root / pattern).exists():
                missing.append(pattern)
    return len(missing) == 0, missing
"""

text = replace_once(text, old_block, new_block, "replace hardcoded stage_evidence_status block")

# -------------------------------------------------------------------
# 3) Faire dériver les preuves dans l’évaluation du préfixe fiable
# -------------------------------------------------------------------
old_block = """    for stage in claimed_prefix:
        ok, missing = stage_evidence_status(run_root, stage)
        if ok:
            trusted_prefix.append(stage)
        else:
            first_non_trusted_stage = stage
            stage_missing_map[stage] = missing
            break
"""

new_block = """    for stage in claimed_prefix:
        evidence_patterns = derive_stage_evidence_patterns(
            repo_root=repo_root,
            pipeline_id=args.pipeline,
            run_id=args.run_id,
            stage_id=stage,
            mode=mode,
        )
        ok, missing = stage_evidence_status(run_root, evidence_patterns)
        if ok:
            trusted_prefix.append(stage)
        else:
            first_non_trusted_stage = stage
            stage_missing_map[stage] = missing
            break
"""

text = replace_once(text, old_block, new_block, "derive evidence in trusted prefix evaluation")

# -------------------------------------------------------------------
# 4) Faire dériver les preuves dans l’invalidation aval
# -------------------------------------------------------------------
old_block = """def invalidate_downstream_artifacts(
    *,
    run_root: Path,
    invalidated_stages: List[str],
    apply: bool,
) -> List[str]:
    removed: List[str] = []

    for stage in invalidated_stages:
        for pattern in STAGE_EVIDENCE.get(stage, []):
            if "*" in pattern or "?" in pattern or "[" in pattern:
                for match in run_root.glob(pattern):
                    if delete_path(match, apply=apply):
                        removed.append(str(match.relative_to(run_root)).replace("\\\\", "/"))
            else:
                path = run_root / pattern
                if delete_path(path, apply=apply):
                    removed.append(str(path.relative_to(run_root)).replace("\\\\", "/"))

        stage_record = run_root / "reports" / f"stage_completion_{stage}.yaml"
        if delete_path(stage_record, apply=apply):
            removed.append(str(stage_record.relative_to(run_root)).replace("\\\\", "/"))

    return sorted(set(removed))
"""

new_block = """def invalidate_downstream_artifacts(
    *,
    repo_root: Path,
    pipeline_id: str,
    run_id: str,
    mode: str,
    run_root: Path,
    invalidated_stages: List[str],
    apply: bool,
) -> List[str]:
    removed: List[str] = []

    for stage in invalidated_stages:
        evidence_patterns = derive_stage_evidence_patterns(
            repo_root=repo_root,
            pipeline_id=pipeline_id,
            run_id=run_id,
            stage_id=stage,
            mode=mode,
        )
        for pattern in evidence_patterns:
            if "*" in pattern or "?" in pattern or "[" in pattern:
                for match in run_root.glob(pattern):
                    if delete_path(match, apply=apply):
                        removed.append(str(match.relative_to(run_root)).replace("\\\\", "/"))
            else:
                path = run_root / pattern
                if delete_path(path, apply=apply):
                    removed.append(str(path.relative_to(run_root)).replace("\\\\", "/"))

        stage_record = run_root / "reports" / f"stage_completion_{stage}.yaml"
        if delete_path(stage_record, apply=apply):
            removed.append(str(stage_record.relative_to(run_root)).replace("\\\\", "/"))

    return sorted(set(removed))
"""

text = replace_once(text, old_block, new_block, "derive evidence in downstream invalidation")

# -------------------------------------------------------------------
# 5) Mettre à jour l’appel à invalidate_downstream_artifacts
# -------------------------------------------------------------------
old_block = """    removed_artifacts = invalidate_downstream_artifacts(
        run_root=run_root,
        invalidated_stages=invalidated_stages,
        apply=args.apply,
    )
"""

new_block = """    removed_artifacts = invalidate_downstream_artifacts(
        repo_root=repo_root,
        pipeline_id=args.pipeline,
        run_id=args.run_id,
        mode=mode,
        run_root=run_root,
        invalidated_stages=invalidated_stages,
        apply=args.apply,
    )
"""

text = replace_once(text, old_block, new_block, "update invalidate_downstream_artifacts call")

# -------------------------------------------------------------------
# 6) Ajouter une info de provenance dans la sortie
# -------------------------------------------------------------------
old_block = """            "trusted_prefix": trusted_prefix,
            "missing_evidence_by_stage": stage_missing_map,
"""

new_block = """            "trusted_prefix": trusted_prefix,
            "evidence_derivation_mode": "skill_expected_outputs_with_fallback",
            "missing_evidence_by_stage": stage_missing_map,
"""

text = replace_once(text, old_block, new_block, "add evidence derivation mode in output")

path.write_text(text, encoding="utf-8")
print("OK: reconcile_run.py dérive maintenant les preuves depuis les *.skill.yaml")