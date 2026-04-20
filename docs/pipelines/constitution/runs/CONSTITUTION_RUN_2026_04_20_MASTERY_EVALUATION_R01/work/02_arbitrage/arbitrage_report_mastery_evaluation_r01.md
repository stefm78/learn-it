# Arbitrage Report — STAGE_02_ARBITRAGE
Run ID: CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01
Scope: mastery_evaluation
Mode: bounded_local_run

## Executive summary

L’arbitrage confirme le diagnostic principal du challenge : le scope `mastery_evaluation` est localement cohérent sur sa logique métier centrale, et aucune correction locale n’est retenue à ce stade sur MSC, la séparation de T, la propagation à un saut, ni sur les règles SIS / NC_MSC.

Le seul écart matériel retenu concerne la cohérence inter-core et inter-artefacts autour des références au Référentiel. Ce point ne doit pas être corrigé silencieusement en STAGE_03 tant qu’une décision humaine n’a pas tranché entre deux voies raisonnables :
- correction locale limitée des références attendues dans le périmètre Constitution du scope ;
- révision plus large du scope catalog / impact bundle / logique de génération des voisins.

Par défaut conservateur, cet arbitrage bloque toute synthèse de patch sur ce point tant que l’origine exacte de l’incohérence n’est pas arbitrée humainement. En revanche, il rejette explicitement toute tentative de retoucher la logique métier locale du scope, qui apparaît saine.

## Scope analysed

Surface principale consommée :
- `inputs/run_context.yaml`
- `inputs/scope_manifest.yaml`
- `inputs/impact_bundle.yaml`
- `inputs/integration_gate.yaml`
- `work/01_challenge/challenge_report_mastery_evaluation_r01.md`

Lecture de support reprise depuis le challenge :
- `inputs/scope_extract.yaml`
- `inputs/neighbor_extract.yaml`
- fallback ciblé déclaré par le challenge sur le Référentiel courant

Périmètre de modification rappelé par le scope manifest :
- fichier modifiable localement : `docs/cores/current/constitution.yaml`
- aucune promotion directe ni modification silencieuse hors scope autorisées

## Detailed arbitrage by finding

### AF-01 — Inter-core reference mismatch between mastery_evaluation scope and referential neighbor bundle
- challenge_finding_id: F1
- challenge_scope_status: in_scope
- arbitrage_decision: reporter
- arbitrage_justification: >-
    L’écart est réel et prioritaire, mais la correction exacte reste ambiguë. Le challenge
    montre un décalage entre une attente de voisinage `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`
    et des références de scope orientées vers `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`,
    alors que le Référentiel courant observé n’est pas aligné simplement sur ce couple. Deux lectures
    restent raisonnables : (1) reliquat obsolète local dans les artefacts du scope, ou (2) problème
    plus large de génération / partitionnement / alignement inter-core. Trancher sans décision humaine
    risquerait de produire un patch faux mais plausible.
- patch_readiness: blocked_by_missing_human_decision
- related_gate_checks:
  - WP_03
- gate_effect: keeps_open
- conservative_default: >-
    Ne produire aucun patch sur ce point en STAGE_03 tant qu’un arbitrage humain n’a pas choisi
    explicitement entre correction locale de référence et révision de génération plus large.

### AF-02 — Local MSC logic remains strict and separated from transfer
- challenge_finding_id: F2
- challenge_scope_status: in_scope
- arbitrage_decision: rejeter
- arbitrage_justification: >-
    Le challenge ne révèle pas de défaut local sur la logique MSC ; au contraire, il confirme que
    `INV_MSC_AND_STRICT`, la séparation de T et la règle `non calculable -> deferred` sont cohérents
    et doivent être préservés. Toute tentative de correction ici serait une sur-réaction hors cible.
- patch_readiness: decision_only_no_patch_yet
- related_gate_checks:
  - WP_01
  - WP_02
  - WP_04
- gate_effect: helps_clear

### AF-03 — Graph propagation boundary appears preserved locally
- challenge_finding_id: F3
- challenge_scope_status: in_scope
- arbitrage_decision: rejeter
- arbitrage_justification: >-
    Le challenge ne montre pas de violation locale de la borne `one hop`. La frontière de propagation
    doit être maintenue telle quelle ; aucune correction n’est retenue.
- patch_readiness: decision_only_no_patch_yet
- related_gate_checks:
  - WP_05
- gate_effect: helps_clear

### AF-04 — Session integrity logic remains inside mastery_evaluation and should not drift to learner_state
- challenge_finding_id: F4
- challenge_scope_status: in_scope
- arbitrage_decision: rejeter
- arbitrage_justification: >-
    Le challenge confirme que SIS et NC_MSC restent correctement situés dans ce scope. Aucune correction
    ne doit les déplacer vers `learner_state`.
- patch_readiness: decision_only_no_patch_yet
- related_gate_checks:
  - WP_06
- gate_effect: helps_clear

### AF-05 — Potential scope-catalog / impact-bundle obsolescence for referential neighbors
- challenge_finding_id: F5
- challenge_scope_status: needs_scope_extension
- arbitrage_decision: necessite_extension_scope
- arbitrage_justification: >-
    Si l’origine du défaut se situe dans la génération du voisinage, les décisions de partition ou
    le catalogue de scopes, la correction dépasse le patch local du run. Ce point doit donc être
    tracé comme extension / révision de gouvernance potentielle, pas absorbé silencieusement dans
    un patch local.
