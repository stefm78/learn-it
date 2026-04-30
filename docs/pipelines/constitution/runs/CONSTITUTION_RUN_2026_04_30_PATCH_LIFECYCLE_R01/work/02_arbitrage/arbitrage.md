# STAGE_02_ARBITRAGE — patch_lifecycle

run_id: `CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01`  
pipeline: `constitution`  
mode: `bounded_local_run`  
stage: `STAGE_02_ARBITRAGE`  
status: `arbitrage_report_written`

## 1. Executive summary

L'arbitrage reprend explicitement les huit findings significatifs du rapport STAGE_01_CHALLENGE et les transforme en décisions exploitables par STAGE_03_PATCH_SYNTHESIS.

Décision globale : **autoriser une synthèse de patch locale, mais uniquement sur un périmètre étroit**.

Le patch autorisé doit :

1. renforcer la sémantique des états terminaux de patch **dans les IDs déjà in-scope** ;
2. clarifier que FIFO gouverne les déclenchements concurrents ordinaires, mais pas le traitement terminal immédiat du rollback, du blocage d'intégrité ou de l'escalade hors session ;
3. limiter explicitement la propriété `patch_lifecycle` aux échecs, blocages, rollback non vérifiables et inefficacités de patches ;
4. réduire le risque de vocabulaire psychologisant autour de l'AR en conservant les IDs, mais en durcissant les formulations observables ;
5. préciser les métadonnées déterministes minimales attendues pour la preuve de QA précomputée.

Le patch ne doit pas :

- introduire un nouveau Core ID de state machine sans extension de scope ;
- modifier le Référentiel ou le Link ;
- inventer localement le paramètre externe `N` ;
- ajouter des priority lanes complètes ;
- modifier la production des signaux learner_state ;
- renommer des IDs existants sans stratégie de migration.

Aucune génération de patch YAML n'est effectuée en STAGE_02.

## 2. Scope analysed

### 2.1 Inputs considered

Challenge report considered:

- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/work/01_challenge/challenge_report_patch_lifecycle_R01.md`

Runtime inputs considered:

- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/run_context.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/integration_gate.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/scope_extract.yaml`
- `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01/inputs/neighbor_extract.yaml`

Challenge report resolution:

- unique challenge report found and consumed;
- no challenge report omitted;
- all priority risks CH-PL-01 through CH-PL-08 considered.

Human notes:

- no additional human arbitration notes were provided for this stage.

Fallback reads:

- none used;
- no missing ID from `scope_extract.yaml` or `neighbor_extract.yaml` was declared by STAGE_01.

### 2.2 Scope constraints

Writable scope remains limited to the `patch_lifecycle` bounded run perimeter.

The impact bundle extends read duties only; it does not authorize:

- modifying learner_state-owned signal generation;
- modifying the Référentiel or Link;
- reallocating cross-core ownership;
- writing directly to `governance_backlog.yaml`.

### 2.3 Integration gate binding

Integration gate checks remain open. This arbitration contributes mainly to:

- `WP_01`: deterministic local patch validation;
- `WP_02`: precomputed patch artifacts;
- `WP_03`: no runtime adaptation drift;
- `WP_04`: learner_state boundary;
- `WP_05`: escalation boundary;
- `FORBIDDEN_OPS_ENFORCEMENT`: no forbidden operation.

## 3. Detailed arbitrage by finding

### CH-PL-01 — Missing explicit patch state model

```yaml
finding_arbitrage:
  challenge_finding_id: CH-PL-01
  challenge_scope_status: in_scope
  arbitrage_decision: corriger_maintenant
  patch_readiness: ready_for_local_patch
  related_gate_checks:
    - WP_01
    - WP_02
    - FORBIDDEN_OPS_ENFORCEMENT
  gate_effect: helps_clear
  ambiguity_declared: true
  conservative_default: >-
    Ne pas introduire de nouveau Core ID de state machine dans ce run.
    Durcir uniquement les états terminaux déterministes dans les IDs déjà in-scope.
  human_decision_required_flag: false
```

Justification :

Le challenge identifie un vrai risque : le vocabulaire terminal existe, mais le modèle d'état est implicite. Une state machine complète pourrait être utile, mais son introduction comme nouveau type ou graphe de transitions dépasserait probablement le patch minimal sûr.

Arbitrage :

