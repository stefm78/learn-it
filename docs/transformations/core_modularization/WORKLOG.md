# Worklog — transformation modularisation des Core

## Règle d'usage

Ce journal est append-only.
Chaque entrée doit rester courte, factuelle, datée, et permettre une reprise sans contexte de conversation.

---

## 2026-04-11 — bootstrap initial

- Mode : `human+ai`
- Branche créée : `feat/core-modularization-bootstrap`
- Artefacts ajoutés : README, ROADMAP, STATUS, WORKLOG.

### Décisions prises

1. La transformation doit être pilotée depuis le repo.
2. Le repo ne doit pas exploser en pipelines ni en prompts.
3. La cible est un régime : sources modulaires gouvernées, bundle canonique compilé, projections dérivées validées, pipelines scope-aware, intégration globale centralisée.

---

## 2026-04-11 — constitution scope-aware et run-aware

- Mode : `human+ai`
- Le pipeline `constitution` a été rendu scope-aware puis run-aware.
- `AI_PROTOCOL.yaml` est devenu le point d'entrée IA autoritatif.
- Un premier scope `learner_state` et un premier run `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01` ont été matérialisés.
- `update_run_tracking.py` a été ajouté.

### Décisions prises

1. Le pipeline `constitution` reste unique ; il n'est pas dupliqué par scope.
2. Les runs consomment des scopes publiés et matérialisent leurs propres inputs.
3. Le startup IA doit être résolu à faible contexte avant lecture profonde.
4. Les anciens `RUN_*.md` ne sont plus les points d'entrée IA principaux.

---

## 2026-04-11 — extension du catalogue de scopes

- Mode : `human+ai`
- `knowledge_graph.yaml` a été ajouté.
- Un manifeste de catalogue V0.2 a été préparé dans `tmp/constitution_scope_catalog_manifest_v0_2.yaml`.

### Décisions prises

1. Partir de l'état réel du repo.
2. Sortir du mono-scope `learner_state`.
3. Garder comme priorités : nettoyage, publication effective des scopes, exécution réelle du run `learner_state`.

---

## 2026-04-12 — clarification scope extraction vs surface de lecture

- Mode : `human+ai`
- Clarification formalisée : les scopes `constitution` restent des dérivés gouvernés des Core canoniques.
- Snapshot ajouté dans le répertoire autoritatif de transformation.

### Décisions prises

1. `source_artifacts` doit être lu comme provenance canonique.
2. Le vrai gap restant est la réduction de la surface de lecture effective.
3. `tmp/` ne doit pas servir de suivi autoritatif de transformation.

### Artefact ajouté

- `docs/transformations/core_modularization/STATUS_2026_04_12_SCOPE_EXTRACTION_AND_READ_SURFACE.yaml`

---

## 2026-04-12 — J2 réduction de la surface de lecture effective

- Mode : `human+ai`
- J2 a été ajouté pour formaliser la prochaine marche de modularisation côté lecture.
- Snapshot J2 ajouté.

### Décisions prises

1. La prochaine marche n'est pas de modifier la provenance canonique des scopes.
2. La cible recommandée est un régime `ids-first` ou `projection-first`, avec fallback explicite sur les fichiers complets.
3. La réduction réelle du coût de contexte doit être portée par un contrat de lecture plus fin.

### Artefacts ajoutés

- `docs/transformations/core_modularization/J2_EFFECTIVE_READ_SURFACE_REDUCTION.md`
- `docs/transformations/core_modularization/STATUS_2026_04_12_J2_EFFECTIVE_READ_SURFACE_REDUCTION.yaml`

---

## 2026-04-12 — J3 reconstruction canonique bidirectionnelle

- Mode : `human+ai`
- J3 a été ajouté pour expliciter la mécanique retour de la modularisation.
- Un template `integrated_scoped_changeset` a été ajouté comme futur contrat d'entrée d'un reconstructeur canonique déterministe.
- Snapshot J3 ajouté.

### Décisions prises

1. Les résultats bruts de pipeline ne reconstruisent jamais directement les Core canoniques.
2. La reconstruction canonique doit consommer un artefact intégré, structuré et déterministe, après intégration globale explicite.
3. La modularisation cible devient explicitement bidirectionnelle : extraction du canon vers des unités de travail bornées, puis reconstruction du canon à partir de résultats intégrés et validés.
4. Les invariants de round-trip doivent être définis avant tout outillage de reconstruction plus ambitieux.

