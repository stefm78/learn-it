# Platform Factory — Plan de cadrage et d’implantation (v2)

## Statut du document

Ce document est un **document d’architecture préparatoire**.

Il n’est pas un Core canonique.
Il ne modifie pas la vérité métier Learn-it.
Il prépare la création éventuelle :
- d’artefacts canoniques dédiés à la fabrique applicative ;
- d’un pipeline `platform_factory` ;
- d’une chaîne d’audit, d’arbitrage, de promotion et de suivi de progression.

Tant qu’il n’y a pas de pipeline dédié validé et promu, ce document doit être lu comme un **plan de travail structurant**, pas comme une autorité finale.

---

## Inspiration from docs/specs

Le plan `platform_factory` doit s’inspirer explicitement des patterns déjà présents dans `docs/specs/`, sans recopier mécaniquement leur contenu métier.

### 1. Discipline issue du Patch DSL
Le plan doit reprendre l’esprit de `docs/specs/patch-dsl/current.md` :
- transformation déterministe ;
- validation avant application ;
- dry-run exécutable ;
- rapport d’exécution ;
- refus de la logique implicite.

### 2. Séparation transformation / promotion issue du Release Patch DSL
Le plan doit reprendre l’esprit de `docs/specs/release-patch/current.md` :
- transformation logique et promotion de dépôt sont deux actes distincts ;
- toute bascule vers `docs/cores/current/` doit être explicite ;
- la promotion doit rester traçable, atomique et auditée.

### 3. Formalisation des artefacts inspirée des schémas existants
Le plan doit s’inspirer des schémas déjà présents, notamment :
- `docs/specs/core-release/current_manifest.schema.yaml`
- `docs/specs/core-release/promotion_report.schema.yaml`

Leçon à reprendre : les artefacts importants de `platform_factory` ne doivent pas être des notes libres, mais des artefacts structurés avec :
- racine canonique ;
- champs obligatoires ;
- invariants explicites ;
- traçabilité de leur origine et de leur promotion.

### 4. Impact attendu sur les futurs travaux
Cette inspiration implique qu’à terme il sera probablement pertinent d’ajouter, sous `docs/specs/`, des spécifications dédiées à `platform_factory`, par exemple :
- un schéma pour `platform_factory_architecture.yaml` ;
- un schéma pour `platform_factory_state.yaml` ;
- un schéma pour la scorecard de progression ;
- un schéma pour les projections dérivées validées ;
- éventuellement un schéma pour le report de promotion ou de closeout du pipeline.

### 5. Lien avec `docs/registry/`
La future couche `platform_factory` devra aussi rester proprement intégrée à `docs/registry/`, notamment :
- `docs/registry/pipelines.md` pour déclarer le pipeline ;
- `docs/registry/resources.md` pour inventorier prompts, specs et outils ;
- `docs/registry/conventions.md` pour rester cohérent avec les zones d’écriture et la discipline de validation ;
- `docs/registry/operating_model.md` pour conserver une hiérarchie d’autorité lisible.

### 6. Lien avec `docs/prompts/shared/`
Les prompts nécessaires au futur pipeline devront être créés dans `docs/prompts/shared/`, conformément au pattern déjà en place dans le repo. Le plan doit donc prévoir une famille de prompts partagés stables, réexécutables et faciles à inventorier dans `docs/registry/resources.md`.

---

## 1. Problème à résoudre

Le repo Learn-it possède déjà :
- une Constitution qui fixe les principes et invariants du système ;
- un Référentiel qui borne les paramètres et tables opérationnelles ;
- un LINK qui explicite les bindings inter-Core ;
- des pipelines qui permettent de challenger, arbitrer, patcher, valider et promouvoir ces artefacts.

Ce cadre est déjà fort pour gouverner le système d’apprentissage lui-même.

En revanche, il manque encore une couche explicite pour gouverner la **fabrique applicative** :
- comment on passe du cadre canonique à une ou plusieurs applications ;
- comment on sépare la plateforme générique des applications produites ;
- comment on mesure la progression de cette capacité de production ;
- comment on évite qu’un audit de readiness reste purement narratif et non gouverné.

