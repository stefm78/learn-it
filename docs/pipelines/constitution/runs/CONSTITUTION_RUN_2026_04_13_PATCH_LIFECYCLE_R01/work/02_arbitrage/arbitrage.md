# Arbitrage — STAGE_02_ARBITRAGE
# Run : CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01
# Scope : patch_lifecycle
# Date : 2026-04-13
# Produit par : AI (bounded_local_run)

---

## Résumé exécutif

**Mode utilisé :** `bounded` (`bounded_local_run`)

| Décision | Nombre |
|---|---|
| `corriger_maintenant` | 4 |
| `reporter` | 1 |
| `rejeter` | 0 |
| `hors_perimetre` | 4 |
| `necessite_extension_scope` | 1 |

**Synthèse :** Le challenge a identifié 6 corrections in-scope (C01–C06) et 4 points hors périmètre. Après arbitrage, 4 corrections sont retenues pour le patch (C01, C02, C03, C04 — les 2 critiques et les 2 élevées in-scope les plus impactantes). C05 est reporté (décision de placement à arbitrer au niveau cross-scope). C06 est transformé en `necessite_extension_scope` (la garde anti-contournement dépend de la spec du script de validation structurelle, hors constitution). Les 4 points hors scope restent `hors_perimetre` sans extension décidée ici.

---

## Périmètre analysé

### Fichiers de challenge considérés
- `runs/CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01/work/01_challenge/challenge_report_01.md`

### Notes humaines prises en compte
Aucune note humaine d'arbitrage fournie.

### Scope déclaré
- `scope_key: patch_lifecycle`
- Modules : `patch_layer`, `patch_validation`, `patch_architecture`, `patch_governance`
- 21 IDs in-scope écrivables
- Opérations autorisées : `challenge`, `arbitrage`, `patch`, `local_validation`
- Opérations interdites : `direct_current_promotion`, `silent_out_of_scope_modification`, `implicit_cross_core_reallocation`

