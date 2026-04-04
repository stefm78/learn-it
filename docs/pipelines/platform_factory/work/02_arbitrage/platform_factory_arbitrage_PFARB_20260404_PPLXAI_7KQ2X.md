# Platform Factory — Arbitrage STAGE_02

- **arbitrage_run_id**: `PFARB_20260404_PPLXAI_7KQ2X`
- **date**: 2026-04-04
- **pipeline**: `docs/pipelines/platform_factory/pipeline.md`
- **stage**: `STAGE_02_FACTORY_ARBITRAGE`

## Challenge reports considérés

Tous les challenge reports présents dans `work/01_challenge/` ont été pris en compte :

1. `challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md`
2. `challenge_report_PFCHAL_20260404_PERPLX_7K2R.md`
3. `challenge_report_PFCHAL_20260404_PERPLX_A1J77P.md`
4. `challenge_report_PFCHAL_20260404_PERP_K7X2.md`
5. `challenge_report_PFCHAL_20260404_PPLXAI_5LVBSV.md`
6. `challenge_report_PFCHAL_20260404_PXADV_BB1MZX.md`

Les six rapports convergent sur une lecture « baseline V0 conceptuellement solide mais incomplète », avec des risques prioritaires concentrés sur :
- la non‑propagation explicite des invariants constitutionnels dans le contrat minimal d’application produite ;
- le caractère non outillé des `validated_derived_execution_projections` ;
- la gouvernance release/manifest incomplète pour les artefacts `platform_factory` ;
- la multi‑IA traitée comme exigence de premier rang mais encore non opérationnelle ;
- l’absence de schémas fins (manifest, configuration, packaging, runtime) et de validators dédiés ;
- quelques cas de maturité sur‑déclarée dans `platform_factory_state.yaml`.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8][cite:9][cite:10]

---

## Résumé exécutif d’arbitrage

1. **La baseline V0 de Platform Factory est confirmée comme base de travail légitime pour poursuivre le pipeline** (challenge → arbitrage → patch), et ne doit pas être réécrite.
2. **Trois familles de risques sont arbitrées comme critiques et à traiter avant tout usage fort de la factory** :
   - la non‑projection des invariants constitutionnels runtime dans le contrat minimal d’application produite ;
   - l’usage autorisé des projections dérivées validées sans stockage, validator ni protocole de régénération ;
   - l’ambiguïté de statut des artefacts `platform_factory_*` placés dans `docs/cores/current/` mais hors manifest officiel.
3. **Deux familles de risques sont arbitrées comme élevées mais traitables dans le même cycle de patch** :
   - l’absence de protocole multi‑IA (décomposition, assemblage, résolution de conflits) ;
   - l’absence de schémas fins (manifest, configuration, packaging, runtime) et de critères de maturité explicites.
4. **Les schémas fins complets ne sont pas exigés en V0**, mais un « sous‑ensemble minimal d’auditabilité » doit être défini pour rendre les validators et la multi‑IA raisonnablement opérables.
5. **Aucun challenge report n’est rejeté sur le fond** ; les différences portent principalement sur la granularité et la sévérité, qui sont réconciliées dans la grille de décisions ci‑dessous.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8]

---

## Synthèse des constats convergents

### 1. Contrat minimal d’application produite

**Constat convergent :** tous les rapports soulignent que `produced_application_minimum_contract` ne rend pas auditables les invariants runtime essentiels :
- runtime 100 % local ;
- absence de génération de contenu ou de feedback runtime hors templates autorisés ;
- patchs pré‑calculés hors session ;
- absence d’état de patch partiel ;
- validation locale déterministe.[cite:3][cite:4][cite:5][cite:7][cite:8]

**Verdict d’arbitrage :** défaut **critique** de complétude contractuelle au niveau factory, à corriger dans l’architecture avant d’exposer la factory comme couche de production sûre.

### 2. Projections d’exécution dérivées

**Constat convergent :** le mécanisme est conceptuellement bien posé mais opérationnellement ouvert : pas de validator, pas de protocole de régénération deterministe, emplacement TBD, aucune invalidation automatique après patch du socle.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8]

**Verdict d’arbitrage :** capacité **fondatrice mais non outillée**. L’usage comme « unique artefact fourni à une IA » est arbitré comme **interdit tant que le minimum de garde‑fous n’est pas posé**.

