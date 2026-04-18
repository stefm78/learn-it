# ARBITRAGE — Constitution pipeline

```yaml
stage: STAGE_02_ARBITRAGE
pipeline: constitution
run_id: CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01
mode: bounded_local_run
date: 2026-04-18
primary_inputs:
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/run_context.yaml
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/scope_manifest.yaml
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/impact_bundle.yaml
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/integration_gate.yaml
supporting_reads:
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/scope_extract.yaml
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/neighbor_extract.yaml
fallback_reads:
  - docs/cores/current/constitution.yaml
  - docs/cores/current/referentiel.yaml
human_arbitrage_notes: none
simulated_scripts: none
traceability_note: >-
  Le challenge_report de STAGE_01 n'a pas pu être relu directement via le connecteur
  dans cette exécution. L'arbitrage ci-dessous est donc reconstruit de manière
  conservatrice à partir de la surface runtime autorisée, de la règle de fallback
  déclenchée par neighbor_extract, du Core canonique courant et de la trace de stage
  déjà présente dans run_manifest. Aucun nouveau finding hors de cette surface n'est
  introduit.
```

---

## Executive summary

Arbitrage borné sur le scope `deployment_governance`.

Décision consolidée :

- **corriger_maintenant** : 3 points
- **reporter** : 0 point
- **rejeter** : 0 point
- **hors_perimetre** : 0 point
- **necessite_extension_scope** : 1 point

Les trois corrections locales retenues sont compatibles avec le périmètre modifiable du run et visent à :

1. expliciter la frontière entre contraintes runtime locales et logique pédagogique ;
2. renforcer la séparation Constitution/Référentiel et le statut non adaptatif des régimes d’autonomie ;
3. isoler les règles top-level de gouvernance (GF-08, probation gamification) du patch_lifecycle.

Le quatrième point ne relève pas d’un patch local de contenu : l’input du run attend encore l’ancre voisine `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`, alors que le Core canonique courant matérialise déjà `REF_CORE_LEARNIT_REFERENTIEL_V3_0_IN_CONSTITUTION`. Ce décalage doit être traité comme un problème de scope generation / partition / input materialization, pas comme une correction silencieuse de contenu dans ce run.

---

## Scope analysed

### Surface effectivement analysée

- `run_context.yaml`
- `scope_manifest.yaml`
- `impact_bundle.yaml`
- `integration_gate.yaml`
- `scope_extract.yaml`
- `neighbor_extract.yaml`
- fallback ciblé sur `constitution.yaml` et `referentiel.yaml`

### Périmètre modifiable autorisé

- fichier autorisé : `docs/cores/current/constitution.yaml`
- modules autorisés : `deployment`, `runtime_architecture`, `runtime_governance`, `governance`, `initialization`, `system`
- IDs autorisés : 19 IDs explicitement listés dans `writable_perimeter.ids`

### Contraintes de scope appliquées

- aucune correction silencieuse hors scope
- l’impact bundle étend la lecture, pas le droit d’écriture
- aucune génération de patch YAML
- aucune réécriture complète des Core
- aucun write direct sur le Référentiel

### Fallback déclenché

`neighbor_extract.yaml` signale explicitement l’ID manquant `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`. Le fallback autorisé sur les Core complets a donc été appliqué. La lecture canonique montre que la Constitution courante dépend déjà de `REF_CORE_LEARNIT_REFERENTIEL_V3_0_IN_CONSTITUTION`, ce qui transforme le point en anomalie de synchronisation des inputs du run plutôt qu’en absence simple de référence inter-Core.

---

## Detailed arbitrage by finding

### R1 — frontière runtime local / logique pédagogique

```yaml
challenge_finding_id: R1
challenge_scope_status: in_scope
arbitrage_decision: corriger_maintenant
patch_readiness: ready_for_local_patch
related_gate_checks:
  - WP_01
gate_effect: helps_clear
arbitrage_justification: >-
  Les invariants runtime locaux et la qualification explicite des signaux sont déjà
  dans le périmètre autorisé. Une clarification locale dans la Constitution suffit,
  sans réallocation inter-Core ni extension de scope.
```

Constat consolidé : les contraintes `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION` et `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` doivent rester des contraintes d’architecture/runtime. Elles ne doivent pas glisser vers une logique pédagogique implicite ni servir de fondement à une adaptation interprétative.

Décision : **corriger_maintenant**.

Effet attendu pour STAGE_03 : synthétiser une correction minimale rappelant que la localité, l’absence de génération runtime et l’exigence de signaux explicites/off-session bornent l’architecture d’exécution et ne valent pas règles pédagogiques autonomes.

---

### R2 — séparation Constitution/Référentiel et statut des régimes d’autonomie

```yaml
challenge_finding_id: R2
challenge_scope_status: in_scope
arbitrage_decision: corriger_maintenant
patch_readiness: ready_for_local_patch
related_gate_checks:
  - WP_02
  - WP_03
  - WP_05
gate_effect: helps_clear
arbitrage_justification: >-
  Le point relève directement du périmètre writable du run : gouvernance,
  runtime_governance, system, séparation Constitution/Référentiel et types
  d’autonomie. Une correction locale peut renforcer la frontière d’autorité sans
  déplacer de logique vers le Référentiel.
```