- corriger maintenant la sémantique terminale minimale ;
- ne pas créer de nouveau `TYPE_PATCH_STATE_MACHINE` ou équivalent dans ce run ;
- autoriser STAGE_03 à renforcer les formulations existantes dans `TYPE_PATCH_ARTIFACT`, `RULE_PATCH_SERIALIZATION`, `INV_NO_PARTIAL_PATCH_STATE`, `ACTION_ROLLBACK_PATCH` et `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`.

Instruction pour STAGE_03 :

Définir textuellement une liste fermée d'issues terminales acceptées, par exemple :

- appliqué ;
- rejeté ;
- rollbacké ;
- bloqué après rollback non vérifiable ;
- escaladé hors session.

Cette liste doit rester une clarification locale, pas une nouvelle architecture complète de state machine.

### CH-PL-02 — FIFO serialization vs severity/priority semantics

```yaml
finding_arbitrage:
  challenge_finding_id: CH-PL-02
  challenge_scope_status: in_scope
  arbitrage_decision: corriger_maintenant
  patch_readiness: ready_for_local_patch
  related_gate_checks:
    - WP_01
    - WP_03
    - WP_05
    - FORBIDDEN_OPS_ENFORCEMENT
  gate_effect: helps_clear
  ambiguity_declared: true
  conservative_default: >-
    Conserver FIFO pour les déclenchements ordinaires, mais exclure du FIFO
    le traitement terminal immédiat du rollback, du blocage d'intégrité et de
    l'escalade hors session. Reporter les priority lanes complètes.
  human_decision_required_flag: false
```

Justification :

FIFO est déterministe, mais peut être insuffisant pour les situations critiques. Introduire des priority lanes complètes serait une extension de conception. Le compromis minimal est de conserver FIFO pour les déclenchements ordinaires et de clarifier que certains événements ne sont pas de nouveaux patches concurrents : ils relèvent du traitement terminal du patch actif.

Arbitrage :

- corriger maintenant `RULE_PATCH_SERIALIZATION` ;
- préserver FIFO pour `ACTION_TRIGGER_RELEVANCE_PATCH`, `ACTION_TRIGGER_AR_SOLLICITATION_PATCH` et déclenchements ordinaires futurs ;
- expliciter que rollback, rollback non vérifiable, blocage d'intégrité et escalade hors session sont des traitements terminaux immédiats, non des éléments FIFO ;
- reporter tout modèle de priority lanes à un design ultérieur.

Instruction pour STAGE_03 :

Réécrire uniquement la logique de sérialisation pour éviter qu'un événement critique soit placé derrière une file FIFO ordinaire.

### CH-PL-03 — External parameter `N`

```yaml
finding_arbitrage:
  challenge_finding_id: CH-PL-03
  challenge_scope_status: out_of_scope_but_relevant
  arbitrage_decision: hors_perimetre
  patch_readiness: blocked_by_scope_extension
  related_gate_checks:
    - WP_05
    - FORBIDDEN_OPS_ENFORCEMENT
  gate_effect: keeps_open
  ambiguity_declared: false
  conservative_default: >-
    Ne pas inventer le paramètre N localement. Conserver l'externalité Référentiel/Link.
  human_decision_required_flag: false
```

Justification :

Le paramètre `N` appartient au Référentiel ou à un contrat cross-core. Le run Constitution `patch_lifecycle` peut consommer l'idée d'un seuil externe, mais ne peut pas le créer ou le canoniser localement.

Arbitrage :

- aucun patch local sur le paramètre `N` ;
- ne pas modifier Référentiel ou Link ;
- conserver une trace backlog locale pour export/relecture STAGE_09 ;
- STAGE_03 peut seulement éviter toute formulation laissant croire que `N` est résolu localement.

Instruction pour STAGE_03 :

Ne pas ajouter de valeur, nom de paramètre, borne ou règle Référentiel. Au maximum, renforcer la formulation `paramètre externe du Référentiel` si cela réduit l'ambiguïté sans modifier le contrat cross-core.

### CH-PL-04 — Escalation ownership boundary

```yaml
finding_arbitrage:
  challenge_finding_id: CH-PL-04
  challenge_scope_status: needs_scope_extension
  arbitrage_decision: corriger_maintenant
  patch_readiness: ready_for_local_patch
  related_gate_checks:
    - WP_04
    - WP_05
    - FORBIDDEN_OPS_ENFORCEMENT
  gate_effect: helps_clear
  ambiguity_declared: true
  conservative_default: >-
    Corriger localement la formulation pour limiter la propriété patch_lifecycle
    aux escalades causées par le cycle de vie patch, tout en conservant une
    trace backlog pour la frontière globale learner_state/governance.
  human_decision_required_flag: false
```

