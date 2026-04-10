# Arbitrage canonique consolidé — Platform Factory V0.3

## arbitrage_run_id
`PFARB_CONSOLIDATION_20260410_PPLX_FINAL`

## Date
2026-04-10

## Statut
Consolidation finale — approuvée par décision humaine explicite.

---

## Challenge reports considérés

| ID | Fichier |
|---|---|
| CR-Nemotron | `docs/pipelines/platform_factory/work/01_challenge/challenge_report_01_Nemotron.md` |
| CR-GPT54 | `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_GPT54_8KQ2.md` |
| CR-PPLX | `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PPLX_7KQ2.md` |

## Arbitrage reports considérés

| ID | Fichier |
|---|---|
| ARB-GPT54 | `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage_PFARB_20260410_GPT54_Q7M4.md` |
| ARB-PPLX-M3F8 | `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage_PFARB_20260410_PPLX_M3F8.md` |
| ARB-PPLX-R7M4 | `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage_PFARB_20260410_PPLX_R7M4.md` |

---

## Résumé exécutif

La baseline V0.3 de la Platform Factory est conceptuellement bien placée, honnête sur son immaturité V0, et suffisamment structurée pour entrer en gouvernance de pipeline. Elle ne viole aucun invariant constitutionnel de façon active. Ses problèmes portent exclusivement sur la fermeture des chaînes de preuve, la cohérence interne architecture/state, et la gouvernance release/manifest.

Les trois challenge reports et les trois arbitrage reports convergent massivement, sans contradiction majeure. CR-Nemotron est le plus précis sur le détail normatif. Les axes de décision sont partagés à consensus fort sur tous les points critiques et élevés.

**Note de gouvernance manifest** : la release `PLATFORM_FACTORY_RELEASE_2026_04_10_R01` est déjà manifestée dans `docs/cores/releases/PLATFORM_FACTORY_RELEASE_2026_04_10_R01/manifest.yaml` (statut `RELEASE_CANDIDATE`, `promotion_candidate: true`). La gouvernance release n'est donc pas totalement ouverte. La fenêtre résiduelle concerne uniquement la promotion vers `docs/cores/current/`, qui reste pendante à STAGE_08 comme prévu par le pipeline. Aucun nouveau fichier manifest n'est créé par ce patch — le state est mis à jour pour refléter cette réalité (CONS-10).

La consolidation retient **12 décisions immédiates**, en **diffère 3 explicitement**, et classe **2 sujets hors périmètre factory**.

---

## Décisions consolidées — Points retenus

---

### CONS-01 — Rendre `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION` explicitement vérifiables dans le contrat minimal

