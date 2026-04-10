# Proposition d'arbitrage — STAGE_02_FACTORY_ARBITRAGE

## arbitrage_run_id

`PFARB_20260410_PERPLEX_X7Q2`

## Date

2026-04-10

## Challenge reports considérés

| ID | Fichier |
|---|---|
| PFCHAL_20260410_GPT54_Z4N8 | `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_GPT54_Z4N8.md` |
| PFCHAL_20260410_PERPLEX_9KR4M | `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLEX_9KR4M.md` |
| PFCHAL_20260410_PERPLX_8ZQA | `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_8ZQA.md` |
| PFCHAL_20260410_PERPLX_9KR3 | `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_9KR3.md` |
| PFCHAL_20260410_PERPLX_K7R2 | `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_K7R2.md` |

---

## Résumé exécutif

Les cinq challenge reports convergent de façon remarquable : les constats majeurs sont partagés par toutes les IA sans contradiction de fond, uniquement des variations de formulation et de priorisation. La baseline V0.4 est unanimement jugée fondatrice et gouvernable, mais non encore probante pour ses promesses les plus fortes.

Trois thèmes critiques cristallisent le consensus fort :
1. L'absence de `constitutional_conformance_matrix.yaml` rend toute conformité constitutionnelle non auditable.
2. L'absence de validator dédié rend le signal `constitutional_invariants_checked` non probant.
3. Le `bootstrap_contract` TBD empêche la clôture du contrat minimal d'application.

Quatre thèmes élevés à fort consensus :
4. `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` est un BLOCKER OPÉRATIONNEL mal classifié.
5. `usage_as_sole_context: blocked` est une politique déclarative sans garde-fou technique.
6. Le script `validate_platform_factory_patchset.py` de STAGE_04 est absent.
7. Plusieurs points de maturité surdéclarée dans le state méritent correction de wording.

Deux points divergents mineurs nécessitent une note d'arbitrage :
- PERPLX_8ZQA identifie deux invariants constitutionnels absents du contrat minimal (`INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION`) non couverts par les autres rapports — retenus comme élevés.
- PERPLX_K7R2 identifie une incohérence de nommage dans `pipeline.md` pour les challenge reports — retenu comme modéré.

---

## Synthèse des constats convergents

### Critique — consensus fort (5/5 rapports)

1. **`constitutional_conformance_matrix.yaml` absente** : tous les rapports identifient `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` comme le trou le plus structurant. La conformité constitutionnelle de toute projection et de toute application produite est inauditable sans cet artefact.

