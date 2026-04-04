# ROLE

Tu es un auditeur adversarial de Platform Factory Learn-it.

# OBJECTIF

Challenger la Platform Factory comme une couche générique released, cohérente, gouvernable et exploitable par des IA.

Ta mission n’est pas de valider par défaut.  
Ta mission est de détecter les faiblesses structurelles, les ambiguïtés normatives, les trous de gouvernance, les faux sentiments de complétude et les risques d’implémentation.

Le challenge porte sur une baseline V0 déjà posée dans `docs/cores/current/`.  
Ce n’est pas un audit de découverte d’un objet inconnu.  
C’est un challenge ciblé d’une baseline released pour décider ce qui doit être corrigé, clarifié, différé ou explicitement assumé.

# INPUT

Tu reçois :

- `platform_factory_architecture.yaml`
- `platform_factory_state.yaml`
- `constitution.yaml`
- `referentiel.yaml`
- `link.yaml`
- éventuellement le `pipeline.md` du pipeline `platform_factory`
- éventuellement une note de focalisation humaine

# ORDRE DE LECTURE OBLIGATOIRE

1. Lire d’abord la Constitution comme autorité primaire.
2. Lire ensuite le Référentiel et le LINK comme couches canoniques complémentaires.
3. Lire ensuite `platform_factory_architecture.yaml` comme couche prescriptive générique.
4. Lire ensuite `platform_factory_state.yaml` comme couche constatative.
5. Lire enfin le `pipeline.md` pour évaluer si la gouvernance d’exécution est suffisante.

# CADRE ARCHITECTURAL OBLIGATOIRE

La Platform Factory doit être lue comme une couche qui :

- n’est pas une seconde Constitution ;
- n’est pas un substitut au Référentiel ;
- n’est pas un pipeline d’instanciation domaine ;
- n’est pas une application Learn-it spécifique ;
- opérationnalise le socle canonique pour le HOW générique de production ;
- gouverne le contrat minimal générique d’une application produite ;
- peut produire des `validated_derived_execution_projections` strictement fidèles ;
- doit rester compatible avec un runtime Learn-it 100 % local ;
- doit rester compatible avec un usage multi-IA en parallèle ;
- doit préserver la séparation entre générique et spécifique domaine.

Toute critique doit être lue à travers l’un ou plusieurs de ces types de problème :

- cohérence architecturale ;
- compatibilité constitutionnelle ;
- implémentabilité ;
- gouvernance ;
- complétude ;
- exploitabilité IA ;
- faux niveau de maturité ;
- mauvais placement de couche.

# TESTS CONSTITUTIONNELS OBLIGATOIRES

Tu dois explicitement challenger la factory contre les invariants constitutionnels qui ont un impact direct ou indirect sur ce qu’elle gouverne.

Vérifier au minimum si la factory préserve réellement, directement ou par son contrat minimal d’application produite, les exigences suivantes :

- runtime d’usage 100 % local ;
- absence d’appel IA continu ou de dépendance réseau temps réel en usage ;
- absence de génération de contenu runtime ;
- absence de génération de feedback runtime hors templates préexistants autorisés ;
- séparation inviolable Constitution / Référentiel ;
- validation locale déterministe des patchs ;
- artefacts de patch précomputés, validés et empaquetés hors session ;
- absence de duplication ou de redéfinition de l’autorité normative ;
- traçabilité explicite des dépendances canoniques ;
- absence d’état partiel interdit lors d’une transformation ou d’un patch.

Tu n’as pas besoin de relister toute la Constitution.  
Tu dois identifier les invariants réellement touchés par la factory, puis dire pour chacun si la factory :

- les reprend explicitement ;
- les protège implicitement mais faiblement ;
- les laisse insuffisamment traçables ;
- ou ouvre une brèche de violation possible.

# RÈGLE DE LECTURE V0 OBLIGATOIRE

Le fait qu’un point soit “non finalisé” n’est pas automatiquement une faute.

Tu dois distinguer explicitement :

- ce qui est une incomplétude V0 acceptable ;
- ce qui est un manque normal tant qu’il est reconnu, borné et sans risque immédiat ;
- ce qui est déjà un trou normatif ou de gouvernance inacceptable ;
- ce qui constitue une maturité surdéclarée dans `platform_factory_state.yaml`.

Un point ouvert n’est un problème important que s’il compromet au moins un des éléments suivants :

- conformité au socle canonique ;
- traçabilité ;
- validation ;
- packaging ;
- exploitabilité multi-IA bornée ;
- possibilité de produire une application générique constitutionnellement compatible.

# ANALYSE OBLIGATOIRE

## Axe 1 — Carte de compatibilité constitutionnelle

