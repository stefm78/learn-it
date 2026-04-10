# Proposition d'Arbitrage — Platform Factory Pipeline STAGE_02

## arbitrage_run_id
`PFARB_20260410_PPLX_R7M4`

## Date
2026-04-10

## Statut
Proposition d'arbitrage indépendante — contribution à consolidation finale humaine-assistée

---

## Challenge reports considérés

| ID | Fichier |
|---|---|
| CR-1 | `challenge_report_01_Nemotron.md` |
| CR-2 | `challenge_report_PFCHAL_20260410_GPT54_8KQ2.md` |
| CR-3 | `challenge_report_PFCHAL_20260410_PPLX_7KQ2.md` (rapport de la même IA, run précédente) |

---

## Résumé exécutif

Les trois challenge reports convergent massivement. Aucune contradiction majeure n'oppose les trois rapports sur les findings prioritaires. La convergence est forte sur les cinq zones de risque structurel :

1. **Chaîne de preuve constitutionnelle incomplète** — `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION` ne sont pas auditablement vérifiés dans le contrat minimal d'application produite.
2. **Projections dérivées non opérationnelles** — Contradiction interne `usage_as_sole_context: blocked` vs `rule_of_use` autorisant, validator absent, matrice de conformité absente.
3. **Gouvernance release/manifest incomplète** — Artefacts factory dans `current/` mais hors manifest officiel, sans différenciation d'autorité dans les métadonnées.
4. **Multi-IA déclaratif sans protocole** — Principes présents, mécanismes d'assemblage et de résolution de conflit absents.
5. **Légère surdéclaration de maturité dans le state** — Deux capacités classées présentes/partielles au-delà de leur maturité réelle.

L'arbitrage propose de retenir 12 décisions immédiates, d'en différer 3 explicitement, et de classer 2 points hors périmètre factory. Aucun finding n'est rejeté comme infirmé.

---

## Synthèse des constats convergents

### Convergence forte (3/3 rapports)

- `INV_RUNTIME_FULLY_LOCAL` non capturé dans le contrat minimal (critique)
- `INV_NO_RUNTIME_CONTENT_GENERATION` non capturé dans le contrat minimal (critique)
- `constitutional_invariants_checked` non auditable (critique)
- Contradiction `usage_as_sole_context: blocked` vs `rule_of_use` (élevé)
- `constitutional_conformance_matrix.yaml` absent mais référencé (élevé)
- Validator `validate_platform_factory_patchset.py` non implémenté (élevé)
- Gouvernance manifest/current incomplète — artefacts factory hors manifest officiel (élevé)
- Multi-IA : protocoles d'assemblage et de résolution de conflit absents (élevé)
- Surdéclaration `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` (modéré)

### Convergence moyenne (2/3 rapports)

- `runtime_policy_conformance` non défini dans `minimum_validation_contract` (élevé)
- `bootstrap_contract: TBD` non tracé comme blocker (élevé)
- Absence de champ `authority_rank` dans les métadonnées factory (élevé)
- Désynchronisation state sur `storage_location_decision` (modéré)

### Finding propre à CR-1 / CR-3 (non infirmé par CR-2)

- `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` partiellement exposé dans la chaîne PF_CHAIN_03→05 (élevé)
- `reproducibility_fingerprints` non vérifiables — dérive silencieuse possible (modéré)

### Finding propre à CR-2 (non infirmé par CR-1 / CR-3)

- Divergence entre `assessed_scope.excludes.exact_projection_storage_location` et la décision ARB-04 déjà actée (modéré)

---

## Propositions d'arbitrage par thème

---

### Thème A — Conformité constitutionnelle dans le contrat minimal

#### ARB-A1 — Rendre `INV_RUNTIME_FULLY_LOCAL` explicitement requis dans le contrat minimal

