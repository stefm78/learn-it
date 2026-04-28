# Constitution scope maturity scoring — spécification V0.2

## Objectif

Définir la chaîne déterministe de scoring de maturité post-scoping pour les scopes du pipeline `constitution`, puis la publication gouvernée des scores calculés dans `policy.yaml`.

Le scoring visé intervient **après** la régénération déterministe du catalogue de scopes. Il observe le catalogue effectivement généré, calcule un score déterministe par scope, puis compare ce score au score actuellement publié. En V0.2, ce score calculé devient le candidat d'autorité publiable : il n'est pas écrit directement par le scorer, mais peut être appliqué à `policy.yaml` par un patcher déterministe gated.

## Position d'autorité

En V0.2 :

- `score_constitution_scope_maturity.py` reste un script de calcul et de preuve : il produit un rapport déterministe et ne modifie jamais directement les fichiers canoniques ;
- le score calculé dans `scope_maturity_scoring_report.yaml` devient le **candidat d'autorité publiable** pour `maturity.axes`, `score_total` et `level` ;
- la publication dans `docs/pipelines/constitution/policies/scope_generation/policy.yaml` passe par un patcher séparé, explicite et gated : `docs/patcher/shared/apply_constitution_scope_maturity_scores.py` ;
- `policy.yaml` reste le fichier canonique publié, mais son contenu de maturité doit être synchronisable depuis le rapport calculé dès que les gates structurels sont satisfaits ;
- `docs/patcher/shared/generate_constitution_scopes.py` continue de propager la maturité publiée dans `policy.yaml` vers `scope_catalog/manifest.yaml` et `scope_definitions/*.yaml`.

Cette règle évite deux vérités concurrentes : le scorer calcule, le patcher publie, puis le catalogue est régénéré depuis la policy canonique.

## Scripts cibles

Calcul non-mutating :

```text
docs/patcher/shared/score_constitution_scope_maturity.py
```

Publication gouvernée des scores calculés :

```text
docs/patcher/shared/apply_constitution_scope_maturity_scores.py
```

Le patcher de publication doit :
- lire `scope_maturity_scoring_report.yaml` ;
- lire `policy.yaml` ;
- refuser toute écriture si le rapport contient des `blocking_findings` structurels ;
- publier les scores calculés par scope dans `policy.yaml` uniquement en mode `--apply` ;
- produire un rapport déterministe `docs/pipelines/constitution/reports/scope_maturity_policy_patch_report.yaml` ;
- ne jamais modifier `decisions.yaml`, le catalogue généré ou les cores.

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
5. mise à jour gouvernée de `policy.yaml` / `decisions.yaml` pour les décisions de partition ;
6. régénération déterministe du catalogue ;
7. scoring déterministe post-scoping ;
8. validation des gates de publication du score calculé ;
9. publication déterministe des scores calculés dans `policy.yaml` via `apply_constitution_scope_maturity_scores.py --apply` ;
10. régénération déterministe du catalogue ;
11. rerun du scoring pour vérifier convergence entre score publié et score calculé.

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
  authority: computed_score_candidate
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

## Non-objectifs V0.2

Le scorer ne doit pas :

- modifier `policy.yaml` ;
- modifier `decisions.yaml` ;
- modifier `manifest.yaml` ;
- modifier `scope_definitions/*.yaml` ;
- recalculer silencieusement le gating utilisé par le launcher.

Le patcher de publication des scores ne doit pas :

- recalculer les scores lui-même ;
- modifier `decisions.yaml` ;
- modifier le catalogue généré ;
- modifier les cores ;
- publier si le rapport de scoring contient des findings structurels bloquants ;
- remplacer l'arbitrage humain sur les règles de calcul du scorer.

## Trajectoire cible

Phase 1 : rapport déterministe non-mutating.

Phase 2 : rapport utilisé comme input obligatoire de STAGE_00.

Phase 3 : publication déterministe des scores calculés dans `policy.yaml` via un patcher séparé, gated et auditable.

Phase 4 : régénération du catalogue et rerun scoring pour vérifier convergence entre maturité publiée et maturité calculée.