- **Élément concerné** : `produced_application_minimum_contract.minimum_validation_contract.minimum_axes` + `minimum_observability_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Aucune obligation explicite dans le contrat minimal ne contraint une application produite à prouver qu'elle est 100 % locale et sans génération runtime. L'axe `runtime_policy_conformance` est un label creux. Le signal `constitutional_invariants_checked` est non auditable.
- **Statut final** : `retained`
- **Gravité** : critique
- **Justification consolidée** : Consensus fort dans les 3 challenge reports (CR-Nemotron C1/C2/C3, CR-GPT54 Risque 1, CR-PPLX Axe 1/Axe 4) et dans les 3 arbitrage reports. Sans correction, la factory ne peut pas garantir sa fonction fondamentale : une application produite constitutionnellement compatible.
- **Dépendance** : liée à CONS-03 (conformance matrix) et CONS-05 (runtime_policy_conformance)
- **Lieu probable de correction** : architecture → `produced_application_minimum_contract`, `minimum_validation_contract`, `minimum_observability_contract`
- **Niveau de consensus final** : strong

---

### CONS-02 — Résoudre la contradiction `usage_as_sole_context` dans `execution_projection_contract`

- **Élément concerné** : `execution_projection_contract` — tension entre `usage_as_sole_context: blocked` et `rule_of_use` autorisant le contexte unique si validé
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Deux énoncés contradictoires coexistent dans le même bloc. Une IA peut interpréter les deux sens.
- **Statut final** : `retained`
- **Gravité** : élevé
- **Justification consolidée** : Consensus fort dans les 3 challenge reports et les 3 arbitrage reports. Correction de wording pure, sans changement de fond. Le blocage V0 est correct et doit rester, mais doit être distingué de la cible architecturale.
- **Correction** : clarifier que `rule_of_use` décrit le régime cible ; ajouter `usage_as_sole_context_unblock_conditions` listant les prérequis de déblocage (validator implémenté, régénération déterministe, matrice de conformité présente).
- **Lieu probable de correction** : architecture → `execution_projection_contract` + state → description de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
- **Niveau de consensus final** : strong

---

### CONS-03 — Enregistrer `constitutional_conformance_matrix.yaml` comme blocker et annoter la référence dans l'architecture

- **Élément concerné** : `conformance_matrix_ref` (deux emplacements dans l'architecture) + state
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : Le fichier `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` est référencé mais absent. Non listé comme blocker dans le state.
- **Statut final** : `retained`
- **Gravité** : élevé
- **Justification consolidée** : Consensus fort (3/3 challenge reports, 3/3 arbitrage reports). Décision retenue : enregistrer `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` dans le state avec exit condition explicite ; ne pas créer le fichier par ce patch ; annoter les champs `conformance_matrix_ref` dans l'architecture comme `# pending: PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT`.
- **Lieu probable de correction** : state → `blockers` + architecture → annotation sur `conformance_matrix_ref`
- **Niveau de consensus final** : strong

---

### CONS-04 — Ajouter `authority_rank: factory_layer` dans les métadonnées des artefacts factory

- **Élément concerné** : `metadata` de `platform_factory_architecture.yaml` et `platform_factory_state.yaml`
- **Localisation** : les deux artefacts factory
- **Problème** : Ces artefacts sont dans `docs/cores/current/` sans champ signalant qu'ils ne sont pas des canoniques primaires. Risque de confusion d'autorité documenté par scénario adversarial (Scénario D dans CR-Nemotron et CR-GPT54).
- **Statut final** : `retained`
- **Gravité** : élevé
- **Justification consolidée** : Problème à consensus fort (3/3 rapports). Retenu dans ARB-PPLX-R7M4 (ARB-C1) et ARB-PPLX-M3F8 (CORR-ARB-04). Rejeté initialement par ARB-GPT54 comme "taxonomie non gouvernée" — rejeté en consolidation car le risque documenté justifie la correction minimale. Forme retenue : `authority_rank: factory_layer`.
- **Lieu probable de correction** : architecture + state → `metadata`
- **Niveau de consensus final** : medium → tranché

---

### CONS-05 — Définir le contenu de `runtime_policy_conformance` (Option A — liste minimale)

- **Élément concerné** : `minimum_validation_contract.minimum_axes.runtime_policy_conformance`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Axe de validation listé sans critère, périmètre ou contenu déterministe.
- **Statut final** : `retained`
- **Gravité** : élevé
- **Justification consolidée** : Lié à CONS-01. Décision humaine DISC-01 tranchée : Option A — liste minimale non exhaustive de 5 items déterministes. Liste retenue :
  1. absence de dépendance réseau au runtime (vérifiable statiquement)
  2. absence de génération de contenu ou de feedback à la volée
  3. conformité au régime d'autonomie déclaré dans le manifest de l'application
  4. absence d'appel implicite à un modèle de langage en usage
  5. runtime entrypoint déclaré et traçable
- **Note** : liste non exhaustive, à compléter lors de la définition du validator.
- **Lieu probable de correction** : architecture → `minimum_validation_contract`
- **Niveau de consensus final** : medium → tranché (DISC-01 Option A)

---

### CONS-06 — Enregistrer `bootstrap_contract: TBD` comme blocker explicite

