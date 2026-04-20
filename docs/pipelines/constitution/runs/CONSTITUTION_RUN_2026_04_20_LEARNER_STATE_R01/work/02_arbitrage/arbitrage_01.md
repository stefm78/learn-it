# STAGE_02_ARBITRAGE — learner_state
run_id: CONSTITUTION_RUN_2026_04_20_LEARNER_STATE_R01
scope_key: learner_state
mode: bounded_local_run

## executive_summary

L’arbitrage confirme le diagnostic du challenge : le problème principal du run `learner_state` n’est pas une incohérence locale majeure de la philosophie d’état apprenant, mais une **fermeture insuffisante des interfaces inter-Core et inter-scope**. Le noyau conceptuel local est globalement sain, mais il est grevé par une référence référentielle non alignée, un voisinage logique sous-matérialisé, et des sorties moteur qui dépassent la surface bornée du run.

Décision d’ensemble :
- corriger maintenant ce qui relève de la **normalisation locale de la chaîne de référence côté Constitution / run borné**
- ne **pas** corriger silencieusement ce qui relève d’une extension de scope ou d’une révision de partition
- appliquer la décision humaine suivante : alignement sur la convention `v3.0` pour la référence inter-Core, et backlog / redécoupage de scope plutôt que patch local pour les dépendances hors périmètre

## scope_analysed

Périmètre modifiable autorisé :
- `docs/cores/current/constitution.yaml`
- uniquement sur les IDs du `scope_manifest` du run

Le `impact_bundle` étend le devoir de lecture mais pas le droit de modifier.
Le `integration_gate` impose notamment :
- de ne pas transformer un seuil référentiel en règle constitutionnelle implicite
- de garder explicites les liens au Référentiel
- de vérifier les frontières entre unknown, détresse, conservatisme et escalade

Challenge report principal consommé :
- `challenge_report_01.md`

Fallback repris explicitement, conformément au skill :
- `docs/cores/current/link.yaml`
- `docs/cores/current/referentiel.yaml`

## detailed_arbitrage_by_finding

### F1
- challenge_finding_id: R1
- challenge_scope_status: in_scope
- finding_title: Discordance inter-Core de références/versionnement
- finding_summary: Le run attend `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` via le voisinage déclaré, alors que `neighbor_extract.yaml` ne le trouve pas, que `link.yaml` expose `LINK_REF_CORE_LEARNIT_REFERENTIEL_v3.0`, et que le Référentiel courant est `CORE_LEARNIT_REFERENTIEL_v3.0`.
- arbitrage_decision: corriger_maintenant
- arbitrage_justification: La correction est admissible localement si elle consiste à **réaligner la référence constitutionnelle / run borné sur la convention canonique réellement en vigueur**, sans réécrire le Référentiel ni le Link. La décision humaine a tranché l’ambiguïté en faveur d’un alignement `v3.0`.
- patch_readiness: ready_for_local_patch
- related_gate_checks:
  - WP_04
  - FORBIDDEN_OPS_ENFORCEMENT
- gate_effect: helps_clear
- ambiguity_declared_per_finding_if_any: false
- human_decision_required_flag_if_needed: false
- scope_status_declared: in_scope

### F2
- challenge_finding_id: R2
- challenge_scope_status: out_of_scope_but_relevant
- finding_title: Sous-déclaration du voisinage logique du scope
- finding_summary: Des règles du scope ciblent des actions absentes de la surface lue : `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK` et `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`.
- arbitrage_decision: necessite_extension_scope
- arbitrage_justification: Le skill interdit toute correction silencieuse hors périmètre. Le `scope_manifest` ne donne pas de droit de modifier ces sorties, et la décision humaine a confirmé backlog / redécoupage de scope plutôt que patch local.
- patch_readiness: blocked_by_scope_extension
- related_gate_checks:
  - WP_05
  - WP_06
  - FORBIDDEN_OPS_ENFORCEMENT
- gate_effect: keeps_open
- ambiguity_declared_per_finding_if_any: false
- human_decision_required_flag_if_needed: false
- scope_status_declared: needs_scope_extension

