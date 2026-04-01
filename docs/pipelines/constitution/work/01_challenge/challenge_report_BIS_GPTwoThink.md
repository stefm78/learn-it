# CHALLENGE REPORT — Constitution Learn-it v1.9

**ID rapport :** challenge_report_BIS_GPTwoThink  
**Auteur :** GPTwoThink  
**Date :** 2026-04-01  
**Cores analysés :**
- `CORE_LEARNIT_CONSTITUTION_V1_9` (version V1_9_FINAL)
- `CORE_LEARNIT_REFERENTIEL_V1_0` (version V1_0_FINAL)
- LINK (non fourni dans ce run ; voir note en Axe 1)

---

## Résumé exécutif

Le système est globalement solide sur ses fondations constitutionnelles. La séparation Constitution/Référentiel est bien respectée, la contrainte locale est tenue, et les derniers patchs (V1_9, V1_0) ont comblé plusieurs angles morts antérieurs (KU sans type, états inconnus, propagation secondaire). Néanmoins, six zones de risque matérielles sont identifiées :

1. **LINK absent de l'analyse** — le LINK n'a pas été fourni en input ; les problèmes de binding inter-Core ne peuvent pas être vérifiés exhaustivement (risque de gouvernance).
2. **Moteur conservateur sans sortie définie** — la règle `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` génère un scaffolding léger indéfiniment sans mécanisme d'escalade constitutionnellement borné, hormis `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` récemment introduit dans le Référentiel, mais sans EVENT associé dans la Constitution.
3. **Divergence MSC/perçu nouvellement couverte mais incomplète** — `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` et `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` sont bien présents (patch ARBITRAGE_2026_04_01), mais l'escalade au design du contenu (Étape 2) n'est pas reliée à un EVENT explicite, ce qui rend son déclenchement dépendant d'une décision hors-spec.
4. **SIS sous-défini en pratique** — `TYPE_SESSION_INTEGRITY_SCORE` est déclaré comme type constitutionnel mais aucun proxy ou méthode de calcul minimal n'est bornée côté Référentiel, exposant le moteur à une indétermination technique.
5. **ICC (Indice de confiance corpus) sans chemin de décision** — `TYPE_CORPUS_CONFIDENCE_ICC` est déclaré mais aucune règle ni invariant ne spécifie ce que le moteur doit faire si ICC est bas.
6. **Régime adaptatif conflict resolution partiel** — `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (arbitrage 2026-04-01) couvre les conflits 2-régimes mais ne documente pas les cas de 3+ régimes simultanés.

---

## Analyse détaillée par axe

---

### Axe 1 — Cohérence interne

#### A1-01 — LINK absent (gouvernance)
**Élément :** Toutes les liaisons inter-Core  
**Nature :** Le LINK n'a pas été fourni. Les `source_anchor: [INTERCORE]` dans la Constitution et le Référentiel garantissent l'existence de références croisées, mais les bindings effectifs ne peuvent pas être audités.  
**Type de problème :** Gouvernance / complétude  
**Impact moteur :** Impossible de vérifier que tous les `depends_on` inter-Core sont résolus dans le LINK, ni que les PARAM référentiels utilisés dans les RULE constitutionnelles sont correctement exposés.  
**Correction à arbitrer :** Fournir le LINK dans les inputs du Stage 01 pour tout run de challenge ultérieur.

#### A1-02 — EVENT manquant pour escalade conservateur prolongé (Constitution)
**Élément :** `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` + `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`  
**Nature :** Le paramètre `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` (Référentiel, source ARBITRAGE_2026_04_01 MOT-01) définit un seuil d'escalade, mais la Constitution ne déclare aucun `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` correspondant. L'escalade n'est donc pas traçable comme événement moteur.  
**Type de problème :** Cohérence interne / complétude  
**Impact moteur :** Le moteur peut rester indéfiniment en mode conservateur sans signal formalisé vers la chaîne de supervision hors session.  
**Correction à arbitrer :** Ajouter `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans la Constitution, lié au paramètre Référentiel, pour fermer la boucle d'escalade.

