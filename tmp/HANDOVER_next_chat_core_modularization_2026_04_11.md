# Handover — next chat

## Repo / branche

- Repo: `learn-it`
- Branche: `feat/core-modularization-bootstrap`

## Point d'arrêt

Le travail a porté sur deux axes :
1. la transformation `constitution` vers un modèle **scope catalog + run instances** ;
2. un **launcher léger** pour décider `continue / new run` avec très peu de contexte avant d'appeler une IA.

Le launcher est maintenant **suffisamment bon pour être gelé temporairement**.
La priorité doit revenir à la transformation réelle du repo.

---

## Décision importante

Le point d'entrée IA pour `constitution` doit désormais être :
- `docs/pipelines/constitution/AI_PROTOCOL.yaml`

`pipeline.md` pointe déjà vers ce fichier avec une note explicite.

Les anciens `RUN_*.md` doivent être considérés comme dépréciés et nettoyés.

---

## État réel connu à la fin du chat

### Pipeline constitution
- `docs/pipelines/constitution/pipeline.md` existe en version run-aware.
- `docs/pipelines/constitution/AI_PROTOCOL.yaml` est le point d'entrée IA autoritatif.

### Run actif
- Un run actif existe déjà :
  - `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01`
- Scope :
  - `learner_state`
- Stage courant :
  - `STAGE_01_CHALLENGE`
- Suivi :
  - `docs/pipelines/constitution/runs/index.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/run_manifest.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/reports/stage_completion_STAGE_01_CHALLENGE.yaml`

### Catalogue de scopes
Attention :
- `learner_state` est publié dans le manifeste actuellement lu par le repo.
- `mastery_model.yaml` existe déjà dans `scope_definitions/`.
- `knowledge_graph.yaml` a été ajouté dans `scope_definitions/`.
- un manifeste étendu V0.2 a été préparé dans `tmp/`, mais il faut **vérifier s'il a été appliqué**.

Fichiers concernés :
- `docs/pipelines/constitution/scope_catalog/manifest.yaml`
- `docs/pipelines/constitution/scope_catalog/scope_definitions/learner_state.yaml`
- `docs/pipelines/constitution/scope_catalog/scope_definitions/mastery_model.yaml`
- `docs/pipelines/constitution/scope_catalog/scope_definitions/knowledge_graph.yaml`
- `tmp/constitution_scope_catalog_manifest_v0_2.yaml`
- `tmp/APPLY_constitution_scope_catalog_v0_2.md`

### Launcher
Le launcher candidat unique est désormais :
- `tmp/pipeline_launcher.py`

Il remplace les anciennes versions `pipeline_launcher_bootstrap*.py`.

Il produit :
- un `decision_summary`
- un `action_menu`
- des `next_best_actions`

Commande de test :
```bash
python ./tmp/pipeline_launcher.py --repo-root . --pipeline constitution --branch feat/core-modularization-bootstrap
```

---

## Commandes utiles déjà préparées

### 1. Nettoyage des anciennes versions du launcher
```bash
rm -f \
  ./tmp/pipeline_launcher_bootstrap.py \
  ./tmp/pipeline_launcher_bootstrap_v2.py \
  ./tmp/pipeline_launcher_bootstrap_v3.py \
  ./tmp/pipeline_launcher_bootstrap_v4.py \
  ./tmp/pipeline_launcher_bootstrap_v5.py \
  ./tmp/pipeline_launcher_bootstrap_v6.py
```

### 2. Appliquer le manifeste de catalogue V0.2 si pas encore fait
```bash
cp ./tmp/constitution_scope_catalog_manifest_v0_2.yaml ./docs/pipelines/constitution/scope_catalog/manifest.yaml
```

### 3. Vérifier le diff du catalogue
```bash
git diff -- \
  ./docs/pipelines/constitution/scope_catalog/manifest.yaml \
  ./docs/pipelines/constitution/scope_catalog/scope_definitions/mastery_model.yaml \
  ./docs/pipelines/constitution/scope_catalog/scope_definitions/knowledge_graph.yaml
```

### 4. Bootstrap tracking pour reprendre le run actif
```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 \
  --stage-id STAGE_01_CHALLENGE \
  --stage-status in_progress \
  --run-status active \
  --next-stage STAGE_01_CHALLENGE \
  --scope-status confirmed_for_bounded_run \
  --summary "Entry decision resolved; resuming existing learner_state run at Stage 01"
```

### 5. Prompt de stage pour reprendre le run actif
```text
Dans le repo learn-it, sur la branche feat/core-modularization-bootstrap, exécute le pipeline docs/pipelines/constitution/pipeline.md au STAGE_01_CHALLENGE en mode run-aware pour run_id=CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01. Lis d'abord docs/pipelines/constitution/AI_PROTOCOL.yaml, puis le run_manifest.yaml et les inputs du run, et produis le livrable du stage uniquement sous docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/... À la fin, donne-moi la commande update_run_tracking.py de clôture du stage à exécuter.
```

---

## Priorités recommandées pour le prochain chat

### Priorité 1 — nettoyage
Faire le ménage avant de repartir dans tous les sens :
- nettoyer les anciennes versions du launcher dans `tmp/`
- nettoyer les anciens `RUN_*.md` dépréciés côté `constitution` s'ils n'ont pas encore été supprimés
- vérifier que `pipeline.md` ne dépend plus de ces anciens docs

### Priorité 2 — publier réellement plusieurs scopes
Vérifier si `manifest.yaml` du catalogue a bien été remplacé par la V0.2.
Si non, l'appliquer.
But :
- avoir réellement plusieurs scopes publiés (`learner_state`, `mastery_model`, `knowledge_graph`)
- permettre au launcher de proposer un vrai `new_run`

### Priorité 3 — avancer sur la transformation réelle
Le plus important maintenant :
- reprendre le run actif `learner_state`
- exécuter réellement `STAGE_01_CHALLENGE`
- puis `STAGE_02_ARBITRAGE`
- utiliser `update_run_tracking.py` à chaque étape

### Priorité 4 — seulement ensuite
- adapter le même modèle à `platform_factory`
- promouvoir plus tard le launcher hors de `tmp/`

---

## Point de vigilance majeur

Le vrai problème identifié dans ce chat :
- on a bien réduit la **gouvernance** via les scopes,
- mais on n'a pas encore assez réduit la **surface réelle de lecture**.

Autrement dit :
- `source_artifacts` comme provenance complète est acceptable ;
- mais `default_neighbors_to_read.files` pointant vers des fichiers Core complets garde encore un coût de contexte trop élevé.

Le prochain chantier de fond à ne pas perdre de vue :
- passer d'une logique `files to read` à une logique plus fine :
  - `ids to read`
  - projections minimales
  - ou bundles d'extraits ciblés

---

## Règle de travail recommandée pour le prochain chat

Ne pas réouvrir un chantier parallèle inutile.
Ordre recommandé :
1. constater l'état réel du repo ;
2. nettoyer ;
3. publier les scopes si nécessaire ;
4. exécuter réellement le run `learner_state` ;
5. seulement ensuite reprendre les raffinements d'architecture.
