# ARBITRAGE — Constitution Pipeline STAGE_02_ARBITRAGE

<!-- stage: STAGE_02_ARBITRAGE -->
<!-- arbitre: Perplexity / Claude Sonnet 4.6 -->
<!-- date: 2026-04-01 -->
<!-- pipeline: constitution v1 -->

---

## Résumé exécutif

L'arbitrage consolide les constats issus de quatre rapports de challenge adversariaux sur `CORE_LEARNIT_CONSTITUTION_V1_9` et `CORE_LEARNIT_REFERENTIEL_V1_0`. Après déduplication et qualification, **18 points distincts** ont été identifiés et arbitrés.

| Décision | Nombre |
|---|---|
| `corriger_maintenant` | 10 |
| `reporter` | 4 |
| `rejeter` | 2 |
| `hors_perimetre` | 2 |

Les corrections immédiates couvrent les trois défaillances systémiques les plus critiques : (1) l'absence de fallback constitutionnel pour les seuils Référentiel non fournis, (2) le comportement indéfini du AND strict MSC en cas de composante non calculable, et (3) l'absence de borne sur les états oscillatoires des règles de régime et de divergence MSC. Les reports concernent des problèmes de gouvernance inter-Core (versioning, LINK) qui nécessitent un chantier dédié. Les rejets concernent des constats de faible impact ou relevant exclusivement de la lisibilité.

---

## Périmètre analysé

### Fichiers challenge considérés

- `challenge_report_01_ClaudeWoThink.md` — Auditeur : Claude sans thinking étendu
- `challenge_report_01_GPTThink.md` — Auditeur : GPT adversarial
- `challenge_report_01_sonar.md` — Auditeur : Sonar adversarial
- `challenge_report_GPTwoThink.md` — Auditeur : GPTwoThink

### Notes humaines

Aucune note humaine d'arbitrage fournie.

### Limites de périmètre

- Le Core LINK (`link.yaml`) n'était pas disponible dans le corpus analysé par les challengers. Les constats relatifs au LINK sont traités avec cette limite.
- Le périmètre d'arbitrage se restreint à `CORE_LEARNIT_CONSTITUTION_V1_9` et `CORE_LEARNIT_REFERENTIEL_V1_0`.

---

## Points consolidés

### Regroupements effectués

**GROUPE A — Fallback Référentiel absent / seuils non fournis**
Sources convergentes : ClaudeWoThink (HIGH-02, A1-4), GPTThink (C-01, 1.1), Sonar (RISK-03), GPTwoThink (F-1.3, 1.3). Ce groupe est le plus convergent (4/4 rapports). Il est traité comme un unique point ARB-01.

**GROUPE B — AND strict MSC avec composante non calculable**
Sources convergentes : Sonar (RISK-02), GPTwoThink (F-2.2, 2.2). Convergence 2/4. Traité comme ARB-02.

**GROUPE C — États oscillatoires non bornés**
Deux sous-problèmes fusionnés :
- Boucle diagnostique MSC divergence non bornée : GPTwoThink (F-1.4), GPTThink mention, ClaudeWoThink (A1-4).
- Régime oscillatoire `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` sans compteur de cycles : ClaudeWoThink (A1-4).
Traité comme ARB-03 (constitution) et ARB-04 (référentiel).

**GROUPE D — Comportement multi-axes `unknown` simultanés**
Sources convergentes : Sonar (RISK-01), GPTThink (C-03, 3.1). Convergence 2/4. Traité comme ARB-05.

**GROUPE E — Escalade détresse activation chronique**
Sources convergentes : Sonar (RISK-06), GPTThink évoqué indirectement. Convergence 2/4. Traité comme ARB-06.

**GROUPE F — Cycle graphe post-patch**
Sources convergentes : GPTwoThink (F-1.2), GPTThink (C-07). Convergence 2/4. Traité comme ARB-07.

**GROUPE G — EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION non déclaré**
Source unique : ClaudeWoThink (HIGH-02). Traité comme ARB-08.