#### A1-03 — Escalade Étape 2 du protocole DIVMSC sans EVENT (Constitution)
**Élément :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` — Étape 2  
**Nature :** L'effet de l'Étape 2 (escalade vers révision du design du contenu — notification externe obligatoire) est décrit dans la `logic.effect` de la règle mais aucun `EVENT` ni `ACTION` constitutionnel ne le matérialise. La Constitution déclare `ACTION_INFORM_LEARNER` pour la transparence, mais aucun équivalent pour la notification externe design.  
**Type de problème :** Cohérence interne / complétude  
**Impact moteur :** L'escalade design est présente textuellement mais ne constitue pas un événement traçable, ce qui rend la supervision hors session fragile.  
**Correction à arbitrer :** Créer un `ACTION_ESCALATE_TO_DESIGN_REVISION` dans la Constitution (scope: design_governance), référencé par `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`.

#### A1-04 — Paramètres orphelins dans la Constitution (Constitution)
**Élément :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`  
**Nature :** Ce paramètre est déclaré constitutionnel (`source_anchor: [S2][S20]`) mais aucune règle ni invariant dans la Constitution ne le consomme explicitement. Il n'est pas non plus visible dans les `depends_on` des règles de reprise diagnostique.  
**Type de problème :** Cohérence interne (paramètre orphelin)  
**Impact moteur :** La fenêtre de vérification de maîtrise provisoire est déclarée mais non opérationnelle ; le moteur ne sait pas quand la déclencher.  
**Correction à arbitrer :** Lier `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` à une règle constitutionnelle existante (ex. `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`) ou créer `RULE_PROVISIONAL_MASTERY_WINDOW_EXPIRES`.

#### A1-05 — Mauvais placement d'un concept opérationnel (Constitution/Référentiel)
**Élément :** `TYPE_SESSION_INTEGRITY_SCORE` (Constitution)  
**Nature :** Ce type est constitutionnel mais son calcul pratique (méthode, proxys acceptés) n'est pas bornée dans le Référentiel. Contrairement au MSC (seuils dans le Référentiel), le SIS n'a aucun bloc paramétrique équivalent dans le Référentiel.  
**Type de problème :** Mauvais placement (complétude Référentiel)  
**Impact moteur :** Le calcul du SIS est indéterminé en pratique ; son effet (pondération ou mise en attente MSC) ne peut pas être appliqué de façon reproductible.  
**Correction à arbitrer :** Ajouter un `TYPE_REFERENTIEL_SIS_PARAMETER_BLOCK` dans le Référentiel avec au moins un proxy minimal et un seuil de référence.

---

### Axe 2 — Solidité théorique

#### Charge cognitive
**Point solide :** `PARAM_REFERENTIEL_COGNITIVE_FATIGUE_MINUTES_GUARDRAIL` (25 min) fournit un garde-fou explicite.  
**Zone de risque :** Ce garde-fou est déclaré comme "dernier recours" sans que la chaîne d'actions préventives soit formalisée avant ce seuil.  
**Angle mort :** Aucune gestion de la charge cognitive intra-tâche (KU longues, ex. créative 5–15 min : une seule KU peut consommer 60% du garde-fou sans signal intermédiaire).

#### Mémoire / consolidation
**Point solide :** La composante R avec multiplicateurs différenciés par type de KU est bien fondée (spacing effect). La distinction rétrogradation courante vs révocation post-maîtrise (`RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`) est théoriquement correcte.  
**Zone de risque :** Le multiplicateur R pour KU créative est fixé à ×1 (fallback constitutionnel). Cela signifie qu'une KU créative bénéficiera du même délai de robustesse qu'une KU sans multiplicateur, ce qui est discutable : les productions créatives peuvent nécessiter un délai plus long pour confirmer la consolidation.  
**Angle mort :** Aucune règle de consolidation pour les KU interleaved n'est documentée — il n'est pas précisé comment R est évalué pour des KU apprises via interleaving (qui peut compresser les répétitions temporelles).

#### Motivation
**Point solide :** La séparation VC / activation / détresse est bien fondée sur la théorie attente-valeur (Eccles) et le modèle de contrôle-valeur (Pekrun).  
**Zone de risque :** `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH` déclenche un patch relevance, mais ne distingue pas la VC basse liée à la valeur perçue de la tâche vs. la VC basse liée au coût perçu trop élevé. Ces deux cas appellent des réponses pédagogiques différentes.  
**Angle mort :** L'axe VC est optionnel (`TYPE_STATE_AXIS_VALUE_COST` : condition "Item VC de AR-N2 renseigné") — en contexte déployé sans AR-N2 complet, la motivation n'est pas modélisée du tout.

