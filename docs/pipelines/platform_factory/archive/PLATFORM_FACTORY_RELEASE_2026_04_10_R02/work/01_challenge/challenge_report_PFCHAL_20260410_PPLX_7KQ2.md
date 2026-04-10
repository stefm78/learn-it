# Challenge Platform Factory Learn-it — baseline V0.3

challenge_run_id: PFCHAL_20260410_PPLX_7KQ2

Date: 2026-04-10

Artefacts challengés:
- docs/cores/current/constitution.yaml
- docs/cores/current/referentiel.yaml
- docs/cores/current/link.yaml
- docs/cores/current/platform_factory_architecture.yaml
- docs/cores/current/platform_factory_state.yaml
- docs/pipelines/platform_factory/pipeline.md

---

## Résumé exécutif

La baseline V0.3 de la Platform Factory pose correctement la séparation entre socle canonique, architecture prescriptive et état constatif, et reconnaît explicitement ses zones d’immaturité (schémas, validators, outillage pipeline, protocole multi‑IA).
La compatibilité avec les invariants constitutionnels critiques (localité du runtime, absence de génération de contenu et de feedback à la volée, patchs déterministes, séparation Constitution/Référentiel, traçabilité) est globalement respectée au niveau des principes, mais reste fragile tant que les validators et manifestes ne sont pas matérialisés.
Les validated_derived_execution_projections sont bien cadrées au niveau des invariants (fidélité stricte, non‑promotion en canonique, régénérabilité), mais le pipeline et le state laissent encore trop de latitude à des usages impropres (projections trop larges, absence de protocole de validation, usage comme unique contexte IA alors que `usage_as_sole_context` est encore bloqué).
Les principaux risques structurants portent sur (1) la capacité réelle de prouver la conformité constitutionnelle d’une application produite à partir de la seule factory, (2) la définition et l’outillage de la parallélisation multi‑IA, et (3) la fermeture de la chaîne release/manifest/traçabilité pour les artefacts de factory.

---

## Carte de compatibilité constitutionnelle

### Invariants explicitement repris ou bien alignés

- Localité runtime et absence de dépendance réseau temps réel : la factory renvoie explicitement au socle canonique comme autorité primaire et ne définit pas de mécanisme runtime propre, ce qui évite de contourner `INV_RUNTIME_FULLY_LOCAL` et les interdictions de génération en usage.
- Séparation Constitution/Référentiel et non‑duplication de norme : les principes `PF_PRINCIPLE_NO_NORM_DUPLICATION` et les dépendances explicites `dependencies_to_constitution`/`dependencies_to_referentiel` vont dans le sens de `INV_CONSTITUTION_REFERENTIAL_SEPARATION`.
- Patchs déterministes et pré‑computés hors session : la présence de contrats sur les projections dérivées (régénérables, validation‑gated, promotion interdite) et de règles de build/packaging limite le risque de patch implicite en usage.
- Traçabilité canonique : le contrat d’application produite impose des `reproducibility_fingerprints` et un manifest avec `canonical_dependencies`, ce qui donne une base solide pour tracer la conformité.

### Invariants couverts de façon implicite ou fragile

- Absence de génération de contenu/feedback runtime : l’architecture et le state ne rappellent pas explicitement les interdits de génération, laissant au futur pipeline d’instanciation le soin d’appliquer les invariants ; c’est acceptable en V0 mais doit être ancré dans le contrat minimal.
- Validation locale déterministe des patchs : les règles de patch sont surtout décrites au niveau du socle canonique ; la factory ne dit pas encore comment ses propres patchs ou projections seront validés concrètement (validators manquants, tooling absent).
- États partiels interdits lors de transformations : la factory reconnaît la nécessité de snapshots et de traceability, mais ne décrit pas encore comment éviter des états intermédiaires non valides pendant un run pipeline ou une promotion.

### Invariants exposés à des brèches potentielles

- Possibilité de fournir à une IA une projection dérivée qui perdrait une contrainte canonique, faute de validator dédié et de conformance matrix opérationnelle.
- Risque qu’une application produite paraisse conforme au contrat minimal tout en violant des invariants (par exemple sur le runtime local) si le manifest et les reports de validation ne sont pas assez contraints ou outillés.

---

## Analyse détaillée par axe

### Axe 1 — Compatibilité constitutionnelle

