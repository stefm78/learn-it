# HANDOVER PROMPT — constitution Stage 00 partition refresh

Tu reprends le chantier dans le repo `stefm78/learn-it`, branche `feat/core-modularization-bootstrap`.

## Règle de reprise
Commence par constater l'état réel du repo, puis travaille uniquement à partir de cet état réel. Ne rouvre pas de chantiers parallèles inutiles.

## État déjà acquis dans le repo

Le pipeline `constitution` connaît maintenant explicitement un mode optionnel `partition_refresh` et un `STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN`.

Artefacts déjà présents :
- `docs/pipelines/constitution/STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN.md`
- `docs/prompts/shared/Make00ConstitutionScopePartitionReview.md`
- `docs/patcher/shared/analyze_constitution_scope_partition.py`
- `docs/pipelines/constitution/pipeline.md`
- `docs/pipelines/constitution/AI_PROTOCOL.yaml`
- `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
- `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`
- `docs/pipelines/constitution/scope_catalog/manifest.yaml`

Le catalogue de scopes `constitution` est déjà sous régime généré.

Le run historique `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01` a été clôturé dans `docs/pipelines/constitution/runs/index.yaml`.

## Cible retenue

- Un seul niveau de scope.
- Pas de sous-scopes hiérarchiques.
- Le nombre de scopes doit pouvoir varier de façon déterministe selon l'état du canon.
- Les extractions modulaires doivent être générées en face des scopes.
- Les politiques durables sont canonisées dans `docs/pipelines/constitution/policies/`, pas dans `docs/transformations/`.
- L'analyse IA de partition reste consultative ; la publication reste déterministe après arbitrage humain et mise à jour des policy/decisions.

## Travail immédiat à faire

1. Vérifier l'état réel des fichiers suivants :
   - `docs/pipelines/constitution/runs/index.yaml`
   - `docs/pipelines/constitution/pipeline.md`
   - `docs/pipelines/constitution/AI_PROTOCOL.yaml`
   - `docs/patcher/shared/analyze_constitution_scope_partition.py`

2. Si aucun run actif n'existe, exécuter réellement :

```bash
python docs/patcher/shared/analyze_constitution_scope_partition.py \
  --report ./docs/pipelines/constitution/reports/scope_partition_review_report.yaml
```

3. Lire le rapport produit :
   - `docs/pipelines/constitution/reports/scope_partition_review_report.yaml`

4. Réaliser ensuite la revue sémantique à partir de :
   - `docs/prompts/shared/Make00ConstitutionScopePartitionReview.md`

5. En sortie, proposer uniquement des modifications des fichiers canonisés :
   - `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
   - `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`

6. Après arbitrage humain, régénérer le catalogue par voie déterministe avec :

```bash
python docs/patcher/shared/generate_constitution_scopes.py \
  --apply \
  --report tmp/constitution_scope_generation_report.yaml
```

## Garde-fous

- Ne pas lancer Stage 00 si un nouveau run actif existe.
- Ne pas introduire de sous-scopes.
- Ne pas modifier directement le `scope_catalog` comme source d'autorité.
- Ne pas déplacer les politiques gouvernantes dans `docs/transformations/`.
- Ne pas repartir vers l'intégration ou la reconstruction canonique tant que le partitionnement adaptatif n'est pas suffisamment stabilisé.

## Résultat attendu de la reprise

La reprise doit produire un diagnostic réel de partition, suivi d'une proposition gouvernée d'évolution du nombre de scopes, compatible avec la cible : un seul niveau de scope, nombre variable et déterministe, extractions modulaires alignées.