Justification :

La frontière globale dépasse le scope, mais le patch peut utilement réduire le risque de sur-appropriation en clarifiant que le patch_lifecycle ne possède pas les signaux de détresse, conservatisme sans sortie ou investigation systémique, sauf lorsqu'ils sont consommés comme signaux externes déjà gouvernés.

Arbitrage :

- corriger maintenant les formulations dans les IDs in-scope concernés ;
- ne pas redéfinir learner_state ;
- ne pas redéfinir governance ;
- créer une trace backlog locale pour la frontière globale.

Instruction pour STAGE_03 :

Dans `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`, `RULE_PERSISTENT_DRIFT_BLOCKED_PATCH_ESCALATES_OFFSESSION` et `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`, formuler clairement que le patch_lifecycle possède seulement :

- patch rejeté ;
- patch impossible ;
- patch bloqué ;
- rollback non vérifiable ;
- patch inefficace après seuil externe.

Les causes plus larges restent des signaux externes, non requalifiés par le patch_lifecycle.

### CH-PL-05 — AR refractory wording

```yaml
finding_arbitrage:
  challenge_finding_id: CH-PL-05
  challenge_scope_status: in_scope
  arbitrage_decision: corriger_maintenant
  patch_readiness: ready_for_local_patch
  related_gate_checks:
    - WP_03
    - WP_04
    - FORBIDDEN_OPS_ENFORCEMENT
  gate_effect: helps_clear
  ambiguity_declared: true
  conservative_default: >-
    Ne pas renommer les IDs existants dans ce run. Corriger les libellés et
    formulations pour les recentrer sur une fenêtre observable de non-réponse AR.
  human_decision_required_flag: false
```

Justification :

L'ID `EVENT_AR_REFRACTORY_PROFILE_DETECTED` et les textes associés peuvent suggérer un profil psychologique, alors que la logique interdit explicitement toute inférence psychologique. Renommer l'ID nécessiterait une migration de références ; ce n'est pas minimal. En revanche, les champs `human_readable` et `logic` peuvent être durcis.

Arbitrage :

- corriger maintenant les formulations ;
- ne pas renommer l'ID dans ce run ;
- éviter les termes `profil` et `réfractaire` dans les champs humains lorsque possible ;
- préférer `fenêtre observable de non-réponse AR`.

Instruction pour STAGE_03 :

Réviser `EVENT_AR_REFRACTORY_PROFILE_DETECTED`, `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH` et `ACTION_TRIGGER_AR_SOLLICITATION_PATCH` en conservant les IDs.

### CH-PL-06 — QA proof schema not visible in bounded surface

```yaml
finding_arbitrage:
  challenge_finding_id: CH-PL-06
  challenge_scope_status: in_scope
  arbitrage_decision: corriger_maintenant
  patch_readiness: ready_for_local_patch
  related_gate_checks:
    - WP_01
    - WP_02
    - FORBIDDEN_OPS_ENFORCEMENT
  gate_effect: helps_clear
  ambiguity_declared: false
  conservative_default: >-
    Renforcer les métadonnées déterministes attendues sans définir une nouvelle
    chaîne de QA sémantique.
  human_decision_required_flag: false
```

Justification :

La preuve QA précomputée est déjà conceptuellement présente, mais sa vérification déterministe peut être renforcée sans créer de nouveau mécanisme. Le patch doit rester au niveau de la présence, intégrité, portée, version, fraîcheur, empreintes et statut déclaré.

Arbitrage :

- corriger maintenant `TYPE_PATCH_QUALITY_GATE`, `TYPE_PATCH_ARTIFACT` et éventuellement `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` ;
- ne pas introduire d'évaluation pédagogique runtime ;
- ne pas définir une nouvelle chaîne complète de QA.

Instruction pour STAGE_03 :

Ajouter ou consolider une liste déterministe minimale des métadonnées vérifiables localement.

### CH-PL-07 — `TYPE_SELF_REPORT_AR_N2` missing from neighbor dependency closure

```yaml
finding_arbitrage:
  challenge_finding_id: CH-PL-07
  challenge_scope_status: needs_scope_extension
  arbitrage_decision: necessite_extension_scope
  patch_readiness: blocked_by_scope_extension
  related_gate_checks:
    - WP_04
    - FORBIDDEN_OPS_ENFORCEMENT
  gate_effect: keeps_open
  ambiguity_declared: false
  conservative_default: >-
    Ne pas lire ni modifier implicitement `TYPE_SELF_REPORT_AR_N2` dans ce run.
    Traiter l'écart comme un signal de scope generation / neighbor declaration.
  human_decision_required_flag: false
```