Constat consolidé : le gate exige simultanément une séparation inviolable Constitution/Référentiel, le maintien des régimes d’autonomie comme configurations gouvernées et l’absence de confusion entre invariant constitutionnel et paramètre référentiel.

Décision : **corriger_maintenant**.

Effet attendu pour STAGE_03 : renforcer une formulation locale rappelant que :

- les régimes d’autonomie restent des configurations gouvernées ;
- ils ne peuvent pas devenir des règles adaptatives implicites ;
- la logique AND et la propagation graphe restent explicitement hors de portée du chantier.

---

### R3 — isolement de GF-08 et de la probation gamification vis-à-vis du patch_lifecycle

```yaml
challenge_finding_id: R3
challenge_scope_status: in_scope
arbitrage_decision: corriger_maintenant
patch_readiness: ready_for_local_patch
related_gate_checks:
  - WP_04
gate_effect: helps_clear
arbitrage_justification: >-
  Les événements et règles concernés sont tous in-scope. Le besoin consiste à
  verrouiller une frontière de gouvernance entre supervision top-level et lifecycle
  de patch, sans aucune opération interdite.
```

Constat consolidé : `RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE`, `RULE_UNVERIFIED_GAMIFICATION_PROBATION`, `RULE_GAMIFICATION_PROBATION_MUST_CLOSE` et les événements associés ne doivent jamais valoir mécanisme implicite de patch, de promotion ou de réallocation inter-Core.

Décision : **corriger_maintenant**.

Effet attendu pour STAGE_03 : produire une formulation minimale indiquant que GF-08 et la probation gamification peuvent imposer une réponse conservatrice, une clôture ou une information explicite, mais ne constituent ni un patch implicite, ni une validation de promotion, ni une autorisation de changement structurel.

---

### R4 — décalage entre l’ancre voisine demandée par le run et l’ancre inter-Core canonique courante

```yaml
challenge_finding_id: R4
challenge_scope_status: needs_scope_extension
arbitrage_decision: necessite_extension_scope
patch_readiness: blocked_by_scope_extension
related_gate_checks:
  - WP_02
  - FORBIDDEN_OPS_ENFORCEMENT
gate_effect: requires_human_clearance
arbitrage_justification: >-
  L’input du run et neighbor_extract ciblent REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION,
  absent du Core courant, tandis que la Constitution active dépend déjà de
  REF_CORE_LEARNIT_REFERENTIEL_V3_0_IN_CONSTITUTION. Le problème porte donc sur la
  génération du scope / partition / input bundle plutôt que sur une correction locale
  de contenu à appliquer silencieusement dans ce run.
```

Constat consolidé : ce point n’est pas une simple référence inter-Core manquante dans la Constitution. La référence explicite existe déjà côté Constitution, mais sous la version V3.0. L’anomalie porte sur la matérialisation du run, qui demande encore V2.0 dans `impact_bundle` / `neighbor_extract`.

Décision : **necessite_extension_scope**.

Effet attendu pour STAGE_03 : **aucun patch local** sur ce point. Le sujet doit être porté vers un ajustement de Stage 00 / scope catalog / partition refresh, avec re-matérialisation correcte des inputs du run.

---

## Consolidated points

### Regroupements retenus

- **Cluster A — runtime boundary** : R1 + WP_01 + invariants runtime locaux
- **Cluster B — authority boundary** : R2 + WP_02/WP_03/WP_05 + séparation Constitution/Référentiel + autonomie
- **Cluster C — top-level governance isolation** : R3 + WP_04 + GF-08 + probation gamification
- **Cluster D — stale inter-core run input** : R4 + neighbor_extract manquant + fallback canonique

### Point de tracking à garder visible

Le run présente une incohérence de tracking : `run_context.yaml` et `run_manifest.yaml` exposent `STAGE_02_ARBITRAGE` à la fois comme stage déjà complété et comme prochain stage exécutable. Cette incohérence n’empêche pas l’arbitrage de contenu, mais elle doit être traitée comme sujet de revue humaine avant toute transition de tracking supplémentaire.

---

## Decisions for patch

### Points transmis à STAGE_03_PATCH_SYNTHESIS


| Priorité | Finding | Décision            | Scope status | Patch readiness       | Surface visée                                                            |
| -------- | ------- | ------------------- | ------------ | --------------------- | ------------------------------------------------------------------------ |
| 1        | R2      | corriger_maintenant | in_scope     | ready_for_local_patch | `constitution.yaml` — gouvernance / séparation / autonomie               |
| 2        | R3      | corriger_maintenant | in_scope     | ready_for_local_patch | `constitution.yaml` — gouvernance top-level / probation / patch boundary |
| 3        | R1      | corriger_maintenant | in_scope     | ready_for_local_patch | `constitution.yaml` — runtime architecture / local boundary              |