- **Élément concerné** : `runtime_entrypoint_contract.bootstrap_contract`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : Champ obligatoire TBD dans l'architecture, non tracé comme blocker dans le state. Aucune application ne peut passer la validation complète du contrat minimal tant que ce champ n'est pas défini.
- **Statut final** : `retained`
- **Gravité** : élevé
- **Justification consolidée** : Retenu dans ARB-PPLX-M3F8 (ARB-PF-07) et ARB-PPLX-R7M4 (ARB-E1). Correction minimale et propre.
- **Correction** : ajouter `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` dans le state avec exit condition : définition de la typologie exacte des runtimes d'application Learn-it.
- **Lieu probable de correction** : state → `blockers`
- **Niveau de consensus final** : medium → retenu

---

### CONS-07 — Recaler le state sur la décision d'emplacement des projections (ARB-04) et corriger les surdéclarations mineures

- **Élément concerné** : `derived_projection_conformity_status.missing`, `assessed_scope.excludes`, `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`, `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : `storage_location_decision` figure encore dans les éléments manquants alors que la décision ARB-04 l'a actée. `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` est classé `capabilities_present` alors qu'il s'agit d'une intention non outillée.
- **Statut final** : `retained`
- **Gravité** : modéré
- **Corrections** :
  - retirer `storage_location_decision` de `derived_projection_conformity_status.missing`
  - mettre à jour `assessed_scope.excludes` si nécessaire
  - déplacer `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` de `capabilities_present` vers `capabilities_partial` avec description : "intent posé, prompts de lancement définis, outillage d'exécution absent"
  - ajuster la description de `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` : "emplacement décidé (ARB-04), répertoire non encore créé, aucune projection stockée, outillage absent"
- **Lieu probable de correction** : state
- **Niveau de consensus final** : strong

---

### CONS-08 — Renforcer la description de `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` comme blocker opérationnel

- **Élément concerné** : `known_gaps.PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : La description actuelle minimise l'impact. L'absence des protocoles d'assemblage et de résolution de conflit constitue une impossibilité opérationnelle pour tout travail multi-IA réel, non une simple sous-optimalité.
- **Statut final** : `retained`
- **Gravité** : élevé
- **Correction** : mettre à jour la description pour y indiquer explicitement "blocker opérationnel pour tout travail multi-IA réel — aucun protocole d'assemblage, de décomposition de tâche ou de résolution de conflit n'existe ; l'usage parallèle multi-IA sans ce protocole expose à des collisions et à des dérivences normatives non détectées".
- **Lieu probable de correction** : state → `known_gaps`
- **Niveau de consensus final** : strong

---

### CONS-09 — Renforcer la description de `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent` avec risque explicite sur les projections

- **Élément concerné** : `capabilities_absent.PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : Le validator est absent mais le state ne lie pas explicitement cette absence au risque de dérive normative sur les projections dérivées — une projection peut être taguée `validation_status: validated` sans aucun critère déterministe.
- **Statut final** : `retained`
- **Gravité** : élevé
- **Correction** : enrichir la description pour y indiquer explicitement que l'absence de validator rend non déterministe tout `validation_status: validated` sur une projection dérivée, et qu'aucune projection ne peut être considérée comme validée de façon auditable tant que ce validator n'est pas implémenté.
- **Lieu probable de correction** : state → `capabilities_absent`
- **Niveau de consensus final** : medium → retenu

---

### CONS-10 — Mettre à jour la description du blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` pour refléter la réalité de gouvernance

