# Proposition d'arbitrage — STAGE_02_FACTORY_ARBITRAGE

## Métadonnées

| Champ | Valeur |
|---|---|
| **Titre** | Proposition d'arbitrage — Platform Factory Baseline V0 |
| **arbitrage_run_id** | `PFARB_20260404_PERPLX_9M4T` |
| **Date** | 2026-04-04 |
| **Stage** | STAGE_02_FACTORY_ARBITRAGE |
| **Pipeline** | docs/pipelines/platform_factory/pipeline.md |
| **Prompt principal** | docs/prompts/shared/Make21PlatformFactoryArbitrage.md |
| **Agent** | PERPLX (Perplexity AI — Sonnet 4.6) |
| **Posture** | Proposition d'arbitrage indépendante — contribution à consolidation finale humaine-assistée |

---

## Challenge reports considérés

| challenge_run_id | Agent | Taille |
|---|---|---|
| `PFCHAL_20260404_GPT54_X7K2Q` | GPT54 | 31 440 oct. |
| `PFCHAL_20260404_PERPLX_7K2R` | PERPLX | 37 616 oct. |
| `PFCHAL_20260404_PERPLX_A1J77P` | PERPLX | 33 541 oct. |
| `PFCHAL_20260404_PERP_K7X2` | PERP | 22 155 oct. |
| `PFCHAL_20260404_PPLXAI_5LVBSV` | PPLXAI | 36 592 oct. |
| `PFCHAL_20260404_PXADV_BB1MZX` | PXADV | 35 528 oct. |

Tous les reports présents dans `work/01_challenge/` ont été lus. Aucun n'a été ignoré.

---

## Résumé exécutif

La baseline Platform Factory V0 est **architecturalement cohérente et constitutionnellement bien intentionnée**, mais elle **n'est pas encore suffisamment fermée pour industrialiser sans risque**. Les six challenge reports convergent massivement sur les mêmes zones critiques, avec un niveau de consensus remarquable.

**Trois risques critiques font consensus absolu (6/6 rapports) :**

1. **C-01 — Binding constitutionnel absent dans le contrat minimal d'application produite.** Une application produite peut passer la validation factory sans que ses invariants runtime (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`) soient prouvés.

2. **C-02 — Projections dérivées entièrement non opérationnalisées.** Emplacement TBD, validateur absent, protocole de régénération absent, invalidation post-patch absente. Le mécanisme central est déclaré mais non instrumenté.

3. **C-03 — Artefacts V0 en `current/` hors manifest officiel.** Zone grise de gouvernance release créant une ambiguïté sur le statut réel de la baseline.

**Trois risques élevés font consensus fort (5-6/6 rapports) :**

4. **E-01 — Sur-déclaration de maturité** dans `capabilities_present` pour `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` et `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`.

5. **E-02 — Protocole d'assemblage multi-IA absent.** `decomposition_protocol`, `module_granularity_convention`, `ai_output_assembly_protocol` tous absents.

6. **E-03 — Contrat minimal incomplet** sur fingerprints de reproductibilité et bootstrap_contract non définis.

**Verdict d'arbitrage global :** La baseline est **patchable et doit être patchée**. Elle n'est pas bloquante pour l'avancement du pipeline, mais les trois risques critiques doivent être traités avant tout usage en production de la factory pour instancier des applications.

---

## Synthèse des constats convergents

### Constats convergents (consensus 5-6/6 rapports)

