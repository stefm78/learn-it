# Challenge Report — STAGE_01_CHALLENGE
# Run : CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01
# Scope : patch_lifecycle
# Date : 2026-04-13
# Produit par : AI (bounded_local_run, ids-first)

---

## Résumé exécutif

**Mode utilisé :** `bounded` (`bounded_local_run`)

**Lecture ids-first :** Confirmée. La surface de lecture primaire a été couverte via :
- `runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/inputs/scope_extract.yaml` — 21 IDs du périmètre écrivable, tous trouvés (`missing_ids: []`)
- `runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/inputs/neighbor_extract.yaml` — 1 ID voisin (`REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`), trouvé

Aucun fallback sur les Core canoniques complets n'a été nécessaire.

**Synthèse :** Le scope `patch_lifecycle` couvre un mécanisme de correction paramétrique borné et bien délimité. La structure est globalement solide. Les risques principaux portent sur (1) la frontière déterminisme/sémantique dans la validation locale, (2) l'opérationnalisation des seuils de déclenchement absents dans le scope, et (3) le risque d'état ambigu entre `EVENT_PERSISTENT_LOW_VC` et les mécanismes d'escalade. Aucun élément in-scope ne présente de contradiction bloquante, mais plusieurs dépendances paramétriques critiques sont déportées hors scope vers le Référentiel sans garde-fou explicite dans ce sous-ensemble.

---

## Périmètre de challenge

### Artefacts lus
| Fichier | Type |
|---|---|
| `inputs/scope_extract.yaml` | Extrait scope (21 IDs, Constitution) |
| `inputs/neighbor_extract.yaml` | Extrait voisin (1 ID, Constitution) |
| `inputs/scope_manifest.yaml` | Périmètre modifiable |
| `inputs/impact_bundle.yaml` | Devoir de lecture étendu |
| `inputs/integration_gate.yaml` | Gate de promotion |

### IDs manquants ayant nécessité un fallback
Aucun. `missing_ids: []` dans les deux extraits.

### Scope déclaré
- `scope_key: patch_lifecycle`
- `scope_id: CONSTITUTION_SCOPE_PATCH_LIFECYCLE`
- Modules : `patch_layer`, `patch_validation`, `patch_architecture`, `patch_governance`
- 21 IDs in-scope écrivables (voir `scope_manifest.yaml`)
- 1 voisin obligatoire en lecture : `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`

### Limites de l'analyse
- Les Core canoniques complets (`constitution.yaml`, `referentiel.yaml`, `link.yaml`) n'ont pas été chargés.
- Toute faiblesse identifiée portant sur des IDs extérieurs au scope est signalée `out_of_scope_but_relevant` ou `needs_scope_extension`.
- Les seuils paramétriques référencés par `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH` et `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH` sont déclarés dans le Référentiel et non lisibles dans ce scope.

---

## Analyse détaillée par axe

---

### Axe 1 — Cohérence interne

**1.1 — Dépendance vers des types hors-scope non patchables**

`RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH` et `EVENT_PERSISTENT_LOW_VC` dépendent de `TYPE_STATE_AXIS_VALUE_COST`, absent du `scope_extract` et non présent dans le `neighbor_extract`. Ce type est vraisemblablement dans un scope `learner_state` ou équivalent.

- Risque : si `TYPE_STATE_AXIS_VALUE_COST` évolue (redéfinition des axes VC), les règles de ce scope peuvent devenir incohérentes sans qu'aucune garde ne soit activée dans le scope `patch_lifecycle`.
- Statut : `out_of_scope_but_relevant`
- Type de problème : cohérence inter-scope

**1.2 — Dépendance vers `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION` non présents dans l'extrait**

`INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` déclare `depends_on: [INV_RUNTIME_FULLY_LOCAL, INV_NO_RUNTIME_CONTENT_GENERATION]`. Ces deux invariants ne sont pas dans le périmètre écrivable ni dans le voisin obligatoire.

- Risque : si ces invariants fondateurs sont amendés dans un autre scope, la précondition de `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` perd son ancrage, sans visibilité depuis ce run.
- Statut : `out_of_scope_but_relevant`
- Type de problème : complétude / dépendance implicite

**1.3 — `TYPE_SELF_REPORT_AR_N1` absent de l'extrait**

`RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH` et `EVENT_AR_REFRACTORY_PROFILE_DETECTED` dépendent de `TYPE_SELF_REPORT_AR_N1`, non présent dans le scope ni dans les voisins déclarés. L'`impact_bundle` mentionne `neighbor_scopes: []`, donc aucun scope voisin n'a été inclus dans le devoir de lecture.