### 3. Gouvernance release / manifest

**Constat convergent :** `platform_factory_architecture.yaml` et `platform_factory_state.yaml` sont dans `docs/cores/current/` mais hors manifest officiel, avec un blocker explicite dans le state. La posture « baseline released » du pipeline n’est pas matérialisée par un artefact de release ou une intégration manifest.

**Verdict d’arbitrage :** **trou de gouvernance à fermer** : il faut soit intégrer `platform_factory` dans le manifest officiel, soit définir un mécanisme de manifest compagnon, soit documenter un régime transitoire explicite pour V0.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8][cite:9]

### 4. Multi‑IA en parallèle

**Constat convergent :** l’exigence multi‑IA est correctement posée comme décision de premier rang, mais les briques opérationnelles clés manquent (protocoles de décomposition, d’assemblage, de résolution de conflit, granularité modulaire, format homogène de reports).

**Verdict d’arbitrage :** capacité multi‑IA **déclarée mais non opérationnelle**. Elle doit rester assumée comme partielle dans le state et ne doit pas être sur‑vendue dans l’architecture ou le pipeline.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8]

### 5. Schémas fins, validators et pipeline

**Constat convergent :**
- manifest/config/packaging/runtime typology sont définis en intention mais sans schéma ;
- aucun validator factory n’est implémenté ;
- STAGE_07 et STAGE_08 délèguent à des specs dont l’existence n’est pas entièrement auditée ;
- STAGE_04 et STAGE_06 partagent le même prompt de validation ;
- STAGE_05 ne documente pas l’atomicité/rollback vis‑à‑vis de `INV_NO_PARTIAL_PATCH_STATE`.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8][cite:9]

**Verdict d’arbitrage :** acceptable en V0 comme squelette, **à condition** de fermer un noyau minimal : (i) protocoles de validation ciblant les points critiques, (ii) atomicité minimale de STAGE_05, (iii) clarification d’usage du prompt partagé STAGE_04/06.

### 6. Maturité et state

**Constat convergent :** certains points sont légerement sur‑déclarés en `capabilities_present` alors qu’ils ne disposent pas d’outillage (règle de projection, scope de factory, pipeline intent), et l’absence de critères de progression explicites rend difficile le pilotage V0→V0.x.[cite:4][cite:5][cite:6][cite:7][cite:8]

**Verdict d’arbitrage :** la posture du state reste honnête globalement, mais des reclassements précis et l’ajout de critères de sortie sont nécessaires pour éviter un faux sentiment de fermeture.

---

## Propositions d’arbitrage par thème

Chaque décision importante est identifiée par un ID `ARB-XX`.

### Thème A — Contrat minimal & invariants constitutionnels

#### ARB-01 — Ajouter un axe explicite de conformité runtime constitutionnelle

- **Sujet** : invariants `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION` non projetés dans `minimum_validation_contract`.
- **Sources** : GPT54, PERPLX_7K2R, PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now**.
- **Lieu principal** : `platform_factory_architecture.yaml` (contrat minimal d’application produite).
- **Lieux secondaires** : futurs validators factory (contrôle automatique), éventuellement pipeline STAGE_04/06 (hook de validation ciblé).
- **Proposition** :
  - Ajouter un axe `runtime_constitutional_compliance` dans `minimum_validation_contract.minimum_axes` couvrant au minimum : localité runtime, absence de génération de contenu/feedback runtime hors templates autorisés.
  - Exiger que le manifest d’une application produite expose une section `constitutional_invariant_conformance` qui référence explicitement les invariants applicables et leur statut.
- **Priorité** : **critique**.
- **Justification** : sans ce bloc, la factory peut certifier compatible une application qui viole des invariants centraux sans détection.

#### ARB-02 — Intégrer la gouvernance des patchs dans le contrat minimal

- **Sujet** : non‑projection de `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`, `INV_NO_PARTIAL_PATCH_STATE` dans le contrat minimal.
- **Sources** : GPT54, PERPLX_7K2R, PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now**.
- **Lieu principal** : architecture (contrat minimal, axes de validation, packaging).
- **Lieux secondaires** : pipeline STAGE_05 (atomicité), validators.
- **Proposition** :
  - Ajouter un axe `patch_governance_conformance` dans `minimum_validation_contract.minimum_axes` qui vérifie au minimum : pré‑computation hors session, validation locale déterministe de patch, absence d’état de patch partiel.
  - Clarifier dans le pipeline (STAGE_05) la règle d’atomicité/rollback alignée sur ces invariants.
