# Arbitrage Platform Factory — Proposition

arbitrage_run_id: PFARB_20260408_PERPX_A1B2

date: 2026-04-08

challenge_reports_considered:
- docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260408_PERPX_7KQ2.md

## Résumé exécutif

Cette proposition d’arbitrage part d’un seul challenge report V0 qui converge fortement sur quatre risques majeurs (fidélité normative des projections dérivées, contrat minimal d’application produite, multi-IA, gouvernance release/manifest) et confirme que la Platform Factory reste une baseline fondatrice mais incomplète, posée de manière honnête dans son state mais encore peu outillée pour une exploitation intensive.[cite:5][cite:6][cite:7][cite:8][cite:12]

L’arbitrage retient comme corrections à traiter en priorité un durcissement du modèle de projections dérivées, un renforcement du contrat minimal d’application au niveau manifest/validation, une spécification opérationnelle du protocole multi-IA et une clarification de la chaîne release/manifest/promotion, en reportant certains aspects de granularité et d’optimisation fine comme sujets V0 assumés mais non bloquants.[cite:5][cite:6][cite:7][cite:8][cite:12]

## Synthèse des constats convergents

- La factory est correctement positionnée comme couche générique non normative qui opérationnalise le socle Constitution/Référentiel/LINK, avec séparation claire architecture/state et reconnaissance explicite des gaps et blockers.[cite:2][cite:3][cite:5][cite:6][cite:8][cite:12]
- Les points de fragilité se concentrent sur la matérialisation concrète des validated_derived_execution_projections, la vérifiabilité du contrat minimal d’une application produite, la définition d’un protocole multi-IA et la gouvernance release/manifest/traçabilité.[cite:5][cite:6][cite:7][cite:8][cite:12]
- Le pipeline V0 fournit un squelette cohérent Challenge → Arbitrage → Patch → Validation → Release → Promotion → Closeout, mais reste largement non outillé en validators et schémas détaillés.[cite:5][cite:6][cite:7][cite:8][cite:12]

## Propositions d’arbitrage par thème

### Thème 1 — Projections dérivées validées

- Élément concerné : generated_projection_rules et execution_projection_contract dans `platform_factory_architecture.yaml`.[cite:5][cite:12]
- Problème : absence de schéma, d’emplacement, de validator et de protocole de régénération pour les validated_derived_execution_projections ; risque de dérive normative silencieuse si une projection compressée devient l’unique contexte IA.[cite:5][cite:6][cite:7][cite:8][cite:12]
- Décision proposée : **retained_now**.
- Lieu principal de correction : **architecture** (définition du modèle et des invariants de projection).[cite:5][cite:12]
- Lieux secondaires : **validator/tooling** (validators de conformité) et **pipeline** (stages de génération/validation/usage des projections).[cite:5][cite:6][cite:7][cite:12]
- Statut : critique, consensus fort.

### Thème 2 — Contrat minimal d’application produite

- Élément concerné : produced_application_minimum_contract dans `platform_factory_architecture.yaml` et sections de maturité associées dans `platform_factory_state.yaml`.[cite:5][cite:6][cite:12]
- Problème : obligations bien listées mais encore peu liées à des schémas concrets, à des champs manifest et à des validators déterministes, rendant difficile la preuve de localité, d’absence de génération runtime interdite et de respect des invariants.[cite:2][cite:3][cite:5][cite:6][cite:8][cite:12]
- Décision proposée : **retained_now** pour le durcissement conceptuel, avec certains détails de schéma en **clarification_required** avant patch.[cite:5][cite:6][cite:12]
- Lieu principal de correction : **architecture** (raffinement du contrat minimal).[cite:5][cite:12]
- Lieux secondaires : **state** (ajustement de la description de maturité) et **validator/tooling** (validators de manifest et de configuration).[cite:5][cite:6][cite:12]
- Statut : critique, consensus fort.

### Thème 3 — Multi-IA parallel readiness

- Élément concerné : multi_ia_parallel_readiness dans l’architecture et multi_ia_parallel_readiness_status dans le state.[cite:5][cite:6][cite:12]
- Problème : exigence reconnue mais absence de protocole opérationnel détaillé (granularité modulaire, conventions de nommage, assemblage, résolution de conflit, homogénéité des reports).[cite:5][cite:6][cite:7][cite:8][cite:12]
- Décision proposée : **retained_now** pour la définition d’un protocole cible minimal, avec certains raffinements en **deferred**.[cite:5][cite:6][cite:12]
- Lieu principal de correction : **architecture** (règles de découpage, d’assemblage et de responsabilité).[cite:5][cite:12]
- Lieux secondaires : **pipeline** (séquençage multi-IA) et **validator/tooling** (contrôles de cohérence multi-IA).[cite:5][cite:6][cite:7][cite:12]
- Statut : élevé, consensus fort.

