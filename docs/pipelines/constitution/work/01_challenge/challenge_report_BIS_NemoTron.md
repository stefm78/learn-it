# CHALLENGE REPORT — Constitution Learn-it

**Pipeline:** constitution
**Stage:** STAGE_01_CHALLENGE
**ID agent:** NemoTron
**Date:** 2026-04-01
**Cores auditées:**
- `CORE_LEARNIT_CONSTITUTION_V1_9` (V1_9_FINAL)
- `CORE_LEARNIT_REFERENTIEL_V1_0` (V1_0_FINAL)
- `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0` (V1_9__V1_0_FINAL)

---

## Résumé exécutif

Le système présente une architecture globalement cohérente et bien gouvernée. La séparation Constitution/Référentiel/LINK est correctement posée. La contrainte de fermeture locale (zéro IA continue au runtime) est un principe fort, bien protégé par plusieurs invariants et contraintes. Cependant, l'audit révèle **8 faiblesses significatives** réparties entre des problèmes de complétude (paramètres délégués non bornés), des états moteur indéfinis (conflits entre règles dans des contextes combinés), des dépendances IA implicites non résolues, et des zones de gouvernance mal couvertes. Aucune faille ne menace l'intégrité structurelle du Core, mais plusieurs peuvent produire des comportements moteur silencieusement incorrects ou des blocages non documentés.

---

## Analyse détaillée par axe

---

### Axe 1 — Cohérence interne

#### C-01 — `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` référence un EVENT absent
- **Élément concerné :** `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` (Référentiel) — déclenche `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION`
- **Nature :** L'event `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` est mentionné en `human_readable` de ce paramètre mais n'est déclaré **ni dans la Constitution ni dans le Référentiel**.
- **Type de problème :** complétude
- **Impact moteur :** Le moteur ne peut pas déclencher l'escalade attendue lorsque le mode conservateur persiste au-delà du seuil. L'escalade est silencieusement abandonnée.
- **Correction à arbitrer :** Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` dans le Référentiel avec une rule associée, ou documenter explicitement que ce signal est purement externe (notification humaine hors-session).

#### C-02 — `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` mentionnée sans être déclarée
- **Élément concerné :** `PARAM_REFERENTIEL_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION` (Référentiel) — référence `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED`
- **Nature :** Cette règle est citée dans `human_readable` mais introuvable dans la Constitution ou le Référentiel.
- **Type de problème :** complétude / gouvernance
- **Impact moteur :** La désactivation de l'axe VC invoque une autorité constitutionnelle non matérialisée. Cela rend la désactivation non traçable et potentiellement contestable.
- **Correction à arbitrer :** Déclarer `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` dans la Constitution comme règle de gouvernance, ou renommer la référence vers l'invariant existant `INV_VC_NOT_GENERAL_MOTIVATION_PROXY`.

#### C-03 — Binding LINK `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` utilise une syntaxe `core_ref` incohérente avec le reste du LINK
- **Élément concerné :** `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` (LINK)
- **Nature :** Les relations `binds` utilisent ici une structure `{core_ref: ..., id: ...}` alors que tous les autres bindings LINK utilisent la forme `id: NAMESPACE::ELEMENT`. Il y a une inconsistance de schéma.
- **Type de problème :** gouvernance / implémentabilité
- **Impact moteur :** Tout parseur ou outil de validation automatique du LINK risque de traiter ce binding différemment, introduisant une faille d'audit silencieuse.
- **Correction à arbitrer :** Uniformiser la syntaxe du LINK — soit adopter `core_ref` partout, soit revenir à la forme `id: NAMESPACE::ELEMENT`.

#### C-04 — `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` dépend de `TYPE_SELF_REPORT_AR_N1` mais la divergence est définie uniquement par rapport à AR-N1 sans condition sur sa disponibilité
- **Élément concerné :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` (Constitution)
- **Nature :** L'event suppose qu'AR-N1 signale un blocage persistant, mais si AR-N1 est absent (profil AR-réfractaire), la divergence ne peut être détectée. Or il n'existe pas de règle de fallback définissant le comportement dans ce cas combiné : MSC validé + AR-N1 absent.
- **Type de problème :** états indéfinis / complétude
- **Impact moteur :** Lorsqu'un apprenant est à la fois en profil AR-réfractaire et que son MSC semble anormal, le moteur ne peut déclencher ni la divergence MSC, ni l'escalade.
- **Correction à arbitrer :** Ajouter une condition explicite dans `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` : si AR-N1 est absent et que d'autres signaux suggèrent une divergence (proxys ou AR-N2), une règle conservatrice dédiée doit être définie.

