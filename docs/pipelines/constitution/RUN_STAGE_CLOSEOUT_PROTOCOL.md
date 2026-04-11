# Constitution — run stage closeout protocol

## Objet

Ce document définit le mécanisme simple qu'une IA doit demander d'exécuter **à la fin d'un stage** pour mettre à jour l'état du run, du stage courant et du scope suivi.

But :
- éviter les mises à jour manuelles dispersées ;
- garder un index léger à jour ;
- conserver une trace stage par stage ;
- permettre à une autre IA de reprendre sans relire tout le run.

---

## Principe

À la fin de chaque stage, l'IA ne doit pas seulement produire les artefacts métier.
Elle doit aussi demander l'exécution d'une commande déterministe qui :
- met à jour le `run_manifest.yaml` ;
- met à jour `docs/pipelines/constitution/runs/index.yaml` ;
- écrit une trace de clôture de stage dans le run.

---

## Script de référence

- `docs/patcher/shared/update_run_tracking.py`

---

## Effets attendus du script

Le script doit :
1. résoudre le run ciblé ;
2. mettre à jour le stage courant et le statut du run ;
3. enregistrer le statut du stage ;
4. mettre à jour le `scope_status` si fourni ;
5. mettre à jour `runs/index.yaml` ;
6. écrire un enregistrement de clôture dans `runs/<run_id>/reports/`.

---

## Commande générique

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id <RUN_ID> \
  --stage-id <STAGE_ID> \
  --stage-status <STATUS> \
  --run-status <RUN_STATUS> \
  --next-stage <NEXT_STAGE_ID> \
  --scope-status <SCOPE_STATUS> \
  --summary "<SHORT_SUMMARY>"
```

---

## Exemples

### Fin de STAGE_01_CHALLENGE réussie

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 \
  --stage-id STAGE_01_CHALLENGE \
  --stage-status done \
  --run-status active \
  --next-stage STAGE_02_ARBITRAGE \
  --scope-status confirmed_for_bounded_run \
  --summary "Challenge borné produit pour learner_state"
```

### Fin de STAGE_02_ARBITRAGE avec besoin d'extension de scope

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 \
  --stage-id STAGE_02_ARBITRAGE \
  --stage-status done \
  --run-status blocked \
  --next-stage STAGE_03_PATCH_SYNTHESIS \
  --scope-status needs_scope_extension \
  --summary "Arbitrage terminé, extension de scope recommandée avant patch"
```

### Fin de STAGE_09_CLOSEOUT_AND_ARCHIVE

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 \
  --stage-id STAGE_09_CLOSEOUT_AND_ARCHIVE \
  --stage-status done \
  --run-status closed \
  --scope-status stable \
  --summary "Run clôturé et archivé" \
  --close-run
```

---

## Valeurs recommandées

### `stage-status`
- `done`
- `in_progress`
- `blocked`
- `failed`
- `skipped`

### `run-status`
- `bootstrap_open`
- `active`
- `blocked`
- `failed`
- `closed`

### `scope-status`
- `draft`
- `confirmed_for_bounded_run`
- `needs_scope_extension`
- `needs_scope_adjustment`
- `stable`

---

## Décision de design

Pour `constitution`, la clôture d'un stage n'est considérée comme propre que si :
- les artefacts métier du stage existent ;
- et le suivi du run a été mis à jour par le script de tracking.
