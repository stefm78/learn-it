### STAGE_10_CONSOLIDATE_PARALLEL_RUNS

Objectif :
- fusionner les sandboxes validées de N runs parallèles sur scopes disjoints en un
  ensemble Core consolidé unique sous `docs/cores/staging/` ;
- vérifier la disjonction des scopes avant toute écriture ;
- produire un rapport de consolidation exploitable ;
- préparer l'entrée de STAGE_07_RELEASE_MATERIALIZATION en mode multi-runs.

Ce stage est **optionnel** si un seul run a été exécuté : dans ce cas, `staging/`
peut être alimenté directement depuis le sandbox du run unique sans consolidation.

## Préconditions

- Tous les runs participants doivent être en statut `closed` avec STAGE_06_CORE_VALIDATION `PASS`
- L'`integration_gate` de chaque run participant doit être explicitement en `status: cleared`
  ou `status: not_applicable`
- Aucun run actif ne doit exister au moment de la consolidation
- Les scopes des runs participants doivent être disjoints (vérifié par le script)

## Inputs

- `runs/<run_id>/work/05_apply/sandbox/` pour chaque run participant
- `runs/<run_id>/inputs/scope_manifest.yaml` pour chaque run participant (vérification disjonction)
- `runs/<run_id>/inputs/integration_gate.yaml` pour chaque run participant (vérification clearance)
- `docs/cores/current/` comme référence de base pour les IDs non patchés

## Stratégie de fusion

- Partir de `docs/cores/current/` comme référence de base
- Pour chaque run, écraser uniquement les IDs déclarés dans son `scope_manifest`
- Les IDs non couverts par aucun scope restent identiques à `current/`
- En cas de chevauchement d'IDs entre deux scopes : **abort** avec rapport FAIL

## Commandes de référence

Dry-run (vérification sans écriture) :
```
python docs/patcher/shared/consolidate_parallel_runs.py \
  --runs RUN_A RUN_B RUN_C \
  --base docs/cores/current \
  --output docs/cores/staging \
  --pipeline constitution \
  --dry-run
```

Consolidation réelle :
```
python docs/patcher/shared/consolidate_parallel_runs.py \
  --runs RUN_A RUN_B RUN_C \
  --base docs/cores/current \
  --output docs/cores/staging \
  --pipeline constitution
```

## Outputs

- `docs/cores/staging/constitution.yaml`
- `docs/cores/staging/referentiel.yaml`
- `docs/cores/staging/link.yaml`
- `docs/cores/staging/consolidation_report.yaml`

## Règle opératoire

- L'exécution réelle de `consolidate_parallel_runs.py` est obligatoire avant de déclarer ce stage `done`
- Le dry-run est fortement recommandé avant l'exécution réelle
- Si `consolidation_report.yaml` retourne `status: FAIL` (chevauchement détecté),
  le pipeline s'arrête ici : les scopes doivent être corrigés avant nouvelle tentative
- Si `consolidation_report.yaml` retourne `status: PASS`, STAGE_07 peut démarrer
  en lisant `docs/cores/staging/` au lieu des sandboxes individuelles
- L'IA ne doit jamais simuler une consolidation ou supposer le contenu de `staging/`
  sans exécution effective du script
- Si l'IA ne peut pas exécuter le script elle-même, elle doit fournir les commandes
  exactes à l'utilisateur et garder ce stage non final jusqu'à retour du résultat réel

## Position dans le pipeline

- Après tous les STAGE_09_CLOSEOUT_AND_ARCHIVE des runs participants
- Avant STAGE_07_RELEASE_MATERIALIZATION
- STAGE_10 est sauté si un seul run a été exécuté (staging = sandbox directement)
