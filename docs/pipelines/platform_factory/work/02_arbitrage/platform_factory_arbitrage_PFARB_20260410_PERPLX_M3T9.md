# STAGE_02_FACTORY_ARBITRAGE — Proposition d'arbitrage Platform Factory

**arbitrage_run_id :** `PFARB_20260410_PERPLX_M3T9`
**Date :** 2026-04-10
**IA :** PERPLX (Perplexity)

**Challenge reports considérés :**
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_K7R2.md`

**Artefacts de référence :**
- `docs/cores/current/platform_factory_architecture.yaml` (PLATFORM_FACTORY_ARCHITECTURE_V0_4)
- `docs/cores/current/platform_factory_state.yaml` (PLATFORM_FACTORY_STATE_V0_4)
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`
- `docs/pipelines/platform_factory/pipeline.md`

---

## Résumé d'arbitrage

Le challenge PFCHAL_20260410_PERPLX_K7R2 identifie 10 points significatifs (3 critiques, 3 élevés, 3 modérés, 1 faible). L'arbitrage présent les répartit en :

- **6 retenus immédiatement** (dont les 3 critiques et 2 élevés)
- **1 clarification préalable requise** (C4 — mécanisme fingerprint)
- **2 reportés V0 assumés** (protocole multi-IA, format rapport de validation)
- **1 rejeté** (evidence insuffisante — V0 normale, pas d'action requise)

Aucun finding ne nécessite d'être reclassé hors périmètre factory. Aucune contradiction entre reports (un seul report disponible).

Le patch qui suivra peut être lancé sur les 6 points retenus. Les 2 reportés devront être inscrits explicitement dans le state avec un wording honnête.

---

## Findings consolidés

Un seul challenge report disponible. Pas de doublons ni de désaccords à trancher.

Les findings du rapport PFCHAL_20260410_PERPLX_K7R2 sont repris ci-dessous avec leur numéro d'origine (C1 à C6 + risques sans ID explicite dans le rapport).

---

## Décisions immédiates

---

### ARB_D01 — Matérialiser `constitutional_conformance_matrix.yaml`

- **Decision ID :** ARB_D01
- **Sujet :** `constitutional_conformance_matrix.yaml` absent alors que plusieurs mécanismes de la factory (signal `constitutional_invariants_checked`, `conformance_matrix_ref` dans les projections dérivées) s'y réfèrent comme obligatoire
- **Source(s) :** C1 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `retained_now`
- **Lieu principal de traitement :** validator/tooling (nouveau fichier `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`)
- **Lieu(x) secondaire(s) :** architecture (binding du champ `conformance_matrix_ref`), state (mise à jour de `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` en résolu après création)
- **Priorité :** Critique
- **Justification :** Sans ce fichier, aucune projection dérivée ne peut être auditée dans son scope déclaré, et aucun signal `constitutional_invariants_checked` n'est probant. Ce n'est pas une lacune V0 acceptable : c'est un trou de validation constitutionnelle actif qui bloque l'usage opérationnel des projections.
- **Impact si non traité :** Une IA peut produire une projection `validated` qui viole un invariant constitutionnel sans que la factory le détecte. Risque de conformité constitutionnelle direct.
- **Pré-condition éventuelle :** Aucune — ce fichier peut être créé sans dépendance sur d'autres corrections.
- **Note de séquencement :** À traiter en premier dans le patch, car il débloque ARB_D05 (validator dédié) et rend ARB_D03 (bootstrap_contract) plus traçable.

---

### ARB_D02 — Définir le `bootstrap_contract` ou borner explicitement son absence

- **Decision ID :** ARB_D02
- **Sujet :** `runtime_entrypoint_contract.bootstrap_contract` déclaré TBD obligatoire dans l'architecture. Aucune application produite ne peut passer la validation complète du contrat minimal.
- **Source(s) :** C2 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `retained_now` — mais sous forme de bornage explicite, pas d'une définition complète
- **Lieu principal de traitement :** architecture
- **Lieu(x) secondaire(s) :** state (mise à jour `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED`)
- **Priorité :** Critique
- **Justification :** Le caractère TBD sans bornage formel signifie que les axes de validation `structure_and_state_alignment` et `runtime_policy_conformance` ne peuvent pas être complétés. Il n'est pas nécessaire de définir un bootstrap_contract complet en V0, mais il est nécessaire d'inscrire dans l'architecture que ces axes sont en état `DEFERRED_UNTIL_BOOTSTRAP_DEFINED` — ce qui n'est pas le cas actuellement. Cette clarification rend le contrat minimal honnête et le patch propre.
- **Impact si non traité :** Tout rapport de validation d'application produite qui passe PASS sur ces axes en V0 est trompeur.
- **Pré-condition éventuelle :** Aucune.
- **Note de séquencement :** Traitable en parallèle de ARB_D01.

---

### ARB_D03 — Corriger le wording de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

- **Decision ID :** ARB_D03
- **Sujet :** `capabilities_partial` → `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` dit "exécutable manuellement" alors que STAGE_04 n'est pas exécutable (script absent).
- **Source(s) :** C3 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `retained_now`
- **Lieu principal de traitement :** state
- **Lieu(x) secondaire(s) :** aucun
- **Priorité :** Modéré
- **Justification :** Correction de wording pure dans un artefact constatif. Elle ne change pas l'architecture ni le pipeline, mais corrige un faux sentiment de capacité qui induit en erreur un opérateur humain ou une IA lisant le state sans le launch prompt. C'est un défaut de maturité surdéclarée mineure mais détectable.
- **Impact si non traité :** Un opérateur croit que STAGE_04 est exécutable manuellement et le lance sans le script, produisant un état intermédiaire invalide.
- **Pré-condition éventuelle :** Aucune.
- **Note de séquencement :** Patch trivial, peut être groupé avec les corrections state.

---

### ARB_D04 — Relier `declared_autonomy_regime_respected` à un invariant constitutionnel source

- **Decision ID :** ARB_D04
- **Sujet :** L'item `declared_autonomy_regime_respected` dans `runtime_policy_conformance` n'est pas relié à un invariant constitutionnel explicite.
- **Source(s) :** C5 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `retained_now`
- **Lieu principal de traitement :** architecture
- **Lieu(x) secondaire(s) :** aucun
- **Priorité :** Modéré
- **Justification :** Cette obligation est non auditable constitutionnellement sans `invariant_ref`. Le risque est réel : si aucun invariant canonique ne couvre cet item, il ne devrait pas figurer comme obligation de validation. Si un invariant le couvre, le binding doit être explicite. L'arbitrage retient une correction de traçabilité dans l'architecture : soit ajouter le `invariant_ref`, soit supprimer l'item. La décision finale (ajouter ou supprimer) est laissée au patch — les deux options sont valides.
- **Impact si non traité :** Obligation de validation orpheline, non reproductible entre IA.
- **Pré-condition éventuelle :** Vérifier dans `constitution.yaml` si un invariant couvre le "régime d'autonomie déclaré". Si oui → ajouter `invariant_ref`. Si non → supprimer l'item.
- **Note de séquencement :** Dépend d'une lecture de `constitution.yaml` — à vérifier lors du patch STAGE_03.

---

### ARB_D05 — Corriger l'incohérence de convention de nommage challenge_report dans `pipeline.md`

- **Decision ID :** ARB_D05
- **Sujet :** `pipeline.md` utilise `challenge_report_##.md` alors que le launch prompt définit `challenge_run_id` au format `PFCHAL_YYYYMMDD_AGENTTAG_RAND`.
- **Source(s) :** C6 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `retained_now`
- **Lieu principal de traitement :** pipeline
- **Lieu(x) secondaire(s) :** aucun
- **Priorité :** Modéré
- **Justification :** Incohérence entre deux artefacts de gouvernance du même pipeline. Le launch prompt est plus récent et plus précis — c'est lui qui fait autorité. Aligner `pipeline.md` évite toute confusion IA lors d'une lecture du pipeline sans le launch prompt.
- **Impact si non traité :** Une IA lisant uniquement `pipeline.md` produit un fichier au nommage incompatible avec la convention du launch prompt.
- **Pré-condition éventuelle :** Aucune.
- **Note de séquencement :** Correction pipeline mineure, groupable avec d'autres corrections pipeline.

---

### ARB_D06 — Inscrire explicitement la dépendance de cycle de déblocage `usage_as_sole_context`

- **Decision ID :** ARB_D06
- **Sujet :** Le cycle de déblocage `usage_as_sole_context: blocked` → `validator_dédié_implémenté` → `constitutional_conformance_matrix` n'a pas de point d'entrée clair. Le bloqueur existe mais le chemin de résolution n'est pas traçable.
- **Source(s) :** Axe 5 risque 5 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `retained_now` — sous forme d'ajout de traçabilité dans le state
- **Lieu principal de traitement :** state
- **Lieu(x) secondaire(s) :** architecture (si la règle de déblocage doit être prescriptive)
- **Priorité :** Élevé
- **Justification :** Sans point d'entrée de déblocage explicite, `usage_as_sole_context` reste bloqué indéfiniment même après la création de `constitutional_conformance_matrix.yaml`. Il faut inscrire dans le state que ARB_D01 (matérialisation de la matrice) constitue la pré-condition de déblocage du validator, et que le validator est la pré-condition de déblocage de `usage_as_sole_context`. Ce chaînage doit être tracé.
- **Impact si non traité :** Après ARB_D01, aucune IA ne sait que le bloqueur `usage_as_sole_context` peut maintenant être avancé.
- **Pré-condition éventuelle :** ARB_D01 retenu.
- **Note de séquencement :** À traiter après ARB_D01 dans le même cycle de patch.

---

## Clarifications requises avant patch

---

### ARB_C01 — Mécanisme de détection de dérive canonique pour `version_fingerprint`

- **Decision ID :** ARB_C01
- **Sujet :** `version_fingerprint` dans les champs obligatoires de projection est défini sans mécanisme de comparaison. Une mise à jour de `constitution.yaml` n'invalide pas automatiquement les projections existantes.
- **Source(s) :** C4 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `clarification_required`
- **Lieu principal de traitement :** architecture
- **Lieu(x) secondaire(s) :** pipeline (STAGE_01 ou STAGE_04 — responsabilité de la vérification)
- **Priorité :** Élevé
- **Justification :** La correction est architecturalement justifiée mais exige une décision de design préalable que l'arbitrage seul ne peut pas trancher : qui est responsable de comparer les fingerprints (factory pipeline, IA, opérateur humain) ? À quelle fréquence ? Sur quel trigger ? Sans réponse à ces questions, un patch de l'architecture produirait une règle soit trop vague (inutile), soit trop prescriptive (irréaliste en V0).
- **Clarification manquante :** Décision humaine sur la responsabilité et le trigger de comparaison des fingerprints.
- **Impact si non traité :** Projections potentiellement dérivées d'un canonique obsolète sans détection.
- **Pré-condition éventuelle :** Discussion opérateur humain. Peut être traitée en STAGE_03 si l'opérateur décide d'une règle simple (ex : "vérification manuelle obligatoire en STAGE_01 de chaque run").

---

## Reports assumés

---

### ARB_R01 — Protocole d'assemblage multi-IA

- **Decision ID :** ARB_R01
- **Sujet :** `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` — absence de protocole d'assemblage, de points d'assemblage concrets, et de convention de granularité modulaire pour le travail multi-IA en parallèle.
- **Source(s) :** Axe 7 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `deferred`
- **Lieu principal de traitement :** architecture + pipeline (cycle ultérieur)
- **Priorité :** Élevé (mais reporté V0 assumé)
- **Justification :** Ce gap est correctement classé `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` dans le state. Le reporter n'est pas une tolérance d'un trou normatif dangereux : tant qu'aucun run multi-IA réel n'est lancé, le risque ne se matérialise pas. La correction nécessite une réflexion de design plus profonde sur les scopes de projection, les points d'assemblage et les conventions de nommage de run. Ce n'est pas patchable proprement en V0 sans un niveau de spécification qui dépasse le scope de ce cycle.
- **Condition de réactivation :** Dès qu'un premier run multi-IA est envisagé, ce report doit être rouvert en priorité critique.
- **Wording state requis :** Le state doit indiquer explicitement "protocole d'assemblage absent — usage multi-IA réel bloqué jusqu'à résolution" (correction de wording, pas ajout de capacité).

---

### ARB_R02 — Format de rapport de validation d'application produite

- **Decision ID :** ARB_R02
- **Sujet :** Absence d'obligation explicite sur le format de rapport de validation des axes minimaux du contrat. Deux IA produiraient deux rapports non comparables.
- **Source(s) :** Axe 4 (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `deferred`
- **Lieu principal de traitement :** architecture (cycle ultérieur)
- **Priorité :** Modéré
- **Justification :** Ce point est réel mais dépend de la finalisation du `bootstrap_contract` (ARB_D02) et du validator dédié (ARB_D01 cascade). Définir le format de rapport avant que les axes de validation soient stabilisés produirait un schéma prématuré à réécrire au prochain cycle. Report V0 assumé, sans risque immédiat tant qu'aucun run de validation d'application produite n'est effectué.
- **Condition de réactivation :** Après ARB_D01 et ARB_D02 résolus.

---

## Points rejetés

### ARB_X01 — Evidence insuffisante (2 entrées seulement)

- **Decision ID :** ARB_X01
- **Sujet :** `evidence` limitée à deux entrées dans `platform_factory_state.yaml`.
- **Source(s) :** Axe 6 faiblesse (PFCHAL_20260410_PERPLX_K7R2)
- **Décision :** `rejected`
- **Justification :** En V0, deux entrées d'evidence sont normales et honnêtes. Ce n'est pas un trou de gouvernance. Les enrichir sans nouveau run de pipeline serait artificiel. L'evidence sera naturellement enrichie dès le premier cycle formel.
- **Impact si non traité :** Aucun.

---

## Points hors périmètre

Aucun finding identifié dans le challenge PFCHAL_20260410_PERPLX_K7R2 ne relève du pipeline d'instanciation domaine ou d'un périmètre extérieur à la factory. Tous les findings sont correctement ciblés sur la factory générique.

---

## Points sans consensus ou nécessitant discussion finale

- **ARB_C01** (`version_fingerprint`) : nécessite une décision opérateur humain sur la responsabilité et le trigger de comparaison. Ni l'architecture seule ni le pipeline seul ne peuvent trancher sans ce choix de design.
- **ARB_D04** (`declared_autonomy_regime_respected`) : la décision ajouter/supprimer dépend d'une lecture de `constitution.yaml` pour vérifier l'existence d'un invariant couvrant cet item. À confirmer en STAGE_03.

---

## Corrections à arbitrer avant patch — récapitulatif

| ID | Sujet | Statut | Lieu principal | Priorité |
|---|---|---|---|---|
| ARB_D01 | Matérialiser `constitutional_conformance_matrix.yaml` | retained_now | validator/tooling | Critique |
| ARB_D02 | Borner `bootstrap_contract` TBD dans l'architecture | retained_now | architecture | Critique |
| ARB_D03 | Corriger wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | retained_now | state | Modéré |
| ARB_D04 | Relier `declared_autonomy_regime_respected` à un invariant constitutionnel | retained_now | architecture | Modéré |
| ARB_D05 | Aligner nommage `challenge_report` dans `pipeline.md` | retained_now | pipeline | Modéré |
| ARB_D06 | Tracer le cycle de déblocage `usage_as_sole_context` | retained_now | state | Élevé |
| ARB_C01 | Mécanisme de comparaison `version_fingerprint` | clarification_required | architecture | Élevé |
| ARB_R01 | Protocole assemblage multi-IA | deferred | architecture + pipeline | Élevé (reporté) |
| ARB_R02 | Format rapport validation application produite | deferred | architecture | Modéré (reporté) |
| ARB_X01 | Evidence insuffisante | rejected | — | Faible |

---

## Répartition par lieu de correction

### Architecture
- ARB_D02 : borner `bootstrap_contract`
- ARB_D04 : relier `declared_autonomy_regime_respected` à invariant constitutionnel
- ARB_C01 (clarification requise) : mécanisme fingerprint

### State
- ARB_D03 : corriger wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`
- ARB_D06 : tracer cycle de déblocage `usage_as_sole_context`
- ARB_R01 (deferred) : corriger wording multi-IA "bloqué jusqu'à résolution"

### Validator / tooling (nouveau fichier)
- ARB_D01 : créer `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`

### Pipeline
- ARB_D05 : aligner convention nommage `challenge_report` dans `pipeline.md`

### Architecture + pipeline (cycle ultérieur)
- ARB_R01 (deferred) : protocole assemblage multi-IA
- ARB_R02 (deferred) : format rapport validation

---

## Séquencement recommandé

1. **ARB_D01** — Matérialiser la `constitutional_conformance_matrix.yaml` (débloque ARB_D06 et le validator dédié)
2. **ARB_D02** — Borner `bootstrap_contract` dans l'architecture (clarifie le contrat minimal)
3. **ARB_D06** — Tracer le cycle de déblocage dans le state (dépend de ARB_D01 retenu)
4. **ARB_D03 + ARB_D05** — Corrections wording state et pipeline (indépendantes, groupables)
5. **ARB_D04** — Relier `declared_autonomy_regime_respected` (dépend d'une lecture constitution — confirmer en STAGE_03)
6. **ARB_C01** — Après décision humaine sur la responsabilité fingerprint

---

## Priorités de patch

| Priorité | IDs |
|---|---|
| Critique | ARB_D01, ARB_D02 |
| Élevé | ARB_D06, ARB_C01 (clarification requise), ARB_R01 (deferred) |
| Modéré | ARB_D03, ARB_D04, ARB_D05, ARB_R02 (deferred) |
| Faible | ARB_X01 (rejeté) |

---

*Fin du rapport d'arbitrage — `PFARB_20260410_PERPLX_M3T9`*
