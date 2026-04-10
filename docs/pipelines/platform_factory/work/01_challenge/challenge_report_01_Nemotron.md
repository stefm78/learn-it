## Résumé exécutif

La Platform Factory V0.3 est une baseline conceptuellement cohérente et honnête sur sa maturité. Elle pose correctement les séparations prescriptif/constatif, générique/spécifique, et exprime une dépendance explicite au socle canonique. Elle n'usurpe pas l'autorité de la Constitution. Ces points sont solides.

Cependant, **cinq zones de risque structurel** compromettent son exploitabilité immédiate comme couche released et gouvernée :

1. **Les invariants constitutionnels critiques (runtime 100% local, pas de génération runtime, patch hors session) ne sont pas repris explicitement dans le contrat minimal d'application produite.** Une application produite par la factory pourrait les violer sans que la factory le détecte.

2. **Le mécanisme de `validated_derived_execution_projection` est défini mais non opérationnel** : pas de validator, pas de protocole de régénération, pas de test d'intégrité, et le champ `usage_as_sole_context: blocked` contradicts l'énoncé autorisant les projections comme contexte unique si validées.

3. **La gouvernance release est réelle mais incomplète** : les artefacts factory sont dans `docs/cores/current/` mais hors manifest officiel, sans exit condition entièrement fermée ni protocole de promotion auditable.

4. **Le multi-IA reste un vœu pieux** : granularité modulaire non définie, protocole d'assemblage absent, protocole de résolution de conflit absent.

5. **L'état (`platform_factory_state.yaml`) présente une légère surdéclaration** dans deux capacités partielles dont la maturité réelle est plus proche de "capability_absent".

Aucun invariant constitutionnel n'est activement violé, mais plusieurs sont protégés **implicitement et faiblement**, ce qui est insuffisant pour une couche released.

***

## Carte de compatibilité constitutionnelle

| Invariant constitutionnel | Élément factory concerné | Binding | Porteur du risque | Application produite détecterait-elle la violation ? |
|---|---|---|---|---|
| `INV_RUNTIME_FULLY_LOCAL` | `produced_application_minimum_contract` / `minimum_observability_contract` | Implicite, faible | Contrat minimal + pipeline | **Non** — aucune obligation explicite de déclarer l'absence de dépendance réseau |
| `INV_NO_RUNTIME_CONTENT_GENERATION` | Contrat minimal, aucune obligation liée | Absent | Contrat minimal | **Non** — non vérifié dans les axes de validation minimale |
| `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` | Architecture factory, `execution_projection_contract` | Implicite | Architecture + projections dérivées | Risque si une projection est utilisée pour générer un patch à la volée |
| `INV_NO_PARTIAL_PATCH_STATE` / `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` | Pipeline STAGE_03/04 | Explicite dans le pipeline, implicite dans l'architecture | Pipeline + validator | Partiellement — le script `validate_platform_factory_patchset.py` est obligatoire mais non implémenté |
| `INV_CONSTITUTION_REFERENTIAL_SEPARATION` | `source_of_authority`, `design_principles` | Explicite | Architecture | Oui — principe `PF_PRINCIPLE_NO_NORM_DUPLICATION` |
| `INV_NO_RUNTIME_CONTENT_GENERATION` (génération de feedback) | Contrat minimal — absence de contrainte | Absent | Contrat minimal | **Non** |
| `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` | Projections dérivées — risque de transport d'inférences IA | Absent | Projections dérivées | Non — une projection mal construite pourrait transporter une inférence IA |
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | Out of scope factory — mais pas dit explicitement | Hors scope déclaré | Contrat minimal — pas de vérification requise | N/A — correctement hors scope, mais à documenter |
| `INV_DISTRESS_REGIME_PRIORITY_CANNOT_BE_OVERRIDDEN` | Hors scope direct factory | Hors scope | — | N/A |

**Synthèse** : `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION` sont les deux invariants les plus exposés. Ils sont fondateurs pour une application Learn-it valide, et le contrat minimal d'application produite ne les rend pas vérifiables.

***