Le besoin n’est donc pas de produire seulement un audit ponctuel.
Le besoin est de construire une **gouvernance explicite de la capacité Learn-it à produire des applications d’apprentissage**.

---

## 2. Décision de principe proposée

### 2.1. Conservation des rôles actuels

La Constitution reste le **WHY** :
- principes ;
- invariants ;
- interdits ;
- exigences de fond.

Le Référentiel reste le **HOW MUCH / operational bounds** :
- seuils ;
- tables ;
- fenêtres ;
- bornes ;
- paramètres opératoires.

### 2.2. Introduction d’une couche Platform Factory

La fabrique applicative doit être gouvernée par deux nouveaux artefacts canoniques distincts :

1. `docs/cores/current/platform_factory_architecture.yaml`
2. `docs/cores/current/platform_factory_state.yaml`

### 2.3. Rôle des deux artefacts

#### A. `platform_factory_architecture.yaml`
Document **prescriptif**.
Il décrit ce que la fabrique doit être.

Il porte notamment :
- l’architecture cible ;
- les couches ;
- les composants ;
- les flux ;
- les contrats ;
- les frontières plateforme / application ;
- les dépendances aux Core existants ;
- les contraintes d’industrialisation ;
- les règles de compilation ou de transformation.

Il correspond au **HOW prescriptif**.

#### B. `platform_factory_state.yaml`
Document **constatif canonique**.
Il décrit l’état actuel officiellement reconnu de la fabrique.

Il porte notamment :
- les capacités présentes ;
- les capacités absentes ;
- les capacités partielles ;
- le niveau de maturité par couche ;
- les blockers ;
- les écarts versus l’architecture cible ;
- les preuves ou rapports de validation associés.

Il correspond au **AS-IS officiel**.

### 2.4. Décision importante

Il est **déconseillé** de fusionner ces deux rôles dans un seul `platform_factory.yaml`.

Raison : un même fichier ne doit pas mélanger sans séparation claire :
- la cible normative ;
- l’état observé ;
- l’écart ;
- l’audit ;
- les arbitrages ;
- les actions futures.

Ce mélange créerait une ambiguïté d’autorité contraire à l’esprit général du repo.

---

## 3. Résultat cible recherché

À terme, la fabrique Learn-it doit disposer de :

### 3.1. Une vérité canonique de fabrique
Sous `docs/cores/current/` :
- `platform_factory_architecture.yaml`
- `platform_factory_state.yaml`

### 3.2. Un pipeline explicite de gouvernance
Sous `docs/pipelines/platform_factory/` :
- `pipeline.md`
- `state.yaml`
- `inputs/`
- `work/`
- `outputs/`
- `reports/`
- éventuellement `archive/`

### 3.3. Une famille de prompts partagés dédiés
Sous `docs/prompts/shared/` :
- `Make20PlatformFactoryAudit.md`
- `Make21PlatformFactoryArbitrage.md`
- `Make22PlatformFactoryPatch.md`
- `Make23PlatformFactoryValidation.md`
- `Make24PlatformFactoryReview.md`

### 3.4. Une capacité de suivi d’avancement dans le temps
Avec au minimum :
- un rapport d’audit narratif ;
- une scorecard YAML structurée ;
- un rapport delta entre deux runs successifs.

### 3.5. Des projections dérivées validées pour exécution IA
Le pipeline `platform_factory` devra pouvoir générer des **validated_derived_execution_projections** strictement conformes, destinées à être fournies comme contexte unique à des IA ou à des pipelines spécialisés dans un scope borné.

---

## 4. Positionnement de la couche Platform Factory

La couche Platform Factory ne gouverne pas directement :
- le contenu pédagogique d’une application produite ;
- la progression d’un apprenant ;
- les paramètres pédagogiques métier eux-mêmes.

Elle gouverne :
- la **capacité de production** ;
- la **structure de transformation** ;
- la **séparation des responsabilités** ;
- la **qualité des contrats techniques** ;
- la **réplicabilité** de la production d’applications ;
- la **lisibilité** de l’état d’avancement de la fabrique.

Formulation directrice proposée :

> Le pipeline `platform_factory` ne gouverne pas une application produite.  
> Il gouverne l’état canonique de la capacité Learn-it à produire des applications.

