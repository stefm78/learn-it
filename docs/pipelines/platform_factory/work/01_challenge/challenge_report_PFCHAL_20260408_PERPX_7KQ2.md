# Rapport de challenge Platform Factory

challenge_run_id: PFCHAL_20260408_PERPX_7KQ2

date: 2026-04-08

artefacts_challenges:
- docs/cores/current/constitution.yaml
- docs/cores/current/referentiel.yaml
- docs/cores/current/link.yaml
- docs/cores/current/platform_factory_architecture.yaml
- docs/cores/current/platform_factory_state.yaml
- docs/pipelines/platform_factory/pipeline.md

## Résumé exécutif

La baseline V0 de la Platform Factory pose clairement son périmètre, sépare bien architecture prescriptive et état constatif, et aligne explicitement la factory sur la Constitution et le Référentiel, mais elle reste incomplète sur plusieurs points structurants (schémas détaillés, validateurs dédiés, emplacement des projections dérivées) et expose des zones de flou de gouvernance autour du manifest et des futures promotions.[cite:2][cite:3][cite:5][cite:6][cite:7][cite:8]

Les risques principaux concernent la matérialisation concrète des validated_derived_execution_projections, la vérifiabilité effective du contrat minimal d’une application produite, et l’absence de protocole opérationnel abouti pour le travail multi-IA et pour la chaîne release / manifest / promotion, même si ces limites sont en grande partie reconnues comme gaps ou capacités partielles.[cite:5][cite:6][cite:7][cite:8]

## Carte de compatibilité constitutionnelle

La factory se déclare explicitement dépendante de la Constitution, du Référentiel et du LINK, sans tenter de dupliquer la logique normative ni d’introduire une seconde couche constitutionnelle : l’architecture rappelle que le socle canonique reste l’autorité primaire et que toute projection dérivée doit rester strictement fidèle au canonique.[cite:2][cite:3][cite:4][cite:5][cite:7][cite:8]

Les invariants de runtime 100 % local, d’absence de génération de contenu et de feedback en usage, et de validation de patchs hors session et de manière déterministe sont bien présents dans la Constitution et reliés à la factory via les dependencies_to_constitution / referentiel / link, mais la baseline V0 reste encore partielle sur la manière dont ces exigences sont vérifiables au niveau manifest, configuration et outillage de validation, ce qui laisse un risque de non-conformité silencieuse au stade d’une application produite.[cite:2][cite:3][cite:5][cite:6][cite:7][cite:8]

## Analyse détaillée par axe

### Axe 1 — Compatibilité constitutionnelle

La plate-forme s’appuie explicitement sur le socle constitutionnel pour tout ce qui touche au runtime local, aux patchs, à la séparation Constitution / Référentiel et aux règles de propagation / MSC, en rappelant que les projections dérivées ne doivent jamais introduire de nouvelles règles ni diverger du canon.[cite:2][cite:3][cite:4][cite:5][cite:7][cite:8]

En revanche, la façon concrète dont une application produite prouve via son manifest, son entrée runtime, sa configuration et ses traces qu’elle respecte ces invariants (100 % local, pas de génération de contenu, patchs déterministes hors session) n’est pas encore schématisée finement dans la factory, ce qui laisse une brèche potentielle pour des implémentations locales non conformes mais difficiles à détecter.[cite:2][cite:3][cite:5][cite:6][cite:8]

### Axe 2 — Cohérence interne de la factory

L’architecture et l’état distinguent clairement prescriptif et constatif et reconnaissent explicitement les capacités présentes, partielles et absentes, avec une liste de known_gaps et de blockers qui limite le risque de maturité surdéclarée.[cite:5][cite:6][cite:7][cite:8]

Il existe toutefois une tension entre la posture RELEASE_CANDIDATE des artefacts et la quantité de capabilities_absent, de gaps et de tooling manquant, qui suggère une maturité réelle plus proche d’un baseline conceptuel qu’un RC pleinement gouvernable, ce qui peut induire en erreur si la mention de release candidate n’est pas encadrée par une politique de release stricte.[cite:5][cite:6][cite:7][cite:8]