**GROUPE H — AR-N3 orphelin**
Sources convergentes : GPTThink (C-06), GPTwoThink (2.3 indirectement). Convergence 2/4. Traité comme ARB-09.

**GROUPE I — Misconception flagging : risque d'inférence runtime**
Sources convergentes : Sonar (RISK-05), GPTwoThink (F-4.1). Convergence 2/4. Traité comme ARB-10.

**GROUPE J — Versioning inter-Core et compatibilité descendante**
Sources convergentes : Sonar (RISK-03), GPTwoThink (F-5.3), GPTThink (5.2). Convergence 3/4. Chantier structurel, traité comme ARB-11 (report).

**GROUPE K — Gouvernance LINK dans la Constitution**
Sources convergentes : ClaudeWoThink (CRIT-01), Sonar (RISK-09). Convergence 2/4. Traité comme ARB-12 (report).

**GROUPE L — Gamification probatoire sans condition de sortie**
Source unique : GPTThink (C-12). Traité comme ARB-13.

**GROUPE M — Densité cumulée AR-N* par session**
Sources convergentes : GPTThink (C-08), GPTwoThink (F-2.1). Convergence 2/4. Traité comme ARB-14.

**GROUPE N — INV_TRANSFER orphelin dans les relations TYPE_MASTERY_MODEL**
Source unique : GPTwoThink (F-1.1). Traité comme ARB-15.

**GROUPE O — Feedback Coverage Matrix : non obligatoire pour KU perceptuelles**
Source unique : GPTwoThink (F-2.4). Traité comme ARB-16.

**GROUPE P — source_anchor hétérogène ARBITRAGE_2026_04_01**
Sources convergentes : GPTThink (C-16), Sonar (RISK-08). Convergence 2/4. Traité comme ARB-17.

**GROUPE Q — Dégradation R non déclarée constitutionnellement**
Sources convergentes : GPTThink (C-02), GPTwoThink (F-2.2 partiellement). Convergence 2/4. Traité comme ARB-18.

### Contradictions éventuelles résolues

- Sur le scope du AND strict MSC : ClaudeWoThink ne soulève pas ce point ; Sonar et GPTwoThink convergent. Décision retenue : ARB-02 est retenu sur la base de la convergence et de la criticité technique.
- Sur la gravité des seuils Référentiel sans fallback : GPTThink classe C-01 comme critique, GPTwoThink également, Sonar comme élevé, ClaudeWoThink comme élevé. Décision : critique retenu (majorité).

---

## Arbitrage détaillé

### ARB-01 — Fallback constitutionnel pour seuils Référentiel absents

- **Source(s) :** ClaudeWoThink (HIGH-02 partiel), GPTThink (C-01 / 1.1), Sonar (RISK-03), GPTwoThink (F-1.3 / 1.3)
- **Constat synthétique :** De nombreuses règles et événements constitutionnels délèguent leurs seuils de déclenchement au Référentiel sans définir de comportement constitutionnel de fallback si le Référentiel est absent, invalide ou ne fournit pas le paramètre attendu. Les éléments concernés incluent `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`, `EVENT_PERSISTENT_LOW_VC`, `EVENT_AR_REFRACTORY_PROFILE_DETECTED`, `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`.
- **Nature :** logique / séparation des couches / sécurité moteur
- **Gravité :** critique
- **Impact :** applicabilité — le moteur peut rester en état indéfini ou ne jamais déclencher une règle de sécurité critique si le Référentiel est manquant ou incomplet.
- **Décision :** `corriger_maintenant`
- **Justification :** Convergence 4/4 rapports. Risque d'état indéfini sur des décisions critiques pour l'apprenant. Correction minimale possible : ajouter un invariant constitutionnel prescrivant le comportement conservateur documenté en absence de seuil Référentiel (= ne pas déclencher la règle dépendante, maintenir le dernier état sûr connu).
- **Conséquence pour le patch :** Ajouter `INV_REFERENTIEL_PARAM_MISSING_SAFE_FALLBACK` dans la Constitution : si un paramètre Référentiel requis par une règle ou un événement constitutionnel est absent ou non résolvable, le moteur applique le comportement conservateur et ne déclenche pas la règle dépendante. Scope : `governance / runtime_evaluation`.