### Contraintes de synthèse à respecter

- aucune correction silencieuse hors scope
- aucune écriture dans `referentiel.yaml`
- aucune réallocation implicite inter-Core
- aucun patch local pour R4
- formulations minimales, auditables, centrées sur la frontière d’autorité

---

## Decisions not retained


| Finding | Décision                  | Justification                                                                         |
| ------- | ------------------------- | ------------------------------------------------------------------------------------- |
| R4      | necessite_extension_scope | anomalie de génération d’inputs / scope catalog, non patchable localement dans ce run |


Aucun finding significatif n’est rejeté.

Aucun finding n’est classé `hors_perimetre` simple : R4 appelle une extension de scope / reprise de stage amont, pas un simple constat informatif.

---

## governance_backlog_candidates

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_R4_DEPLOYMENT_GOVERNANCE_REF_ALIGNMENT
    backlog_entry_type: scope_gap
    title: Aligner les inputs bornés deployment_governance sur l’ancre inter-Core Référentiel V3.0
    related_scope_keys:
      - deployment_governance
    originating_run_id: CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01
    source_finding_id: R4
    rationale: >-
      Le run matérialisé attend encore REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION
      dans impact_bundle / neighbor_extract, alors que le Core Constitution courant
      dépend déjà de REF_CORE_LEARNIT_REFERENTIEL_V3_0_IN_CONSTITUTION. Le problème
      porte sur la génération de la surface bornée et non sur l’absence d’une référence
      inter-Core dans le contenu canonique actuel.
    recommended_stage00_action: >-
      Rejouer la génération de partition / scope catalog / inputs bornés pour remplacer
      l’ancre voisine V2.0 par l’ancre canonique V3.0 et vérifier que les edges inter-Core
      et les fingerprints dérivés restent cohérents.
    candidate_status: candidate_open
```

---

## Deferred_or_blocked_decisions


| Finding | Statut  | Motif                                                                       | Suite attendue                                                   |
| ------- | ------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| R4      | blocked | correction hors surface locale de patch ; anomalie de génération des inputs | traiter en backlog de gouvernance / Stage 00 / partition refresh |


| Sujet transverse | Statut   | Motif                                                | Suite attendue                                        |
| ---------------- | -------- | ---------------------------------------------------- | ----------------------------------------------------- |
| tracking du run  | deferred | STAGE_02 déjà marqué done tout en restant next_stage | revue humaine du tracking avant transition ultérieure |


---

## Ambiguities_requiring_human_decision

### A1 — traçabilité directe du challenge_report indisponible dans cette exécution

- **Ambiguïté :** le `challenge_report` n’a pas pu être relu directement via le connecteur, alors que le contrat idéal du stage demande sa consommation explicite.
- **Portée affectée :** R1 à R4.
- **Option conservatrice retenue par défaut :** ne pas introduire de nouveau finding ; rester strictement dans la surface ids-first + fallback autorisé + trace de stage existante.
- **Human decision required flag :** `true`
- **Impact pratique :** la relecture humaine doit confirmer que la reconstruction R1–R4 couvre bien l’intégralité des arbitrages ouverts de STAGE_01 avant de lancer STAGE_03.

### A2 — nature exacte de R4

- **Ambiguïté :** R4 pourrait être décrit soit comme `scope_gap`, soit comme `orphan_id` de matérialisation.
- **Option conservatrice retenue par défaut :** `scope_gap`, car l’action correcte porte sur la régénération de la surface bornée plutôt que sur une simple suppression locale d’un identifiant.
- **Human decision required flag :** `false`
- **Impact pratique :** aucun impact sur STAGE_03 local, car dans tous les cas R4 reste non patchable dans ce run.

### A3 — incohérence de tracking

- **Ambiguïté :** STAGE_02 est à la fois déjà complété et encore prochain stage exécutable.
- **Option conservatrice retenue par défaut :** traiter le présent livrable comme une révision du contenu d’arbitrage, sans tirer de conclusion implicite sur le tracking.
- **Human decision required flag :** `true`
- **Impact pratique :** la validation humaine doit décider comment remettre le tracking dans un état cohérent avant ou pendant la transition vers STAGE_03.

---

## Human actions to execute

1. Relire et valider ce rapport d’arbitrage.
2. Confirmer explicitement que la reconstruction R1–R4 couvre bien les arbitrages ouverts du challenge report source.
3. Décider du traitement du tracking incohérent avant mise à jour de stage.
4. Si validation obtenue, mettre à jour le tracking :

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01 \
  --stage-id STAGE_02_ARBITRAGE \
  --stage-status done \
  --run-status active \
  --next-stage STAGE_03_PATCH_SYNTHESIS \
  --summary "Arbitrage report validated; decisions ready for patch synthesis."
```

5. Ne pas démarrer STAGE_03 tant que la validation humaine sur la traçabilité et le tracking n’est pas explicitement posée.