### 4.1. Portée retenue
La portée retenue est la suivante :
- `platform_factory` gouverne la fabrique générique Learn-it ;
- `platform_factory` gouverne aussi le **contrat minimal générique** d’une application produite ;
- le spécifique domaine est produit ultérieurement, dans un pipeline d’instanciation distinct ;
- les projections dérivées validées servent d’interface d’exécution bornée pour les IA et les pipelines aval.

### 4.2. Connexion avec le socle canonique
La connexion avec le socle canonique (Constitution + Référentiel + LINK) doit être conservée explicitement.

Règles :
- `platform_factory` ne duplique pas la norme ;
- `platform_factory` peut produire des projections dérivées générées, à champ restreint ;
- ces projections restent strictement fidèles au canonique applicable à leur scope ;
- en cas d’évolution du canonique, les projections doivent être régénérées ;
- la conformité des projections au canonique devient un point de validation de la factory elle-même.

---

## 5. Validated Derived Execution Projections

### 5.1. Définition
Une **validated_derived_execution_projection** est une projection dérivée, générée par `platform_factory`, destinée à un usage borné par une IA ou un pipeline spécialisé.

Elle n’ajoute aucune règle nouvelle. Elle extrait, filtre et réorganise seulement le canonique applicable à un travail donné, complété par les contraintes et contrats génériques fixés par `platform_factory`.

### 5.2. Règle d’usage fondamentale

> Une vue dérivée peut être l’unique artefact fourni à une IA pour un travail donné, à condition qu’elle soit validée comme projection strictement fidèle, sans divergence normative, du canonique applicable à ce travail.

### 5.3. Statut
Une projection dérivée validée doit être comprise à la fois comme :
- une **projection d’exécution strictement conforme** pour l’IA qui la consomme ;
- une projection dérivée régénérable dont la source normative primaire reste le canonique.

### 5.4. Invariants minimaux
Chaque projection dérivée validée doit respecter au minimum :
- `no_new_rule`
- `no_normative_divergence`
- `no_omission_within_declared_scope`
- `canonical_source_remains_primary_authority`
- `deterministic_regeneration_required`

### 5.5. Effet recherché
Les projections dérivées validées doivent permettre :
- la réduction du contexte transmis aux IA ;
- le travail parallèle de plusieurs IA ;
- la distribution claire des responsabilités ;
- l’exécution de pipelines spécialisés sans relecture intégrale du socle canonique.

### 5.6. Interdits
Il est interdit de :
- modifier manuellement une projection dérivée validée comme source de vérité ;
- y introduire une règle absente du canonique applicable ;
- promouvoir une projection dérivée comme artefact canonique primaire ;
- paraphraser librement une contrainte normative au lieu de l’extraire, la filtrer et la réorganiser.

### 5.7. Emplacement et cycle de vie
L’emplacement exact reste à préciser, mais le principe est fixé :
- les projections dérivées ne doivent pas brouiller la couche `docs/cores/current/` ;
- elles doivent vivre dans une zone logique, stable et facile à suivre pour le développement ;
- elles doivent être générées, consommées, archivées si utile, puis régénérées dès que le canonique ou la factory évoluent.

---

## 6. Contrat minimal générique d’une application produite

Le contrat minimal générique décrit le minimum requis pour qu’une application puisse être reconnue comme produite par Learn-it, traçable, instanciable, validable et exploitable.

Ce contrat n’a pas vocation à figer toute l’application ni tout le spécifique domaine. Il fixe seulement les obligations minimales génériques.

### 6.1. Identité d’application
Chaque application produite doit disposer d’une identité explicite, distinguant :
- l’identité logique de l’application ;
- l’identité d’instance produite ;
- les fingerprints ou signatures utiles à la reproductibilité.

Point d’attention explicitement retenu :
- deux utilisateurs distincts peuvent produire des applications différentes à partir d’inputs identiques ;
- le modèle d’identité doit donc distinguer clairement identité logique, identité d’instance et empreinte de génération.

### 6.2. Manifest d’application
Chaque application produite doit disposer d’un manifest minimal décrivant au moins :
- son identité ;
- son origine ;
- ses dépendances au canonique et à la factory ;
- les modules génériques réutilisés ;
- les artefacts spécifiques instanciés ;
- les statuts minimaux de validation ;
- les informations minimales de packaging et de traçabilité.