- Risque : le déclencheur AR-réfractaire est opérationnel en lecture (via le Référentiel), mais non challengeable dans ce run sans fallback. Si `TYPE_SELF_REPORT_AR_N1` est fragile ou mal défini dans son scope d'origine, cela fragilise ces deux mécanismes.
- Statut : `out_of_scope_but_relevant`
- Type de problème : complétude

**1.4 — Paramétrable vs non patchable : tension non résolue**

Plusieurs entrées sont `patchable: false` ET `parameterizable: true` (ex : `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`, `EVENT_PERSISTENT_LOW_VC`). Cette combinaison signifie que le comportement peut évoluer via un paramètre Référentiel, mais la règle elle-même ne peut pas être patchée. La frontière entre "changer un paramètre" et "changer la règle" n'est pas formellement définie dans ce scope.

- Risque : ambiguïté d'interprétation lors d'un arbitrage sur le seuil de VC — est-ce un patch ou un paramètre Référentiel ?
- Statut : `in_scope`
- Type de problème : gouvernance

---

### Axe 2 — Solidité théorique

**Charge cognitive**
- Point solide : `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` protège contre l'injection de décisions sémantiques complexes en session.
- Zone de risque : les déclencheurs de patch (`EVENT_PERSISTENT_LOW_VC`, `EVENT_AR_REFRACTORY_PROFILE_DETECTED`) supposent une accumulation de signal cross-session. Si la fenêtre d'observation n'est pas robuste, le déclenchement peut être trop précoce ou trop tardif.
- Angle mort : aucun mécanisme explicite dans ce scope ne protège contre la sur-sollicitation de patch (patch-fatigue si plusieurs seuils sont atteints simultanément).

**Motivation / VC**
- Point solide : `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH` cible correctement la relevance (contextualisation/enjeux) plutôt que la difficulté — cohérent avec les principes de motivation intrinsèque.
- Zone de risque : le patch de relevance n'adresse que la valeur perçue, pas l'expectancy (espérance de succès). Un apprenant avec VC basse persistante pour une raison d'auto-efficacité ne sera pas corrigé par ce mécanisme.
- Angle mort : pas de déclencheur distinct pour VC basse liée à la compréhension vs VC basse liée à la valeur.

**Mastery learning**
- Point solide : `INV_NO_PARTIAL_PATCH_STATE` et `ACTION_ROLLBACK_PATCH` garantissent l'atomicité — cohérent avec le principe de non-régression en mastery.
- Zone de risque : un patch de relevance peut modifier la présentation sans modifier la structure d'évaluation. Si le critère de mastery reste inchangé après un patch de contextualisation, le patch peut sembler inutile.
- Angle mort : aucune trace de suivi post-patch de l'effet sur VC.

**Gouvernance / SRL**
- Point solide : séparation explicite entre patch local et escalade hors session (`ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`) — favorise la métacognition systémique de la plateforme.
- Zone de risque : le mécanisme AR-réfractaire est entièrement paramétrique. Si le seuil Référentiel est mal calibré, le système peut surinférer des profils réfractaires sans signal réel.

---

### Axe 3 — États indéfinis moteur

**3.1 — Accumulation simultanée de déclencheurs**

Scénario : `EVENT_PERSISTENT_LOW_VC` ET `EVENT_AR_REFRACTORY_PROFILE_DETECTED` sont tous deux actifs au même moment. Deux patches sont déclenchés : un patch de relevance et un patch de sollicitation. Aucune règle dans ce scope ne gère la priorité entre `ACTION_TRIGGER_RELEVANCE_PATCH` et `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`.

- Risque moteur : deux patches concurrents, aucun mécanisme de mutex ou de file.
- Statut : `in_scope`
- Type de problème : implémentabilité

**3.2 — Patch bloqué sans signal de dérive persistante**

`INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` déclenche une escalade si un patch reste rejeté. Mais la condition "persistance" n'est pas quantifiée dans ce scope (seuil déporté vers le Référentiel). Si le Référentiel ne définit pas ce seuil, le moteur oscille entre "rejeter et attendre" et "escalader" sans critère décisionnel.

- Risque moteur : oscillation ou blocage.
- Statut : `out_of_scope_but_relevant`

**3.3 — Rollback post-application partielle**

`INV_NO_PARTIAL_PATCH_STATE` exige un rollback en cas de patch partiellement appliqué. Mais `ACTION_ROLLBACK_PATCH` ne précise pas le mécanisme de détection de "partialité" ni la méthode de retour à l'état antérieur (snapshot ? journalisation ?). L'invariant est posé, mais la mécanique d'implémentation reste implicite.