- **Élément concerné** : `blockers.PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : La description ne reflète pas que la release `PLATFORM_FACTORY_RELEASE_2026_04_10_R01` est déjà manifestée dans `docs/cores/releases/`. Le risque résiduel est uniquement la promotion vers `current/`, pas l'absence totale de manifest.
- **Statut final** : `retained`
- **Gravité** : modéré
- **Décision humaine DISC-02** : Option C — documenter dans le state, aucun nouveau fichier manifest créé par ce patch. À revoir au prochain challenge si nécessaire.
- **Correction** : mettre à jour la description du blocker pour préciser que la release est manifestée dans `docs/cores/releases/PLATFORM_FACTORY_RELEASE_2026_04_10_R01/manifest.yaml` (statut `RELEASE_CANDIDATE`, `promotion_candidate: true`) et que la fermeture attendue est la promotion STAGE_08 uniquement.
- **Lieu probable de correction** : state → `blockers`
- **Niveau de consensus final** : strong (sur le problème) → tranché (DISC-02 Option C)

---

### CONS-11 — Mettre à jour la description de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` pour refléter la distinction régime cible / politique V0

- **Élément concerné** : `capabilities_present.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : La description actuelle ne distingue pas explicitement le régime cible (usage en contexte unique si validé) de la politique V0 actuellement bloquée. Lié à CONS-02.
- **Statut final** : `retained`
- **Gravité** : élevé
- **Correction** : mettre à jour la description pour y indiquer "règle définie ; usage en contexte unique = régime cible, actuellement bloqué (V0) — voir `execution_projection_contract.usage_as_sole_context_unblock_conditions` dans l'architecture".
- **Lieu probable de correction** : state → `capabilities_present`
- **Niveau de consensus final** : strong

---

### CONS-12 — Annoter les champs `conformance_matrix_ref` dans l'architecture comme pending blocker

- **Élément concerné** : `mandatory_fields_per_projection.conformance_matrix_ref` + `dependencies_to_constitution.constitutional_conformance_matrix_ref`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Ces deux champs référencent un fichier absent sans indiquer que c'est un blocker connu. Lié à CONS-03.
- **Statut final** : `retained`
- **Gravité** : élevé
- **Correction** : ajouter une annotation inline `# pending: PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` sur les deux champs concernés. Ne pas supprimer la référence pour préserver le design intent.
- **Lieu probable de correction** : architecture
- **Niveau de consensus final** : strong

---

## Points rejetés

### REJ-01 — Reclassement de `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` en capacité absente

- **Source** : CR-Nemotron (M3)
- **Statut final** : `rejected`
- **Gravité** : faible
- **Justification consolidée** : La décision d'emplacement est bien prise (ARB-04). Ce qui manque est l'outillage, pas la décision. La correction juste est un ajustement de description (CONS-07), pas un reclassement.
- **Niveau de consensus final** : medium

### REJ-02 — Rejet de la position ARB-GPT54 sur `authority_rank` comme "taxonomie non gouvernée"

- **Source** : ARB-GPT54 (REJ-01)
- **Statut final** : `rejected` (cette position de rejet est elle-même rejetée — voir CONS-04)
- **Justification consolidée** : Les deux autres arbitrage reports ont retenu la correction. Le risque documenté par scénario adversarial justifie la correction minimale. La consolidation tranche en faveur du retenu.
- **Niveau de consensus final** : conflicting → tranché

---

## Points différés

| ID | Sujet | Justification | Lieu de déferrement |
|---|---|---|---|
| DIFF-01 | Protocole multi-IA complet (assemblage, granularité, résolution de conflit) | Spec dédiée requise avant correction architecturale | Itération suivante avec spec dédiée |
| DIFF-02 | Vérifiabilité des `reproducibility_fingerprints` (dérive silencieuse) | Différé à la même itération que l'implémentation du validator | Itération validators |
| DIFF-03 | Rappel `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` dans chaîne PF_CHAIN_03→05 | Dépend de CONS-02 — à traiter après résolution de la contradiction `usage_as_sole_context` | Après patch CONS-02 stabilisé |

---

## Points hors périmètre factory

