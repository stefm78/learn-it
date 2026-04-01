# CHALLENGE REPORT — Constitution Learn-it V1.9
## challenge_report_01_GPTThink.md

**Date :** 2026-04-01  
**Auditeur :** GPT adversarial  
**Core cible :** CORE_LEARNIT_CONSTITUTION_V1_9  
**Version auditée :** V1_9_FINAL  
**Note de focalisation :** aucune

---

## Résumé exécutif

La Constitution V1.9 est un système de gouvernance pédagogique dense et structuré. Elle présente une architecture cohérente dans ses grandes lignes : séparation Constitution/Référentiel, localité du moteur, modèle MSC à 4 composantes, modèle d'état apprenant à 3 axes. Elle a visiblement bénéficié de plusieurs patches successifs (PATCH_V1_9, ARBITRAGE_2026_04_01).

Cependant, l'audit adversarial révèle plusieurs faiblesses non triviales :

1. **Le couplage implicite au Référentiel est sous-spécifié en Constitution** — de nombreux éléments constitutionnels délèguent leurs seuils et comportements au Référentiel sans contraindre les bornes acceptables ni les comportements de défaut si le Référentiel est absent ou corrompu.
2. **L'état apprenant composite est partiellement flottant** — l'axe VC est optionnel, l'axe Activation dépend exclusivement d'AR-N1, et aucune règle constitutionnelle ne définit comment le moteur doit arbitrer entre des axes en conflit ou entre `unknown` et une action nécessaire.
3. **La gestion des KU créatives est insuffisamment bornée** — l'invariant `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` bloque le déploiement en mode autonome, mais aucune règle ne définit le comportement obligatoire du moteur si une KU créative est déployée sans que la vérification ait été effectuée.
4. **L'événement `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` introduit un couplage temporel non borné** — la divergence est conditionnée à un seuil référentiel (`PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`) dont l'existence n'est pas garantie constitutionnellement.
5. **La gouvernance de patch souffre d'une lacune d'escalade structurelle** — `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` exige une escalade mais ne définit ni la cible, ni le délai, ni le circuit d'escalade.

---

## Analyse détaillée par axe

---

### Axe 1 — Cohérence interne

#### 1.1 — Bindings Référentiel sous-spécifiés (risque : **élevé**)

De nombreux types, invariants et règles déclarent `depends_on: REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` pour déléguer leurs seuils (exemples : `TYPE_MASTERY_COMPONENT_P`, `TYPE_MASTERY_COMPONENT_R`, `TYPE_MASTERY_COMPONENT_A`, `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`, `EVENT_PERSISTENT_LOW_VC`, `EVENT_AR_REFRACTORY_PROFILE_DETECTED`, `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`).

**Problème :** La Constitution ne définit aucune contrainte sur les bornes minimales/maximales que le Référentiel est autorisé à déclarer pour ces seuils. Elle ne définit pas non plus de comportement de défaut constitutionnel si le Référentiel est absent, invalide ou non chargé.