- Risque moteur : état corrompu non détectable si la détection de partialité n'est pas outillée.
- Statut : `in_scope`
- Type de problème : implémentabilité

---

### Axe 4 — Dépendances IA implicites

**4.1 — Détection du profil AR-réfractaire**

`EVENT_AR_REFRACTORY_PROFILE_DETECTED` suppose la détection d'un pattern de non-réponse. Cette détection est présentée comme déterministe (fenêtre de non-réponse + seuil Référentiel). Elle est plausible si la fenêtre est strictement temporelle/comptable. Pas de dépendance IA continue identifiée dans ce scope tant que le seuil reste purement quantitatif.

- Risque résiduel : si "non-réponse AR-N1" nécessite une interprétation qualitative pour être distinguée d'une absence technique, une inférence sémantique pourrait s'introduire.
- Statut : `in_scope`
- Alternative sans IA : fenêtre strictement comptable sur `TYPE_SELF_REPORT_AR_N1` absent/null.

**4.2 — Calcul de `impact_scope` pour la validation locale**

`INV_INVALID_PATCH_REJECTED` exige que `impact_scope` soit calculable. `TYPE_PATCH_IMPACT_SCOPE` déclare que le calcul doit être possible. Aucune définition de l'algorithme de calcul n'est présente dans ce scope. Si ce calcul implique une évaluation sémantique (ex : mesurer l'effet pédagogique d'un changement), une IA continue serait nécessaire — ce qui violerait `CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE`.

- Risque moteur : dépendance IA masquée dans la validation locale si `impact_scope` n'est pas réduit à des critères structurels.
- Statut : `in_scope`
- Alternative sans IA : définir `impact_scope` comme un ensemble d'IDs affectés, calculable déterministiquement par diff structurel.
- Type de problème : implémentabilité / gouvernance

---

### Axe 5 — Gouvernance

**5.1 — `ACTION_LOG_UNCOVERED_CONFLICT` hors module patch**

`ACTION_LOG_UNCOVERED_CONFLICT` est dans le scope écrivable mais son `scope` logique est `runtime_governance`, non couvert par les modules `patch_layer`, `patch_validation`, `patch_architecture`, `patch_governance` déclarés dans `scope_manifest`. Cette entrée semble orpheline dans ce scope.

- Risque : modification possible d'un mécanisme de `runtime_governance` via un run `patch_lifecycle` sans que ce module ne soit formellement dans le périmètre déclaré.
- Statut : `in_scope` (car dans les IDs déclarés du scope), mais signalé comme incohérence de module.
- Type de problème : gouvernance / mauvais placement

**5.2 — Pas de versioning interne des règles paramétriques**

`RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH` et `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH` sont `parameterizable: true` mais `patchable: false`. Il n'existe pas dans ce scope de mécanisme de versioning ou de traçabilité des changements de paramètres Référentiel qui affectent ces règles.

- Risque : un changement de seuil dans le Référentiel peut rendre ces règles sémantiquement différentes sans déclencher un cycle patch/validation de ce scope.
- Statut : `out_of_scope_but_relevant`
- Type de problème : gouvernance / traçabilité

**5.3 — `patchable: false` sur les invariants fondateurs**

Tous les invariants (`INV_*`) sont `patchable: false`. C'est un choix fort et cohérent. Mais aucun mécanisme explicite dans ce scope n'empêche un patch de modifier *indirectement* un invariant via une réécriture de dépendance (ex : patch sur `TYPE_PATCH_ARTIFACT` qui modifie un `depends_on`).

- Risque : contournement indirect d'un invariant `patchable: false` via un patch sur un type qui dépend de lui.
- Statut : `in_scope`
- Type de problème : gouvernance / invariant mal protégé

---

### Axe 6 — Scénarios adversariaux

**Scénario A — Deux patches concurrents, mutex absent**

Contexte : un apprenant affiche une VC basse persistante depuis 4 sessions ET un profil AR-réfractaire confirmé. Le moteur déclenche simultanément `ACTION_TRIGGER_RELEVANCE_PATCH` et `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`.

Mécanismes activés : `EVENT_PERSISTENT_LOW_VC` → `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH` → `ACTION_TRIGGER_RELEVANCE_PATCH` ET `EVENT_AR_REFRACTORY_PROFILE_DETECTED` → `RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH` → `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`.

Limite révélée : aucun mécanisme de priorité ou de sérialisation des patches concurrents. Les deux `TYPE_PATCH_ARTIFACT` sont générés. Si `INV_NO_PARTIAL_PATCH_STATE` s'applique à chaque patch indépendamment, les deux peuvent coexister — mais leur interaction sur l'état apprenant n'est pas couverte.