### F3
- challenge_finding_id: R3
- challenge_scope_status: in_scope
- finding_title: Mismatch entre extracts et vrais besoins de lecture
- finding_summary: `neighbor_extract.yaml` est présent mais vide en contenu utile pour le run, car son unique ID cible est manquant, alors que le fallback vers Link/Référentiel a été nécessaire.
- arbitrage_decision: corriger_maintenant
- arbitrage_justification: C’est un problème concret de matérialisation du voisinage logique du run. La décision humaine a confirmé une correction locale minimale, alignée sur la convention `v3.0`, sans élargir silencieusement le périmètre.
- patch_readiness: ready_for_local_patch
- related_gate_checks:
  - WP_04
- gate_effect: helps_clear
- ambiguity_declared_per_finding_if_any: false
- human_decision_required_flag_if_needed: false
- scope_status_declared: in_scope

## consolidated_points

1. Le challenge report est retenu sur son diagnostic principal : la fermeture inter-Core et inter-scope est le vrai problème, pas la philosophie learner_state elle-même.
2. Le modèle local learner_state est considéré comme **théoriquement acceptable** et ne justifie pas, à ce stade, une refonte de ses invariants de prudence, de non-inférence ou de priorité de détresse.
3. L’arbitrage autorise un patch local minimal pour :
   - réaligner la référence inter-Core côté Constitution / run
   - réaligner le voisinage déclaré pour qu’il redevienne extractible et audit-able
4. L’arbitrage refuse toute correction silencieuse visant à :
   - intégrer localement des actions cross-scope non gouvernées
   - modifier Link ou Référentiel depuis ce run
   - compenser le défaut de partition par un patch local implicite

## decisions_for_patch

### DP1
- source_finding_id: R1
- decision: corriger_maintenant
- patch_target_kind: constitution_reference_alignment
- patch_scope_status: in_scope
- patch_readiness: ready_for_local_patch
- rationale: réaligner la référence inter-Core learner_state sur la convention canonique `v3.0`, sans modifier Link ni Référentiel dans ce run

### DP2
- source_finding_id: R3
- decision: corriger_maintenant
- patch_target_kind: impact_neighbor_reference_alignment
- patch_scope_status: in_scope
- patch_readiness: ready_for_local_patch
- rationale: remplacer l’ID voisin non résolu par un voisin canonique réellement extractible, aligné sur la convention `v3.0`

## decisions_not_retained

### DNR1
- source_finding_id: R2
- decision: non retenue pour patch local
- reason: les actions cibles hors surface (`ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`, `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`) relèvent d’une fermeture cross-scope ou d’une révision de partition, pas d’un patch local silencieux

### DNR2
- source_finding_id: R1
- decision: rejet d’une correction large inter-Core immédiate
- reason: ce run n’a ni mandat ni périmètre pour réécrire simultanément Constitution, Link et Référentiel

## governance_backlog_candidates

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_LS_R2_SCOPE_CLOSURE_ACTION_TARGETS
    backlog_entry_type: scope_extension_needed
    title: Clarifier la fermeture cross-scope des actions de reprise diagnostique et d’escalade hors session
    related_scope_keys:
      - learner_state
    originating_run_id: CONSTITUTION_RUN_2026_04_20_LEARNER_STATE_R01
    source_finding_id: R2
    rationale: >-
      Le scope learner_state contient des règles qui déclenchent des actions
      absentes du périmètre lisible du run borné. Leur statut doit être
      explicitement gouverné : voisinage obligatoire, dépendance cross-scope,
      ou révision de partition.
    recommended_stage00_action: >-
      Réévaluer la partition sémantique pour déterminer si
      ACTION_PLAN_SHORT_DIAGNOSTIC_TASK et
      ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION doivent être intégrées à un
      scope voisin explicite ou matérialisées comme dépendances inter-scope
      canonisées.
    candidate_status: candidate_open
```

## deferred_or_blocked_decisions

1. Statut cross-scope des actions cibles hors surface
   État : reporté vers backlog / Stage 00 / éventuelle révision de partition

## ambiguities_requiring_human_decision

Aucune ambiguïté matérielle résiduelle :
- A1 a été tranchée par l’humain en faveur de l’alignement `v3.0`
- A2 a été tranchée par l’humain en faveur d’un backlog / redécoupage de scope plutôt que patch local pour les dépendances hors périmètre
