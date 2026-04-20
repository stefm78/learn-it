# Arbitrage Report — STAGE_02_ARBITRAGE
Run ID: CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01
Scope: mastery_evaluation
Mode: bounded_local_run

## Executive summary

L’arbitrage confirme le diagnostic principal du challenge : le scope `mastery_evaluation` est localement cohérent sur sa logique métier centrale, et aucune correction locale n’est retenue à ce stade sur MSC, la séparation de T, la propagation à un saut, ni sur les règles SIS / NC_MSC.

Le seul écart matériel retenu concerne la cohérence inter-core et inter-artefacts autour des références au Référentiel. La décision humaine a désormais tranché : **Option B**. Le défaut n’est donc pas traité comme un simple reliquat local patchable dans ce run, mais comme un sujet de gouvernance / génération / partitionnement à remonter via backlog.

En conséquence :
- aucun patch local ne doit être synthétisé en STAGE_03 sur ce point ;
- l’écart est conservé comme candidat backlog de gouvernance ;
- les décisions de STAGE_02 sont désormais closes et ne nécessitent plus d’arbitrage humain complémentaire sur ce finding.

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
    L’écart est réel et prioritaire. La décision humaine a retenu l’Option B : le sujet doit être traité
    comme un problème plus large de gouvernance / génération / partitionnement, et non comme une correction
    locale à synthétiser dans ce run. Il serait donc incorrect de produire un patch local sur la seule base
    du mismatch observé.
- patch_readiness: blocked_by_scope_extension
- related_gate_checks:
  - WP_03
- gate_effect: keeps_open
- human_decision_applied: Option B

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
    La décision humaine Option B confirme que l’origine probable du défaut se situe dans la génération du
    voisinage, les décisions de partition ou le catalogue de scopes. Ce point doit être traité hors patch local,
    via backlog de gouvernance et révision plus large.
- patch_readiness: blocked_by_scope_extension
- related_gate_checks:
  - WP_03
- gate_effect: keeps_open
- human_decision_applied: Option B

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
3. La décision humaine Option B confirme que ce point sort du traitement patch local de ce run.
4. Le gate reste ouvert principalement à cause de la frontière Référentiel / voisinage / partitionnement.

## Decisions for patch

Aucune décision n’est `ready_for_local_patch`.

État global patch synthesis:
- `blocked_by_scope_extension`

Conséquence opérationnelle :
- STAGE_03 ne doit pas synthétiser de patch local sur le finding AF-01.
- Si STAGE_03 est ouvert malgré tout, il devra conclure à l’absence de patch local autorisé pour ce finding.

## Decisions not retained

Les corrections suivantes sont explicitement non retenues :
- modifier `INV_MSC_AND_STRICT`
- réintégrer T dans la maîtrise de base
- affaiblir `RULE_MSC_COMPONENT_NON_CALCULABLE_DEFERS_BASE_MASTERY`
- modifier `INV_GRAPH_PROPAGATION_ONE_HOP`
- déplacer SIS / NC_MSC vers `learner_state`
- produire un patch YAML local pour corriger le mismatch référentiel dans ce run
- réécrire les Core pendant STAGE_02

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
      et les références réellement observées dans le scope et le Référentiel courant. La décision humaine Option B
      confirme que la correction dépasse le patch local et doit être traitée via gouvernance / révision de génération.
    recommended_stage00_action: >-
      Réévaluer les policy/decisions de génération de scope et les ancres inter-Core canonisées pour déterminer
      comment réaligner le scope mastery_evaluation, le voisinage référentiel et le catalogue de scopes.
    candidate_status: candidate_open
```

## Deferred or blocked decisions

### BD-01 — Patch local sur le mismatch référentiel
- status: blocked
- reason: >-
    La décision humaine Option B interdit le traitement comme patch local dans ce run.
- effect_on_stage_03: >-
    Aucun patch local ne doit être synthétisé sur ce finding ; le sujet relève d’une extension / révision plus large.

## Ambiguities requiring human decision

Aucune ambiguïté matérielle restante sur le finding principal.

Décision humaine intégrée :
- AD-01 resolved as **Option B**

human_decision_required_flag: false

## Human actions to execute

1. **Relire et valider cet arbitrage révisé**
   - Fichier cible :
     `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01/work/02_arbitrage/arbitrage_report_mastery_evaluation_r01.md`

2. **Mettre à jour le tracking de STAGE_02**
   - exécuter :
     ```bash
     python docs/patcher/shared/update_run_tracking.py \
       --pipeline constitution \
       --run-id CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01 \
       --stage-id STAGE_02_ARBITRAGE \
       --stage-status done \
       --run-status active \
       --next-stage STAGE_03_PATCH_SYNTHESIS \
       --summary "Arbitrage report validated; Option B retained; no local patch on referential mismatch."
     ```

3. **Préserver le candidat backlog jusqu’au STAGE_09**
   - ne pas perdre la section `governance_backlog_candidates` ; elle devra être relue en clôture pour export canonique.

4. **Relancer ensuite**
   - prompt suivant :
     `Continue le run CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01 — STAGE_02 est done, démarre STAGE_03_PATCH_SYNTHESIS.`