### 6.3. Contrat de dépendance au canonique
L’application produite doit déclarer explicitement :
- les versions ou releases canoniques utilisées ;
- les versions pertinentes de la factory ;
- les projections dérivées utilisées ;
- les références nécessaires à la reproductibilité et à l’audit.

### 6.4. Point d’entrée runtime explicite
L’application produite doit posséder un point d’entrée runtime identifiable, avec :
- un identifiant de point d’entrée ;
- un type d’entrée ou de bootstrap ;
- un contrat minimal d’initialisation ;
- les prérequis minimaux nécessaires à son exécution.

### 6.5. Configuration minimale explicite
L’application produite doit disposer d’une configuration minimale structurée couvrant au minimum :
- l’identité ;
- l’activation des modules ;
- les références d’instanciation ;
- la traçabilité.

Le niveau de détail exact reste à challenger, mais la présence de ces quatre blocs minimaux est retenue dès maintenant.

### 6.6. Déclaration des modules génériques réutilisés
L’application produite doit indiquer explicitement quels modules génériques de la factory elle réutilise.

### 6.7. Déclaration des artefacts spécifiques instanciés
L’application produite doit déclarer quels artefacts spécifiques ont été instanciés pour le domaine ou le cas d’usage visé.

### 6.8. Validation minimale
L’application produite doit pouvoir produire au moins un socle minimal de validation couvrant :
- la structure ;
- la conformité au contrat minimal ;
- la traçabilité ;
- le packaging.

Le détail exact des reports reste à challenger et compléter ultérieurement.

### 6.9. Packaging minimal
L’application produite doit disposer d’un packaging minimal identifiable, relié à son manifest, et vérifiable comme complet, incomplet ou invalide.

Le détail exact du packaging reste à challenger et compléter ultérieurement.

### 6.10. Observabilité minimale
L’application produite doit laisser au moins des traces minimales sur :
- son identité de build ;
- ses modules activés ;
- les projections dérivées utilisées ;
- son statut de validation ;
- les références nécessaires à la traçabilité.

---

## 7. Multi-IA Parallel Development Readiness

Le développement assisté par plusieurs IA en parallèle est une contrainte clé du design de `platform_factory`.

### 7.1. Exigence structurante
`platform_factory` doit produire des artefacts suffisamment modulaires, bornés, traçables et stables pour permettre un travail parallèle de plusieurs IA sans ambiguïté de responsabilité ni divergence d’assemblage.

### 7.2. Conséquences minimales
Cela implique au minimum :
- des scopes bornés par projection dérivée ;
- des identifiants stables pour les modules, projections et artefacts ;
- des dépendances explicites ;
- des points d’assemblage clairs ;
- des reports homogènes ;
- l’absence de dépendances implicites non documentées ;
- la possibilité de régénérer les projections sans dérive.

### 7.3. Posture retenue
Le niveau de détail optimal pour le travail parallèle multi-IA sera challengé ultérieurement, mais la contrainte elle-même est déjà retenue comme exigence de premier rang de la factory.

---

## 8. Plan détaillé par phases

### PHASE 0 — Validation du cadrage

**Objectif**
Valider ensemble le présent plan avant toute exécution structurante.

**Décisions attendues**
- accepter ou ajuster le découpage en deux artefacts canoniques ;
- confirmer le nom du pipeline cible : `platform_factory` ;
- confirmer que la première étape reste documentaire/architecturale, pas canonique ;
- confirmer que l’état actuel et la cible doivent rester séparés.

**Livrable**
- ce document validé ou amendé.

**Critère de sortie**
- accord explicite sur le modèle cible.

---

### PHASE 1 — Définition du modèle canonique minimal de fabrique

**Objectif**
Définir la structure logique minimale de :
- `platform_factory_architecture.yaml`
- `platform_factory_state.yaml`

**Travail à produire**

#### Pour `platform_factory_architecture.yaml`
Définir les sections minimales, par exemple :
- metadata
- purpose
- scope
- design_principles
- platform_layers
- transformation_chain
- contracts
- variant_governance
- build_and_packaging_rules
- observability_requirements
- dependencies_to_constitution
- dependencies_to_referentiel
- invariants
- constraints
- generated_projection_rules
- produced_application_minimum_contract
- multi_ia_parallel_readiness

