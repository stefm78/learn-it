# STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN

## Objectif

Permettre, uniquement lorsqu'aucun run n'est actif, une révision optionnelle du partitionnement
sémantique des scopes `constitution` avant ouverture de nouveaux runs.

Chaîne gouvernée attendue :
1. lecture et synthèse du `governance_backlog.yaml` (angles morts inter-runs) ;
2. analyse déterministe obligatoire ;
3. analyse sémantique assistée par IA sur la base du rapport déterministe et du backlog ;
4. arbitrage humain ;
5. mise à jour des fichiers de policy/decisions canonisés pour les décisions de partition ;
6. régénération déterministe du catalogue de scopes ;
7. scoring déterministe post-scoping du catalogue généré ;
8. publication gouvernée des scores calculés dans `policy.yaml` via un patcher déterministe gated ;
9. régénération déterministe du catalogue de scopes après publication des scores ;
10. rerun du scoring pour vérifier la convergence score publié / score calculé ;
11. si le scoring expose des neighbor IDs Constitution sous-déclarés, génération
    déterministe d'un rapport de gouvernance neighbor IDs, préparation d'une surface
    d'arbitrage humain, validation de l'arbitrage, puis seulement après arbitrage
    complet : éventuelle mise à jour de `policy.yaml` / `decisions.yaml`, régénération
    du catalogue et rerun du scoring.

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
été explicitement revues. Une entrée peut soit passer à `addressed`, soit passer à `wont_fix`,
soit rester `open` avec justification de report. `deferred` / `reporté` n'est pas un statut
canonique : le report conserve `status: open` et ajoute les métadonnées de revue prévues.


## Mode `run_candidate_preflight` — cadrage pré-run

Le `STAGE_00_SCOPE_PARTITION_REVIEW_AND_REGEN` peut aussi être utilisé en mode
`run_candidate_preflight` avant une action `OPEN_NEW_RUN`.

Objectif :
- décider si des entrées ouvertes du `governance_backlog.yaml` justifient l'ouverture
  d'un nouveau `bounded_local_run` ;
- cadrer le thème, le scope cible, les entrées backlog incluses, les entrées exclues
  et les garde-fous avant toute ouverture de run ;
- éviter d'ouvrir un run trop large ou de mélanger des sujets de design hétérogènes.

Ce mode ne remplace pas `partition_refresh` :
- `partition_refresh` sert à revoir et éventuellement régénérer la partition de scopes ;
- `run_candidate_preflight` sert à décider si un run doit être ouvert à partir d'un signal
  backlog déjà identifié.

Déclenchement recommandé :
- lorsqu'une action `OPEN_NEW_RUN` est envisagée pour un scope impacté par des entrées
  `governance_backlog` encore `open` ;
- lorsqu'un humain souhaite transformer un backlog de design en run exécutable ;
- lorsqu'un launcher ou une entry action détecte un `governance_backlog_signal` sur le scope
  demandé.

Déclenchement non obligatoire :
- pour les runs purement locaux qui ne sont pas motivés par une entrée backlog ouverte ;
- pour une simple reprise de run déjà ouvert ;
- lorsqu'un humain décide explicitement de laisser les entrées backlog au cycle normal
  STAGE_00 sans ouvrir de run.

Entrées minimales :
- `docs/pipelines/constitution/runs/index.yaml`
- `docs/pipelines/constitution/scope_catalog/governance_backlog.yaml`
- `docs/pipelines/constitution/reports/governance_backlog_report.yaml`
- `docs/pipelines/constitution/reports/governance_backlog_lifecycle_validation.yaml`
- `docs/pipelines/constitution/scope_catalog/manifest.yaml`
- `docs/pipelines/constitution/policies/scope_generation/policy.yaml`
- `docs/pipelines/constitution/policies/scope_generation/decisions.yaml`

Sorties attendues :
- `docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml`
- `docs/pipelines/constitution/reports/bounded_run_preflight.md`