| Constat | Rapports sources | Consensus |
|---|---|---|
| Contrat minimal ne prouve pas la conformité constitutionnelle runtime | GPT54, PERPLX_7K2R, PERPLX_A1J77P, PERP, PPLXAI, PXADV | **6/6 — consensus fort** |
| Projections dérivées sans emplacement, validateur, régénération | GPT54, PERPLX_7K2R, PERPLX_A1J77P, PERP, PPLXAI, PXADV | **6/6 — consensus fort** |
| Artefacts V0 hors manifest officiel | PERPLX_7K2R, PERPLX_A1J77P, PERP, PPLXAI, PXADV | **5/6 — consensus fort** |
| Sur-déclaration de maturité capabilities_present | PERPLX_7K2R, PERPLX_A1J77P, PERP, PPLXAI, PXADV | **5/6 — consensus fort** |
| Absence protocole assemblage multi-IA | GPT54, PERPLX_7K2R, PERP, PPLXAI, PXADV | **5/6 — consensus fort** |
| Séparation architecture/state correctement tenue | GPT54, PERPLX_7K2R, PERPLX_A1J77P, PERP, PPLXAI, PXADV | **6/6 — point solide** |
| Séparation Constitution/Référentiel bien respectée | GPT54, PERPLX_7K2R, PERPLX_A1J77P, PERP, PPLXAI, PXADV | **6/6 — point solide** |

### Constats partiellement divergents

| Constat | Divergence | Décision proposée |
|---|---|---|
| Gravité de l'absence d'atomicité STAGE_05 (rollback) | PXADV classe Élevé, GPT54 classe Fragile, PPLXAI ne l'isole pas explicitement | **→ Classé Élevé, lieu : pipeline** |
| Périmètre exact de la correction des fingerprints | PPLXAI / PXADV : architecture ; PERP : aussi pipeline | **→ Lieu principal : architecture** |
| Lien d'appartenance run des challenge reports | PPLXAI / PXADV signalent ; GPT54 ne signale pas | **→ Retenu, lieu : pipeline** |
| Ambiguïté STAGE_04 vs STAGE_06 (même prompt) | Soulevé par PPLXAI uniquement | **→ Retenu Modéré, lieu : pipeline, pour clarification** |

---

## Propositions d'arbitrage par thème

---

### THEME-01 — Binding constitutionnel dans le contrat minimal d'application produite

**Problème consolidé :** Le `produced_application_minimum_contract` dans `platform_factory_architecture.yaml` ne contient aucune obligation explicite et auditable de conformité aux invariants constitutionnels de runtime. Une application produite peut passer la validation factory sans prouver :
- absence d'appel réseau runtime (`INV_RUNTIME_FULLY_LOCAL`)
- absence de génération de contenu runtime (`INV_NO_RUNTIME_CONTENT_GENERATION`)
- absence de génération de feedback hors templates (`INV_NO_RUNTIME_FEEDBACK_GENERATION`)
- patchs pré-calculés hors session (`INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`)
- validation déterministe des patchs (`INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`)
- conformité Référentiel pour évaluation déléguée (`INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION`)