#### Métacognition / SRL
**Point solide :** La hiérarchie AR-N1/N2/N3 et l'intention de session sont alignées avec les phases forethought/performance/self-reflection du modèle Zimmerman.  
**Zone de risque :** L'intention de session est explicitement "non bloquante et non pénalisée" (`RULE_SESSION_INTENTION_NON_BLOCKING`) — mais aucune règle ne précise comment elle influence la planification de session, hormis "support de forethought SRL". Son impact moteur concret est absent.  
**Angle mort :** AR-N3 (bilan périodique dérivé d'AEQ) alimente un "indice de calibration auto-rapport" mais l'effet précis de cet indice sur le moteur n'est documenté que via `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`, ce qui ne couvre que le cas de calibration basse. Le cas de calibration élevée stable n'a aucun effet déclaré.

#### Émotions / engagement
**Point solide :** La distinction confusion/frustration/anxiété dans AR-N1 est bien fondée (modèle AEQ/Pekrun). La réponse conservatrice en l'absence d'AR-N1 évite les réponses punitives.  
**Zone de risque :** `TYPE_STATE_AXIS_ACTIVATION` distingue productif/détresse/sous-défi mais le moteur n'a aucune règle de transition définie entre ces états — comment passe-t-on de "détresse" à "productif" ? Le scaffolding léger réversible est déclenché, mais aucun critère de résolution de la détresse n'est déclaré constitutionnellement.  
**Angle mort :** L'ennui (sous-défi prolongé) est détecté dans la matrice des régimes adaptatifs Référentiel, mais il n'existe pas de règle constitutionnelle propre à l'ennui prolongé (uniquement couvert par la matrice 3×3 du Référentiel).

#### Mastery learning
**Point solide :** Le AND strict sur P×R×A est une implémentation robuste du mastery learning (Bloom, 1968). La séparation de T (transférabilité) est théoriquement solide.  
**Zone de risque :** La composante A (autonomie, 3 réussites consécutives sans aide) peut être atteinte dans une fenêtre temporelle très courte si une session concentre beaucoup de tâches. Sans contrainte temporelle minimale sur A, une maîtrise déclarée peut être superficielle.  
**Angle mort :** Le mastery learning suppose une granularité de KU suffisante pour que les seuils aient du sens. La Constitution ne contraint pas la taille minimale d'une KU, laissant des KU trop larges potentiellement déclarées maîtrisées trop tôt.

#### Ingénierie pédagogique
**Point solide :** La phase Analyse (graphe, contexte authentique, ICC, Bloom) est bien structurée. La contrainte Bloom ≥ 4 → contexte authentique obligatoire est correcte.  
**Zone de risque :** La `TYPE_FEEDBACK_COVERAGE_MATRIX` est un livrable obligatoire pour les KU formelles ou procédurales, mais la Constitution ne spécifie pas ce qui se passe si elle est incomplète (seuil Référentiel 70%, mais en dessous de ce seuil, le signal est "révision prioritaire" — non bloquant).  
**Angle mort :** Aucune contrainte sur la cohérence pédagogique entre les KU d'un même graphe — deux KU voisines peuvent avoir des niveaux Bloom très éloignés sans que le moteur le signale comme incohérence de design.

---

### Axe 3 — États indéfinis moteur

#### EI-01 — Oscilation en mode conservateur sans sortie
**Scénario :** AR-N1 constamment absent sur 10+ sessions. Le moteur déclenche `ACTION_APPLY_LIGHT_REVERSIBLE_SCAFFOLDING` indéfiniment. Le Référentiel prévoit une escalade après N sessions (`PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`), mais l'EVENT n'est pas dans la Constitution — voir A1-02.  
**Risque moteur :** Blocage soft : l'apprenant reçoit un scaffolding léger en boucle sans progression ni signal de révision.

#### EI-02 — Conflit non résolu entre SIS bas et MSC valide
**Scénario :** L'apprenant a P×R×A satisfaits (maîtrise déclarée) mais SIS bas sur la même session. `TYPE_SESSION_INTEGRITY_SCORE` permet une "pondération ou mise en attente" de l'intégration des performances (`RULE_LOW_SIS_NEVER_AUTO_PENALIZES`). Le moteur est-il supposé confirmer la maîtrise ou attendre une prochaine session de confirmation ?  
**Risque moteur :** Indétermination : la mise en attente n'a pas de durée définie ni de condition de levée dans la Constitution.

#### EI-03 — ICC bas et déploiement autorisé
**Scénario :** Le corpus d'entrée a un ICC bas (`TYPE_CORPUS_CONFIDENCE_ICC`). Aucune règle ne bloque le déploiement dans ce cas. Le moteur peut être déployé sur un graphe de faible confiance sans signal clair.  
**Risque moteur :** Le moteur fonctionne avec un graphe de KU potentiellement mal défini sans avertissement visible à l'usage.

#### EI-04 — Interleaving et gestion R simultanée
**Scénario :** Deux KU en interleaving ont des multiplicateurs R différents (ex. déclarative ×1 et procédurale ×2–3). Lors d'une rétrogradation MSC sur la KU déclarative, les KU procédurales dépendantes ont-elles leur R recalculé ? Aucune règle ne le précise.  
**Risque moteur :** Perte d'information sur la robustesse des KU mêlées dans l'interleaving lors d'un événement de rétrogradation.

---

### Axe 4 — Dépendances IA implicites

#### IA-01 — Détection de misconception sans corpus structuré
**Élément :** `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` — déclenché par "KU flaggée misconception"  
**Problème :** Le flagging de misconception n'est pas défini constitutionnellement — qui décide qu'une KU est une misconception ? Si cette décision dépend d'une inférence sémantique sur les réponses apprenantes, elle viole `INV_RUNTIME_FULLY_LOCAL`.  
**Alternative sans IA continue :** Le flag misconception doit être déclaré statiquement au moment du design du graphe (phase Analyse), non inféré dynamiquement. Renforcer via contrainte constitutionnelle explicite.

#### IA-02 — Couverture de la matrice de feedback
**Élément :** `TYPE_FEEDBACK_COVERAGE_MATRIX` — "patterns d'erreurs couverts"  
**Problème :** La correspondance entre une erreur réelle et un template de feedback nécessite une classification de l'erreur. Si cette classification est sémantique (ex. reconnaissance d'une erreur de raisonnement par inspection de la réponse libre), elle implique une inférence continue.  
**Alternative sans IA continue :** Restreindre les feedbacks couvrables aux erreurs formellement codifiables (réponses à choix, patterns syntaxiques). Les erreurs ouvertes → `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK` est déjà prévue ; s'assurer que les KU ouvertes sont systématiquement categorisées comme telles au design.