#### Pour `platform_factory_state.yaml`
Définir les sections minimales, par exemple :
- metadata
- assessed_scope
- maturity_by_layer
- capabilities_present
- capabilities_partial
- capabilities_absent
- blockers
- validated_decisions
- known_gaps
- evidence
- last_assessment
- delta_since_previous
- derived_projection_conformity_status
- produced_application_contract_status
- multi_ia_parallel_readiness_status

**Livrables attendus**
- un premier design de structure pour les deux YAML ;
- une convention de lecture claire : prescriptif vs constatif.

**Critère de sortie**
- structure cible stable et assez claire pour justifier un pipeline dédié.

---

### PHASE 2 — Définition du pipeline `platform_factory`

**Objectif**
Définir le pipeline qui gouvernera cette nouvelle couche.

**Principe**
Le pipeline doit conserver le même esprit général que `constitution` :
- audit ;
- arbitrage ;
- synthèse ;
- validation ;
- application en zone de travail ;
- promotion explicite éventuelle.

**Différence importante**
L’objet gouverné n’est pas un Core pédagogique, mais un **état de fabrique**.

**Stages proposés**

#### STAGE_01_FACTORY_SCAN
But :
- inventorier les artefacts utiles à la fabrique ;
- identifier ce qui existe déjà ;
- préparer l’audit.

Outputs proposés :
- `work/01_scan/platform_factory_inventory.md`

#### STAGE_02_FACTORY_AUDIT
But :
- évaluer la capacité du repo à soutenir la production d’applications ;
- produire un audit de readiness ;
- produire une scorecard structurée.

Outputs proposés :
- `work/02_audit/platform_factory_audit.md`
- `reports/platform_factory_scorecard.yaml`

#### STAGE_03_FACTORY_ARBITRAGE
But :
- décider ce qui relève :
  - d’une correction architecturale ;
  - d’un manque de contrat ;
  - d’un manque de pipeline ;
  - d’une simple note de progression ;
  - d’un report.

Outputs proposés :
- `work/03_arbitrage/platform_factory_arbitrage.md`

#### STAGE_04_FACTORY_PATCH_SYNTHESIS
But :
- synthétiser les évolutions retenues sur les artefacts Platform Factory ;
- produire un patch destiné à l’architecture, à l’état, ou aux deux.

Outputs proposés :
- `work/04_patch/platform_factory_patchset.yaml`

#### STAGE_05_FACTORY_PATCH_VALIDATION
But :
- vérifier que le patch est structurellement recevable ;
- vérifier que les deux artefacts restent cohérents ;
- vérifier la séparation prescriptif / constatif ;
- vérifier la cohérence des règles de projections dérivées et du contrat minimal générique.

Outputs proposés :
- `work/05_validation/platform_factory_patch_validation.yaml`
- `reports/platform_factory_patch_validation_report.md`

#### STAGE_06_FACTORY_APPLY
But :
- appliquer le patch dans une sandbox ;
- matérialiser les fichiers patchés ;
- conserver une trace d’exécution.

Outputs proposés :
- `work/06_apply/patched/platform_factory_architecture.yaml`
- `work/06_apply/patched/platform_factory_state.yaml`
- `reports/platform_factory_execution_report.yaml`

#### STAGE_07_FACTORY_CORE_VALIDATION
But :
- valider la cohérence d’ensemble des artefacts Platform Factory patchés ;
- vérifier leur lisibilité canonique ;
- vérifier leur cohérence avec la Constitution et le Référentiel ;
- vérifier que la factory peut soutenir la génération de projections dérivées conformes.

Outputs proposés :
- `work/07_validation/platform_factory_core_validation.yaml`
- `reports/platform_factory_core_validation_report.md`

#### STAGE_08_FACTORY_PROMOTION
But :
- promouvoir explicitement les nouveaux artefacts vers `docs/cores/current/` si validés.

Outputs proposés :
- `reports/platform_factory_promotion_report.yaml`

#### STAGE_09_FACTORY_CLOSEOUT
But :
- archiver le run ;
- produire un résumé final ;
- réinitialiser le workspace.

