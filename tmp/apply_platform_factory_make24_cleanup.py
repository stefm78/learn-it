#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Pattern not found in {label}: {old!r}")
    return text.replace(old, new, 1)


def replace_all(text: str, old: str, new: str, label: str, expected_count: int | None = None) -> str:
    count = text.count(old)
    if count == 0:
        raise SystemExit(f"Pattern not found in {label}: {old!r}")
    if expected_count is not None and count != expected_count:
        raise SystemExit(
            f"Unexpected occurrence count in {label}: expected {expected_count}, got {count} for {old!r}"
        )
    return text.replace(old, new)


def rewrite(path_str: str, transform) -> None:
    path = REPO_ROOT / path_str
    original = path.read_text(encoding="utf-8")
    updated = transform(original)
    if updated == original:
        raise SystemExit(f"No changes produced for {path_str}")
    path.write_text(updated, encoding="utf-8")
    print(f"UPDATED {path_str}")


rewrite(
    "docs/pipelines/platform_factory/pipeline.md",
    lambda text: replace_once(
        replace_once(
            text,
            "- `docs/prompts/shared/Make24PlatformFactoryReview.md`",
            "- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`",
            "docs/pipelines/platform_factory/pipeline.md",
        ),
        "## Required shared prompts\n\nExpected shared prompt family:\n- `docs/prompts/shared/Challenge_platform_factory.md`\n- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`\n- `docs/prompts/shared/Make22PlatformFactoryPatch.md`\n- `docs/prompts/shared/Make23PlatformFactoryValidation.md`\n- `docs/prompts/shared/Make24PlatformFactoryReview.md`\n\nPrompt usage companion:",
        "## Required shared prompts\n\nExpected shared prompt family:\n- `docs/prompts/shared/Challenge_platform_factory.md`\n- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`\n- `docs/prompts/shared/Make22PlatformFactoryPatch.md`\n- `docs/prompts/shared/Make23PlatformFactoryValidation.md`\n\nStage-specific launch prompts:\n- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`\n- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`\n- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`\n\nPrompt usage companion:",
        "docs/pipelines/platform_factory/pipeline.md",
    ),
)


def transform_prompt_usage(text: str) -> str:
    text = replace_once(
        text,
        "Ce document complète `pipeline.md` en indiquant quel prompt partagé utiliser à chaque étape du pipeline `platform_factory`.",
        "Ce document complète `pipeline.md` en indiquant quel prompt utiliser à chaque étape du pipeline `platform_factory`.",
        "docs/pipelines/platform_factory/PROMPT_USAGE.md",
    )
    text = replace_once(
        text,
        "Prompts disponibles:\n- `docs/prompts/shared/Challenge_platform_factory.md`\n- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`\n- `docs/prompts/shared/Make22PlatformFactoryPatch.md`\n- `docs/prompts/shared/Make23PlatformFactoryValidation.md`\n- `docs/prompts/shared/Make24PlatformFactoryReview.md`",
        "Prompts disponibles:\n- `docs/prompts/shared/Challenge_platform_factory.md`\n- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`\n- `docs/prompts/shared/Make22PlatformFactoryPatch.md`\n- `docs/prompts/shared/Make23PlatformFactoryValidation.md`\n- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`\n- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`\n- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`",
        "docs/pipelines/platform_factory/PROMPT_USAGE.md",
    )
    text = replace_once(
        text,
        "### STAGE_08_FACTORY_PROMOTION",
        "### STAGE_08_FACTORY_PROMOTE_CURRENT",
        "docs/pipelines/platform_factory/PROMPT_USAGE.md",
    )
    text = replace_once(
        text,
        "### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE\nPrompt principal :\n- `docs/prompts/shared/Make24PlatformFactoryReview.md`\n\nBut :\n- produire une appréciation de clôture ;\n- capitaliser les décisions ;\n- préparer le prochain cycle.",
        "### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE\nPrompt principal :\n- `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`\n\nBut :\n- exécuter le closeout déterministe du run ;\n- archiver `work/`, `reports/` et `outputs/` ;\n- produire `platform_factory_closeout_report.yaml` et `platform_factory_summary.md` ;\n- réinitialiser `work/` pour le prochain cycle.",
        "docs/pipelines/platform_factory/PROMPT_USAGE.md",
    )
    return text


rewrite("docs/pipelines/platform_factory/PROMPT_USAGE.md", transform_prompt_usage)


def transform_plan(text: str) -> str:
    text = replace_all(
        text,
        "- `Make24PlatformFactoryReview.md`",
        "- `Make24PlatformFactoryReview.md` *(historical candidate, no longer retained in the nominal deterministic Stage 09 flow)*",
        "docs/architecture/Platform_Factory_Plan.md",
        expected_count=2,
    )
    return text


rewrite("docs/architecture/Platform_Factory_Plan.md", transform_plan)

obsolete = REPO_ROOT / "docs/prompts/shared/Make24PlatformFactoryReview.md"
if obsolete.exists():
    obsolete.unlink()
    print("DELETED docs/prompts/shared/Make24PlatformFactoryReview.md")
else:
    print("ALREADY ABSENT docs/prompts/shared/Make24PlatformFactoryReview.md")

print("DONE")