#### IA-03 — Calcul de l'ICC
**Élément :** `TYPE_CORPUS_CONFIDENCE_ICC`  
**Problème :** "Corpus d'entrée évalué" — l'évaluation de la qualité d'un corpus implique potentiellement une analyse sémantique du contenu (cohérence, couverture, fiabilité). Cette analyse est faite hors session (phase Analyse), ce qui est acceptable, mais la méthode n'est pas définie.  
**Risque :** Si l'ICC est calculé par IA générative hors session, cela reste compatible avec `INV_RUNTIME_FULLY_LOCAL`, mais la traçabilité de l'ICC doit être garantie (artefact signé, non recalculé à la volée).  
**Alternative :** Définir l'ICC comme un score structuré à déclarer explicitement par le concepteur pédagogique après analyse, non inféré automatiquement.

---

### Axe 5 — Gouvernance

#### G-01 — Absence de versioning explicite des PARAM entre Constitution et Référentiel
**Élément :** `depends_on: [REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION]` dans de nombreux types  
**Nature :** La référence inter-Core est fixée à une version précise (V1_0). En cas de patch du Référentiel vers V1_1, cette référence devient stale sans mécanisme de mise à jour automatique déclaré.  
**Type de problème :** Gouvernance / versioning  
**Impact moteur :** Incertitude sur la version effective du Référentiel utilisée en runtime si un patch Référentiel intervient sans mise à jour coordonnée de la Constitution.  
**Correction à arbitrer :** Définir une politique explicite de compatibilité inter-Core dans le LINK ou la Constitution (semver-like : patch Référentiel rétrocompatible = pas de mise à jour Constitution nécessaire ; breaking change = mise à jour obligatoire des références).

#### G-02 — Invariants protégés mais non auditables sans LINK
**Élément :** `INV_CONSTITUTION_REFERENTIAL_SEPARATION`  
**Nature :** Cet invariant est bien déclaré mais son respect ne peut être vérifié mécaniquement que via le LINK (bindings inter-Core). En l'absence du LINK dans ce run, l'invariant est supposé respecté sans preuve.  
**Type de problème :** Gouvernance / traçabilité  
**Impact moteur :** Risque de dérive silencieuse si un patch Référentiel introduit une logique qui devrait être constitutionnelle.

