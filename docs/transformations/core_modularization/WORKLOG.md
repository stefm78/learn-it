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

### Prochaines actions utiles

1. Synchroniser les fichiers centraux `STATUS.yaml` et `WORKLOG.md`.
2. Prototyper sur `learner_state` un premier scope distinguant provenance, cible gouvernée, lecture primaire par IDs et fallback fichiers.
3. Faire évoluer le `impact_bundle` d'un run pilote vers un plan de lecture minimal ids-first.
4. Instancier un premier `integrated_scoped_changeset` sur un cas `constitution` borné.
5. Préparer ensuite un squelette de script déterministe pour le calcul des scopes et/ou la reconstruction canonique.