## Analyse détaillée par axe

***

### Axe 1 — Compatibilité constitutionnelle

**Problème 1.1 — `INV_RUNTIME_FULLY_LOCAL` non capturé dans le contrat minimal (CRITIQUE)**

Le contrat minimal (`produced_application_minimum_contract`) liste des axes de validation (`structure`, `minimum_contract_conformance`, `traceability`, `packaging`, `structure_and_state_alignment`, `runtime_policy_conformance`). Le signal `constitutional_invariants_checked` est présent dans `minimum_observability_contract`, mais **aucun axe de validation minimum ne requiert explicitement de vérifier l'absence de dépendance réseau runtime**. Une application produite peut passer la validation factory sans jamais démontrer qu'elle est 100% locale.

- Source : `platform_factory_architecture.yaml` → `produced_application_minimum_contract.minimum_validation_contract.minimum_axes` + `INV_RUNTIME_FULLY_LOCAL` (Constitution `[S4][S13]`)
- Type : compatibilité constitutionnelle
- Gravité : **critique**

**Problème 1.2 — `INV_NO_RUNTIME_CONTENT_GENERATION` non capturé dans le contrat minimal (CRITIQUE)**

Aucune obligation dans le contrat minimal ne contraint une application produite à prouver qu'elle ne génère pas de contenu à la volée (ni feedback généré, ni contenu IA implicite). L'axe `runtime_policy_conformance` dans la validation minimale est un label — son contenu n'est pas défini dans l'architecture factory. Une application violerait silencieusement `INV_NO_RUNTIME_CONTENT_GENERATION` et `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION`.

- Source : `platform_factory_architecture.yaml` → `minimum_validation_contract` ; Constitution `[S13]`
- Type : compatibilité constitutionnelle
- Gravité : **critique**

**Problème 1.3 — `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` partiellement exposé (ÉLEVÉ)**

L'architecture précise que les projections dérivées doivent être générées hors session (`PF_CHAIN_03`) et que leur usage comme contexte unique est `blocked`. Mais si cette restriction est levée à l'avenir (quand la maturité sera suffisante), rien dans l'architecture ne prévient explicitement qu'une IA utilisant une projection pour préparer un patch ne le génère à la volée. La chaîne `PF_CHAIN_03 → PF_CHAIN_05` ne rappelle pas `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`.

- Source : `platform_factory_architecture.yaml` → `transformation_chain`, `execution_projection_contract`
- Type : compatibilité constitutionnelle, complétude
- Gravité : **élevé**

***

### Axe 2 — Cohérence interne de la factory

**Problème 2.1 — Contradiction sur `usage_as_sole_context` (ÉLEVÉ)**