- **Élément** : `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : L'axe `runtime_policy_conformance` est un label sans contenu. Aucune obligation ne requiert de prouver l'absence de dépendance réseau runtime. Une application produite peut violer `INV_RUNTIME_FULLY_LOCAL` sans être détectée.
- **Sources** : CR-1 (C1, C3), CR-2 (Risque 1, PF-CHAL-01), CR-3 (Axe 1, COR-01)
- **Statut proposé** : `retained_now`
- **Gravité** : critique
- **Justification** : Invariant constitutionnel fondateur. Le risque de violation silencieuse est réel et documenté par scénario adversarial (Scénario B dans CR-1/CR-3, Scénario B dans CR-2). Ce n'est pas une exigence prématurée V0 — c'est une exigence minimale de toute couche released qui prétend produire des applications Learn-it conformes.
- **Impact si non traité** : La factory ne peut pas garantir sa fonction première. Une application produite peut violer l'invariant constitutionnel le plus fondamental sans déclencher d'alerte.
- **Lieu principal** : architecture → `produced_application_minimum_contract`
- **Lieux secondaires** : architecture → `minimum_observability_contract`
- **Pré-condition** : Aucune — correction de wording et d'axes, ne requiert pas de tooling.
- **Niveau de consensus** : strong

#### ARB-A2 — Rendre `INV_NO_RUNTIME_CONTENT_GENERATION` explicitement requis dans le contrat minimal

- **Élément** : `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Aucune obligation dans le contrat minimal ne requiert de prouver l'absence de génération de contenu à la volée. `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION` n'est pas capturé.
- **Sources** : CR-1 (C2, C3), CR-2 (Risque 1, PF-CHAL-01), CR-3 (COR-01)
- **Statut proposé** : `retained_now`
- **Gravité** : critique
- **Justification** : Même raisonnement qu'ARB-A1. Les deux invariants forment une paire indissociable pour la conformité constitutionnelle runtime.
- **Impact si non traité** : Une application peut générer du feedback à la volée, violer `INV_NO_RUNTIME_CONTENT_GENERATION`, et passer toute validation factory.
- **Lieu principal** : architecture → `produced_application_minimum_contract`
- **Niveau de consensus** : strong

#### ARB-A3 — Définir le contenu de `runtime_policy_conformance`

- **Élément** : `minimum_validation_contract.minimum_axes.runtime_policy_conformance`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Axe de validation listé sans aucun critère, périmètre ou contenu déterministe. Une IA validant une application produite n'a aucune instruction.
- **Sources** : CR-1 (E2), CR-3 (COR-04)
- **Statut proposé** : `retained_now`
- **Gravité** : élevé
- **Justification** : ARB-A1 et ARB-A2 nécessitent que `runtime_policy_conformance` soit redéfini. Les trois corrections sont liées et doivent être traitées ensemble.
- **Impact si non traité** : Les axes ARB-A1 et ARB-A2 restent creux même après ajout de labels.
- **Lieu principal** : architecture → `minimum_validation_contract`
- **Dépendance** : ARB-A1, ARB-A2
- **Niveau de consensus** : medium (explicite dans 2/3, implicite dans CR-2)

#### ARB-A4 — Rendre `constitutional_invariants_checked` auditable

- **Élément** : `minimum_observability_contract.constitutional_invariants_checked`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Le signal existe mais sans définition de quels invariants, selon quel artefact, selon quel protocole. Il est actuellement non auditable.
- **Sources** : CR-1 (C3, Problème 4.1), CR-2 (Risque 1), CR-3 (COR-01)
- **Statut proposé** : `retained_now`
- **Gravité** : critique
- **Justification** : La chaîne de preuve constitutionnelle ne peut être fermée sans que ce signal soit rattaché à une liste d'invariants vérifiés et à un protocole.
- **Lieu principal** : architecture → `minimum_observability_contract`
- **Dépendance** : ARB-A1, ARB-A2, ARB-A3
- **Niveau de consensus** : strong

---

### Thème B — Projections dérivées

#### ARB-B1 — Résoudre la contradiction `usage_as_sole_context`

- **Élément** : `execution_projection_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : `usage_as_sole_context: blocked` et `rule_of_use` (capacité cible = contexte unique autorisé si validé) coexistent sans clause de levée ni distinction explicite régime-cible / politique-V0.
- **Sources** : CR-1 (E1, Problème 2.1), CR-2 (PF-CHAL-02, Axe 5), CR-3 (COR-02)
- **Statut proposé** : `retained_now`
- **Gravité** : élevé
- **Justification** : Ambiguïté normative qui peut induire n'importe quelle IA en erreur. Correction de wording pure, pas de changement de fond — le bloquage V0 est correct et doit rester, mais doit être distingué de la cible architecturale.
- **Correction** : Clarifier que `rule_of_use` décrit le régime cible; ajouter `usage_as_sole_context_unblock_conditions` listant les prérequis de déblocage (validator implémenté, régénération déterministe, matrice conformité présente).
- **Lieu principal** : architecture → `execution_projection_contract`
- **Lieu secondaire** : state (mettre à jour la description de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`)
- **Niveau de consensus** : strong

