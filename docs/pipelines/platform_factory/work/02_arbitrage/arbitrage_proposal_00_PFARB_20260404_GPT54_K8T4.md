# Proposition d’arbitrage — STAGE_02_FACTORY_ARBITRAGE

- **arbitrage_run_id**: `PFARB_20260404_GPT54_K8T4`
- **date**: `2026-04-04`
- **pipeline**: `docs/pipelines/platform_factory/pipeline.md`
- **prompt canonique d’arbitrage utilisé**: `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

## Challenge reports considérés

1. `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md`

Note d’exécution : un seul `challenge_report*.md` était présent dans `work/01_challenge/` au moment de l’exécution. Les niveaux de consensus ci-dessous distinguent donc :
- le support direct du challenge report disponible ;
- la confirmation par relecture des artefacts `platform_factory_architecture.yaml`, `platform_factory_state.yaml` et `pipeline.md`.

---

## Résumé exécutif

La baseline `platform_factory` V0 est conservée comme base de gouvernance viable, mais plusieurs fermetures sont nécessaires avant tout patch utile.

Décision d’ensemble proposée :
- **retenir maintenant** les sujets qui conditionnent la solidité normative et la gouvernance minimale de la factory ;
- **reporter explicitement** les raffinements de schéma fins compatibles avec une V0 assumée ;
- **rejeter** toute sur-correction qui déplacerait l’autorité normative hors du socle canonique ;
- **laisser hors périmètre** ce qui relève du futur pipeline d’instanciation ou du domaine spécifique.

Trois sujets doivent être traités comme structurants pour le patch à venir :
1. rendre le **contrat minimal d’application produite** plus probant vis-à-vis des invariants constitutionnels critiques ;
2. **rabaisser le niveau de promesse opérationnelle** des `validated_derived_execution_projections` tant que validator, régénération et emplacement ne sont pas clos ;
3. fermer ou encadrer explicitement le **trou de gouvernance current / manifest / release**.

---

## Synthèse des constats convergents

### Convergences fortes

1. **La séparation prescriptif / constatif est saine et doit être préservée.**
   - `platform_factory_architecture.yaml` porte bien le HOW prescriptif.
   - `platform_factory_state.yaml` porte bien le constat reconnu de maturité.
   - Le pipeline est aligné sur cette séparation.

2. **La factory ne duplique pas légitimement l’autorité normative primaire.**
   - La dépendance explicite à `constitution.yaml`, `referentiel.yaml` et `link.yaml` est correctement posée.
   - Il n’y a pas lieu d’ouvrir un patch qui réécrirait le socle primaire dans la factory.

3. **Le contrat minimal produit est utile mais encore trop haut niveau.**
   - Les blocs identité / manifest / entrypoint / configuration / validation / packaging / observabilité existent.
   - En revanche, la preuve de conformité forte à certains invariants runtime n’est pas encore suffisamment audit-able.

4. **Le mécanisme de projection dérivée est conceptuellement défini mais opérationnellement immature.**
   - L’architecture autorise l’usage fort d’une projection comme contexte unique.
   - L’état reconnaît explicitement l’absence de validator, de protocole de régénération et de décision d’emplacement.

5. **Le statut de baseline en `docs/cores/current/` reste imparfaitement fermé côté release governance.**
   - Architecture et state indiquent explicitement l’absence d’intégration au manifest courant officiel.

### Convergences moyennes

6. **Le multi-IA est bien traité comme exigence de premier rang, mais reste trop déclaratif.**
   - L’objectif est pertinent.
   - Les protocoles fins de décomposition, d’assemblage et de résolution de conflit restent absents.

7. **La frontière factory → instanciation est globalement saine, mais le handoff contract reste implicite.**
   - Le partage générique / spécifique est bien posé.
   - Le passage concret vers le pipeline d’instanciation devra être mieux balisé, sans nécessairement bloquer tout patch V0.

---

## Propositions d’arbitrage par thème

### Thème A — Compatibilité constitutionnelle du contrat minimal produit

**Proposition**
Retenir le finding et demander un renforcement maintenant.

**Arbitrage proposé**
Le patch doit renforcer la traçabilité ou la démontrabilité des invariants critiques suivants au niveau factory :
- local runtime constraints ;
- absence de dépendance réseau temps réel en usage ;
- absence de génération runtime interdite ;
- traçabilité des projections dérivées réellement utilisées.

**Décision de fond**
Il ne s’agit pas de réécrire la Constitution dans la factory, mais de rendre la conformité du produit aval plus vérifiable à travers le contrat minimal, la validation minimale ou l’observabilité minimale.

**Lieu probable de correction**
- principal : `architecture`
- secondaires : `validator/tooling`

**Consensus perçu**: `strong`

### Thème B — Statut réel des validated_derived_execution_projections

**Proposition**
Retenir le finding et corriger le niveau de promesse maintenant.

**Arbitrage proposé**
Tant que le triptyque suivant n’est pas clos :
- validator_definition,
- regeneration_protocol,
- storage_location_decision,

la factory ne doit pas laisser entendre qu’une projection dérivée est opérationnellement sûre sans garde-fou.

**Décision de fond**
Le patch doit soit :
- interdire provisoirement l’usage fort « artefact unique pour IA » ;
- soit le subordonner à une condition explicite de validation et d’outillage effectif.

**Lieu probable de correction**
- principal : `architecture`
- secondaires : `state`, `pipeline`, `validator/tooling`

**Consensus perçu**: `strong`

### Thème C — Gouvernance release / current / manifest

**Proposition**
Retenir le finding et exiger une fermeture ou un régime transitoire explicite.

**Arbitrage proposé**
La coexistence suivante n’est pas suffisamment propre :
- artefacts `platform_factory` présents dans `docs/cores/current/`
- mais hors manifest officiel courant

Le patch ou la gouvernance associée doit expliciter le régime retenu :
- intégration au manifest officiel,
- companion manifest,
- ou statut transitoire explicitement borné.

**Décision de fond**
Ce sujet ne relève pas principalement d’un enrichissement métier de `platform_factory_architecture.yaml`, mais d’une fermeture de gouvernance de release et de traçabilité.

**Lieu probable de correction**
- principal : `manifest/release governance`
- secondaires : `state`, `pipeline`

**Consensus perçu**: `strong`

### Thème D — Multi-IA parallel readiness

**Proposition**
Retenir le finding, mais ne pas surcharger la V0.

**Arbitrage proposé**
Le patch ne doit pas prétendre fermer un protocole complet multi-IA. En revanche, il peut et doit :
- clarifier que la readiness reste partielle ;
- expliciter les manques bloquants restants ;
- éviter toute formulation pouvant suggérer une opérationalisation déjà acquise.

**Décision de fond**
Conserver l’exigence comme principe architectural ; reporter la spécification complète du protocole.

**Lieu probable de correction**
- principal : `state`
- secondaires : `architecture`, `pipeline`

**Consensus perçu**: `medium`

### Thème E — Handoff contract factory → instanciation

**Proposition**
Retenir le sujet, mais le classer en amélioration différée plutôt qu’en correction bloquante immédiate.

**Arbitrage proposé**
La frontière est déjà assez bonne pour une V0. Le vrai manque est l’explicitation du passage entre contrat minimal générique et pipeline d’instanciation aval.

**Décision de fond**
Le sujet mérite d’être documenté et probablement patché à terme, mais il n’est pas le meilleur premier candidat si l’objectif immédiat est de fermer les risques normatifs plus élevés.

**Lieu probable de correction**
- principal : `architecture`
- secondaires : `pipeline`

**Consensus perçu**: `medium`

### Thème F — Validators et outillage dédiés

**Proposition**
Retenir le finding sur le besoin, mais différer l’implémentation complète.

**Arbitrage proposé**
Il faut distinguer :
- la **décision de besoin** de validators dédiés, à retenir maintenant ;
- leur **implémentation complète**, à différer.

Le patch de contenu peut donc :
- rendre l’absence plus explicite ;
- lier certains usages à la disponibilité future de validators ;
- éviter toute promesse excessive.

**Lieu probable de correction**
- principal : `state`
- secondaires : `pipeline`, `validator/tooling`

**Consensus perçu**: `strong`

---

## Findings consolidés

| Finding ID | Sujet | Sources | Qualification | Niveau de consensus |
|---|---|---|---|---|
| PFARB-F01 | Contrat minimal produit pas assez probant sur certains invariants critiques | challenge report `PFCHAL_20260404_GPT54_X7K2Q` | confirmé | strong |
| PFARB-F02 | Usage fort des projections dérivées trop ambitieux au regard de l’outillage réel | challenge report `PFCHAL_20260404_GPT54_X7K2Q` | confirmé | strong |
| PFARB-F03 | Trou de gouvernance current / manifest / release | challenge report `PFCHAL_20260404_GPT54_X7K2Q` | confirmé | strong |
| PFARB-F04 | Multi-IA readiness encore trop déclarative | challenge report `PFCHAL_20260404_GPT54_X7K2Q` | confirmé mais non bloquant au même niveau | medium |
| PFARB-F05 | Handoff contract vers instanciation encore implicite | challenge report `PFCHAL_20260404_GPT54_X7K2Q` | confirmé | medium |
| PFARB-F06 | Pipeline V0 cohérent mais pas encore assez outillé | challenge report `PFCHAL_20260404_GPT54_X7K2Q` | confirmé | strong |
| PFARB-F07 | Risque de duplication normative par la factory | challenge report `PFCHAL_20260404_GPT54_X7K2Q` | infirmé comme risque actuel majeur | strong |

---

## Décisions immédiates

### PFARB-DEC-01
- **Sujet**: compatibilité constitutionnelle du contrat minimal produit
- **Source(s)**: PFARB-F01
- **Décision**: `retained_now`
- **Lieu principal de traitement**: `architecture`
- **Lieu(x) secondaire(s)**: `validator/tooling`
- **Priorité**: `élevé`
- **Justification**: le contrat minimal existe mais ne suffit pas encore à rendre audit-able la conformité forte de l’application produite sur plusieurs invariants critiques.
- **Impact si non traité**: validation trop formelle, risque d’application apparemment valide mais insuffisamment conforme.
- **Pré-condition éventuelle**: aucune clarification de fond indispensable avant patch, si l’on reste sur un renforcement de preuve et non sur une réécriture de la norme primaire.
- **Note de séquencement éventuelle**: à traiter avant ou en même temps que les sujets sur projections dérivées.

### PFARB-DEC-02
- **Sujet**: niveau de promesse opérationnelle des projections dérivées
- **Source(s)**: PFARB-F02
- **Décision**: `retained_now`
- **Lieu principal de traitement**: `architecture`
- **Lieu(x) secondaire(s)**: `state`, `pipeline`, `validator/tooling`
- **Priorité**: `élevé`
- **Justification**: l’architecture permet un usage très fort, alors que le state reconnaît un manque de validator, de régénération et d’emplacement.
- **Impact si non traité**: faux sentiment de sécurité normative et dérive possible dans des travaux IA bornés.
- **Pré-condition éventuelle**: clarification humaine utile sur le degré de gel souhaité.
- **Note de séquencement éventuelle**: corriger d’abord la règle ou le wording, puis seulement l’outillage.

### PFARB-DEC-03
- **Sujet**: fermeture de gouvernance current / manifest / release
- **Source(s)**: PFARB-F03
- **Décision**: `retained_now`
- **Lieu principal de traitement**: `manifest/release governance`
- **Lieu(x) secondaire(s)**: `state`, `pipeline`
- **Priorité**: `élevé`
- **Justification**: la présence en `current/` sans intégration au manifest officiel courant crée une ambiguïté de traçabilité.
- **Impact si non traité**: lecture divergente du statut officiel de la baseline.
- **Pré-condition éventuelle**: choix humain du mécanisme de fermeture préféré.
- **Note de séquencement éventuelle**: la décision de gouvernance peut être séparée d’un patch contenu, mais doit être explicitée sans tarder.

### PFARB-DEC-04
- **Sujet**: multi-IA readiness
- **Source(s)**: PFARB-F04
- **Décision**: `deferred`
- **Lieu principal de traitement**: `state`
- **Lieu(x) secondaire(s)**: `architecture`, `pipeline`
- **Priorité**: `modéré`
- **Justification**: le sujet est réel mais n’impose pas encore un protocole complet si la baseline V0 reste honnête sur sa maturité.
- **Impact si non traité**: opérationalisation future plus fragile, mais pas contradiction canonique immédiate.
- **Pré-condition éventuelle**: aucune.
- **Note de séquencement éventuelle**: d’abord corriger le niveau de promesse, ensuite spécifier le protocole.

### PFARB-DEC-05
- **Sujet**: handoff contract factory → instanciation
- **Source(s)**: PFARB-F05
- **Décision**: `deferred`
- **Lieu principal de traitement**: `architecture`
- **Lieu(x) secondaire(s)**: `pipeline`
- **Priorité**: `modéré`
- **Justification**: la frontière existe déjà ; le manque porte surtout sur l’explicitation du passage.
- **Impact si non traité**: transfert de responsabilité moins lisible vers le pipeline aval.
- **Pré-condition éventuelle**: meilleure vision du futur pipeline d’instanciation.
- **Note de séquencement éventuelle**: à traiter après fermeture des sujets normatifs plus risqués.

### PFARB-DEC-06
- **Sujet**: validators et outillage dédiés
- **Source(s)**: PFARB-F06
- **Décision**: `clarification_required`
- **Lieu principal de traitement**: `validator/tooling`
- **Lieu(x) secondaire(s)**: `pipeline`, `state`
- **Priorité**: `modéré`
- **Justification**: il faut distinguer le besoin minimal indispensable de l’implémentation exhaustive.
- **Impact si non traité**: validation trop dépendante d’appréciations rédactionnelles.
- **Pré-condition éventuelle**: arbitrer la short-list des validators minimum réellement attendus au prochain cycle.
- **Note de séquencement éventuelle**: utile pour cadrer le Stage 03 et la suite, sans exiger l’implémentation complète immédiatement.

### PFARB-DEC-07
- **Sujet**: risque de duplication normative par la factory
- **Source(s)**: PFARB-F07
- **Décision**: `rejected`
- **Lieu principal de traitement**: `none`
- **Lieu(x) secondaire(s)**: `none`
- **Priorité**: `faible`
- **Justification**: la baseline actuelle référence correctement le socle canonique et ne montre pas de dérive majeure de ce type.
- **Impact si non traité**: aucun risque immédiat établi.
- **Pré-condition éventuelle**: aucune.
- **Note de séquencement éventuelle**: maintenir simplement la vigilance de séparation des couches.

---

## Points retenus

1. Renforcer la capacité de la factory à **prouver** la compatibilité forte d’une application produite.
2. Corriger le **niveau de promesse** des projections dérivées tant qu’elles ne sont pas outillées.
3. Fermer ou encadrer explicitement le **statut current / manifest / release**.
4. Maintenir la séparation stricte entre :
   - socle canonique,
   - architecture prescriptive,
   - state constatif,
   - pipeline / validators / gouvernance.
5. Conserver l’approche V0, mais sans faux sentiment de fermeture.

---

## Points rejetés

1. Rejeter toute tentative de faire porter à la factory une **réécriture normative** du socle primaire.
2. Rejeter une sur-correction qui transformerait immédiatement la V0 en framework entièrement outillé alors que le state reconnaît encore des absences structurantes.
3. Rejeter l’idée implicite selon laquelle la simple présence de blocs minimaux suffit déjà à démontrer la conformité forte du produit aval.

---

## Points différés

1. Spécification complète du protocole multi-IA.
2. Formalisation complète du handoff contract factory → instanciation.
3. Schémas fins complets du manifest, de la configuration, du packaging et de la typologie runtime.
4. Implémentation complète de validators dédiés.

Ces reports sont acceptables **à condition** que le wording de la baseline reste honnête sur le niveau réel de maturité.

---

## Points hors périmètre

1. Le design détaillé d’une application instanciée particulière.
2. Le contenu spécifique domaine.
3. Le futur pipeline d’instanciation complet, au-delà de l’interface minimale à prévoir.
4. Les choix détaillés de feedback métier spécifique.

---

## Points sans consensus ou nécessitant discussion finale

Même avec un seul challenge report, plusieurs décisions de consolidation humaine restent nécessaires :

1. **Mode de fermeture du trou current / manifest / release**
   - extension du manifest officiel,
   - companion manifest,
   - ou régime transitoire explicite.

2. **Politique exacte sur l’usage mono-contexte des projections dérivées**
   - gel provisoire total,
   - ou autorisation conditionnelle sous gate explicite.

3. **Niveau exact de formalisation à ajouter au contrat minimal produit**
   - nouveaux axes de validation,
   - nouvelles preuves d’observabilité,
   - ou bloc contractuel dédié.

4. **Short-list des validators minimum à exiger rapidement**
   - projection conformity,
   - runtime policy conformance,
   - minimum contract conformance,
   - release lineage.

Ces sujets ne sont pas des désaccords entre rapports ici ; ce sont des choix de design et de gouvernance qu’une consolidation finale doit fermer explicitement.

---

## Corrections à arbitrer avant patch

| Correction ID | Élément concerné | Localisation | Statut proposé | Gravité | Justification | Dépendance éventuelle | Lieu probable de correction | Consensus |
|---|---|---|---|---|---|---|---|---|
| PFARB-C01 | preuve de conformité forte du contrat minimal produit | `platform_factory_architecture.yaml` | retained | élevé | ferme un risque normatif réel sans déplacer l’autorité primaire | aucune forte | architecture | strong |
| PFARB-C02 | statut opérationnel des projections dérivées | `platform_factory_architecture.yaml` + `platform_factory_state.yaml` | retained | élevé | réduit une sur-promesse de capacité | arbitrage humain sur degré de gel | architecture / state / pipeline / validator | strong |
| PFARB-C03 | fermeture current / manifest / release | gouvernance transverse + `platform_factory_state.yaml` + `pipeline.md` | retained | élevé | supprime une ambiguïté de traçabilité officielle | arbitrage humain sur mécanisme | manifest/release governance | strong |
| PFARB-C04 | honnêteté V0 sur la readiness multi-IA | `platform_factory_state.yaml` | deferred | modéré | utile mais pas au même niveau de criticité | aucune | state | medium |
| PFARB-C05 | handoff contract minimal vers instanciation | `platform_factory_architecture.yaml` | deferred | modéré | améliore la lisibilité de frontière, sans bloquer le premier patch | vision du pipeline aval | architecture | medium |
| PFARB-C06 | validators minimum nécessaires | `pipeline.md` / tooling | clarification_required | modéré | il faut d’abord trancher le sous-ensemble minimal vraiment requis | oui | validator/tooling / pipeline | strong |

---

## Répartition par lieu de correction

### Architecture
- renforcement du contrat minimal produit ;
- limitation ou conditionnement explicite de l’usage fort des projections dérivées ;
- éventuel handoff contract minimal vers l’instanciation.

### State
- honnêteté accrue sur la maturité réelle ;
- explicitation des absences et dépendances d’outillage ;
- éventuelle mise en cohérence avec les arbitrages sur projections et multi-IA.

### Pipeline
- éventuel cadrage des gates ou préconditions de patch liés aux projections dérivées ;
- meilleure articulation avec les besoins de validation future ;
- éventuel rappel explicite sur la gouvernance release/current.

### Validator / tooling
- définition des validators prioritaires ;
- pas nécessairement leur implémentation complète dès ce cycle.

### Manifest / release governance
- fermeture officielle du statut des artefacts `platform_factory` présents en `current/`.

### Hors périmètre factory
- design détaillé du futur pipeline d’instanciation ;
- design détaillé d’applications spécifiques.

---

## Séquencement recommandé

1. **D’abord** arbitrer les trois sujets structurants :
   - contrat minimal produit,
   - projections dérivées,
   - gouvernance current / manifest / release.
2. **Ensuite** ajuster le wording de maturité V0 pour éviter toute sur-promesse.
3. **Ensuite seulement** cadrer la short-list des validators minimum utiles.
4. **Enfin** traiter les raffinements différés : multi-IA détaillé, handoff contract, schémas fins.

---

## Priorités de patch

### Élevé
- PFARB-DEC-01
- PFARB-DEC-02
- PFARB-DEC-03

### Modéré
- PFARB-DEC-04
- PFARB-DEC-05
- PFARB-DEC-06

### Faible
- PFARB-DEC-07

---

## Conclusion d’arbitrage

Proposition d’arbitrage :
- **retenir maintenant** les corrections qui ferment la probativité du contrat minimal, le réalisme des projections dérivées et la gouvernance current/manifest ;
- **reporter explicitement** le protocole multi-IA détaillé, le handoff contract complet et les schémas fins ;
- **rejeter** toute correction qui déplacerait l’autorité normative primaire ou surchargerait artificiellement la V0.

Cette proposition est exploitable comme contribution indépendante à la consolidation finale humaine-assistée du Stage 02.