# Worklog — transformation modularisation des Core

## Règle d'usage

Ce journal est append-only.
Chaque entrée doit rester courte, factuelle, datée, et permettre une reprise sans contexte de conversation.

Format recommandé :
- Date
- Auteur ou mode (`human`, `ai`, `human+ai`)
- Changement effectué
- Décision prise
- Prochaine action utile

---

## 2026-04-11 — bootstrap initial

- Mode : `human+ai`
- Branche créée : `feat/core-modularization-bootstrap`
- Artefacts ajoutés :
  - `docs/transformations/core_modularization/README.md`
  - `docs/transformations/core_modularization/ROADMAP.md`
  - `docs/transformations/core_modularization/STATUS.yaml`
  - `docs/transformations/core_modularization/WORKLOG.md`

### Décisions prises

1. La transformation doit être pilotée depuis le repo, pas depuis le contexte implicite d'une conversation.
2. Le repo ne doit pas exploser en nombre de pipelines ni de prompts.
3. La cible est un régime :
   - sources modulaires gouvernées,
   - bundle canonique compilé,
   - projections dérivées validées,
   - pipelines capables de traiter des scopes bornés,
   - intégration globale centralisée avant promotion.
4. Le strict nécessaire posé à ce stade est un socle de continuité et de pilotage, pas une refonte technique immédiate.

### État constaté

- Le chantier est amorcé mais aucun contrat de scope n'est encore matérialisé.
- Aucun pipeline n'a encore été rendu scope-aware.
- Aucun artefact canonique n'a encore été modularisé effectivement.

### Prochaine action utile

Définir le premier jalon J1 :
- `scope_manifest`
- `impact_bundle`
- `integration_gate`

Puis déterminer le delta minimal à apporter au pipeline `constitution` pour supporter un premier run borné.

---

## 2026-04-11 — J1 posé et remplacement pipeline préparé

- Mode : `human+ai`
- J1 défini dans le repo :
  - `docs/transformations/core_modularization/J1_SCOPED_RUN_CONTRACT.md`
  - `docs/transformations/core_modularization/templates/scope_manifest.template.yaml`
  - `docs/transformations/core_modularization/templates/impact_bundle.template.yaml`
  - `docs/transformations/core_modularization/templates/integration_gate.template.yaml`
  - `docs/transformations/core_modularization/J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md`
- Remplacement préparé pour `docs/pipelines/constitution/pipeline.md` dans :
  - `tmp/constitution_pipeline_scoped_v1_1/01_header_to_stage03.md`
  - `tmp/constitution_pipeline_scoped_v1_1/02_stage04_to_stage06.md`
  - `tmp/constitution_pipeline_scoped_v1_1/03_stage07_to_end.md`
- Notice d'application ajoutée :
  - `tmp/APPLY_constitution_pipeline_scoped_v1_1.md`

### Décisions prises

1. La première adaptation réelle porte sur le pipeline `constitution`, pas sur `platform_factory`.
2. Le pipeline n'est pas dupliqué ; il reçoit un mode borné piloté par artefacts de scope.
3. Le write direct du fichier cible n'a pas été finalisé via le connecteur ; un remplacement exact prêt à appliquer a été déposé dans `tmp/` pour ne pas bloquer le chantier.
4. Après application locale du remplacement, `STATUS.yaml` et `WORKLOG.md` doivent être synchronisés avec l'état réellement appliqué.

### État constaté

- Le contrat minimal d'un run borné est désormais explicite.
- Le contenu scope-aware du pipeline `constitution` est prêt.
- Les prompts de challenge et d'arbitrage ne sont pas encore ajustés.

### Prochaine action utile

1. Appliquer localement le remplacement de `docs/pipelines/constitution/pipeline.md`.
2. Mettre à jour `docs/transformations/core_modularization/STATUS.yaml` et `WORKLOG.md` à partir des drafts préparés dans `tmp/`.
3. Adapter `Challenge_constitution.md` et `Make04ConstitutionArbitrage.md` au mode borné.