#### ARB-B2 — Enregistrer `constitutional_conformance_matrix.yaml` absent comme blocker

- **Élément** : `conformance_matrix_ref` (deux emplacements) + state
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : Le fichier `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` est référencé dans l'architecture à deux endroits mais n'existe pas. Ce n'est pas inscrit comme blocker dans le state.
- **Sources** : CR-1 (E3, Problème 2.3), CR-2 (PF-CHAL-01), CR-3 (COR-03)
- **Statut proposé** : `retained_now`
- **Gravité** : élevé
- **Justification** : Référence morte dans un contrat released. Deux options : créer un squelette minimal, ou enregistrer le manque comme blocker explicite. La deuxième est plus sûre pour ne pas bâcler un artefact critique.
- **Décision proposée** : Enregistrer `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` dans le state avec exit condition explicite; ne pas créer le fichier par patch (réserve cette création pour une tâche dédiée post-arbitrage).
- **Lieu principal** : state → `blockers`
- **Lieu secondaire** : architecture → annotation sur `conformance_matrix_ref` précisant "pending blocker PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT"
- **Niveau de consensus** : strong

#### ARB-B3 — Enregistrer l'absence de protocole de validation des projections comme blocker

- **Élément** : `execution_projection_contract.validation_status` + `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : Aucun critère déterministe ne définit ce que signifie `validation_status: validated` pour une projection. Le validator est absent. Le blocage `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent` le reconnaît, mais sans lien explicite avec le risque sur les projections.
- **Sources** : CR-1 (E5, Problème 5.2), CR-2 (Risque 2)
- **Statut proposé** : `retained_now`
- **Gravité** : élevé
- **Justification** : Lié à ARB-B2. Une projection peut être taguée `validated` sans aucun critère — ce qui est une violation par analogie de `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`.
- **Décision** : Renforcer la description de `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent` dans le state pour y expliciter le risque sur les projections dérivées. Ne pas créer de validator par ce patch.
- **Lieu principal** : state → `capabilities_absent`
- **Niveau de consensus** : medium

---

### Thème C — Gouvernance release / manifest / traçabilité

#### ARB-C1 — Ajouter `authority_rank` dans les métadonnées des artefacts factory

- **Élément** : `metadata` de `platform_factory_architecture.yaml` et `platform_factory_state.yaml`
- **Localisation** : les deux artefacts factory
- **Problème** : Ces artefacts sont dans `docs/cores/current/` sans champ signalant qu'ils ne sont PAS des canoniques primaires. Une IA peut les lire comme ayant la même autorité que `constitution.yaml`.
- **Sources** : CR-1 (E8, Problème 8.1, Scénario D), CR-2 (PF-CHAL-04), CR-3 (COR-07, M5)
- **Statut proposé** : `retained_now`
- **Gravité** : élevé
- **Justification** : Risque de confusion d'autorité documenté par scénario adversarial dans deux rapports. Correction minimale : ajout d'un champ `authority_rank: factory_layer` (ou équivalent) dans les métadonnées.
- **Lieu principal** : architecture + state → `metadata`
- **Niveau de consensus** : strong

#### ARB-C2 — Documenter explicitement la stratégie de fermeture manifest/current dans le pipeline et le state

- **Élément** : `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` + `pipeline.md Rule 3`
- **Localisation** : `platform_factory_state.yaml` + `pipeline.md`
- **Problème** : Les artefacts factory sont dans `current/` mais hors manifest officiel. Le blocker le reconnaît. Mais la stratégie de fermeture (manifest factory dédié ? extension du manifest officiel courant ?) n'est pas arbitrée.
- **Sources** : CR-1 (E8, Problème 8.1), CR-2 (PF-CHAL-04, Risque 3), CR-3 (M4)
- **Statut proposé** : `clarification_required`
- **Gravité** : élevé
- **Justification** : Deux options valides s'affrontent (manifest factory dédié vs extension manifest officiel). L'arbitrage humain doit trancher avant que le pipeline patch puisse proposer une correction.
- **Clarification requise** : Décider entre (A) création d'un `manifest.yaml` factory dédié dans `docs/cores/platform_factory/` ou (B) extension du manifest officiel courant de `docs/cores/current/` avec une section factory.
- **Lieu probable de correction** : pipeline + state + manifest/release governance
- **Niveau de consensus** : strong sur le problème, conflicting sur la solution

#### ARB-C3 — Corriger le classement de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

- **Élément** : `capabilities_present.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : Classé `capabilities_present` avec la description "intent only, not yet tooled". Une intention non outillée n'est pas une capacité présente.
- **Sources** : CR-1 (M2, Surdéclaration 6.1), CR-2 (Axe 6), CR-3 (COR-06)
- **Statut proposé** : `retained_now`
- **Gravité** : modéré
- **Justification** : Surdéclaration légère mais réelle. Simple déplacement vers `capabilities_partial` avec description précisant "intent posé, prompts définis, outillage absent".
- **Lieu principal** : state → déplacer de `capabilities_present` vers `capabilities_partial`
- **Niveau de consensus** : strong