- **Priorité** : **élevée**.
- **Justification** : ces invariants sont structurants pour la confiance dans toute application produite.

#### ARB-03 — Ne pas pousser les contraintes domaine‑spécifiques dans le contrat minimal V0

- **Sujet** : certaines suggestions frôlent la frontière entre contrat minimal générique et contraintes d’une future application instanciée (ex. détails très fins de packaging ou de qualification de graphe domaine).
- **Sources** : PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now mais borné**.
- **Lieu principal** : architecture (limiter le contrat minimal aux invariants génériques et à ce qui est nécessaire pour l’outillage factory).
- **Priorité** : **modérée**.
- **Justification** : ne pas sur‑normer la V0 ni absorber le pipeline d’instanciation ; garder une frontière nette factory/instanciation.

### Thème B — Projections dérivées

#### ARB-04 — Geler l’usage « artefact unique » tant que les garde‑fous manquent

- **Sujet** : le pipeline et l’architecture autorisent qu’une `validated_derived_execution_projection` soit l’unique contexte fourni à une IA, alors que validator, stockage et régénération deterministic font défaut.
- **Sources** : l’ensemble des rapports convergent sur ce risque.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now**.
- **Lieu principal** : architecture (`execution_projection_contract` + `generated_projection_rules`).
- **Lieux secondaires** : state (`derived_projection_conformity_status`), pipeline Rule 4, validators.
- **Proposition** :
  - Modifier l’architecture pour expliciter que l’usage "artefact unique pour IA" est **conditionnel** et **désactivé tant que** : (i) un validator dédié n’est pas défini, (ii) un emplacement stable n’est pas fermé, (iii) un protocole de régénération n’est pas décrit.
  - Répercuter dans le state le caractère **partial** de la capacité, avec un wording explicite.
- **Priorité** : **critique**.
- **Justification** : c’est un point de dérive normative silencieuse immédiate si des projections commencent à être utilisées en production.

#### ARB-05 — Décider et documenter l’emplacement cible des projections dérivées

- **Sujet** : `emplacement_policy.status: TBD` rend le mécanisme non utilisable de manière déterministe.
- **Sources** : PERPLX_7K2R, PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:4][cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now**.
- **Lieu principal** : architecture (choix de l’emplacement, ex. `docs/pipelines/platform_factory/projections/`).
- **Lieux secondaires** : state (capabilité correspondante), release/manifest governance si les projections deviennent des artefacts gouvernés.
- **Priorité** : **élevée**.
- **Justification** : sans emplacement stable, pas de versionning, pas d’assemblage multi‑IA robuste, pas de traçabilité.

#### ARB-06 — Préparer un validator minimal de projection dérivée

- **Sujet** : absence totale de validator alors que des invariants très fins sont déclarés.
- **Sources** : tous les rapports insistent sur le gap validator.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now**, mais limité à un **validator minimal V0.1**.
- **Lieu principal** : validator/tooling (hors architecture), avec ancrage conceptuel dans l’architecture.
- **Priorité** : **élevée**.
- **Justification** : même un validator partiel (par ex. vérification de présence des IDs d’invariants canonique + absence de mots‑clés interdits) réduit fortement les risques par rapport à l’absence totale de garde‑fou.

### Thème C — Gouvernance release / manifest

#### ARB-07 — Régulariser la présence des artefacts factory en `current/`

- **Sujet** : artefacts factory dans `docs/cores/current/` hors manifest officiel ; posture « released baseline » déclarative mais non matérialisée.
- **Sources** : tous les rapports soulignent ce trou de gouvernance.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8][cite:9]
- **Décision** : **retained_now**.
- **Lieu principal** : gouvernance manifest/release (hors YAML factory proprement dite).
- **Lieux secondaires** : state (`PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`), pipeline STAGE 07/08.
- **Proposition** :
  - Décider dans STAGE_07/08 d’un mécanisme explicite pour **intégrer** la factory au manifest officiel (extension de schéma) ou **créer un manifest compagnon** clairement référencé.
  - Tant que ce point n’est pas résolu, laisser le blocker en place avec wording renforcé sur le risque.
- **Priorité** : **critique**.
- **Justification** : la factory est déjà en `current/`; il faut clarifier rapidement si ce statut est formel ou transitoire.