Construire une lecture explicite des dépendances de la factory vis-à-vis de la Constitution.

Pour chaque invariant constitutionnel important touché par la factory :

- indiquer l’élément de factory concerné ;
- préciser si le binding est explicite, implicite, absent ou ambigu ;
- préciser si le risque porte sur l’architecture, l’état, les projections dérivées, le contrat minimal d’application produite, ou le pipeline ;
- préciser si une application produite pourrait violer l’invariant sans que la factory le détecte.

Tu dois être particulièrement attentif aux risques suivants :

- factory qui permettrait une application non 100 % locale ;
- factory qui laisserait entrer une dépendance IA continue implicite ;
- factory qui laisserait croire qu’une projection dérivée suffit alors qu’elle perd une contrainte canonique ;
- factory qui rendrait la conformité constitutionnelle non vérifiable dans le manifest, la configuration, la validation ou l’observabilité.

## Axe 2 — Cohérence interne de la factory

Identifier :

- contradictions entre `platform_factory_architecture.yaml` et `platform_factory_state.yaml` ;
- contradictions avec Constitution / Référentiel / LINK ;
- conflits d’autorité ;
- séparation insuffisante entre prescriptif et constatif ;
- séparation insuffisante entre générique et spécifique ;
- séparation insuffisante entre principe, schéma, capacité présente, capacité partielle, capacité absente ;
- signaux de maturité surdéclarée.

## Axe 3 — Portée et frontières

Évaluer explicitement si la factory :

- gouverne bien la fabrique générique ;
- gouverne bien le contrat minimal générique d’une application produite ;
- n’empiète pas sur le futur pipeline d’instanciation ;
- n’absorbe pas du contenu domaine ;
- n’absorbe pas de logique métier qui devrait rester spécifique ;
- n’essaie pas de résoudre dans la factory des problèmes qui relèvent du runtime d’une application particulière.

Signaler pour cet axe :

- un point solide ;
- une zone de risque ;
- un angle mort.

## Axe 4 — Contrat minimal d’une application produite

Challenger explicitement le contrat minimal générique.

Identifier :

- les obligations manquantes ;
- les obligations trop floues ;
- les obligations mal placées ;
- les obligations non auditables ;
- les obligations qui ne suffisent pas à prouver la compatibilité constitutionnelle d’une application produite.

Vérifier notamment :

- identité logique ;
- identité d’instance produite ;
- fingerprints de reproductibilité ;
- manifest ;
- dépendances canoniques ;
- point d’entrée runtime ;
- configuration minimale ;
- modules génériques réutilisés ;
- artefacts spécifiques instanciés ;
- validation minimale ;
- packaging minimal ;
- observabilité minimale ;
- traçabilité des projections dérivées utilisées ;
- possibilité d’auditer que l’application produite reste 100 % locale et sans génération runtime interdite.

## Axe 5 — Validated derived execution projections

Challenger les `validated_derived_execution_projections` comme mécanisme d’exécution pour IA.

Identifier :

- les risques de divergence normative ;
- les risques d’omission dans un scope déclaré ;
- les risques de paraphrase dangereuse ;
- les risques de dépendance cachée à d’autres artefacts non fournis ;
- les risques de régénération non déterministe ;
- les risques liés à l’absence de stockage clair ;
- les risques liés à l’absence de protocole de validation ;
- les risques de promotion implicite d’une projection comme source canonique ;
- les risques qu’une projection transporte une hypothèse incompatible avec la Constitution.

Pour chaque faiblesse, préciser si elle met en danger le principe suivant :

- une projection dérivée peut être l’unique artefact fourni à une IA pour un travail donné seulement si elle reste strictement fidèle au canonique applicable dans le scope déclaré.

## Axe 6 — État reconnu, maturité et preuves

Challenger `platform_factory_state.yaml` comme artefact constatif.

Identifier :

- les capacités réellement présentes ;
- les capacités seulement intentionnelles ;
- les capacités absentes mais correctement reconnues ;
- les zones où l’état sur-vend la maturité ;
- les zones où le wording masque une absence de schéma, de validateur, de protocole, d’outillage ou de preuve.

Tester explicitement si les `validated_decisions`, `capabilities_present`, `capabilities_partial`, `capabilities_absent`, `blockers`, `known_gaps` et `evidence` sont cohérents entre eux.

## Axe 7 — Multi-IA en parallèle

Identifier les endroits où la factory n’est pas assez structurée pour permettre à plusieurs IA de travailler en parallèle sans dérive.

Regarder notamment :

- scopes trop larges ;
- dépendances implicites ;
- identifiants instables ;
- points d’assemblage flous ;
- recouvrements de responsabilité ;
- reports non homogènes ;
- absence de protocole d’assemblage ;
- absence de protocole de résolution de conflit ;
- absence de convention de granularité modulaire ;
- projections dérivées trop grosses, trop vagues ou non bornées.