### Artefacts ajoutés

- `docs/transformations/core_modularization/J3_CANONICAL_RECONSTRUCTION_FROM_INTEGRATED_SCOPED_RESULTS.md`
- `docs/transformations/core_modularization/templates/integrated_scoped_changeset.template.yaml`
- `docs/transformations/core_modularization/STATUS_2026_04_12_J3_CANONICAL_RECONSTRUCTION.yaml`

---

## 2026-04-13 — J2 étape 3 : extract_scope_slice.py (ids-first effectif)

- Mode : `human+ai`
- Livraison de `extract_scope_slice.py` : réduction effective de la surface de lecture en mode `bounded_local_run`.
- Le script extrait des Core canoniques uniquement les entrées déclarées dans `scope_manifest.writable_perimeter.ids` → `scope_extract.yaml` et `impact_bundle.mandatory_reads.ids` → `neighbor_extract.yaml`.
- L'IA travaillant sur `STAGE_01_CHALLENGE` doit lire ces deux fichiers au lieu des Core complets.
- `pipeline.md` mis à jour : `extract_scope_slice.py` enregistré en `Spec and tools`, pré-condition ajoutée dans `STAGE_01_CHALLENGE`.

### Décisions prises

1. `ids-first` est le mode de lecture primaire en mode `bounded_local_run`.
2. `scope_extract.yaml` et `neighbor_extract.yaml` sont des vues dérivées, pas des secondes sources de vérité.
3. Le fallback sur les Core complets est explicite et tracé — uniquement si un ID est signalé manquant dans l'extrait.
4. L'IA ne doit jamais charger les Core complets silencieusement en mode borné.

### Artefacts ajoutés / mis à jour

- `docs/patcher/shared/extract_scope_slice.py` ← nouveau
- `docs/pipelines/constitution/pipeline.md` ← mis à jour (Spec and tools + pré-condition STAGE_01)
- `docs/transformations/core_modularization/STATUS_2026_04_13_J2_EXTRACT_SCOPE_SLICE.yaml` ← nouveau
- `docs/transformations/core_modularization/WORKLOG.md` ← cette entrée

### Prochaine action

- **J2 étape 4** : amender `docs/prompts/shared/Challenge_constitution.md` pour qu'en mode `bounded_local_run` l'IA lise en priorité `inputs/scope_extract.yaml` + `inputs/neighbor_extract.yaml` et ne consulte les Core complets que si un ID est signalé manquant.

---

## 2026-04-28 — archivage partiel des journaux J2/J3/J4

- Mode : `human+ai`
- Les journaux intermédiaires J2, J3 et J4 ont été déplacés vers `docs/transformations/core_modularization/archive/journals/`.
- Les fichiers conservés au premier niveau sont ceux encore actifs ou encore référencés par des artefacts pipeline :
  - `J1_SCOPED_RUN_CONTRACT.md`
  - `J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md`
  - `J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md`

### Décisions prises

1. Les journaux J2/J3/J4 sont conservés pour traçabilité, mais ne sont plus des documents actifs de pilotage.
2. Les décisions stabilisées de J2/J3/J4 sont désormais portées par les artefacts pipeline, les scripts déterministes, les specs et le scope catalog.
3. Les anciens liens dans le worklog restent historiques ; le nouvel emplacement autoritatif d'archive est `archive/journals/`.

### Artefacts déplacés

- `J2_EFFECTIVE_READ_SURFACE_REDUCTION.md`
- `J3_CANONICAL_RECONSTRUCTION_FROM_INTEGRATED_SCOPED_RESULTS.md`
- `J4_DERIVED_RUNTIME_TASK_VIEW_AND_STAGE_SKILLS.md`
- `J4_GENERATED_SCOPES_FROM_CANON_AND_POLICY.md`

---

## 2026-04-28 — réduction de la surface documentaire active