---

### ARB-02 — AND strict MSC avec composante non calculable (R en première session)

- **Source(s) :** Sonar (RISK-02 / 3.2), GPTwoThink (F-2.2 / 2.2)
- **Constat synthétique :** `INV_MSC_AND_STRICT` suppose que P, R, A sont toutes calculables. En première session ou en absence de données temporelles, R ne peut être calculé. La Constitution ne définit pas si la maîtrise est alors `false`, `unknown` ou `deferred`. Ce comportement indéfini peut provoquer des oscillations de trajectoire selon l'implémentation.
- **Nature :** logique / état moteur indéfini
- **Gravité :** critique
- **Impact :** applicabilité / stabilité moteur — les implémentations divergeront sans décision constitutionnelle claire.
- **Décision :** `corriger_maintenant`
- **Justification :** Convergence 2/4 mais criticité élevée et vide structurel avéré dans l'invariant. Correction minimale : préciser dans un invariant complémentaire ou dans `INV_MSC_AND_STRICT` que si une composante P, R ou A est `unknown` (non calculable faute de données), la maîtrise est `deferred` (non accordée, non révoquée) jusqu'à ce que la composante soit calculable.
- **Conséquence pour le patch :** Ajouter un `notes` explicatif dans `INV_MSC_AND_STRICT` ou créer `INV_MSC_COMPONENT_UNKNOWN_DEFERS_MASTERY` : composante `unknown` → maîtrise `deferred`, jamais `true`. Scope : `runtime_evaluation`.

---

### ARB-03 — Borne de fin de boucle de `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`

- **Source(s) :** GPTwoThink (F-1.4 / 1.4), ClaudeWoThink (HIGH-01 partiel), GPTThink (mention implicite)
- **Constat synthétique :** La règle définit un protocole en deux étapes (diagnostique → escalade si persistance), mais « persistance » n'est pas définie constitutionnellement. Aucune borne de fin de boucle (nombre de cycles, délai maximal) n'est déclarée. La boucle diagnostique → escalade → diagnostique est potentiellement infinie.
- **Nature :** logique / état moteur oscillatoire non borné
- **Gravité :** élevé
- **Impact :** stabilité moteur / applicabilité
- **Décision :** `corriger_maintenant`
- **Justification :** Le risque d'oscillation infinie est structurel. Correction minimale : ajouter dans `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` une déclaration que la condition de « persistance après diagnostique » est paramétrisée par le Référentiel (via un paramètre nommé `PARAM_REFERENTIEL_MSC_DIVERGENCE_PERSISTENCE_THRESHOLD`), et qu'en absence de ce paramètre, ARB-01 s'applique.
- **Conséquence pour le patch :** Modifier `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` pour déclarer le paramètre Référentiel requis pour la condition de persistance. Ajouter `PARAM_REFERENTIEL_MSC_DIVERGENCE_PERSISTENCE_THRESHOLD` dans le Référentiel avec une valeur par défaut défensive. Scope : `runtime_state`.

---

### ARB-04 — Régime oscillatoire `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` sans borne de cycles

- **Source(s) :** ClaudeWoThink (A1-4)
- **Constat synthétique :** La condition de sortie du régime oscillatoire est `R atteint`, sans borne temporelle ni compteur de cycles maximal. Si R n'est jamais atteint (KU créative à multiplicateur R faible), l'oscillation est potentiellement infinie.
- **Nature :** logique / état moteur non borné
- **Gravité :** élevé
- **Impact :** stabilité moteur — l'apprenant peut rester bloqué dans une boucle indéfinie.
- **Décision :** `corriger_maintenant`
- **Justification :** Source unique mais risque structurel avéré et correction minimale possible. Ajouter un paramètre de borne maximale de cycles dans le Référentiel, et une sortie par défaut si le maximum est atteint sans que R ne soit satisfait.
- **Conséquence pour le patch :** Modifier `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` pour déclarer `PARAM_REFERENTIEL_OSCILLATORY_REGIME_MAX_CYCLES` avec comportement de sortie défini si la borne est atteinte (ex. : escalade ou sortie forcée vers consolidation). Scope : `runtime_state` / Référentiel.

