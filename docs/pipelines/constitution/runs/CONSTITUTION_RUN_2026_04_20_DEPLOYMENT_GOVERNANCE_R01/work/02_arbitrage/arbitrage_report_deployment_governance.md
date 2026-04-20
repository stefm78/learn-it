# STAGE_02_ARBITRAGE — deployment_governance

run_id: CONSTITUTION_RUN_2026_04_20_DEPLOYMENT_GOVERNANCE_R01
scope_key: deployment_governance
mode: bounded_local_run
challenge_report_source: docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_DEPLOYMENT_GOVERNANCE_R01/work/01_challenge/challenge_report_deployment_governance.md

## executive_summary

L'arbitrage confirme que le scope `deployment_governance` ne présente pas, à ce stade, d'écart in-scope justifiant un patch local immédiat sur les IDs actuellement bornés par le run.

Le principal constat du challenge — dérive de référence inter-Core entre `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` et la référence active observée `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION` — doit être traité comme un sujet de gouvernance et de génération de surface, pas comme un patch local silencieux sur ce run.

Conclusion d'arbitrage :
- aucun patch local immédiat n'est retenu pour `deployment_governance`
- un candidat backlog de gouvernance doit être préservé pour export canonique ultérieur
- STAGE_03 peut démarrer, mais uniquement en mode `decision_only_no_patch_yet` sauf si l'humain décide explicitement d'ouvrir une correction locale très bornée de documentation de référence

## scope_analysed

Surface principale consommée :
- inputs/run_context.yaml
- inputs/scope_manifest.yaml
- inputs/impact_bundle.yaml
- inputs/integration_gate.yaml
- work/01_challenge/challenge_report_deployment_governance.md

Surface de support consommée car déclarée par le challenge :
- inputs/scope_extract.yaml
- inputs/neighbor_extract.yaml

Fallback repris explicitement :
- voisin absent `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`
- lecture ciblée du Core canonique pour constater que la référence active exposée est `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`

## detailed_arbitrage_by_finding

### A1
- challenge_finding_id: R1
- title: inter_core_reference_drift
- challenge_scope_status: out_of_scope_but_relevant
- arbitrage_decision: necessite_extension_scope
- arbitrage_justification: >-
    Le constat est matériel et significatif, mais il ne relève pas d'une correction
    locale silencieuse dans le périmètre writable actuel. Il touche la cohérence
    entre génération de scope, voisinage de lecture et références inter-Core.
    Le traitement correct doit passer par une revue de génération/policy et une
    remise en cohérence gouvernée, potentiellement rejouée en STAGE_00.
- patch_readiness: blocked_by_scope_extension
- related_gate_checks:
  - WP_02
  - FORBIDDEN_OPS_ENFORCEMENT
- gate_effect: keeps_open
- arbitration_notes: >-
    Toute correction directe dans le run sans revue de frontière serait à risque
    de réallocation implicite inter-Core ou de correction hors périmètre.

### A2
- challenge_finding_id: R2
- title: hidden_generation_staleness
- challenge_scope_status: out_of_scope_but_relevant
- arbitrage_decision: reporter
- arbitrage_justification: >-
    Le risque est plausible et cohérent avec A1, mais il n'est pas démontré ici
    sur d'autres scopes ni sur d'autres artefacts. Il doit être conservé comme
    signal de vigilance gouvernante plutôt que converti immédiatement en patch.
- patch_readiness: decision_only_no_patch_yet
- related_gate_checks:
  - WP_02
- gate_effect: keeps_open
- arbitration_notes: >-
    Ce point soutient le backlog candidate mais ne justifie pas, à lui seul,
    un changement local immédiat dans ce run.

### A3
- challenge_finding_id: R3
- title: parameterization_boundary_watchpoint
- challenge_scope_status: in_scope
- arbitrage_decision: reporter
- arbitrage_justification: >-
    Le challenge identifie une vigilance de frontière, mais pas une violation
    effective du principe constitutionnel. Les formulations actuelles restent
    acceptables ; aucun patch local n'est justifié sans preuve de dérive réelle.
- patch_readiness: decision_only_no_patch_yet
- related_gate_checks:
  - WP_05
- gate_effect: no_effect
- arbitration_notes: >-
    Point de surveillance à conserver dans la relecture humaine et les runs futurs,
    sans action corrective immédiate.

## consolidated_points

- Tous les risques prioritaires du challenge ont reçu une décision explicite.
- Aucun finding significatif n'appelle un patch local immédiat dans le périmètre actuel.
- Le point majeur porte sur la gouvernance des références inter-Core et la cohérence de génération.
- L'integration_gate reste ouvert, surtout au titre de WP_02 (séparation Constitution/Référentiel) et de la vérification d'absence de réallocation implicite.

## decisions_for_patch

Décisions retenues pour STAGE_03_PATCH_SYNTHESIS :
- aucune correction locale obligatoire à synthétiser dans le patchset pour ce run
- si STAGE_03 est lancé, il devra produire soit un patchset vide/gouverné, soit une note de non-patch local motivée, selon le contrat du stage
- aucun changement ne doit être fait sur les Core pour traiter A1 sans décision de gouvernance plus large

## decisions_not_retained

- corriger maintenant la référence inter-Core directement dans les Core du run : non retenu
- corriger silencieusement le voisinage de lecture ou l'impact_bundle local sans revue de génération : non retenu
- transformer R3 en correction locale : non retenu

## governance_backlog_candidates

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_DEPLOYMENT_GOVERNANCE_INTERCORE_REF_ALIGNMENT_2026_04_20
    backlog_entry_type: scope_extension_needed
    title: Aligner la référence inter-Core Constitution → Référentiel avec le canon courant
    related_scope_keys:
      - deployment_governance
    originating_run_id: CONSTITUTION_RUN_2026_04_20_DEPLOYMENT_GOVERNANCE_R01
    source_finding_id: R1
    rationale: >-
      Le voisin requis dans l'impact_bundle et le neighbor_extract pointe vers
      REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION, tandis que la Constitution
      active expose une référence V4.0. La remise en cohérence dépasse le patch local
      d'un run borné et doit être rejouée dans une chaîne gouvernée de génération.
    recommended_stage00_action: >-
      Réévaluer la policy/decisions de génération des scopes et des voisins,
      confirmer l'identifiant inter-Core canonique attendu, puis régénérer le
      scope catalog si nécessaire.
    candidate_status: candidate_open
```

## deferred_or_blocked_decisions

- A1 bloqué par extension/revue de scope generation et décision de gouvernance
- A2 reporté en signal de vigilance jusqu'à constat plus large
- A3 reporté en watchpoint sans patch local

## ambiguities_requiring_human_decision

Aucune ambiguïté matérielle bloquante n'impose un arbitrage humain avant STAGE_03, à condition d'accepter explicitement la décision suivante :
- STAGE_03 peut être ouvert sans objectif de patch local immédiat, uniquement pour formaliser qu'aucune correction locale n'est retenue à ce stade

Point de confirmation humaine recommandé :
- confirmer que l'on préfère `aucun patch local` plutôt qu'une tentative de correction documentaire locale de la référence inter-Core

## human_actions_required

- relire et valider cet arbitrage_report
- préserver le bloc `governance_backlog_candidates` pour l'export canonique en STAGE_09
- si l'arbitrage est validé, mettre à jour le tracking vers STAGE_03_PATCH_SYNTHESIS