- La factory se lie explicitement à la Constitution, au Référentiel et au LINK comme sources normatives, et renvoie vers une `constitutional_conformance_matrix` dédiée ; c’est un point fort de design, mais la matrix reste documentaire tant que les validators ne sont pas matérialisés.
- Le contrat des `validated_derived_execution_projections` encode plusieurs invariants constitutionnels (pas de nouvelle règle, pas de divergence normative, promotion interdite, régénérabilité), ce qui fait de la factory un bon vecteur de protection si les champs sont réellement renseignés et vérifiés.
- L’état `PLATFORM_FACTORY_STATE` reconnaît que le cycle de vie des projections dérivées et le tooling de validation manquent encore ; tant que cette lacune persiste, une IA pourrait consommer une projection formellement marquée « validated » sans garantie d’alignement effectif avec le canonique.
- Le contrat minimal d’application produite reconnaît la nécessité de vérifier les `constitutional_invariants_checked`, mais sans décrire comment ces checks sont construits ni comment ils se connectent aux invariants du socle ; l’auditabilité reste donc partielle.

### Axe 2 — Cohérence interne de la factory

- La séparation architecture (prescriptive) / state (constatatif) est nette, cohérente avec la doctrine du pipeline et les décisions `PF_DECISION_TWO_ARTIFACTS` et `PF_DECISION_SCOPE_B`.
- `platform_factory_state.yaml` reste globalement honnête sur la maturité : beaucoup de capacités sont marquées comme partielles ou absentes, et des blockers explicites sont posés sur le manifest et le pipeline ; c’est un bon signal de sincérité V0.
- Il existe néanmoins une tension entre la description d’un `Platform Factory Pipeline` déjà structuré (stages 01–09) et l’aveu que le pipeline n’est pas encore matérialisé ni complètement outillé ; le risque est un faux sentiment d’opérationnalité alors que les validators manquent.
- Sur les projections, l’architecture parle d’un usage possible comme contexte unique pour une IA, tandis que l’état rappelle que `usage_as_sole_context` est encore bloqué ; cette tension doit être clarifiée pour éviter des interprétations divergentes.

### Axe 3 — Portée et frontières de couche

- La factory reste globalement bien bornée : elle gouverne l’architecture générique, l’état, les projections dérivées et le contrat minimal, mais ne prétend pas piloter le graph domaine ni le runtime d’une application spécifique.
- La séparation entre générique et spécifique est rappelée dans les principes et dans la `scope.out_of_scope`, ainsi que dans les décisions (`PF_DECISION_DOWNSTREAM_INSTANTIATION`).
- Le principal angle mort concerne la frontière exacte avec le futur pipeline d’instanciation : la factory spécifie fortement ce qu’une application produite doit respecter, mais ne décrit pas encore clairement comment ces exigences se propagent dans le pipeline aval.

### Axe 4 — Contrat minimal d’une application produite

- Points solides : présence d’un manifest obligatoire, d’un contrat de dépendances canoniques, de `reproducibility_fingerprints`, d’un runtime entrypoint contract, de blocs de configuration minimaux et d’axes de validation (structure, contrat minimal, traçabilité, packaging, runtime policy).
- Lacunes et flous :
  - le schéma exact du manifest reste à définir, ce qui rend l’auditabilité effective encore théorique ;
  - le `runtime_entrypoint_contract` est obligatoire mais sa typologie reste `TBD`, ce qui laisse ouverte la possibilité d’un runtime non 100 % local si le pipeline aval n’est pas aligné ;
  - la distinction entre obligations structurelles (manifest, packaging) et obligations de preuve (capacités de validation, rapports, signaux d’intégrité) n’est pas encore assez explicite.
- Le contrat ne formalise pas encore des hooks explicites pour vérifier que les invariants sensibles (localité, non‑génération runtime, pas de dépendance IA continue) sont effectivement satisfaits au niveau de chaque application instanciée.

### Axe 5 — Validated derived execution projections

- Les invariants de projection sont bien posés (fidélité stricte, interdiction de nouvelle norme, interdiction de promotion, régénérabilité, usage borné) et l’emplacement `docs/cores/platform_factory/projections/` est décidé avec interdiction explicite de polluer `docs/cores/current/`.
- L’état reconnaît honnêtement que le validator dédié, le protocole de régénération automatisé et la politique d’usage runtime/offsession restent à implémenter ; tant que ces manques perdurent, la notion de « validated » reste en grande partie déclarative.
- La règle selon laquelle une projection peut être l’unique artefact fourni à une IA pour un travail donné est très exigeante ; sans tooling fort, elle risque d’être utilisée de façon informelle, ce qui ouvre des scénarios de dérive normative ou d’omission dans le scope déclaré.

### Axe 6 — État reconnu, maturité et preuves

- Les sections `capabilities_present`, `capabilities_partial`, `capabilities_absent`, `blockers`, `known_gaps` et `evidence` sont globalement cohérentes et convergent vers un diagnostic « fondationnelle mais incomplète ».
- La présence de `evidence` pointant vers le plan d’architecture et l’architecture V0 ancre le state dans des artefacts concrets, ce qui est un bon réflexe de probativité.
- Certains items de `capabilities_partial` et `capabilities_absent` pourraient néanmoins être plus rigoureusement alignés : par exemple, la capacité `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` est marquée absente alors que le pipeline est déjà décrit en V0 ; le state doit clarifier ce que « complete » signifie (scripts, prompts, validators, runbook, etc.).

