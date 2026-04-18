#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZE_RELEASE_PATH = ROOT / 'docs/patcher/shared/materialize_release.py'
STAGE07_PATH = ROOT / 'docs/pipelines/constitution/stages/STAGE_07_RELEASE_MATERIALIZATION.skill.yaml'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f'[{label}] bloc introuvable')
    return text.replace(old, new, 1)


def patch_materialize_release(text: str) -> str:
    old = '''def semantic_version_aliases(version: str) -> List[str]:
    aliases = {version}
    if version.endswith("_FINAL"):
        aliases.add(version.replace("_FINAL", ""))
    raw = version.replace("_FINAL", "")
    if raw.startswith("V") and "_" in raw:
        major_minor = raw[1:]
        aliases.add(f"v{major_minor.replace('_', '.')}")
        aliases.add(f"V{major_minor.replace('_', '.')}")
    return sorted(aliases, key=len, reverse=True)


def build_editorial_replacements(target_versions: Dict[str, Any]) -> List[Tuple[str, str, None]]:
    replacements: List[Tuple[str, str, None]] = []
    seen = set()
    for role, entry in target_versions.items():
        if not isinstance(entry, dict):
            continue
        current_version = entry.get("current_version")
        target_version = entry.get("target_version")
        current_core_id = entry.get("current_core_id")
        target_core_id = entry.get("target_core_id")
        if isinstance(current_core_id, str) and isinstance(target_core_id, str) and current_core_id != target_core_id:
            key = (current_core_id, target_core_id)
            if key not in seen:
                seen.add(key)
                replacements.append((current_core_id, target_core_id, None))
        if isinstance(current_version, str) and isinstance(target_version, str) and current_version != target_version:
            current_aliases = semantic_version_aliases(current_version)
            target_aliases = semantic_version_aliases(target_version)
            for old_alias, new_alias in zip(current_aliases, target_aliases):
                key = (old_alias, new_alias)
                if old_alias != new_alias and key not in seen:
                    seen.add(key)
                    replacements.append((old_alias, new_alias, None))
    return replacements
'''
    new = '''def semantic_version_aliases(version: str) -> List[str]:
    aliases = {version}
    if version.endswith("_FINAL"):
        aliases.add(version.replace("_FINAL", ""))
    raw = version.replace("_FINAL", "")
    if raw.startswith("V") and "_" in raw:
        major_minor = raw[1:]
        aliases.add(f"v{major_minor.replace('_', '.')}")
        aliases.add(f"V{major_minor.replace('_', '.')}")
    return sorted(aliases, key=len, reverse=True)


def build_editorial_replacements(target_versions: Dict[str, Any]) -> List[Tuple[str, str, str | None]]:
    replacements: List[Tuple[str, str, str | None]] = []
    seen = set()
    for role, entry in target_versions.items():
        if not isinstance(entry, dict):
            continue
        current_version = entry.get("current_version")
        target_version = entry.get("target_version")
        current_core_id = entry.get("current_core_id")
        target_core_id = entry.get("target_core_id")
        if isinstance(current_core_id, str) and isinstance(target_core_id, str) and current_core_id != target_core_id:
            key = (role, current_core_id, target_core_id)
            if key not in seen:
                seen.add(key)
                replacements.append((current_core_id, target_core_id, role))
        if isinstance(current_version, str) and isinstance(target_version, str) and current_version != target_version:
            current_aliases = semantic_version_aliases(current_version)
            target_aliases = semantic_version_aliases(target_version)
            for old_alias, new_alias in zip(current_aliases, target_aliases):
                key = (role, old_alias, new_alias)
                if old_alias != new_alias and key not in seen:
                    seen.add(key)
                    replacements.append((old_alias, new_alias, role))
    return replacements
'''
    return replace_once(text, old, new, 'materialize_release.py')