**Decision ID :** `ARB-01`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` |
| **Localisation** | architecture |
| **Statut proposé** | **retained_now** |
| **Gravité** | Critique |
| **Justification** | Consensus 6/6. Risque de conformité constitutionnelle invérifiable. Trou normatif dangereux même en V0 : ce n'est pas un manque de maturité tolérable, c'est une brèche structurelle dans la chaîne de garantie. |
| **Impact si non traité** | Une application produite peut paraître valide selon la factory tout en violant les invariants les plus critiques de la Constitution. Ce risque s'aggrave à chaque instanciation. |
| **Lieu principal de traitement** | `platform_factory_architecture.yaml` |
| **Lieux secondaires** | `platform_factory_state.yaml` (mettre à jour l'état du contrat minimal) ; validator/outillage futur |
| **Niveau de consensus** | **strong** |
| **Pré-condition** | Aucune — patchable sans clarification supplémentaire |
| **Note de séquencement** | Premier patch à produire — conditionne la valeur de tous les autres |

---

### THEME-02 — Opérationnalisation des `validated_derived_execution_projections`

**Problème consolidé :** L'invariant `PF_INV_DERIVED_PROJECTIONS_MUST_BE_STRICTLY_CONFORMANT` est déclaré, la règle d'usage est posée, mais aucun des éléments opérationnels n'existe : emplacement (`TBD`), validateur (`absent`), protocole de régénération (`absent`), invalidation post-patch canonique (`absent`). Une IA peut recevoir et utiliser une projection sans que son intégrité, sa date de validation ou sa version soit vérifiable.

**Decision ID :** `ARB-02`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `platform_factory_architecture.yaml` → `generated_projection_rules` ; `platform_factory_state.yaml` → `derived_projection_conformity_status` |
| **Localisation** | architecture + state |
| **Statut proposé** | **retained_now** pour la décision d'emplacement et le principe de validator ; **deferred** pour l'implémentation complète du validator |
| **Gravité** | Critique |
| **Justification** | Consensus 6/6. Le mécanisme central d'alimentation IA est déclaré mais entièrement non instrumenté. Tant que l'emplacement n'est pas décidé, aucun validator ne peut être créé. La décision d'emplacement est un pré-requis de patch minimal. |
| **Impact si non traité** | Dérive normative silencieuse active dès que des IA commencent à utiliser des projections en parallèle. |
| **Lieu principal de traitement** | `platform_factory_architecture.yaml` (décision d'emplacement + schéma de validator) |
| **Lieux secondaires** | `platform_factory_state.yaml` (mettre à jour `derived_projection_conformity_status`) ; pipeline (ajouter gate de validation avant usage IA) |
| **Niveau de consensus** | **strong** |
| **Pré-condition** | Décision humaine sur l'emplacement canonique des projections (dans `docs/` ou dans `cores/` ou artefact séparé) |
| **Note de séquencement** | Décision d'emplacement avant tout patch de validator |

---

### THEME-03 — Gouvernance release / manifest officiel

**Problème consolidé :** Les artefacts `platform_factory_architecture.yaml` et `platform_factory_state.yaml` sont dans `docs/cores/current/` mais hors du manifest officiel courant. Ils ont été posés directement sans passer par un STAGE_08 de promotion. Le pipeline STAGE_07 et STAGE_08 ne savent pas comment traiter cette régularisation initiale.

**Decision ID :** `ARB-03`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `metadata.notes` des deux artefacts ; manifest officiel |
| **Localisation** | manifest/release governance |
| **Statut proposé** | **retained_now** pour une décision de régularisation explicite dans le pipeline |
| **Gravité** | Critique |
| **Justification** | Consensus 5/6. Zone grise de gouvernance qui crée une ambiguïté sur le statut réel de la baseline. Risque pour tous les stages qui dépendent d'un état canonique traçable. |
| **Impact si non traité** | Traçabilité incomplète. Un run ultérieur ne peut pas déterminer de façon fiable quelle version des artefacts est "officiellement" gouvernée. |
| **Lieu principal de traitement** | Pipeline (STAGE_08 ou procédure de régularisation initiale dédiée) |
| **Lieux secondaires** | `platform_factory_state.yaml` (traçabilité explicite de la situation de régularisation) |
| **Niveau de consensus** | **strong** |
| **Pré-condition** | Décision humaine : régularisation immédiate par un STAGE_08 simulé, ou acceptation explicite du statut "pre-governance baseline" dans l'état |

---

### THEME-04 — Sur-déclaration de maturité dans `capabilities_present`

**Problème consolidé :** Deux capacités sont classées en `capabilities_present` alors qu'elles ne sont que des intentions posées sans outillage :
- `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` : règle définie sans validator, sans emplacement, sans schéma
- `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` : intention posée, pipeline non exécuté

Certains rapports signalent aussi `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` comme partiellement contestable (6 open_points restants).

**Decision ID :** `ARB-04`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `platform_factory_state.yaml` → `capabilities_present` |
| **Statut proposé** | **retained_now** |
| **Gravité** | Élevé |
| **Justification** | Consensus 5/6. Un faux sentiment de fermeture dans l'état nuit à la fiabilité du constat. L'état doit refléter la réalité, pas l'intention. |
| **Impact si non traité** | Un opérateur ou une IA lisant `capabilities_present` croit à une capacité opérationnelle inexistante. Risque d'exploitation d'une capacité non instrumentée. |
| **Lieu principal de traitement** | `platform_factory_state.yaml` |
| **Lieux secondaires** | Aucun |
| **Niveau de consensus** | **strong** |
| **Pré-condition** | Aucune — patch direct sur le state |

---

### THEME-05 — Protocole d'assemblage multi-IA

**Problème consolidé :** Les trois éléments nécessaires à l'assemblage multi-IA sont absents : `decomposition_protocol`, `module_granularity_convention`, `ai_output_assembly_protocol`. Leur absence est reconnue dans l'état comme `requirement_defined_not_yet_operationalized`, mais sans critère de déclenchement ni date.

**Decision ID :** `ARB-05`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `platform_factory_architecture.yaml` → `multi_ia_parallel_readiness` ; `platform_factory_state.yaml` → `multi_ia_parallel_readiness_status` |
| **Statut proposé** | **deferred** — mais avec wording de l'état corrigé pour éviter une promesse implicite |
| **Gravité** | Élevé |
| **Justification** | Consensus 5/6. L'absence de protocole est une limite V0 acceptable si elle est clairement wording-ée dans l'état. Elle ne bloque pas le pipeline actuel, mais elle doit être explicitement signalée comme bloquante pour tout usage multi-IA en production. |
| **Impact si non traité** | Collisions silencieuses entre outputs IA parallèles. Assemblage non déterministe. |
| **Lieu principal de traitement** | `platform_factory_state.yaml` (wording corrigé) |
| **Lieux secondaires** | `platform_factory_architecture.yaml` (ajout de la contrainte explicite "multi-IA non opérationnel en V0") |
| **Niveau de consensus** | **strong** |
| **Pré-condition** | Aucune pour le wording patch. Décision de scope pour l'implémentation. |

---

### THEME-06 — Complétude du contrat minimal (fingerprints, bootstrap_contract)

**Problème consolidé :** Le contrat minimal d'application produite déclare des champs obligatoires (`reproducibility_fingerprints`, `bootstrap_contract`) mais sans définition de contenu. Un manifest peut les satisfaire par simple présence d'une clé vide.

**Decision ID :** `ARB-06`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.produced_instance_identity.reproducibility_fingerprints` et `runtime_entrypoint_contract.bootstrap_contract` |
| **Statut proposé** | **retained_now** (définition minimale des champs obligatoires requise pour que le contrat soit vérifiable) |
| **Gravité** | Élevé |
| **Justification** | Consensus 4-5/6. Un champ déclaré obligatoire sans définition de contenu n'est pas un contrat — c'est une apparence de contrat. |
| **Impact si non traité** | La validation factory devient formelle sans substance. Tout manifest passe. |
| **Lieu principal de traitement** | `platform_factory_architecture.yaml` |
| **Lieux secondaires** | `platform_factory_state.yaml` |
| **Niveau de consensus** | **medium** |
| **Pré-condition** | Aucune pour une définition minimale. La définition complète peut être déférée à V0.2. |

