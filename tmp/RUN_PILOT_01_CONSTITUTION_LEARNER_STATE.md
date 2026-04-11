# Run — Pilot 01 Constitution learner_state

## Inputs déjà posés dans le repo

- `docs/pipelines/constitution/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/inputs/integration_gate.yaml`
- `docs/transformations/core_modularization/PILOT_01_CONSTITUTION_LEARNER_STATE.md`

## Lecture minimale avant exécution

1. `docs/pipelines/constitution/pipeline.md`
2. `docs/prompts/shared/Challenge_constitution.md`
3. `docs/prompts/shared/Make04ConstitutionArbitrage.md`
4. `docs/transformations/core_modularization/PILOT_01_CONSTITUTION_LEARNER_STATE.md`
5. les trois inputs du pilote

## Exécution recommandée

### Stage 01
Lancer un challenge borné sur le scope `CONSTITUTION_BOUNDARY_PILOT_01_LEARNER_STATE`.

Livrable attendu :
- `docs/pipelines/constitution/work/01_challenge/challenge_report_<ID>.md`

Contraintes :
- mode `bounded`
- classification explicite des constats `in_scope` / `out_of_scope_but_relevant` / `needs_scope_extension`

### Stage 02
Arbitrer le ou les `challenge_report*.md` obtenus.

Livrable attendu :
- `docs/pipelines/constitution/work/02_arbitrage/arbitrage.md`

Contraintes :
- distinguer `hors_perimetre` et `necessite_extension_scope`
- ne pas forcer un patch si l'arbitrage conclut qu'un `no_patch` ou un `scope_extension_needed` est plus sûr

## Après le pilote

Mettre à jour le `integration_gate.yaml` selon l'un des cas :
- challenge utile mais pas de patch
- patch borné autorisé
- extension de scope nécessaire
- run borné insuffisant / à ajuster

Puis mettre à jour la traçabilité de transformation dans :
- `docs/transformations/core_modularization/STATUS.yaml`
- `docs/transformations/core_modularization/WORKLOG.md`
