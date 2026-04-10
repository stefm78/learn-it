# tmp

Zone temporaire, non canonique, pour patches, remplacements, scripts one-shot, brouillons et notes intermédiaires.
Aucun contenu de `tmp/` n’a d’effet canonique sans promotion explicite.

```yaml
TMP_WORKSPACE:
  id: TMP_WORKSPACE_USAGE_V1
  version: 1.1.0
  status: active
  description: >
    Spécification du répertoire tmp/ comme zone de travail temporaire,
    libre et non canonique du repo.

  purpose:
    primary: >
      Préparer, comparer, tester, déposer ou échanger des artefacts intermédiaires
      sans polluer les zones gouvernées du repo.
    posture:
      - temporary
      - non_canonical
      - non_governed
      - replaceable
      - removable

  invariants:
    - id: TMP_INV_NON_CANONICAL
      statement: Tout artefact de tmp/ est non canonique.
    - id: TMP_INV_EXPLICIT_PROMOTION_REQUIRED
      statement: Aucun artefact de tmp/ ne produit d’effet canonique sans promotion explicite.
    - id: TMP_INV_NO_STRUCTURAL_DEPENDENCY
      statement: Aucun pipeline ne doit dépendre structurellement d’un contenu placé dans tmp/.
    - id: TMP_INV_TEMPORARY_BY_NATURE
      statement: Tout contenu de tmp/ est présumé modifiable, remplaçable ou supprimable à tout moment.
    - id: TMP_INV_NOT_SOURCE_OF_TRUTH
      statement: tmp/ ne doit jamais devenir une source de vérité durable du repo.

  allowed_artifact_kinds:
    - patch
    - full_replacement
    - one_shot_script
    - prompt_draft
    - analysis_note
    - handover_artifact
    - temporary_workspace
    - miscellaneous

  allowed_uses:
    - id: TMP_USE_PATCH_STAGING
      kind: patch
      description: Déposer un patch temporaire à relire ou appliquer localement.
      examples:
        - tmp/constitution_stage02_arbitrage.patch
        - tmp/platform_factory_cleanup.patch

    - id: TMP_USE_FULL_REPLACEMENT
      kind: full_replacement
      description: Déposer une version complète de remplacement quand un patch est trop fragile.
      examples:
        - tmp/arbitrage.md
        - tmp/platform_factory_pipeline.md

    - id: TMP_USE_ONE_SHOT_SCRIPT
      kind: one_shot_script
      description: Déposer un script ponctuel de transformation ou de nettoyage.
      examples:
        - tmp/apply_platform_factory_make24_cleanup_v2.py
        - tmp/platform_factory_harden_operator_flow.py

    - id: TMP_USE_PROMPT_DRAFT
      kind: prompt_draft
      description: Déposer des variantes, sauvegardes ou brouillons de prompts.
      examples:
        - tmp/LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.original.md
        - tmp/LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.with_contract.md

    - id: TMP_USE_INTERMEDIATE_NOTES
      kind: analysis_note
      description: Déposer des notes de travail, analyses, synthèses externes ou arbitrages préparatoires.

    - id: TMP_USE_SUBWORKSPACE
      kind: temporary_workspace
      description: Créer un sous-répertoire dédié à un chantier ponctuel.
      examples:
        - tmp/platform_factory_stage07_hardening/
        - tmp/constitution_cleanup/

    - id: TMP_USE_HANDOVER
      kind: handover_artifact
      description: Déposer un artefact à télécharger, tester, relire ou transmettre.

  placement_decision:
    allow_tmp_when:
      - preparatory
      - exploratory
      - temporary
      - pending_arbitration
      - operator_or_ia_exchange
    reject_tmp_when:
      - official_pipeline_output
      - canonical_report
      - release_artifact
      - source_of_truth
      - durable_tooling

  naming_conventions:
    patch_pattern: tmp/<subject>_<stage>.patch
    markdown_pattern: tmp/<subject>_<usage>.md
    script_pattern: tmp/<subject>_<action>.py
    subworkspace_pattern: tmp/<workspace>/

  local_subworkspace_recommendations:
    recommended_contents:
      - README.md
      - scripts
      - comparisons
      - drafts
      - preparatory_artifacts
    rule: >
      Quand un sous-répertoire tmp/ contient plusieurs fichiers,
      un README local est recommandé.

  lifecycle:
    expected_duration: short_lived
    cleanup_rule: >
      Supprimer ou remplacer les artefacts tmp/ dès qu’ils n’apportent plus de valeur,
      ou dès qu’une version canonique a été intégrée ailleurs.
    keep_if:
      - still_useful_for_operator
      - active_workspace
      - handover_in_progress

  constraints:
    - id: TMP_CONSTRAINT_NO_OFFICIAL_REPORT
      statement: tmp/ ne doit pas héberger un report canonique présenté comme output officiel.
    - id: TMP_CONSTRAINT_NO_RELEASE_SOURCE
      statement: tmp/ ne doit pas être utilisé comme source directe d’une release.
    - id: TMP_CONSTRAINT_NO_IMPLICIT_VALIDITY
      statement: Aucun contenu de tmp/ ne doit être supposé exact, final ou promu par défaut.
    - id: TMP_CONSTRAINT_NO_DURABLE_RUNTIME_ROLE
      statement: Un script devenu indispensable au fonctionnement normal doit sortir de tmp/.

  actions:
    - id: TMP_ACTION_STAGE_PATCH
      effect: Déposer un patch temporaire dans tmp/.
    - id: TMP_ACTION_STAGE_FULL_REPLACEMENT
      effect: Déposer une version complète de remplacement dans tmp/.
    - id: TMP_ACTION_STAGE_SCRIPT
      effect: Déposer un script one-shot dans tmp/.
    - id: TMP_ACTION_STAGE_DRAFT
      effect: Déposer un brouillon, une note ou un artefact de handover dans tmp/.
    - id: TMP_ACTION_CREATE_SUBWORKSPACE
      effect: Créer un sous-répertoire temporaire dédié à un chantier.
    - id: TMP_ACTION_PROMOTE_ARTIFACT
      effect: Copier, appliquer ou intégrer explicitement un contenu tmp/ vers une zone canonique.
    - id: TMP_ACTION_CLEANUP
      effect: Supprimer un contenu tmp/ devenu obsolète ou inutile.

  summary:
    tmp_equals: zone_de_chantier_libre
    governed_zones:
      - work/
      - reports/
      - outputs/
    final_statement: >
      tmp/ est une zone de travail pratique ; ce n’est pas une couche canonique du repo.
```