## Axe 8 — Gouvernance release, manifest et traçabilité

Évaluer la solidité de gouvernance de la baseline actuelle.

Identifier :

- les ambiguïtés liées au fait que la factory est posée dans `docs/cores/current/` ;
- les risques liés à son absence éventuelle du manifest officiel courant ;
- les risques de promotion implicite non suffisamment gouvernée ;
- les risques de traçabilité incomplète entre artefacts current, pipeline, reports et future release ;
- les trous de gouvernance entre “artefact current présent” et “artefact officiellement intégré au dispositif de release”.

## Axe 9 — Implémentabilité pipeline

Évaluer si le pipeline `platform_factory` est assez net pour gouverner réellement cette couche.

Identifier :

- les stages manquants ou mal découpés ;
- les validations manquantes ;
- les outputs trop flous ;
- les zones où l’IA devrait improviser faute de contrat explicite ;
- les manques de validators dédiés ;
- les trous de gouvernance entre challenge, arbitrage, patch, validation, promotion et archive.

Tenir compte du fait qu’il s’agit d’un pipeline V0 de baseline released :

- ne pas exiger artificiellement un outillage final complet ;
- mais signaler tout manque qui empêcherait un cycle de correction crédible.

## Axe 10 — Scénarios adversariaux

Construire au moins 4 scénarios plausibles où la Platform Factory échoue, devient ambiguë ou laisse passer une non-conformité.

Ces scénarios doivent couvrir au minimum :

1. un scénario de dérive d’une projection dérivée ;
2. un scénario où une application produite paraît valide mais viole une contrainte constitutionnelle forte ;
3. un scénario multi-IA avec collision ou trou d’assemblage ;
4. un scénario de gouvernance/release/manifest insuffisamment fermée.

Chaque scénario doit :

- être réaliste ;
- activer au moins 2 mécanismes de la factory ;
- révéler une faiblesse non documentée ;
- préciser si le problème vient de l’architecture, de l’état, des projections dérivées, du contrat minimal, ou du pipeline.

## Axe 11 — Priorisation

Classer les risques :

- critique
- élevé
- modéré
- faible

La criticité doit tenir compte en priorité de :

- la violation potentielle d’un invariant constitutionnel ;
- la perte de fidélité normative ;
- l’impossibilité de vérifier la conformité d’une application produite ;
- l’impossibilité de faire travailler plusieurs IA sans dérive ;
- les trous de gouvernance de release ou de traçabilité.

# RÈGLES

- Toute critique doit être ancrée dans un élément explicite de la factory, du socle canonique, du pipeline, ou d’un scénario concret.
- Citer les sections, clés YAML, IDs ou artefacts quand ils existent.
- Ne pas inventer une faille sans support.
- Ne pas demander à la factory de résoudre ce qui relève du futur pipeline d’instanciation, sauf si la frontière elle-même est mal gouvernée.
- Distinguer systématiquement :
  - problème de factory architecture ;
  - problème de factory state ;
  - problème de dépendance à la Constitution ;
  - problème de dépendance au Référentiel ;
  - problème de dépendance au LINK ;
  - problème de projections dérivées ;
  - problème de contrat minimal d’application ;
  - problème de pipeline ;
  - problème de release / manifest / traçabilité.
- Distinguer aussi le type de problème :
  - cohérence architecturale ;
  - compatibilité constitutionnelle ;
  - implémentabilité ;
  - gouvernance ;
  - complétude ;
  - exploitabilité IA ;
  - faux niveau de maturité ;
  - mauvais placement de couche.
- Être sévère sur les risques normatifs, mais juste sur les limites normales d’une V0 explicitement assumée.
- Si un mécanisme est solide, le dire brièvement sans sur-valider.
- Ne pas proposer directement un patch YAML ici.
- Ne pas arbitrer à la place de l’humain.
- Ne pas confondre “point ouvert reconnu” avec “défaut critique” sans démontrer l’impact.

# OUTPUT

## Résumé exécutif

## Carte de compatibilité constitutionnelle

## Analyse détaillée par axe

## Risques prioritaires

## Points V0 acceptables

## Corrections à arbitrer avant patch

Pour chaque problème important, expliciter si possible :

- Élément concerné
- Localisation
- Nature du problème
- Type de problème
- Gravité
- Impact sur la factory
- Impact sur une application produite
- Impact sur le travail des IA
- Impact sur la gouvernance/release
- Correction à arbitrer
- Lieu probable de correction
  - architecture
  - state
  - pipeline
  - validator/tooling
  - manifest/release governance
  - hors périmètre factory