Justification :

`TYPE_STATE_AXIS_VALUE_COST` est un neighbor lu, et il dépend de `TYPE_SELF_REPORT_AR_N2`. Le run ne signale pas d'ID manquant car `TYPE_SELF_REPORT_AR_N2` n'était pas demandé ; c'est donc un signal de fermeture de voisinage, pas une erreur d'extract.

Arbitrage :

- ne pas corriger localement ;
- ne pas fallback-read le Core complet ;
- créer une trace backlog locale pour STAGE_09 ;
- demander à la génération de scopes de décider si `TYPE_SELF_REPORT_AR_N2` doit être explicitement voisin de `patch_lifecycle`.

Instruction pour STAGE_03 :

Aucune correction locale sur ce point.

### CH-PL-08 — `ACTION_LOG_UNCOVERED_CONFLICT` ownership ambiguity

```yaml
finding_arbitrage:
  challenge_finding_id: CH-PL-08
  challenge_scope_status: out_of_scope_but_relevant
  arbitrage_decision: reporter
  patch_readiness: decision_only_no_patch_yet
  related_gate_checks:
    - FORBIDDEN_OPS_ENFORCEMENT
  gate_effect: no_effect
  ambiguity_declared: false
  conservative_default: >-
    Ne pas modifier cet ID dans ce run, sauf si STAGE_03 découvre une dépendance
    directe nécessaire à une décision patch_lifecycle retenue.
  human_decision_required_flag: false
```

Justification :

Le challenge indique un risque P3 : l'ID est dans le périmètre writable mais son champ `scope` indique `runtime_governance`. Des analyses antérieures semblent avoir déjà conclu que ce n'est pas bloquant sauf défaut concret. Aucune correction prioritaire n'est nécessaire pour le patch local actuel.

Arbitrage :

- reporter ;
- ne pas modifier dans ce run ;
- ne pas créer de backlog supplémentaire sauf découverte d'un défaut concret ultérieur.

Instruction pour STAGE_03 :

Ne pas toucher `ACTION_LOG_UNCOVERED_CONFLICT`.

## 4. Consolidated points

### 4.1 Points retained for local patch synthesis

The following decisions are retained for STAGE_03:

1. Minimal terminal-state clarification for patch outcomes.
2. FIFO clarification: ordinary triggers are FIFO; terminal rollback/block/escalation handling is immediate and out-of-band.
3. Escalation ownership clarification: patch_lifecycle owns only patch-caused failure/block/ineffectiveness paths.
4. AR wording hardening: observable non-response terminology, no ID rename.
5. Deterministic QA proof metadata hardening.

### 4.2 Points explicitly excluded from local patch

The following points must not be patched locally:

1. Creating or setting external parameter `N`.
2. Modifying Référentiel or Link.
3. Adding `TYPE_SELF_REPORT_AR_N2` by implicit fallback or direct scope change.
4. Introducing a full priority-lane model.
5. Introducing a new Core ID for a full patch state machine.
6. Reassigning `ACTION_LOG_UNCOVERED_CONFLICT`.

### 4.3 Patch minimality rule

STAGE_03 must prefer modifications to existing in-scope entries over adding new IDs. Any new ID must be treated as blocked unless it is demonstrably inside the existing writable perimeter or explicitly authorized by a revised scope decision.

## 5. Decisions for patch

