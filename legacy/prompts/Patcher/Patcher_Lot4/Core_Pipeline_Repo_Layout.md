# Core Pipeline Repo Layout

## Objectif

Ce document propose une arborescence simple et stable pour industrialiser
le pipeline Challenge → Patch → Validation → Release.

## Arborescence recommandée

```text
learn-it/
  docs/
    constitution/
    referentiel/
    link/
    prompts/
      Challenge_constitution.md
      Make02CoreValidation.md
      Make05CorePatch.md
      Make05CorePatch_Lot2.md
      Make05CorePatch_Lot3.md
      Make05CorePatch_Lot4.md
      Make06PatchValidation.md
      Make07CoreRelease.md
    patch_dsl/
      Patch_DSL_v2.md
      Patch_DSL_v2_5.md
      Patch_DSL_v3.md
      Patch_DSL_v4.md
    tools/
      apply_learnit_core_patch.py
      apply_learnit_core_patch_v2.py
      apply_learnit_core_patch_v2_5.py
      apply_learnit_core_patch_v3.py
      apply_learnit_core_patch_v4.py
      validate_patchset_v2_5.py
      validate_patchset_v3.py
      validate_patchset_v4.py
    patches/
      patchset.yaml
      patchset_v2_example.yaml
      patchset_v2_5_example.yaml
      patchset_v3_example.yaml
      patchset_v4_example.yaml
    reports/
      patch_execution_report.yaml
      patch_validation_report.yaml
```

## Pipeline recommandé

1. Challenge :
   - prompt : `Challenge_constitution.md`
   - sortie : audit structuré

2. Arbitrage :
   - humain ou prompt secondaire
   - sortie : corrections retenues

3. Synthesis patch :
   - prompt : `Make05CorePatch_Lot4.md`
   - sortie : `patchset.yaml`

4. Validation patch :
   - script : `validate_patchset_v4.py`
   - sortie : PASS / FAIL patch-level

5. Dry-run :
   - script : `apply_learnit_core_patch_v4.py ... true`
   - sortie : rapport d’exécution sans écriture

6. Apply :
   - script : `apply_learnit_core_patch_v4.py ... false`
   - sortie : YAML modifiés + `.bak`

7. Validation Core :
   - prompt : `Make02CoreValidation.md`
   - sortie : PASS / FAIL structurel

8. Release :
   - prompt : `Make07CoreRelease.md`
   - sortie : plan de versioning et synchronisation

## Convention de nommage

- patchs : `PATCH_<scope>_<version>_<seq>`
- reports : `patch_execution_report_<date>.yaml`
- releases : `release_plan_<core>_<version>.md`

## Recommandations pratiques

- toujours exécuter un dry-run avant écriture ;
- stocker les patchsets dans Git ;
- stocker les rapports d’exécution dans un dossier dédié ;
- garder le LINK aussi léger que possible ;
- réserver `replace_text scope: all_strings` aux corrections de gouvernance/version ;
- faire suivre tout rename d’un dry-run et d’une validation structurelle.