Décisions possibles :
- `open_new_bounded_run`
- `defer_to_stage00_backlog_review`
- `create_design_note_only`
- `keep_backlog_open`
- `wont_fix_or_address_backlog`

Le rapport de preflight doit au minimum préciser :
- le scope cible proposé ;
- les entrées backlog incluses ;
- les entrées backlog explicitement exclues ;
- les dépendances cross-scope ou cross-core à ne pas embarquer par erreur ;
- le thème de run proposé ;
- les gates à vérifier avant `OPEN_NEW_RUN` ;
- la recommandation finale : ouvrir, différer, documenter seulement, ou garder ouvert.

Politique de mutation :
- ce mode est non-mutating par défaut ;
- il ne modifie pas `policy.yaml`, `decisions.yaml`, le catalogue de scopes, les cores ou
  `governance_backlog.yaml` ;
- il ne peut pas ouvrir un run par lui-même ;
- l'ouverture réelle d'un run reste une décision d'entry action après validation humaine.

Exemple de décision prudente :

```yaml
run_candidate_preflight:
  status: PASS_RECOMMEND_DEFER_TO_NORMAL_STAGE00_REVIEW
  new_pipeline_run_recommended_now: false
  reason: >-
    Les entrées backlog restantes sont des follow-ups de design revus, pas des
    blockers de pipeline. Elles doivent rester visibles via STAGE_00 / launcher
    warnings jusqu'à décision humaine explicite.
```

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
- marquer chaque entrée open du backlog comme `addressed`, `wont_fix`, ou la laisser `open`
  avec justification de report et métadonnées de revue complètes.

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

## Script déterministe obligatoire — scoring post-scoping

Script canonique :
- `docs/patcher/shared/score_constitution_scope_maturity.py`

Commande de référence :
- `python docs/patcher/shared/score_constitution_scope_maturity.py --report docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml`

Le script doit être exécuté après `generate_constitution_scopes.py --apply`.

Le script doit :
- lire le catalogue de scopes généré ;
- lire les `scope_definitions/*.yaml` générées ;
- lire la policy et les décisions canonisées ;
- lire le rapport déterministe `scope_partition_review_report.yaml` ;
- calculer un scoring déterministe post-scoping par scope ;
- comparer ce scoring calculé au score publié dans `policy.yaml` ;
- produire un rapport structuré avec preuves, deltas et recommandations ;
- ne jamais modifier directement `policy.yaml`, `decisions.yaml`, `manifest.yaml` ou les `scope_definitions/*.yaml`.

Règle d'autorité :
- En V2, le score calculé devient le candidat d'autorité publiable.
- Le scorer reste non-mutating : il calcule et prouve, mais n'écrit pas `policy.yaml`.
- La publication du score calculé dans `policy.yaml` passe par un patcher déterministe séparé, gated et explicite.
- Après publication dans `policy.yaml`, le catalogue doit être régénéré et le scoring rejoué.

## Script déterministe conditionnel — publication des scores calculés

Script canonique cible :
- `docs/patcher/shared/apply_constitution_scope_maturity_scores.py`

Commande dry-run de référence :
- `python docs/patcher/shared/apply_constitution_scope_maturity_scores.py --report docs/pipelines/constitution/reports/scope_maturity_policy_patch_report.yaml`

Commande apply de référence :
- `python docs/patcher/shared/apply_constitution_scope_maturity_scores.py --apply --report docs/pipelines/constitution/reports/scope_maturity_policy_patch_report.yaml`

Le patcher doit :
- lire `docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml` ;
- lire `docs/pipelines/constitution/policies/scope_generation/policy.yaml` ;
- refuser toute écriture si le rapport de scoring contient des `blocking_findings` structurels ;
- copier les `axis_scores.*.score`, `computed_maturity.score_total` et `computed_maturity.level` vers la maturité publiée de chaque scope ;
- préserver ou enrichir la rationale publiée avec une trace de source calculée ;
- écrire uniquement `policy.yaml` en mode `--apply` ;
- produire `docs/pipelines/constitution/reports/scope_maturity_policy_patch_report.yaml`.