```yaml
decisions_for_patch:
  - decision_id: ARB-PL-01
    source_findings:
      - CH-PL-01
    action: harden_minimal_terminal_patch_outcomes
    allowed_target_ids:
      - TYPE_PATCH_ARTIFACT
      - INV_NO_PARTIAL_PATCH_STATE
      - RULE_PATCH_SERIALIZATION
      - ACTION_ROLLBACK_PATCH
      - ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION
    patch_readiness: ready_for_local_patch
    constraints:
      - no_new_state_machine_id
      - no_full_transition_graph
      - deterministic_terminal_vocabulary_only

  - decision_id: ARB-PL-02
    source_findings:
      - CH-PL-02
    action: clarify_fifo_vs_terminal_handling
    allowed_target_ids:
      - RULE_PATCH_SERIALIZATION
      - ACTION_ROLLBACK_PATCH
      - ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION
    patch_readiness: ready_for_local_patch
    constraints:
      - keep_fifo_for_ordinary_patch_triggers
      - terminal_rollback_block_escalation_not_fifo
      - no_priority_lanes_in_this_patch

  - decision_id: ARB-PL-03
    source_findings:
      - CH-PL-04
    action: restrict_patch_lifecycle_escalation_ownership
    allowed_target_ids:
      - INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED
      - RULE_PERSISTENT_DRIFT_BLOCKED_PATCH_ESCALATES_OFFSESSION
      - ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION
    patch_readiness: ready_for_local_patch
    constraints:
      - consume_external_signals_only
      - no_learner_state_redefinition
      - no_governance_reallocation

  - decision_id: ARB-PL-04
    source_findings:
      - CH-PL-05
    action: harden_ar_non_response_wording
    allowed_target_ids:
      - EVENT_AR_REFRACTORY_PROFILE_DETECTED
      - RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH
      - ACTION_TRIGGER_AR_SOLLICITATION_PATCH
    patch_readiness: ready_for_local_patch
    constraints:
      - no_id_rename
      - no_psychological_inference
      - use_observable_non_response_wording

  - decision_id: ARB-PL-05
    source_findings:
      - CH-PL-06
    action: strengthen_deterministic_qa_proof_metadata
    allowed_target_ids:
      - TYPE_PATCH_ARTIFACT
      - TYPE_PATCH_QUALITY_GATE
      - INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC
      - INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION
    patch_readiness: ready_for_local_patch
    constraints:
      - no_runtime_semantic_judgment
      - no_runtime_pedagogical_evaluation
      - verify_presence_integrity_scope_version_freshness_fingerprints_status
```

## 6. Decisions not retained

```yaml
decisions_not_retained:
  - decision_id: REJECT-PL-01
    source_findings:
      - CH-PL-01
    rejected_option: introduce_full_patch_state_machine
    reason: >-
      Trop large pour ce bounded run. Nécessite probablement un nouveau type, un graphe
      de transitions et une stratégie de migration.
    retained_alternative: minimal_terminal_vocabulary_hardening

  - decision_id: REJECT-PL-02
    source_findings:
      - CH-PL-02
    rejected_option: introduce_priority_lanes
    reason: >-
      Dépasse le patch minimal et risque d'introduire une politique de scheduling non arbitrée.
    retained_alternative: fifo_for_ordinary_triggers_terminal_handling_out_of_band

  - decision_id: REJECT-PL-03
    source_findings:
      - CH-PL-05
    rejected_option: rename_ar_refractory_ids
    reason: >-
      Le renommage d'IDs existants implique une migration de références qui n'est pas
      nécessaire pour réduire le risque de formulation.
    retained_alternative: harden_human_readable_and_logic_text

  - decision_id: REJECT-PL-04
    source_findings:
      - CH-PL-08
    rejected_option: reassign_action_log_uncovered_conflict
    reason: >-
      Aucun défaut concret nouveau ne justifie de réouvrir cette frontière dans le patch courant.
    retained_alternative: report_no_patch
```

## 7. Governance backlog candidates

STAGE_02 ne modifie jamais `governance_backlog.yaml`. Les candidats ci-dessous sont des traces locales à conserver pour STAGE_09.

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_PATCH_LIFECYCLE_REFERENTIEL_PARAMETER_R02
    backlog_entry_type: scope_gap
    title: Confirm external Référentiel parameter contract for ineffective patch iteration threshold N
    related_scope_keys:
      - patch_lifecycle
    originating_run_id: CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01
    source_finding_id: CH-PL-03
    rationale: >-
      The patch_lifecycle Constitution scope references an external parameter N controlling
      the number of ineffective patch iterations before escalation, but this bounded run
      cannot define, validate or modify that parameter in Référentiel or Link.
    recommended_stage00_action: >-
      Keep as cross-core follow-up. Decide whether a concrete external-read-only
      parameter should be declared in scope generation or whether a cross-core
      change request is required.
    candidate_status: candidate_open

  - candidate_id: GBC_PATCH_LIFECYCLE_ESCALATION_BOUNDARY_R02
    backlog_entry_type: scope_extension_needed
    title: Preserve global escalation ownership boundary across patch_lifecycle, learner_state and governance
    related_scope_keys:
      - patch_lifecycle
      - learner_state
      - deployment_governance
    originating_run_id: CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01
    source_finding_id: CH-PL-04
    rationale: >-
      The local patch can clarify patch-caused escalation paths, but the broader
      ownership of distress, conservatism-without-exit and systemic investigation
      signals remains cross-scope and must not be silently transferred to patch_lifecycle.
    recommended_stage00_action: >-
      Revisit escalation ownership during a dedicated partition/scope review if
      future runs touch learner_state or governance escalation semantics.
    candidate_status: candidate_open

  - candidate_id: GBC_PATCH_LIFECYCLE_VALUE_COST_AR_N2_NEIGHBOR_R01
    backlog_entry_type: scope_gap
    title: Decide whether TYPE_SELF_REPORT_AR_N2 should be an explicit read neighbor for patch_lifecycle
    related_scope_keys:
      - patch_lifecycle
      - learner_state
    originating_run_id: CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01
    source_finding_id: CH-PL-07
    rationale: >-
      TYPE_STATE_AXIS_VALUE_COST is a mandatory read neighbor and depends on
      TYPE_SELF_REPORT_AR_N2, but TYPE_SELF_REPORT_AR_N2 is not itself present in
      the run mandatory read surface. This is a neighbor-closure governance signal,
      not a local patch authorization.
    recommended_stage00_action: >-
      Re-evaluate scope_generation policy/decisions for patch_lifecycle neighbor
      declarations and regenerate the scope catalog if explicit neighbor closure is approved.
    candidate_status: candidate_needs_human_review