---

### Axe 2 — Solidité théorique

#### Charge cognitive
- **Point solide :** La contrainte multimodale (`INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL`) témoigne d'une bonne intégration de la charge cognitive intrinsèque par type de KU.
- **Zone de risque :** Il n'existe pas de mécanisme déclaré pour détecter la charge cognitive extrinsèque en cours de session (redondance inutile dans la présentation, mauvaise organisation des livrables). Seul le garde-fou temporel (`PARAM_REFERENTIEL_COGNITIVE_FATIGUE_MINUTES_GUARDRAIL`) intervient de façon très tardive.
- **Angle mort :** La charge germane (effort d'apprentissage productif) n'est pas instrumentée. Il n'existe pas de proxy ou de KPI constitutionnel pour distinguer un apprenant en effort intense d'un apprenant en surcharge.

#### Mémoire / consolidation
- **Point solide :** La composante R (robustesse temporelle) avec ses multiplicateurs par type de KU (`TYPE_REFERENTIEL_TEMPORAL_MULTIPLIER_TABLE`) est bien articulée avec la théorie de l'oubli.
- **Zone de risque :** La révocation post-maîtrise (`RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`) suppose un nombre d'échecs consécutifs configurable, mais aucune protection n'existe contre une révocation trop rapide sur une KU procédurale à forte variance de performance (la performance procédurale est naturellement bruitée).
- **Angle mort :** Aucune distinction entre oubli d'un concept appris et erreur due au bruit mesure pour les KU procédurales à forte variance.

#### Motivation
- **Point solide :** L'axe VC (`TYPE_STATE_AXIS_VALUE_COST`) est fondé sur la théorie VIE/EVT, correctement séparé d'un proxy général de motivation.
- **Zone de risque :** Le déclenchement du patch relevance sur VC basse persistante ne prend pas en compte le profil de l'apprenant (étudiant en début vs en fin de parcours). Un étudiant en fin de parcours avec VC basse peut légitimement déprioriser ce contenu, mais le moteur déclencherait le patch relevance de façon identique.
- **Angle mort :** Pas de distinction entre VC basse liée à un manque de sens perçu et VC basse liée à un sentiment de compétence déjà acquise (effet plafond de pertinence perçue).

#### Métacognition / SRL
- **Point solide :** La collecte de l'intention de session (`TYPE_REFERENTIEL_SESSION_INTENTION_CONFIGURATION`) et son statut non-bloquant sont bien alignés avec les modèles SRL de forethought.
- **Zone de risque :** Il n'existe pas de mécanisme de clôture réflexive explicite pour le self-evaluation post-session (AR-N2 collecte des données mais ne structure pas de moment réflexif formel).
- **Angle mort :** L'auto-régulation lors d'une session (monitoring en cours d'action) n'est pas instrumentée, seul l'état post-session est capturé.

#### Émotions / engagement
- **Point solide :** La distinction confusion/frustration/anxiété via AR-N1 (`TYPE_SELF_REPORT_AR_N1`) est explicitement liée à une réponse différenciée, ce qui est théoriquement robuste.
- **Zone de risque :** En mode conservateur sans AR-N1, la réponse est un scaffolding léger identique quelle que soit l'émotion inférée. Cela peut amplifier la frustration si l'apprenant est réellement sous-défié (état de flow bloqué).
- **Angle mort :** Aucun mécanisme de détection d'ennui ou de désengagement passif (absence d'émotion visible sans non-réponse AR).

#### Mastery learning
- **Point solide :** L'agrégation AND stricte de P×R×A (`INV_MSC_AND_STRICT`) est une des meilleures implémentations formelles du mastery learning identifiées dans la littérature.
- **Zone de risque :** L'absence d'un seuil minimal d'occurrences pour R (distinct de P) peut permettre une déclaration de robustesse sur un délai court sans test suffisant de rétention à moyen terme.
- **Angle mort :** Pas de mécanisme de décroissance graduelle de R entre deux mesures (le délai R est binaire : passé ou non passé).

#### Ingénierie pédagogique
- **Point solide :** La contrainte `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4` protège correctement les missions de Bloom supérieur.
- **Zone de risque :** Le plafonnement à Bloom 2 en absence de contexte authentique est particulièrement restrictif. Dans certaines disciplines formelles, un design correct de Bloom 3 (application) peut exister sans contexte authentique déclaré explicitement.
- **Angle mort :** La notion de "contexte authentique" n'est pas définie formellement dans le système. Sa présence est auto-déclarée lors de la phase Analyse (`TYPE_AUTHENTIC_CONTEXT`), sans critère de validation objective.

---

### Axe 3 — États indéfinis moteur

#### I-01 — Conflit entre `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` et l'absence de priorité quand Détresse + AR-réfractaire sont simultanés
- **Description :** La table de priorité des régimes adaptatifs déclare que Détresse prime toujours. Cependant, si l'apprenant est en Détresse **ET** en profil AR-réfractaire, les deux règles de patch (relevance/sollicitation) peuvent être actives simultanément. Aucune règle de séquencement n'existe.
- **Impact moteur :** Deux patchs éligibles simultanément sans ordre de traitement déclaré = comportement non déterministe au niveau de la gouvernance patch.

#### I-02 — `TYPE_LEARNER_STATE_MODEL` avec les 3 axes `unknown` simultanément
- **Description :** `RULE_LEARNER_STATE_MODEL_AXIS_UNKNOWN_ALLOWED` autorise n'importe quel axe à rester `unknown`. Si les 3 axes (Calibration, Activation, VC) sont `unknown` simultanément, l'état apprenant est entièrement indéterminé. Aucune règle ne couvre ce cas.
- **Impact moteur :** Le moteur doit décider d'une réponse adaptative sans aucune information d'état. La réponse conservatrice par défaut (`RULE_NO_CALIBRATION_CONSERVATIVE_START`) ne couvre qu'un cas d'initialisation, pas un état `unknown` en cours de session.

#### I-03 — Maîtrise provisoire expirée non résolue : aucun fallback déclaré
- **Description :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` déclare une fenêtre de confirmation de maîtrise provisoire, mais aucune règle ne définit ce qui se passe si la fenêtre est expirée sans confirmation.
- **Impact moteur :** Rétrogradation automatique ? Signalement ? Traitement comme maîtrise non établie ? Ce scénario est un état moteur indéfini.

---

### Axe 4 — Dépendances IA implicites

#### IA-01 — Qualification du "contexte authentique" nécessite une inférence sémantique
- **Élément concerné :** `TYPE_AUTHENTIC_CONTEXT` (Constitution)
- **Description :** La déclaration d'un contexte authentique en phase Analyse repose sur la reconnaissance par un humain ou un agent qu'une situation-problème est "réelle". Aucun critère formel local-déterministe n'est fourni pour valider ce jugement.
- **Alternative sans IA continue :** Définir une liste de critères binaires (ex. : contexte issu d'un cas réel documenté, référence à un professionnel ou une organisation réelle nommée, etc.) vérifiables sans inférence sémantique.

#### IA-02 — Détection de la "misconception" (`RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT`) non formalisée
- **Élément concerné :** `TYPE_KNOWLEDGE_UNIT` → flag misconception (Constitution, `[S3][S18]`)
- **Description :** Une KU est flaggée "misconception" en phase Analyse, mais aucun critère formel de flaggage n'est déclaré dans le Core. Le design suppose implicitement une annotation humaine ou une inférence sémantique externe.
- **Alternative sans IA continue :** Ajouter un attribut `misconception_type` dans le schéma KU (ex. : alternative_conception, overconfidence, procedural_error) avec critères de flaggage déclaratifs.

#### IA-03 — Évaluation de la qualité du feedback dans `TYPE_FEEDBACK_COVERAGE_MATRIX`
- **Élément concerné :** `TYPE_FEEDBACK_COVERAGE_MATRIX` (Constitution)
- **Description :** La matrice indique une "couverture" mais aucun critère formel de complétude d'un template de feedback n'est défini. Une décision sur la qualité du feedback suppose implicitement une évaluation de contenu.
- **Alternative sans IA continue :** Définir un schéma minimal de template de feedback (présence de : identification d'erreur, explication, action de correction) validable structurellement hors session.

---

### Axe 5 — Gouvernance

#### G-01 — Absence de versioning explicite du LINK_CORE
- **Élément concerné :** `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0`
- **Description :** Le LINK encode sa version dans son `id` et son `version`, mais il n'existe aucune règle de gouvernance déclarant qu'un LINK doit être mis à jour lors d'un patch de la Constitution ou du Référentiel. La patchabilité du LINK est totalement absente (`INVARIANTS: []`, `RULES: []`, `PARAMETERS: []`).
- **Type de problème :** gouvernance
- **Impact moteur :** Un patch de Constitution ou de Référentiel peut invalider silencieusement des bindings LINK sans que le pipeline pipeline.md n'impose une révision du LINK.

#### G-02 — Pas de règle déclarant qui a autorité sur la désactivation de l'axe VC
- **Élément concerné :** `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` (Référentiel)
- **Description :** La désactivation de l'axe VC est effectuée côté Référentiel, mais l'axe est déclaré côté Constitution. Aucun invariant constitutionnel n'autorise explicitement cette désactivation.
- **Type de problème :** séparation des couches
- **Impact moteur :** La désactivation d'un axe constitutionnel par une règle référentielle sans binding LINK explicite constitue une violation potentielle du principe de séparation.
- **Correction à arbitrer :** Soit ajouter un invariant constitutionnel autorisant explicitement la désactivation par délégation référentielle, soit matérialiser un binding LINK dédié.

#### G-03 — Absence de couverture de la fermeture du pipeline d'investigation systémique
- **Élément concerné :** `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR`
- **Description :** Le comportement d'investigation systémique est défini (gel des ajustements, journalisation renforcée, escalade hors session), mais aucune règle ne décrit les conditions de **clôture** de l'investigation : quand et comment le moteur sort-il du mode minimal ?
- **Type de problème :** complétude / gouvernance
- **Impact moteur :** Le moteur peut rester bloqué indefiniment en mode minimal si les conditions de sortie ne sont pas formalisées.

---

### Axe 6 — Scénarios adversariaux

#### SC-01 — Apprenant en profil AR-réfractaire avec MSC en apparence validé mais contenu inadapté

**Scénario :** Un apprenant ne répond jamais à AR-N1 (5 sessions consécutives → profil AR-réfractaire). Le moteur déclenche un patch de sollicitation. En parallèle, le MSC calculé atteint P×R×A. L'apprenant continue à échouer aux tâches de compréhension profonde (observable uniquement par les proxys) sans jamais signaler son état.

**Mécanismes activés :**
- `EVENT_AR_REFRACTORY_PROFILE_DETECTED` → patch sollicitation
- `INV_MSC_AND_STRICT` → MSC validé
- Proxys comportementaux → régime adaptatif dégradé possible

**Limite révélée :** Le MSC est validé mais ne reflète pas la compréhension réelle. Sans AR-N1, la divergence MSC (`EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`) ne peut pas se déclencher. Le moteur est en état de fausse maîtrise sans escalade possible.

---

#### SC-02 — Déploiement en mode autonome d'une KU créative sans feedback déterministe disponible

**Scénario :** Un concepteur déclare une KU créative avec un contexte authentique, autorise Bloom 4+, et déploie en mode autonome. La matrice de feedback ne couvre pas ce type de KU (coverage < 70%). Le moteur tente de générer du feedback, déclenche `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK`, mais le feedback générique est insuffisant pour des tâches créatives.

**Mécanismes activés :**
- `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` → devrait bloquer
- `TYPE_AUTHENTIC_CONTEXT` → autorise Bloom 4+
- `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK` → fallback générique activé

**Limite révélée :** `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` bloque théoriquement le déploiement, mais la vérification que le feedback est "explicitement formalisé" n'est pas formellement outillée. Le blocage peut être contourné par une déclaration auto-validée.

---

#### SC-03 — Investigation systémique ouverte + patch relevance simultané

**Scénario :** L'apprenant cumule : VC basse persistante (4 sessions) + mode conservateur sans sortie (5 sessions) + AR-N1 absent. Deux signaux en anomalie → investigation systémique ouverte. En parallèle, `RULE_REFERENTIEL_VC_PERSISTENCE_TRIGGERS_RELEVANCE_PATCH` déclenche le patch relevance.

**Mécanismes activés :**
- `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` → gel des ajustements agressifs
- `RULE_REFERENTIEL_VC_PERSISTENCE_TRIGGERS_RELEVANCE_PATCH` → patch relevance éligible

**Limite révélée :** Ces deux règles sont contradictoires : le gel systémique devrait bloquer tout patch, mais le patch VC est déclenché indépendamment. Il n'existe pas de règle de préemption explicite entre investigation systémique et éligibilité des patchs.

---

### Axe 7 — Priorisation des risques

| ID | Élément | Type de problème | Priorité |
|----|---------|-----------------|---------|
| C-01 | `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` absent | Complétude | **Élevé** |
| C-04 | Divergence MSC non détectable si AR-réfractaire | États indéfinis | **Élevé** |
| I-01 | Détresse + AR-réfractaire : patchs simultanés non séquencés | États indéfinis | **Élevé** |
| I-03 | Maîtrise provisoire expirée : aucun fallback | Complétude | **Élevé** |
| SC-03 | Investigation systémique vs patch VC : contradiction | Gouvernance | **Élevé** |
| G-01 | LINK non révisé lors de patch Constitution/Référentiel | Gouvernance | **Modéré** |
| G-02 | Désactivation axe VC sans autorité constitutionnelle | Séparation couches | **Modéré** |
| G-03 | Clôture investigation systémique non définie | Complétude | **Modéré** |
| C-02 | `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` absente | Complétude | **Modéré** |
| C-03 | Syntaxe `core_ref` incohérente dans LINK | Gouvernance / implémentabilité | **Faible** |
| I-02 | 3 axes `unknown` simultanément : état indéfini | États indéfinis | **Faible** |
| IA-01 | Qualification contexte authentique sans critère formel | IA implicite | **Faible** |
| IA-02 | Flaggage misconception sans critère formel | IA implicite | **Faible** |
| IA-03 | Qualité template feedback non définie formellement | IA implicite | **Faible** |

---

## Corrections à arbitrer avant patch

### PRIO-1 : Déclarer `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` (Référentiel)
- Créer l'event avec logic d'escalade hors-session ou expliciter qu'il s'agit d'un signal externe uniquement.

### PRIO-2 : Couvrir le cas Divergence MSC + AR-réfractaire simultanés (Constitution)
- Ajouter une condition dans `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` ou une règle de gouvernance couvrant le cas où AR-N1 est absent mais d'autres signaux indiquent une divergence.

### PRIO-3 : Définir la préemption Investigation systémique sur les patchs éligibles (Référentiel)
- Ajouter une règle déclarant qu'en présence d'une investigation systémique ouverte, tout nouveau patch est suspendu jusqu'à clôture de l'investigation.

### PRIO-4 : Déclarer le fallback de maîtrise provisoire expirée (Constitution ou Référentiel)
- Créer un event et une règle couvrant l'expiration sans confirmation, avec comportement déclaré (rétrogradation ou signalement hors-session).

### PRIO-5 : Déclarer `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` dans la Constitution (ou renommer vers invariant existant)
- Pour lever l'ambiguïté sur l'autorité de désactivation de l'axe VC.

### PRIO-6 : Ajouter une règle de gouvernance du LINK lors de patch Constitution/Référentiel (pipeline ou LINK)
- Imposer une étape de validation du LINK dans le pipeline lors de tout patch impactant des éléments bindés.

### PRIO-7 : Définir les conditions de clôture de l'investigation systémique (Référentiel)
- Créer un event ou une règle de sortie du mode investigation, avec critères déclaratifs.