---

### THEME-07 — Atomicité et rollback en STAGE_05 (patch)

**Problème consolidé :** Le pipeline STAGE_05 (patch) ne documente pas de protocole d'atomicité ni de rollback. En l'état, un patch partiel peut être appliqué, violant `INV_NO_PARTIAL_PATCH_STATE`.

**Decision ID :** `ARB-07`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `pipeline.md` → STAGE_05 |
| **Statut proposé** | **retained_now** |
| **Gravité** | Élevé |
| **Justification** | Soulevé par PXADV (Élevé), cohérent avec GPT54 (Fragile). Risque de violation d'un invariant fort (`INV_NO_PARTIAL_PATCH_STATE`) dans la procédure même de gouvernance. |
| **Impact si non traité** | Un patch avorté peut laisser la baseline dans un état partiellement modifié non traçable. |
| **Lieu principal de traitement** | Pipeline |
| **Lieux secondaires** | `platform_factory_state.yaml` (traçabilité des patches appliqués) |
| **Niveau de consensus** | **medium** |
| **Pré-condition** | Aucune pour un wording pipeline. Implémentation outillage déférable. |

---

### THEME-08 — Lien d'appartenance run dans les challenge reports

**Problème consolidé :** Les challenge reports dans `work/01_challenge/` ne sont pas liés à un run_id de pipeline identifié. Un report d'un run antérieur peut être consommé par un STAGE_02 ultérieur sans que l'opérateur le détecte.

