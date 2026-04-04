# Proposition d’arbitrage — STAGE_02_FACTORY_ARBITRAGE

- **arbitrage_run_id**: `PFARB_20260404_GPT54_R8M3K`
- **date**: `2026-04-04`
- **stage**: `STAGE_02_FACTORY_ARBITRAGE`
- **nature du livrable**: proposition indépendante d’arbitrage multi-IA, non canonique
- **pipeline**: `docs/pipelines/platform_factory/pipeline.md`

## Challenge reports considérés

Au moment de l’exécution, le dossier `docs/pipelines/platform_factory/work/01_challenge/` expose le challenge report suivant :

1. `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md`

## Cadre de lecture effectivement appliqué

1. socle canonique applicable
2. challenge report disponible
3. `docs/cores/current/platform_factory_architecture.yaml`
4. `docs/cores/current/platform_factory_state.yaml`
5. `docs/pipelines/platform_factory/pipeline.md`
6. vérification de gouvernance sur `docs/cores/current/manifest.yaml`

## Résumé exécutif

La baseline `platform_factory` V0 est **recevable comme base de gouvernance** et le pipeline est **recevable pour poursuivre le cycle challenge → arbitrage → patch**. En revanche, l’arbitrage doit fermer immédiatement trois zones structurantes avant tout patch significatif :

1. **preuve de compatibilité constitutionnelle du produit aval** ;
2. **statut opérationnel réel des `validated_derived_execution_projections`** ;
3. **fermeture de la gouvernance current / manifest / release**.

La proposition d’arbitrage ci-dessous **retient** les corrections qui conditionnent la solidité du stage de patch, **rejette** les fausses bonnes directions qui déplaceraient mal l’autorité normative, **diffère** plusieurs détails de schéma acceptables en V0, et **sort du périmètre** tout ce qui relève du futur pipeline d’instanciation ou d’un domaine applicatif spécifique.

## Synthèse des constats convergents

### Constat C-01 — séparation architecture / state saine
- **élément concerné** : structure globale `platform_factory`
- **localisation** : `platform_factory_architecture.yaml` / `platform_factory_state.yaml`
- **problème ou question** : aucun défaut majeur sur la séparation prescriptif / constatif
- **statut proposé** : `retained`
- **gravité** : faible
- **justification** : la séparation est explicite et cohérente avec le pipeline ; elle ne doit pas être réouverte inutilement
- **dépendance éventuelle** : aucune
- **lieu probable de correction** : aucun correctif de fond ; préserver l’existant
- **niveau de consensus perçu** : `strong`

### Constat C-02 — contrat minimal produit encore insuffisamment auditable
- **élément concerné** : `produced_application_minimum_contract`
- **localisation** : `platform_factory_architecture.yaml`
- **problème ou question** : le contrat minimal ne prouve pas encore explicitement la conformité aux invariants constitutionnels critiques
- **statut proposé** : `retained`
- **gravité** : élevé
- **justification** : les invariants constitutionnels sur runtime local, absence de réseau temps réel, absence de génération runtime et absence de feedback runtime généré doivent être rendus auditables par le contrat générique produit
- **dépendance éventuelle** : clarification partielle sur le lieu exact de preuve
- **lieu probable de correction** : `architecture`
- **niveau de consensus perçu** : `strong`

### Constat C-03 — projections dérivées conceptuellement solides mais opérationnellement trop ouvertes
- **élément concerné** : `validated_derived_execution_projection`
- **localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **problème ou question** : usage fort autorisé alors que validator, protocole de régénération et stockage restent incomplets
- **statut proposé** : `retained`
- **gravité** : élevé
- **justification** : la règle d’usage est plus forte que le niveau réel d’outillage ; il faut éviter une dérive normative silencieuse
- **dépendance éventuelle** : arbitrage sur le gate transitoire
- **lieu probable de correction** : `architecture` principal ; `state`, `pipeline`, `validator/tooling` secondaires
- **niveau de consensus perçu** : `strong`

### Constat C-04 — trou de gouvernance current / manifest / release
- **élément concerné** : statut officiel des artefacts `platform_factory`
- **localisation** : `platform_factory_architecture.yaml`, `platform_factory_state.yaml`, `docs/cores/current/manifest.yaml`
- **problème ou question** : les artefacts sont dans `current/` mais hors manifest courant officiel
- **statut proposé** : `retained`
- **gravité** : élevé
- **justification** : il existe un risque de confusion entre présence matérielle dans `current/` et promotion formellement gouvernée
- **dépendance éventuelle** : arbitrage sur le mécanisme transitoire ou cible
- **lieu probable de correction** : `manifest/release governance`
- **niveau de consensus perçu** : `strong`