---

### Thème D — Multi-IA en parallèle

#### ARB-D1 — Qualifier honnêtement la readiness multi-IA comme déclarative

- **Élément** : `multi_ia_parallel_readiness_status` + `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : La readiness multi-IA est bien reconnue comme gap, mais l'impact réel — impossibilité opérationnelle et non simple sous-optimalité — n'est pas reflété dans le state.
- **Sources** : CR-1 (E7, Problème 7.1), CR-2 (PF-CHAL-05, Risque 5), CR-3 (Axe 7)
- **Statut proposé** : `retained_now`
- **Gravité** : élevé
- **Justification** : La description doit être mise à jour pour qualifier le gap comme "blocker opérationnel pour tout travail multi-IA réel" plutôt que "amélioration souhaitable". Ne pas corriger l'architecture pour l'instant — cette décision requiert une spec dédiée.
- **Lieu principal** : state → `known_gaps` (renforcement description de `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED`)
- **Niveau de consensus** : strong

#### ARB-D2 — Différer la création des protocoles multi-IA (spec requise)

- **Élément** : `multi_ia_parallel_readiness` — protocoles d'assemblage, granularité modulaire, résolution de conflit
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Protocoles d'assemblage et de résolution de conflit absents dans l'architecture.
- **Sources** : CR-1 (E7, Problèmes 7.1-7.3), CR-2 (PF-CHAL-05), CR-3 (Axe 7)
- **Statut proposé** : `deferred`
- **Gravité** : élevé
- **Justification** : Corriger l'architecture sur ce sujet sans spec dédiée produirait un patch superficiel ou mal placé. La correction juste est de renforcer le wording du gap (ARB-D1) et de créer un travail dédié post-patch.
- **Report assumé** : Correction architecturale différée à une prochaine itération avec spec de protocole multi-IA dédiée.
- **Niveau de consensus** : strong

---

### Thème E — Bootstrap contract et fingerprints

#### ARB-E1 — Enregistrer `bootstrap_contract: TBD` comme blocker explicite

- **Élément** : `runtime_entrypoint_contract.bootstrap_contract`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Problème** : Champ obligatoire déclaré TBD, non tracé comme blocker dans le state. Aucune application ne peut passer la validation complète du contrat minimal tant que ce champ n'est pas défini.
- **Sources** : CR-1 (E4, Problème 4.2), CR-2 (Axe 4), CR-3 (COR-05)
- **Statut proposé** : `retained_now`
- **Gravité** : élevé
- **Justification** : Simple ajout d'un blocker `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` dans le state avec exit condition (définition de la typologie des runtimes). Ne nécessite pas de modifier l'architecture.
- **Lieu principal** : state → `blockers`
- **Niveau de consensus** : medium

#### ARB-E2 — Différer la vérifiabilité des `reproducibility_fingerprints`

- **Élément** : `identity.reproducibility_fingerprints_definition`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : Fingerprints définis mais aucun mécanisme pour détecter leur obsolescence ou invalider une application avec fingerprints périmés.
- **Sources** : CR-1 (M1, Problème 4.3), CR-3 (M1)
- **Statut proposé** : `deferred`
- **Gravité** : modéré
- **Justification** : Problème réel mais non bloquant pour le cycle V0 actuel. La correction requiert une décision sur le validator, qui est déjà reconnu comme absent. Différé à la même itération que l'implémentation des validators.
- **Report assumé** : Différé à la même itération que `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED`.
- **Niveau de consensus** : medium

---

### Thème F — Synchronisation state/architecture

#### ARB-F1 — Resynchroniser le state sur la décision d'emplacement des projections (ARB-04)

- **Élément** : `derived_projection_conformity_status.missing` + `assessed_scope.excludes`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : `storage_location_decision` figure encore dans les éléments manquants alors que la décision ARB-04 l'a actée dans l'architecture. `assessed_scope.excludes` contient `exact_projection_storage_location` qui est désormais obsolète.
- **Sources** : CR-2 (PF-CHAL-03, Axe 2)
- **Statut proposé** : `retained_now`
- **Gravité** : modéré
- **Justification** : Désynchronisation factuelle. Correction directe dans le state.
- **Lieu principal** : state → `derived_projection_conformity_status` + `assessed_scope`
- **Niveau de consensus** : medium (explicite dans CR-2, cohérent avec les autres rapports)

---

### Thème G — Chaîne constitutionnelle `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`

#### ARB-G1 — Ajouter un rappel explicite de l'invariant dans la chaîne PF_CHAIN_03→05

- **Élément** : `transformation_chain` (PF_CHAIN_03 et PF_CHAIN_05)
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : La chaîne génère des projections hors session (correct) mais ne rappelle pas explicitement qu'elles ne peuvent pas être utilisées pour générer un patch à la volée. Si le bloquage `usage_as_sole_context: blocked` est levé un jour, rien dans la chaîne n'empêche la dérive.
- **Sources** : CR-1 (Problème 1.3), CR-3 (COR-02 implicite)
- **Statut proposé** : `deferred`
- **Gravité** : élevé
- **Justification** : Correction valide mais dépendante de ARB-B1 (résolution contradiction `usage_as_sole_context`). Différer à la même itération de patch, après résolution de ARB-B1.
- **Dépendance** : ARB-B1
- **Lieu principal** : architecture → `transformation_chain`
- **Niveau de consensus** : medium

---

## Points retenus (retained_now)

| ID | Thème | Gravité | Lieu principal |
|---|---|---|---|
| ARB-A1 | `INV_RUNTIME_FULLY_LOCAL` dans contrat minimal | critique | architecture |
| ARB-A2 | `INV_NO_RUNTIME_CONTENT_GENERATION` dans contrat minimal | critique | architecture |
| ARB-A3 | Définir `runtime_policy_conformance` | élevé | architecture |
| ARB-A4 | Rendre `constitutional_invariants_checked` auditable | critique | architecture |
| ARB-B1 | Résoudre contradiction `usage_as_sole_context` | élevé | architecture + state |
| ARB-B2 | Blocker `constitutional_conformance_matrix.yaml` absent | élevé | state |
| ARB-B3 | Renforcer description validator projections absent | élevé | state |
| ARB-C1 | Ajouter `authority_rank` dans métadonnées | élevé | architecture + state |
| ARB-C3 | Reclasser `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | modéré | state |
| ARB-D1 | Qualifier gap multi-IA comme blocker opérationnel | élevé | state |
| ARB-E1 | Blocker `bootstrap_contract: TBD` | élevé | state |
| ARB-F1 | Resynchroniser state sur décision ARB-04 emplacement projections | modéré | state |