### Axe 3 — Portée et frontières

La factory se positionne correctement comme couche générique de production (HOW), distincte du pipeline d’instanciation domaine et de toute application Learn-it spécifique, et insiste sur la séparation générique/spécifique, sur la non-duplication de la norme et sur la limitation du scope aux contrats et projections génériques.[cite:5][cite:6][cite:7][cite:8]

Cependant, certains éléments du contrat minimal d’application produite et de la gouvernance manifest / packaging restent décrits à un niveau d’intention qui laisse encore floue la frontière exacte avec le futur pipeline d’instanciation et avec les responsabilités de runtime d’une application particulière, ce qui complique la lecture des responsabilités respectives.[cite:5][cite:6][cite:7][cite:8]

### Axe 4 — Contrat minimal d’une application produite

Le contrat minimal liste de façon structurée les blocs d’identité, de manifest, de dépendances canoniques, de runtime entrypoint, de configuration minimale, de validation, de packaging et d’observabilité, ce qui constitue un socle solide pour une preuve de compatibilité.[cite:5][cite:6][cite:8]

Néanmoins, l’absence de schémas détaillés, de critères de validation formalisés et de liens explicites avec des validateurs outillés fait que ce contrat reste pour l’instant difficile à auditer automatiquement, et ne garantit pas encore qu’une application produite expose bien les signaux nécessaires pour démontrer sa conformité constitutionnelle (localité, absence de génération runtime interdite, respect des invariants).[cite:2][cite:3][cite:5][cite:6][cite:8]

### Axe 5 — Validated derived execution projections

L’architecture décrit clairement ce qu’est une validated_derived_execution_projection, en posant des invariants forts de non-divergence normative, de régénérabilité déterministe, de scope déclaré et de possibilité d’être l’unique contexte fourni à une IA pour un travail borné.[cite:5][cite:7][cite:8]

Le principal manque porte sur l’absence de schéma concret, d’emplacement de stockage décidé, de protocole de validation outillé et de règles explicites de non-promotion d’une projection comme source canonique, ce qui rend plausible des dérives où des projections semi-stables, mal tracées ou trop larges seraient utilisées par les IA sans garantie que toutes les contraintes canoniques pertinentes restent présentes et vérifiables.[cite:5][cite:6][cite:7][cite:8]

### Axe 6 — État reconnu, maturité et preuves

`platform_factory_state.yaml` distingue de façon explicite capabilities_present, partial, absent, blockers, validated_decisions, known_gaps et evidence, ce qui fournit une base saine de lecture constative et évite de masquer les trous majeurs.[cite:6][cite:7][cite:8]

Cependant, plusieurs capabilities_partial et capabilities_absent touchent directement les validateurs, la complétude du pipeline, la matérialisation des projections et le protocole multi-IA, ce qui relativise fortement le niveau de « foundational_but_incomplete » et l’étiquette RELEASE_CANDIDATE, surtout en l’absence d’un manifest officiel intégrant la factory.[cite:5][cite:6][cite:7][cite:8]

### Axe 7 — Multi-IA en parallèle

La multi-IA parallel readiness est explicitement reconnue comme exigence de premier rang, avec des objectifs de scopes bornés, d’identifiants stables, de dépendances explicites, de points d’assemblage clairs et de projections régénérables, ce qui va dans le bon sens.[cite:5][cite:6][cite:7][cite:8]

Mais la granularité modulaire optimale, le protocole d’assemblage des sorties IA, la résolution de conflit et les conventions opérationnelles sont encore absents ou seulement esquissés, ce qui crée un risque que des équipes ou des IA parallèles se marchent dessus, produisent des reports hétérogènes ou laissent des zones d’ambiguïté dans les responsabilités et l’assemblage final.[cite:5][cite:6][cite:7][cite:8]

### Axe 8 — Gouvernance release, manifest et traçabilité

