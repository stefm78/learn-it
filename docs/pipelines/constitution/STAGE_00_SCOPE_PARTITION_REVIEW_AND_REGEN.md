# STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN

## Objectif

Permettre, uniquement lorsqu'aucun run n'est actif, une révision optionnelle du partitionnement sémantique des scopes `constitution` avant ouverture de nouveaux runs.

Chaîne gouvernée attendue :
1. analyse déterministe obligatoire ;
2. analyse sémantique assistée par IA sur la base du rapport déterministe ;
3. arbitrage humain ;
4. mise à jour des fichiers de policy/decisions canonisés ;
5. régénération déterministe du catalogue de scopes.

## Précondition bloquante

Aucun run `constitution` ne doit être actif.

Source de vérité :
- `docs/pipelines/constitution/runs/index.yaml`

Règle :
- si `active_runs` n'est pas vide, le Stage 00 est bloqué ;
- aucune révision de partition ni régénération sémantique des scopes ne doit être engagée tant qu'un run actif existe ;
- la partition doit rester figée pendant la vie d'un run.

## Inputs

- `docs/pipelines/constitution/runs/index.yaml`
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
- `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`
- `docs/pipelines/constitution/scope_catalog/manifest.yaml`
- `docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml`

## Script déterministe obligatoire

Script canonique :
- `docs/patcher/shared/analyze_constitution_scope_partition.py`

Commande de référence :
- `python docs/patcher/shared/analyze_constitution_scope_partition.py --report ./docs/pipelines/constitution/reports/scope_partition_review_report.yaml`

Le script doit :
- vérifier l'absence de run actif ;
- bloquer explicitement sinon ;
- analyser le Core `constitution` courant ;
- produire des métriques stables sur le volume, les sections, les `logic.scope`, les couplages inter-groupes, la partition actuelle publiée et les candidats déterministes de regroupement/séparation ;
- produire un rapport structuré exploitable par arbitrage humain et IA.

## Analyse IA complémentaire

Prompt recommandé :
- `docs/prompts/shared/Make00ConstitutionScopePartitionReview.md`

Rôle de l'IA :
- analyser le rapport déterministe ;
- proposer des ajustements sémantiques de partition ;
- identifier les coupes dangereuses ou les regroupements nécessaires ;
- proposer des évolutions des fichiers de policy/decisions.

Interdictions :
- l'IA ne décide pas seule la nouvelle partition publiée ;
- l'IA ne remplace pas l'exécution du script déterministe ;
- l'IA ne modifie pas directement le catalogue comme source d'autorité.

## Sorties attendues

Sortie déterministe obligatoire :
- `docs/pipelines/constitution/reports/scope_partition_review_report.yaml`

Sorties analytiques optionnelles :
- `docs/pipelines/constitution/reports/scope_partition_review_notes.md`
- `tmp/constitution_scope_generation_policy_candidate.yaml`
- `tmp/constitution_scope_generation_decisions_candidate.yaml`

Après arbitrage humain et mise à jour des policy/decisions canonisés, la régénération déterministe repasse par :
- `docs/patcher/shared/generate_constitution_scopes.py`

## Règles opératoires

1. Le Stage 00 est optionnel.
2. Le Stage 00 est interdit s'il existe un run actif.
3. Le script déterministe est obligatoire et doit être réellement exécuté avant toute conclusion de stage.
4. L'analyse IA n'est qu'un complément d'interprétation sémantique.
5. Toute évolution gouvernante doit entrer par les fichiers canonisés de `docs/pipelines/constitution/policies/scope_generation/`.
6. Le catalogue reste un output généré.
7. Le Stage 00 ne doit jamais être utilisé pour contourner un run en cours ou requalifier rétroactivement son scope.

## Critère de succès

Le Stage 00 est réussi lorsque :
- aucun run actif n'existe ;
- le rapport déterministe a été produit ;
- l'analyse sémantique a été discutée ;
- les arbitrages humains nécessaires ont été capturés dans les fichiers canonisés ;
- le catalogue de scopes a été régénéré de façon déterministe ;
- le nouveau partitionnement est traçable et reproductible.
