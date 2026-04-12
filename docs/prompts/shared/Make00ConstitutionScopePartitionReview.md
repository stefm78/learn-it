# Make00 — Constitution Scope Partition Review

Analyse le rapport déterministe de partition `constitution` et propose, sans publier directement de nouveau catalogue, des ajustements sémantiques gouvernés.

## Inputs attendus
- `docs/pipelines/constitution/reports/scope_partition_review_report.yaml`
- `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
- `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`
- `docs/pipelines/constitution/scope_catalog/manifest.yaml`
- éventuellement les `scope_definitions/*.yaml` générés

## Mission
1. Lire le rapport déterministe.
2. Identifier les regroupements sémantiquement cohérents.
3. Identifier les coupes dangereuses ou artificielles.
4. Identifier si le nombre actuel de scopes paraît trop faible, trop élevé, ou adéquat.
5. Proposer uniquement des évolutions à inscrire dans les fichiers canonisés de policy/decisions.

## Contraintes
- Ne pas proposer de sous-scopes hiérarchiques.
- Rester sur un seul niveau de scope.
- Respecter l'idée d'un nombre de scopes variable mais déterministe selon la taille et la cohésion du canon.
- Ne jamais traiter le catalogue actuel comme source d'autorité supérieure à la policy.
- Ne jamais publier directement un nouveau `scope_catalog/manifest.yaml` comme résultat de cette analyse.

## Sortie attendue
Un avis structuré contenant :
- `partition_assessment`
- `recommended_scope_count_direction` (`keep`, `increase`, `decrease`)
- `semantic_grouping_notes`
- `required_human_arbitrations`
- `policy_changes_to_make`
- `decision_changes_to_make`

## Règle
Le résultat de cette analyse est une aide d'arbitrage. La publication reste déterministe et passe ensuite par les fichiers canonisés de policy/decisions puis par `generate_constitution_scopes.py`.