La factory est posée dans `docs/cores/current/` avec un statut de baseline released, mais le pipeline rappelle que la promotion vers current et la release materialization doivent rester des actes explicites et séparés, et que le manifest actuel ne couvre pas encore ces artefacts.[cite:5][cite:6][cite:7][cite:8]

Ce décalage entre présence en current, limitation du manifest existant et absence de chaîne complète release / promotion / archive matérialisée crée un risque de confusion sur ce qui est réellement « current » pour la plateforme et sur la traçabilité complète entre challenges, arbitrages, patchs, validations, promotions et archives.[cite:5][cite:6][cite:7][cite:8]

### Axe 9 — Implémentabilité du pipeline

Le pipeline `platform_factory` est bien structuré en stages Challenge → Arbitrage → Patch → Validation → Apply → Core Validation → Release Materialization → Promote Current → Closeout/Archive, avec une doctrine claire de non-duplication normative et de séparation release/promotion.[cite:5][cite:6][cite:7][cite:8]

En V0, plusieurs zones restent néanmoins trop peu outillées (validators dédiés, fichiers de patch, protocoles de validation, intégration avec le manifest et avec un orchestrateur d’exécution), ce qui signifie que la pipeline est aujourd’hui surtout un squelette conceptuel et nécessite un travail conséquent de tooling et de spécification pour être implémentable sans improvisation importante côté IA.[cite:5][cite:6][cite:7][cite:8]

### Axe 10 — Scénarios adversariaux

1) Dérive de projection dérivée : une équipe génère une validated_derived_execution_projection très compressée pour une tâche IA, sans schéma ni validator dédiés et sans emplacement de stockage normé ; la projection omet implicitement certaines contraintes sur les patchs ou sur le runtime local, mais reste utilisée comme unique contexte, ce qui permet une décision IA qui violerait un invariant sans que la factory détecte la perte de fidélité normative.[cite:2][cite:3][cite:5][cite:6][cite:7][cite:8]

2) Application produite apparemment valide mais violant un invariant fort : une application respecte le contrat minimal au niveau de wording (manifest, configuration, observabilité) mais sans schéma détaillé ni validation automatique ; elle introduit une dépendance réseau temps réel ou une génération de feedback à la volée, que le manifest ne permet pas d’auditer finement, exposant un risque de violation d’INV_RUNTIME_FULLY_LOCAL ou d’INV_NO_RUNTIME_CONTENT_GENERATION sans signal clair côté factory.[cite:2][cite:3][cite:5][cite:6][cite:8]

3) Scénario multi-IA avec collision : plusieurs IA travaillent en parallèle sur des extensions du contrat minimal et des projections dérivées, en l’absence de protocole d’assemblage, de convention de granularité ou de règles de consolidation ; leurs outputs hétérogènes sont assemblés manuellement, créant des incohérences entre architecture, state, projections et pipeline, sans que la factory ne fournisse de mécanisme explicite pour détecter ou arbitrer ces collisions.[cite:5][cite:6][cite:7][cite:8]

4) Scénario de gouvernance release / manifest : les artefacts platform_factory, bien que en current et marqués RELEASE_CANDIDATE, restent hors manifest officiel ; un opérateur les traite comme norme de fait sans passer par les stages 07–09 du pipeline, ce qui conduit à une adoption implicite de la baseline sans traçabilité claire des décisions, sans archive et sans alignement du manifest, rendant difficile tout audit ultérieur de la chaîne de release.[cite:5][cite:6][cite:7][cite:8]

### Axe 11 — Priorisation

Critiques : les risques liés à la fidélité normative des projections dérivées (scénario 1) et à l’impossibilité de prouver la compatibilité constitutionnelle d’une application produite (scénario 2) sont critiques, car ils touchent directement la possibilité de violer des invariants de runtime local, de génération et de patch sans détectabilité fiable.[cite:2][cite:3][cite:5][cite:6][cite:7][cite:8]