| Sujet | Justification |
|---|---|
| Comportement runtime détaillé d'une application spécifique | Hors scope factory — relève du futur pipeline d'instanciation |
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` et autres invariants runtime domaine | Hors scope factory — à annoter comme tel dans l'architecture si nécessaire |
| Contenu du graph domaine ou logique pédagogique | Hors scope par construction |
| Logique détaillée du futur pipeline d'instanciation domaine | Hors périmètre factory |

---

## Corrections à appliquer en STAGE_03 — tableau de synthèse

| Code | Correction | Artefact(s) | Gravité | Statut |
|---|---|---|---|---|
| COR-A | Ajouter axes `constitutional_invariants_runtime_local` + `no_runtime_content_generation_proof` dans `minimum_validation_contract` | `platform_factory_architecture.yaml` | critique | patchable |
| COR-A' | Définir `runtime_policy_conformance` (liste 5 items, CONS-05) | `platform_factory_architecture.yaml` | élevé | patchable |
| COR-A'' | Rattacher `constitutional_invariants_checked` à une liste d'invariants + protocole dans `minimum_observability_contract` | `platform_factory_architecture.yaml` | critique | patchable |
| COR-B | Clarifier `usage_as_sole_context` / `rule_of_use` + ajouter `usage_as_sole_context_unblock_conditions` | `platform_factory_architecture.yaml` | élevé | patchable |
| COR-B' | Mettre à jour description `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` (CONS-11) | `platform_factory_state.yaml` | élevé | patchable |
| COR-C | Ajouter blocker `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` (CONS-03) | `platform_factory_state.yaml` | élevé | patchable |
| COR-C' | Annoter `conformance_matrix_ref` (CONS-12) | `platform_factory_architecture.yaml` | élevé | patchable |
| COR-C'' | Renforcer description `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent` (CONS-09) | `platform_factory_state.yaml` | élevé | patchable |
| COR-D | Ajouter `authority_rank: factory_layer` dans `metadata` des deux artefacts (CONS-04) | `platform_factory_architecture.yaml` + `platform_factory_state.yaml` | élevé | patchable |
| COR-E | Renforcer description `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` (CONS-08) | `platform_factory_state.yaml` | élevé | patchable |
| COR-F | Ajouter blocker `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` (CONS-06) | `platform_factory_state.yaml` | élevé | patchable |
| COR-G | Déplacer `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` vers `capabilities_partial` (CONS-07) | `platform_factory_state.yaml` | modéré | patchable |
| COR-H | Resynchroniser state sur ARB-04 — retirer `storage_location_decision` des manquants (CONS-07) | `platform_factory_state.yaml` | modéré | patchable |
| COR-I | Mettre à jour description `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` (CONS-10) | `platform_factory_state.yaml` | modéré | patchable |

---

## Séquencement recommandé du patch (STAGE_03)

1. **En premier** — COR-D (`authority_rank`) : protège la cohérence de lecture des artefacts avant toute autre modification
2. **En deuxième** — COR-A + COR-A' + COR-A'' (conformité constitutionnelle contrat minimal) : bloc critique, fondement de la factory
3. **En troisième** — COR-B + COR-B' (contradiction `usage_as_sole_context`) : clarifie le régime des projections
4. **En quatrième** — COR-C + COR-C' + COR-C'' (blockers conformance matrix + validators)
5. **En cinquième** — COR-E + COR-F + COR-G + COR-H + COR-I (corrections state restantes)

---

## Répartition par lieu de correction

| Lieu | Corrections |
|---|---|
| Architecture seule | COR-A, COR-A', COR-A'', COR-B |
| State seul | COR-B', COR-C, COR-C'', COR-E, COR-F, COR-G, COR-H, COR-I |
| Architecture + State | COR-C' (annotation arch + blocker state), COR-D (metadata des deux) |

---

## Priorités de patch

| Priorité | Corrections |
|---|---|
| critique | COR-A, COR-A'', CONS-01 |
| élevé | COR-A', COR-B, COR-B', COR-C, COR-C', COR-C'', COR-D, COR-E, COR-F |
| modéré | COR-G, COR-H, COR-I |
| différé | DIFF-01, DIFF-02, DIFF-03 |