Après tout `--apply`, exécuter obligatoirement :
1. `generate_constitution_scopes.py --apply`
2. `score_constitution_scope_maturity.py`
3. validation que les scores publiés et calculés convergent, ou que tout écart restant est explicite et justifié.

## Gouvernance générique des neighbor IDs Constitution après scoring

Si `scope_maturity_scoring_report.yaml` révèle des dépendances Constitution-to-Constitution
non déclarées dans les neighbor IDs de scopes, le STAGE_00 DOIT traiter ce signal comme une
gouvernance générique, et non comme un cas particulier lié à un run pilote.

Scripts canoniques :

1. Rapport déterministe non-mutating :

```bash
python docs/patcher/shared/report_constitution_neighbor_ids_governance.py \
  --report docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml
```

2. Préparation de la surface d'arbitrage humain :

```bash
python docs/patcher/shared/prepare_constitution_neighbor_ids_arbitration.py
```

3. Validation de l'arbitrage :

```bash
python docs/patcher/shared/validate_constitution_neighbor_ids_arbitration.py \
  --report docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml
```

4. Patch déterministe gated de `decisions.yaml` après validation `PASS_READY_TO_PATCH` :

```bash
python docs/patcher/shared/apply_constitution_neighbor_ids_arbitration.py \
  --report docs/pipelines/constitution/reports/constitution_neighbor_ids_decisions_patch_report.yaml
```

Par défaut, ce script est en dry-run. Il produit `BLOCKED` tant que l'arbitrage n'est pas
`PASS_READY_TO_PATCH`. L'écriture réelle de `decisions.yaml` nécessite explicitement `--apply` :

```bash
python docs/patcher/shared/apply_constitution_neighbor_ids_arbitration.py \
  --apply \
  --report docs/pipelines/constitution/reports/constitution_neighbor_ids_decisions_patch_report.yaml
```

Sémantique de validation :

- `PENDING_HUMAN_ARBITRATION` : état valide intermédiaire ; aucun patch de policy/decisions
  ne doit être appliqué ;
- `PASS_READY_TO_PATCH` : tous les candidats sont arbitrés, les rationales sont présentes,
  et les flags `patch_policy_decisions_after_approval` sont cohérents ;
- `FAIL` : blocage structurel à corriger avant toute suite.

Règles :

- aucune mise à jour de `policy.yaml` ou `decisions.yaml` n'est autorisée tant que le rapport
  de validation n'est pas `PASS_READY_TO_PATCH` ;
- les scores publiés dans `policy.yaml` ne sont pas modifiés par cette séquence ;
- le scorer V1.1 n'est pas recalibré dans cette séquence ;
- le catalogue de scopes n'est régénéré que si l'arbitrage humain approuve une modification
  canonique de `policy.yaml` ou `decisions.yaml` ;
- après toute modification canonique acceptée, `generate_constitution_scopes.py --apply`
  puis `score_constitution_scope_maturity.py` doivent être rejoués.

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

Sortie déterministe obligatoire — scoring post-scoping :
- `docs/pipelines/constitution/reports/scope_maturity_scoring_report.yaml`
  (produit par `score_constitution_scope_maturity.py`)

Sortie déterministe conditionnelle — publication des scores calculés :
- `docs/pipelines/constitution/reports/scope_maturity_policy_patch_report.yaml`
  (produit par `apply_constitution_scope_maturity_scores.py`)

Sorties déterministes conditionnelles — cadrage pré-run :
- `docs/pipelines/constitution/reports/bounded_run_preflight_report.yaml`
- `docs/pipelines/constitution/reports/bounded_run_preflight.md`

Sorties déterministes conditionnelles — gouvernance neighbor IDs Constitution :
- `docs/pipelines/constitution/reports/constitution_neighbor_ids_governance_report.yaml`
- `docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.yaml`
- `docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration.md`
- `docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml`
- `docs/pipelines/constitution/reports/constitution_neighbor_ids_decisions_patch_report.yaml`

