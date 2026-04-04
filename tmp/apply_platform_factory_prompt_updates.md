# Apply platform_factory prompt updates

## Backup current files

```bash
cp docs/prompts/shared/Make21PlatformFactoryArbitrage.md tmp/Make21PlatformFactoryArbitrage.backup.md
cp docs/prompts/shared/Make22PlatformFactoryPatch.md tmp/Make22PlatformFactoryPatch.backup.md
cp docs/prompts/shared/Make23PlatformFactoryValidation.md tmp/Make23PlatformFactoryValidation.backup.md
cp docs/prompts/shared/Make24PlatformFactoryReview.md tmp/Make24PlatformFactoryReview.backup.md
```

## Apply proposed versions

```bash
cp tmp/Make21PlatformFactoryArbitrage.proposed.md docs/prompts/shared/Make21PlatformFactoryArbitrage.md
cp tmp/Make22PlatformFactoryPatch.proposed.md docs/prompts/shared/Make22PlatformFactoryPatch.md
cp tmp/Make23PlatformFactoryValidation.proposed.md docs/prompts/shared/Make23PlatformFactoryValidation.md
cp tmp/Make24PlatformFactoryReview.proposed.md docs/prompts/shared/Make24PlatformFactoryReview.md
```

## Optional quick diff check

```bash
git diff -- docs/prompts/shared/Make21PlatformFactoryArbitrage.md docs/prompts/shared/Make22PlatformFactoryPatch.md docs/prompts/shared/Make23PlatformFactoryValidation.md docs/prompts/shared/Make24PlatformFactoryReview.md
```

## Recommended next step after prompt application

Review and harmonize:
- `docs/pipelines/platform_factory/pipeline.md`
- `docs/pipelines/platform_factory/PROMPT_USAGE.md`

Reason:
- current stage naming is not fully aligned between these two files.