- Mode : `human+ai`
- Le répertoire `docs/transformations/core_modularization/` a été clarifié pour réduire la surface de reprise active.
- Les journaux J2, J3 et J4 ont été déplacés vers `docs/transformations/core_modularization/archive/journals/`.
- Le README principal a été remplacé par un index de reprise actuel distinguant documents actifs, documents de référence, analyses historiques et journaux archivés.

### Décisions prises

1. Les fichiers J2/J3/J4 sont conservés pour traçabilité mais ne sont plus des documents actifs de pilotage.
2. Les fichiers J1 restent visibles car ils sont encore liés au contrat de run borné.
3. Le fichier J5 reste visible tant que le chemin de consolidation multi-scopes n'a pas été validé par un vrai run multi-scopes.
4. `SCOPE_GRAPH_CLUSTERING_PROGRESS.md` reste le tracker principal de la transformation.
5. La prochaine phase macro reste `PHASE_18 — MACRO_005_NEIGHBOR_DECLARATION_REVIEW`.

### Artefacts concernés

Actifs au premier niveau :

- `README.md`
- `SCOPE_GRAPH_CLUSTERING_PROGRESS.md`
- `SCOPE_GRAPH_CLUSTERING_APPROACH.md`
- `REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md`
- `POST_PILOT_PATCH_LIFECYCLE_BACKLOG_TRIAGE.md`
- `J1_SCOPED_RUN_CONTRACT.md`
- `J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md`
- `J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md`

Archivés :

- `archive/journals/J2_EFFECTIVE_READ_SURFACE_REDUCTION.md`
- `archive/journals/J3_CANONICAL_RECONSTRUCTION_FROM_INTEGRATED_SCOPED_RESULTS.md`
- `archive/journals/J4_DERIVED_RUNTIME_TASK_VIEW_AND_STAGE_SKILLS.md`
- `archive/journals/J4_GENERATED_SCOPES_FROM_CANON_AND_POLICY.md`
---

## 2026-04-30 — passe globale et archivage post-PHASE_29

- Mode : `human+ai`
- Passe globale sur la transformation `core_modularization` après synchronisation de `PHASE_29`.
- Le tracker compact indique `NO_ACTIVE_PHASE`, aucun run actif, preflight `PREFLIGHT_KEEP_BACKLOG_OPEN`.
- Le README a été rafraîchi pour refléter l'état post-PHASE_29.
- Les snapshots top-level `STATUS_*`, s'il en restait, ont été archivés sous `archive/status_snapshots/`.

### Décisions prises

1. Garder le premier niveau du répertoire comme surface active compacte.
2. Conserver `POST_PILOT_PATCH_LIFECYCLE_BACKLOG_TRIAGE.md` tant que les entrées backlog associées restent ouvertes.
3. Conserver les fichiers J1/J5 encore référencés ou non validés par un vrai cas multi-scope.
4. Ne pas ouvrir de run automatiquement : tout challenge futur nécessite une décision humaine explicite via le flux canonique `OPEN_NEW_RUN`.

### Artefacts concernés

- `docs/transformations/core_modularization/README.md`
- `docs/transformations/core_modularization/WORKLOG.md`
- `docs/transformations/core_modularization/archive/status_snapshots/`

### Archivage effectué

- Aucun snapshot `STATUS_*` restant au premier niveau.
---

## 2026-04-30 — consolidation additionnelle du répertoire core_modularization

- Mode : `human+ai`
- Nouvelle réduction de la surface active du répertoire `docs/transformations/core_modularization/`.
- Les anciens documents J1 ont été archivés car leurs décisions sont maintenant portées par `pipeline.md`, les entry actions, les scripts déterministes et les stage skills.
- Le triage post-pilot `patch_lifecycle` a été archivé car ses décisions sont maintenant reflétées dans `governance_backlog.yaml`, STAGE_00, les rapports et les signaux pipeline.
- `J5_PARALLEL_SCOPED_RUNS_AND_CANONICAL_CONSOLIDATION.md` reste actif jusqu'à validation par un vrai cas multi-scope.
- `REFERENTIEL_LINK_EXTERNAL_READ_ONLY_TREATMENT.md` reste actif comme doctrine ouverte.

### Décisions prises

1. Réduire le premier niveau aux documents nécessaires à la reprise immédiate.
2. Archiver les notes de design absorbées par les contrats canoniques.
3. Garder `J5` actif tant que le mode consolidation parallèle n'a pas été éprouvé en conditions réelles.
4. Ne pas supprimer les historiques : déplacer vers `archive/`.

