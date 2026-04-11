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

---

## 2026-04-11 — constitution scope-aware

- Mode : `human+ai`
- Le pipeline `constitution` a été rendu scope-aware.
- Les prompts `Challenge_constitution.md` et `Make04ConstitutionArbitrage.md` ont été rendus compatibles avec les modes `global` et `bounded`.
- Un premier pilote borné learner_state a été préparé.

### Décisions prises

1. Le pipeline `constitution` reste unique ; il n'est pas dupliqué par scope.
2. Les prompts restent génériques, mais acceptent désormais les artefacts de scope.
3. Le premier pilote borné porte sur `learner_state`.

---

## 2026-04-11 — scope catalog, maturity model, first run instance

- Mode : `human+ai`
- Le modèle `scope catalog + run instances` a été documenté.
- Le modèle de maturité des scopes a été ajouté.
- Le premier scope catalogué `CONSTITUTION_SCOPE_LEARNER_STATE` a été publié avec un score de maturité `17/24`, niveau `L3_operational`.
- Le premier run instancié `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01` a été matérialisé sous `docs/pipelines/constitution/runs/`.

### Décisions prises

1. Un `scope_definition` ne doit pas être improvisé à l'intérieur d'un challenge borné.
2. La définition officielle des scopes revient à la couche catalogue.
3. Les runs consomment des scopes publiés et matérialisent leurs propres inputs.
4. Les anciens fichiers plats dans `docs/pipelines/constitution/inputs/` deviennent des artefacts de transition pour les runs bornés.

---

## 2026-04-11 — pipeline run-aware préparé

- Mode : `human+ai`
- Ajout de `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`.
- Remplacement run-aware de `docs/pipelines/constitution/pipeline.md` préparé dans :
  - `tmp/constitution_pipeline_run_layout_v1_2/01_header_to_resolution.md`
  - `tmp/constitution_pipeline_run_layout_v1_2/02_stage03_to_stage06.md`
  - `tmp/constitution_pipeline_run_layout_v1_2/03_stage07_to_end.md`
- Notice d'application ajoutée :
  - `tmp/APPLY_constitution_pipeline_run_layout_v1_2.md`

### Décisions prises

1. Le `run_id` doit devenir l'unité primaire d'exécution des runs bornés du pipeline `constitution`.
2. Le layout `runs/<run_id>/...` devient la cible pour les runs bornés ; le layout plat reste supporté seulement comme transition.
3. Les chemins de stage, reports et outputs doivent se résoudre à partir du `run_id` quand il est fourni.

### Prochaine action utile

1. Appliquer localement le remplacement run-aware du pipeline `constitution`.
2. Poser les placeholders de `work/`, `reports/` et `outputs/` sous le premier run.
3. Exécuter le premier pilote learner_state directement sous `runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/`.
4. Synchroniser `STATUS.yaml` et `WORKLOG.md` avec les drafts préparés après application réelle.