**Decision ID :** `ARB-08`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `pipeline.md` → STAGE_01 (format des challenge reports) + STAGE_02 (règle de consommation) |
| **Statut proposé** | **retained_now** pour la règle de pipeline ; **deferred** pour un outillage de filtrage automatique |
| **Gravité** | Modéré |
| **Justification** | Soulevé par PPLXAI et PXADV. Dans un contexte multi-IA, le risque d'arbitrer des findings obsolètes est réel et croît avec le nombre de runs. |
| **Impact si non traité** | Arbitrage pollué. Findings d'un run antérieur traités comme findings courants. |
| **Lieu principal de traitement** | Pipeline |
| **Niveau de consensus** | **medium** |

---

### THEME-09 — Ambiguïté STAGE_04 vs STAGE_06

**Problème consolidé :** Les stages STAGE_04 (validation du patchset) et STAGE_06 (validation des artefacts patchés) utilisent le même prompt `Make23PlatformFactoryValidation.md`. La différence d'objet entre les deux validations n'est pas explicitement documentée.

**Decision ID :** `ARB-09`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `pipeline.md` → STAGE_04 et STAGE_06 |
| **Statut proposé** | **clarification_required** avant patch |
| **Gravité** | Modéré |
| **Justification** | Soulevé uniquement par PPLXAI. Risque réel mais à confirmer : si le même prompt est intentionnel avec des contextes différents, pas de patch nécessaire ; sinon, deux prompts distincts doivent être créés. |
| **Impact si non traité** | Ambiguïté dans l'exécution des stages de validation. |
| **Lieu principal de traitement** | Pipeline |
| **Niveau de consensus** | **weak** — un seul rapport |
| **Pré-condition** | Confirmation humaine : usage intentionnel du même prompt ou non |

---

### THEME-10 — Evidence `PF_EVIDENCE_PLAN_V2` lien potentiellement mort

**Problème consolidé :** L'évidence `PF_EVIDENCE_PLAN_V2` dans `platform_factory_state.yaml` pointe vers un fichier hors `current/`, risquant un lien mort si la structure évolue.

**Decision ID :** `ARB-10`
| Champ | Valeur |
|---|---|
| **Élément concerné** | `platform_factory_state.yaml` → `validated_decisions` → `PF_EVIDENCE_PLAN_V2` |
| **Statut proposé** | **retained_now** (vérification du lien avant patch) |
| **Gravité** | Modéré |
| **Justification** | Soulevé par PPLXAI. Petit risque de traçabilité. Vérifiable et corrigeable sans décision architecturale. |
| **Lieu principal de traitement** | `platform_factory_state.yaml` |
| **Niveau de consensus** | **weak** — un seul rapport |

---

## Points retenus (retained_now)