**Scénario B — Patch de relevance appliqué, VC basse persiste (test frontière scope)**

Contexte : un patch de relevance est appliqué (`ACTION_TRIGGER_RELEVANCE_PATCH`). Trois sessions plus tard, `EVENT_PERSISTENT_LOW_VC` se redéclenche. Le moteur doit décider si un second patch de relevance est possible ou si la dérive est à escalader.

Mécanismes activés : `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`, `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`.

Limite révélée : si le premier patch était dans les bornes et a été appliqué mais est inefficace, `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` ne se déclenche que si le patch suivant est *rejeté ou impossible* — pas si le patch précédent est inefficace. Le moteur peut boucler indéfiniment en appliquant des patches de relevance sans escalader. Ce cas est une **frontière de scope critique** : la décision d'arrêter de patcher et d'escalader dépend d'un critère d'efficacité absent de ce scope.

**Scénario C — Patch invalide en état partiel avec rollback silencieux**

Contexte : un `TYPE_PATCH_ARTIFACT` est soumis avec un `impact_scope` non calculable (ex : ID cible absent du référentiel). `INV_INVALID_PATCH_REJECTED` devrait rejeter le patch. Mais avant le rejet, une partie de l'artefact a été journalisée.

Mécanismes activés : `INV_INVALID_PATCH_REJECTED` (rejet), `INV_NO_PARTIAL_PATCH_STATE` (rollback obligatoire), `ACTION_ROLLBACK_PATCH`.

Limite révélée : `ACTION_ROLLBACK_PATCH` déclare un effet ("retour à l'état antérieur") mais ne spécifie pas la méthode (snapshot, journal, undo-stack). Si la détection de l'état partiel intervient après journalisation partielle, le rollback peut être incomplet. La limite non documentée : absence de définition du périmètre exact de l'état "antérieur".

---

### Axe 7 — Priorisation des risques

| Priorité | ID / Mécanisme | Nature | Type | Statut périmètre |
|---|---|---|---|---|
| **Critique** | Absence de mutex sur patches concurrents (Scénario A) | État moteur indéfini | Implémentabilité | `in_scope` |
| **Critique** | `impact_scope` non défini comme calculable déterministiquement | Dépendance IA masquée | Implémentabilité / Gouvernance | `in_scope` |
| **Élevé** | Rollback sans définition de l'état antérieur (`ACTION_ROLLBACK_PATCH`) | Implémentabilité | Implémentabilité | `in_scope` |
| **Élevé** | Boucle infinie patch-relevance sans critère d'escalade sur inefficacité (Scénario B) | État moteur | Complétude | `in_scope` |
| **Élevé** | `ACTION_LOG_UNCOVERED_CONFLICT` module hors périmètre `patch_*` | Mauvais placement | Gouvernance | `in_scope` |
| **Modéré** | `patchable: false` contournable via dépendance indirecte | Invariant mal protégé | Gouvernance | `in_scope` |
| **Modéré** | `TYPE_STATE_AXIS_VALUE_COST` non dans le voisin obligatoire | Dépendance implicite | Cohérence | `out_of_scope_but_relevant` |
| **Modéré** | `INV_RUNTIME_FULLY_LOCAL` / `INV_NO_RUNTIME_CONTENT_GENERATION` non dans le voisin | Dépendance implicite | Complétude | `out_of_scope_but_relevant` |
| **Modéré** | Pas de versioning des paramètres Référentiel impactant les règles | Traçabilité | Gouvernance | `out_of_scope_but_relevant` |
| **Faible** | `parameterizable: true` + `patchable: false` : frontière patch/paramètre non formalisée | Ambiguïté | Gouvernance | `in_scope` |
| **Faible** | `TYPE_SELF_REPORT_AR_N1` absent du voisin obligatoire | Complétude | Cohérence | `out_of_scope_but_relevant` |

---

## Corrections à arbitrer avant patch

### C01 — Définir un mécanisme de sérialisation / priorité pour les patches concurrents
- **Élément concerné :** `ACTION_TRIGGER_RELEVANCE_PATCH`, `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`
- **Nature :** absence de règle de priorité ou de mutex
- **Type :** implémentabilité
- **Impact moteur :** double patch non ordonné, effet apprenant non déterministe
- **Statut périmètre :** `in_scope`
- **Correction à arbitrer :** introduire une règle de sérialisation explicite (ex : une seule action de patch active à la fois par apprenant, queue FIFO ou priorité déclarée) dans `patch_governance`.

