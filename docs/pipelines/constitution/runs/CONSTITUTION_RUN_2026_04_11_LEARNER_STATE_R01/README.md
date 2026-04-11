# Constitution run — learner_state R01

## Identité

- `run_id`: `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01`
- `scope_id`: `CONSTITUTION_SCOPE_LEARNER_STATE`
- mode : `bounded_local_run`

## Rôle

Ce répertoire matérialise la première instance de run du pipeline `constitution` à partir du nouveau modèle :
- scope catalogué ;
- run instancié ;
- inputs propres au run ;
- futur `work/` propre au run.

## Transition

À ce stade du chantier :
- les anciens fichiers plats dans `docs/pipelines/constitution/inputs/` existent encore ;
- mais ils doivent désormais être compris comme des artefacts de transition ;
- le layout cible est celui de ce répertoire `runs/<run_id>/...`.

## Prochaine action structurelle

La prochaine évolution logique sera :
- d'adapter le pipeline pour lire prioritairement les artefacts de run ;
- puis de déprécier le layout plat historique pour les runs bornés.