**Risque moteur :** Le moteur peut rester en état indéfini sur des décisions critiques (déclenchement d'une reprise diagnostique, détection d'une divergence MSC, détection d'un profil AR-réfractaire) si le Référentiel manque.

**Correction à arbitrer :** Ajouter en Constitution soit (a) des valeurs plancher/plafond constitutionnelles pour les seuils critiques, soit (b) un invariant de défaut explicite forçant le comportement conservateur documenté lorsque le Référentiel est absent ou invalide pour un seuil donné.

---

#### 1.2 — `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` sans mécanisme de détection runtime (risque : **modéré**)

L'invariant déclare que la présence d'un cycle est un état interdit bloquant le chargement. Cependant, la Constitution ne déclare aucun type ou action associé à la **détection** de ce cycle (`scope: knowledge_model` mais aucun `ACTION_*` lié, aucun `EVENT_CYCLE_DETECTED`).

**Risque moteur :** Un cycle non détecté à la validation design peut atteindre le runtime. L'invariant n'est alors plus applicable sans mécanisme d'application.

**Correction à arbitrer :** Déclarer un `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` et une `ACTION_BLOCK_GRAPH_LOAD` associés à `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC`.

---

#### 1.3 — Dépendance circulaire apparente entre `TYPE_MASTERY_COMPONENT_T` et `TYPE_MASTERY_MODEL` (risque : **faible**)

`TYPE_MASTERY_COMPONENT_T` déclare `derives_from: TYPE_MASTERY_MODEL`, et `TYPE_MASTERY_MODEL` dépend de `TYPE_MASTERY_COMPONENT_T`. Cette relation circulaire est justifiée sémantiquement (T est séparé et dérive du modèle global) mais crée une ambiguïté sur l'ordre de résolution au chargement du Core.

**Correction à arbitrer :** Documenter explicitement l'ordre de résolution ou clarifier que la relation `derives_from` est de nature descriptive et non d'instanciation.

---

#### 1.4 — `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` source_anchor hétérogène (risque : **modéré**)

Cette règle et son événement associé portent `source_anchor: '[ARBITRAGE_2026_04_01][DIVMSC-01]'` — une référence à un arbitrage daté, pas à une ancre de source constitutionnelle normative (`[Sxx]`). Cela crée une hétérogénéité de traçabilité dans la Constitution : les autres éléments référencent des ancres `[Sxx]` stables.

**Risque :** Si la traceability des arbitrages évolue, cette règle sera difficile à localiser dans l'historique constitutionnel.

**Correction à arbitrer :** Normaliser le source_anchor vers une ancre `[Sxx]` si la règle devient permanente, ou documenter la convention d'ancrage par arbitrage.

---

### Axe 2 — Solidité théorique

#### 2.1 — Charge cognitive : absence de règle constitutionnelle bornant la densité de sollicitation AR (risque : **modéré**)

Les types AR-N1, AR-N2, AR-N3 sont déclarés avec des budgets d'interaction (PARAM_AR_N*_INTERACTION_BUDGET), mais aucune règle ne contraint la **fréquence cumulée** des sollicitations AR sur une session ou une période. Un moteur conforme à la Constitution peut saturer l'apprenant avec des micro-sondages sans violer aucun invariant.

**Correction à arbitrer :** Déclarer un invariant ou une règle bornant la fréquence cumulative des sollicitations AR (toutes natures confondues) par session ou par unité de temps.

---

#### 2.2 — Mémoire / consolidation : `TYPE_MASTERY_COMPONENT_R` (robustesse temporelle) sans mécanisme de degradation constitutionnel (risque : **élevé**)

R qualifie la robustesse temporelle, mais aucun mécanisme constitutionnel ne définit comment R se dégrade avec le temps en l'absence d'activité. Le Référentiel est censé borner les multiplicateurs, mais la Constitution ne déclare pas que la dégradation de R est obligatoire ou même possible.

**Risque moteur :** Un moteur peut maintenir R constant à sa valeur maximale indéfiniment, rendant la maîtrise de base indéfiniment déclarée même après une très longue interruption sans réactivation diagnostique.

**Correction à arbitrer :** Ajouter en Constitution une déclaration explicite que R est soumis à une décroissance temporelle constitutive, dont les paramètres sont bornés par le Référentiel.

---

#### 2.3 — Métacognition / SRL : AR-N3 est déclaré mais structurellement orphelin (risque : **modéré**)

`TYPE_SELF_REPORT_AR_N3` est déclaré comme « bilan périodique dérivé d'AEQ » alimentant un « indice de calibration auto-rapport ». Mais aucune règle ni action ne définit ce que le moteur fait de cet indice — il n'est consommé par aucun `TYPE_*`, `RULE_*`, ni `INV_*` identifiable dans la Constitution.

**Risque moteur :** AR-N3 est collecté sans effet garanti sur le modèle apprenant ou la trajectoire. Son utilité moteur est non définie constitutionnellement.

**Correction à arbitrer :** Soit déclarer explicitement la consommation de l'indice AR-N3 (par quelle composante du modèle, sous quelle condition), soit documenter que l'usage relève du Référentiel et ajouter le binding explicite.

---

#### 2.4 — Engagement / gamification : `RULE_UNVERIFIED_GAMIFICATION_PROBATION` sans définition de clôture de probation (risque : **modéré**)

La règle déclare un « mode probatoire » si la gamification n'a pas été testée, mais aucun invariant ni action ne définit les conditions de sortie de ce mode probatoire.

**Risque moteur :** Le moteur peut rester en mode probatoire de gamification indéfiniment sans mécanisme de validation.

**Correction à arbitrer :** Déclarer les conditions de sortie du mode probatoire (ex. : après N sessions sans effet négatif mesuré, passage automatique au mode validé).

---

### Axe 3 — États indéfinis moteur

#### 3.1 — Conflit entre `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` et les règles déclenchées par l'état apprenant (risque : **élevé**)

`RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise explicitement que l'axe d'Activation ou l'axe VC reste `unknown`. Mais plusieurs règles se déclenchent sur la valeur de ces axes (ex. : `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`, `INV_VC_NOT_GENERAL_MOTIVATION_PROXY`, `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`).

**État indéfini :** Si l'axe VC est `unknown` pendant N sessions, `EVENT_PERSISTENT_LOW_VC` ne peut pas se déclencher (pas de valeur basse persistante). Mais le moteur n'a aucune règle constitutionnelle sur le comportement à adopter face à une VC persistamment inconnue.

**Correction à arbitrer :** Définir explicitement le comportement moteur face à un axe VC persistamment `unknown` (ex. : neutralité, escalade vers l'humain, reclassification en `unknown-significant`).

---

#### 3.2 — `EVENT_GF08_UNCOVERED_CONFLICT` : réponse conservatrice non définie opérationnellement (risque : **modéré**)

La règle `RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE` prescrit une réponse conservatrice et un log, mais ne définit pas ce que « conservatrice » signifie dans ce contexte précis (par opposition à `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` qui la définit comme « scaffolding léger réversible »).

**Risque moteur :** Deux occurrences du terme « conservatrice » avec des sémantiques potentiellement différentes. Un conflit inter-principes non couvert peut recevoir une réponse inadaptée si la définition n'est pas harmonisée.

**Correction à arbitrer :** Aligner la définition constitutionnelle de la réponse conservatrice en contexte GF-08 avec celle déjà déclarée pour l'absence d'AR-N1, ou les distinguer explicitement.

---

#### 3.3 — `INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK` : comportement de gel partiellement indéfini (risque : **modéré**)

L'invariant déclare que la KU est « gelée pour l'adaptation fine ». Mais aucune règle ne définit ce qui se passe si l'apprenant atteint une KU gelée dans un parcours obligatoire — le moteur peut-il sauter la KU ? La signaler ? Bloquer le parcours ?

**Correction à arbitrer :** Déclarer le comportement obligatoire du moteur face à une KU gelée en chemin critique (blocage, déviation, signalement).

---

### Axe 4 — Dépendances IA implicites

#### 4.1 — `TYPE_FEEDBACK_COVERAGE_MATRIX` : couverture déclarée comme livrable de design, mais vérification runtime non définie (risque : **élevé**)

La matrice de couverture est produite en phase Design (`scope: design`). La règle `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK` s'applique si aucun template n'est couvert. Mais aucun mécanisme constitutionnel ne garantit que la matrice est **chargée et accessible** au moteur en runtime.

**Dépendance implicite :** Le moteur doit inférer la présence ou l'absence d'un template couvert — ce qui suppose un accès structuré à la matrice. Si la matrice est manquante ou corrompue, le moteur appliquera systématiquement le feedback générique sans le détecter comme anormal.

**Correction à arbitrer :** Ajouter un invariant exigeant la présence et l'intégrité de la matrice de couverture comme précondition de chargement du domaine.

---

#### 4.2 — Détection du profil AR-réfractaire (`EVENT_AR_REFRACTORY_PROFILE_DETECTED`) : inférence comportementale sans critère constitutionnel (risque : **modéré**)

La détection du profil AR-réfractaire repose sur une « fenêtre de non-réponse » dont le seuil est dans le Référentiel. Mais la Constitution ne définit pas si la non-réponse à AR-N1 est distinguable d'un problème technique, d'une session très courte ou d'un refus délibéré.

**Dépendance implicite :** Le moteur doit inférer l'intentionnalité de la non-réponse — ce qui requiert une sémantique comportementale qui dépasse les données structurelles.

**Correction à arbitrer :** Déclarer constitutionnellement que la non-réponse AR-N1 est traitée comme un signal neutre jusqu'au seuil référentiel, sans inférence sur la cause.

---

### Axe 5 — Gouvernance

#### 5.1 — `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` : circuit d'escalade non défini (risque : **élevé**)

L'invariant exige une escalade « hors session vers la chaîne d'analyse/correction » mais ne déclare ni la cible de l'escalade, ni le délai maximal avant escalade, ni la forme du signal d'escalade.

**Risque :** Invariant déclaratif sans applicabilité technique — un moteur conforme peut générer une escalade vide ou non adressée.

**Correction à arbitrer :** Déclarer dans la Constitution les attributs minimaux d'un signal d'escalade (cible, format minimal, délai maximal) ou déléguer explicitement cette spécification au Référentiel avec un binding explicite.

---

#### 5.2 — Versioning du Core : absence de règle de compatibilité descendante (risque : **modéré**)

La Constitution est en `V1_9_FINAL` mais aucune règle ne définit ce qui est autorisé ou interdit lors du passage à une version ultérieure (ex. : `V2.0`). La séparation Constitution/Référentiel est déclarée inviolable, mais la compatibilité des entités d'une version à l'autre n'est pas définie.

**Risque :** Un upgrade majeur peut casser silencieusement des dépendances inter-Core sans violation d'invariant constitutionnel.

**Correction à arbitrer :** Déclarer une règle de compatibilité minimale (ex. : tout ID constitutionnel existant ne peut être supprimé sans passer par un cycle de dépréciation explicite).

---

#### 5.3 — Traçabilité des patches appliqués : `source_anchor` PATCH_V1_9 sans registre constitutionnel (risque : **faible**)

Plusieurs éléments portent `source_anchor: '[PATCH_V1_9]'` ou `'[PATCH_V1_9__STAGE03]'`, mais la Constitution ne déclare pas de mécanisme de registre des patches appliqués. La trace est dans les ancres, pas dans un artefact structuré.

**Correction à arbitrer :** Envisager un bloc `APPLIED_PATCHES` dans le Core pour tracer les patches intégrés de façon structurée et requêtable.

---

### Axe 6 — Priorisation des risques

| ID | Titre court | Axe | Priorité |
|---|---|---|---|
| C-01 | Seuils Référentiel sans défaut constitutionnel | 1 | **Critique** |
| C-02 | Dégradation de R non déclarée constitutionnellement | 2 | **Élevé** |
| C-03 | État VC persistamment unknown sans comportement défini | 3 | **Élevé** |
| C-04 | Circuit d'escalade non défini pour dérive persistante | 5 | **Élevé** |
| C-05 | Feedback Coverage Matrix sans garantie de chargement | 4 | **Élevé** |
| C-06 | AR-N3 orphelin sans consommation définie | 2 | **Modéré** |
| C-07 | Cycle KU sans EVENT/ACTION de détection runtime | 1 | **Modéré** |
| C-08 | Densité cumulée AR-N* sans borne constitutionnelle | 2 | **Modéré** |
| C-09 | KU créative gelée en chemin critique sans comportement | 3 | **Modéré** |
| C-10 | GF-08 réponse conservatrice non opérationnellement définie | 3 | **Modéré** |
| C-11 | Profil AR-réfractaire : non-réponse sans sémantique | 4 | **Modéré** |
| C-12 | Gamification probatoire sans condition de sortie | 2 | **Modéré** |
| C-13 | Divergence MSC — seuil référentiel non garanti exister | 1 | **Modéré** |
| C-14 | Compatibilité descendante entre versions de Core | 5 | **Modéré** |
| C-15 | Dépendance circulaire T ↔ MasteryModel (ordre de résolution) | 1 | **Faible** |
| C-16 | source_anchor hétérogène ARBITRAGE_2026_04_01 | 1 | **Faible** |
| C-17 | Registre structuré des patches appliqués absent | 5 | **Faible** |

---

## Corrections à arbitrer avant patch

Les éléments suivants doivent être soumis à l'arbitrage (STAGE_02) avant toute synthèse de patch :

1. **[C-01]** Définir le comportement de défaut constitutionnel lorsque le Référentiel ne fournit pas un seuil attendu (valeur plancher, comportement conservateur, état interdit de déploiement).
2. **[C-02]** Déclarer constitutionnellement que R est soumis à une décroissance temporelle, paramétrisée par le Référentiel.
3. **[C-03]** Définir le comportement moteur face à une VC persistamment `unknown` (neutralité active, escalade, traitement différencié).
4. **[C-04]** Spécifier les attributs minimaux du signal d'escalade requis par `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`.
5. **[C-05]** Ajouter un invariant de précondition garantissant la présence et l'intégrité de la Feedback Coverage Matrix avant chargement du domaine.
6. **[C-06]** Décider si la consommation de l'indice AR-N3 est constitutionnelle ou référentielle, et déclarer le binding correspondant.
7. **[C-07]** Déclarer EVENT et ACTION associés à la détection d'un cycle dans le graphe de KU.
8. **[C-08]** Introduire une contrainte ou un invariant sur la densité cumulée des sollicitations AR par session.
9. **[C-09]** Déclarer le comportement obligatoire du moteur face à une KU créative gelée en chemin critique.
10. **[C-10]** Harmoniser la définition opérationnelle de la « réponse conservatrice » entre les contextes GF-08 et absence d'AR-N1.