Outputs proposés :
- `reports/platform_factory_closeout_report.yaml`
- `outputs/platform_factory_summary.md`

**Critère de sortie**
- pipeline défini à un niveau comparable aux autres pipelines actifs.

---

### PHASE 3 — Définition des prompts partagés

**Objectif**
Créer une famille cohérente de prompts réexécutables, alignés sur les conventions du repo.

**Prompts proposés**
- `Make20PlatformFactoryAudit.md`
- `Make21PlatformFactoryArbitrage.md`
- `Make22PlatformFactoryPatch.md`
- `Make23PlatformFactoryValidation.md`
- `Make24PlatformFactoryReview.md`

**Contraintes de design**
Les prompts doivent conserver la structure canonique déjà présente dans le repo :
- ROLE
- OBJECTIF
- INPUT
- AXES / ANALYSE
- RÈGLES
- OUTPUT

**Critère de sortie**
- prompts stables, relisibles, réexécutables et localisables.

---

### PHASE 4 — Définition de la scorecard et du suivi de progression

**Objectif**
Éviter qu’un audit soit uniquement narratif.

**Scorecard proposée**
Le fichier `platform_factory_scorecard.yaml` doit permettre de suivre dans le temps au moins :
- abstraction_genericity
- platform_application_separation
- compilation_readiness
- technical_contracts
- pipeline_coverage
- packaging_readiness
- observability_readiness
- variant_governance
- derived_projection_conformity
- multi_ia_parallel_readiness
- blockers

**Pour chaque rubrique**
- status: `green | amber | red`
- score: échelle bornée
- evidence
- gaps
- next_actions

**Rapport delta proposé**
Le pipeline devrait aussi pouvoir produire un rapport delta du type :
- progrès ;
- stagnation ;
- régression ;
- ambiguïtés persistantes.

**Critère de sortie**
- possibilité réelle de lire l’avancement à mesure.

---

### PHASE 5 — Intégration au repo

**Objectif**
Inscrire la couche Platform Factory dans la gouvernance standard du repo.

**Modifications attendues**
Après validation du modèle :
- ajouter le pipeline dans `docs/registry/pipelines.md` ;
- ajouter les nouveaux prompts dans `docs/registry/resources.md` ;
- éventuellement ajuster `docs/README.md` si la navigation doit mentionner la fabrique ;
- créer les nouveaux artefacts canoniques sous `docs/cores/current/`.

**Critère de sortie**
- aucun nouvel artefact important ne reste hors couche d’autorité attendue.

---

### PHASE 6 — Premier run de baseline

**Objectif**
Produire un premier état de référence officiel de la fabrique.

**Résultat attendu**
Le premier run ne vise pas nécessairement à tout corriger.
Il vise à établir :
- une architecture cible minimale ;
- un état actuel officiel ;
- une première scorecard ;
- une liste claire des écarts.

**Critère de sortie**
- existence d’une baseline exploitable pour les runs suivants.

---

## 9. Choix d’implantation proposés

### 9.1. Emplacement du présent document
Le meilleur emplacement de ce plan est `docs/architecture/` car :
- il s’agit d’un document d’architecture préparatoire ;
- il ne s’agit pas encore d’un pipeline canonique actif ;
- il ne doit pas être confondu avec un Core déjà promu.

### 9.2. Emplacement futur des artefacts canoniques
Sous `docs/cores/current/` :
- `platform_factory_architecture.yaml`
- `platform_factory_state.yaml`

### 9.3. Emplacement futur du pipeline
Sous `docs/pipelines/platform_factory/`.

### 9.4. Emplacement futur des prompts
Sous `docs/prompts/shared/`.

---

## 10. Ce que ce plan ne doit pas faire

Ce plan ne doit pas :
- créer immédiatement un pipeline non validé ;
- prétendre qu’un état de fabrique est canonique alors qu’il n’a pas été promu ;
- mélanger architecture cible et état observé dans un seul artefact ;
- transformer un audit d’architecture en simple backlog produit ;
- réécrire la Constitution sous prétexte de parler de la fabrique.

---

## 11. Risques majeurs à éviter