### Constat C-05 — readiness multi-IA réelle mais encore incomplètement opérationnalisée
- **élément concerné** : `multi_ia_parallel_readiness`
- **localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml` + `pipeline.md`
- **problème ou question** : l’exigence est bien posée, mais le protocole d’assemblage et de résolution de conflit manque
- **statut proposé** : `retained`
- **gravité** : modéré
- **justification** : le sujet est réel mais n’invalide pas la baseline V0 ; il faut le fermer au minimum sans transformer la V0 en framework complet
- **dépendance éventuelle** : séquencement après fermeture des risques élevés
- **lieu probable de correction** : `architecture` principal ; `pipeline` secondaire
- **niveau de consensus perçu** : `medium`

### Constat C-06 — plusieurs schémas fins restent ouverts mais acceptables en V0
- **élément concerné** : manifest détaillé, runtime entrypoint typology, configuration détaillée, packaging détaillé
- **localisation** : `platform_factory_architecture.yaml` / `platform_factory_state.yaml`
- **problème ou question** : la baseline n’a pas encore fermé les schémas détaillés
- **statut proposé** : `deferred`
- **gravité** : modéré
- **justification** : ces ouvertures sont acceptables tant que la baseline ne surdéclare pas sa maturité et tant que les invariants critiques sont verrouillés en premier
- **dépendance éventuelle** : dépend de la fermeture préalable des risques élevés
- **lieu probable de correction** : `architecture`
- **niveau de consensus perçu** : `medium`

## Propositions d’arbitrage par thème

### Thème T-01 — Compatibilité constitutionnelle du contrat minimal produit

#### DEC-01
- **Decision ID** : `PFARB-DEC-01`
- **Sujet** : rendre auditables les invariants constitutionnels critiques dans le contrat minimal produit
- **Source(s)** :
  - `challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md`
  - `docs/cores/current/platform_factory_architecture.yaml`
  - `docs/cores/current/constitution.yaml`
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `validator/tooling`
- **Priorité** : `élevé`
- **Justification** : la factory gouverne le contrat minimal générique ; elle ne peut pas repousser totalement au pipeline aval la preuve de conformité à des invariants constitutionnels explicites
- **Impact si non traité** : une application pourrait paraître valide tout en violant des interdits majeurs
- **Pré-condition éventuelle** : clarification légère sur la forme de preuve attendue
- **Note de séquencement éventuelle** : à traiter avant tout enrichissement de schéma fin
- **Niveau de consensus perçu** : `strong`

#### DEC-02
- **Decision ID** : `PFARB-DEC-02`
- **Sujet** : ne pas créer une seconde autorité normative dans la factory
- **Source(s)** :
  - `platform_factory_architecture.yaml`
  - `constitution.yaml`
  - challenge report
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : aucun
- **Priorité** : `élevé`
- **Justification** : il faut fermer la preuve de conformité sans redéfinir les invariants constitutionnels ; la factory doit exiger des bindings et des preuves, pas réécrire la Constitution
- **Impact si non traité** : risque de duplication normative et confusion d’autorité
- **Pré-condition éventuelle** : aucune
- **Note de séquencement éventuelle** : parallèle à DEC-01
- **Niveau de consensus perçu** : `strong`

### Thème T-02 — Statut opérationnel des projections dérivées

#### DEC-03
- **Decision ID** : `PFARB-DEC-03`
- **Sujet** : geler le mode d’usage fort “artefact unique pour IA” tant que la chaîne de conformité n’est pas outillée
- **Source(s)** :
  - challenge report
  - `platform_factory_architecture.yaml`
  - `platform_factory_state.yaml`
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `state`, `pipeline`, `validator/tooling`
- **Priorité** : `élevé`
- **Justification** : l’architecture autorise un usage fort que l’état déclare non encore outillé ; il faut aligner la règle prescriptive sur le niveau réel de gouvernance
- **Impact si non traité** : faux sentiment de conformité stricte lors d’un travail IA borné
- **Pré-condition éventuelle** : arbitrer la forme exacte du gate transitoire
- **Note de séquencement éventuelle** : avant tout usage opérationnel des projections comme seul contexte
- **Niveau de consensus perçu** : `strong`

#### DEC-04
- **Decision ID** : `PFARB-DEC-04`
- **Sujet** : conserver l’ambition `validated_derived_execution_projection`
- **Source(s)** :
  - challenge report
  - `platform_factory_architecture.yaml`
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `state`
- **Priorité** : `modéré`
- **Justification** : il ne faut pas abandonner le mécanisme ; il faut le requalifier honnêtement comme objectif structurant sous gate explicite
- **Impact si non traité** : soit dérive normative, soit abandon prématuré d’un levier clé pour le multi-IA
- **Pré-condition éventuelle** : aucune
- **Note de séquencement éventuelle** : après DEC-03
- **Niveau de consensus perçu** : `strong`

### Thème T-03 — Gouvernance release / manifest / current

#### DEC-05
- **Decision ID** : `PFARB-DEC-05`
- **Sujet** : fermer explicitement le trou de gouvernance entre `current/` et `manifest.yaml`
- **Source(s)** :
  - challenge report
  - `platform_factory_architecture.yaml`
  - `platform_factory_state.yaml`
  - `docs/cores/current/manifest.yaml`
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `manifest/release governance`
- **Lieu(x) secondaire(s)** : `pipeline`
- **Priorité** : `élevé`
- **Justification** : un artefact présent en `current/` mais hors manifest officiel crée une ambiguïté de statut incompatible avec une gouvernance claire
- **Impact si non traité** : traçabilité partielle, lecture divergente de la baseline active, promotion implicite mal définie
- **Pré-condition éventuelle** : choisir un mécanisme transitoire ou cible
- **Note de séquencement éventuelle** : avant toute prétention à une baseline factory “released” pleinement fermée
- **Niveau de consensus perçu** : `strong`

#### DEC-06
- **Decision ID** : `PFARB-DEC-06`
- **Sujet** : accepter un régime transitoire explicite plutôt qu’un faux sentiment de fermeture
- **Source(s)** :
  - challenge report
  - `platform_factory_state.yaml`
  - `manifest.yaml`
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `manifest/release governance`
- **Lieu(x) secondaire(s)** : `state`
- **Priorité** : `modéré`
- **Justification** : une solution transitoire documentée est préférable à une ambiguïté silencieuse
- **Impact si non traité** : surdéclaration de maturité et auditabilité affaiblie
- **Pré-condition éventuelle** : arbitrage humain sur la cible de gouvernance
- **Note de séquencement éventuelle** : peut précéder une évolution de schéma plus complète
- **Niveau de consensus perçu** : `medium`

### Thème T-04 — Frontière factory / instanciation et multi-IA

#### DEC-07
- **Decision ID** : `PFARB-DEC-07`
- **Sujet** : matérialiser un handoff contract minimum factory → instanciation
- **Source(s)** :
  - challenge report
  - `platform_factory_architecture.yaml`
  - `platform_factory_state.yaml`
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `pipeline`
- **Priorité** : `modéré`
- **Justification** : il faut préciser ce qui est déjà garanti par la factory et ce qui reste à compléter par l’aval sans déplacer l’autorité normative
- **Impact si non traité** : zones grises de responsabilité et recouvrement entre travaux parallèles
- **Pré-condition éventuelle** : aucune
- **Note de séquencement éventuelle** : après fermeture des risques élevés
- **Niveau de consensus perçu** : `medium`

#### DEC-08
- **Decision ID** : `PFARB-DEC-08`
- **Sujet** : poser un protocole minimal multi-IA sans surcharger la V0
- **Source(s)** :
  - challenge report
  - `platform_factory_architecture.yaml`
  - `pipeline.md`
- **Décision** : `retained_now`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : `pipeline`
- **Priorité** : `modéré`
- **Justification** : il suffit à ce stade de fermer les conventions minimales de scope, ownership, assemblage et conflit
- **Impact si non traité** : collisions d’artefacts et arbitrages coûteux au stade patch
- **Pré-condition éventuelle** : aucune
- **Note de séquencement éventuelle** : après DEC-03 et DEC-05
- **Niveau de consensus perçu** : `medium`

### Thème T-05 — Niveau V0 et reports assumés

#### DEC-09
- **Decision ID** : `PFARB-DEC-09`
- **Sujet** : différer la fermeture des schémas fins non critiques
- **Source(s)** :
  - challenge report
  - `platform_factory_architecture.yaml`
  - `platform_factory_state.yaml`
- **Décision** : `deferred`
- **Lieu principal de traitement** : `architecture`
- **Lieu(x) secondaire(s)** : aucun
- **Priorité** : `modéré`
- **Justification** : ces sujets ne doivent pas retarder la fermeture des trois zones à risque élevé
- **Impact si non traité** : dette de complétude acceptable en V0
- **Pré-condition éventuelle** : avoir verrouillé les invariants critiques
- **Note de séquencement éventuelle** : après DEC-01, DEC-03 et DEC-05
- **Niveau de consensus perçu** : `strong`

## Points retenus

1. **Retenir immédiatement** la fermeture de la preuve de compatibilité constitutionnelle dans le contrat minimal produit.
2. **Retenir immédiatement** un gate explicite sur l’usage fort des projections dérivées.
3. **Retenir immédiatement** la fermeture du trou `current / manifest / release`.
4. **Retenir** un handoff contract minimum factory → instanciation.
5. **Retenir** un protocole minimal multi-IA.
6. **Retenir** le principe de ne pas dupliquer l’autorité normative du socle canonique.

## Points rejetés

### REJ-01
- **élément concerné** : remise en cause de la séparation architecture / state
- **localisation** : structure globale des deux YAML
- **problème ou question** : faudrait-il fusionner ou redessiner profondément les deux artefacts ?
- **statut proposé** : `rejected`
- **gravité** : faible
- **justification** : la séparation actuelle est saine et cohérente avec le pipeline
- **dépendance éventuelle** : aucune
- **lieu probable de correction** : aucun
- **niveau de consensus perçu** : `strong`

### REJ-02
- **élément concerné** : déplacement intégral de la compatibilité constitutionnelle vers le pipeline aval d’instanciation
- **localisation** : frontière factory / application instanciée
- **problème ou question** : la factory devrait-elle s’abstenir d’exiger une preuve générique ?
- **statut proposé** : `rejected`
- **gravité** : élevé
- **justification** : la factory gouverne explicitement le contrat minimal générique ; elle doit donc porter un minimum de preuve générique
- **dépendance éventuelle** : aucune
- **lieu probable de correction** : aucun
- **niveau de consensus perçu** : `strong`

### REJ-03
- **élément concerné** : traitement des projections dérivées comme mécanisme déjà pleinement opérationnel
- **localisation** : architecture / state
- **problème ou question** : peut-on considérer la projection mono-contexte comme prête à l’emploi ?
- **statut proposé** : `rejected`
- **gravité** : élevé
- **justification** : le state constate explicitement l’absence de validator, de stockage décidé et de protocole de régénération
- **dépendance éventuelle** : aucune
- **lieu probable de correction** : aucun
- **niveau de consensus perçu** : `strong`

## Points différés

1. **Schéma final détaillé du manifest produit** — `deferred` — après fermeture des invariants critiques.
2. **Typologie exacte du runtime entrypoint** — `deferred` — utile mais non bloquante à ce stade.
3. **Schéma détaillé de configuration** — `deferred`.
4. **Schéma détaillé de packaging** — `deferred`.
5. **Granularité optimale du travail multi-IA** — `deferred` — après protocole minimal.

## Points hors périmètre

### OOS-01
- **élément concerné** : design détaillé d’une application spécifique instanciée
- **localisation** : aval de `platform_factory`
- **problème ou question** : la factory doit-elle détailler une application Learn-it particulière ?
- **statut proposé** : `out_of_scope`
- **gravité** : faible
- **justification** : le pipeline `platform_factory` gouverne le générique, pas une application particulière
- **dépendance éventuelle** : aucune
- **lieu probable de correction** : `hors périmètre factory`
- **niveau de consensus perçu** : `strong`

### OOS-02
- **élément concerné** : contenu pédagogique domaine-spécifique
- **localisation** : contenu aval
- **problème ou question** : faut-il l’intégrer dans les artefacts factory ?
- **statut proposé** : `out_of_scope`
- **gravité** : faible
- **justification** : explicitement hors scope de l’architecture factory
- **dépendance éventuelle** : aucune
- **lieu probable de correction** : `hors périmètre factory`
- **niveau de consensus perçu** : `strong`

### OOS-03
- **élément concerné** : pipeline complet d’instanciation domaine
- **localisation** : couche aval
- **problème ou question** : faut-il le spécifier maintenant dans le stage 02 factory ?
- **statut proposé** : `out_of_scope`
- **gravité** : modéré
- **justification** : la boundary existe, mais le pipeline aval n’est pas gouverné par le présent stage
- **dépendance éventuelle** : aucune
- **lieu probable de correction** : `hors périmètre factory`
- **niveau de consensus perçu** : `strong`

## Points sans consensus ou nécessitant discussion finale

> Note : un seul challenge report était présent au moment de l’exécution. Les points ci-dessous ne sont donc pas des conflits inter-reports établis, mais des arbitrages de conception encore ouverts qui nécessitent une consolidation finale humaine-assistée.

### DISC-01
- **sujet** : forme exacte de la preuve de compatibilité constitutionnelle
- **question** : bloc dédié de type `constitutional_compatibility_evidence`, extension du manifest, renforcement du validation contract, renforcement de l’observability contract, ou combinaison de plusieurs ?
- **statut proposé** : `clarification_required`
- **gravité** : élevé
- **justification** : le besoin est retenu, mais la forme exacte doit être décidée proprement avant patch
- **lieu probable de correction** : `architecture`
- **niveau de consensus perçu** : `medium`

### DISC-02
- **sujet** : gate transitoire sur l’usage mono-contexte des projections dérivées
- **question** : interdiction stricte tant que la chaîne n’est pas outillée, ou autorisation exceptionnelle sous garde-fou humain explicite ?
- **statut proposé** : `clarification_required`
- **gravité** : élevé
- **justification** : l’usage fort ne peut pas rester implicite ; il faut choisir une règle transitoire nette
- **lieu probable de correction** : `architecture` avec support `state` / `pipeline`
- **niveau de consensus perçu** : `medium`

### DISC-03
- **sujet** : mécanisme de fermeture current / manifest / release
- **question** : extension du schéma de manifest courant, companion manifest, ou régime transitoire formalisé ?
- **statut proposé** : `clarification_required`
- **gravité** : élevé
- **justification** : le problème est clair, mais la solution cible de gouvernance reste ouverte
- **lieu probable de correction** : `manifest/release governance`
- **niveau de consensus perçu** : `medium`

## Corrections à arbitrer avant patch

### CORR-01
- **Élément concerné** : contrat minimal produit
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème ou question** : absence de preuve suffisamment explicite sur localité runtime, absence de réseau temps réel, absence de génération runtime et usage autorisé des feedbacks/templates
- **Statut proposé** : `retained`
- **Gravité** : élevé
- **Justification** : conditionne la conformité générique du produit aval
- **Dépendance éventuelle à d’autres arbitrages** : DISC-01
- **Lieu probable de correction** : `architecture`
- **Niveau de consensus perçu** : `strong`

### CORR-02
- **Élément concerné** : règle d’usage des projections dérivées
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème ou question** : désalignement entre puissance d’usage autorisée et niveau réel d’outillage
- **Statut proposé** : `retained`
- **Gravité** : élevé
- **Justification** : conditionne la sûreté du travail IA borné
- **Dépendance éventuelle à d’autres arbitrages** : DISC-02
- **Lieu probable de correction** : `architecture` principal ; `state`, `pipeline`, `validator/tooling` secondaires
- **Niveau de consensus perçu** : `strong`

### CORR-03
- **Élément concerné** : régime officiel de gouvernance des artefacts `platform_factory`
- **Localisation** : `manifest.yaml` + notes de statut des artefacts factory
- **Problème ou question** : ambiguïté entre présence en `current/` et statut officiellement promu/gouverné
- **Statut proposé** : `retained`
- **Gravité** : élevé
- **Justification** : conditionne la lisibilité de la baseline active
- **Dépendance éventuelle à d’autres arbitrages** : DISC-03
- **Lieu probable de correction** : `manifest/release governance`
- **Niveau de consensus perçu** : `strong`

### CORR-04
- **Élément concerné** : handoff contract factory → instanciation
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème ou question** : insuffisance de matérialisation de la frontière de responsabilité
- **Statut proposé** : `retained`
- **Gravité** : modéré
- **Justification** : améliore la lisibilité du scope sans re-spécifier l’aval
- **Dépendance éventuelle à d’autres arbitrages** : aucune
- **Lieu probable de correction** : `architecture`
- **Niveau de consensus perçu** : `medium`

### CORR-05
- **Élément concerné** : protocole minimal multi-IA
- **Localisation** : `platform_factory_architecture.yaml` + `pipeline.md`
- **Problème ou question** : absence de conventions minimales d’ownership, assemblage et résolution de conflit
- **Statut proposé** : `retained`
- **Gravité** : modéré
- **Justification** : améliore la fiabilité de la factory sans exiger un outillage complet immédiat
- **Dépendance éventuelle à d’autres arbitrages** : séquencement après CORR-02
- **Lieu probable de correction** : `architecture` + `pipeline`
- **Niveau de consensus perçu** : `medium`

### CORR-06
- **Élément concerné** : set minimal de validators prioritaires
- **Localisation** : `pipeline.md` + future chaîne de `validator/tooling`
- **Problème ou question** : quels validators sont indispensables avant de qualifier la gouvernance factory comme mieux fermée ?
- **Statut proposé** : `retained`
- **Gravité** : modéré
- **Justification** : la baseline V0 peut continuer, mais pas prétendre être vraiment fermée sans un minimum d’instrumentation
- **Dépendance éventuelle à d’autres arbitrages** : dépend du choix sur projections et preuve constitutionnelle
- **Lieu probable de correction** : `validator/tooling` principal ; `pipeline` secondaire
- **Niveau de consensus perçu** : `medium`

## Répartition par lieu de correction

### Architecture
- fermeture de la preuve de compatibilité constitutionnelle du contrat minimal produit
- gate transitoire sur les projections dérivées
- handoff contract minimum factory → instanciation
- protocole minimal multi-IA
- fermeture ultérieure des schémas fins différés

### State
- requalification explicite du statut opérationnel réel des projections dérivées
- wording honnête sur les capacités présentes / absentes si un gate transitoire est posé
- explicitation éventuelle du régime transitoire de gouvernance

### Pipeline
- matérialiser les gates liés aux projections dérivées
- matérialiser les points de contrôle liés au protocole minimal multi-IA
- relier la gouvernance stage/release aux décisions sur manifest/current

### Validator / tooling
- validator de conformité des projections dérivées
- validator du contrat minimal produit
- validator minimal de lineage / release si retenu

### Manifest / release governance
- fermeture du statut officiel des artefacts `platform_factory`
- choix du mécanisme cible ou transitoire pour éviter l’ambiguïté de `current/`

### Hors périmètre factory
- application spécifique instanciée
- contenu pédagogique domaine-spécifique
- pipeline aval complet d’instanciation

## Séquencement recommandé

1. **Fermer DEC-01 / CORR-01** : obligations auditables de compatibilité constitutionnelle.
2. **Fermer DEC-03 / CORR-02** : règle transitoire claire sur les projections dérivées.
3. **Fermer DEC-05 / CORR-03** : gouvernance current / manifest / release.
4. **Fermer DEC-07 et DEC-08** : handoff contract et protocole minimal multi-IA.
5. **Différer DEC-09** : schémas fins détaillés et raffinements non critiques.
6. **Planifier CORR-06** : validators prioritaires alignés sur les décisions déjà prises.

## Priorités de patch

### Priorité élevée
- preuve de compatibilité constitutionnelle du contrat minimal produit
- gate sur les projections dérivées
- fermeture current / manifest / release

### Priorité modérée
- handoff contract minimum
- protocole minimal multi-IA
- validators minimaux prioritaires

### Priorité faible
- fermeture des schémas fins non critiques de V0

## Conclusion d’arbitrage

Cette proposition d’arbitrage considère que la baseline `platform_factory` est **suffisamment saine pour continuer**, mais **pas suffisamment fermée pour patcher sans cadrage préalable** sur trois sujets structurants : preuve constitutionnelle, projections dérivées, gouvernance current/manifest/release.

L’arbitrage proposé est donc :
- **ferme** sur les sujets qui conditionnent la sécurité normative et la traçabilité ;
- **sobre** sur les sujets acceptables en V0 ;
- **strict** sur le refus de déplacer l’autorité normative hors du bon niveau ;
- **pragmatique** sur le séquencement pour permettre un STAGE_03 propre.
