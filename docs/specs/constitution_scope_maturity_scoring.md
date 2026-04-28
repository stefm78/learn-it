# Constitution scope maturity scoring — spécification V0.1

## Objectif

Définir le futur script déterministe de scoring de maturité post-scoping pour les scopes du pipeline `constitution`.

Le scoring visé intervient **après** la régénération déterministe du catalogue de scopes. Il observe le catalogue effectivement généré, calcule un score déterministe par scope, puis compare ce score au score gouverné actuellement publié.

## Position d'autorité

En V0.1 :

- `docs/pipelines/constitution/policies/scope_generation/policy.yaml` reste la source d'autorité pour `maturity.axes`, `score_total`, `level` et `rationale` ;
- `docs/patcher/shared/generate_constitution_scopes.py` continue de propager cette maturité gouvernée vers `scope_catalog/manifest.yaml` et `scope_definitions/*.yaml` ;
- le futur script `score_constitution_scope_maturity.py` produit un **rapport déterministe non publiant** ;
- le rapport peut signaler un écart ou recommander un arbitrage, mais il ne modifie jamais directement la policy canonique.

Cette règle évite deux vérités concurrentes : le score publié reste gouverné, le score calculé devient une preuve déterministe d'audit.

## Script cible

Emplacement canonique :

```text
docs/patcher/shared/score_constitution_scope_maturity.py
```

## Place dans STAGE_00

Le script doit être exécuté après :

```text
docs/patcher/shared/generate_constitution_scopes.py --apply
```

Chaîne cible :

1. lecture du `governance_backlog.yaml` ;
2. analyse déterministe de partition ;
3. analyse sémantique IA ;
4. arbitrage humain ;
5. mise à jour gouvernée de `policy.yaml` / `decisions.yaml` ;
6. régénération déterministe du catalogue ;
7. scoring déterministe post-scoping ;
8. arbitrage ou report explicite des écarts éventuels.

## Inputs

Inputs obligatoires :

- `docs/pipelines/constitution/runs/index.yaml`
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
- `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`
- `docs/pipelines/constitution/scope_catalog/manifest.yaml`
- `docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml`
- `docs/pipelines/constitution/reports/scope_partition_review_report.yaml`
- `tmp/constitution_scope_generation_report.yaml`

Input optionnel mais recommandé :

- `docs/pipelines/constitution/scope_catalog/governance_backlog.yaml`

## Output

Output canonique :

```text
docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml
```

Le rapport doit contenir au minimum :

```yaml
scope_maturity_scoring_report:
  schema_version: 0.1
  pipeline_id: constitution
  status: PASS | WARN | FAIL
  authority: diagnostic_report_only
  does_not_update_policy: true
  scoring_model:
    ref: docs/transformations/core_modularization/CONSTITUTION_SCOPE_MATURITY_MODEL.md
    max_score: 24
  scope_results:
    - scope_key: example_scope
      published_maturity:
        source: policy.yaml
        score_total: 0
        level: L0_experimental
      computed_maturity:
        score_total: 0
        level: L0_experimental
      axis_scores: {}
      delta:
        score_delta: 0
        level_delta: none
        action_required: false
```

## Axes de scoring

Le modèle reprend le référentiel existant : 6 axes sur 4 points chacun, soit 24 points.

Axes :

1. `clarity_of_scope`
2. `internal_coherence`
3. `inter_scope_boundaries`
4. `dependency_explicitness`
5. `bounded_run_executability`
6. `inter_release_stability`

## Principes de calcul V0.1

Le scoring doit rester explicable. Chaque note doit être accompagnée d'une preuve déterministe ou d'un signal explicitement marqué comme limité.

Exemples de signaux acceptables :

- présence ou absence de `target.files`, `target.modules`, `target.ids` ;
- cohérence entre `policy.yaml`, `manifest.yaml` et `scope_definitions/*.yaml` ;
- résultats de `bijection_check` dans le rapport de partition ;
- densité et direction des `cross_scope_edges` ;
- volume d'IDs cible ;
- volume de voisins obligatoires ;
- nombre et nature des watchpoints ;
- entrées ouvertes du `governance_backlog.yaml` liées au scope ;
- historique disponible dans les releases, si exploitable.

Si un axe ne peut pas être évalué avec une preuve suffisante, le rapport doit l'indiquer explicitement au lieu de masquer l'incertitude.

## Règles de statut

`PASS` :

- tous les scopes sont scorés ;
- aucune incohérence structurelle bloquante ;
- aucun delta critique entre maturité calculée et maturité publiée.

`WARN` :

- delta non bloquant ;
- preuve limitée sur un axe ;
- backlog ouvert non bloquant ;
- score calculé différent mais niveau inchangé.

`FAIL` :

- scope publié sans `scope_definition` générée ;
- mismatch bloquant policy/catalogue/definition ;
- bijection en échec ;
- niveau calculé inférieur au niveau publié sans arbitrage explicite ;
- preuve déterministe manquante sur un axe critique.

## Non-objectifs V0.1

Le script ne doit pas :

- modifier `policy.yaml` ;
- modifier `decisions.yaml` ;
- modifier `manifest.yaml` ;
- modifier `scope_definitions/*.yaml` ;
- recalculer silencieusement le gating utilisé par le launcher ;
- remplacer l'arbitrage humain.

## Trajectoire cible

Phase 1 : rapport déterministe non publiant.

Phase 2 : rapport utilisé comme input obligatoire d'arbitrage STAGE_00.

Phase 3 : publication gouvernée d'un score accepté, avec trace explicite de l'écart éventuel entre score calculé et score validé.
