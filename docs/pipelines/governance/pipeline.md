# PIPELINE — governance

id: governance
version: 1
scope: repo-operating-model

## Goal

Maintenir la cohérence opératoire du repo Learn-it.

Ce pipeline gouverne :
- l’arborescence active
- les conventions
- la séparation operating / releases / legacy
- la cohérence des registres
- la cohérence des pipelines actifs
- la présence éventuelle de dérives documentaires ou structurelles

Il ne gouverne pas directement le contenu métier Learn-it.

## Canonical resources

### Prompts
- Governance audit: `docs/prompts/shared/Make10GovernanceAudit.md`
- Governance patch: `docs/prompts/shared/Make11GovernancePatch.md`
- Governance review: `docs/prompts/shared/Make12GovernanceReview.md`

### Specs and tools
- Patch DSL: `docs/specs/patch-dsl/current.md`
- Release Patch DSL: `docs/specs/release-patch/current.md`
- Apply patch: `docs/patcher/shared/apply_patch.py`
- Validate patchset: `docs/patcher/shared/validate_patchset.py`
- Apply release patch: `docs/patcher/shared/apply_release_patch.py`
- Validate release patch: `docs/patcher/shared/validate_release_patch.py`

### Repo sources under governance
- `docs/README.md`
- `docs/registry/operating_model.md`
- `docs/registry/pipelines.md`
- `docs/registry/resources.md`
- `docs/registry/conventions.md`
- `docs/specs/**`
- `docs/prompts/shared/**`
- `docs/patcher/shared/**`
- `docs/pipelines/**`
- `docs/cores/current/**`
- `docs/cores/releases/**`
- `docs/architecture/**`
- `legacy/**`

## Staging

- inputs: `docs/pipelines/governance/inputs/`
- work/01_scan: `docs/pipelines/governance/work/01_scan/`
- work/02_audit: `docs/pipelines/governance/work/02_audit/`
- work/03_arbitrage: `docs/pipelines/governance/work/03_arbitrage/`
- work/04_patch: `docs/pipelines/governance/work/04_patch/`
- work/05_validation: `docs/pipelines/governance/work/05_validation/`
- work/06_apply: `docs/pipelines/governance/work/06_apply/`
- work/07_review: `docs/pipelines/governance/work/07_review/`
- outputs: `docs/pipelines/governance/outputs/`
- reports: `docs/pipelines/governance/reports/`

## Stages

### STAGE_01_REPO_SCAN
Objectif :
- scanner la structure active du repo
- identifier les couches présentes
- préparer l’inventaire opérationnel

Inputs :
- repo courant
- éventuellement notes manuelles dans `inputs/`

Outputs :
- `work/01_scan/repo_inventory.md`

### STAGE_02_GOVERNANCE_AUDIT
Objectif :
- comparer l’état réel du repo à l’operating model attendu

Prompt :
- `docs/prompts/shared/Make10GovernanceAudit.md`

Outputs :
- `work/02_audit/governance_audit.md`

### STAGE_03_ARBITRAGE
Objectif :
- décider ce qu’il faut corriger, promouvoir, archiver ou ignorer

Outputs :
- `work/03_arbitrage/governance_arbitrage.md`

### STAGE_04_PATCH_SYNTHESIS
Objectif :
- produire soit un patch DSL standard
- soit un release patch repo-level
- soit les deux

Prompt :
- `docs/prompts/shared/Make11GovernancePatch.md`

Outputs :
- `work/04_patch/governance_patchset.yaml`
- ou `work/04_patch/governance_release_patchset.yaml`

### STAGE_05_VALIDATION
Objectif :
- valider le patch de gouvernance avant application

Tools :
- `docs/patcher/shared/validate_patchset.py`
- `docs/patcher/shared/validate_release_patch.py`

Outputs :
- `work/05_validation/governance_patch_validation.yaml`

### STAGE_06_APPLY
Objectif :
- appliquer le patch validé

Outputs :
- `work/06_apply/`
- `reports/governance_execution_report.yaml`

### STAGE_07_POSTCHECK
Objectif :
- vérifier que le repo raconte maintenant une seule vérité opérationnelle

Prompt :
- `docs/prompts/shared/Make12GovernanceReview.md`

Outputs :
- `work/07_review/governance_review.md`
- `outputs/governance_summary.md`

## Success criteria

Le pipeline est considéré comme réussi si :
- aucun chemin actif ne pointe vers `legacy/`
- les fichiers `current/` sont bien canoniques
- les registres reflètent la réalité du repo
- les pipelines actifs sont complets et cohérents
- l’operating model est aligné avec l’arborescence réelle
- aucune ambiguïté majeure operating / release / legacy ne subsiste