Élevés : les risques multi-IA (scénario 3) et de gouvernance release / manifest ambiguë (scénario 4) sont élevés, car ils compromettent la cohérence d’ensemble, la traçabilité et la capacité de faire évoluer la baseline de manière audit-able dans un contexte de travail parallèle par plusieurs IA.[cite:5][cite:6][cite:7][cite:8]

Modérés : les incomplétudes de schéma, de tooling de validation et de définition du pipeline d’instanciation sont modérées tant qu’elles restent reconnues comme V0 et encadrées par des blockers et des gaps explicites, mais elles deviendront critiques si le label RELEASE_CANDIDATE est interprété comme prêt pour une adoption large sans garde-fous supplémentaires.[cite:5][cite:6][cite:7][cite:8]

Faibles : certains points ouverts de granularité modulaire ou d’optimalité de projection peuvent être considérés comme risques faibles de V0, dès lors qu’ils n’exposent pas directement un invariant fort et qu’ils sont listés comme sujets d’optimisation future.[cite:5][cite:6][cite:7][cite:8]

## Risques prioritaires

- Fidélité normative des validated_derived_execution_projections insuffisamment garantie par schéma, validators et protocole de validation outillé (critique).[cite:2][cite:3][cite:5][cite:6][cite:7][cite:8]
- Contrat minimal d’application produite encore trop peu outillé pour prouver localité, absence de génération runtime interdite et respect des invariants (critique).[cite:2][cite:3][cite:5][cite:6][cite:8]
- Chaîne multi-IA sans protocole d’assemblage, de résolution de conflit ni conventions opérationnelles robustes (élevé).[cite:5][cite:6][cite:7][cite:8]
- Gouvernance release / manifest / promotion encore floue, avec une baseline en current mais hors manifest officiel et sans pipeline totalement matérialisé (élevé).[cite:5][cite:6][cite:7][cite:8]

## Points V0 acceptables

- Positionnement clair de la factory comme couche générique non normative qui opérationnalise le socle canonique, sans prétendre le remplacer.[cite:2][cite:3][cite:5][cite:7][cite:8]
- Reconnaissance explicite des gaps, capabilities_absent et blockers dans `platform_factory_state.yaml`, ce qui limite les illusions de complétude et fournit une base honnête pour l’itération.[cite:5][cite:6][cite:7][cite:8]
- Structuration en stages du pipeline avec une doctrine claire de séquence (challenge → arbitrage → patch → validation → apply → release materialization → promote → closeout), compatible avec un durcissement progressif plutôt qu’un big bang.[cite:5][cite:6][cite:7][cite:8]

## Corrections à arbitrer avant patch

1) Définir et challenger un schéma concret pour les validated_derived_execution_projections (structure, scope, sources, traceability hooks, statut de validation, contraintes de régénération) et l’outiller avec un validator dédié, en clarifiant aussi l’emplacement de stockage et les règles d’usage pour les IA.[cite:2][cite:3][cite:5][cite:6][cite:7][cite:8]

2) Durcir le contrat minimal d’une application produite en liant chaque obligation (localité, absence de génération runtime interdite, patchs hors session, traçabilité) à des champs manifest, des signaux d’observabilité et des validators déterministes, de manière à rendre l’audit de conformité réalisable sans interprétation libre.[cite:2][cite:3][cite:5][cite:6][cite:8]

3) Spécifier un protocole multi-IA opérationnel (granularité modulaire, scopes, conventions de nommage, assemblage et résolution de conflit), en s’appuyant sur les exigences déjà posées mais en les traduisant en règles et en structures concrètes dans la factory et son pipeline.[cite:5][cite:6][cite:7][cite:8]

4) Clarifier la gouvernance release / manifest / promotion pour la Platform Factory elle-même, en alignant la présence dans `docs/cores/current/`, le statut RELEASE_CANDIDATE, les stages 07–09 du pipeline et l’évolution du manifest officiel, afin qu’aucune adoption implicite de la baseline ne puisse se faire hors chaîne traçable.[cite:5][cite:6][cite:7][cite:8]