### Risque 1 — Fichier unique confus
Créer un seul `platform_factory.yaml` qui mélange :
- cible ;
- constat ;
- backlog ;
- audit ;
- arbitrages.

### Risque 2 — Pipeline sans objet canonique
Créer un pipeline `platform_factory` qui produit seulement des rapports et aucune vérité canonique stabilisée.

### Risque 3 — Glissement de couche
Utiliser `platform_factory` pour réécrire indirectement la Constitution ou le Référentiel au lieu de gouverner la capacité de production.

### Risque 4 — Spécificité disciplinaire cachée
Concevoir la fabrique comme si toutes les applications produites étaient de type déclaratif ou textuel.

### Risque 5 — Sur-ingénierie précoce
Créer trop d’artefacts ou trop de couches avant d’avoir stabilisé le besoin minimal.

### Risque 6 — Projection dérivée divergente
Produire une projection dérivée qui diverge du canonique applicable tout en étant consommée seule par une IA.

### Risque 7 — Factory non découpable pour plusieurs IA
Produire une factory correcte pour un humain mais mal structurée pour une exécution multi-IA parallèle.

---

## 12. Checklist de validation avant exécution

Avant de lancer la mise en œuvre, vérifier explicitement :

- [ ] le découpage en deux artefacts canoniques est accepté ;
- [ ] le nom `platform_factory` est accepté ;
- [ ] l’emplacement de ce plan dans `docs/architecture/` est accepté ;
- [ ] la distinction Architecture cible / État actuel est acceptée ;
- [ ] l’idée d’un pipeline dédié est acceptée ;
- [ ] la logique de scorecard YAML est acceptée ;
- [ ] le niveau de parallélisme avec `constitution` est accepté ;
- [ ] les projections dérivées validées sont acceptées comme mécanisme d’exécution pour IA ;
- [ ] les non-objectifs sont compris.

---

## 13. Questions à revoir ensemble

### Q1. Nommage
- faut-il conserver `platform_factory` ?
- ou préférer `application_factory`, `platform_factory`, `factory_runtime`, etc. ?

### Q2. Artefacts canoniques
- faut-il démarrer avec 2 fichiers (`architecture` + `state`) ?
- ou introduire dès le départ un 3e fichier de traçabilité/lien ?

### Q3. Portée du pipeline
- le pipeline doit-il gouverner seulement la fabrique générique ?
- ou aussi la structure minimale attendue d’une application produite ?

### Q4. Manifest
- à quel moment faut-il intégrer les nouveaux artefacts dans le manifest courant ?
- dès le premier run promu ou après stabilisation ?

### Q5. Niveau de granularité du state
- le `state.yaml` de fabrique doit-il rester synthétique ?
- ou suivre très finement les capacités et sous-capacités ?

### Q6. Emplacement des projections dérivées
- où doivent vivre concrètement les `validated_derived_execution_projections` pour rester faciles à utiliser et à suivre ?

---

## 14. Proposition de séquence immédiate

Si ce plan est globalement validé, la suite recommandée est :

1. revue humaine de ce document ;
2. ajustements éventuels ;
3. définition de la structure YAML de `platform_factory_architecture.yaml` ;
4. définition de la structure YAML de `platform_factory_state.yaml` ;
5. rédaction du `pipeline.md` de `docs/pipelines/platform_factory/` ;
6. rédaction du prompt `Make20PlatformFactoryAudit.md` ;
7. premier run de baseline.

---

## 15. Résumé exécutif

Le bon choix proposé est le suivant :

- ne pas créer un seul `platform_factory.yaml` ;
- créer une couche Platform Factory explicite ;
- séparer **prescriptif** et **constatif** ;
- gouverner cette couche par un pipeline dédié ;
- produire des rapports de progression, mais aussi une vérité canonique promouvable ;
- produire des projections dérivées validées, strictement conformes, pour l’exécution bornée par IA ;
- rendre la factory exploitable par plusieurs IA en parallèle.

Formule synthétique :

> Constitution = WHY  
> Référentiel = HOW MUCH  
> Platform Factory Architecture = HOW  
> Platform Factory State = WHERE WE ARE NOW

Ce plan vise à introduire cette nouvelle couche sans casser la logique d’autorité ni la discipline par pipelines du repo.