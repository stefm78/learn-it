#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path_str: str) -> str:
    return (REPO_ROOT / path_str).read_text(encoding="utf-8")


def write(path_str: str, content: str) -> None:
    (REPO_ROOT / path_str).write_text(content, encoding="utf-8")
    print(f"UPDATED {path_str}")


def ensure_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"Required content not found in {label}: {needle!r}")


# -----------------------------------------------------------------------------
# pipeline.md
# -----------------------------------------------------------------------------
pipeline_path = "docs/pipelines/platform_factory/pipeline.md"
pipeline = read(pipeline_path)
old_stage09_prompt = "- `docs/prompts/shared/Make24PlatformFactoryReview.md`"
new_stage09_prompt = "- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`"
if old_stage09_prompt in pipeline:
    pipeline = pipeline.replace(old_stage09_prompt, new_stage09_prompt, 1)

old_shared_block = """## Required shared prompts

Expected shared prompt family:
- `docs/prompts/shared/Challenge_platform_factory.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- `docs/prompts/shared/Make24PlatformFactoryReview.md`

Prompt usage companion:
"""
new_shared_block = """## Required shared prompts

Expected shared prompt family:
- `docs/prompts/shared/Challenge_platform_factory.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`

Stage-specific launch prompts:
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`
- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`

Prompt usage companion:
"""
if old_shared_block in pipeline:
    pipeline = pipeline.replace(old_shared_block, new_shared_block, 1)

ensure_contains(pipeline, new_stage09_prompt, pipeline_path)
ensure_contains(pipeline, "Stage-specific launch prompts:", pipeline_path)
write(pipeline_path, pipeline)


# -----------------------------------------------------------------------------
# PROMPT_USAGE.md
# -----------------------------------------------------------------------------
prompt_usage_path = "docs/pipelines/platform_factory/PROMPT_USAGE.md"
prompt_usage = read(prompt_usage_path)

prompt_usage = prompt_usage.replace(
    "Ce document complète `pipeline.md` en indiquant quel prompt partagé utiliser à chaque étape du pipeline `platform_factory`.",
    "Ce document complète `pipeline.md` en indiquant quel prompt utiliser à chaque étape du pipeline `platform_factory`.",
)

lines = prompt_usage.splitlines()
new_lines: list[str] = []
i = 0
while i < len(lines):
    line = lines[i]

    if line == "Prompts disponibles:":
        new_lines.extend([
            "Prompts disponibles:",
            "- `docs/prompts/shared/Challenge_platform_factory.md`",
            "- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`",
            "- `docs/prompts/shared/Make22PlatformFactoryPatch.md`",
            "- `docs/prompts/shared/Make23PlatformFactoryValidation.md`",
            "- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`",
            "- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`",
            "- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`",
        ])
        i += 1
        while i < len(lines) and lines[i].startswith("- `"):
            i += 1
        continue

    if line == "### STAGE_08_FACTORY_PROMOTION":
        new_lines.append("### STAGE_08_FACTORY_PROMOTE_CURRENT")
        i += 1
        continue

    if line == "### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE":
        new_lines.extend([
            "### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE",
            "Prompt principal :",
            "- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`",
            "",
            "But :",
            "- exécuter le closeout déterministe du run ;",
            "- archiver `work/`, `reports/` et `outputs/` ;",
            "- produire `platform_factory_closeout_report.yaml` et `platform_factory_summary.md` ;",
            "- réinitialiser `work/` pour le prochain cycle.",
        ])
        i += 1
        while i < len(lines) and lines[i] != "---":
            i += 1
        continue

    new_lines.append(line)
    i += 1

prompt_usage = "\n".join(new_lines) + "\n"
ensure_contains(prompt_usage, "- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`", prompt_usage_path)
ensure_contains(prompt_usage, "### STAGE_08_FACTORY_PROMOTE_CURRENT", prompt_usage_path)
write(prompt_usage_path, prompt_usage)


# -----------------------------------------------------------------------------
# Platform_Factory_Plan.md
# -----------------------------------------------------------------------------
plan_path = "docs/architecture/Platform_Factory_Plan.md"
plan = read(plan_path)
plan = plan.replace(
    "- `Make24PlatformFactoryReview.md`",
    "- `Make24PlatformFactoryReview.md` *(historical candidate, no longer retained in the nominal deterministic Stage 09 flow)*",
)
ensure_contains(
    plan,
    "Make24PlatformFactoryReview.md` *(historical candidate, no longer retained in the nominal deterministic Stage 09 flow)*",
    plan_path,
)
write(plan_path, plan)


# -----------------------------------------------------------------------------
# Delete obsolete prompt
# -----------------------------------------------------------------------------
obsolete = REPO_ROOT / "docs/prompts/shared/Make24PlatformFactoryReview.md"
if obsolete.exists():
    obsolete.unlink()
    print("DELETED docs/prompts/shared/Make24PlatformFactoryReview.md")
else:
    print("ALREADY ABSENT docs/prompts/shared/Make24PlatformFactoryReview.md")

print("DONE")