---

### ARB-05 — Comportement composite multi-axes `unknown` simultanés

- **Source(s) :** Sonar (RISK-01 / 3.1), GPTThink (C-03 / 3.1)
- **Constat synthétique :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise des axes `unknown`. Mais lorsque ≥2 axes sont simultanément `unknown` (ex. : Activation = unknown ET VC = unknown), aucune règle ne définit le comportement composite du moteur. Les règles conservatrices individuelles existent, mais leur composition n'est pas déclarée.
- **Nature :** logique / état moteur indéfini
- **Gravité :** critique (Sonar) / élevé (GPTThink)
- **Impact :** stabilité moteur — comportement divergent selon l'implémentation.
- **Décision :** `corriger_maintenant`
- **Justification :** Convergence 2/4 rapports, gravité critique retenue. Correction minimale : ajouter un invariant ou une note dans `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` précisant que si ≥2 axes sont simultanément `unknown`, le moteur applique la réponse conservatrice maximale (scaffolding léger réversible, AR-N1 sollicité en priorité), sans déclenchement de règles dépendantes des valeurs spécifiques de ces axes.
- **Conséquence pour le patch :** Ajouter `INV_MULTI_AXIS_UNKNOWN_COMPOSITE_FALLBACK` : ≥2 axes `unknown` simultanément → réponse conservatrice maximale globale. Scope : `runtime_state / governance`.

---

### ARB-06 — Escalade constitutionnelle pour la détresse activation chronique

