# STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN

## Objectif

Permettre, uniquement lorsqu'aucun run n'est actif, une révision optionnelle du partitionnement
sémantique des scopes `constitution` avant ouverture de nouveaux runs.

Chaîne gouvernée attendue :
1. lecture et synthèse du `governance_backlog.yaml` (angles morts inter-runs) ;
2. analyse déterministe obligatoire ;
3. analyse sémantique assistée par IA sur la base du rapport déterministe et du backlog ;
4. arbitrage humain ;
5. mise à jour des fichiers de policy/decisions canonisés ;
6. régénération déterministe du catalogue de scopes.

## Précondition bloquante

Aucun run `constitution` ne doit être actif.

Source de vérité :
- `docs/pipelines/constitution/runs/index.yaml`

Règle :
- si `active_runs` n'est pas vide, le Stage 00 est bloqué ;
- aucune révision de partition ni régénération sémantique des scopes ne doit être engagée
  tant qu'un run actif existe ;
- la partition doit rester figée pendant la vie d'un run.

## Inputs

### Obligatoires
- `docs/pipelines/constitution/runs/index.yaml`
- `docs/pipelines/constitution/scope_catalog/governance_backlog.yaml`  ← **NOUVEAU — lu en premier**
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
- `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`
- `docs/pipelines/constitution/scope_catalog/manifest.yaml`
- `docs/pipelines/constitution/scope_catalog/scope_definitions/*.yaml`

## Script déterministe obligatoire — analyse

Script canonique :
- `docs/patcher/shared/analyze_constitution_scope_partition.py`

Commande de référence :
- `python docs/patcher/shared/analyze_constitution_scope_partition.py --report ./docs/pipelines/constitution/reports/scope_partition_review_report.yaml`

Le script doit :
- vérifier l'absence de run actif ;
- bloquer explicitement sinon ;
- analyser le Core `constitution` courant ;
- produire des métriques stables sur le volume, les sections, les `logic.scope`, les couplages
  inter-groupes, la partition actuelle publiée et les candidats déterministes de
  regroupement/séparation ;
- produire un rapport structuré exploitable par arbitrage humain et IA.

## Lecture du governance_backlog (obligatoire avant analyse sémantique)

Avant toute analyse sémantique de la partition, l'IA DOIT :
1. Lire `docs/pipelines/constitution/scope_catalog/governance_backlog.yaml` ;
2. Filtrer les entrées `status: open` ;
3. Produire une synthèse courte : entrées par type, scopes concernés, fréquence de signal ;
4. Intégrer cette synthèse comme signal prioritaire dans l'analyse de partition :
   - Les `scope_gap` et `scope_extension_needed` récurrents sur un même scope signalent
     un périmètre sous-dimensionné à élargir ou à scinder ;
   - Les `orphan_id` signalent des IDs à rattacher à un scope existant ou à un nouveau scope ;
   - Les `partition_angle_mort` signalent des zones sémantiques à couvrir par un nouveau scope.

Interdiction : l'IA ne peut pas déclarer le STAGE_00 terminé si des entrées `open` n'ont pas
été explicitement traitées (addressed) ou reportées avec justification (wont_fix ou report décidé).

## Format attendu en provenance des runs

Les runs qui identifient des ajustements de scope à rejouer plus tard doivent produire dans leur
rapport d'arbitrage une section `governance_backlog_candidates` sérialisée dans un bloc YAML
fencé, par exemple :

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_R4_SCOPE_REF_V3_ALIGNMENT
    backlog_entry_type: scope_extension_needed
    title: Aligner la référence inter-Core Constitution → Référentiel v3.0
    related_scope_keys:
      - deployment_governance
    originating_run_id: CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01
    source_finding_id: R4
    rationale: >-
      La référence inter-Core actuelle pointe vers un identifiant V2.0 alors que
      le Core référentiel courant est v3.0 ; la remise en cohérence dépasse le
      patch local du run et doit être rejouée lors d'une révision de partition.
    recommended_stage00_action: >-
      Réévaluer la policy/decisions de scope generation pour canoniser la bonne
      ancre inter-Core et régénérer le scope catalog si nécessaire.
    candidate_status: candidate_open