Dans `execution_projection_contract` :
- `usage_as_sole_context: blocked` (→ bloqué jusqu'à maturité suffisante)
- `rule_of_use` : « Une projection dérivée peut être l'unique artefact fourni à une IA [...] si elle est validée »

Ces deux énoncés se contredisent dans le même bloc. L'architecture dit "oui sous conditions" et "bloqué pour l'instant" simultanément, sans clause de levée ni condition de déblocage explicite. Une IA lisant ce contrat peut interpréter les deux sens.

- Source : `platform_factory_architecture.yaml` → `contracts.execution_projection_contract`
- Type : cohérence architecturale
- Gravité : **élevé**

**Problème 2.2 — `runtime_policy_conformance` non défini (ÉLEVÉ)**

L'axe de validation `runtime_policy_conformance` est listé dans `minimum_validation_contract.minimum_axes` sans aucune définition de son contenu, critères ou périmètre. C'est un label creux. Une IA chargée de valider la conformité runtime n'a aucune instruction déterministe.

- Source : `platform_factory_architecture.yaml` → `minimum_validation_contract`
- Type : implémentabilité, complétude
- Gravité : **élevé**

**Problème 2.3 — `constitutional_conformance_matrix_ref` référence un fichier absent (ÉLEVÉ)**

Le champ `conformance_matrix_ref` pointe vers `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`. Ce fichier n'est pas présent dans le repo (non visible dans les artefacts existants), n'est pas listé comme capacité absente dans le state, et n'a pas de blocker associé. C'est une référence morte dans un contrat qui prétend être released.

- Source : `platform_factory_architecture.yaml` → `mandatory_fields_per_projection.conformance_matrix_ref` + `dependencies_to_constitution.constitutional_conformance_matrix_ref`
- Type : gouvernance, complétude, traçabilité
- Gravité : **élevé**

**Problème 2.4 — Légère incohérence architecture/state sur `capability_derived_projection_rule_defined` (MODÉRÉ)**

Dans `platform_factory_state.yaml`, `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` est en `capabilities_partial` avec la description : "La règle d'usage des projections dérivées est définie. [...] Restent absents : validator dédié, protocole de régénération automatisé, usage comme contexte unique bloqué."

Mais dans `platform_factory_architecture.yaml`, `execution_projection_contract` inclut des `mandatory_fields_per_projection` — ce qui est plus que juste une règle. Le state ne mentionne pas que les champs obligatoires sont désormais définis dans l'architecture, créant une légère désynchronisation descriptive.

- Source : `platform_factory_state.yaml` → `capabilities_partial`
- Type : cohérence interne (architecture vs state)
- Gravité : **modéré**

***

### Axe 3 — Portée et frontières

**Point solide** : La factory délimite très clairement ce qu'elle ne gouverne pas : `domain_specific_learning_content`, `detailed_architecture_of_one_instantiated_application`, `learner_runtime_state`, `specific_domain_feedback_logic`. Cette séparation est robuste et cohérente entre l'architecture et le state.

**Zone de risque** : La frontière entre "contrat minimal générique d'une application produite" et "comportement runtime d'une application particulière" est définie au niveau de la liste (`out_of_scope: detailed_runtime_behavior_of_one_specific_application`), mais **le contrat minimal inclut des obligations sur le runtime entrypoint (`runtime_entrypoint_contract`)** dont le `bootstrap_contract` est explicitement "TBD". Une IA implémentant ce contrat devra inévitablement décider de ce que signifie "respecter le bootstrap contract" — ce qui est une improvisation de scope runtime autorisée implicitement.

**Angle mort** : La factory ne définit pas qui produit les projections dérivées (la factory elle-même ? une IA spécifique ? un pipeline dédié ?). La chaîne `PF_CHAIN_03_GENERATE_EXECUTION_PROJECTIONS` reste une intention sans acteur défini, sans protocole et sans validation gate définie dans l'architecture.

- Source : `platform_factory_architecture.yaml` → `transformation_chain`, `runtime_entrypoint_contract`
- Type : complétude, gouvernance
- Gravité : **modéré**

***

### Axe 4 — Contrat minimal d'une application produite

**Problème 4.1 — Absence de clause d'auditabilité de la conformité constitutionnelle (CRITIQUE)**

Le contrat minimal ne contient aucune obligation de produire une preuve que l'application respecte `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`. Le signal `constitutional_invariants_checked` est dans l'observabilité minimale, mais sans définir quels invariants, comment, ni par quel artefact. Il est non auditable.

- Source : `platform_factory_architecture.yaml` → `minimum_observability_contract`, `minimum_validation_contract`
- Type : compatibilité constitutionnelle, gouvernance
- Gravité : **critique**

**Problème 4.2 — `bootstrap_contract` TBD bloque la validation (ÉLEVÉ)**

Le `runtime_entrypoint_contract` exige un `bootstrap_contract` mais le documente comme "TBD. Ce champ sera défini quand la typologie exacte des runtimes d'application Learn-it sera arrêtée." Cela signifie qu'aucune application ne peut passer la validation complète du contrat minimal — car un champ obligatoire est absent de sa définition. Une validation minimum_contract_conformance sur une application produite serait donc structurellement incomplète.

- Source : `platform_factory_architecture.yaml` → `runtime_entrypoint_contract.bootstrap_contract_tbd_condition`
- Type : implémentabilité, complétude
- Gravité : **élevé**

**Problème 4.3 — `fingerprints de reproductibilité` définis mais non auditables (MODÉRÉ)**

Les `reproducibility_fingerprints` sont définis comme "hash ou identifiant de version stable de chaque dépendance canonique." Mais ni la validation minimale ni l'observabilité ne précisent comment vérifier la fraîcheur de ces fingerprints, ni si une dérive de version canonique doit invalider l'application. Une application avec des fingerprints périmés passerait silencieusement.

- Source : `platform_factory_architecture.yaml` → `identity.reproducibility_fingerprints_definition`
- Type : gouvernance, traçabilité
- Gravité : **modéré**

**Point solide** : Les blocs d'identité (`logical_identity`, `produced_instance_identity`, `reproducibility_fingerprints`) sont bien distincts et leur obligation est claire. C'est une bonne fondation.

***

### Axe 5 — Validated derived execution projections

**Problème 5.1 — Contradiction `usage_as_sole_context` (déjà documenté en 2.1) — impact direct sur le principe (ÉLEVÉ)**

Le principe central — *"une projection dérivée peut être l'unique artefact fourni à une IA pour un travail donné seulement si elle reste strictement fidèle au canonique applicable dans le scope déclaré"* — est affaibli par la contradiction interne entre `rule_of_use` et `usage_as_sole_context: blocked`. Jusqu'à résolution, aucune IA ne sait avec certitude si elle est autorisée à fonctionner sur projection seule ou non.

**Problème 5.2 — Absence de protocole de validation des projections (ÉLEVÉ)**

Le contrat de projection liste des `mandatory_fields` mais ne définit pas de procédure de validation, ni de critère d'acceptation pour `validation_status: validated`. `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` est absent. Une projection peut être taguée `validated` par une IA sans qu'aucun critère déterministe ne soit respecté — violant `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` par analogie.

**Problème 5.3 — Risque de paraphrase normative (ÉLEVÉ)**

Les `prohibited` items (`uncontrolled_paraphrase`, `implicit_rule_addition`) sont listés mais il n'existe aucun mécanisme de détection. Une IA générant une projection peut ajouter une nuance sémantique ("la règle X s'applique sauf si Y") qui n'est pas dans le canonique, sans que la factory ne le détecte. Le `version_fingerprint` protège contre les dérives de version, pas contre les dérives de sens.

**Problème 5.4 — `conformance_matrix_ref` mort (déjà documenté en 2.3)**
Chaque projection doit référencer `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` — qui n'existe pas. Toute projection générée référencera un artefact inexistant.

***

### Axe 6 — État reconnu, maturité et preuves

**Surdéclaration 6.1 — `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` (MODÉRÉ)**

Statut : `capabilities_present`. Description : "L'intention de pipeline platform_factory est explicitement posée (intent only, not yet tooled execution framework). Les stages existent et les prompts de lancement sont définis."

Le qualificatif "intent only, not yet tooled" contredit directement le classement en `capabilities_present`. Une intention non outillée n'est pas une capacité présente — c'est une capacité partielle. Cela constitue une légère surdéclaration.

**Surdéclaration 6.2 — `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` (MODÉRÉ)**

Statut : `capabilities_partial`. La décision de stockage est actée (ARB-04, `docs/cores/platform_factory/projections/`), mais le répertoire n'existe pas encore, aucune projection n'y est stockée, et l'outillage est absent. Le nom "FINALIZED" dans l'ID et la description "emplacement décidé" pourraient laisser croire que la capacité est prête à l'emploi. Elle ne l'est pas.

**Cohérence blockers/capabilities :**
- `PF_BLOCKER_MANIFEST_SCHEMA_PENDING` est `medium` mais son exit condition dépend de `STAGE_08` — qui ne peut s'exécuter que si la chaîne complète (STAGE_01 à STAGE_07) a produit des artefacts valides. Cette dépendance en cascade n'est pas documentée dans le blocker.
- `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` a bien une exit condition explicite : c'est solide.

**Cohérence evidence** : `PF_EVIDENCE_PLAN_V2` référence `docs/architecture/Platform_Factory_Plan.md`. Ce fichier n'a pas été fourni dans le contexte de ce challenge. S'il est absent ou divergent, l'evidence devient vide.

***

### Axe 7 — Multi-IA en parallèle

**Problème 7.1 — Granularité modulaire non définie (ÉLEVÉ)**

`PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` est reconnu comme known_gap. Mais l'impact est plus grave que reconnu : sans convention de granularité modulaire, deux IA travaillant en parallèle sur la même projection ou le même module ne savent pas quelle portion leur appartient. Aucun protocole d'assemblage des outputs n'existe. Le risque n'est pas "non optimal" — c'est une impossibilité opérationnelle d'exécution multi-IA parallèle.

**Problème 7.2 — Points d'assemblage flous (ÉLEVÉ)**

`clear_assembly_points` est listé comme exigence dans `multi_ia_parallel_readiness.minimum_requirements`, mais aucun point d'assemblage n'est défini dans l'architecture (ni dans les stages du pipeline, ni dans les modules génériques). C'est une exigence déclarée sans contenu.

**Problème 7.3 — Reports non homogènes (MODÉRÉ)**

L'architecture exige `homogeneous_reports` mais ne définit pas de schéma de report commun. Un schéma de report différent entre deux IA parallèles rendrait l'assemblage manuel ou impossible.

***

### Axe 8 — Gouvernance release, manifest et traçabilité

**Problème 8.1 — Artefacts dans `current/` mais hors manifest (ÉLEVÉ)**

`platform_factory_architecture.yaml` et `platform_factory_state.yaml` sont dans `docs/cores/current/` — la zone des canoniques primaires — mais ne sont pas dans le manifest officiel (`PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`). Cette situation crée une ambiguïté : leur statut "current" est soit une promotion implicite non gouvernée, soit un état hybride sans équivalent documenté. Le pipeline ne définit pas de garde-fou pour éviter qu'une IA lise ces fichiers comme des canoniques primaires au même titre que `constitution.yaml`.

**Problème 8.2 — Absence de séparation release/promotion dans les artefacts (MODÉRÉ)**

Le pipeline (`Rule 6`) distingue release materialization et promotion. Mais ni l'architecture ni le state ne contiennent de champ permettant à un artefact lui-même d'indiquer s'il est "released mais non promu" vs "promu current". Une IA lisant `platform_factory_architecture.yaml` verra `status: RELEASE_CANDIDATE` — mais ce statut n'est pas défini dans une taxonomie officielle. Que signifie exactement `RELEASE_CANDIDATE` dans ce contexte ?

**Problème 8.3 — `conformance_matrix_ref` absent (déjà noté)**

***

### Axe 9 — Implémentabilité pipeline

**Problème 9.1 — `validate_platform_factory_patchset.py` non implémenté (ÉLEVÉ)**

STAGE_04 dépend d'un script Python obligatoire (`validate_platform_factory_patchset.py`) qui n'est pas encore implémenté (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent`). Le pipeline dit "Le stage ne peut continuer que si `status: PASS`" — mais si le script n'existe pas, le stage est bloqué dès le premier run. La pipeline ne définit pas de comportement de secours.

**Problème 9.2 — STAGE_01 multi-challenge sans protocole de consolidation (MODÉRÉ)**

STAGE_02 dit "every `challenge_report*.md` present in `work/01_challenge/` must be considered during arbitrage". Mais si plusieurs IA produisent des challenge reports contradictoires, l'arbitrage n'a pas de règle de résolution de conflits entre reports. C'est laissé à l'humain sans protocole.

**Problème 9.3 — STAGE_07 et STAGE_08 déléguées à des specs hors pipeline (MODÉRÉ)**

STAGE_07 et STAGE_08 n'ont pas de description inline dans `pipeline.md` — elles délèguent à `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` et `STAGE_08_FACTORY_PROMOTE_CURRENT.md` qui n'ont pas été fournis dans les artefacts de ce challenge. Si ces fichiers sont absents ou incomplets, les stages critiques (release materialization et promotion to current) sont non gouvernés.

**Point solide** : La règle "no file in `docs/cores/current/` may be modified directly before explicit promotion" est claire, forte et correctement exprimée.

***

### Axe 10 — Scénarios adversariaux

**Scénario A — Dérive de projection dérivée (réaliste)**

Une IA reçoit une `validated_derived_execution_projection` couvrant le contrat de patch factory. La projection paraphrase `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` en "la validation doit être vérifiable localement" — supprimant l'exigence "déterministe". L'IA produit un patchset avec une validation sémantique. Le script STAGE_04 vérifie les chemins YAML mais pas la fidélité sémantique à la Constitution. La validation passe en PASS. La non-conformité constitutionnelle entre silencieusement dans le cycle.

**Mécanismes activés** : `execution_projection_contract` (validation_status accepté), `validate_platform_factory_patchset.py` (vérifie paths, pas sémantique)
**Faiblesse révélée** : Absence de validation sémantique des projections + validator non implémenté
**Origine** : projections dérivées + pipeline

***

**Scénario B — Application produite paraissant valide mais violant `INV_RUNTIME_FULLY_LOCAL` (réaliste)**

Une IA produit une application qui charge dynamiquement les fingerprints depuis un dépôt distant au démarrage. Le manifest est complet, les axes de validation `structure`, `traceability`, `packaging` passent. L'axe `runtime_policy_conformance` est présent mais son contenu n'est pas défini. Le signal `constitutional_invariants_checked` est coché "checked" sans critère. La factory certifie l'application comme conforme. L'application viole `INV_RUNTIME_FULLY_LOCAL`.

**Mécanismes activés** : `minimum_validation_contract` (axes listés), `minimum_observability_contract` (signal présent)
**Faiblesse révélée** : `runtime_policy_conformance` non défini + `constitutional_invariants_checked` non auditable
**Origine** : contrat minimal + architecture

***

**Scénario C — Collision multi-IA (réaliste)**

Deux IA travaillent en parallèle sur une projection dérivée couvrant le même scope (contrat minimal d'application). L'IA-1 produit une projection avec 12 champs obligatoires, l'IA-2 en produit une avec 10 champs car elle a interprété différemment les `mandatory_fields`. Les deux projections sont taguées `validated`. L'assemblage en STAGE_02 confronte deux versions divergentes. Aucun protocole de résolution de conflit entre projections n'existe. L'arbitrage humain est requis pour toute progression.

**Mécanismes activés** : `multi_ia_parallel_readiness.minimum_requirements` (violated), `execution_projection_contract` (champs obligatoires non partagés)
**Faiblesse révélée** : Pas de convention de granularité, pas de protocole de résolution de conflit entre projections
**Origine** : architecture multi-IA + projections dérivées

***

**Scénario D — Gouvernance release insuffisamment fermée (réaliste)**

Une IA consulte `docs/cores/current/platform_factory_architecture.yaml` (artefact dans `current/`, authority non définie comme différente de `constitution.yaml`) et le traite comme une autorité primaire pour décider d'un arbitrage constitutionnel. Elle invoque `PF_PRINCIPLE_NO_NORM_DUPLICATION` pour refuser un patch qui modifie un paramètre dans `constitution.yaml`, estimant que cela "duplique une norme factory". La confusion de statut entre canonique primaire et couche factory produit une décision de rejet erronée.

**Mécanismes activés** : placement dans `current/`, `authority` non différenciée dans les métadonnées
**Faiblesse révélée** : Absence de champ `authority_rank` ou équivalent dans les artefacts factory; ambiguïté de co-placement dans `current/`
**Origine** : gouvernance release + manifest

***

### Axe 11 — Priorisation des risques

#### Critique
| # | Problème | Localisation | Impact |
|---|---|---|---|
| C1 | `INV_RUNTIME_FULLY_LOCAL` non capturé dans le contrat minimal | Architecture — `minimum_validation_contract` | Application produite peut violer l'invariant sans détection |
| C2 | `INV_NO_RUNTIME_CONTENT_GENERATION` non capturé dans le contrat minimal | Architecture — `minimum_validation_contract` | Idem |
| C3 | `constitutional_invariants_checked` non auditable | Architecture — `minimum_observability_contract` | Garantie de conformité constitutionnelle creuse |

#### Élevé
| # | Problème | Localisation | Impact |
|---|---|---|---|
| E1 | Contradiction `usage_as_sole_context: blocked` vs `rule_of_use` autorisant | Architecture — `execution_projection_contract` | Ambiguïté normative pour toute IA |
| E2 | `runtime_policy_conformance` non défini | Architecture — `minimum_validation_contract` | Axe de validation creux |
| E3 | `constitutional_conformance_matrix_ref` fichier absent | Architecture — deux emplacements | Référence morte dans un contrat released |
| E4 | `bootstrap_contract: TBD` bloque la validation complète | Architecture — `runtime_entrypoint_contract` | Contrat minimal incomplétable |
| E5 | Absence de protocole de validation des projections dérivées | Architecture + state | Projections non validables de manière déterministe |
| E6 | `validate_platform_factory_patchset.py` absent | Pipeline STAGE_04 | STAGE_04 bloqué au premier run |
| E7 | Granularité modulaire et assemblage multi-IA non définis | Architecture — `multi_ia_parallel_readiness` | Multi-IA inopérant en pratique |
| E8 | Artefacts dans `current/` sans différenciation d'autorité | Gouvernance release + artefacts | Risque de confusion statut canonique |

#### Modéré
| # | Problème | Localisation | Impact |
|---|---|---|---|
| M1 | `reproducibility_fingerprints` non vérifiables (dérive silencieuse) | Architecture — contrat minimal | Fingerprints obsolètes non détectés |
| M2 | Légère surdéclaration `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | State | Maturité légèrement sur-annoncée |
| M3 | `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` — nom trompeur | State | Confusion sur la disponibilité réelle |
| M4 | STAGE_07/08 délégués à fichiers non fournis dans ce contexte | Pipeline | Stages critiques potentiellement non gouvernés |
| M5 | Absence de `authority_rank` dans les artefacts factory | Artefacts + gouvernance | Risque de confusion par une IA |

#### Faible
- Désynchronisation mineure entre architecture et state sur `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
- Absence de schéma de report homogène pour multi-IA

***

## Points V0 acceptables

Ces points sont des incomplétudes V0 normales, reconnues, bornées, sans risque immédiat :

- **Schéma fin du manifest** (`PF_BLOCKER_MANIFEST_SCHEMA_PENDING`) : correctement reconnu, borné par un exit condition au STAGE_08.
- **Pipeline non automatisé** : annoncé explicitement comme "V0 skeleton", suffisant pour lancer le challenge itératif.
- **Outillage de génération de projections absent** : reconnu comme capacité partielle/absente, sans impact immédiat tant qu'aucune projection n'est produite.
- **Protocol d'assemblage multi-IA absent** : reconnu comme `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` — acceptable tant que les IA ne travaillent pas effectivement en parallèle.
- **Schéma de packaging et configuration non finalisés** : clairement listés comme manquants.
- **`bootstrap_contract: TBD`** est un point ouvert reconnu et borné — acceptable en V0 si documenté comme blocker (ce qui n'est pas encore le cas, voir E4).

***

## Corrections à arbitrer avant patch

***

### COR-01 — Rendre `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION` explicitement requis dans le contrat minimal

- **Élément** : `minimum_validation_contract.minimum_axes` + `minimum_observability_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Nature** : Ajout d'une obligation explicite de vérification de ces deux invariants dans les axes de validation et l'observabilité minimale
- **Type** : compatibilité constitutionnelle, gouvernance
- **Gravité** : critique
- **Impact factory** : Sans correction, la factory ne peut pas garantir la conformité constitutionnelle des applications qu'elle produit
- **Impact application produite** : Une application peut violer les invariants les plus fondamentaux de Learn-it sans déclencher d'alerte
- **Impact IA** : Une IA validant une application produite n'a pas les critères pour refuser
- **Impact gouvernance/release** : La factory ne peut pas être considérée comme fiable sur sa fonction première
- **Correction** : Ajouter dans `minimum_validation_contract.minimum_axes` un axe `constitutional_invariants_runtime_local` et un axe `no_runtime_content_generation_proof` avec des critères déterministes (ex : liste d'artefacts déclarée, absence de dépendance réseau vérifiée statiquement)
- **Lieu** : architecture → `produced_application_minimum_contract`

***

### COR-02 — Résoudre la contradiction `usage_as_sole_context`

- **Élément** : `execution_projection_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Nature** : Contradiction interne entre `rule_of_use` et `usage_as_sole_context: blocked`
- **Type** : cohérence architecturale
- **Gravité** : élevé
- **Correction** : Clarifier que `usage_as_sole_context: blocked` est l'état actuel V0, et que `rule_of_use` décrit le régime cible. Ajouter un champ `usage_as_sole_context_conditions` listant les conditions de déblocage (validator implémenté, régénération déterministe, etc.)
- **Lieu** : architecture → `execution_projection_contract`

***

### COR-03 — Créer ou bocker `constitutional_conformance_matrix.yaml`

- **Élément** : Champ `conformance_matrix_ref` dans deux emplacements
- **Localisation** : `platform_factory_architecture.yaml`
- **Nature** : Référence morte
- **Type** : gouvernance, traçabilité
- **Gravité** : élevé
- **Correction** : Soit créer le fichier `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` comme capacité à implémenter (avec un squelette minimal), soit enregistrer son absence comme blocker dans `platform_factory_state.yaml` avec exit condition explicite
- **Lieu** : architecture (correction de la référence) + state (nouveau blocker)

***

### COR-04 — Définir le contenu de `runtime_policy_conformance`

- **Élément** : `minimum_validation_contract.minimum_axes`
- **Localisation** : `platform_factory_architecture.yaml`
- **Nature** : Axe de validation sans contenu
- **Type** : implémentabilité, complétude
- **Gravité** : élevé
- **Correction** : Définir (même à haut niveau) ce que couvre `runtime_policy_conformance` : au minimum, vérification de l'absence de dépendances réseau runtime, vérification de l'absence de génération de contenu, conformité au régime d'autonomie déclaré
- **Lieu** : architecture → `minimum_validation_contract`

***

### COR-05 — Enregistrer `bootstrap_contract: TBD` comme blocker dans le state

- **Élément** : `runtime_entrypoint_contract.bootstrap_contract`
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Nature** : Champ obligatoire TBD non tracé comme blocker
- **Type** : implémentabilité, gouvernance
- **Gravité** : élevé
- **Correction** : Ajouter dans `platform_factory_state.yaml` un blocker `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` avec exit condition (définition de la typologie des runtimes)
- **Lieu** : state → `blockers`

***

### COR-06 — Corriger le classement de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

- **Élément** : `capabilities_present`
- **Localisation** : `platform_factory_state.yaml`
- **Nature** : Surdéclaration légère
- **Type** : faux niveau de maturité
- **Gravité** : modéré
- **Correction** : Déplacer vers `capabilities_partial` avec description précisant "intent posé, prompts définis, outillage absent"
- **Lieu** : state → `capabilities_present` → `capabilities_partial`

***

### COR-07 — Ajouter un champ de différenciation d'autorité dans les métadonnées factory

- **Élément** : `metadata` des deux artefacts factory
- **Localisation** : `platform_factory_architecture.yaml` + `platform_factory_state.yaml`
- **Nature** : Absence de champ signalant que ces artefacts ne sont PAS des canoniques primaires au sens Constitution/Référentiel/LINK
- **Type** : gouvernance, mauvais placement de couche
- **Gravité** : élevé
- **Correction** : Ajouter dans `metadata` un champ `authority_rank: factory_layer` (distinct de `canonical_primary`) ou équivalent, pour éviter toute confusion par une IA lisant `docs/cores/current/`
- **Lieu** : architecture + state → `metadata`

***