def patch_stage07(text: str) -> str:
    text = replace_once(
        text,
        '''script_execution_contract:
  required_before_pass_or_fail:
    - build_release_plan_executed_for_real
    - validate_release_plan_executed_for_real
    - materialize_release_executed_for_real
    - validate_release_manifest_executed_for_real
    - release_plan_yaml_materialized
    - release_manifest_yaml_materialized
''',
        '''script_execution_contract:
  required_before_pass_or_fail:
    - build_release_plan_executed_for_real
    - validate_release_plan_executed_for_real
    - materialize_release_executed_for_real
    - validate_release_manifest_executed_for_real
    - release_plan_yaml_materialized
    - release_plan_validation_yaml_materialized
    - release_materialization_report_yaml_materialized
    - release_manifest_yaml_materialized
    - release_manifest_validation_yaml_materialized
''',
        'stage07 skill',
    )

    text = replace_once(
        text,
        '''expected_outputs:
  bounded_local_run:
    report_path_pattern: docs/pipelines/constitution/runs/<run_id>/work/07_release/release_plan.yaml
  parallel_consolidation:
    report_path_pattern: docs/pipelines/constitution/work/consolidation/release_plan.yaml
  nominal_global:
    report_path_pattern: docs/pipelines/constitution/work/07_release/release_plan.yaml
  bounded_transition:
    report_path_pattern: docs/pipelines/constitution/work/07_release/release_plan.yaml
''',
        '''expected_outputs:
  bounded_local_run:
    primary_output_path_pattern: docs/pipelines/constitution/runs/<run_id>/work/07_release/release_plan.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/runs/<run_id>/reports/release_plan_validation.yaml
      - docs/pipelines/constitution/runs/<run_id>/reports/release_materialization_report.yaml
      - docs/pipelines/constitution/runs/<run_id>/reports/release_manifest_validation.yaml
  parallel_consolidation:
    primary_output_path_pattern: docs/pipelines/constitution/work/consolidation/release_plan.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/reports/release_plan_validation.yaml
      - docs/pipelines/constitution/reports/release_materialization_report.yaml
      - docs/pipelines/constitution/reports/release_manifest_validation.yaml
  nominal_global:
    primary_output_path_pattern: docs/pipelines/constitution/work/07_release/release_plan.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/reports/release_plan_validation.yaml
      - docs/pipelines/constitution/reports/release_materialization_report.yaml
      - docs/pipelines/constitution/reports/release_manifest_validation.yaml
  bounded_transition:
    primary_output_path_pattern: docs/pipelines/constitution/work/07_release/release_plan.yaml
    required_raw_artifacts:
      - docs/pipelines/constitution/reports/release_plan_validation.yaml
      - docs/pipelines/constitution/reports/release_materialization_report.yaml
      - docs/pipelines/constitution/reports/release_manifest_validation.yaml
''',
        'stage07 skill',
    )

    text = replace_once(
        text,
        '''completion_evidence:
  required:
    - release_commands_emitted_or_executed
    - real_execution_evidence_declared
    - release_plan_materialized
    - release_manifest_materialized
    - final_status_is_pass_fail_or_blocked
    - human_actions_explicitly_stated_in_output
  not_sufficient:
    - informal_chat_summary_only
    - release_reasoning_without_script_evidence
    - pass_without_materialized_release_artifacts
    - simulated_script_execution
''',
        '''completion_evidence:
  required:
    - release_commands_emitted_or_executed
    - real_execution_evidence_declared
    - release_plan_materialized
    - release_plan_validation_materialized
    - release_materialization_report_materialized
    - release_manifest_materialized
    - release_manifest_validation_materialized
    - final_status_is_pass_fail_or_blocked
    - human_actions_explicitly_stated_in_output
  not_sufficient:
    - informal_chat_summary_only
    - release_reasoning_without_script_evidence
    - pass_without_materialized_release_artifacts
    - pass_without_release_manifest_validation_yaml
    - simulated_script_execution
''',
        'stage07 skill',
    )
    return text


def main() -> None:
    materialize_release = MATERIALIZE_RELEASE_PATH.read_text(encoding='utf-8')
    stage07 = STAGE07_PATH.read_text(encoding='utf-8')

    materialize_release = patch_materialize_release(materialize_release)
    stage07 = patch_stage07(stage07)

    MATERIALIZE_RELEASE_PATH.write_text(materialize_release, encoding='utf-8', newline='\n')
    STAGE07_PATH.write_text(stage07, encoding='utf-8', newline='\n')

    print('Patched:')
    print('-', MATERIALIZE_RELEASE_PATH.relative_to(ROOT))
    print('-', STAGE07_PATH.relative_to(ROOT))


if __name__ == '__main__':
    main()
