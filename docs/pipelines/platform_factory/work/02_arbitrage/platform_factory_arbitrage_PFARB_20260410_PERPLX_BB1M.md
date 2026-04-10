# PROPOSITION D'ARBITRAGE — STAGE_02_FACTORY_ARBITRAGE

**arbitrage_run_id** : `PFARB_20260410_PERPLX_BB1M`  
**Date** : 2026-04-10  
**IA** : PERPLX (Perplexity)  
**Challenge reports considérés** :
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_9KR3.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_K7R2.md`

**Prompt canonique de cadrage** : `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

---

## Résumé exécutif

Les deux challenge reports convergent sur l'essentiel : la Platform Factory V0.4.0 est une baseline de gouvernance architecturalement saine, mais elle ne peut pas encore produire d'artefact constitutionnellement probant. Cinq zones de risque structurel sont confirmées avec fort consensus entre les deux rapports :

1. **Validator absent** (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED`) → toute déclaration de conformité constitutionnelle est non auditable.
2. **`constitutional_conformance_matrix.yaml` absent** → référence obligatoire inutilisable par toute projection ou application produite.
3. **`bootstrap_contract` TBD** → aucune application ne peut passer la validation complète du contrat minimal.
4. **`PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` classé `known_gap` mais désigné "BLOCKER OPÉRATIONNEL"** → asymétrie de classification masquant l'impact réel.
5. **Script `validate_platform_factory_patchset.py` absent** → STAGE_04 non exécutable dans sa forme canonique.

Quatre corrections supplémentaires sont retenues à priorité modérée. Deux points donnent lieu à des formulations divergentes entre les rapports (wording de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`, mécanisme de détection de dérive canonique) et sont soumis à clarification en consolidation finale.

Cette proposition ne constitue pas l'arbitrage canonique final. Elle vise à fournir une contribution structurée et complète pour la consolidation humaine-assistée.

---

## Synthèse des constats convergents

Les deux rapports partagent les constats suivants, formulés de façon convergente :

| Sujet | Convergence |
|---|---|
| Validator dédié absent → conformité constitutionnelle non auditable | **Forte** — identique dans les deux rapports |
| `constitutional_conformance_matrix.yaml` absent — bloque projections et signal observabilité | **Forte** — identique |
| `bootstrap_contract` TBD obligatoire — bloque validation complète du contrat minimal | **Forte** — identique |
| `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` : classement `known_gap` asymétrique vs description "BLOCKER OPÉRATIONNEL" | **Forte** — identique |
| Script STAGE_04 absent — blocage silencieux du pipeline | **Forte** — identique |
| `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` wording "exécutable manuellement" inexact pour STAGE_04 | **Forte** — identique |
| Incohérence nommage `challenge_report_##.md` dans `pipeline.md` vs convention `PFCHAL_...` du launch prompt | **Forte** — soulevée uniquement par K7R2 mais confirmable |
| Absence de gate d'inéligibilité vers pipeline d'instanciation aval | **Forte** — 9KR3 développé, K7R2 évoqué implicitement |
| Surdéclaration de maturité sur `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` (`partial` alors que blocage structurel) | **Moyenne** — 9KR3 propose `absent_pending_conditions`, K7R2 indique `partial` avec note — voir §Points sans consensus |
| `declared_autonomy_regime_respected` sans invariant constitutionnel source | **Moyenne** — K7R2 développé, 9KR3 non explicitement |
| Mécanisme de détection de dérive canonique pour projections (`version_fingerprint` sans comparaison) | **Moyenne** — soulevé uniquement par K7R2 |
| `reproducibility_fingerprints` en intention sans format obligatoire | **Faible** — 9KR3 relevé, K7R2 mentionné |

---

## Propositions d'arbitrage par thème

---

### THEME A — Compatibilité constitutionnelle et validators

---

#### ARB-A1 — Élever l'absence de validator au rang de blocker `high`

