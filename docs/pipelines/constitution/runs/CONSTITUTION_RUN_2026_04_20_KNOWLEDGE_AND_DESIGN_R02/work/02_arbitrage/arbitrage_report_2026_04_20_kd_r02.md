# STAGE_02_ARBITRAGE — arbitrage_report_2026_04_20_kd_r02

## executive_summary

Le challenge du scope `knowledge_and_design` confirme une bonne cohérence locale du périmètre, mais fait ressortir deux écarts structurants qui ne doivent pas être corrigés silencieusement en patch local :

1. un drift d’identifiants / de version entre le voisin attendu par le run (`REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`) et le `LINK` courant, qui expose des références `LINK_REF_CORE_LEARNIT_CONSTITUTION_V4_0` et `LINK_REF_CORE_LEARNIT_REFERENTIEL_v3.0` ;
2. une dépendance implicite hors surface entre `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION` et `INV_NO_RUNTIME_CONTENT_GENERATION`, absente du périmètre de lecture borné.

Ces deux points sont matériels pour la qualité du futur patch, mais ils dépassent la sécurité d’un correctif strictement local sur les IDs actuellement autorisés en écriture. L’arbitrage retient donc une posture conservatrice :
- **aucune correction silencieuse hors périmètre** ;
- **aucun patch local sur les points inter-Core / extension de scope tant qu’une décision humaine explicite n’a pas été donnée** ;
- **préservation d’une trace locale de backlog candidate** pour export canonique ultérieur.

En revanche, le constat de cohérence locale du cœur `knowledge_and_design` est retenu comme validé, sans action de patch immédiate.

## scope_analysed