### Thème 4 — Gouvernance release / manifest / traçabilité

- Élément concerné : variant_governance, build_and_packaging_rules et observability_requirements dans l’architecture, ainsi que produced_application_contract_status et blockers dans le state, plus les stages 07–09 du pipeline.[cite:5][cite:6][cite:7][cite:12]
- Problème : baseline platform_factory posée en `docs/cores/current/` avec statut RELEASE_CANDIDATE, mais manifest existant qui ne l’intègre pas encore, et pipeline de release/promotion/closeout non matérialisé jusqu’au bout ; risque de promotion implicite et de traçabilité incomplète.[cite:5][cite:6][cite:7][cite:8][cite:12]
- Décision proposée : **retained_now** pour clarifier la gouvernance de la factory elle-même (alignement current/manifest/pipeline), avec un volet **manifest/release governance** plutôt que contenu canonique seul.[cite:5][cite:6][cite:7][cite:12]
- Lieu principal de correction : **manifest/release governance**.[cite:5][cite:7][cite:12]
- Lieux secondaires : **state** (wording de maturité et blockers) et **pipeline** (durcissement des stages 07–09).[cite:5][cite:6][cite:7][cite:12]
- Statut : élevé, consensus fort.

## Points retenus

- Nécessité de définir un modèle et des invariants plus concrets pour les validated_derived_execution_projections.[cite:5][cite:6][cite:7][cite:8][cite:12]
- Nécessité de relier le contrat minimal d’application produite à des schémas, des champs manifest et des validators déterministes.[cite:2][cite:3][cite:5][cite:6][cite:8][cite:12]
- Nécessité de spécifier un protocole multi-IA minimal couvrant granularité, assemblage et résolution de conflits.[cite:5][cite:6][cite:7][cite:8][cite:12]
- Nécessité de clarifier la gouvernance release/manifest/promotion pour la Platform Factory et de la relier au pipeline de manière traçable.[cite:5][cite:6][cite:7][cite:8][cite:12]

## Points rejetés

À ce stade et avec un seul challenge report, aucun finding majeur n’est explicitement rejeté ; certains risques sont reclassés comme **V0 acceptable** ou **reporté** lorsqu’ils relèvent davantage d’optimisation fine que de conformité canonique ou de gouvernance minimale.[cite:6][cite:12]

## Points différés

- Granularité optimale des modules et taille idéale des projections dérivées ; ces sujets sont différés en optimisation V0+ tant qu’un minimum de schémas et de validators n’est pas en place.[cite:5][cite:6][cite:7][cite:8][cite:12]
- Détails complets du futur pipeline d’instanciation domaine, considérés comme hors périmètre immédiat de la factory tant que le contrat minimal générique n’est pas durci.[cite:5][cite:6][cite:7][cite:8][cite:12]

## Points hors périmètre

- Choix UI/UX spécifiques des applications instanciées, non couverts par la factory tant que les contrats de packaging, de manifest et de runtime restent respectés.[cite:5][cite:6][cite:12]

## Points sans consensus ou nécessitant discussion finale

- Niveau exact de sévérité associé au label RELEASE_CANDIDATE pour la factory alors que plusieurs capabilities restent absentes ; une discussion humaine est recommandée pour fixer la politique de labellisation et éviter l’ambiguïté entre baseline conceptuelle et RC prête à l’usage.[cite:5][cite:6][cite:7][cite:8][cite:12]

## Corrections à arbitrer avant patch

1) Définir un premier schéma concret pour les validated_derived_execution_projections (structure, métadonnées de scope, sources, traceability hooks, statut de validation, contraintes de régénération) et décider du lieu de stockage cible, de préférence hors `docs/cores/current/` pour éviter toute confusion avec le canonique.[cite:5][cite:6][cite:7][cite:8][cite:12]

2) Lier le contrat minimal d’application produite à des champs manifest et à des signaux d’observabilité explicites permettant d’auditer localité, absence de génération runtime interdite et respect des invariants de patch, sans interprétation implicite.[cite:2][cite:3][cite:5][cite:6][cite:8][cite:12]

3) Spécifier un protocole multi-IA minimal (scopes, conventions de nommage, articulation des reports, points d’assemblage et résolution de conflit) en restant dans la portée factory, et ajuster le state pour refléter cette clarification une fois réalisée.[cite:5][cite:6][cite:7][cite:8][cite:12]

4) Clarifier la relation entre la présence de la factory dans `docs/cores/current/`, le statut RELEASE_CANDIDATE, les stages 07–09 du pipeline et le manifest officiel, afin que toute promotion future passe par une chaîne traçable et explicitement close en closeout/archive.[cite:5][cite:6][cite:7][cite:8][cite:12]