- **Élément concerné** : `capabilities_absent.PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED`
- **Sources** : 9KR3 (C1), K7R2 (Critique — validator absent)
- **Problème** : l'absence du validator implique que `constitutional_invariants_checked` est non auditable, que tout `validation_status: validated` sur projection est non déterministe, et qu'aucune application produite ne peut prouver sa conformité constitutionnelle.
- **Statut proposé** : **retained_now**
- **Lieu principal** : state
- **Lieux secondaires** : aucun (l'architecture documente déjà cette limite)
- **Priorité** : critique
- **Justification** : risque de violation silencieuse des invariants `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`. L'absence de validator ne peut pas rester classée uniquement en `capabilities_absent` sans être un bloqueur formel.
- **Impact si non traité** : la factory produit des artefacts déclarant la conformité constitutionnelle sans preuve vérifiable.
- **Correction à arbitrer** : déplacer `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` dans `blockers` avec sévérité `high`, exit condition = implémentation des trois validators prioritaires (`derived_projection_conformance`, `minimum_contract_conformance`, `runtime_policy_conformance`).
- **Niveau de consensus** : **strong**

---

#### ARB-A2 — Créer `constitutional_conformance_matrix.yaml`

- **Élément concerné** : `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` + `conformance_matrix_ref` dans l'architecture
- **Sources** : 9KR3 (R2), K7R2 (C1 — Critique)
- **Problème** : fichier obligatoire absent. Toute projection et tout signal `constitutional_invariants_checked` y font référence. En l'état, la référence pointe un artefact inexistant.
- **Statut proposé** : **retained_now**
- **Lieu principal** : nouveau fichier `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`
- **Lieux secondaires** : architecture (champ `conformance_matrix_ref` à maintenir, état `unavailable` à signaler) ; state (mise à jour de `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` à la levée)
- **Priorité** : critique
- **Justification** : condition de déblocage de `usage_as_sole_context`. Sans ce fichier, aucune projection ne peut être auditée dans son scope. C'est le trou normatif le plus direct de la V0.
- **Impact si non traité** : cycle de déblocage du régime cible de projection bloqué indéfiniment. Risque de dérive normative silencieuse non détectable.
- **Pré-condition** : dépend partiellement de ARB-A1 (validator dédié) pour être opérationnelle, mais la matrice peut être créée (même minimalement) avant que le validator soit implémenté.
- **Note de séquencement** : créer la matrice minimale en premier ; lier l'implémentation du validator à la matrice en second.
- **Niveau de consensus** : **strong**

---

#### ARB-A3 — Signaler l'indisponibilité de `constitutional_conformance_matrix.yaml` dans le contrat de projection

- **Élément concerné** : `execution_projection_contract.mandatory_fields_per_projection.conformance_matrix_ref`
- **Sources** : 9KR3 (C5)
- **Problème** : une IA consommant une projection peut tenter d'utiliser la matrice sans savoir qu'elle est absente. Aucun signal explicite dans la projection elle-même.
- **Statut proposé** : **retained_now**
- **Lieu principal** : architecture
- **Priorité** : modéré
- **Justification** : correction de traçabilité exploitabilité IA, complémentaire à ARB-A2. Peut être traitée dans le même cycle de patch.
- **Niveau de consensus** : **medium** (soulevé uniquement par 9KR3 ; K7R2 ne contredit pas mais n'explicite pas)

---

### THEME B — Contrat minimal d'application

---

#### ARB-B1 — Borner explicitement l'absence du `bootstrap_contract`

- **Élément concerné** : `runtime_entrypoint_contract.bootstrap_contract` (TBD) dans l'architecture
- **Sources** : 9KR3 (R5), K7R2 (C2 — Critique)
- **Problème** : champ obligatoire `required: true` déclaré TBD. Aucune application ne peut passer la validation complète du contrat minimal.
- **Statut proposé** : **retained_now** — mais avec deux options d'arbitrage à trancher en consolidation finale :
  - **Option A** : définir une première version minimale du `bootstrap_contract`
  - **Option B** : arbitrer que les axes dépendants sont en état `DEFERRED_UNTIL_BOOTSTRAP_DEFINED` et l'inscrire explicitement dans le contrat minimal
- **Lieu principal** : architecture
- **Lieux secondaires** : state (mise à jour du blocker `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED`)
- **Priorité** : critique (impact cascade sur axes `structure_and_state_alignment` et `runtime_policy_conformance`)
- **Pré-condition** : choix entre Option A et Option B à valider en consolidation humaine.
- **Niveau de consensus** : **strong**

---

#### ARB-B2 — Relier `declared_autonomy_regime_respected` à un invariant constitutionnel source

- **Élément concerné** : `runtime_policy_conformance_definition.declared_autonomy_regime_respected`
- **Sources** : K7R2 (C5 — Modéré)
- **Problème** : obligation dans le contrat minimal sans référence à un invariant constitutionnel source — non auditable constitutionnellement.
- **Statut proposé** : **retained_now**
- **Lieu principal** : architecture
- **Priorité** : modéré
- **Justification** : tout item de `runtime_policy_conformance` doit être relié à un invariant constitutionnel source ou supprimé s'il n'en trouve pas. Le principe de séparation Constitution / architecture factory l'exige.
- **Niveau de consensus** : **medium** (soulevé uniquement par K7R2 ; non contredit par 9KR3)

---

#### ARB-B3 — Préciser le format attendu des `reproducibility_fingerprints`

- **Élément concerné** : `reproducibility_fingerprints` dans le contrat minimal application
- **Sources** : 9KR3 (R10), K7R2 (Axe 4)
- **Problème** : défini en intention ("hash ou identifiant de version stable") sans format contraint. Deux IA pourraient produire des fingerprints incomparables.
- **Statut proposé** : **deferred** — acceptable en V0 tant qu'aucune application n'est instanciée, mais doit être bornée avant tout premier cycle formel.
- **Lieu principal** : architecture
- **Priorité** : faible
- **Niveau de consensus** : **medium**

---

### THEME C — Gouvernance state et classification des blockers

---

#### ARB-C1 — Créer le blocker formel pour `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED`

- **Élément concerné** : `known_gaps.PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` dans le state
- **Sources** : 9KR3 (C2 — Élevé), K7R2 (Élevé)
- **Problème** : classé `known_gap` mais décrit "BLOCKER OPÉRATIONNEL". Asymétrie de classification masquant l'impact réel sur la promesse `PF_PRINCIPLE_MULTI_IA_READY`.
- **Statut proposé** : **retained_now**
- **Lieu principal** : state
- **Priorité** : élevé
- **Justification** : un élément décrit comme "BLOCKER OPÉRATIONNEL" doit être un blocker formel avec sévérité et exit condition. La discordance texte/classification est un défaut de gouvernance en soi, indépendamment du fond.
- **Impact si non traité** : la factory ne peut pas garantir sa promesse multi-IA. Tout usage parallèle réel est exposé à des collisions non gérées.
- **Correction à arbitrer** : déplacer dans `blockers`, sévérité `high`, exit condition = spec du protocole multi-IA (décomposition, assemblage, résolution de conflit).
- **Niveau de consensus** : **strong**

---

#### ARB-C2 — Corriger le wording de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

- **Élément concerné** : `capabilities_partial.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`
- **Sources** : 9KR3 (Axe 2), K7R2 (C3 — Modéré)
- **Problème** : "exécutable manuellement" inexact pour les stages avec script obligatoire (STAGE_04 bloqué par script absent).
- **Statut proposé** : **retained_now**
- **Lieu principal** : state
- **Priorité** : modéré
- **Justification** : défaut de maturité surdéclarée. Un opérateur lisant le state croit pouvoir exécuter STAGE_04 manuellement.
- **Correction à arbitrer** : préciser "exécutable manuellement pour les stages sans script obligatoire ; STAGE_04 bloqué par absence de `validate_platform_factory_patchset.py`".
- **Niveau de consensus** : **strong**

---

#### ARB-C3 — Tracer la disponibilité du script STAGE_04 dans le state

- **Élément concerné** : `capabilities_absent` — script `validate_platform_factory_patchset.py`
- **Sources** : 9KR3 (C4), K7R2 (Élevé)
- **Problème** : script requis par STAGE_04 non tracé dans le state. Son absence bloquerait tout le pipeline à partir de STAGE_04 sans que le state le signale.
- **Statut proposé** : **retained_now**
- **Lieu principal** : state
- **Priorité** : modéré
- **Correction à arbitrer** : ajouter la disponibilité du script comme sous-condition dans `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` ou créer une entrée dédiée.
- **Niveau de consensus** : **strong**

---

### THEME D — Pipeline et implémentabilité

---

#### ARB-D1 — Corriger l'incohérence de convention de nommage des challenge reports dans `pipeline.md`

- **Élément concerné** : convention `work/01_challenge/challenge_report_##.md` dans `pipeline.md`
- **Sources** : K7R2 (C6 — Modéré)
- **Problème** : `pipeline.md` indique `challenge_report_##.md` (numéro de run) ; le launch prompt `LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md` définit la convention `PFCHAL_YYYYMMDD_AGENTTAG_RAND`. Incohérence créant un risque d'ambiguïté pour une IA lisant le pipeline sans le launch prompt.
- **Statut proposé** : **retained_now**
- **Lieu principal** : pipeline (`pipeline.md`)
- **Priorité** : modéré
- **Niveau de consensus** : **medium** (soulevé par K7R2 uniquement ; 9KR3 ne contredit pas)

---

#### ARB-D2 — Ajouter une gate d'inéligibilité vers le pipeline d'instanciation aval

- **Élément concerné** : frontière factory / pipeline d'instanciation (Axe 3 des deux rapports)
- **Sources** : 9KR3 (C3)
- **Problème** : rien n'empêche un pipeline d'instanciation aval de démarrer tant que des blockers `high` restent ouverts. Risque de travail inutilisable.
- **Statut proposé** : **retained_now**
- **Lieu principal** : architecture (section `variant_governance` ou nouvelle section `factory_to_instantiation_boundary`)
- **Lieux secondaires** : pipeline (`pipeline.md`)
- **Priorité** : modéré
- **Niveau de consensus** : **medium** (développé par 9KR3 ; implicite dans K7R2)

---

#### ARB-D3 — Borner le mécanisme de détection de dérive canonique pour les projections

- **Élément concerné** : `version_fingerprint` dans les champs obligatoires de projection
- **Sources** : K7R2 (C4 — Élevé)
- **Problème** : une mise à jour de `constitution.yaml` n'invalide pas automatiquement les projections existantes. La responsabilité de comparaison n'est pas assignée.
- **Statut proposé** : **retained_now** pour la définition de la règle ; **deferred** pour son outillage
- **Lieu principal** : architecture (règle dans le contrat de projection)
- **Lieux secondaires** : pipeline (STAGE_01 ou STAGE_04)
- **Priorité** : élevé
- **Justification** : risque de dérive normative silencieuse documenté à l'Axe 5 des deux rapports. La règle peut être définie architecturalement sans attendre le validator.
- **Niveau de consensus** : **medium** (développé par K7R2 ; 9KR3 traite le problème en Axe 5 sans formaliser ce point précis)

---

### THEME E — Points différés et hors périmètre

---

#### ARB-E1 — `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` : classification `partial` vs `absent_pending_conditions`

- **Élément concerné** : `capabilities_partial.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`
- **Sources** : 9KR3 (C6 — propose `absent_pending_conditions`), K7R2 (indique `partial` avec note explicite)
- **Problème** : le régime cible est `blocked` par deux conditions absentes. 9KR3 propose de reclassifier en `absent_pending_conditions` ou d'ajouter `blocked_pending_conditions`. K7R2 conserve `partial` mais avec une note explicite de blocage structurel.
- **Statut proposé** : **clarification_required** — les deux options sont défendables ; voir §Points sans consensus
- **Lieu principal** : state
- **Priorité** : faible à modéré
- **Niveau de consensus** : **conflicting** (formulations divergentes ; fond convergent)

---

#### ARB-E2 — Absence de rollback explicite dans le pipeline

- **Sources** : 9KR3 (Axe 9 — incomplétude V0 normale)
- **Statut proposé** : **deferred** — incomplétude V0 reconnue, sans risque immédiat dans un pipeline manuel.
- **Lieu principal** : pipeline
- **Priorité** : faible
- **Niveau de consensus** : **strong**

---

#### ARB-E3 — `evidence` auto-référentielle (deux entrées seulement)

- **Sources** : 9KR3, K7R2
- **Statut proposé** : **deferred** — normal en V0 sans cycle formel complété. À enrichir lors d'un premier cycle réel.
- **Lieu principal** : state
- **Priorité** : faible
- **Niveau de consensus** : **strong**

---

#### ARB-E4 — Companion prompts (`Make21`, `Make22`, `Make23`) non vérifiés

- **Sources** : K7R2 (Axe 9)
- **Statut proposé** : **deferred** — vérification hors périmètre de cet arbitrage ; à tracer si nécessaire.
- **Lieu principal** : hors périmètre direct du patch
- **Priorité** : faible
- **Niveau de consensus** : **weak**

---

## Points retenus (synthèse)

| ID | Sujet | Lieu | Priorité |
|---|---|---|---|
| ARB-A1 | Validator absent → blocker `high` dans state | state | critique |
| ARB-A2 | Créer `constitutional_conformance_matrix.yaml` | nouveau fichier + architecture + state | critique |
| ARB-B1 | `bootstrap_contract` TBD → borner ou définir (choix à trancher) | architecture + state | critique |
| ARB-A3 | Signal indisponibilité matrice dans contrat projection | architecture | modéré |
| ARB-B2 | `declared_autonomy_regime_respected` → invariant constitutionnel source | architecture | modéré |
| ARB-C1 | `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` → blocker `high` | state | élevé |
| ARB-C2 | Wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` corrigé | state | modéré |
| ARB-C3 | Script STAGE_04 tracé dans state | state | modéré |
| ARB-D1 | Nommage challenge reports aligné dans `pipeline.md` | pipeline | modéré |
| ARB-D2 | Gate d'inéligibilité factory → instanciation aval | architecture + pipeline | modéré |
| ARB-D3 | Règle de dérive canonique pour projections (règle maintenant, outillage différé) | architecture | élevé |

---

## Points rejetés

Aucun finding n'est rejeté. Tous les findings des deux rapports sont soit retenus, différés, ou soumis à clarification.

---

## Points différés

| ID | Sujet | Raison | Lieu |
|---|---|---|---|
| ARB-B3 | Format `reproducibility_fingerprints` | V0 acceptable tant qu'aucune application instanciée | architecture |
| ARB-E2 | Rollback explicite pipeline | V0 normale, pipeline manuel | pipeline |
| ARB-E3 | Evidence auto-référentielle | V0 normale, enrichir au premier cycle | state |
| ARB-E4 | Companion prompts non vérifiés | Hors périmètre direct | — |

---

## Points hors périmètre

Aucun finding n'est classé hors périmètre factory. Les sujets liés au pipeline d'instanciation aval relèvent bien de la factory (gate d'inéligibilité) et non du domaine spécifique.

---

## Points sans consensus ou nécessitant discussion finale

### CONF-1 — Classification de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`

- **9KR3** propose `absent_pending_conditions` ou `blocked_pending_conditions` (reclassification structurelle)
- **K7R2** conserve `partial` avec une note explicite sur le blocage structurel
- **Fond** : les deux rapports s'accordent que le blocage est structurel et non progressif
- **Question à trancher** : faut-il créer un nouveau statut de classification (`blocked_pending_conditions`) ou maintenir `partial` avec wording renforcé ? La création d'un nouveau statut a des implications sur la cohérence du schéma state global.
- **Recommandation de l'arbitrage** : maintenir `partial` mais ajouter une note explicite de blocage structurel dans le wording — option moins invasive en V0. La création d'un nouveau statut relève d'une évolution de schéma à préparer en STAGE_03 si la factory décide d'enrichir les statuts de capacité.

### CONF-2 — `bootstrap_contract` : Option A vs Option B (ARB-B1)

- **9KR3** et **K7R2** convergent sur la critique mais ne proposent pas la même issue :
  - K7R2 (C2) propose deux options symétriques (définir une première version ou déclarer `DEFERRED_UNTIL_BOOTSTRAP_DEFINED`)
  - 9KR3 ne précise pas l'option préférée
- **Décision humaine requise** : définir une première version minimale exige de trancher la "typologie exacte des runtimes" — question métier hors portée de l'arbitrage IA.
- **Recommandation de l'arbitrage** : retenir l'Option B en attendant la définition des runtimes, avec inscription explicite dans le contrat minimal.

---

## Corrections à arbitrer avant patch (consolidée)

### CORR-1 — state : élever validator absent en blocker `high`
- Déplacer `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` de `capabilities_absent` vers `blockers`, sévérité `high`, avec exit condition explicite (trois validators prioritaires).

### CORR-2 — nouveau fichier + architecture : créer `constitutional_conformance_matrix.yaml` minimal
- Créer `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` avec liste des invariants constitutionnels couverts et leur statut de couverture.
- Ajouter dans l'architecture un champ `conformance_matrix_availability_status` dans le contrat de projection pour signaler l'indisponibilité.

### CORR-3 — architecture : borner le `bootstrap_contract`
- Option retenue : arbitrer que les axes dépendants sont en état `DEFERRED_UNTIL_BOOTSTRAP_DEFINED` et l'inscrire dans le contrat minimal.
- Mettre à jour le blocker `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` dans le state pour refléter cet arbitrage explicite.

### CORR-4 — state : créer blocker formel pour multi-IA
- Déplacer `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` vers `blockers`, sévérité `high`, exit condition = spec protocole multi-IA (décomposition, assemblage, résolution de conflit).

### CORR-5 — state : corriger wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`
- Préciser que l'exécutabilité manuelle est limitée aux stages sans script obligatoire ; STAGE_04 est bloqué par l'absence du script.

### CORR-6 — state : tracer script STAGE_04
- Ajouter sous-condition de disponibilité de `validate_platform_factory_patchset.py` dans `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` (ou entrée dédiée).

### CORR-7 — architecture : ajouter invariant source pour `declared_autonomy_regime_respected`
- Ajouter un `invariant_ref` vers la Constitution pour cet item de `runtime_policy_conformance`, ou supprimer l'item si aucun invariant ne le couvre.

### CORR-8 — architecture : règle de détection de dérive canonique pour les projections
- Ajouter dans le contrat de projection une règle décrivant : qui compare le `version_fingerprint`, à quel moment, et quelle est la conséquence d'une divergence canonique.

### CORR-9 — architecture + pipeline : gate d'inéligibilité factory → instanciation aval
- Définir dans l'architecture les conditions préalables bloquantes (blockers `high` devant être levés) pour toute instanciation aval. Mentionner dans `pipeline.md`.

### CORR-10 — pipeline : aligner convention nommage challenge reports
- Remplacer `challenge_report_##.md` par la convention `challenge_run_id` (`PFCHAL_YYYYMMDD_AGENTTAG_RAND`) dans `pipeline.md`.

---

## Répartition par lieu de correction

| Lieu | Corrections |
|---|---|
| **state** | CORR-1, CORR-4, CORR-5, CORR-6 |
| **architecture** | CORR-2 (partiel), CORR-3, CORR-7, CORR-8, CORR-9 (partiel) |
| **nouveau fichier** | CORR-2 (`constitutional_conformance_matrix.yaml`) |
| **pipeline** | CORR-9 (partiel), CORR-10 |
| **validator/tooling** | ARB-D3 (outillage différé) |
| **release governance** | aucune correction immédiate |

---

## Séquencement recommandé

1. **D'abord** : CORR-2 (créer la matrice minimale) + CORR-1 (élever validator en blocker) → débloquent la chaîne de conformité constitutionnelle
2. **Ensuite** : CORR-3 (borner bootstrap_contract) + CORR-4 (blocker multi-IA) → ferment les deux autres trous critiques
3. **En parallèle** : CORR-5, CORR-6, CORR-7, CORR-10 → corrections de wording et de traçabilité dans state et pipeline
4. **En dernier** : CORR-8, CORR-9 → enrichissements architecturaux conditionnant l'évolution future

---

## Priorités de patch

| Priorité | Corrections |
|---|---|
| **Critique** | CORR-1, CORR-2, CORR-3 |
| **Élevé** | CORR-4, CORR-8 |
| **Modéré** | CORR-5, CORR-6, CORR-7, CORR-9, CORR-10 |
| **Faible** | ARB-B3, ARB-E2, ARB-E3 (différés) |

---

*Fin de la proposition d'arbitrage — PFARB_20260410_PERPLX_BB1M*
