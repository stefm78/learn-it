### STAGE_06B_CONSOLIDATION

Objectif :
- fusionner les sandboxes validées de N runs parallèles sur scopes disjoints en un
  ensemble Core consolidé unique sous `docs/pipelines/constitution/work/consolidation/` ;
- vérifier la disjonction des scopes avant toute écriture ;
- produire un rapport de consolidation exploitable ;
- préparer l'entrée de STAGE_07_RELEASE_MATERIALIZATION en mode multi-runs.

Ce stage est **optionnel si un seul run a été exécuté** : dans ce cas,
`consolidate_parallel_runs.py` est tout de même exécuté avec `--runs <run_id>` unique
pour garantir le même chemin de validation (integration_gate, scope, rapport).
STAGE_07 lit alors `work/consolidation/` dans tous les cas.

## Position dans le pipeline

```
RUN_A / STAGE_06_CORE_VALIDATION PASS  ─┐
RUN_B / STAGE_06_CORE_VALIDATION PASS  ─┤  STAGE_06B  →  work/consolidation/  →  STAGE_07  →  releases/  →  STAGE_08  →  current/
RUN_C / STAGE_06_CORE_VALIDATION PASS  ─┘
```

- Après tous les STAGE_06_CORE_VALIDATION de tous les runs participants (tous `PASS`)
- Après tous les STAGE_09_CLOSEOUT_AND_ARCHIVE de tous les runs participants
- Avant STAGE_07_RELEASE_MATERIALIZATION

**Règle de déclenchement :**
STAGE_06B est exécuté une seule fois, après que **tous** les runs prévus ont terminé
leur STAGE_06_CORE_VALIDATION. Il n'est pas exécuté run par run — c'est un stage
de niveau pipeline, pas de niveau run.

## Préconditions

- Tous les runs participants doivent être en statut `closed` avec STAGE_06_CORE_VALIDATION `PASS`
- L'`integration_gate` de chaque run participant doit être explicitement en `status: cleared`
  ou `status: not_applicable` (voir ci-dessous)
- Aucun run actif ne doit exister au moment de la consolidation
- Les scopes des runs participants doivent être disjoints (vérifié par le script)

## Review de l'integration_gate

La clearance de l'`integration_gate` est un acte **explicite humain ou IA gouverné**,
non automatique. Elle s'effectue en deux temps :

1. **Pendant STAGE_09_CLOSEOUT_AND_ARCHIVE** (niveau run) :
   - Rejouer chaque check (`WP_01`…`FORBIDDEN_OPS_ENFORCEMENT`) sur le contenu du run
   - Marquer chaque check `cleared: true` dans `inputs/integration_gate.yaml`
   - Passer `status: cleared` une fois tous les checks validés

2. **Au début de STAGE_06B** (niveau pipeline, avant toute écriture) :
   - Le script vérifie programmatiquement que tous les runs ont `status: cleared`
   - Si un gate est encore `open` : **abort** (sauf `--dry-run` qui émet un warning)
   - Si tous sont `cleared` : la consolidation peut s'écrire

La gate bloque donc la promotion implicite d'un résultat local vers le Core partagé.

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
  --output docs/pipelines/constitution/work/consolidation \
  --pipeline constitution \
  --dry-run
```

Consolidation réelle :
```
python docs/patcher/shared/consolidate_parallel_runs.py \
  --runs RUN_A RUN_B RUN_C \
  --base docs/cores/current \
  --output docs/pipelines/constitution/work/consolidation \
  --pipeline constitution
```

Cas run unique :
```
python docs/patcher/shared/consolidate_parallel_runs.py \
  --runs RUN_A \
  --base docs/cores/current \
  --output docs/pipelines/constitution/work/consolidation \
  --pipeline constitution
```

## Outputs

- `docs/pipelines/constitution/work/consolidation/constitution.yaml`
- `docs/pipelines/constitution/work/consolidation/referentiel.yaml`
- `docs/pipelines/constitution/work/consolidation/link.yaml`
- `docs/pipelines/constitution/work/consolidation/consolidation_report.yaml`

## Règle opératoire

- L'exécution réelle de `consolidate_parallel_runs.py` est obligatoire avant de déclarer ce stage `done`
- Le dry-run est fortement recommandé avant l'exécution réelle
- Si `consolidation_report.yaml` retourne `status: FAIL` (chevauchement détecté),
  le pipeline s'arrête ici : les scopes doivent être corrigés avant nouvelle tentative
- Si `consolidation_report.yaml` retourne `status: PASS`, STAGE_07 peut démarrer
  en lisant `work/consolidation/` au lieu des sandboxes individuelles
- L'IA ne doit jamais simuler une consolidation ou supposer le contenu de `work/consolidation/`
  sans exécution effective du script
- Si l'IA ne peut pas exécuter le script elle-même, elle doit fournir les commandes
  exactes à l'utilisateur et garder ce stage non final jusqu'à retour du résultat réel