2. **Validator dédié absent** (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` = absent) : le signal `constitutional_invariants_checked` ne peut pas être émis de façon probante. Tout `validation_status: validated` sur projection est non déterministe.

3. **`bootstrap_contract` TBD** (`PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED`) : aucune application produite ne peut passer la validation complète du contrat minimal. La brèche est dangereuse car une IA pourrait introduire une dépendance réseau via un bootstrap implicite.

### Élevé — consensus fort (4-5/5 rapports)

4. **`PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` mal classifié** : désigné "BLOCKER OPÉRATIONNEL" dans sa description mais listé dans `known_gaps` et non dans `blockers`. Asymétrie de classification unanimement relevée.

5. **`usage_as_sole_context: blocked` sans mécanisme d'application** : la politique est déclarative, sans garde-fou technique dans le pipeline ou les launch prompts.

6. **Script `validate_platform_factory_patchset.py` absent** : STAGE_04 ne peut pas s'exécuter dans sa forme canonique. Blocage silencieux de tout le pipeline à partir de STAGE_04.

7. **Wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` (partial) trop optimiste** : "exécutable manuellement" est inexact pour les stages avec script obligatoire.

### Modéré — consensus (3-4/5 rapports)

8. **Promotion directe vers `docs/cores/current/` non bloquée techniquement** : Rule 6 du pipeline est déclarative, sans hook ni protection de branche.

9. **Format de sortie STAGE_01 non schématisé** : `challenge_report_*.md` est libre. STAGE_02 ne peut pas parser de façon déterministe. Assemblage multi-IA dégradé.

10. **Incohérence référencement STAGE_01 dans `pipeline.md`** : le pipeline pointe le prompt métier partagé, non le launch prompt d'exécution dédié.

11. **Maturité surdéclarée sur `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` (partial)** : le régime cible est structurellement bloqué, pas en cours de progression.

12. **`reproducibility_fingerprints` définis en intention mais sans format contraint** : deux IA pourraient produire des fingerprints incomparables.

### Élevé — identifié uniquement par PERPLX_8ZQA (1/5, retenu)

13. **`INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` absent du contrat minimal produit** : invariant constitutionnel fort non couvert par les axes de validation.

14. **`INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` absent du contrat minimal** : invariant récent (`ARBITRAGE_2026_04_01`) non répercuté.

### Élevé — identifié uniquement par PERPLX_K7R2 (1/5, retenu)

15. **`version_fingerprint` sans mécanisme de détection de dérive canonique** : une mise à jour de `constitution.yaml` n'invalide pas automatiquement les projections existantes.

### Modéré — identifié par PERPLX_K7R2 (1/5, retenu)

16. **Incohérence convention de nommage des challenge reports entre `pipeline.md` (`##`) et le launch prompt** (format `PFCHAL_YYYYMMDD_AGENTTAG_RAND`).

### Angle mort spécifique — PERPLEX_9KR4M

17. **Absence de référence au double-buffer/swap atomique constitutionnel pour les patches d'artefacts factory** : la factory ne mentionne pas l'obligation constitutionnelle de double-buffer pour ses propres patches internes. Retenu comme modéré.

---

## Propositions d'arbitrage par thème

---

### Thème 1 — Conformance matrix et auditabilité constitutionnelle

#### ARB-01 — Créer `constitutional_conformance_matrix.yaml`

- **Élément concerné** : artefact `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` (absent)
- **Localisation principale** : validator/tooling + manifest/release governance
- **Localisation secondaire** : architecture (le champ `constitutional_conformance_matrix_ref` doit continuer de pointer vers cet artefact une fois créé)
- **Problème** : artefact obligatoire absent ; toute projection ou application produite y faisant référence est inauditable constitutionnellement
- **Statut proposé** : `retained`
- **Gravité** : critique
- **Justification** : convergence 5/5. Blocker `high` actif. Condition nécessaire au déblocage de `usage_as_sole_context` et à toute release d'application constitutionnellement probante.
- **Dépendance** : conditionne ARB-02 (validator), ARB-06 (projections).
- **Lieu principal de correction** : création d'artefact dédié — hors patch YAML direct sur architecture/state. À orchestrer via un cycle pipeline dédié ou un STAGE_02/03 parallèle.
- **Consensus** : strong

#### ARB-02 — Ajouter une interdiction explicite d'émission de `constitutional_invariants_checked` en l'absence du validator

- **Élément concerné** : `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.minimum_observability_contract`
- **Localisation** : architecture
- **Problème** : le signal peut être émis par convention sans validator, produisant un faux PASS
- **Statut proposé** : `retained`
- **Gravité** : critique
- **Justification** : convergence 5/5. Le patch est simple : ajouter une contrainte normative explicite dans la note d'observabilité. Sauf inspection statique documentée comme protocole manuel minimal acceptable en V0, le signal doit être interdit.
- **Lieu principal** : architecture
- **Consensus** : strong

---

### Thème 2 — Validator dédié

#### ARB-03 — Reclasser l'absence de `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` en blocker `high`

- **Élément concerné** : `platform_factory_state.yaml` → `capabilities_absent.PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED`
- **Localisation** : state
- **Problème** : l'absence de validator est actuellement une simple `capabilities_absent` sans statut de blocker, alors que son impact est critique sur deux signaux fondamentaux.
- **Statut proposé** : `retained`
- **Gravité** : critique
- **Justification** : PERPLX_9KR3 et PERPLEX_9KR4M convergent explicitement sur ce point. GPT54_Z4N8 le traite comme R1 critique. Patch simple sur le state.
- **Lieu principal** : state
- **Consensus** : strong

---

### Thème 3 — Bootstrap contract

#### ARB-04 — Arbitrer le traitement V0 du `bootstrap_contract`

- **Élément concerné** : `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.runtime_entrypoint_contract.bootstrap_contract`
- **Localisation** : architecture + state
- **Problème** : champ obligatoire TBD. Brèche d'inventivité pouvant introduire une dépendance réseau.
- **Statut proposé** : `retained`
- **Gravité** : critique
- **Option A** : définir un scope minimal V0 du bootstrap (aucun appel réseau, aucun appel LLM, dépendances uniquement locales) sans finaliser la typologie complète des runtimes.
- **Option B** : maintenir TBD mais ajouter une contrainte architecturale explicite d'interdiction d'appel réseau/LLM dans tout bootstrap jusqu'à définition formelle.
- **Décision proposée** : Option B comme patch immédiat (plus sûr, moins risqué d'erreur de schéma prématuré) + tracer en blocker avec exit condition dans le state.
- **Justification** : convergence 5/5. Option B ne sur-contraint pas la V0 tout en fermant la brèche dangereuse.
- **Lieu principal** : architecture (contrainte normative) + state (blocker avec exit condition)
- **Consensus** : strong

---

### Thème 4 — Protocole multi-IA

#### ARB-05 — Reclasser `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker formel

- **Élément concerné** : `platform_factory_state.yaml` → `known_gaps.PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED`
- **Localisation** : state
- **Problème** : gap auto-déclaré "BLOCKER OPÉRATIONNEL" mais classé `known_gap` sans exit condition ni sévérité formelle.
- **Statut proposé** : `retained`
- **Gravité** : élevée
- **Justification** : convergence 5/5. Patch simple sur state : déplacer vers `blockers` avec sévérité `medium`, définir exit condition (spec du protocole multi-IA : décomposition, assemblage, résolution de conflit).
- **Lieu principal** : state
- **Lieu secondaire** : architecture (note sur `multi_ia_parallel_readiness_status` à aligner)
- **Consensus** : strong

---

### Thème 5 — Projections dérivées

#### ARB-06 — Ajouter un signal `conformance_matrix_availability_status` dans le contrat de projection

- **Élément concerné** : `platform_factory_architecture.yaml` → `contracts.execution_projection_contract.mandatory_fields_per_projection`
- **Localisation** : architecture
- **Problème** : une projection émise aujourd'hui contient un `conformance_matrix_ref` pointant un fichier absent, sans que l'IA réceptrice en soit informée.
- **Statut proposé** : `retained`
- **Gravité** : élevée
- **Justification** : identifié par PERPLX_9KR3 (C5) et cohérent avec les autres rapports. Patch simple dans l'architecture.
- **Lieu principal** : architecture
- **Dépendance** : ARB-01 (création de la matrice lève ce point à terme)
- **Consensus** : medium

#### ARB-07 — Gouverner concrètement `usage_as_sole_context: blocked`

- **Élément concerné** : `execution_projection_contract` + launch prompts du pipeline
- **Localisation principale** : pipeline
- **Localisation secondaire** : architecture
- **Problème** : politique déclarative sans garde-fou technique dans le pipeline.
- **Statut proposé** : `retained`
- **Gravité** : élevée
- **Justification** : convergence 5/5. Patch pipeline : ajouter dans chaque launch prompt de STAGE utilisant des projections une instruction explicite rappelant ce blocage. Patch architecture : ajouter un header obligatoire ou une note de blocage dans le champ `usage_as_sole_context`.
- **Lieu principal** : pipeline (launch prompts)
- **Lieu secondaire** : architecture
- **Consensus** : strong

#### ARB-08 — Ajouter un mécanisme de détection de dérive canonique sur `version_fingerprint`

- **Élément concerné** : `platform_factory_architecture.yaml` → `contracts.execution_projection_contract.mandatory_fields_per_projection.version_fingerprint`
- **Localisation** : architecture
- **Problème** : le champ est obligatoire mais le mécanisme de comparaison (qui compare, quand, par rapport à quoi) est absent. Une mise à jour canonique n'invalide pas les projections existantes.
- **Statut proposé** : `retained`
- **Gravité** : élevée
- **Justification** : PERPLX_K7R2 (C4). Non identifié explicitement par les autres rapports, mais cohérent avec la logique de traçabilité. Impact direct sur la fidélité des projections.
- **Lieu principal** : architecture
- **Note** : une règle descriptive (sans implémentation outillée) suffit en V0 pour borner le risque.
- **Consensus** : weak (1/5 — à consolider en consolidation humaine finale)

---

### Thème 6 — Contrat minimal d'application : invariants manquants

#### ARB-09 — Ajouter `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` au contrat minimal

- **Élément concerné** : `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes`
- **Localisation** : architecture
- **Problème** : invariant constitutionnel fort (`INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`) non couvert par les axes minimaux de validation.
- **Statut proposé** : `retained`
- **Gravité** : élevée
- **Justification** : identifié par PERPLX_8ZQA (C2). Non présent dans les autres rapports mais l'invariant est constitutionnel fort. Correction à moindre coût (ajout d'un axe dans `minimum_axes`).
- **Lieu principal** : architecture
- **Consensus** : weak (1/5 — à consolider en consolidation humaine finale)

#### ARB-10 — Ajouter `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` au contrat minimal

- **Élément concerné** : `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.minimum_validation_contract` et/ou `runtime_policy_conformance_definition`
- **Localisation** : architecture
- **Problème** : invariant récent (`ARBITRAGE_2026_04_01`) non répercuté dans la factory.
- **Statut proposé** : `retained`
- **Gravité** : élevée
- **Justification** : identifié par PERPLX_8ZQA (C3). L'invariant est dans le socle canonique — son absence du contrat minimal est un gap de synchronisation.
- **Lieu principal** : architecture
- **Pré-condition** : vérifier que cet invariant est bien présent dans `constitution.yaml` courante avant patch (PERPLX_8ZQA le date de `ARBITRAGE_2026_04_01`).
- **Consensus** : weak (1/5 — vérification canonique requise avant patch)

---

### Thème 7 — Pipeline et gouvernance de stages

#### ARB-11 — Ajouter un plan de résolution pour le script STAGE_04

- **Élément concerné** : `platform_factory_state.yaml` + `pipeline.md` STAGE_04
- **Localisation principale** : state (traçabilité du blocker) + pipeline (note de dérogation V0 si applicable)
- **Problème** : le script `validate_platform_factory_patchset.py` est obligatoire pour STAGE_04 mais absent. Blocage silencieux du pipeline.
- **Statut proposé** : `retained`
- **Gravité** : élevée
- **Options** : (a) créer le script en priorité ; (b) définir un protocole de validation manuelle documenté acceptable comme fallback V0 avec limitation explicite ; (c) bloquer STAGE_04 jusqu'à création.
- **Décision proposée** : option (b) pour ce cycle, en attendant la matérialisation de l'outillage. Documenter explicitement dans le state et dans le pipeline.
- **Lieu principal** : state (ajouter dans `blockers` ou `capabilities_absent` avec exit condition) + pipeline (note V0 fallback)
- **Consensus** : strong (4/5)

#### ARB-12 — Aligner `pipeline.md` STAGE_01 avec le launch prompt réel

- **Élément concerné** : `docs/pipelines/platform_factory/pipeline.md` → section STAGE_01_CHALLENGE
- **Localisation** : pipeline
- **Problème** : `pipeline.md` référence le prompt métier partagé (`Challenge_platform_factory.md`) mais le vrai launch prompt d'exécution est `LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md`. Les deux niveaux ne sont pas distingués.
- **Statut proposé** : `retained`
- **Gravité** : modérée
- **Justification** : convergence 3/5 (PERPLX_8ZQA, PERPLX_9KR3 implicitement, PERPLX_K7R2 explicitement).
- **Lieu principal** : pipeline
- **Consensus** : medium

#### ARB-13 — Corriger la convention de nommage des challenge reports dans `pipeline.md`

- **Élément concerné** : `docs/pipelines/platform_factory/pipeline.md` → STAGE_01_CHALLENGE outputs
- **Localisation** : pipeline
- **Problème** : `pipeline.md` utilise `challenge_report_##.md` alors que le launch prompt définit `challenge_run_id` avec format `PFCHAL_YYYYMMDD_AGENTTAG_RAND`.
- **Statut proposé** : `retained`
- **Gravité** : modérée
- **Justification** : identifié par PERPLX_K7R2 (C6). Incohérence concrète mais non critique. Patch simple.
- **Lieu principal** : pipeline
- **Consensus** : weak (1/5 — mais correction évidente)

---

### Thème 8 — State : maturité et classification

#### ARB-14 — Corriger le wording de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

- **Élément concerné** : `platform_factory_state.yaml` → `capabilities_partial.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`
- **Localisation** : state
- **Problème** : "exécutable manuellement" est inexact pour les stages avec script obligatoire.
- **Statut proposé** : `retained`
- **Gravité** : modérée
- **Justification** : convergence 4/5.
- **Lieu principal** : state
- **Consensus** : strong

#### ARB-15 — Corriger le wording de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`

- **Élément concerné** : `platform_factory_state.yaml` → `capabilities_partial.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
- **Localisation** : state
- **Problème** : classée `partial` alors que le régime cible est structurellement bloqué (pas en cours de progression). "Partial" donne un faux sentiment de progression.
- **Statut proposé** : `retained`
- **Gravité** : modérée
- **Justification** : identifié par PERPLX_9KR3 (C6), PERPLX_K7R2 et GPT54_Z4N8.
- **Décision** : soit conserver `partial` avec note explicite que le blocage est structurel, soit créer une classification `blocked_pending_conditions`.
- **Lieu principal** : state
- **Consensus** : medium

#### ARB-16 — Ajouter un plan de résolution pour `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT`

- **Élément concerné** : `platform_factory_state.yaml` → `blockers.PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT`
- **Localisation** : state
- **Problème** : blocker `high` sans plan de résolution, sans date cible, sans responsable désigné.
- **Statut proposé** : `retained`
- **Gravité** : critique (impact gouvernance)
- **Justification** : PERPLEX_9KR4M (C1). Patch simple : ajouter `exit_condition` et note de portage.
- **Lieu principal** : state
- **Consensus** : medium (2/5 explicitement, cohérent avec les autres)

---

### Thème 9 — Gouvernance release / manifest

#### ARB-17 — Documenter l'interdiction de modification directe de `docs/cores/current/`

- **Élément concerné** : `docs/pipelines/platform_factory/pipeline.md` → Rule 6
- **Localisation** : pipeline
- **Problème** : Rule 6 est déclarative sans garde-fou technique. Une modification directe de `current/` reste possible hors STAGE_08.
- **Statut proposé** : `retained` (documentation) / `deferred` (garde-fou technique)
- **Gravité** : modérée
- **Justification** : convergence 4/5. Patch immédiat sur le pipeline (renforcer la règle avec une note d'avertissement) ; le garde-fou technique (branch protection, hook) est `deferred` — hors portée d'un patch YAML.
- **Lieu principal** : pipeline (documentation renforcée)
- **Consensus** : strong

#### ARB-18 — Ajouter le manifest release dans la liste de lecture obligatoire du challenge (STAGE_01)

- **Élément concerné** : `LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md`
- **Localisation** : pipeline
- **Problème** : le manifest release courant n'est pas dans l'ordre de lecture obligatoire du challenge.
- **Statut proposé** : `retained`
- **Gravité** : modérée
- **Justification** : PERPLX_8ZQA (C8).
- **Lieu principal** : pipeline (launch prompt STAGE_01)
- **Consensus** : weak (1/5 — mais pertinent pour la traçabilité)

---

### Thème 10 — Angle mort double-buffer

#### ARB-19 — Signaler l'absence de référence au double-buffer/swap atomique pour les patches factory

- **Élément concerné** : `platform_factory_architecture.yaml` ou `pipeline.md`
- **Localisation** : architecture ou pipeline
- **Problème** : la factory ne mentionne pas l'obligation constitutionnelle de double-buffer/swap atomique pour ses propres patches d'artefacts internes.
- **Statut proposé** : `deferred`
- **Gravité** : modérée
- **Justification** : identifié par PERPLEX_9KR4M uniquement. Non confirmé par les autres rapports. Reporté en attente de consolidation humaine finale pour décider si cette obligation s'applique littéralement aux artefacts YAML factory ou seulement aux runtimes applicatifs.
- **Lieu probable** : architecture (note de traçabilité)
- **Consensus** : weak — nécessite discussion en consolidation finale

---

### Thème 11 — Ajout d'une gate d'inéligibilité aval

#### ARB-20 — Définir des conditions préalables bloquantes pour tout pipeline d'instanciation aval

- **Élément concerné** : `platform_factory_architecture.yaml` (section `variant_governance` ou nouvelle section)
- **Localisation** : architecture
- **Problème** : rien n'empêche un pipeline d'instanciation aval de démarrer tant que des blockers `high` restent ouverts sur la factory.
- **Statut proposé** : `deferred`
- **Gravité** : modérée
- **Justification** : identifié par PERPLX_9KR3 (C3). Valide en intention, mais prématuré pour un patch V0 : il n'existe pas encore de pipeline d'instanciation actif. Documenter l'intention dans le state est suffisant pour ce cycle.
- **Lieu probable** : architecture (à terme) + state (note d'intention immédiate)
- **Consensus** : weak — à prioriser dès l'émergence du pipeline d'instanciation

---

### Thème 12 — Point hors périmètre factory

#### ARB-21 — `declared_autonomy_regime_respected` sans invariant constitutionnel source

- **Élément concerné** : `runtime_policy_conformance_definition.items_to_verify.declared_autonomy_regime_respected`
- **Localisation** : architecture
- **Problème** : obligation sans `invariant_ref` constitutionnel.
- **Statut proposé** : `clarification_required`
- **Gravité** : modérée
- **Justification** : PERPLX_K7R2 (C5). La correction dépend de l'identification de l'invariant constitutionnel source. Si aucun invariant ne le couvre, l'item doit être supprimé ou reformulé comme contrainte factory propre. À vérifier dans le socle canonique avant patch.
- **Pré-condition** : vérifier si un invariant constitutionnel source existe dans `constitution.yaml` pour `declared_autonomy_regime_respected`.
- **Consensus** : weak — clarification humaine requise

---

## Points retenus

| ID | Sujet | Gravité | Lieu principal |
|---|---|---|---|
| ARB-01 | Créer `constitutional_conformance_matrix.yaml` | critique | validator/tooling |
| ARB-02 | Interdire émission de `constitutional_invariants_checked` sans validator | critique | architecture |
| ARB-03 | Reclasser absence validator comme blocker `high` dans state | critique | state |
| ARB-04 | Arbitrer bootstrap_contract : option B (contrainte normative d'interdiction réseau/LLM) | critique | architecture + state |
| ARB-05 | Reclasser `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker | élevé | state |
| ARB-06 | Ajouter `conformance_matrix_availability_status` dans contrat projection | élevé | architecture |
| ARB-07 | Gouverner `usage_as_sole_context: blocked` dans les launch prompts | élevé | pipeline |
| ARB-08 | Ajouter mécanisme de détection de dérive canonique sur `version_fingerprint` | élevé | architecture |
| ARB-09 | Ajouter `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` au contrat minimal | élevé | architecture |
| ARB-10 | Ajouter `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` au contrat minimal | élevé | architecture |
| ARB-11 | Ajouter plan de résolution STAGE_04 (protocole fallback V0) | élevé | state + pipeline |
| ARB-12 | Aligner `pipeline.md` STAGE_01 avec le launch prompt réel | modéré | pipeline |
| ARB-13 | Corriger convention de nommage challenge reports dans `pipeline.md` | modéré | pipeline |
| ARB-14 | Corriger wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | modéré | state |
| ARB-15 | Corriger wording `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` | modéré | state |
| ARB-16 | Ajouter plan de résolution `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` | critique (gouvernance) | state |
| ARB-17 | Renforcer Rule 6 pipeline (documentation interdiction modification directe `current/`) | modéré | pipeline |
| ARB-18 | Ajouter manifest release dans lecture obligatoire STAGE_01 | modéré | pipeline |

## Points rejetés

Aucun finding n'a été rejeté. Les cinq rapports ne contiennent pas de faux finding. Les formulations divergentes ont été fusionnées.

## Points différés

| ID | Sujet | Justification |
|---|---|---|
| ARB-19 | Angle mort double-buffer pour patches factory | Applicabilité à confirmer en consolidation humaine finale |
| ARB-20 | Gate d'inéligibilité pipeline d'instanciation aval | Prématuré : aucun pipeline d'instanciation actif |
| Garde-fou technique Rule 6 | Branch protection / hook | Hors portée patch YAML |
| Protocole multi-IA complet | Décomposition, assemblage, résolution de conflit | Bloqueur identifié, spec à développer dans un cycle dédié |

## Points hors périmètre

- Schémas fins du manifest, configuration, packaging applicatifs : incomplétudes V0 assumées, pas de patch immédiat.
- Gouvernance du futur pipeline d'instanciation domaine : hors scope factory générique.
- Implémentation réelle des validators dédiés : hors portée d'un patch YAML sur architecture/state — nécessite un cycle d'outillage dédié.

## Points sans consensus ou nécessitant discussion finale

| ID | Sujet | Niveau de consensus | Question ouverte |
|---|---|---|---|
| ARB-08 | `version_fingerprint` et détection de dérive canonique | weak (1/5) | Faut-il définir le mécanisme dans l'architecture ou le laisser au validator ? |
| ARB-09 | `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` absent du contrat minimal | weak (1/5) | Confirmer que cet invariant s'applique aux applications produites et non seulement aux patches de la factory elle-même. |
| ARB-10 | `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` absent | weak (1/5) | Vérifier la présence et la formulation exacte dans `constitution.yaml` courante avant patch. |
| ARB-19 | Double-buffer/swap atomique pour patches factory | weak (1/5) | Le double-buffer constitutionnel s'applique-t-il aux artefacts YAML factory (prescriptif/constatif) ou uniquement aux runtimes applicatifs ? |
| ARB-21 | `declared_autonomy_regime_respected` sans invariant source | weak (1/5) | Identifier l'invariant constitutionnel source ou supprimer l'item. |

---

## Corrections à arbitrer avant patch

### Corrections immédiates (architectures + state + pipeline)

Par ordre de priorité :

1. **ARB-02** : Ajouter contrainte normative d'interdiction d'émission de `constitutional_invariants_checked` sans validator — architecture
2. **ARB-04** : Ajouter contrainte normative d'interdiction d'appel réseau/LLM dans tout bootstrap — architecture
3. **ARB-06** : Ajouter `conformance_matrix_availability_status` dans le contrat de projection — architecture
4. **ARB-09** : Ajouter `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` dans `minimum_axes` — architecture (pré-condition : vérification canonique)
5. **ARB-10** : Ajouter `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` — architecture (pré-condition : vérification canonique)
6. **ARB-08** : Ajouter règle de comparaison `version_fingerprint` — architecture
7. **ARB-03** : Reclasser absence validator comme blocker `high` — state
8. **ARB-05** : Reclasser `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker — state
9. **ARB-11** : Ajouter plan de résolution STAGE_04 (protocole fallback) — state + pipeline
10. **ARB-14** : Corriger wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` — state
11. **ARB-15** : Corriger wording `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` — state
12. **ARB-16** : Ajouter exit condition à `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` — state
13. **ARB-07** : Renforcer l'instruction `usage_as_sole_context: blocked` dans les launch prompts — pipeline
14. **ARB-12** : Aligner `pipeline.md` STAGE_01 avec le launch prompt — pipeline
15. **ARB-13** : Corriger convention de nommage challenge reports — pipeline
16. **ARB-17** : Renforcer Rule 6 (documentation) — pipeline
17. **ARB-18** : Ajouter manifest release dans lecture STAGE_01 — pipeline

### Hors patch immédiat (nécessite cycle dédié)

- ARB-01 : création de `constitutional_conformance_matrix.yaml` — cycle outillage dédié
- ARB-20 : gate d'inéligibilité aval — différé
- ARB-19 : double-buffer — clarification humaine d'abord

---

*Fin de la proposition d'arbitrage — PFARB_20260410_PERPLEX_X7Q2*