Mise à jour obligatoire en fin de STAGE_00 :
- `docs/pipelines/constitution/scope_catalog/governance_backlog.yaml`
  Chaque entrée `open` revue doit suivre l'un des chemins suivants :
  - passage en `addressed` avec `resolved_at`, `resolved_by`, `resolution_note` ;
  - passage en `wont_fix` avec `resolved_at`, `resolved_by`, `resolution_note` ;
  - maintien en `open` avec `last_reviewed_at`, `last_reviewed_by`, `review_note`,
    `next_review_trigger`.
  `deferred` / `reporté` ne doit jamais être utilisé comme statut.

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
    `open` doit être traitée ou explicitement revue avant que le STAGE_00 puisse être
    déclaré `done`. Une entrée reportée reste `open` avec métadonnées de revue ; `deferred`
    n'est pas un statut.

12. Le scoring post-scoping doit être exécuté après régénération du catalogue.
13. Le scorer ne modifie jamais directement la policy canonique.
14. Le score calculé doit être publié dans `policy.yaml` via `apply_constitution_scope_maturity_scores.py --apply` lorsque les gates structurels du rapport de scoring sont satisfaits.
15. Après publication des scores calculés, le catalogue doit être régénéré et le scoring rejoué.
16. Les neighbor IDs Constitution sous-déclarés révélés par le scoring doivent passer par
    `report_constitution_neighbor_ids_governance.py`, `prepare_constitution_neighbor_ids_arbitration.py`
    et `validate_constitution_neighbor_ids_arbitration.py` avant toute modification canonique.
17. Toute modification de `decisions.yaml` issue de cette gouvernance doit passer par
    `apply_constitution_neighbor_ids_arbitration.py --apply`, et seulement si le rapport
    de validation est `PASS_READY_TO_PATCH`.

18. Le mode `run_candidate_preflight` doit être utilisé avant `OPEN_NEW_RUN` lorsqu'un run
    est motivé par des entrées `governance_backlog` encore `open` sur le scope demandé.
19. Le mode `run_candidate_preflight` est non-mutating par défaut : il ne modifie pas
    `policy.yaml`, `decisions.yaml`, le catalogue, les cores ou `governance_backlog.yaml`.
20. Le mode `run_candidate_preflight` ne peut pas ouvrir un run par lui-même ; il produit
    seulement une recommandation gouvernée pour l'entry action.

## Critère de succès

Le Stage 00 est réussi lorsque :
- aucun run actif n'existe ;
- le rapport déterministe `scope_partition_review_report.yaml` a été produit par exécution
  réelle du script d'analyse ;
- le `governance_backlog.yaml` a été lu et toutes les entrées `open` ont été traitées
  (`addressed`), rejetées explicitement (`wont_fix`) ou maintenues `open` avec justification
  de report et métadonnées de revue complètes ;
- l'analyse sémantique a été discutée en intégrant les signaux du backlog ;
- les arbitrages humains nécessaires ont été capturés dans les fichiers canonisés ;
- le catalogue de scopes a été régénéré de façon déterministe par exécution réelle de
  `generate_constitution_scopes.py` ;
- le rapport `constitution_scope_generation_report.yaml` a été produit ;
- le rapport `scope_maturity_scoring_report.yaml` a été produit ;
- si les gates structurels du scoring sont satisfaits, les scores calculés ont été publiés
  dans `policy.yaml` via `apply_constitution_scope_maturity_scores.py --apply` ;
- après publication des scores, le catalogue a été régénéré et le scoring rejoué ;
- si le scoring expose des neighbor IDs Constitution sous-déclarés, le rapport de gouvernance
  neighbor IDs, la surface d'arbitrage, le rapport de validation et le rapport de patch gated
  ont été produits ;
- le nouveau partitionnement est traçable et reproductible.