### Axe 7 — Multi‑IA en parallèle

- La multi‑IA est explicitement reconnue comme exigence de premier rang côté architecture et state, avec une section dédiée `multi_ia_parallel_readiness` et des capacités associées.
- Les invariants posés (scopes bornés, identifiants stables, dépendances explicites, points d’assemblage clairs, rapports homogènes, projections régénérables) vont dans le bon sens, mais restent largement au niveau du principe.
- Les principaux trous concernent la granularité modulaire, le protocole d’assemblage des sorties IA, la résolution de conflit et les conventions de taille de projection ; sans ces éléments, plusieurs IA peuvent encore se marcher sur les pieds ou générer des configurations difficilement mergeables.

### Axe 8 — Gouvernance release, manifest et traçabilité

- Le pipeline comporte des stages explicites pour la release materialization, la promotion dans `docs/cores/current/` et le closeout/archive, avec des règles claires sur l’interdiction de modifier directement `current/` hors promotion.
- Le state enregistre le blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` et lie explicitement sa levée à la complétion du STAGE_08, ce qui aligne bien gouvernance pipeline et état constatif.
- Le risque principal réside dans le fait que la factory elle‑même est déjà dans `docs/cores/current/` alors que le manifest ne sait pas encore la décrire : il existe une fenêtre où l’artefact est de facto « current » mais sans intégration manifeste ni contraintes explicites pour les pipelines de release existants.

### Axe 9 — Implémentabilité du pipeline

- La carte des stages 01–09 est structurée, alignée avec la doctrine des pipelines canoniques (challenge → arbitrage → patch → validation → apply → core validation → release materialization → promotion → closeout), et indique clairement les zones d’écriture autorisées.
- Le stage 04 prévoit déjà un validator Python obligatoire pour le patchset, ce qui est un bon signal d’implémentabilité future.
- Globalement, le pipeline est encore un squelette : il manque des validators spécifiques pour les projections, pour le contrat minimal, pour la traçabilité manifest, et pour la multi‑IA ; ces manques sont critiques pour passer d’un pipeline documentaire à un pipeline de gouvernance exécutable.

### Axe 10 — Scénarios adversariaux plausibles

1. **Dérive de projection dérivée**  
   - Une équipe IA génère une `validated_derived_execution_projection` large couvrant plusieurs invariants, mais sans validator dédié ni conformance matrix opérationnelle.  
   - La projection perd subtilement un interdit (par exemple, l’interdiction de génération de contenu runtime) ; elle est fournie comme unique contexte à une IA qui conçoit une application acceptant un composant génératif en usage.  
   - Problème d’architecture (projection) et de validator/tooling.

2. **Application produite apparemment valide mais non locale**  
   - Une application respecte le manifest minimal et les fingerprints, mais son runtime entrypoint pointe vers un service cloud externe non explicitement banni au niveau du contrat minimal.  
   - La factory ne fournit pas encore de check systématique des invariants de localité ; l’application passe en revue sans qu’on détecte la violation de `INV_RUNTIME_FULLY_LOCAL`.  
   - Problème de contrat minimal et de validator/tooling.

3. **Scénario multi‑IA avec collision**  
   - Deux IA travaillent en parallèle sur des projections et des modules génériques sans convention claire de granularité ni protocole d’assemblage.  
   - Chacune produit un sous‑ensemble cohérent, mais leurs outputs se recouvrent partiellement et utilisent des identifiants ou conventions différentes ; la factory ne dispose pas encore de protocole de merge ou de résolution de conflit.  
   - Problème multi‑IA et governance/assembly.

4. **Gouvernance release/manifest insuffisamment fermée**  
   - La factory continue d’évoluer dans `docs/cores/current/` alors que le manifest officiel n’a pas encore été mis à jour ; les pipelines de release existants ignorent l’existence de ces artefacts.  
   - Une équipe s’appuie implicitement sur la factory pour produire un livrable, mais le cycle de release officiel ne trace pas cette dépendance ; en cas de rollback ou d’audit, la chaîne de responsabilité est floue.  
   - Problème de manifest/release governance.

### Axe 11 — Priorisation des risques

- **Critiques**  
  - Absence de validators dédiés pour les projections dérivées et pour la preuve de conformité constitutionnelle d’une application produite.  
  - Manque de protocole opérationnel pour la multi‑IA (granularité, assemblage, résolution de conflit) alors que c’est une exigence de premier rang.

- **Élevés**  
  - Tension entre la possibilité d’utiliser une projection comme contexte unique IA et le blocage actuel de `usage_as_sole_context`, sans garde‑fou explicite dans le pipeline.  
  - Fenêtre où la factory est `current` mais sans schéma de manifest ni intégration formelle dans le dispositif de release.

- **Modérés**  
  - Flous sur la typologie des runtimes d’application et sur la façon dont les invariants de localité et de non‑génération runtime seront vérifiés au niveau du contrat minimal.  
  - Définition encore partielle des schémas (manifest, configuration, packaging) qui retarde l’outillage mais est compatible avec une V0 assumée.

- **Faibles**  
  - Divergences de tonalité entre architecture et state sur certaines capacités (pipeline, projections), tant que les gaps sont reconnus et bornés.

---

## Points V0 acceptables

- Le fait que le manifest, les schémas et les validators ne soient pas finalisés est acceptable en V0 dès lors que les gaps et blockers sont explicitement reconnus et reliés à des stages de pipeline ou à des décisions à venir.
- L’absence de pipeline d’instanciation détaillé est acceptable tant que la factory ne prétend pas gouverner le runtime d’une application spécifique et que la frontière est cadrée par des décisions explicites.
- Le positionnement de la multi‑IA comme exigence structurante mais non encore opérationnalisée est acceptable en baseline si une feuille de route claire est attachée aux gaps identifiés.

---

## Corrections à arbitrer avant patch

Pour chaque problème important :

1. **Validators de conformance pour projections dérivées**  
   - Élément concerné : `generated_projection_rules`, `execution_projection_contract`, `derived_projection_conformity_status`.  
   - Nature : manque de validator/tooling, gouvernance, exploitabilité IA.  
   - Gravité : critique.  
   - Impacts : risque de dérive normative non détectée, difficulté à prouver la conformité d’un travail IA basé sur une projection unique.  
   - Correction à arbitrer : définition d’un schéma minimal de projection, de règles de validation et d’un validator outillé.  
   - Lieu probable : architecture (schéma), validator/tooling, manifest/release governance.

2. **Preuve de conformité constitutionnelle d’une application produite**  
   - Élément concerné : `produced_application_minimum_contract`, `minimum_validation_contract`, `minimum_observability_contract`.  
   - Nature : gouvernance, compatibilité constitutionnelle, complétude.  
   - Gravité : critique.  
   - Impacts : applications produites difficiles à auditer, risque de non‑conformité non détectée.  
   - Correction à arbitrer : expliciter les checks d’invariants (localité, génération runtime, patchs) dans le contrat minimal et les relier à des validators concrets et à des signaux d’observabilité.  
   - Lieu probable : architecture, validator/tooling, manifest/release governance.

3. **Multi‑IA sans protocole d’assemblage**  
   - Élément concerné : `multi_ia_parallel_readiness`, `multi_ia_parallel_readiness_status`.  
   - Nature : exploitabilité IA, gouvernance, implémentabilité.  
   - Gravité : élevée.  
   - Impacts : collisions entre sorties IA, dérives de responsabilité, difficulté à stabiliser un état commun.  
   - Correction à arbitrer : définir un protocole de découpage, d’assemblage et de résolution de conflit entre outputs IA, avec conventions d’identifiants et de granularité modulaire.  
   - Lieu probable : architecture, state, validator/tooling.

4. **Fenêtre de gouvernance floue autour de `docs/cores/current/` et du manifest**  
   - Élément concerné : présence de la factory en `current`, blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`, stages 07–08 du pipeline.  
   - Nature : gouvernance, traçabilité, release/manifest.  
   - Gravité : élevée.  
   - Impacts : risques de release informelle s’appuyant sur la factory sans qu’elle soit reflétée dans le manifest et les pipelines de release, difficulté de rollback et d’audit.  
   - Correction à arbitrer : rendre explicite dans le pipeline et le state comment les artefacts de factory sont intégrés au manifest existant (ou à un manifest dédié) et sous quelles conditions de release.  
   - Lieu probable : pipeline, manifest/release governance.

5. **Clarification de la portée du contrat minimal vs pipeline d’instanciation**  
   - Élément concerné : `produced_application_minimum_contract`, décisions `PF_DECISION_DOWNSTREAM_INSTANTIATION`, `assessed_scope`.  
   - Nature : cohérence architecturale, gouvernance, complétude.  
   - Gravité : modérée.  
   - Impacts : risque que des exigences runtime critiques soient laissées à l’appréciation du pipeline aval sans ancrage suffisant dans le contrat minimal.  
   - Correction à arbitrer : préciser les responsabilités respectives de la factory et du pipeline d’instanciation pour chaque bloc du contrat minimal (qui définit, qui vérifie, qui outille).  
   - Lieu probable : architecture, state, pipeline.