---

## Points différés (deferred)

| ID | Thème | Gravité | Justification du report |
|---|---|---|---|
| ARB-D2 | Protocoles multi-IA | élevé | Spec dédiée requise avant correction architecturale |
| ARB-E2 | Vérifiabilité fingerprints | modéré | Différé à l'itération validators |
| ARB-G1 | Rappel invariant patch dans chaîne PF_CHAIN_03→05 | élevé | Dépend de ARB-B1 |

---

## Points nécessitant clarification préalable (clarification_required)

| ID | Thème | Question ouverte |
|---|---|---|
| ARB-C2 | Stratégie manifest/current | Choisir entre manifest factory dédié ou extension manifest officiel courant |

---

## Points rejetés

Aucun finding des trois rapports n'est rejeté comme infirmé. Tous les findings ont un support factuel dans les artefacts.

---

## Points hors périmètre factory

| Sujet | Justification |
|---|---|
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` et autres invariants runtime domaine | Hors scope factory — à documenter comme tel dans l'architecture (annotation explicite) mais non corrigible par ce pipeline |
| Comportement runtime détaillé d'une application instanciée | Relève du futur pipeline d'instanciation |

---

## Points sans consensus ou nécessitant discussion finale

| Sujet | Nature du désaccord | Recommandation |
|---|---|---|
| ARB-C2 — Stratégie manifest | Deux solutions valides et non équivalentes | Décision humaine requise avant patch |
| Création immédiate vs enregistrement comme blocker de `constitutional_conformance_matrix.yaml` | CR-1 et CR-3 penchent pour enregistrement; CR-2 aussi — consensus fort pour blocker, mais le contenu et la structure du fichier futur restent à préciser | Conserver la décision blocker (ARB-B2) et organiser un travail dédié |

---

## Corrections à arbitrer avant patch

### Bloc critique — à traiter impérativement dans ce patch

| Correction | Artefact(s) | Lieu(x) |
|---|---|---|
| COR-A — Ajouter axes `constitutional_invariants_runtime_local` et `no_runtime_content_generation_proof` dans `minimum_validation_contract.minimum_axes` avec critères déterministes | `platform_factory_architecture.yaml` | architecture |
| COR-A' — Définir `runtime_policy_conformance` dans `minimum_validation_contract` | `platform_factory_architecture.yaml` | architecture |
| COR-A'' — Rattacher `constitutional_invariants_checked` à une liste d'invariants et à un protocole dans `minimum_observability_contract` | `platform_factory_architecture.yaml` | architecture |

### Bloc élevé — à traiter dans ce patch

| Correction | Artefact(s) | Lieu(x) |
|---|---|---|
| COR-B — Clarifier `usage_as_sole_context` / `rule_of_use` (régime cible vs politique V0) + ajouter `usage_as_sole_context_unblock_conditions` | `platform_factory_architecture.yaml` | architecture |
| COR-B' — Mettre à jour description `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` pour refléter le régime cible / politique V0 | `platform_factory_state.yaml` | state |
| COR-C — Ajouter blocker `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` dans le state + annotation sur `conformance_matrix_ref` | `platform_factory_state.yaml` + `platform_factory_architecture.yaml` | state + architecture |
| COR-C' — Renforcer description `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent` avec risque explicite sur projections | `platform_factory_state.yaml` | state |
| COR-D — Ajouter champ `authority_rank: factory_layer` dans `metadata` des deux artefacts factory | `platform_factory_architecture.yaml` + `platform_factory_state.yaml` | architecture + state |
| COR-E — Renforcer description `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` comme blocker opérationnel | `platform_factory_state.yaml` | state |
| COR-F — Ajouter blocker `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` dans le state | `platform_factory_state.yaml` | state |

### Bloc modéré — à traiter dans ce patch

| Correction | Artefact(s) | Lieu(x) |
|---|---|---|
| COR-G — Déplacer `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` de `capabilities_present` vers `capabilities_partial` | `platform_factory_state.yaml` | state |
| COR-H — Resynchroniser state sur ARB-04 : retirer `storage_location_decision` des manquants, mettre à jour `assessed_scope` | `platform_factory_state.yaml` | state |

---

## Répartition par lieu de correction

### architecture uniquement
- COR-A (3 sous-corrections)
- COR-B (partiellement)

### state uniquement
- COR-B' (partiellement)
- COR-C' (renforcement description)
- COR-E (renforcement description)
- COR-F (nouveau blocker)
- COR-G (reclassement capacité)
- COR-H (resynchronisation)

### architecture + state
- COR-B (contradiction usage_as_sole_context)
- COR-C (blocker conformance_matrix + annotation)
- COR-D (authority_rank dans métadonnées)

### manifest / release governance (clarification humaine requise)
- ARB-C2 (stratégie manifest/current)

### pipeline (hors patch YAML)
- ARB-C2 (documentation stratégie manifest dans pipeline.md si décision prise)

---

## Séquencement recommandé du patch

1. **En premier** : corrections bloc critique (COR-A, COR-A', COR-A'') — fondent la conformité constitutionnelle du contrat minimal
2. **En deuxième** : COR-D (authority_rank) — protège la cohérence de lecture des artefacts avant toute autre modification
3. **En troisième** : COR-B + COR-B' (contradiction usage_as_sole_context) — clarifie le régime des projections
4. **En quatrième** : COR-C + COR-C' (blockers conformance_matrix + validators)
5. **En cinquième** : COR-E, COR-F, COR-G, COR-H (corrections state restantes)
6. **Après patch** : solliciter arbitrage humain sur ARB-C2 (stratégie manifest), puis traiter en itération suivante

---

## Priorités de patch

| Priorité | Decisions |
|---|---|
| critique | ARB-A1, ARB-A2, ARB-A4 |
| élevé | ARB-A3, ARB-B1, ARB-B2, ARB-B3, ARB-C1, ARB-C2(clarif), ARB-D1, ARB-E1 |
| modéré | ARB-C3, ARB-F1 |
| différé | ARB-D2, ARB-E2, ARB-G1 |