- Run: `CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02`
- Mode: `bounded_local_run`
- Challenge report source principal: `challenge_report_2026_04_20_kd_r02.md`
- Surface relue pour arbitrage:
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/run_context.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/scope_manifest.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/impact_bundle.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/integration_gate.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/work/01_challenge/challenge_report_2026_04_20_kd_r02.md`
  - lecture de fallback explicitement reprise : `docs/cores/current/link.yaml`
- Notes humaines d’arbitrage reçues : aucune.

## detailed_arbitrage_by_finding

### AF1 — Cohérence locale du cœur knowledge_and_design
- `challenge_finding_id`: `CF1_LOCAL_COHERENCE`
- `challenge_scope_status`: `in_scope`
- `arbitrage_decision`: `rejeter`
- `arbitrage_justification`: Le challenge ne signale pas ici un écart à corriger mais un constat positif : le noyau local du scope est cohérent et gouverné correctement. Il n’y a donc pas de correction à lancer en STAGE_03 sur ce point.
- `patch_readiness`: `decision_only_no_patch_yet`
- `related_gate_checks`:
  - `WP_01`
  - `WP_03`
  - `WP_04`
  - `WP_05`
- `gate_effect`: `helps_clear`
- `notes`: La bonne séparation entre structure du graphe, design et garde-fous de feedback est considérée comme confirmée localement.

### AF2 — Drift d’identifiants / versions inter-Core entre impact bundle et LINK courant
- `challenge_finding_id`: `CF2_INTERCORE_REF_DRIFT`
- `challenge_scope_status`: `out_of_scope_but_relevant`
- `arbitrage_decision`: `necessite_extension_scope`
- `arbitrage_justification`: Le problème est réel et prioritaire, mais il ne doit pas être corrigé par un patch local aveugle dans ce run. Le run attend un ID voisin historique alors que le `LINK` courant expose une autre convention de nommage/version. Corriger ce point exige une décision d’architecture sur l’ancre canonique attendue et potentiellement une régénération du scope catalog ou l’introduction d’un alias de compatibilité.
- `patch_readiness`: `blocked_by_missing_human_decision`
- `related_gate_checks`:
  - `WP_02`
  - `FORBIDDEN_OPS_ENFORCEMENT`
- `gate_effect`: `requires_human_clearance`
- `ambiguity_declared`: true
- `options_presented`:
  - `Option A`: réaligner `impact_bundle` / voisinage sur les IDs `LINK_REF_CORE_*` actuellement canoniques.
  - `Option B`: conserver l’ID attendu par le run et introduire un alias / binding de compatibilité explicite dans le système.
- `conservative_default_identified`: `Ne rien patcher localement avant décision humaine explicite sur l’ancre inter-Core canonique.`
- `human_decision_required_flag`: true

### AF3 — Dépendance implicite hors surface sur INV_NO_RUNTIME_CONTENT_GENERATION
- `challenge_finding_id`: `CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY`
- `challenge_scope_status`: `needs_scope_extension`
- `arbitrage_decision`: `necessite_extension_scope`
- `arbitrage_justification`: La dépendance est suffisamment structurante pour ne pas être traitée comme détail documentaire. Elle touche l’autosuffisance du scope en mode borné. Deux voies sont plausibles : étendre le voisinage/impact bundle pour rendre l’invariant lisible, ou reconnaître explicitement que cette contrainte dépend d’un socle hors-scope assumé. Ce choix doit être arbitré avant patch synthesis sur ce point.
- `patch_readiness`: `blocked_by_missing_human_decision`
- `related_gate_checks`:
  - `WP_04`
  - `FORBIDDEN_OPS_ENFORCEMENT`
- `gate_effect`: `keeps_open`
- `ambiguity_declared`: true
- `options_presented`:
  - `Option A`: enrichir le voisinage borné pour inclure `INV_NO_RUNTIME_CONTENT_GENERATION`.
  - `Option B`: garder l’invariant hors-scope mais documenter explicitement cette dépendance comme hypothèse gouvernée du périmètre.
- `conservative_default_identified`: `Aucune synthèse de patch sur ce point avant décision humaine.`
- `human_decision_required_flag`: true

### AF4 — Frontière design / runtime / graphe à sanctuariser
- `challenge_finding_id`: `CF4_SCOPE_BOUNDARY_SANCTUARIZATION`
- `challenge_scope_status`: `in_scope`
- `arbitrage_decision`: `reporter`
- `arbitrage_justification`: Le challenge ne démontre pas d’erreur actuelle, mais une zone de fragilité future. Il n’y a pas de correction minimale évidente à synthétiser immédiatement. Le bon arbitrage est de préserver explicitement cette frontière dans le raisonnement de patch futur et dans les watchpoints, sans modification locale immédiate.
- `patch_readiness`: `decision_only_no_patch_yet`
- `related_gate_checks`:
  - `WP_01`
  - `WP_02`
  - `WP_03`
  - `WP_04`
  - `WP_05`
- `gate_effect`: `keeps_open`
- `human_decision_required_flag`: false

### AF5 — Lecture voisine prescrite mais sous-spécifiée en mode borné
- `challenge_finding_id`: `CF5_NEIGHBOR_READ_UNDERSPECIFIED`
- `challenge_scope_status`: `out_of_scope_but_relevant`
- `arbitrage_decision`: `necessite_extension_scope`
- `arbitrage_justification`: Le run déclare un devoir de lecture vers `referentiel.yaml` et `link.yaml`, mais n’apporte matériellement qu’un unique ID voisin non résolu. Cette sous-spécification ne bloque pas la lecture locale du scope, mais rend le mécanisme borné fragile et peu reproductible. Cela relève d’une révision de partition / génération de scope plutôt que d’un patch local.
- `patch_readiness`: `blocked_by_scope_extension`
- `related_gate_checks`:
  - `WP_02`
  - `FORBIDDEN_OPS_ENFORCEMENT`
- `gate_effect`: `keeps_open`
- `human_decision_required_flag`: false

## consolidated_points

- Tous les risques prioritaires du challenge ont été consommés explicitement.
- Aucun risque majeur n’est omis.
- La cohérence locale du scope est retenue comme un acquis.
- Les deux écarts P1 sont arbitré comme non patchables localement sans extension de scope ou décision humaine.
- Le drift inter-Core et la dépendance implicite hors surface sont traités comme problèmes gouvernants, pas comme simples défauts rédactionnels.

## decisions_for_patch

Aucun item n’est actuellement `ready_for_local_patch` sans risque de correction hors périmètre ou de décision silencieuse d’architecture.

Conséquence pour STAGE_03_PATCH_SYNTHESIS :
- **ne pas synthétiser de patch** sur `CF2_INTERCORE_REF_DRIFT`, `CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY` ni `CF5_NEIGHBOR_READ_UNDERSPECIFIED` tant qu’une décision humaine explicite n’a pas été fournie ;
- il n’existe pas, à ce stade, de correction locale minimale et sûre déjà arbitrée qui justifierait un patch YAML autonome.

## decisions_not_retained

- Décision non retenue : `corriger_maintenant` pour le drift inter-Core.
  - Motif : plusieurs solutions architecturales plausibles subsistent ; trancher sans validation humaine serait contraire au contrat.

- Décision non retenue : `corriger_maintenant` pour la dépendance à `INV_NO_RUNTIME_CONTENT_GENERATION`.
  - Motif : la correction dépend du choix de frontière de scope et du voisinage canonique attendu.

- Décision non retenue : `hors_perimetre` pur et simple sur les écarts P1.
  - Motif : ils dépassent le patch local, mais restent matériellement importants pour le système et doivent être tracés.

## governance_backlog_candidates

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_KD_R02_INTERCORE_REF_ALIGNMENT
    backlog_entry_type: scope_extension_needed
    title: Aligner la référence inter-Core attendue par knowledge_and_design avec le LINK courant
    related_scope_keys:
      - knowledge_and_design
    originating_run_id: CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02
    source_finding_id: CF2_INTERCORE_REF_DRIFT
    rationale: >-
      Le run borné attend l'identifiant REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION,
      alors que le LINK courant expose une convention LINK_REF_CORE_* alignée sur les versions
      actuelles. La remise en cohérence dépasse le patch local du run et requiert un arbitrage
      sur l'ancre canonique ou un mécanisme explicite de compatibilité.
    recommended_stage00_action: >-
      Réévaluer la policy/decisions de génération de scopes et la convention canonique
      de références inter-Core afin de régénérer un voisinage borné cohérent.
    candidate_status: candidate_open

  - candidate_id: GBC_KD_R02_RUNTIME_CONTENT_DEPENDENCY_SURFACING
    backlog_entry_type: scope_gap
    title: Rendre explicite dans le périmètre borné la dépendance à INV_NO_RUNTIME_CONTENT_GENERATION
    related_scope_keys:
      - knowledge_and_design
    originating_run_id: CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02
    source_finding_id: CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY
    rationale: >-
      CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION dépend d'un invariant non présent dans la surface
      bornée lue par le run. Cette dépendance implicite fragilise l'autosuffisance du scope.
    recommended_stage00_action: >-
      Décider si l'invariant doit rejoindre le voisinage canonique de knowledge_and_design
      ou si la dépendance hors-scope doit être rendue explicitement gouvernée dans les artefacts.
    candidate_status: candidate_open

  - candidate_id: GBC_KD_R02_NEIGHBOR_READ_QUALITY
    backlog_entry_type: partition_angle_mort
    title: Renforcer la qualité de lecture voisine du scope knowledge_and_design en mode borné
    related_scope_keys:
      - knowledge_and_design
    originating_run_id: CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02
    source_finding_id: CF5_NEIGHBOR_READ_UNDERSPECIFIED
    rationale: >-
      Le run déclare un devoir de lecture voisin sur referentiel.yaml et link.yaml, mais ne fournit
      qu'un unique identifiant voisin non résolu. La granularité du voisinage borné apparaît
      insuffisante pour une fermeture inter-Core robuste.
    recommended_stage00_action: >-
      Réexaminer les cross-scope edges et les mandatory_reads du scope afin de publier un voisinage
      borné plus exploitable et moins dépendant des fallbacks opportunistes.
    candidate_status: candidate_open
```