| Decision ID | Sujet | Lieu principal | Gravité | Consensus |
|---|---|---|---|---|
| ARB-01 | Binding constitutionnel manquant dans contrat minimal | architecture | Critique | strong |
| ARB-02 (partiel) | Décision emplacement projections + principe validator | architecture | Critique | strong |
| ARB-03 | Régularisation manifest officiel | pipeline/release governance | Critique | strong |
| ARB-04 | Sur-déclaration maturité capabilities_present | state | Élevé | strong |
| ARB-06 | Définition minimale fingerprints et bootstrap_contract | architecture | Élevé | medium |
| ARB-07 | Atomicité et rollback STAGE_05 | pipeline | Élevé | medium |
| ARB-08 (partiel) | Règle de consommation des challenge reports par run | pipeline | Modéré | medium |
| ARB-10 | Vérification lien `PF_EVIDENCE_PLAN_V2` | state | Modéré | weak |

---

## Points différés (deferred)

| Decision ID | Sujet | Justification de report | Condition de déclenchement |
|---|---|---|---|
| ARB-02 (partiel) | Implémentation complète du validator de projections | Décision d'emplacement requise avant tout validator | Après décision humaine sur l'emplacement |
| ARB-05 | Implémentation protocole assemblage multi-IA | Limite V0 acceptable — wording corrigé en attendant | Avant tout usage multi-IA en production |
| ARB-08 (partiel) | Outillage de filtrage automatique des challenge reports par run | Dépend d'un mécanisme run_id qui n'existe pas encore | Après introduction d'un run_id pipeline |

---

## Points rejetés (rejected)

Aucun finding des 6 rapports n'est rejeté. Tous les findings majeurs sont soit retenus, soit différés explicitement, soit classés en clarification requise.

---

## Points hors périmètre (out_of_scope)

| Sujet | Justification |
|---|---|
| `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` | Invariant du domaine — hors périmètre factory générique (consensus 6/6) |
| Format canonique des prompts STAGE_01 (output IA) | Relève de la gouvernance des prompts, pas de la factory |
| Gestion des prompts manquants dans le repo `prompts/` | Hors périmètre factory (signalé par PERP_K7X2 SA-05) |

---

## Clarifications requises avant patch

| Decision ID | Question | Porteur attendu |
|---|---|---|
| ARB-02 | Quel est l'emplacement canonique des `validated_derived_execution_projections` ? (`docs/`, `cores/`, artefact séparé ?) | Décision humaine |
| ARB-03 | La régularisation du statut manifest se fait-elle via un STAGE_08 simulé ou via une décision explicite de "pre-governance baseline" ? | Décision humaine |
| ARB-09 | L'usage du même prompt pour STAGE_04 et STAGE_06 est-il intentionnel ou un oubli de création d'un second prompt ? | Décision humaine |

---

## Corrections à arbitrer avant patch

Par ordre de priorité :