### C02 — Formaliser la définition déterministe de `impact_scope`
- **Élément concerné :** `TYPE_PATCH_IMPACT_SCOPE`, `INV_INVALID_PATCH_REJECTED`
- **Nature :** calcul d'`impact_scope` non spécifié comme déterministe
- **Type :** implémentabilité / gouvernance
- **Impact moteur :** risque de dépendance IA masquée dans la validation locale
- **Statut périmètre :** `in_scope`
- **Correction à arbitrer :** ajouter dans `TYPE_PATCH_IMPACT_SCOPE` ou dans une règle `patch_validation` la définition formelle de l'algorithme de calcul (ex : ensemble d'IDs affectés, calculable par diff structurel sur les fichiers concernés).

### C03 — Spécifier le mécanisme de rollback dans `ACTION_ROLLBACK_PATCH`
- **Élément concerné :** `ACTION_ROLLBACK_PATCH`, `INV_NO_PARTIAL_PATCH_STATE`
- **Nature :** rollback déclaré sans mécanique d'implémentation
- **Type :** implémentabilité
- **Impact moteur :** état corrompu possible si la méthode de rollback est ambiguë
- **Statut périmètre :** `in_scope`
- **Correction à arbitrer :** préciser dans `ACTION_ROLLBACK_PATCH` la méthode (snapshot avant application, journal transactionnel, ou undo-stack) et la condition de détection de partialité.

### C04 — Ajouter un critère d'escalade basé sur l'inefficacité d'un patch précédent
- **Élément concerné :** `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`, `RULE_PERSISTENT_DRIFT_BLOCKED_PATCH_ESCALATES_OFFSESSION`
- **Nature :** boucle possible si un patch est valide mais inefficace
- **Type :** complétude
- **Impact moteur :** boucle infinie de patches de relevance sans sortie d'escalade
- **Statut périmètre :** `in_scope`
- **Correction à arbitrer :** étendre `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` ou créer une règle complémentaire : si N patches successifs du même type ont été appliqués sans résolution du signal de dérive, l'escalade devient obligatoire (N = paramètre Référentiel).

### C05 — Réexaminer le placement de `ACTION_LOG_UNCOVERED_CONFLICT` dans ce scope
- **Élément concerné :** `ACTION_LOG_UNCOVERED_CONFLICT` (module déclaré : `runtime_governance`)
- **Nature :** module non couvert par `scope_manifest` (modules déclarés : `patch_layer`, `patch_validation`, `patch_architecture`, `patch_governance`)
- **Type :** gouvernance / mauvais placement
- **Impact moteur :** risque de modification de `runtime_governance` via un run `patch_lifecycle`
- **Statut périmètre :** `in_scope` (ID dans le scope, module incohérent)
- **Correction à arbitrer :** soit retirer `ACTION_LOG_UNCOVERED_CONFLICT` du scope `patch_lifecycle` (et le déplacer vers un scope `runtime_governance`), soit déclarer explicitement `runtime_governance` comme module couvert par ce scope.

### C06 — Protéger les invariants `patchable: false` contre contournement via dépendance
- **Élément concerné :** tous les `INV_*` avec `patchable: false`
- **Nature :** absence de garde explicite contre la modification indirecte
- **Type :** gouvernance
- **Impact moteur :** invariant fondateur potentiellement contournable via patch sur un type dépendant
- **Statut périmètre :** `in_scope`
- **Correction à arbitrer :** ajouter une règle de validation structurelle dans `patch_validation` : un patch ne peut pas modifier un champ `depends_on` d'un type si cela affecte directement un invariant `patchable: false`.

---

## Éléments hors scope signalés (non correctibles dans ce run sans décision d'élargissement)

| ID / Mécanisme | Motif | Recommandation |
|---|---|---|
| `TYPE_STATE_AXIS_VALUE_COST` | Dépendance non couverte par le voisin obligatoire | Envisager l'ajout comme `neighbor_scope` dans un run futur |
| `INV_RUNTIME_FULLY_LOCAL` / `INV_NO_RUNTIME_CONTENT_GENERATION` | Dépendances fondatrices de `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` non lisibles | Ajouter au `neighbor_extract` si le scope est revu |
| `TYPE_SELF_REPORT_AR_N1` | Ancrage des déclencheurs AR non challengeable | Signaler au scope d'origine (`learner_state` ou équivalent) |
| Versioning paramètres Référentiel | Aucune traçabilité cross-scope sur l'évolution des paramètres | Décision de gouvernance inter-scope nécessaire |

---

*Rapport produit en mode `bounded_local_run`, lecture ids-first, aucun fallback sur Core complet.*
*Scope : `patch_lifecycle` | Run : `CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01` | Stage : STAGE_01_CHALLENGE*
