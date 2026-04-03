# ARBITRAGE — Constitution Learn-it V1.9
## arbitrage_01_GPTThink.md

**Date :** 2026-04-01  
**Arbitre :** GPT governance  
**Source challenge :** `work/01_challenge/challenge_report_01_GPTThink.md`  
**Notes humaines :** aucune  
**Contraintes de portée :** aucune déclarée

---

## Résumé exécutif

L'arbitrage porte sur 17 constats issus du `challenge_report_01_GPTThink.md`.

Après consolidation (3 regroupements effectués), les décisions sont :

| Décision | Nb |
|---|---|
| `corriger_maintenant` | 8 |
| `reporter` | 4 |
| `rejeter` | 1 |
| `hors_perimetre` | 1 |

Les 8 corrections prioritaires couvrent les risques critiques et élevés : comportement de défaut face au Référentiel absent, dégradation temporelle de R, état VC unknown persistant, circuit d'escalade de dérive, garantie de chargement de la Feedback Coverage Matrix, et trois corrections modérées à fort impact moteur (AR-N3, cycle KU sans EVENT/ACTION, KU gelée en chemin critique).

---

## Périmètre analysé

- **Fichier de challenge considéré :** `work/01_challenge/challenge_report_01_GPTThink.md`
- **Core audité :** `CORE_LEARNIT_CONSTITUTION_V1_9`
- **Notes humaines :** aucune
- **Limites de périmètre :** Le Core Référentiel et le Core LINK n'étaient pas disponibles en entrée du challenge — les constats inter-Core sont traités sur la base de la Constitution seule. Les corrections impliquant une modification du Référentiel sont signalées et reportées si elles ne peuvent pas être résolues constitutionnellement.

---

## Arbitrage détaillé

---

### Point C-01 — Seuils Référentiel sans comportement de défaut constitutionnel

- **Source(s) :** C-01 (Axe 1.1)
- **Constat synthétique :** De nombreuses règles et composantes MSC délèguent leurs seuils au Référentiel sans déclarer de comportement constitutionnel de défaut si ce dernier est absent, invalide ou non chargé.
- **Nature :** logique, gouvernance, sécurité moteur
- **Gravité :** critique
- **Impact :** applicabilité, stabilité du système, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Un moteur conforme peut se retrouver en état indéfini sur des décisions critiques (reprise diagnostique, divergence MSC, profil AR-réfractaire) si le Référentiel est absent. Ce risque est constitutionnel et ne peut pas être délégué au Référentiel lui-même.
- **Conséquence attendue pour l'étape patch :** Ajouter un invariant constitutionnel déclarant que toute absence de seuil référentiel attendu déclenche obligatoirement le comportement conservateur documenté (scaffolding léger, pas d'adaptation fine, signal de correction). Cet invariant s'applique à toutes les composantes et règles dépendant de `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION`.

---

### Point C-02 — Dégradation temporelle de R non déclarée constitutionnellement