```

## 8. Deferred or blocked decisions

```yaml
deferred_or_blocked_decisions:
  - source_finding_id: CH-PL-03
    decision: hors_perimetre
    blocked_reason: requires_referentiel_or_link_contract
    patch_readiness: blocked_by_scope_extension
    may_block_stage03: false
    condition: >-
      Does not block STAGE_03 as long as STAGE_03 does not invent or patch N.

  - source_finding_id: CH-PL-07
    decision: necessite_extension_scope
    blocked_reason: neighbor_dependency_closure_requires_scope_generation_decision
    patch_readiness: blocked_by_scope_extension
    may_block_stage03: false
    condition: >-
      Does not block STAGE_03 as long as STAGE_03 does not modify or rely on
      TYPE_SELF_REPORT_AR_N2 beyond the already-read TYPE_STATE_AXIS_VALUE_COST neighbor.

  - source_finding_id: CH-PL-08
    decision: reporter
    blocked_reason: no_current_defect_requiring_patch
    patch_readiness: decision_only_no_patch_yet
    may_block_stage03: false
```

## 9. Ambiguities requiring human decision

No material ambiguity blocks STAGE_03 under the conservative defaults selected above.

Human validation is still required before transition to STAGE_03 because STAGE_02 is a high-closure cognitive stage. If the human rejects any conservative default, the arbitrage must be revised before patch synthesis.

Potential optional human overrides:

1. If a full state machine is desired now, revise this arbitrage; do not proceed with the minimal patch.
2. If priority lanes are desired now, revise this arbitrage; do not proceed with the FIFO clarification only.
3. If ID renaming for AR wording is desired, revise this arbitrage and prepare a migration strategy.
4. If `TYPE_SELF_REPORT_AR_N2` must be read now, revise the run scope or rerun materialization after scope update.

## 10. Completion evidence

- `arbitrage_report_written`: yes
- `all_challenge_reports_considered`: yes
- `every_significant_finding_has_explicit_decision`: yes
- `every_priority_risk_from_challenge_has_explicit_decision`: yes
- `every_arbitrage_request_from_challenge_is_resolved`: yes
- `decisions_for_patch_section_present`: yes
- `scope_status_declared_per_finding`: yes
- `human_notes_integrated_if_provided`: yes, none provided
- `ambiguities_explicitly_flagged_if_any`: yes
- `governance_backlog_candidates_declared_if_needed`: yes
- `governance_backlog_candidates_serialized_in_yaml_block_if_present`: yes
- `patch_yaml_produced`: no
- `core_document_rewrite`: no
- `direct_write_to_governance_backlog_during_stage_02`: no

## 11. Human actions to execute

If this arbitration is accepted, execute:

```bash
RUN_ID="CONSTITUTION_RUN_2026_04_30_PATCH_LIFECYCLE_R01"

python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id "$RUN_ID" \
  --stage-id STAGE_02_ARBITRAGE \
  --stage-status done \
  --run-status active \
  --next-stage STAGE_03_PATCH_SYNTHESIS \
  --summary "Arbitrage report validated; decisions ready for patch synthesis."
```

Then commit and push the run updates before asking the AI to continue STAGE_03_PATCH_SYNTHESIS.
