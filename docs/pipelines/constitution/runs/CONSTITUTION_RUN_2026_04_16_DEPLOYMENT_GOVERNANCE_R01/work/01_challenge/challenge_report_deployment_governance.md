# STAGE_01_CHALLENGE — Challenge du scope `deployment_governance`

**Run :** `CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01`
**Mode :** `bounded_local_run`
**Status :** `active`
**Next executable stage :** `STAGE_01_CHALLENGE`

---

## Executive Summary

Le scope `deployment_governance` regroupe les invariants, règles, contraintes et événements qui encadrent le déploiement du moteur Learn-it (modes d'autonomie, architecture runtime locale, gouvernance de la gamification, séparation Constitution/Référentiel, transparence apprenant).

L'analyse ids-first de 19 IDs constitutionnels, complétée par un fallback ciblé sur le Core Référentiel v3.0 pour un voisin manquant, ne révèle pas de contradiction logique interne entre invariants non patchables et règles dérivées.

**Quatre risques prioritaires émergent :**
1. Dépendance forte au paramétrage référentiel pour borner la durée de probation gamification
2. Définition incomplète au niveau constitutionnel de l'infrastructure tutorale requise pour le mode Assisté
3. Frontière à clarifier entre signaux explicitement autorisés par `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` et l'usage de proxys comportementaux dans le Référentiel
4. Ambiguïté de naming entre `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` et le Core effectif `CORE_LEARNIT_REFERENTIEL_v3.0`

---

## Challenge Scope

### Surface de lecture

En mode `bounded_local_run`, le contrat impose une lecture ids-first de :
- `run_context.yaml` (vue runtime, statut, stage, ids_first_ready, integration_gate)
- `scope_extract.yaml` (19 IDs cibles du scope, avec entrées dérivées de la Constitution)
- `neighbor_extract.yaml` (IDs voisins référentiels ciblés par l'impact_bundle)
- `scope_manifest.yaml`, `impact_bundle.yaml`, `integration_gate.yaml` comme contexte de périmètre, devoir de lecture et garde-fous d'intégration

`scope_extract` couvre les 19 IDs déclarés dans `scope_manifest.writable_perimeter.ids`, avec `missing_ids: []` — la vue constitutionnelle du scope est complète. Le `neighbor_extract` cible `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` mais le signale comme `missing_ids` (aucune entrée dérivée), déclenchant la règle de fallback.

### Fallback déclaré

**ID manquant :** `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`
**Action :** Lecture ciblée de `docs/cores/current/referentiel.yaml` (`CORE_LEARNIT_REFERENTIEL_v3.0`) uniquement pour cet ID.
**Résultat :** Core v3.0 fédéré à la Constitution via `REF_CORE_LEARNIT_CONSTITUTION_V3_0_IN_REFERENTIEL` ; invariants référentiels verrouillant la logique AND, la propagation graphe 1-saut et certains garde-fous patch confirmés conformes.

Tous les autres IDs référentiels sont traités comme `out_of_scope_but_relevant` : leur contenu n'est utilisé que pour vérifier que les contraintes constitutionnelles ne sont pas contournées par le paramétrage référentiel.

---

## Detailed Analysis by Axis

### Axis: internal_coherence

Les invariants non patchables du scope sont présents avec des logiques alignées sur leurs scopes déclarés :

| ID | Scope déclaré | Statut |
|---|---|---|
| `INV_RUNTIME_FULLY_LOCAL` | runtime_architecture | ✅ cohérent |
| `INV_NO_RUNTIME_CONTENT_GENERATION` | governance | ✅ cohérent |
| `INV_CONSTITUTION_REFERENTIAL_SEPARATION` | governance | ✅ cohérent |
| `INV_ASSISTED_MODE_REQUIRES_TUTORING` | deployment | ✅ cohérent |
| `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` | runtime_transparency | ✅ cohérent |

Les règles associées à GF-08 (`EVENT_GF08_UNCOVERED_CONFLICT` → `RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE`) forment une boucle cohérente : détection d'un conflit inter-principes non couvert, réponse conservatrice, log pour futur patch. Le graphe de dépendances reste orienté et acyclique.

### Axis: theoretical_soundness

`RULE_NO_CALIBRATION_CONSERVATIVE_START` impose un démarrage conservateur en absence de calibrage, cohérent avec la philosophie de prudence en cas de manque de données. Le Référentiel complète cette règle par des tables de calibrage détaillées sans modifier la logique constitutionnelle.

Les invariants référentiels `INV_REFERENTIEL_CONSTITUTIONAL_AND_LOGIC_NOT_MODIFIABLE_HERE` et `INV_REFERENTIEL_GRAPH_ONE_HOP_NOT_MODIFIABLE_HERE` verrouillent les mêmes invariants que `CONSTRAINT_NO_CHANGE_TO_AND_LOGIC` et `CONSTRAINT_NO_CHANGE_TO_GRAPH_PROPAGATION_RULE` côté Constitution. Le Référentiel ne peut ajuster que des seuils et des paramètres, pas la logique d'agrégation ni la profondeur de propagation.

### Axis: undefined_engine_states

`TYPE_AUTONOMY_REGIME` définit quatre régimes d'autonomie (autonome, hybride recommandé, hybride bloquant, assisté), mais ne précise pas constitutionnellement les conditions de sélection d'un régime pour un déploiement donné. Sans lien explicite vers des paramètres référentiels (matrice d'états cibles, profil de risque), l'état moteur « régime actif » peut rester partiellement indéterminé.

`TYPE_HUMAN_CHECKPOINT`, paramétrable, déclare un jalon humain « bloquant ou non selon le niveau d'autonomie » sans fixer constitutionnellement les seuils ou critères de blocage. En l'absence de paramétrage explicite, un déploiement pourrait rester en état ambigu (checkpoint présent mais sans statut opérationnel déterminable).

### Axis: implicit_ai_dependencies

`INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` interdit de qualifier des signaux de gouvernance via inférence locale IA — seuls les artefacts hors session ou les indicateurs explicites déterministes sont autorisés.

Le Référentiel introduit un socle de proxys comportementaux (`TYPE_REFERENTIEL_MINIMAL_BEHAVIORAL_PROXY_SET`, `PARAM_REFERENTIEL_PROXY_MIN_WEIGHT`) pour pallier l'absence d'AR-N1, avec contrainte de mesurabilité et de documentation. **Tension détectée :** si des proxys comportementaux trop riches sont interprétés comme substitut implicite d'un jugement IA hors session plutôt que comme simple signal empirique borné, la frontière constitutionnelle serait franchie. Ce risque est partiellement contrôlé par des invariants référentiels (VC inconnue = pas d'inférence, désactivation de l'axe VC non observable), mais ces garde-fous restent purement référentiels.

### Axis: governance

`INV_CONSTITUTION_REFERENTIAL_SEPARATION` fixe une séparation inviolable : Constitution = quoi/pourquoi, Référentiel = combien/comment. Pour `deployment_governance`, la gouvernance de la gamification est répartie :
- **Constitution :** `RULE_UNVERIFIED_GAMIFICATION_PROBATION`, `RULE_GAMIFICATION_PROBATION_MUST_CLOSE`, `EVENT_GAMIFICATION_PROBATION_MAX_DURATION_REACHED`, `ACTION_INFORM_LEARNER`
- **Référentiel :** `PARAM_REFERENTIEL_GAMIFICATION_PROBATION_MAX_SESSIONS`

Le mécanisme de probation est constitutionnellement défini, mais la durée maximale est entièrement paramétrée référentiellement, sans borne constitutionnelle explicite.

### Axis: adversarial_scenarios

**Scénario 1 — Probation gamification :** Un opérateur pourrait augmenter `PARAM_REFERENTIEL_GAMIFICATION_PROBATION_MAX_SESSIONS` à une valeur très élevée. La Constitution garantit une clôture « un jour », mais l'horizon temporel effectif serait délégué au paramétrage référentiel sans garde-fou constitutionnel borné.

**Scénario 2 — Mode Assisté sans tutorat réel :** Les invariants `INV_ASSISTED_MODE_REQUIRES_TUTORING` et `CONSTRAINT_NO_ASSISTED_DEPLOYMENT_WITHOUT_TUTORING` interdisent le déploiement sans tutorat, mais ne définissent ni le type ni le niveau minimal de cette infrastructure, laissant un espace d'interprétation potentiellement exploitable.

### Axis: risk_prioritization

| ID | Description synthétique | Gravité | Scope_status |
|---|---|---|---|
| R1 | Probation gamification bornée uniquement par un paramètre référentiel de durée | Élevée | `in_scope` |
| R2 | Infrastructure tutorale non définie constitutionnellement pour le mode Assisté | Élevée | `in_scope` |
| R3 | Frontière proxys comportementaux / signaux explicites à clarifier | Moyenne | `in_scope` |
| R4 | Ambiguïté d'identifiant Référentiel V2.0 vs V3.0 | Moyenne | `needs_scope_extension` |

---

## Priority Risks

### R1 — Probation gamification dépendante du Référentiel

- **Manifestation :** `RULE_GAMIFICATION_PROBATION_MUST_CLOSE` dépend de `EVENT_GAMIFICATION_PROBATION_MAX_DURATION_REACHED` → `PARAM_REFERENTIEL_GAMIFICATION_PROBATION_MAX_SESSIONS`
- **Risque :** Durée de probation potentiellement très longue sans borne constitutionnelle explicite
- **Portée :** Logique constitutionnelle préservée, paramétrage non borné

### R2 — Infrastructure tutorale non définie constitutionnellement

- **Manifestation :** `INV_ASSISTED_MODE_REQUIRES_TUTORING` et `CONSTRAINT_NO_ASSISTED_DEPLOYMENT_WITHOUT_TUTORING` interdisent le déploiement sans tutorat mais ne définissent pas les exigences minimales
- **Risque :** Mode Assisté activé avec une infrastructure tutorale minimale ou mal qualifiée
- **Portée :** Absence de référence vers un type référentiel décrivant les propriétés minimales

### R3 — Frontière proxys comportementaux / signaux explicites

- **Manifestation :** `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` vs `TYPE_REFERENTIEL_MINIMAL_BEHAVIORAL_PROXY_SET`
- **Risque :** Glissement progressif vers une inférence implicite non conforme à l'invariant constitutionnel
- **Portée :** Garde-fous référentiels existants mais non constitutionnels

### R4 — Ambiguïté d'identifiant Référentiel V2.0 vs V3.0

- **Manifestation :** `neighbor_extract` cible `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`, Core effectif est `CORE_LEARNIT_REFERENTIEL_v3.0`
- **Risque :** Confusion d'ancres lors de patchs futurs ciblant des IDs inter-Core
- **Portée :** `needs_scope_extension` — concerne les inputs de run, pas uniquement la Constitution

---

## Corrections to Arbitrate Before Patch

> Ce stage ne génère aucun patch YAML. Les quatre points suivants sont soumis à arbitrage pour STAGE_02_ARBITRAGE.

**Arbitrage 1 (R1) — Encadrement constitutionnel de la durée de probation gamification**
Décider si la Constitution doit introduire un invariant ou une règle bornant explicitement l'intervalle acceptable pour `PARAM_REFERENTIEL_GAMIFICATION_PROBATION_MAX_SESSIONS`, ou si le pilotage purement référentiel est jugé suffisant.

**Arbitrage 2 (R2) — Typage de l'infrastructure tutorale requise**
Décider si `INV_ASSISTED_MODE_REQUIRES_TUTORING` et `CONSTRAINT_NO_ASSISTED_DEPLOYMENT_WITHOUT_TUTORING` doivent être complétés par une référence explicite vers un type référentiel décrivant les propriétés minimales de l'infrastructure tutorale (indépendance, disponibilité, traçabilité).

**Arbitrage 3 (R3) — Clarification de la frontière proxys / signaux explicites**
Décider si la Constitution doit pointer explicitement vers les blocs référentiels encadrant l'usage des proxys, afin de renforcer la lisibilité de `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION`.

**Arbitrage 4 (R4) — Remise en cohérence des identifiants Référentiel**
Décider si `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` doit être migré ou dupliqué pour pointer clairement vers le Core v3.0 actuel, ou si un mécanisme de compatibilité ascendante explicite est requis.

---

## Read Surface & Completion Evidence

| Critère | Statut |
|---|---|
| `challenge_report_written` | ✅ ce document |
| `read_surface_declared` | ✅ run_context, scope_extract, neighbor_extract, scope_manifest, impact_bundle, integration_gate, referentiel.yaml (fallback) |
| `fallback_ids_declared_if_any` | ✅ `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` → `CORE_LEARNIT_REFERENTIEL_v3.0` |
| `scope_status_declared_for_major_findings` | ✅ R1/R2/R3 = `in_scope`, R4 = `needs_scope_extension` |

---

*Généré le 2026-04-16 — STAGE_01_CHALLENGE — bounded_local_run*