1. **ARB-01** — Ajouter dans `minimum_validation_contract.minimum_axes` les invariants constitutionnels runtime (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`) — _lieu : architecture_
2. **ARB-02** — Résoudre l'emplacement TBD des projections dérivées et ajouter les pré-conditions de validator dans l'architecture — _lieu : architecture + clarification humaine_
3. **ARB-03** — Créer dans le pipeline une procédure de régularisation initiale ou documenter explicitement le statut "pre-governance baseline" dans les deux artefacts — _lieu : pipeline + clarification humaine_
4. **ARB-04** — Déplacer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` et `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` de `capabilities_present` vers `capabilities_partial` ou `capabilities_absent` avec wording exact — _lieu : state_
5. **ARB-05** — Corriger le wording de `multi_ia_parallel_readiness_status` dans le state pour déclarer explicitement que le multi-IA en parallèle est **bloquant** sans protocole — _lieu : state_
6. **ARB-06** — Définir le contenu minimal attendu de `reproducibility_fingerprints` et `bootstrap_contract` pour que ces champs soient vérifiables — _lieu : architecture_
7. **ARB-07** — Ajouter dans STAGE_05 du pipeline une règle explicite d'atomicité et de procédure rollback — _lieu : pipeline_
8. **ARB-08** — Ajouter dans STAGE_01 un champ `pipeline_run_id` requis dans les challenge reports et dans STAGE_02 une règle de consommation par run courant — _lieu : pipeline_
9. **ARB-10** — Vérifier et corriger le chemin de `PF_EVIDENCE_PLAN_V2` — _lieu : state_

---

## Points sans consensus ou nécessitant discussion finale

| Sujet | Nature de l'ambiguïté | Rapports en désaccord |
|---|---|---|
| Gravité de l'absence de rollback STAGE_05 | PXADV : Élevé ; autres : Fragile ou non isolé | GPT54 vs PXADV — → proposé Élevé |
| Périmètre exact de la correction du bootstrap_contract | Certains incluent le runtime local dans le bootstrap ; d'autres l'isolent dans le contrat minimal | → clarifier lors du patch ARB-01 |
| ARB-09 : prompt dupliqué STAGE_04/STAGE_06 | Un seul rapport l'isole ; peut être intentionnel | → clarification humaine requise |
| Seuil de déclenchement pour le multi-IA opérationnel | Aucun rapport ne propose de critère précis | → à définir lors de l'arbitrage final |

---

## Répartition par lieu de correction

### `platform_factory_architecture.yaml` (principal)
- ARB-01 : binding constitutionnel contrat minimal
- ARB-02 : décision emplacement projections + principe validator
- ARB-06 : définition fingerprints et bootstrap_contract

### `platform_factory_state.yaml` (principal)
- ARB-04 : correction maturité capabilities_present
- ARB-05 : wording multi-IA bloquant
- ARB-10 : vérification lien evidence

### `platform_factory_architecture.yaml` + `platform_factory_state.yaml` (les deux)
- ARB-02 (implémentation) : décision et constat mis à jour en cohérence
- ARB-06 : architecture d'abord, state ensuite

### Pipeline (principal)
- ARB-03 : procédure de régularisation manifest
- ARB-07 : atomicité et rollback STAGE_05
- ARB-08 : lien run_id challenge reports

### Release governance / manifest (principal)
- ARB-03 (second lieu) : intégration manifest officiel

---

## Séquencement recommandé

```
Étape 1 : Clarifications humaines (ARB-02, ARB-03, ARB-09)
     ↓
Étape 2 : Patch architecture — ARB-01 (critique, sans dépendance)
     ↓
Étape 3 : Patch architecture — ARB-02 (emplacement projections, post-clarification)
     ↓
Étape 4 : Patch architecture — ARB-06 (fingerprints, bootstrap_contract)
     ↓
Étape 5 : Patch state — ARB-04 (maturité), ARB-05 (wording multi-IA), ARB-10 (lien evidence)
     ↓
Étape 6 : Patch pipeline — ARB-07 (atomicité), ARB-08 (run_id), ARB-03 (régularisation)
     ↓
Étape 7 : Validation et release
```

---

## Priorités de patch

| Priorité | Decision IDs | Sujets |
|---|---|---|
| **Critique** | ARB-01, ARB-02, ARB-03 | Binding constitutionnel, projections dérivées, manifest |
| **Élevé** | ARB-04, ARB-05, ARB-06, ARB-07 | Maturité state, multi-IA, fingerprints, atomicité |
| **Modéré** | ARB-08, ARB-10 | Run linkage, evidence link |
| **Clarification** | ARB-09 | Ambiguïté STAGE_04/06 |

---

## Résultat terminal

**arbitrage_run_id :** `PFARB_20260404_PERPLX_9M4T`

**Fichier écrit :** `docs/pipelines/platform_factory/work/02_arbitrage/arbitrage_proposal_PFARB_20260404_PERPLX_9M4T.md`

**Résumé ultra-court :** Baseline V0 patchable. 3 risques critiques (binding constitutionnel contrat minimal, projections dérivées non opérationnalisées, artefacts hors manifest officiel). 4 risques élevés. 10 decisions d'arbitrage produites (ARB-01 à ARB-10). 3 clarifications humaines requises avant patch complet. Consensus 6/6 sur les trois points critiques.
