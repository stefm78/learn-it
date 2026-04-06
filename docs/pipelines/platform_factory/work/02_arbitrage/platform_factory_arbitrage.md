# Arbitrage canonique — STAGE_02_FACTORY_ARBITRAGE

- **date**: `2026-04-06`
- **pipeline**: `docs/pipelines/platform_factory/pipeline.md`
- **stage**: `STAGE_02_FACTORY_ARBITRAGE`
- **statut**: `canonical_stage_output`
- **objectif**: fournir l’enregistrement canonique d’arbitrage du stage 02, exploitable par le stage 03 de synthèse de patch

---

## Challenge reports considérés

1. `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md`

## Arbitrage reports considérés

1. `docs/pipelines/platform_factory/work/02_arbitrage/arbitrage_proposal_00_PFARB_20260404_GPT54_K8T4.md`

## Références de cadrage considérées

- `docs/pipelines/platform_factory/pipeline.md`
- `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

---

## Résumé exécutif

La baseline `platform_factory` V0 est **retenue comme base de gouvernance valide**.

Elle ne doit toutefois pas passer au patch sans fermeture explicite de trois sujets structurants :

1. le **renforcement de la probativité** du contrat minimal d’application produite ;
2. le **conditionnement explicite** de l’usage fort des `validated_derived_execution_projections` ;
3. la **fermeture de gouvernance** du sujet `current / manifest / release`.

L’arbitrage consolidé retient la ligne suivante :
- **corriger maintenant** ce qui ferme un risque normatif ou de gouvernance réel ;
- **ne pas surcharger artificiellement la V0** ;
- **laisser une trajectoire d’enrichissement ouverte** pour les prochaines itérations du pipeline.

---

## Décisions humaines intégrées

### HUM-01 — Gouvernance current / manifest / release

Décision humaine intégrée :

La fermeture du décalage entre la présence des artefacts `platform_factory` dans `docs/cores/current/` et leur absence du manifest officiel doit être effectuée **lors de la prochaine release de `platform_factory_architecture.yaml`, en fin de pipeline**.

Conséquence d’arbitrage :
- le sujet est **retenu maintenant** comme obligation de gouvernance ;
- il ne demande **pas** une modification directe immédiate de `docs/cores/current/` hors séquence ;
- il devra être traité dans le cycle normal `release materialization` puis `promote current`, conformément au pipeline.

### HUM-02 — Usage fort des projections dérivées

Décision humaine intégrée : **Option B**.

Conséquence d’arbitrage :
- une projection dérivée validée peut être utilisée comme unique contexte pour une IA **uniquement sous conditions explicites** ;
- le wording de l’architecture et, si nécessaire, du state et du pipeline, doit être ajusté pour éviter toute promesse implicite de sécurité non encore outillée.

Conditions minimales attendues à ce stade :
- périmètre déclaré ;
- sources déclarées ;
- fidélité stricte explicitement requise ;
- traçabilité explicite ;
- validation ou garde-fou explicitement posés.

### HUM-03 — Renforcement du contrat minimal produit

Décision humaine intégrée : **Option B pour cette itération**, avec ouverture explicite vers une évolution future vers une structuration de type C ou A si les itérations suivantes le justifient.

Conséquence d’arbitrage :
- pour cette itération, le renforcement doit passer **prioritairement par les blocs déjà existants** du contrat minimal ;
- cette décision **ne fige pas** la structure cible ;
- les prochains challenges de ce pipeline pourront continuer à enrichir le modèle et, si utile, faire émerger ultérieurement un bloc dédié plus explicite.

### HUM-04 — Liste prioritaire de validateurs

Décision humaine intégrée : **Option B**.

Conséquence d’arbitrage :
- il faut cadrer une **courte liste prioritaire** de validateurs à forte valeur ;
- il n’est **pas** demandé d’industrialiser immédiatement un ensemble complet de validateurs.

Short-list prioritaire retenue comme cible de cadrage :
- `derived_projection_conformance`
- `minimum_contract_conformance`
- `runtime_policy_conformance`

Le sujet `release_lineage` reste pertinent, mais peut être traité après cette première short-list si le séquencement l’exige.

---

## Findings consolidés

| Finding ID | Sujet | Qualification consolidée | Niveau de consensus |
|---|---|---|---|
| PFARB-F01 | Contrat minimal produit pas assez probant sur certains invariants critiques | confirmé | strong |
| PFARB-F02 | Usage fort des projections dérivées trop ambitieux au regard de l’outillage réel | confirmé | strong |
| PFARB-F03 | Trou de gouvernance current / manifest / release | confirmé | strong |
| PFARB-F04 | Multi-IA readiness encore trop déclarative | confirmé mais non bloquant au même niveau | medium |
| PFARB-F05 | Handoff contract vers instanciation encore implicite | confirmé | medium |
| PFARB-F06 | Pipeline V0 cohérent mais pas encore assez outillé | confirmé | strong |
| PFARB-F07 | Risque de duplication normative par la factory | infirmé comme risque actuel majeur | strong |

---

## Décisions consolidées

### PFARB-DEC-01
- **Sujet**: compatibilité forte du contrat minimal produit
- **Décision**: `retained_now`
- **Lieu principal de traitement**: `architecture`
- **Lieu(x) secondaire(s)**: `validator/tooling`
- **Priorité**: `élevé`
- **Justification**: le contrat minimal existe déjà, mais il ne rend pas encore assez auditables certains invariants critiques du produit aval.
- **Arbitrage de mise en œuvre**: pour cette itération, le renforcement doit passer prioritairement par les blocs déjà existants.
- **Ouverture explicite**: une évolution ultérieure vers une structuration plus explicite reste possible si les prochaines itérations la justifient.

### PFARB-DEC-02
- **Sujet**: niveau de promesse opérationnelle des projections dérivées
- **Décision**: `retained_now`
- **Lieu principal de traitement**: `architecture`
- **Lieu(x) secondaire(s)**: `state`, `pipeline`, `validator/tooling`
- **Priorité**: `élevé`
- **Justification**: l’usage fort des projections dérivées doit être conditionné explicitement tant que l’outillage n’est pas complètement fermé.
- **Arbitrage de mise en œuvre**: Option B retenue — autorisation uniquement sous conditions explicites.

### PFARB-DEC-03
- **Sujet**: fermeture de gouvernance current / manifest / release
- **Décision**: `retained_now`
- **Lieu principal de traitement**: `manifest/release governance`
- **Lieu(x) secondaire(s)**: `state`, `pipeline`
- **Priorité**: `élevé`
- **Justification**: la coexistence actuelle entre présence en `current/` et absence du manifest officiel doit être refermée.
- **Arbitrage de mise en œuvre**: la fermeture doit être réalisée lors de la prochaine release de `platform_factory_architecture.yaml`, en fin de pipeline.

### PFARB-DEC-04
- **Sujet**: multi-IA readiness
- **Décision**: `deferred`
- **Lieu principal de traitement**: `state`
- **Lieu(x) secondaire(s)**: `architecture`, `pipeline`
- **Priorité**: `modéré`
- **Justification**: le sujet est réel mais ne doit pas conduire à surcharger la V0 avec un protocole complet dès maintenant.
- **Arbitrage de mise en œuvre**: l’exigence reste première, mais la formulation doit rester honnête sur le niveau réel de maturité.

### PFARB-DEC-05
- **Sujet**: handoff contract factory → instanciation
- **Décision**: `deferred`
- **Lieu principal de traitement**: `architecture`
- **Lieu(x) secondaire(s)**: `pipeline`
- **Priorité**: `modéré`
- **Justification**: le manque est réel mais ne bloque pas le premier patch structurant.
- **Arbitrage de mise en œuvre**: amélioration différée, à reprendre après fermeture des sujets normatifs et de gouvernance prioritaires.

### PFARB-DEC-06
- **Sujet**: validateurs prioritaires
- **Décision**: `retained_now`
- **Lieu principal de traitement**: `validator/tooling`
- **Lieu(x) secondaire(s)**: `pipeline`, `state`
- **Priorité**: `modéré`
- **Justification**: une courte liste prioritaire doit être cadrée pour réduire la dépendance à une validation purement rédactionnelle.
- **Arbitrage de mise en œuvre**: Option B retenue — short-list limitée et à forte valeur.

### PFARB-DEC-07
- **Sujet**: risque de duplication normative par la factory
- **Décision**: `rejected`
- **Lieu principal de traitement**: `none`
- **Priorité**: `faible`
- **Justification**: la baseline actuelle ne montre pas de dérive majeure de duplication normative.

---

## Points retenus

1. Renforcer la capacité de la factory à **prouver** la conformité forte du produit aval.
2. Conditionner explicitement l’usage fort des projections dérivées.
3. Fermer la gouvernance du sujet `current / manifest / release` au prochain cycle de release concerné.
4. Cadrer une courte liste prioritaire de validateurs à forte valeur.
5. Préserver strictement la séparation entre :
   - socle canonique ;
   - architecture prescriptive ;
   - state constatif ;
   - pipeline, validateurs et gouvernance transverse.

## Points rejetés

1. Toute tentative de réécrire le socle canonique primaire dans la factory.
2. Toute sur-correction qui ferait passer artificiellement la V0 pour un framework déjà complètement outillé.
3. Toute promesse implicite selon laquelle une projection dérivée serait déjà sûre sans condition explicite.

## Points différés

1. Protocole multi-IA complet.
2. Handoff contract complet factory → instanciation.
3. Schémas fins exhaustifs du manifest, de la configuration, du packaging et de la typologie runtime.
4. Implémentation complète d’une famille étendue de validateurs.

## Points hors périmètre

1. Design détaillé d’une application instanciée particulière.
2. Contenu spécifique domaine.
3. Pipeline d’instanciation complet, au-delà de l’interface minimale à prévoir.

---

## Répartition par lieu de correction

### Architecture
- renforcement des blocs existants du contrat minimal produit ;
- limitation ou conditionnement explicite de l’usage fort des projections dérivées ;
- éventuel enrichissement futur plus structuré si les itérations suivantes le justifient.

### State
- honnêteté accrue sur la maturité réelle ;
- mise en cohérence avec les arbitrages sur projections dérivées et multi-IA.

### Pipeline
- rappel explicite du traitement du sujet manifest/release au bon moment de fin de pipeline ;
- meilleure articulation avec les validateurs prioritaires attendus ;
- éventuel cadrage des préconditions d’usage des projections dérivées.

### Validator / tooling
- cadrage prioritaire de :
  - `derived_projection_conformance`
  - `minimum_contract_conformance`
  - `runtime_policy_conformance`

### Manifest / release governance
- fermeture officielle du statut des artefacts `platform_factory` lors de la prochaine release concernée, conformément à la décision humaine intégrée HUM-01.

---

## Séquencement recommandé pour la suite

1. Utiliser le présent arbitrage canonique comme base unique du **STAGE_03_FACTORY_PATCH_SYNTHESIS**.
2. Produire un patchset borné aux décisions retenues maintenant.
3. Valider ce patchset sans ouvrir les sujets explicitement différés.
4. Préparer le traitement du sujet manifest/release dans le cycle de release concerné en fin de pipeline, et non par modification directe hors séquence.

---

## Conclusion canonique du stage 02

Le stage 02 est considéré comme **consolidé et fermé**.

La ligne retenue est la suivante :
- corriger maintenant ce qui ferme un risque réel ;
- préserver une V0 sobre et honnête ;
- maintenir ouverte la capacité d’enrichissement lors des prochaines itérations ;
- utiliser ce fichier comme unique base canonique pour le stage 03.