- **Source(s) :** C-02 (Axe 2.2)
- **Constat synthétique :** La composante R (robustesse temporelle) ne déclare aucun mécanisme de dégradation avec le temps. Un moteur conforme peut maintenir R à sa valeur maximale indéfiniment après une longue inactivité.
- **Nature :** logique, solidité théorique (mémoire/consolidation)
- **Gravité :** élevé
- **Impact :** applicabilité, cohérence pédagogique, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** La robustesse temporelle est un axe fondateur du MSC. Ne pas déclarer constitutionnellement que R est soumis à une décroissance temporelle laisse une liberté interprétative qui contredit la théorie sous-jacente (spacing effect, courbe d'oubli). La paramétrisation reste référentielle.
- **Conséquence attendue pour l'étape patch :** Ajouter dans `TYPE_MASTERY_COMPONENT_R` une déclaration explicite que R est soumis à une décroissance temporelle constitutive, dont les paramètres (rythme, plancher) sont bornés par le Référentiel. Ajouter un invariant `INV_R_TEMPORAL_DECAY_IS_CONSTITUTIVE` garantissant que R ne peut rester à son niveau maximal au-delà du seuil référentiel de temps sans réactivation.

---

### Point C-03 — VC persistamment unknown sans comportement défini

- **Source(s) :** C-03 (Axe 3.1)
- **Constat synthétique :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise VC à rester `unknown` indéfiniment, mais aucune règle ne définit le comportement moteur face à une VC persistamment `unknown` (différent d'une VC basse).
- **Nature :** logique, état indéfini moteur
- **Gravité :** élevé
- **Impact :** applicabilité, stabilité moteur
- **Décision :** `corriger_maintenant`
- **Justification :** La distinction entre VC basse et VC inconnue est sémantiquement correcte (`INV_VC_NOT_GENERAL_MOTIVATION_PROXY`), mais l'absence de règle sur la persistance de l'inconnu crée un angle mort moteur. Ce n'est pas un comportement de déploiement exceptionnel — un apprenant qui ne répond jamais à AR-N2 peut rester en état VC unknown indéfiniment.
- **Conséquence attendue pour l'étape patch :** Ajouter une règle `RULE_PERSISTENT_UNKNOWN_VC_TRIGGERS_NEUTRAL_FALLBACK` déclarant qu'une VC persistamment unknown au-delà du seuil référentiel déclenche une réponse neutre documentée (pas d'adaptation fine sur cet axe, pas de pénalisation, signal optionnel vers l'humain si mode non-autonome).

---

### Point C-04 — Circuit d'escalade non défini pour dérive persistante

- **Source(s) :** C-04 (Axe 5.1)
- **Constat synthétique :** `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` exige une escalade mais ne définit ni la cible, ni le délai, ni le format minimal du signal.
- **Nature :** gouvernance, traçabilité
- **Gravité :** élevé
- **Impact :** maintenabilité, applicabilité, capacité de patch/release
- **Décision :** `corriger_maintenant`
- **Justification :** Un invariant d'escalade sans attributs obligatoires est déclaratif mais non applicable techniquement. Le moteur peut générer un signal d'escalade vide ou non adressé sans violer l'invariant.
- **Conséquence attendue pour l'étape patch :** Amender `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` pour déclarer les attributs minimaux du signal d'escalade : (1) identifiant de la dérive, (2) nombre de cycles sans correction, (3) cible d'escalade (humain ou chaîne d'analyse externe). Les valeurs de seuil sont déléguées au Référentiel avec binding explicite.

---

### Point C-05 — Feedback Coverage Matrix sans garantie de chargement

- **Source(s) :** C-05 (Axe 4.1)
- **Constat synthétique :** La `TYPE_FEEDBACK_COVERAGE_MATRIX` est produite en Design mais aucun invariant ne garantit sa présence et son intégrité comme prérequis au chargement du domaine en runtime.
- **Nature :** logique, sécurité moteur
- **Gravité :** élevé
- **Impact :** applicabilité, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** Sans cette garantie, le moteur peut opérer un domaine entier en mode feedback générique permanent sans le détecter comme anormal. Ce n'est pas un état tolérable constitutionnellement.
- **Conséquence attendue pour l'étape patch :** Ajouter un invariant `INV_FEEDBACK_COVERAGE_MATRIX_REQUIRED_AT_DOMAIN_LOAD` déclarant que la présence et l'intégrité structurelle de la Feedback Coverage Matrix sont une précondition au chargement d'un domaine comportant des KU formelles ou procédurales. Absence = état interdit, chargement bloqué.

---

### Point C-07 — Cycle KU sans EVENT/ACTION de détection runtime

- **Source(s) :** C-07 (Axe 1.2)
- **Constat synthétique :** `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` déclare le cycle comme état interdit, mais aucun `EVENT_*` ni `ACTION_*` n'est associé à sa détection.
- **Nature :** structurelle, logique
- **Gravité :** modéré
- **Impact :** applicabilité, sécurité logique
- **Décision :** `corriger_maintenant`
- **Justification :** L'invariant est inopérant sans mécanisme d'application. Un cycle non détecté à la validation design peut atteindre le runtime. La correction est minimale : déclarer l'événement et l'action associés.
- **Conséquence attendue pour l'étape patch :** Ajouter `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` (trigger : validation design ou chargement ; effet : blocage) et `ACTION_BLOCK_GRAPH_LOAD` avec relation vers `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC`.

---

### Point C-09 — KU créative gelée en chemin critique sans comportement défini

- **Source(s) :** C-09 (Axe 3.3)
- **Constat synthétique :** `INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK` gèle la KU pour l'adaptation fine, mais aucune règle ne définit le comportement si la KU gelée est sur un chemin obligatoire.
- **Nature :** logique, état indéfini moteur
- **Gravité :** modéré
- **Impact :** applicabilité, stabilité moteur
- **Décision :** `corriger_maintenant`
- **Justification :** L'absence de règle expose le moteur à un état indéfini concret (KU obligatoire, gelée, pas de contournement déclaré). La correction est minimale et ne remet pas en cause l'invariant existant.
- **Conséquence attendue pour l'étape patch :** Ajouter dans `INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK` (ou dans une règle dérivée) le comportement obligatoire en chemin critique : la KU gelée bloque la progression et génère un signal de correction obligatoire ; aucun saut silencieux n'est autorisé.

---

### Point C-06 — AR-N3 orphelin sans consommation définie

- **Source(s) :** C-06 (Axe 2.3)
- **Constat synthétique :** `TYPE_SELF_REPORT_AR_N3` produit un indice de calibration auto-rapport mais aucune règle, invariant ou type ne le consomme constitutionnellement.
- **Nature :** logique, cohérence inter-documents
- **Gravité :** modéré
- **Impact :** maintenabilité, applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Un type déclaré sans consommation est soit un artefact résiduel, soit une dépendance implicite vers le Référentiel non déclarée. Les deux cas doivent être résolus. La correction est minimale : soit déclarer le binding référentiel, soit déclarer la consommation constitutionnelle.
- **Conséquence attendue pour l'étape patch :** Ajouter dans `TYPE_SELF_REPORT_AR_N3` une relation explicite vers `TYPE_STATE_AXIS_CALIBRATION` (si la consommation est constitutionnelle) ou ajouter une dépendance vers `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` avec déclaration que l'usage de l'indice AR-N3 est défini dans le Référentiel.

---

### Point C-08 — Densité cumulée AR-N* sans borne constitutionnelle

- **Source(s) :** C-08 (Axe 2.1)
- **Constat synthétique :** Les budgets d'interaction AR-N1/N2/N3 sont déclarés individuellement mais aucune contrainte ne borne la fréquence cumulée des sollicitations AR sur une session.
- **Nature :** logique, charge cognitive
- **Gravité :** modéré
- **Impact :** applicabilité, expérience apprenant
- **Décision :** `reporter`
- **Justification :** La correction nécessite de définir une sémantique inter-niveaux (N1 + N2 + N3 cumulés) qui dépasse le périmètre d'un patch minimal de la Constitution seule. Ce point est mieux traité dans un cycle de patch coordonné Constitution + Référentiel. Le risque est modéré et non bloquant en V1.9.
- **Conséquence attendue pour l'étape patch :** Aucune. À inscrire dans le backlog pour un prochain cycle de patch conjoint Constitution/Référentiel.

---

### Point C-10 — GF-08 réponse conservatrice non définie opérationnellement

- **Source(s) :** C-10 (Axe 3.2)
- **Constat synthétique :** `RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE` utilise le terme « conservatrice » sans le définir dans ce contexte, potentiellement différent de la définition dans `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`.
- **Nature :** éditoriale, logique
- **Gravité :** modéré
- **Impact :** compréhension, applicabilité
- **Décision :** `reporter`
- **Justification :** L'harmonisation terminologique est souhaitable mais ne constitue pas un risque moteur bloquant en V1.9. Les deux usages du terme sont sémantiquement proches (scaffolding léger, pas de pénalisation). Ce point peut être traité dans un cycle de patch éditorial dédié.
- **Conséquence attendue pour l'étape patch :** Aucune. À inscrire dans le backlog éditorial.

---

### Point C-11 — Profil AR-réfractaire : non-réponse sans sémantique

- **Source(s) :** C-11 (Axe 4.2)
- **Constat synthétique :** La détection du profil AR-réfractaire repose sur une fenêtre de non-réponse sans distinguer cause technique, session courte, ou refus délibéré.
- **Nature :** logique, dépendance IA implicite
- **Gravité :** modéré
- **Impact :** applicabilité, sécurité logique
- **Décision :** `reporter`
- **Justification :** La correction idéale nécessiterait de déclarer des critères de discrimination de la non-réponse qui impliquent des données de session (durée, événements) non encore spécifiées dans la Constitution. Ce point est structurellement lié à la spec du moteur de session, hors périmètre d'un patch constitutionnel minimal.
- **Conséquence attendue pour l'étape patch :** Aucune. À traiter lors de la spécification du modèle de session runtime.

---

### Point C-12 — Gamification probatoire sans condition de sortie

- **Source(s) :** C-12 (Axe 2.4)
- **Constat synthétique :** `RULE_UNVERIFIED_GAMIFICATION_PROBATION` déclare un mode probatoire sans définir les conditions de sortie.
- **Nature :** logique, gouvernance
- **Gravité :** modéré
- **Impact :** maintenabilité, applicabilité
- **Décision :** `reporter`
- **Justification :** La gamification est un périmètre optionnel non activé dans les déploiements actuels connus. La correction est souhaitable mais non urgente. Elle peut être traitée dans un patch dédié à la gouvernance de déploiement.
- **Conséquence attendue pour l'étape patch :** Aucune. À inscrire dans le backlog gouvernance déploiement.

---

### Point C-13 — Divergence MSC : seuil référentiel non garanti exister

- **Source(s) :** C-13 (Axe 1.4 partiel + Axe 1.1)
- **Constat synthétique :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` est conditionné à `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` dont l'existence dans le Référentiel n'est pas garantie constitutionnellement.
- **Nature :** logique, cohérence inter-Core
- **Gravité :** modéré
- **Impact :** applicabilité
- **Décision :** `corriger_maintenant` *(consolidé avec C-01)*
- **Justification :** Ce point est un cas particulier de C-01. La correction de C-01 (invariant de défaut référentiel) couvre également ce cas : si le paramètre est absent, le comportement conservateur s'applique. Pas de patch séparé nécessaire.
- **Conséquence attendue pour l'étape patch :** Couverte par le patch C-01.

---

### Point C-14 — Compatibilité descendante entre versions de Core

- **Source(s) :** C-14 (Axe 5.2)
- **Constat synthétique :** Aucune règle ne définit ce qui est autorisé ou interdit lors d'un upgrade majeur de version du Core.
- **Nature :** gouvernance, versioning
- **Gravité :** modéré
- **Impact :** maintenabilité, capacité de patch/release
- **Décision :** `hors_perimetre`
- **Justification :** Ce point relève de la spec du cycle de release et de la gouvernance inter-versions, qui est définie dans les stages 07 et 08 du pipeline. Il n'est pas résolvable par un patch constitutionnel sans empiéter sur le périmètre de la spec release.
- **Conséquence attendue pour l'étape patch :** Aucune. À traiter dans la spec release (STAGE_07/STAGE_08).

---

### Point C-15 — Dépendance circulaire T ↔ MasteryModel

- **Source(s) :** C-15 (Axe 1.3)
- **Constat synthétique :** `TYPE_MASTERY_COMPONENT_T` déclare `derives_from: TYPE_MASTERY_MODEL` qui lui-même dépend de T, créant une ambiguïté sur l'ordre de résolution.
- **Nature :** structurelle, éditoriale
- **Gravité :** faible
- **Impact :** compréhension
- **Décision :** `rejeter`
- **Justification :** La relation `derives_from` est de nature descriptive (T est un niveau supérieur dérivé du MSC global), pas d'instanciation. `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` clarifie déjà que T ne conditionne pas la maîtrise de base et n'est jamais un prérequis inverse. Il n'y a pas de cycle fonctionnel réel. Introduire un commentaire dans le Core serait suffisant mais n'est pas un patch YAML nécessaire.
- **Conséquence attendue pour l'étape patch :** Aucune.

---

### Point C-16 — source_anchor hétérogène ARBITRAGE_2026_04_01

- **Source(s) :** C-16 (Axe 1.4)
- **Constat synthétique :** Deux éléments portent `source_anchor: '[ARBITRAGE_2026_04_01][DIVMSC-01]'` au lieu d'une ancre `[Sxx]` normative.
- **Nature :** traçabilité, éditoriale
- **Gravité :** faible
- **Impact :** maintenabilité
- **Décision :** `reporter`
- **Justification :** Ce point est éditorial. La convention d'ancrage par arbitrage peut être délibérée pour tracer l'origine des ajouts récents. La normalisation peut être effectuée lors d'un prochain cycle éditorial une fois la convention documentée.
- **Conséquence attendue pour l'étape patch :** Aucune dans ce cycle.

---

### Point C-17 — Registre structuré des patches appliqués absent

- **Source(s) :** C-17 (Axe 5.3)
- **Constat synthétique :** La traçabilité des patches intégrés repose sur les source_anchors, pas sur un bloc structuré dans le Core.
- **Nature :** traçabilité, gouvernance
- **Gravité :** faible
- **Impact :** maintenabilité
- **Décision :** `reporter`
- **Justification :** Amélioration souhaitable mais non bloquante. À traiter dans un cycle de gouvernance documentaire dédié, potentiellement via la spec DSL patch.
- **Conséquence attendue pour l'étape patch :** Aucune dans ce cycle.

---

## Points consolidés

### Regroupements effectués

- **C-01 + C-13 :** Fusionnés. C-13 est un cas particulier de C-01 (seuil référentiel manquant). La correction de C-01 couvre C-13 intégralement.
- **C-02 seul :** Constat unique, pas de doublon identifié.
- **C-09 seul :** Constat unique, distinct de `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` (qui porte sur le déploiement autonome) — ici il s'agit du comportement en chemin obligatoire.

### Contradictions entre rapports

Aucune contradiction identifiée (un seul rapport de challenge en entrée).

---

## Décisions à transmettre au patch

| Priorité | ID constat | Titre court | Correction attendue |
|---|---|---|---|
| 1 — Critique | C-01 (+ C-13) | Défaut constitutionnel Référentiel absent | Ajouter `INV_REFERENTIEL_ABSENT_TRIGGERS_CONSERVATIVE_FALLBACK` |
| 2 — Élevé | C-02 | Dégradation temporelle de R | Amender `TYPE_MASTERY_COMPONENT_R` + ajouter `INV_R_TEMPORAL_DECAY_IS_CONSTITUTIVE` |
| 3 — Élevé | C-03 | VC unknown persistant | Ajouter `RULE_PERSISTENT_UNKNOWN_VC_TRIGGERS_NEUTRAL_FALLBACK` |
| 4 — Élevé | C-04 | Circuit d'escalade dérive persistante | Amender `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` |
| 5 — Élevé | C-05 | Feedback Coverage Matrix chargement | Ajouter `INV_FEEDBACK_COVERAGE_MATRIX_REQUIRED_AT_DOMAIN_LOAD` |
| 6 — Modéré | C-07 | Cycle KU sans détection runtime | Ajouter `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` + `ACTION_BLOCK_GRAPH_LOAD` |
| 7 — Modéré | C-09 | KU gelée en chemin critique | Amender `INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK` |
| 8 — Modéré | C-06 | AR-N3 orphelin | Ajouter binding explicite dans `TYPE_SELF_REPORT_AR_N3` |

**Contraintes de minimalité :**
- Chaque correction doit rester dans le périmètre Constitution ; aucune modification du Référentiel n'est attendue dans ce patch.
- Les nouveaux invariants et règles doivent respecter la séparation Constitution (quoi/pourquoi) / Référentiel (combien/comment).
- Les seuils numériques restent exclusivement dans le Référentiel.
- Pas de refonte des sections existantes : les corrections sont des ajouts ou des amendements ciblés.

---

## Décisions explicitement non retenues

| ID | Titre court | Décision | Justification |
|---|---|---|---|
| C-08 | Densité AR cumulée | `reporter` | Nécessite spec inter-niveaux AR + Référentiel. Non bloquant V1.9. |
| C-10 | GF-08 conservatrice non définie | `reporter` | Risque éditorial faible, pas de blocage moteur. Cycle éditorial dédié. |
| C-11 | AR-réfractaire sans sémantique | `reporter` | Lié à spec session runtime hors périmètre constitutionnel. |
| C-12 | Gamification probatoire sans sortie | `reporter` | Périmètre optionnel non activé. Backlog gouvernance déploiement. |
| C-14 | Compatibilité descendante versions | `hors_perimetre` | Relève spec release STAGE_07/08. |
| C-15 | Dépendance circulaire T ↔ MasteryModel | `rejeter` | Relation descriptive, pas fonctionnelle. Invariant existant suffisant. |
| C-16 | source_anchor hétérogène | `reporter` | Éditorial. Convention arbitrage potentiellement délibérée. |
| C-17 | Registre patches absent | `reporter` | Amélioration gouvernance non urgente. Scope DSL patch. |