#### G-03 — `patchable: false` sur des éléments qui pourraient nécessiter évolution
**Élément :** `INV_GRAPH_PROPAGATION_ONE_HOP`, `INV_MSC_AND_STRICT`  
**Nature :** Ces invariants sont légitimement protégés. Cependant, l'absence de tout mécanisme de révision constitutionnelle formelle (un "Constitutional Amendment Process") signifie que si la théorie évolue (ex. propagation 2-sauts justifiée empiriquement), la seule voie est un Core entièrement nouveau. Cette rigidité est un choix de gouvernance, mais elle n'est pas documentée.  
**Type de problème :** Gouvernance  
**Correction à arbitrer :** Documenter explicitement le processus de révision constitutionnelle (nouveau Core, non patch), au moins comme note dans la Constitution.

---

### Axe 6 — Scénarios adversariaux

#### SA-01 — Apprenant fantôme (AR-N1 systématiquement absent, SIS faible)
**Description :** Un apprenant complète toutes les tâches sans jamais répondre aux AR-N1, avec un SIS faible (comportements ambigus). Il atteint P et A en session unique intensive.  
**Mécanismes activés :** `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` + `TYPE_SESSION_INTEGRITY_SCORE` + `INV_MSC_AND_STRICT`  
**Limite révélée :** La maîtrise peut être déclarée via P et A sur une session unique avec SIS bas, l'attente étant "possible" mais non obligatoire. R reste le seul garde-fou temporel, mais si les sessions sont rapprochées dans les bornes R, une maîtrise fragile est validée. L'axe A (3 réussites consécutives) ne contraint pas la fenêtre temporelle minimale — voir Axe 2.

#### SA-02 — Graphe très plat (peu de dépendances explicites)
**Description :** Un concepteur pédagogique crée un graphe avec 50 KU mais peu d'arêtes de dépendance. Toutes les KU sont déclarées indépendantes.  
**Mécanismes activés :** `INV_EXPLICIT_DEPENDENCY_EDGES_REQUIRED` + `RULE_MSC_DOWNGRADE_MARKS_DEPENDENTS` + `INV_GRAPH_PROPAGATION_ONE_HOP`  
**Limite révélée :** `INV_EXPLICIT_DEPENDENCY_EDGES_REQUIRED` interdit la propagation si les arêtes sont absentes — correct — mais le moteur ne signale pas qu'un graphe plat est pédagogiquement suspect. Un graphe sans dépendances est valide structurellement mais peut trahir un design Analyse de mauvaise qualité. Aucune règle ne détecte un ICC de graphe (degré de connectivité faible).