- **Source(s) :** Sonar (RISK-06 / 2.1)
- **Constat synthétique :** Par symétrie avec `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, il n'existe pas de mécanisme d'escalade constitutionnel lorsque l'axe Activation reste en détresse sur N sessions consécutives malgré le scaffolding conservateur. L'asymétrie est structurelle.
- **Nature :** logique / gouvernance pédagogique
- **Gravité :** élevé
- **Impact :** applicabilité / sécurité apprenant — une détresse chronique n'a pas de sortie constitutionnelle définie.
- **Décision :** `corriger_maintenant`
- **Justification :** Source principale Sonar, mais asymétrie structurelle bien identifiée. Correction minimale : déclarer un invariant ou une règle prescrivant qu'une détresse Activation persistante sur N sessions (N paramétrisé par le Référentiel) déclenche une escalade hors-session. Par symétrie avec le protocole divergence MSC.
- **Conséquence pour le patch :** Ajouter `RULE_PERSISTENT_ACTIVATION_DISTRESS_TRIGGERS_ESCALATION` dans la Constitution avec dépendance sur un paramètre Référentiel `PARAM_REFERENTIEL_ACTIVATION_DISTRESS_PERSISTENCE_THRESHOLD`. Scope : `runtime_state / governance`.

---

### ARB-07 — `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` ne couvre pas les mises à jour post-chargement

- **Source(s) :** GPTwoThink (F-1.2 / 1.2), GPTThink (C-07)
- **Constat synthétique :** L'invariant se déclenche au chargement du graphe. Un patch incrémental sur le graphe (ajout d'arête ou de KU) peut réintroduire un cycle sans déclencher l'invariant. Aucun `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` ni `ACTION_BLOCK_GRAPH_LOAD` ne sont déclarés.
- **Nature :** logique / cohérence interne
- **Gravité :** critique (GPTwoThink) / modéré (GPTThink)
- **Impact :** applicabilité — un cycle post-patch est silencieux et peut bloquer le runtime.
- **Décision :** `corriger_maintenant`
- **Justification :** Convergence 2/4 et gravité critique retenue. Correction minimale : étendre le trigger de `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` pour couvrir toute modification incrémentale du graphe (patch de graphe inclus), ou ajouter un invariant dédié `INV_KNOWLEDGE_GRAPH_PATCH_MUST_REVALIDATE_ACYCLICITY`.
- **Conséquence pour le patch :** Modifier `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` pour ajouter dans son trigger la validation post-patch de graphe. Optionnellement déclarer `EVENT_KNOWLEDGE_GRAPH_CYCLE_DETECTED` et `ACTION_BLOCK_GRAPH_LOAD`. Scope : `knowledge_model / governance`.

---

### ARB-08 — `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` non déclaré

- **Source(s) :** ClaudeWoThink (HIGH-02 / A1-2)
- **Constat synthétique :** `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` cite `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans son human_readable, mais cet événement n'est déclaré dans aucune section `EVENTS` du Référentiel ou de la Constitution. La sortie d'escalade du mode conservateur est techniquement inaccessible.
- **Nature :** logique / cohérence interne / runtime_state
- **Gravité :** élevé
- **Impact :** applicabilité — l'apprenant peut rester indéfiniment en mode conservateur.
- **Décision :** `corriger_maintenant`
- **Justification :** Source unique mais vide structurel clair et correction triviale. Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans le Référentiel.
- **Conséquence pour le patch :** Ajouter la déclaration de `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans le Référentiel, avec binding vers `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`. Scope : `runtime_state` / Référentiel.

---

### ARB-09 — AR-N3 orphelin sans consommation définie

- **Source(s) :** GPTThink (C-06 / 2.3), Sonar (implicite via calibration)
- **Constat synthétique :** `TYPE_SELF_REPORT_AR_N3` est collecté mais aucune règle, action ou invariant constitutionnel ne définit la consommation de l'indice AR-N3 résultant. Son effet sur le modèle apprenant n'est pas déclaré constitutionnellement.
- **Nature :** logique / cohérence interne
- **Gravité :** modéré
- **Impact :** maintenabilité / applicabilité — collecte inutile ou sous-définie.
- **Décision :** `corriger_maintenant`
- **Justification :** Convergence 2/4. Correction minimale : déclarer dans la Constitution que la consommation de l'indice AR-N3 est déléguée au Référentiel et ajouter le binding explicite `depends_on: [REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION]` sur `TYPE_SELF_REPORT_AR_N3` avec une `note` indiquant que l'indice alimente le calibrage AR-N3 tel que défini dans le Référentiel.
- **Conséquence pour le patch :** Modifier `TYPE_SELF_REPORT_AR_N3` pour déclarer son binding vers le Référentiel et la cible de consommation. Scope : `runtime_evaluation / intercore_reference`.

---

### ARB-10 — Misconception flagging : clarification du scope `design_runtime`

- **Source(s) :** Sonar (RISK-05 / 4.1), GPTwoThink (F-4.1 / 4.1)
- **Constat synthétique :** `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` se déclenche sur `KU flaggée misconception`. Le scope `design_runtime` est ambigu. Si le flagging est inféré en runtime, cela viole `INV_NO_RUNTIME_CONTENT_GENERATION` et `INV_RUNTIME_FULLY_LOCAL`. La Constitution doit préciser que le flag misconception est exclusivement posé en phase design ou par outillage off-session.
- **Nature :** dépendance IA implicite / cohérence interne
- **Gravité :** élevé
- **Impact :** sécurité logique — risque de violation d'invariant constitutionnel majeur.
- **Décision :** `corriger_maintenant`
- **Justification :** Convergence 2/4, risque de violation d'invariant non-patchable. Correction minimale : ajouter une précision dans `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` et/ou dans `TYPE_KNOWLEDGE_UNIT` que le flag `misconception` est exclusivement un attribut design ou off-session.
- **Conséquence pour le patch :** Modifier la note ou les conditions de `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` pour lever l'ambiguïté : flagging = design / outillage off-session uniquement, jamais inférence runtime. Scope : `design / governance`.

---

### ARB-11 — Versioning inter-Core et mécanisme de release coordonnée

- **Source(s) :** Sonar (RISK-03), GPTwoThink (F-5.3), GPTThink (5.2)
- **Constat synthétique :** La Constitution référence `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` (`patchable: false`). Aucun mécanisme de release coordonnée inter-Core n'est décrit pour gérer la promotion du Référentiel vers V1_1 ou V2_0. Aucune contrainte de compatibilité descendante entre versions de Core n'est définie.
- **Nature :** gouvernance / versioning
- **Gravité :** élevé
- **Impact :** maintenabilité / stabilité du système documentaire à long terme.
- **Décision :** `reporter`
- **Justification :** Problème structurel réel mais qui nécessite un chantier de gouvernance inter-Core qui dépasse le périmètre d'un patch correctif ciblé. Un patch minimal ne peut pas résoudre ce problème sans risquer de toucher à des éléments `patchable: false`. À traiter dans un cycle dédié.
- **Conséquence pour le patch :** Aucune. Reporter à un pipeline de gouvernance inter-Core dédié.

---

### ARB-12 — Gouvernance du LINK dans la Constitution

- **Source(s) :** ClaudeWoThink (CRIT-01), Sonar (RISK-09)
- **Constat synthétique :** La Constitution ne protège pas contre une modification du LINK qui introduirait de la logique métier autonome ou une désynchronisation après un patch sélectif. Le LINK n'est pas soumis à des règles constitutionnelles de gouvernance. Note : le LINK n'était pas disponible dans le corpus d'analyse.
- **Nature :** gouvernance / séparation des couches
- **Gravité :** modéré (LINK absent du corpus)
- **Impact :** maintenabilité — problème réel mais non evaluable sans le LINK.
- **Décision :** `reporter`
- **Justification :** Le LINK étant absent du corpus d'analyse des challengers, l'évaluation complète est impossible. Reporter après audit complet du LINK.
- **Conséquence pour le patch :** Aucune. Reporter à un cycle incluant l'audit du LINK.

---

### ARB-13 — Gamification probatoire sans condition de sortie

- **Source(s) :** GPTThink (C-12 / 2.4)
- **Constat synthétique :** `RULE_UNVERIFIED_GAMIFICATION_PROBATION` déclare un mode probatoire sans conditions de sortie définies. Le moteur peut rester indéfiniment en mode probatoire.
- **Nature :** logique / état moteur indéfini
- **Gravité :** modéré
- **Impact :** applicabilité — sortie probatoire non définie.
- **Décision :** `reporter`
- **Justification :** Source unique, gravité modérée, et le problème ne bloque pas un chemin critique apprenant (mode probatoire est conservateur par nature). À corriger dans un prochain cycle mais pas prioritaire.
- **Conséquence pour le patch :** Aucune. À inscrire dans le backlog du prochain cycle de challenge.

---

### ARB-14 — Densité cumulée AR-N* sans borne constitutionnelle

- **Source(s) :** GPTThink (C-08 / 2.1), GPTwoThink (F-2.1 / 2.1)
- **Constat synthétique :** Aucune règle constitutionnelle ne borne la fréquence cumulée des sollicitations AR toutes natures confondues par session. Un moteur peut saturer l'apprenant sans violer d'invariant.
- **Nature :** logique / charge cognitive
- **Gravité :** modéré
- **Impact :** applicabilité / charge apprenant.
- **Décision :** `reporter`
- **Justification :** Convergence 2/4 mais problème de calibrage dont la valeur optimale est difficile à fixer constitutionnellement sans données empiriques. À déléguer au Référentiel dans un cycle dédié.
- **Conséquence pour le patch :** Aucune. À traiter en Référentiel dans un prochain cycle.

---

### ARB-15 — `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` orphelin dans les relations de `TYPE_MASTERY_MODEL`

- **Source(s) :** GPTwoThink (F-1.1 / 1.1)
- **Constat synthétique :** `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` contraint `TYPE_MASTERY_MODEL` mais n'est référencé dans aucune relation depuis ce type. La contrainte est invisible lors d'une traversée graphe depuis `TYPE_MASTERY_MODEL`.
- **Nature :** traçabilité / cohérence des relations
- **Gravité :** élevé (GPTwoThink)
- **Impact :** maintenabilité — une implémentation peut ignorer la séparation de T.
- **Décision :** `rejeter`
- **Justification :** La contrainte est fonctionnellement présente dans la Constitution et déclarée dans `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`. L'absence de relation inversée depuis `TYPE_MASTERY_MODEL` est un problème de navigation graphe mais pas un vide logique. La sémantique de `derives_from` est descriptive, non d'instanciation (comme indiqué par GPTThink en C-15). Ajouter une relation inversée risque de créer la dépendance circulaire notée en C-15. Rejet motivé par le risque d'effet de bord plus élevé que le bénéfice.
- **Conséquence pour le patch :** Aucune.

---

### ARB-16 — Feedback Coverage Matrix non obligatoire pour KU perceptuelles

- **Source(s) :** GPTwoThink (F-2.4 / 2.4)
- **Constat synthétique :** `TYPE_FEEDBACK_COVERAGE_MATRIX` n'est obligatoire que pour les KU formelles et procédurales. Les KU perceptuelles (identifiées par `INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL`) ne sont pas explicitement dans le scope d'obligation.
- **Nature :** cohérence interne / ingénierie pédagogique
- **Gravité :** modéré
- **Impact :** applicabilité — une KU perceptuelle peut être déployée sans matrice feedback.
- **Décision :** `corriger_maintenant`
- **Justification :** Incohérence avec `INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL` déjà existant. Correction triviale et minimale : ajouter `perceptual` à la liste des types KU concernés par l'obligation de `TYPE_FEEDBACK_COVERAGE_MATRIX`.
- **Conséquence pour le patch :** Modifier la condition d'obligation de `TYPE_FEEDBACK_COVERAGE_MATRIX` pour inclure les KU perceptuelles. Scope : `design / governance`.

---

### ARB-17 — `source_anchor` hétérogène pour les éléments issus d'arbitrage

- **Source(s) :** GPTThink (C-16 / 1.4), Sonar (RISK-08)
- **Constat synthétique :** Les éléments introduits par `[ARBITRAGE_2026_04_01]` portent un source_anchor d'arbitrage plutôt qu'une ancre `[Sxx]` normative stable. Hétérogénéité de traçabilité.
- **Nature :** traçabilité / gouvernance éditoriale
- **Gravité :** faible
- **Impact :** maintenabilité à long terme.
- **Décision :** `rejeter`
- **Justification :** La convention d'ancrage par arbitrage est une décision de gouvernance éditoriale qui dépasse le périmètre d'un patch correctif. Les ancres `[ARBITRAGE_*]` sont traçables et non ambiguës. Normaliser vers `[Sxx]` exigerait une réforme de la convention d'ancrage à définir au préalable. Rejet dans ce cycle.
- **Conséquence pour le patch :** Aucune.

---

### ARB-18 — Dégradation temporelle de R non déclarée constitutionnellement

- **Source(s) :** GPTThink (C-02 / 2.2), GPTwoThink (F-2.2 partiel)
- **Constat synthétique :** La composante R (robustesse temporelle) n'est soumise à aucun mécanisme constitutionnel de décroissance temporelle. Un moteur peut maintenir R à sa valeur maximale indéfiniment, rendant la maîtrise de base valide même après une très longue interruption.
- **Nature :** solidité théorique / learning science
- **Gravité :** élevé
- **Impact :** applicabilité — maîtrise déclarée illusoirement stable sans réactivation.
- **Décision :** `corriger_maintenant`
- **Justification :** Convergence 2/4. La décroissance de R est une exigence de la science de l'apprentissage (courbe d'oubli). Correction minimale : ajouter une déclaration constitutionnelle que R est soumis à une décroissance temporelle constitutive, dont les paramètres sont bornés par le Référentiel. Ne pas fixer de valeur : la déléguer au Référentiel.
- **Conséquence pour le patch :** Ajouter dans `TYPE_MASTERY_COMPONENT_R` ou via un invariant `INV_MASTERY_R_SUBJECT_TO_TEMPORAL_DECAY` que R décroît avec le temps en absence d'activité, paramétrisé par le Référentiel. Scope : `runtime_evaluation / learning_science`.

---

## Décisions à transmettre au patch

| ID | Titre court | Priorité | Core cible | Contrainte de minimalité |
|---|---|---|---|---|
| ARB-01 | Fallback constitutionnel seuils Référentiel absents | critique | Constitution | Invariant additionnel uniquement, ne pas modifier les éléments existants |
| ARB-02 | MSC AND strict — composante non calculable → `deferred` | critique | Constitution | Note ou invariant complémentaire, ne pas réécrire `INV_MSC_AND_STRICT` |
| ARB-05 | Multi-axes unknown simultanés — fallback composite | critique | Constitution | Invariant additionnel uniquement |
| ARB-07 | Cycle graphe post-patch — extension du trigger | critique | Constitution | Modifier le trigger de l'invariant existant ou ajouter un invariant dédié |
| ARB-03 | Borne boucle divergence MSC | élevé | Constitution + Référentiel | Ajouter le paramètre nommé dans le Référentiel, modifier la règle en Constitution |
| ARB-06 | Escalade détresse activation chronique | élevé | Constitution + Référentiel | Règle symétrique à `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` |
| ARB-10 | Misconception flagging — scope design-only | élevé | Constitution | Précision minimale dans la règle existante |
| ARB-18 | Dégradation temporelle de R | élevé | Constitution + Référentiel | Invariant additionnel en Constitution, délégation paramétrique au Référentiel |
| ARB-04 | Régime oscillatoire — borne de cycles | élevé | Référentiel | Paramètre additionnel dans le Référentiel uniquement |
| ARB-08 | EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION manquant | élevé | Référentiel | Déclaration d'événement manquant dans le Référentiel |
| ARB-09 | AR-N3 — binding consommation déclaré | modéré | Constitution | Ajout `depends_on` et `note` sur l'élément existant |
| ARB-16 | Feedback Coverage Matrix — KU perceptuelles incluses | modéré | Constitution | Extension de condition, pas de réécriture |

**Contraintes transversales à respecter par le patch :**
- Séparation Constitution / Référentiel strictement maintenue : aucune logique métier ne doit être introduite dans le LINK.
- Corrections minimales privilégiées : invariants additionnels préférés aux réécritures d'éléments existants.
- Aucun élément `patchable: false` ne doit être modifié.
- Tout nouveau paramètre Référentiel introduit doit avoir une valeur par défaut défensive documentée.

---

## Décisions explicitement non retenues

| ID | Titre court | Décision | Justification |
|---|---|---|---|
| ARB-11 | Versioning inter-Core / release coordonnée | `reporter` | Chantier structurel dépassant le périmètre d'un patch correctif ; nécessite un cycle dédié |
| ARB-12 | Gouvernance LINK dans la Constitution | `reporter` | LINK absent du corpus d'analyse ; évaluation impossible sans audit LINK complet |
| ARB-13 | Gamification probatoire sans sortie | `reporter` | Source unique, gravité modérée, chemin non critique ; backlog prochain cycle |
| ARB-14 | Densité cumulée AR-N* | `reporter` | Valeur optimale non fixable constitutionnellement sans données empiriques ; déléguer au Référentiel dans un cycle dédié |
| ARB-15 | INV_TRANSFER orphelin dans les relations | `rejeter` | Relation inversée risque d'introduire une dépendance circulaire ; contrainte fonctionnellement présente |
| ARB-17 | source_anchor hétérogène arbitrage | `rejeter` | Convention d'ancrage par arbitrage valide et traçable ; réforme hors périmètre de ce cycle |
