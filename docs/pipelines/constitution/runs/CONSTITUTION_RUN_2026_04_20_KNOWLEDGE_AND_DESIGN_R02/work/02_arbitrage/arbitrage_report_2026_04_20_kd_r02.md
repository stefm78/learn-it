# STAGE_02_ARBITRAGE — arbitrage_report_2026_04_20_kd_r02

## executive_summary

Le challenge du scope `knowledge_and_design` confirme une bonne cohérence locale du périmètre, mais fait ressortir deux écarts structurants :

1. un drift d’identifiants / de version entre le voisin attendu par le run (`REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`) et le `LINK` courant, qui expose des références `LINK_REF_CORE_LEARNIT_CONSTITUTION_V4_0` et `LINK_REF_CORE_LEARNIT_REFERENTIEL_v3.0` ;
2. une dépendance implicite hors surface entre `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION` et `INV_NO_RUNTIME_CONTENT_GENERATION`, absente du périmètre de lecture borné.

Décision humaine intégrée :
- sur le point 1, la direction retenue est **l’alignement sur la convention actuelle du `LINK`** ;
- sur le point 2, le constat est traité comme **sujet de backlog / redécoupage de scope**, et non comme patch local immédiat.

Conséquence :
- le point 1 devient **corrigeable maintenant** en synthèse de patch locale, dans le sens d’un réalignement vers les références inter-Core actuelles ;
- le point 2 reste un **signal gouvernant** à préserver pour backlog et révision de partition, sans patch local dans ce run ;
- la cohérence locale du cœur `knowledge_and_design` reste retenue comme validée, sans action de patch directe.

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
- Notes humaines d’arbitrage intégrées :
  - `A1 = aligner sur les références inter-Core actuelles du LINK`
  - `A2 = backlog / redécoupage de scope, pas de patch local`

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
- `arbitrage_decision`: `corriger_maintenant`
- `arbitrage_justification`: Décision humaine explicite reçue : la convention canonique à suivre est la convention actuelle du `LINK`. Le correctif à synthétiser doit donc viser l’alignement des artefacts bornés et/ou des références attendues sur les identifiants inter-Core actuellement publiés, et non la conservation de l’ancre historique.
- `patch_readiness`: `ready_for_local_patch`
- `related_gate_checks`:
  - `WP_02`
  - `FORBIDDEN_OPS_ENFORCEMENT`
- `gate_effect`: `helps_clear`
- `ambiguity_declared`: false
- `human_decision_required_flag`: false
- `notes`: Le patch futur doit rester minimal et borné : il s’agit d’un réalignement sur la convention actuelle, pas d’une réécriture libre de la logique inter-Core.

### AF3 — Dépendance implicite hors surface sur INV_NO_RUNTIME_CONTENT_GENERATION
- `challenge_finding_id`: `CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY`
- `challenge_scope_status`: `needs_scope_extension`
- `arbitrage_decision`: `reporter`
- `arbitrage_justification`: Décision humaine explicite reçue : ce point n’est pas à corriger par patch local immédiat. Il révèle un sujet de découpage / autosuffisance du scope borné et doit être traité comme backlog de gouvernance, potentiellement lors d’un redécoupage de scope ou d’une révision de partition.
- `patch_readiness`: `decision_only_no_patch_yet`
- `related_gate_checks`:
  - `WP_04`
  - `FORBIDDEN_OPS_ENFORCEMENT`
- `gate_effect`: `keeps_open`
- `ambiguity_declared`: false
- `human_decision_required_flag`: false
- `notes`: Pas de patch local sur ce point dans ce run ; conserver une trace backlog candidate.

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
- Le drift inter-Core est désormais orienté vers une correction locale ciblée, sur décision humaine explicite.
- La dépendance implicite hors surface est confirmée comme sujet de backlog / redécoupage de scope, sans patch local.
- Le manque de qualité de lecture voisine reste un sujet de gouvernance de partition.

## decisions_for_patch

Les décisions suivantes sont retenues pour STAGE_03_PATCH_SYNTHESIS :

- `CF2_INTERCORE_REF_DRIFT` : **ready_for_local_patch**
  - direction imposée : réaligner les références attendues par le scope / run sur la convention inter-Core actuelle exposée par le `LINK`.
  - contrainte : rester minimal, explicite et borné.

Les décisions suivantes **ne doivent pas** produire de patch local dans ce run :

- `CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY`
- `CF4_SCOPE_BOUNDARY_SANCTUARIZATION`
- `CF5_NEIGHBOR_READ_UNDERSPECIFIED`

## decisions_not_retained

- Décision non retenue : conserver l’ancre historique via alias / compatibilité comme option par défaut pour `CF2_INTERCORE_REF_DRIFT`.
  - Motif : décision humaine explicite en faveur de l’alignement sur la convention actuelle.

- Décision non retenue : `corriger_maintenant` pour `CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY`.
  - Motif : le point est requalifié comme backlog / redécoupage de scope, pas comme patch local.

- Décision non retenue : `hors_perimetre` pur et simple sur les écarts structurants.
  - Motif : ils dépassent partiellement le patch local, mais restent matériellement importants pour le système et doivent être tracés.

## governance_backlog_candidates

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_KD_R02_RUNTIME_CONTENT_DEPENDENCY_SURFACING
    backlog_entry_type: scope_gap
    title: Rendre explicite dans le périmètre borné la dépendance à INV_NO_RUNTIME_CONTENT_GENERATION
    related_scope_keys:
      - knowledge_and_design
    originating_run_id: CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02
    source_finding_id: CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY
    rationale: >-
      CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION dépend d'un invariant non présent dans la surface
      bornée lue par le run. Cette dépendance implicite fragilise l'autosuffisance du scope
      et pointe vers un possible redécoupage ou enrichissement de voisinage.
    recommended_stage00_action: >-
      Réexaminer la partition du scope knowledge_and_design pour décider si cet invariant doit
      rejoindre le voisinage canonique ou rester hors-scope mais explicitement gouverné.
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

- `CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY` — reporté vers backlog / redécoupage de scope.
- `CF5_NEIGHBOR_READ_UNDERSPECIFIED` — différé vers révision de partition / scope generation.
- `CF4_SCOPE_BOUNDARY_SANCTUARIZATION` — conservé comme vigilance d’architecture, sans patch immédiat.

## ambiguities_requiring_human_decision

Aucune ambiguïté matérielle restante n’empêche STAGE_03 sur le finding `CF2_INTERCORE_REF_DRIFT`.

Le point `CF3_IMPLICIT_RUNTIME_CONTENT_DEPENDENCY` a été explicitement requalifié comme backlog de gouvernance / redécoupage de scope ; il ne bloque donc plus la synthèse de patch, puisqu’il ne doit pas produire de patch local.

## human_actions_to_execute

1. Relire et valider cet arbitrage_report révisé.
2. Si tu le valides, mettre à jour le tracking :

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02 \
  --stage-id STAGE_02_ARBITRAGE \
  --stage-status done \
  --run-status active \
  --next-stage STAGE_03_PATCH_SYNTHESIS \
  --summary "Arbitrage report revised with human decisions; ready for patch synthesis."
```

3. Après exécution confirmée, relancer avec :

```text
Continue le run CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02 — STAGE_02 est done, démarre STAGE_03_PATCH_SYNTHESIS.
```

4. Préserver les `governance_backlog_candidates` ci-dessus pour export canonique en STAGE_09.