#### ARB-08 — Matérialiser un artefact minimal de release V0

- **Sujet** : absence d’artefact de release formelle (tag, fichier de release, entrée dans un registre) pour la baseline V0.
- **Sources** : PERP_K7X2, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:6][cite:7][cite:8]
- **Décision** : **retained_now** mais réalisable à coût limité.
- **Lieu principal** : gouvernance release (par ex. petit fichier `docs/cores/releases/platform_factory_V0.yaml` ou équivalent).
- **Priorité** : **modérée**.
- **Justification** : utile pour la traçabilité, mais secondaire par rapport aux invariants runtime et aux projections.

### Thème D — Multi‑IA

#### ARB-09 — Reclasser la multi‑IA en capacité partielle et définir un protocole minimal

- **Sujet** : multi‑IA déclarée exigence de premier rang mais sans protocole d’assemblage, de granularité ou de résolution de conflit ; capacité parfois classée `present`.
- **Sources** : surtout PERPLX_7K2R, PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:4][cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now**.
- **Lieu principal** : state (reclassement en `capabilities_partial`, `blockers` plus explicites), architecture (section `multi_ia_parallel_readiness`).
- **Proposition** :
  - Documenter un **protocole minimal V0.1** : conventions sur les scopes, identifiants stables, point d’assemblage privilégié, règle simple de résolution de conflit (par ex. arbitrage humain obligatoire en cas de divergence sur un même ID).
- **Priorité** : **élevée** (mais sous les axes contract minimal & projections).

#### ARB-10 — Reporter la granularité optimale et l’assemblage avancé

- **Sujet** : granularité optimale des modules, protocoles avancés d’assemblage multi‑IA, etc.
- **Sources** : PERP_K7X2, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:6][cite:7][cite:8]
- **Décision** : **deferred**.
- **Lieu principal** : architecture / state (`deferred_challenges`).
- **Justification** : ces sujets sont importants mais peuvent rester explicitement déférés, une fois qu’un protocole minimal multi‑IA est en place.
- **Priorité** : **faible** à ce stade.

### Thème E — Pipeline & validators

#### ARB-11 — Clarifier STAGE_04 vs STAGE_06 et l’usage du prompt Make23

- **Sujet** : même prompt `Make23PlatformFactoryValidation.md` utilisé pour STAGE_04 (validation du patchset) et STAGE_06 (validation des artefacts patchés).
- **Sources** : PERPLX_7K2R, PERPLX_A1J77P, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:4][cite:5][cite:7][cite:8][cite:9]
- **Décision** : **retained_now**.
- **Lieu principal** : pipeline (`pipeline.md`) et éventuellement prompts.
- **Proposition** :
  - soit séparer en deux prompts (patch vs core) ;
  - soit documenter clairement dans Make23 les deux modes d’usage, avec paramètres différenciés.
- **Priorité** : **modérée**.

#### ARB-12 — Documenter l’atomicité de STAGE_05 vis‑à‑vis de `INV_NO_PARTIAL_PATCH_STATE`

- **Sujet** : STAGE_05 ne déclare pas de contrat d’atomicité/rollback pour l’application de patchs.
- **Sources** : PERPLX_7K2R, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:4][cite:7][cite:8][cite:9]
- **Décision** : **retained_now**.
- **Lieu principal** : pipeline STAGE_05 ; secondaire : documentation d’exécution.
- **Priorité** : **élevée** (liée aux invariants patch).

#### ARB-13 — Introduire un squelette de validators factory

- **Sujet** : aucun validator factory n’est implémenté, alors que plusieurs décisions supposent des checks systématiques.
- **Sources** : plusieurs rapports l’acceptent comme V0 mais le point revient comme préoccupation.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now** pour un jeu de validators minimal (projection, contrat minimal, release lineage).
- **Lieu principal** : validator/tooling (hors portées YAML canoniques).
- **Priorité** : **élevée**, mais avec un scope volontairement limité pour ce cycle.

#### ARB-14 — Lier challenge reports et runs de pipeline

- **Sujet** : STAGE_02 exige de considérer « tous les challenge_report*.md », sans lien clair avec un run_id ; risque de réutiliser des reports anciens.
- **Sources** : surtout PPLXAI_5LVBSV et PERPLX_7K2R.[cite:4][cite:7][cite:9]
- **Décision** : **retained_now**.
- **Lieu principal** : pipeline (`pipeline.md`), éventuellement convention de nommage des reports.
- **Priorité** : **modérée**.