```

Le backlog canonique `governance_backlog.yaml` est alimenté en STAGE_09 par export depuis ce
bloc structuré. Le format legacy par notes `Cxx` peut rester accepté transitoirement, mais le
format YAML ci-dessus devient le format canonique à privilégier.

## Analyse IA complémentaire

Prompt recommandé :
- `docs/prompts/shared/Make00ConstitutionScopePartitionReview.md`

Rôle de l'IA :
- synthétiser le governance_backlog (entrées open) ;
- analyser le rapport déterministe ;
- proposer des ajustements sémantiques de partition intégrant les signaux du backlog ;
- identifier les coupes dangereuses ou les regroupements nécessaires ;
- proposer des évolutions des fichiers de policy/decisions ;
- marquer chaque entrée open du backlog comme `addressed` ou `wont_fix` avec justification.

Interdictions :
- l'IA ne décide pas seule la nouvelle partition publiée ;
- l'IA ne remplace pas l'exécution du script déterministe ;
- l'IA ne modifie pas directement le catalogue comme source d'autorité.

## Script déterministe obligatoire — régénération

Script canonique :
- `docs/patcher/shared/generate_constitution_scopes.py`

Commande de référence :
- `python docs/patcher/shared/generate_constitution_scopes.py --apply --report tmp/constitution_scope_generation_report.yaml`

Le script doit être exécuté après arbitrage humain et mise à jour des fichiers canonisés de
policy/decisions. Il produit le nouveau catalogue de scopes de façon déterministe.

## Sorties attendues

Sortie déterministe obligatoire — analyse :
- `docs/pipelines/constitution/reports/scope_partition_review_report.yaml`

Sorties analytiques optionnelles :
- `docs/pipelines/constitution/reports/scope_partition_review_notes.md`
- `tmp/constitution_scope_generation_policy_candidate.yaml`
- `tmp/constitution_scope_generation_decisions_candidate.yaml`

Sortie déterministe obligatoire — régénération :
- `tmp/constitution_scope_generation_report.yaml`
  (produit par `generate_constitution_scopes.py --apply`)

Mise à jour obligatoire en fin de STAGE_00 :
- `docs/pipelines/constitution/scope_catalog/governance_backlog.yaml`
  Chaque entrée `open` traitée doit passer en `addressed` ou `wont_fix` avec :
  - `resolved_at` : date ISO 8601
  - `resolved_by` : run_id ou 'STAGE_00_<date>'
  - `resolution_note` : justification courte

## Règles opératoires

1. Le Stage 00 est optionnel.
2. Le Stage 00 est interdit s'il existe un run actif.
3. Le script `analyze_constitution_scope_partition.py` est obligatoire et doit être réellement
   exécuté avant toute analyse sémantique ou conclusion de stage.
4. Le Stage 00 ne peut pas être déclaré `done` sans que `scope_partition_review_report.yaml`
   ait été produit par exécution réelle de `analyze_constitution_scope_partition.py`.
5. La régénération du catalogue ne peut pas être déclarée accomplie sans exécution réelle de
   `generate_constitution_scopes.py` ; aucune simulation ou substitution par lecture
   documentaire n'est autorisée.
6. Si l'IA ne peut pas exécuter ces scripts elle-même, elle doit fournir les commandes exactes
   à l'utilisateur et garder le stage non final jusqu'au retour du résultat réel.
7. L'analyse IA n'est qu'un complément d'interprétation sémantique ; elle ne remplace jamais
   l'exécution des scripts déterministes.
8. Toute évolution gouvernante doit entrer par les fichiers canonisés de
   `docs/pipelines/constitution/policies/scope_generation/`.
9. Le catalogue reste un output généré.
10. Le Stage 00 ne doit jamais être utilisé pour contourner un run en cours ou requalifier
    rétroactivement son scope.
11. Le `governance_backlog.yaml` DOIT être lu avant toute analyse sémantique. Chaque entrée
    `open` doit être traitée ou explicitement reportée avant que le STAGE_00 puisse être
    déclaré `done`.

## Critère de succès

Le Stage 00 est réussi lorsque :
- aucun run actif n'existe ;
- le rapport déterministe `scope_partition_review_report.yaml` a été produit par exécution
  réelle du script d'analyse ;
- le `governance_backlog.yaml` a été lu et toutes les entrées `open` ont été traitées
  (addressed) ou explicitement reportées (wont_fix / décision documentée) ;
- l'analyse sémantique a été discutée en intégrant les signaux du backlog ;
- les arbitrages humains nécessaires ont été capturés dans les fichiers canonisés ;
- le catalogue de scopes a été régénéré de façon déterministe par exécution réelle de
  `generate_constitution_scopes.py` ;
- le rapport `constitution_scope_generation_report.yaml` a été produit ;
- le nouveau partitionnement est traçable et reproductible.
