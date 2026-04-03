# Platform Factory — Plan de cadrage et d’implantation

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

---

## 5. Plan détaillé par phases

## PHASE 0 — Validation du cadrage

### Objectif
Valider ensemble le présent plan avant toute exécution structurante.

### Décisions attendues
- accepter ou ajuster le découpage en deux artefacts canoniques ;
- confirmer le nom du pipeline cible : `platform_factory` ;
- confirmer que la première étape reste documentaire/architecturale, pas canonique ;
- confirmer que l’état actuel et la cible doivent rester séparés.

### Livrable
- ce document validé ou amendé.

### Critère de sortie
- accord explicite sur le modèle cible.

---

## PHASE 1 — Définition du modèle canonique minimal de fabrique

### Objectif
Définir la structure logique minimale de :
- `platform_factory_architecture.yaml`
- `platform_factory_state.yaml`

### Travail à produire

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

### Livrables attendus
- un premier design de structure pour les deux YAML ;
- une convention de lecture claire : prescriptif vs constatif.

### Critère de sortie
- structure cible stable et assez claire pour justifier un pipeline dédié.

---

## PHASE 2 — Définition du pipeline `platform_factory`

### Objectif
Définir le pipeline qui gouvernera cette nouvelle couche.

### Principe
Le pipeline doit conserver le même esprit général que `constitution` :
- audit ;
- arbitrage ;
- synthèse ;
- validation ;
- application en zone de travail ;
- promotion explicite éventuelle.

### Différence importante
L’objet gouverné n’est pas un Core pédagogique, mais un **état de fabrique**.

### Stages proposés

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
- vérifier la séparation prescriptif / constatif.

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
- vérifier leur cohérence avec la Constitution et le Référentiel.

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

### Critère de sortie
- pipeline défini à un niveau comparable aux autres pipelines actifs.

---

## PHASE 3 — Définition des prompts partagés

### Objectif
Créer une famille cohérente de prompts réexécutables, alignés sur les conventions du repo.

### Prompts proposés
- `Make20PlatformFactoryAudit.md`
- `Make21PlatformFactoryArbitrage.md`
- `Make22PlatformFactoryPatch.md`
- `Make23PlatformFactoryValidation.md`
- `Make24PlatformFactoryReview.md`

### Contraintes de design
Les prompts doivent conserver la structure canonique déjà présente dans le repo :
- ROLE
- OBJECTIF
- INPUT
- AXES / ANALYSE
- RÈGLES
- OUTPUT

### Critère de sortie
- prompts stables, relisibles, réexécutables et localisables.

---

## PHASE 4 — Définition de la scorecard et du suivi de progression

### Objectif
Éviter qu’un audit soit uniquement narratif.

### Scorecard proposée
Le fichier `platform_factory_scorecard.yaml` doit permettre de suivre dans le temps au moins :
- abstraction_genericity
- platform_application_separation
- compilation_readiness
- technical_contracts
- pipeline_coverage
- packaging_readiness
- observability_readiness
- variant_governance
- blockers

### Pour chaque rubrique
- status: `green | amber | red`
- score: échelle bornée
- evidence
- gaps
- next_actions

### Rapport delta proposé
Le pipeline devrait aussi pouvoir produire un rapport delta du type :
- progrès ;
- stagnation ;
- régression ;
- ambiguïtés persistantes.

### Critère de sortie
- possibilité réelle de lire l’avancement à mesure.

---

## PHASE 5 — Intégration au repo

### Objectif
Inscrire la couche Platform Factory dans la gouvernance standard du repo.

### Modifications attendues
Après validation du modèle :
- ajouter le pipeline dans `docs/registry/pipelines.md` ;
- ajouter les nouveaux prompts dans `docs/registry/resources.md` ;
- éventuellement ajuster `docs/README.md` si la navigation doit mentionner la fabrique ;
- créer les nouveaux artefacts canoniques sous `docs/cores/current/`.

### Critère de sortie
- aucun nouvel artefact important ne reste hors couche d’autorité attendue.

---

## PHASE 6 — Premier run de baseline

### Objectif
Produire un premier état de référence officiel de la fabrique.

### Résultat attendu
Le premier run ne vise pas nécessairement à tout corriger.
Il vise à établir :
- une architecture cible minimale ;
- un état actuel officiel ;
- une première scorecard ;
- une liste claire des écarts.

### Critère de sortie
- existence d’une baseline exploitable pour les runs suivants.

---

## 6. Choix d’implantation proposés

## 6.1. Emplacement du présent document

Le meilleur emplacement de ce plan est `docs/architecture/` car :
- il s’agit d’un document d’architecture préparatoire ;
- il ne s’agit pas encore d’un pipeline canonique actif ;
- il ne doit pas être confondu avec un Core déjà promu.

## 6.2. Emplacement futur des artefacts canoniques

Sous `docs/cores/current/` :
- `platform_factory_architecture.yaml`
- `platform_factory_state.yaml`

## 6.3. Emplacement futur du pipeline

Sous `docs/pipelines/platform_factory/`.

## 6.4. Emplacement futur des prompts

Sous `docs/prompts/shared/`.

---

## 7. Ce que ce plan ne doit pas faire

Ce plan ne doit pas :
- créer immédiatement un pipeline non validé ;
- prétendre qu’un état de fabrique est canonique alors qu’il n’a pas été promu ;
- mélanger architecture cible et état observé dans un seul artefact ;
- transformer un audit d’architecture en simple backlog produit ;
- réécrire la Constitution sous prétexte de parler de la fabrique.

---

## 8. Risques majeurs à éviter

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

---

## 9. Checklist de validation avant exécution

Avant de lancer la mise en œuvre, vérifier explicitement :

- [ ] le découpage en deux artefacts canoniques est accepté ;
- [ ] le nom `platform_factory` est accepté ;
- [ ] l’emplacement de ce plan dans `docs/architecture/` est accepté ;
- [ ] la distinction Architecture cible / État actuel est acceptée ;
- [ ] l’idée d’un pipeline dédié est acceptée ;
- [ ] la logique de scorecard YAML est acceptée ;
- [ ] le niveau de parallélisme avec `constitution` est accepté ;
- [ ] les non-objectifs sont compris.

---

## 10. Questions à revoir ensemble

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

---

## 11. Proposition de séquence immédiate

Si ce plan est globalement validé, la suite recommandée est :

1. revue humaine de ce document ;
2. ajustements éventuels ;
3. définition de la structure YAML de `platform_factory_architecture.yaml` ;
4. définition de la structure YAML de `platform_factory_state.yaml` ;
5. rédaction du `pipeline.md` de `docs/pipelines/platform_factory/` ;
6. rédaction du prompt `Make20PlatformFactoryAudit.md` ;
7. premier run de baseline.

---

## 12. Résumé exécutif

Le bon choix proposé est le suivant :

- ne pas créer un seul `platform_factory.yaml` ;
- créer une couche Platform Factory explicite ;
- séparer **prescriptif** et **constatif** ;
- gouverner cette couche par un pipeline dédié ;
- produire des rapports de progression, mais aussi une vérité canonique promouvable.

Formule synthétique :

> Constitution = WHY  
> Référentiel = HOW MUCH  
> Platform Factory Architecture = HOW  
> Platform Factory State = WHERE WE ARE NOW

Ce plan vise à introduire cette nouvelle couche sans casser la logique d’autorité ni la discipline par pipelines du repo.