- patch_readiness: blocked_by_scope_extension
- related_gate_checks:
  - WP_03
- gate_effect: keeps_open

### AF-06 — Run context stale after extract generation (challenge-time technical issue)
- challenge_finding_id: R2
- challenge_scope_status: in_scope
- arbitrage_decision: rejeter
- arbitrage_justification: >-
    Ce point était valable au moment du challenge, mais le run_context courant montre désormais que
    les extraits `scope_extract` et `neighbor_extract` sont présents. Le défaut est considéré comme
    techniquement résolu ; aucun patch de core n’est requis.
- patch_readiness: decision_only_no_patch_yet
- related_gate_checks: []
- gate_effect: no_effect

## Consolidated points

1. La logique métier locale du scope est jugée suffisamment saine pour ne pas justifier de patch local immédiat.
2. Le point critique est un défaut de cohérence inter-core / inter-artefacts, pas un défaut de logique MSC.
3. Le gate reste ouvert principalement à cause de la frontière Référentiel / voisinage / partitionnement.
4. La voie conservatrice consiste à bloquer STAGE_03 sur ce point tant que l’humain n’a pas arbitré l’origine exacte de la correction.

## Decisions for patch

Aucune décision n’est actuellement `ready_for_local_patch`.

Décision la plus proche d’un futur patch :
- AF-01 pourrait devenir patchable localement **uniquement** si l’humain confirme que l’écart est un reliquat
  local de référence dans le périmètre Constitution du scope, et non un problème de génération plus large.

État global patch synthesis:
- `blocked_by_missing_human_decision`

## Decisions not retained

Les corrections suivantes sont explicitement non retenues :
- modifier `INV_MSC_AND_STRICT`
- réintégrer T dans la maîtrise de base
- affaiblir `RULE_MSC_COMPONENT_NON_CALCULABLE_DEFERS_BASE_MASTERY`
- modifier `INV_GRAPH_PROPAGATION_ONE_HOP`
- déplacer SIS / NC_MSC vers `learner_state`
- produire un patch YAML ou réécrire les Core pendant STAGE_02

## Governance backlog candidates

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_ME_R01_REFERENTIAL_NEIGHBOR_ALIGNMENT
    backlog_entry_type: scope_extension_needed
    title: Aligner les références inter-Core et le voisinage référentiel du scope mastery_evaluation
    related_scope_keys:
      - mastery_evaluation
    originating_run_id: CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01
    source_finding_id: AF-05
    rationale: >-
      Le run révèle un écart entre la référence de voisinage attendue (`REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`)
      et les références réellement observées dans le scope et le Référentiel courant. La correction pourrait dépasser
      le patch local et nécessiter une révision du scope catalog, du partitionnement ou de la logique de génération
      des voisins.
    recommended_stage00_action: >-
      Réévaluer les policy/decisions de génération de scope et les ancres inter-Core canonisées pour déterminer
      si l’alignement doit être local au scope mastery_evaluation ou rejoué au niveau Stage 00 / génération du catalogue.
    candidate_status: candidate_open
```

## Deferred or blocked decisions

### BD-01 — Source exacte de la correction inter-core
- status: blocked
- reason: >-
    Ambiguïté matérielle non levée entre correction locale in-scope et révision de génération / partition plus large.
- effect_on_stage_03: >-
    STAGE_03_PATCH_SYNTHESIS ne doit pas démarrer sur ce finding sans arbitrage humain explicite.

## Ambiguities requiring human decision

### AD-01 — Comment traiter l’écart de référence référentielle ?

Options raisonnables :
1. **Option A — correction locale in_scope**
   - Considérer que `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` est un reliquat obsolète local.
   - Autoriser STAGE_03 à synthétiser un patch minimal dans le périmètre Constitution du scope.

2. **Option B — révision de gouvernance / génération**
   - Considérer que le défaut provient du scope catalog, des décisions de partition ou du générateur d’artefacts.
   - Interdire tout patch local sur ce point dans ce run et traiter le sujet via backlog / Stage 00.

Default conservateur retenu :
- **Option B** tant qu’aucune décision humaine contraire n’est fournie.

human_decision_required_flag: true

## Human actions to execute

1. **Relire et valider cet arbitrage**
   - Fichier cible :
     `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01/work/02_arbitrage/arbitrage_report_mastery_evaluation_r01.md`

2. **Arbitrer explicitement AD-01**
   - Décision attendue :
     - soit `Option A` (patch local autorisé sur la référence inter-core)
     - soit `Option B` (pas de patch local ; backlog / extension de scope)

3. **Si tu valides l’arbitrage sans ambiguïté restante pour STAGE_03**
   - exécuter :
     ```bash
     python docs/patcher/shared/update_run_tracking.py \
       --pipeline constitution \
       --run-id CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01 \
       --stage-id STAGE_02_ARBITRAGE \
       --stage-status done \
       --run-status active \
       --next-stage STAGE_03_PATCH_SYNTHESIS \
       --summary "Arbitrage report validated; decisions ready for patch synthesis."
     ```

4. **Si tu dois me faire réviser l’arbitrage avec une décision humaine**
   - relance avec :
     `Révise l'arbitrage du run CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01 — décision humaine sur ambiguïtés : <tes notes>.`
