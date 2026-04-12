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

## 2026-04-11 — constitution scope-aware et premier run

- Mode : `human+ai`
- Le pipeline `constitution` a été rendu scope-aware.
- Les prompts principaux ont été rendus compatibles avec les modes `global` et `bounded`.
- Un premier scope `learner_state` a été catalogué.
- Un premier run `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01` a été matérialisé sous `docs/pipelines/constitution/runs/`.

### Décisions prises

1. Le pipeline `constitution` reste unique ; il n'est pas dupliqué par scope.
2. Les runs consomment des scopes publiés et matérialisent leurs propres inputs.
3. Le layout `runs/<run_id>/...` devient la cible pour les runs bornés ; le layout plat reste transitoire.

---

## 2026-04-11 — pipeline run-aware et tracking explicite

- Mode : `human+ai`
- `docs/pipelines/constitution/pipeline.md` a été consolidé en mode run-aware.
- `docs/pipelines/constitution/AI_PROTOCOL.yaml` est devenu le point d'entrée IA autoritatif.
- `docs/patcher/shared/update_run_tracking.py` a été ajouté pour suivre explicitement stage et run.
- Les répertoires `work/`, `reports/` et `outputs/` du premier run ont été matérialisés.

### Décisions prises

1. Le startup IA doit être résolu à faible contexte avant toute lecture profonde.
2. Le suivi du run doit être matérialisé explicitement via le script de tracking.
3. Les anciens RUN_*.md ne doivent plus être les points d'entrée IA principaux.

---

## 2026-04-11 — consolidation du protocole IA et launcher helper

- Mode : `human+ai`
- La logique de démarrage IA a été consolidée autour de `docs/pipelines/constitution/AI_PROTOCOL.yaml`.
- Un launcher helper a été prototypé dans `tmp/` puis convergé vers un candidat unique : `tmp/pipeline_launcher.py`.
- Le launcher produit maintenant :
  - un `decision_summary`
  - un `action_menu`
  - des `next_best_actions`
  - une commande de bootstrap tracking pour le chemin `continue`
  - un prompt de stage pour le run actif

### Décisions prises

1. Le launcher est un helper et non le chantier principal.
2. Il faut geler le launcher à un candidat unique et éviter la prolifération de versions.
3. La priorité doit revenir à la transformation réelle du repo.

---

## 2026-04-11 — extension du catalogue de scopes et recentrage

- Mode : `human+ai`
- Constat : `mastery_model.yaml` existait déjà dans le catalogue dans une forme plus aboutie que le brouillon bootstrap initial.
- `knowledge_graph.yaml` a été ajouté dans `docs/pipelines/constitution/scope_catalog/scope_definitions/`.
- Un manifeste de catalogue V0.2 a été préparé dans `tmp/constitution_scope_catalog_manifest_v0_2.yaml`.

### Décisions prises

1. Partir de l'état réel du repo, pas d'un brouillon moins riche.
2. Sortir du mono-scope `learner_state` pour permettre de vrais nouveaux runs sur d'autres scopes publiés.
3. Traiter maintenant comme priorités :
   - nettoyage,
   - publication effective des scopes,
   - exécution réelle du run `learner_state`.

### Prochaines actions utiles

1. Nettoyer les anciennes versions du launcher dans `tmp/`.
2. Nettoyer les anciens RUN_*.md dépréciés côté `constitution`.
3. Vérifier si le manifeste V0.2 du catalogue a bien été appliqué ; sinon l'appliquer.
4. Retester `tmp/pipeline_launcher.py` une fois plusieurs scopes publiés.
5. Reprendre réellement `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01` au `STAGE_01_CHALLENGE` puis enchaîner `STAGE_02_ARBITRAGE`.

---

## Point de vigilance transversal

Le vrai sujet restant n'est plus seulement la gouvernance des scopes, mais la réduction effective de la surface de lecture.

Aujourd'hui :
- `source_artifacts` comme provenance canonique complète reste acceptable ;
- mais `default_neighbors_to_read.files` pointant vers des fichiers Core complets garde encore un coût de contexte trop élevé.

Le prochain chantier d'architecture, à ne pas perdre de vue :
- passer d'une logique `files to read` à une logique plus fine :
  - `ids to read`
  - projections minimales
  - bundles d'extraits ciblés