### Limites de périmètre
- Les IDs `TYPE_STATE_AXIS_VALUE_COST`, `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `TYPE_SELF_REPORT_AR_N1` sont hors scope et non modifiables dans ce run.
- Le versioning des paramètres Référentiel est une décision de gouvernance inter-scope, hors périmètre.

---

## Arbitrage détaillé

---

### Point C01 — Mutex / sérialisation des patches concurrents

- **Source :** challenge_report_01.md, Axe 3.1 + Scénario A + tableau Axe 7
- **Constat synthétique :** Deux actions de patch (`ACTION_TRIGGER_RELEVANCE_PATCH` et `ACTION_TRIGGER_AR_SOLLICITATION_PATCH`) peuvent être déclenchées simultanément. Aucune règle de priorité ou de sérialisation n'est déclarée dans `patch_governance`. L'interaction de deux patches concurrents sur l'état apprenant est non déterministe.
- **Nature :** logique / implémentabilité
- **Gravité :** critique
- **Impact :** applicabilité, sécurité logique du moteur, stabilité
- **Statut de périmètre :** `in_scope`
- **Décision :** `corriger_maintenant`
- **Justification :** Le risque est critique, directement actionnable dans le scope `patch_governance`, et la correction est minimale : ajouter une règle de sérialisation (une seule action de patch active par apprenant à un instant donné, queue FIFO ou priorité déclarée). Le patch n'impacte aucun élément hors scope.
- **Conséquence attendue pour le patch :** Ajouter une règle ou un invariant dans `patch_governance` déclarant la sérialisation des actions de patch concurrentes. Candidat : nouvelle `RULE_PATCH_SERIALIZATION` ou extension de `TYPE_PATCH_ARTIFACT`.

---

### Point C02 — Définition déterministe de `impact_scope`

- **Source :** challenge_report_01.md, Axe 4.2 + tableau Axe 7
- **Constat synthétique :** `TYPE_PATCH_IMPACT_SCOPE` déclare que `impact_scope` doit être calculable, mais ne définit pas l'algorithme de calcul. Si ce calcul implique une évaluation sémantique, cela viole `CONSTRAINT_NO_AUTONOMOUS_PSYCHOLOGICAL_INFERENCE` et introduit une dépendance IA masquée dans la validation locale.
- **Nature :** gouvernance / implémentabilité
- **Gravité :** critique
- **Impact :** sécurité logique, applicabilité, cohérence avec `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`
- **Statut de périmètre :** `in_scope`
- **Décision :** `corriger_maintenant`
- **Justification :** La correction est directement exigée par `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` déjà dans le scope. Il suffit d'ajouter dans la `logic` de `TYPE_PATCH_IMPACT_SCOPE` la définition formelle : `impact_scope` = ensemble structurel d'IDs affectés, calculable par diff déterministe. Correction minimale, aucun élément hors scope touché.
- **Conséquence attendue pour le patch :** Modifier la `logic` de `TYPE_PATCH_IMPACT_SCOPE` pour y déclarer explicitement que le calcul est structurel et déterministe (liste d'IDs delta). Pas de nouvelle entrée nécessaire.

---

### Point C03 — Mécanisme de rollback dans `ACTION_ROLLBACK_PATCH`

- **Source :** challenge_report_01.md, Axe 3.3 + Scénario C + tableau Axe 7
- **Constat synthétique :** `ACTION_ROLLBACK_PATCH` déclare un effet (retour à l'état antérieur) sans spécifier la méthode (snapshot, journal transactionnel, undo-stack) ni la condition de détection de partialité. `INV_NO_PARTIAL_PATCH_STATE` exige le rollback mais ne peut être garanti sans méthode définie.
- **Nature :** implémentabilité
- **Gravité :** élevé
- **Impact :** applicabilité, sécurité logique, maintenabilité
- **Statut de périmètre :** `in_scope`
- **Décision :** `corriger_maintenant`
- **Justification :** Correction minimale : préciser dans la `logic` de `ACTION_ROLLBACK_PATCH` la méthode de rollback et la condition de détection (snapshot d'état avant application). Directement actable dans `patch_layer`, aucun élément hors scope. Sans cette précision, `INV_NO_PARTIAL_PATCH_STATE` reste un invariant sans mécanisme opérationnel garanti.
- **Conséquence attendue pour le patch :** Modifier la `logic` de `ACTION_ROLLBACK_PATCH` pour y déclarer : condition de déclenchement (détection d'état partiel = toute interruption avant commit complet), méthode (snapshot pré-application obligatoire), et périmètre de retour (état identique au snapshot pré-application).

---

### Point C04 — Escalade sur inefficacité de patch (boucle relevance)

- **Source :** challenge_report_01.md, Axe 3.2 + Scénario B + tableau Axe 7
- **Constat synthétique :** `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` ne couvre que le cas où le patch est rejeté ou impossible. Si le patch est valide et appliqué mais inefficace, le moteur peut boucler indéfiniment en appliquant des patches de relevance sans jamais escalader.
- **Nature :** complétude
- **Gravité :** élevé
- **Impact :** stabilité moteur, applicabilité, sécurité logique
- **Statut de périmètre :** `in_scope`
- **Décision :** `corriger_maintenant`
- **Justification :** Le trou de couverture est direct et actionnable : il suffit d'étendre la condition d'escalade pour couvrir aussi le cas « N patches successifs du même type appliqués sans résolution du signal ». N est paramétrique (Référentiel), ce qui préserve la séparation des couches. Correction minimale, aucun élément hors scope.
- **Conséquence attendue pour le patch :** Étendre `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` : ajouter dans sa `logic` la condition complémentaire (N applications successives du même type de patch sans disparition du signal de dérive → escalade obligatoire). N déclaré comme paramètre Référentiel.

---

### Point C05 — Placement de `ACTION_LOG_UNCOVERED_CONFLICT` (module `runtime_governance`)

- **Source :** challenge_report_01.md, Axe 5.1 + tableau Axe 7
- **Constat synthétique :** `ACTION_LOG_UNCOVERED_CONFLICT` est dans les IDs du scope `patch_lifecycle` mais son champ `scope` logique est `runtime_governance`, non couvert par les modules déclarés du scope (`patch_layer`, `patch_validation`, `patch_architecture`, `patch_governance`). L'entrée est incohérente avec le périmètre modulaire déclaré.
- **Nature :** gouvernance / mauvais placement
- **Gravité :** élevé
- **Impact :** gouvernance, maintenabilité
- **Statut de périmètre :** `in_scope` (ID dans le scope), mais incohérence de module
- **Décision :** `reporter`
- **Justification :** La correction correcte nécessite une décision cross-scope : soit retirer cet ID du scope `patch_lifecycle` et l'affecter à un scope `runtime_governance` (qui n'existe peut-être pas encore), soit déclarer `runtime_governance` comme module couvert par ce scope. Cette décision dépasse le périmètre d'un arbitrage local sans vision de l'ensemble des scopes publiés. Reporter à un arbitrage de partitionnement (STAGE_00 d'un run futur ou révision de la scope_definition).
- **Conséquence attendue pour le patch :** Aucune modification de `ACTION_LOG_UNCOVERED_CONFLICT` dans ce run. Ouvrir une note de gouvernance dans le rapport.

---

### Point C06 — Protection des invariants `patchable: false` contre contournement indirect

- **Source :** challenge_report_01.md, Axe 5.3 + tableau Axe 7
- **Constat synthétique :** Aucune garde explicite n'empêche qu'un patch modifie un champ `depends_on` d'un type de façon à affecter indirectement un invariant `patchable: false`. La protection est conceptuelle, pas structurellement enforced.
- **Nature :** gouvernance
- **Gravité :** modéré
- **Impact :** sécurité logique, maintenabilité
- **Statut de périmètre :** `in_scope`
- **Décision :** `necessite_extension_scope`
- **Justification :** La garde anti-contournement devrait être une règle de validation structurelle dans `patch_validation`. Cependant, son implémentation dépend de la spec de `validate_patchset.py` (script déterministe), qui est hors périmètre Constitution. Introduire cette règle dans la Constitution sans la spec correspondante du script créerait une règle non enforçable. Décision : déclarer le besoin, mais ne pas patcher sans que la spec du script soit alignée.
- **Conséquence attendue pour le patch :** Aucune modification immédiate. Créer une note `needs_scope_extension` dans le rapport pour ouvrir le sujet dans un run futur couvrant `patch_validation` + la spec de `validate_patchset.py`.

---

### Points hors périmètre (non correctibles dans ce run)

#### HP-01 — `TYPE_STATE_AXIS_VALUE_COST` absent du voisinage obligatoire
- **Source :** challenge_report_01.md, Axe 1.1
- **Décision :** `hors_perimetre`
- **Justification :** ID appartenant probablement au scope `learner_state`. Non modifiable dans ce run. À signaler pour ajout comme `neighbor_scope` dans la scope_definition `patch_lifecycle` lors d'une révision de partition.

#### HP-02 — `INV_RUNTIME_FULLY_LOCAL` / `INV_NO_RUNTIME_CONTENT_GENERATION` absents du voisinage
- **Source :** challenge_report_01.md, Axe 1.2
- **Décision :** `hors_perimetre`
- **Justification :** Dépendances fondatrices de `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`. Non challengeable sans élargissement. À ajouter au `neighbor_extract` si la scope_definition est révisée.

#### HP-03 — `TYPE_SELF_REPORT_AR_N1` absent du voisinage
- **Source :** challenge_report_01.md, Axe 1.3
- **Décision :** `hors_perimetre`
- **Justification :** Ancrage des déclencheurs AR non challengeable dans ce run. Signaler au scope d'origine.

#### HP-04 — Versioning des paramètres Référentiel impactant les règles `parameterizable: true`
- **Source :** challenge_report_01.md, Axe 5.2
- **Décision :** `hors_perimetre`
- **Justification :** Décision de gouvernance inter-scope. Aucune correction possible dans ce run sans vision complète des scopes Référentiel.

---

## Points consolidés

- **C01 + Scénario A** : regroupés (même problème — mutex concurrent). Un seul point arbitré.
- **C02 + Axe 4.2** : regroupés (même problème — déterminisme `impact_scope`). Un seul point arbitré.
- **C03 + Scénario C** : regroupés (même problème — rollback sans méthode). Un seul point arbitré.
- **C04 + Scénario B** : regroupés (même problème — boucle relevance sans escalade). Un seul point arbitré.
- Aucune contradiction entre constats. Un seul rapport de challenge, pas de divergence inter-rapports.

---

## Décisions à transmettre au patch

| Priorité | Point | Élément(s) à modifier | Contrainte |
|---|---|---|---|
| **Critique** | C01 | `patch_governance` — nouvelle règle de sérialisation des patches concurrents | Minimale, pas de nouvel ID hors scope |
| **Critique** | C02 | `TYPE_PATCH_IMPACT_SCOPE` — préciser `logic` : calcul déterministe structurel | Modification de `logic` uniquement |
| **Élevé** | C03 | `ACTION_ROLLBACK_PATCH` — préciser `logic` : snapshot pré-application + condition partialité | Modification de `logic` uniquement |
| **Élevé** | C04 | `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` — étendre condition escalade | Ajouter condition N-patches inefficaces ; N = param Référentiel |

**Contrainte transversale :** tout patch doit rester dans les modules `patch_layer`, `patch_validation`, `patch_architecture`, `patch_governance`. Aucune modification hors `writable_perimeter` du `scope_manifest`. Aucune promotion implicite.

---

## Décisions explicitement non retenues

| Point | Décision | Justification |
|---|---|---|
| C05 — Placement `ACTION_LOG_UNCOVERED_CONFLICT` | `reporter` | Décision cross-scope requise (scope `runtime_governance` inexistant ou non ouvert) |
| C06 — Garde anti-contournement `patchable: false` | `necessite_extension_scope` | Dépend de la spec de `validate_patchset.py`, hors Constitution |
| HP-01 — `TYPE_STATE_AXIS_VALUE_COST` | `hors_perimetre` | Scope `learner_state`, non modifiable ici |
| HP-02 — `INV_RUNTIME_FULLY_LOCAL` / `INV_NO_RUNTIME_CONTENT_GENERATION` | `hors_perimetre` | Hors scope, à ajouter au voisinage si scope révisé |
| HP-03 — `TYPE_SELF_REPORT_AR_N1` | `hors_perimetre` | Scope d'origine non ouvert |
| HP-04 — Versioning paramètres Référentiel | `hors_perimetre` | Gouvernance inter-scope, hors périmètre de ce run |

---

*Arbitrage produit en mode `bounded_local_run`.*  
*Scope : `patch_lifecycle` | Run : `CONSTITUTION_RUN_2026_04_13_PATCH_LIFECYCLE_R01` | Stage : STAGE_02_ARBITRAGE*