### Thème F — State & maturité

#### ARB-15 — Reclasser certaines capabilities de `present` à `partial`

- **Sujet** : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`, `PF_CAPABILITY_FACTORY_SCOPE_DEFINED`, `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` parfois perçues comme sur‑déclarées.
- **Sources** : PERPLX_7K2R, PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:4][cite:5][cite:6][cite:7][cite:8]
- **Décision** : **retained_now**.
- **Lieu principal** : `platform_factory_state.yaml` (sections `capabilities_present`, `capabilities_partial`).
- **Priorité** : **modérée**.
- **Justification** : ajuster la perception de maturité sans changer la substance.

#### ARB-16 — Introduire des critères de sortie de maturité par couche

- **Sujet** : absence de `exit_criteria` ou de `next_maturity_target` dans le state.
- **Sources** : surtout PERP_K7X2 et PERPLX_A1J77P.[cite:5][cite:6]
- **Décision** : **retained_now** mais à granularité minimale.
- **Lieu principal** : state (`maturity_by_layer`).
- **Priorité** : **modérée**.

### Thème G — Divers

#### ARB-17 — Clarifier le contenu minimal de `reproducibility_fingerprints` et `bootstrap_contract`

- **Sujet** : blocs requis mais non définis.
- **Sources** : PERPLX_A1J77P, PPLXAI_5LVBSV, PXADV_BB1MZX.[cite:5][cite:7][cite:8]
- **Décision** : **clarification_required_before_patch**.
- **Lieu principal** : architecture.
- **Priorité** : **modérée**.

---

## Points retenus, rejetés, différés, hors périmètre

### Points retenus (sélection)

- **R1** : Compléter le contrat minimal avec un axe de conformité runtime constitutionnelle et un axe de gouvernance des patchs (ARB‑01, ARB‑02).
- **R2** : Geler l’usage fort des projections dérivées tant que validator, emplacement et régénération ne sont pas définis (ARB‑04 à ARB‑06).
- **R3** : Régulariser le statut manifest/release de `platform_factory` (ARB‑07, ARB‑08).
- **R4** : Documenter un protocole minimal multi‑IA et reclasser la capacité en partielle (ARB‑09).
- **R5** : Clarifier STAGE_04/06, STAGE_05, et introduire un socle de validators (ARB‑11 à ARB‑14).
- **R6** : Ajuster le state (capabilities, critères de maturité) (ARB‑15, ARB‑16).

### Points rejetés

Aucun finding n’est rejeté sur le fond.

Les seuls « rejets » concernent :
- des formulations trop fortes de certaines sévérités (certaines propositions de classer tout le mécanisme de projections comme bloquant la V0 sont **ramenées à « capacité non exploitable tant que non outillée »** plutôt qu’à « V0 invalide ») ;
- des suggestions qui poussaient trop loin la normalisation de détails domaine‑spécifiques dans le contrat minimal, reclassées comme **hors périmètre factory V0**.

### Points différés

- granularité optimale modulaire et protocoles multi‑IA avancés (ARB‑10) ;
- design complet des schémas manifest/config/packaging/runtime : un noyau minimal d’auditabilité est exigé maintenant, la complétude fine est déférée à un cycle ultérieur ;
- matérialisation d’un artefact de release plus riche (ex. changelog détaillé) : ARB‑08 se limite à un artefact minimal.

### Points hors périmètre factory

- details d’implémentation du futur pipeline d’instanciation d’application (sauf là où le contrat minimal est en cause) ;
- contraintes sur des graphes de connaissance domaine‑spécifiques (ex. acyclicity détaillée) qui relèvent des applications instanciées et non de la factory générique ;
- aspects purement organisationnels de gouvernance humaine hors repo.

---

## Points sans consensus ou nécessitant discussion finale

1. **Niveau de formalisme attendu pour le validator de projections dérivées en V0** : les rapports convergent sur le besoin, mais pas sur le niveau de sophistication minimal. Discussion finale requise pour calibrer un premier incrément.
2. **Stratégie exacte de régularisation des artefacts déjà en `current/`** : intégration directe au manifest vs manifest compagnon vs régime transitoire explicite ; plusieurs options sont ouvertes.
3. **Amplitude de la section `constitutional_invariant_conformance` dans le manifest d’application** : jusqu’où aller dans la granularité des invariants référencés sans sur‑charger V0.
4. **Découpage précis des responsabilités factory vs pipeline d’instanciation** autour de `bootstrap_contract` et des fingerprints de reproductibilité.

Ces sujets sont marqués **clarification_required_before_patch** là où ils conditionnent l’écriture des patchs.

---

## Corrections à arbitrer avant patch (vue synthétique)

### Corrections critiques

1. **C‑01 — Compléter le contrat minimal sur les invariants runtime et patch**  
   - Lieu principal : architecture (`produced_application_minimum_contract`).  
   - Décisions : ARB‑01, ARB‑02.  
   - Pré‑condition : arbitrer le niveau d’expressivité attendu dans le manifest.

2. **C‑02 — Geler l’usage fort des projections dérivées et fermer les garde‑fous minimaux**  
   - Lieu principal : architecture + state + pipeline (Rule 4) + validators.  
   - Décisions : ARB‑04, ARB‑05, ARB‑06.  
   - Pré‑condition : choix d’emplacement et spécification d’un validator minimal.

3. **C‑03 — Régulariser le statut manifest/release des artefacts factory**  
   - Lieu principal : manifest/release governance.  
   - Décision : ARB‑07.  
   - Pré‑condition : arbitrage humain sur la stratégie (extension manifest vs manifest compagnon).

### Corrections élevées

4. **C‑04 — Multi‑IA : protocole minimal et reclassement de maturité**  
   - Lieu : architecture + state (ARB‑09, ARB‑15).  
   - Impact : permettre un travail multi‑IA borné sans sur‑promettre.

5. **C‑05 — Pipeline : STAGE_05 atomicité + clarifications STAGE_04/06 + liaison reports/runs**  
   - Lieu : `pipeline.md` (ARB‑11, ARB‑12, ARB‑14).

6. **C‑06 — Introduire un petit socle de validators factory**  
   - Lieu : tooling (ARB‑06, ARB‑13).

### Corrections modérées

7. **C‑07 — Ajuster le state (capabilities, critères de maturité)**  
   - Lieu : `platform_factory_state.yaml` (ARB‑15, ARB‑16).

8. **C‑08 — Clarifier `reproducibility_fingerprints` et `bootstrap_contract`**  
   - Lieu : architecture (ARB‑17).  
   - Statut : clarification requise avant écriture du patch correspondant.

---

## Séquencement recommandé (vue haute)

1. **Étape 1 — Arbitrage humain ciblé**  
   - Valider les décisions critiques ARB‑01/02/04/05/07.  
   - Choisir la stratégie manifest/release (C‑03).  
   - Calibrer le niveau d’exigence du validator de projections dérivées.

2. **Étape 2 — Patch architecture & state**  
   - Intégrer les axes de validation manquants dans le contrat minimal.  
   - Encadrer l’usage des projections dérivées.  
   - Reclasser les capabilities et enrichir les critères de maturité.

3. **Étape 3 — Patch pipeline & gouvernance release**  
   - Mettre à jour `pipeline.md` sur STAGE_04/05/06/07/08 et la liaison des reports.  
   - Introduire un artefact minimal de release V0 et la stratégie manifest choisie.

4. **Étape 4 — Outillage minimal**  
   - Implémenter un validator minimal de projections.  
   - Poser un premier checker sur le contrat minimal (présence des blocs d’attestation constitutionnelle).

5. **Étape 5 — Re‑challenge ciblé**  
   - Lancer un STAGE_01_CHALLENGE focalisé sur les corrections critiques pour vérifier qu’aucune dérive normative n’a été introduite.

---

## Conclusion d’arbitrage

- La baseline V0 de Platform Factory est **confirmée comme fondation légitime**, en cohérence avec le socle canonique, mais **ne peut pas être utilisée comme dispositif de production sûrs d’applications** tant que les corrections critiques C‑01, C‑02 et C‑03 ne sont pas traitées.
- Les décisions ARB‑01 à ARB‑17 fournissent un cadre d’action borné pour STAGE_03_FACTORY_PATCH_SYNTHESIS, en préservant la séparation des couches (canonique / architecture / state / pipeline / outillage / release) et en préparant un noyau opérable multi‑IA.