## deferred_or_blocked_decisions

- `CF2_INTERCORE_REF_DRIFT` — bloqué par décision humaine sur l’ancre canonique inter-Core.
- `CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY` — bloqué par décision humaine sur la frontière de scope / voisinage.
- `CF5_NEIGHBOR_READ_UNDERSPECIFIED` — différé vers révision de partition / scope generation.

## ambiguities_requiring_human_decision

### Ambiguïté A1 — référence inter-Core canonique attendue pour knowledge_and_design
- Pourquoi c’est matériel : ce choix conditionne la validité de tout patch futur touchant aux lectures voisines ou aux bindings inter-Core.
- Options raisonnables :
  1. réaligner les artefacts bornés sur les IDs `LINK_REF_CORE_*` actuels ;
  2. conserver l’ancienne ancre et introduire une compatibilité explicite.
- Défaut conservateur proposé : **ne rien patcher localement tant que l’option n’est pas choisie**.
- Décision humaine requise : **oui**.

### Ambiguïté A2 — statut canonique de la dépendance à INV_NO_RUNTIME_CONTENT_GENERATION
- Pourquoi c’est matériel : ce choix détermine si l’autosuffisance bornée du scope doit être renforcée par extension de voisinage ou assumée comme dépendance externe gouvernée.
- Options raisonnables :
  1. ajouter cet invariant au voisinage / impact bundle du scope ;
  2. laisser l’invariant hors scope mais documenter explicitement la dépendance.
- Défaut conservateur proposé : **bloquer tout patch local sur ce point avant décision humaine**.
- Décision humaine requise : **oui**.

## human_actions_to_execute

1. Relire et valider cet arbitrage_report.
2. Arbitrer explicitement les ambiguïtés A1 et A2 avant tout passage à STAGE_03 sur les points concernés.
3. Si tu veux une révision de l’arbitrage avec ta décision, relance avec :

```text
Révise l'arbitrage du run CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02 — décision humaine sur ambiguïtés : <tes notes>.
```

4. Tant qu’aucune décision humaine n’est fournie sur A1 et A2, **ne pas exécuter** la transition vers `STAGE_03_PATCH_SYNTHESIS` pour ces findings.
5. Préserver les `governance_backlog_candidates` ci-dessus pour export canonique en STAGE_09.