#### SA-03 — Patch relevance VC en boucle
**Description :** Un apprenant a VC basse persistante. Le patch relevance est déclenché (cycle 1), amélioration absente. Deuxième cycle : escalade Analyse signalée (`RULE_REFERENTIEL_VC_PATCH_ESCALATION_AFTER_TWO_CYCLES`). L'équipe ne peut pas intervenir (contrainte externe). Le moteur continue : troisième dérive VC.  
**Mécanismes activés :** `EVENT_PERSISTENT_LOW_VC` + `RULE_REFERENTIEL_VC_PATCH_ESCALATION_AFTER_TWO_CYCLES` + `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`  
**Limite révélée :** `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` prévoir une escalade hors session, mais aucune règle ne définit le comportement moteur pendant l'attente de l'escalade (continuation à l'identique? mode conservateur? suspension?). L'apprenant peut être exposé à un contenu dont le problème de pertinence est connu et non traité.

---

### Axe 7 — Priorisation

| Priorité | ID | Titre court |
|---|---|---|
| **Critique** | A1-02 / EI-01 | EVENT escalade conservateur absent dans la Constitution |
| **Critique** | EI-02 | SIS bas + MSC valide : indétermination de mise en attente |
| **Élevé** | A1-03 | ACTION escalade design DIVMSC Étape 2 non matérialisée |
| **Élevé** | A1-05 | SIS sans bloc paramétrique dans le Référentiel |
| **Élevé** | IA-01 | Flagging misconception : risque inférence runtime |
| **Élevé** | SA-03 | Comportement moteur pendant attente escalade VC non défini |
| **Modéré** | A1-04 | PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW orphelin |
| **Modéré** | EI-03 | ICC bas sans blocage de déploiement |
| **Modéré** | EI-04 | R de KU interleaved lors de rétrogradation non défini |
| **Modéré** | SA-01 | Maîtrise possible sans contrainte temporelle sur composante A |
| **Modéré** | G-01 | Versioning inter-Core sans politique de compatibilité |
| **Faible** | A1-01 | LINK absent de ce run |
| **Faible** | SA-02 | Graphe plat pédagogiquement suspect sans signal moteur |
| **Faible** | G-02 | Invariants non auditables sans LINK |
| **Faible** | G-03 | Absence de processus de révision constitutionnelle documenté |

---

## Risques prioritaires

### CRITIQUE — EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION manquant
**Éléments :** `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`, `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`  
**Nature :** Incohérence interne — le Référentiel prévoit un seuil d'escalade, la Constitution ne déclare pas l'événement associé.  
**Type :** Cohérence interne / complétude  
**Impact moteur :** Apprenant en mode scaffolding indéfini sans supervision.  
**Correction à arbitrer :** Ajouter `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` en Constitution (scope: runtime_state), déclenché par `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` + seuil Référentiel. L'action associée pourrait réutiliser `ACTION_INFORM_LEARNER` + une nouvelle `ACTION_ESCALATE_TO_SUPERVISION`.

---

### CRITIQUE — Indétermination SIS bas + MSC valide
**Éléments :** `TYPE_SESSION_INTEGRITY_SCORE`, `RULE_LOW_SIS_NEVER_AUTO_PENALIZES`, `INV_MSC_AND_STRICT`  
**Nature :** La "mise en attente possible" n'est pas définie dans la durée ni dans les conditions de levée.  
**Type :** État indéfini moteur  
**Impact moteur :** Maîtrise déclarée ou indéterminée selon implémentation — non reproductible.  
**Correction à arbitrer :** Ajouter dans la Constitution une règle `RULE_SIS_LOW_MASTERY_PENDING` définissant : (1) la durée de mise en attente (1 session par défaut, paramétrable Référentiel), (2) la condition de levée (SIS ≥ seuil sur session suivante → confirmation ; SIS encore bas → rétrogradation préventive).

---

### ÉLEVÉ — ACTION_ESCALATE_TO_DESIGN_REVISION absente
**Éléments :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` (Étape 2)  
**Nature :** L'escalade design est décrite dans l'effet d'une règle mais non matérialisée comme ACTION constitutionnelle.  
**Type :** Complétude  
**Impact moteur :** L'escalade design n'est pas traçable, auditable ni déclenchable de façon déterministe.  
**Correction à arbitrer :** Créer `ACTION_ESCALATE_TO_DESIGN_REVISION` dans la Constitution, référencée par `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` Étape 2.

---

## Corrections à arbitrer avant patch

| # | Élément concerné | Nature du problème | Type | Impact moteur | Correction proposée |
|---|---|---|---|---|---|
| C-01 | Constitution — manque `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` | Incohérence interne | Complétude | Scaffolding indéfini | Ajouter EVENT + ACTION_ESCALATE_TO_SUPERVISION |
| C-02 | Constitution — `RULE_SIS_LOW_MASTERY_PENDING` absente | État indéfini | Implémentabilité | Maîtrise non reproductible | Ajouter règle avec durée et condition de levée |
| C-03 | Constitution — `ACTION_ESCALATE_TO_DESIGN_REVISION` absente | Complétude | Gouvernance | Escalade non traçable | Créer ACTION, lier à DIVMSC protocole Étape 2 |
| C-04 | Référentiel — `TYPE_REFERENTIEL_SIS_PARAMETER_BLOCK` absent | Mauvais placement | Implémentabilité | Calcul SIS indéterminé | Ajouter bloc paramétrique SIS dans Référentiel |
| C-05 | Constitution — `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` orphelin | Paramètre orphelin | Complétude | Fenêtre provisoire inactive | Lier à une règle constitutionnelle existante ou nouvelle |
| C-06 | Constitution — Flagging misconception non borné | Dépendance IA implicite | Implémentabilité | Risque inférence runtime | Contraindre le flagging au design statique dans la Constitution |
| C-07 | Constitution/Référentiel — Comportement moteur pendant attente escalade VC non défini | État indéfini | Implémentabilité | Apprenant exposé à contenu problématique connu | Ajouter règle de comportement pendant la période d'attente escalade |
| C-08 | Constitution — Composante A sans contrainte temporelle minimale | Solidité théorique | Théorique | Maîtrise superficielle possible | Étudier l'ajout d'une fenêtre minimale inter-sessions pour A |
| C-09 | Gouvernance — Politique de compatibilité versioning inter-Core absente | Gouvernance | Gouvernance | Référence stale possible | Définir politique semver minimale dans le LINK ou Constitution |

---

*Rapport produit conformément au prompt `Challenge_constitution.md` — Aucun patch YAML n'est proposé dans ce rapport.*