### Archivage effectué

- `moved docs\transformations\core_modularization\J1_SCOPED_RUN_CONTRACT.md -> docs\transformations\core_modularization\archive\journals\J1_SCOPED_RUN_CONTRACT.md ; reason=J1 scoped run contract absorbed by pipeline, entry actions, run inputs, and stage skills`
- `moved docs\transformations\core_modularization\J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md -> docs\transformations\core_modularization\archive\journals\J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md ; reason=J1 minimal Constitution delta absorbed by pipeline.md and STAGE skills`
- `moved docs\transformations\core_modularization\POST_PILOT_PATCH_LIFECYCLE_BACKLOG_TRIAGE.md -> docs\transformations\core_modularization\archive\analyses\POST_PILOT_PATCH_LIFECYCLE_BACKLOG_TRIAGE.md ; reason=post-pilot triage superseded by governance_backlog review metadata, Stage 00 reports, and pipeline signals`
---

## 2026-04-30 — PHASE_30 bundle déterministe STAGE_00

- Mode : `human+ai`
- Début de `PHASE_30_STAGE00_REVIEW_BUNDLE`.
- Objectif : intégrer un wrapper déterministe unique pour matérialiser les diagnostics STAGE_00 après closeout et avant revue sémantique.
- Le wrapper doit exécuter les validations/reports backlog, partition, scoring, neighbor governance et refresh des signaux.
- La phase ne doit pas modifier `policy.yaml`, `decisions.yaml`, `governance_backlog.yaml`, le scope catalog généré ou les cores courants.

### Artefacts prévus

- `docs/patcher/shared/run_constitution_stage00_review_bundle.py`
- `docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md`
- `docs/pipelines/constitution/stages/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.skill.yaml`
- `docs/pipelines/constitution/pipeline.md`
- `docs/pipelines/constitution/reports/stage00_review_bundle_report.yaml`
---

## 2026-04-30 — PHASE_31 revue STAGE_00 post-run

- Mode : `human+ai`
- Début de `PHASE_31_STAGE00_POST_RUN_REVIEW`.
- Source : le bundle STAGE_00 a passé (`PASS`) après la clôture de `CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01`, mais a révélé :
  - une bijection `FAIL` sur `REF_CORE_LEARNIT_REFERENTIEL_V6_0_IN_CONSTITUTION` ;
  - trois nouvelles entrées backlog ouvertes sans métadonnées de revue.
- Décision locale : aligner la décision de neighbor inter-core forcé vers `REF_CORE_LEARNIT_REFERENTIEL_V6_0_IN_CONSTITUTION`.
- Décision backlog : maintenir les trois nouvelles entrées `open` avec métadonnées de revue ; ne pas les résoudre automatiquement.
- Date de revue : `2026-04-30T09:56:22Z`.

### Commandes attendues après patch

```bash
python docs/patcher/shared/generate_constitution_scopes.py --apply --report tmp/constitution_scope_generation_report.yaml
python docs/patcher/shared/run_constitution_stage00_review_bundle.py
```
---

## 2026-04-30 — clôture PHASE_31

- Mode : `human+ai`
- `PHASE_31_STAGE00_POST_RUN_REVIEW` est clôturée.
- Le forced inter-core reference a été aligné sur `REF_CORE_LEARNIT_REFERENTIEL_V6_0_IN_CONSTITUTION`.
- Les trois entrées backlog exportées par `CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01` ont été revues et maintenues `open` avec métadonnées complètes.
- Le catalogue de scopes a été régénéré.
- Le bundle STAGE_00 repasse en `PASS`.
- La bijection repasse en `PASS` avec `ids_not_covered: []`.
- Les signaux reviennent à `KEEP_BACKLOG_OPEN_WITH_REVIEW_METADATA`.
- Le preflight revient à `PREFLIGHT_KEEP_BACKLOG_OPEN`.
- Aucun run n'est ouvert automatiquement.

### État final

```yaml
current_phase: NO_ACTIVE_PHASE
last_completed_phase: PHASE_31
recommended_next_action: keep_NO_ACTIVE_PHASE
```

