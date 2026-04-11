# Constitution — pipeline protocol integration notes

## Objet

Ce document liste les protocoles compagnons que `pipeline.md` doit considérer comme normatifs ou quasi-normatifs pendant la transition vers le modèle `runs/<run_id>/...`.

## Protocoles à référencer depuis `pipeline.md`

### Lancement et résolution
- `docs/pipelines/constitution/RUN_LAUNCH_PROTOCOL.md`
- `docs/pipelines/constitution/RUN_STARTUP_PROTOCOL.md`
- `docs/pipelines/constitution/RUN_LAYOUT_RESOLUTION.md`

### Clôture et tracking
- `docs/pipelines/constitution/RUN_STAGE_CLOSEOUT_PROTOCOL.md`
- `docs/patcher/shared/update_run_tracking.py`

## Règle opérationnelle recommandée

Pour un run borné `constitution` :
1. résoudre le point d'entrée via le startup protocol ;
2. exécuter le stage visé dans le layout du run ;
3. clôturer le stage via le closeout protocol ;
4. maintenir `runs/index.yaml` à jour ;
5. ne charger le contexte profond qu'après résolution du bon run.

## Décision de transition

Tant que `pipeline.md` n'intègre pas inline tout ce contenu :
- ces documents compagnons doivent être lus comme partie du contrat opératoire du pipeline.
