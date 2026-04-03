# CHALLENGE REPORT — Constitution + Référentiel + LINK

**ID:** ClaudeWoThink  
**Pipeline:** constitution  
**Stage:** STAGE_01_CHALLENGE  
**Date:** 2026-04-01  
**Cores auditées:**
- Constitution: `CORE_LEARNIT_CONSTITUTION_V1_9` (V1_9_FINAL)
- Référentiel: `CORE_LEARNIT_REFERENTIEL_V1_0` (V1_0_FINAL)
- LINK: `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0` (V1_9__V1_0_FINAL)

**Note de focalisation:** aucune

---

## Résumé exécutif

Le système est architecturalement cohérent dans sa séparation Constitution / Référentiel / LINK. La majorité des invariants constitutionnels sont correctement protégés et non patchables. L'arbitrage du 2026-04-01 a produit deux nouvelles règles (`RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`) qui constituent des ajouts substantiels récents ; ce sont des surfaces de risque prioritaires à challenger.

**Points de vigilance principaux identifiés :**

1. **Paramètre fantôme (CRITIQUE)** — `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` est référencé dans `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` mais absent du Référentiel.
2. **Binding LINK manquant (ÉLEVÉ)** — `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` ne sont pas couverts par un binding inter-Core dans le LINK.
3. **État moteur indéfini sur conflit de régimes adaptatifs (ÉLEVÉ)** — La règle de résolution de conflit `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` mentionne un "régime oscillatoire" qui n'est pas un état de la matrice et dont le comportement moteur exact reste implicite.
4. **Absence de clôture explicite du flux diagnostique post-divergence MSC (MODÉRÉ)** — La règle `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` prévoit une escalade mais ne spécifie pas les conditions de sortie du régime diagnostique.
5. **Dépendance IA implicite résiduelle sur la détection de misconceptions (MODÉRÉ)** — `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` exige la détection de misconceptions à la construction du graphe, sans protocole déterministe outillé.

---

## Analyse détaillée par axe

---

### Axe 1 — Cohérence interne

#### 1.1 Paramètre orphelin — `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`

**Élément concerné :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` [Constitution, `ARBITRAGE_2026_04_01`]  
**Nature :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` (condition) mentionne explicitement :
> "sur le nombre de sessions défini dans `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`"

Ce paramètre est **absent du Référentiel** (V1_0_FINAL). Il n'est déclaré ni dans `TYPES`, `PARAMETERS`, `RULES` ni nulle part dans `referentiel.yaml`.

**Type de problème :** Complétude + Implémentabilité  
**Impact moteur :** Le moteur ne peut pas évaluer la condition de déclenchement de `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` sans ce paramètre. En absence de valeur, le déclencheur est soit ignoré, soit indéfini — les deux états sont des états moteur non autorisés.

**Correction à arbitrer :** Ajouter `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` dans le Référentiel (PARAMETERS, source_anchor `[ARBITRAGE_2026_04_01]`, patchable:true, parameterizable:true) avec une valeur de référence et des bornes. Décision d'autorité : Référentiel (seuil opérationnel délégué).

---

#### 1.2 Binding LINK manquant — divergence MSC perçu/calculé

**Élément concerné :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`, `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` [Constitution], `TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN` [LINK]  
**Nature :** Deux éléments issus de l'arbitrage 2026-04-01 (`DIVMSC-01`) sont absents du LINK. Le LINK ne contient aucun binding reliant ces éléments au Référentiel ni au flux inter-Core qui les sous-tend (notamment `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`).

**Type de problème :** Complétude (gouvernance inter-Core)  
**Impact moteur :** Le LINK est incomplet pour les ajouts de l'arbitrage ; l'auditabilité inter-Core et la traçabilité de la dépendance sont insuffisantes.

**Correction à arbitrer :** Ajouter dans le LINK un binding `TYPE_BINDING_MSC_PERCEPTION_DIVERGENCE_TO_REFERENTIEL_THRESHOLD` reliant `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` (Constitution) et `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` (Référentiel, une fois créé). Source_anchor : `[ARBITRAGE_2026_04_01][DIVMSC-01]`.

---

#### 1.3 Régime oscillatoire — état non formalisé dans la matrice

**Élément concerné :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` [Référentiel, `ARBITRAGE_2026_04_01`, `MATRIX-01`]  
**Nature :** La règle décrit un "régime oscillatoire" entre Consolidation et Exploration ("alternance 1 session consolidation satisfaisante → 1 session exploration → retour consolidation, sortie quand R atteint"). Ce régime n'est pas déclaré comme état dans `TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX` et aucun TYPE ni RULE ne le gouverne formellement.

**Type de problème :** Implémentabilité + Complétude  
**Impact moteur :** Un moteur déterministe ne peut pas implémenter un régime oscillatoire s'il n'est pas formalisé comme état de la matrice avec ses conditions d'entrée, de maintien et de sortie.

**Correction à arbitrer :** Formaliser le régime oscillatoire soit comme un 10e état de la matrice (nécessite PARAM_REFERENTIEL_ADAPTIVE_REGIME_TARGET_STATES actuel = 9 → révision à arbitrer), soit comme une méta-règle de planification séquentielle avec des conditions de transition déterministes déclarées dans le Référentiel.

---

#### 1.4 Paramètre `PARAM_REFERENTIEL_AR_REFRACTORY_SESSIONS_REFERENCE` — troncature du Référentiel

**Élément concerné :** `referentiel.yaml`, fin du fichier  
**Nature :** Le fichier Référentiel est tronqué à `PARAM_REFERENTIEL_AR_REFRACTORY_SESSIONS_REFERENCE`. Il est impossible de confirmer l'intégrité du reste du fichier (CONSTRAINTS, EVENTS, ACTIONS) depuis ce challenge.

**Type de problème :** Gouvernance (validité d'audit)  
**Impact moteur :** Non évaluable sans le fichier complet. À vérifier lors de l'arbitrage.

---

#### 1.5 SOURCE_ANCHOR incohérent sur `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`

**Élément concerné :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` [Référentiel]  
**Nature :** Le source_anchor est `[ARBITRAGE_2026_04_01][MATRIX-01]` mais `[MATRIX-01]` n'est référencé nulle part ailleurs dans le Référentiel comme section ou table formelle. Les autres règles de l'arbitrage utilisent `[ARBITRAGE_2026_04_01]` seul.

**Type de problème :** Gouvernance (traçabilité)  
**Impact moteur :** Faible, mais rupture de traçabilité mineure.

---

### Axe 2 — Solidité théorique

#### Charge cognitive
**Solide :** La contrainte AR-N1 (micro-sondage événementiel léger), AR-N2 (max 3 items), AR-N3 (bilan borné) constitue une architecture de mesure à charge minimale.  
**Zone de risque :** Le régime oscillatoire Consolidation/Exploration introduit une variabilité de session à session potentiellement déstabilisante pour les apprenants à faible métacognition — charge méta augmentée sans garde-fou.  
**Angle mort :** La charge cognitive d'implémentation du graphe (construction des arêtes de dépendance explicites) n'est pas bornée au niveau du design. Un graphe très dense peut rendre la propagation à 1 saut impraticable sans outil.

#### Mémoire / Consolidation
**Solide :** Le MSC AND strict (P + R + A) capture correctement la dimension temporelle (R) et opérationnalise le spacing avec des multiplicateurs par type de KU.  
**Zone de risque :** La révocation post-maîtrise (`RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`) requiert une fenêtre temporelle et des répétitions configurées, mais la configuration concrète de ces valeurs n'est pas exposée comme paramètres distincts (PARAM_REFERENTIEL_DEGRADATION_FAILURE_COUNT est déclaré, mais la fenêtre temporelle associée n'a pas de paramètre dédié explicitement visible dans le Référentiel).  
**Angle mort :** L'interleaving de contenus (`RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A`) exige que la composante A soit au seuil sur les KU concernées, mais aucun mécanisme de gestion du contexte de session ne garantit que les KU en interleaving appartiennent au même domaine sémantique proximal — risque d'interleaving contre-productif sur KU distales.

#### Motivation
**Solide :** L'axe VC (`TYPE_STATE_AXIS_VALUE_COST`) avec son invariant `INV_VC_NOT_GENERAL_MOTIVATION_PROXY` est une bonne protection contre la sur-interprétation. Le patch relevance (et non baisse de difficulté) est théoriquement aligné sur la théorie de l'expectancy-value.  
**Zone de risque :** La désactivation de l'axe VC par non-observabilité (`RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING`) retire une source d'information sans mécanisme de réactivation explicite — un apprenant pourrait rester dans un régime sans VC indefiniment si le format de collecte reste inadapté.  
**Angle mort :** Aucun mécanisme ne couvre la motivation intrinsèque vs extrinsèque ni la théorie de l'autodétermination (SDT). L'architecture repose entièrement sur VC perçue et activation — un angle mort pour les designers de contenu qui déploient sur des contextes à motivation très extrinsèque.

#### Métacognition / SRL
**Solide :** L'intention de session (`RULE_SESSION_INTENTION_NON_BLOCKING`) comme support du forethought SRL est un mécanisme léger et non punitif. AR-N3 (bilan périodique AEQ-dérivé) est un bon proxy de la dimension self-reflection SRL.  
**Zone de risque :** Le protocole de divergence MSC/perçu (`RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`) présuppose que le moteur peut « déclencher une phase diagnostique ciblée » sans spécifier comment l'apprenant est informé ou impliqué dans la résolution. Un retour diagnostique sans transparence peut dégrader la calibration méta de l'apprenant.  
**Angle mort :** Aucun mécanisme de goal-setting explicite (objectifs déclarés par l'apprenant) n'est prévu. L'intention de session est un proxy faible du goal-setting SRL.

#### Émotions / Engagement
**Solide :** L'axe activation (productif / détresse / sous-défi) est ancré sur des données AR-N1 événementielles plutôt que des inférences — robuste à la contrainte locale.  
**Zone de risque :** La distinction confusion / frustration / anxiété déclarée dans `TYPE_SELF_REPORT_AR_N1` ("Distinction temps réel confusion/frustration/anxiété") n'est pas opérationnalisée dans le Référentiel — aucun paramètre ni règle ne différencie le traitement moteur de ces trois états pourtant théoriquement distincts (la frustration peut signaler un défi proximal, l'anxiété peut signaler une charge traumatique non pédagogique).  
**Angle mort :** Les émotions positives (fierté, curiosité, flow) sont totalement absentes du modèle d'état. Le système détecte les états défavorables mais ne tire pas parti des états émotionnels favorables pour moduler positivement la progression.

#### Mastery learning
**Solide :** Le AND strict (P + R + A) avec seuils paramétriques et multiplicateurs temporels par type de KU est une opérationnalisation solide et locale du mastery learning de style Bloom/Carroll.  
**Zone de risque :** Le seuil P de référence (80 %, fourchette 70–90 %) est identique pour tous les types de KU. Des KU créatives ou perceptuelles peuvent nécessiter des seuils P différenciés. Cette différenciation n'est pas couverte.  
**Angle mort :** La composante T (transférabilité) est déclarée comme séparée de la maîtrise de base mais aucun mécanisme d'évaluation du transfert n'est spécifié dans les cores — ce mécanisme serait entièrement à implémenter par le designer sans garde-fou.

#### Ingénierie pédagogique
**Solide :** La matrice de couverture de feedback (`TYPE_FEEDBACK_COVERAGE_MATRIX`) comme livrable obligatoire de design est une bonne pratique d'ingénierie pédagogique.  
**Zone de risque :** Le contexte authentique (`TYPE_AUTHENTIC_CONTEXT`) est requis pour Bloom ≥ 4 mais aucune procédure de validation de l'authenticité n'est décrite — le designer peut déclarer un contexte comme authentique sans critère vérifiable.  
**Angle mort :** L'ADDIE est implicite (phases Analyse/Design/Développement peuvent être inférées) mais non formalisé comme cycle explicite dans le système — les transitions entre phases de design ne sont pas gouvernées.

---

### Axe 3 — États indéfinis moteur

#### 3.1 Détection de `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` sans paramètre de seuil

**Scénario :** L'apprenant a P+R+A validés et envoie AR-N1 "blocage total" session après session. Le moteur doit décider quand déclencher le protocole. Seuil manquant → le moteur ne peut pas décider. État indéfini.

#### 3.2 Sortie du protocole diagnostique post-divergence MSC

**Scénario :** La règle `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` déclenche une phase diagnostique. Si la phase diagnostique montre une récupération partielle (ex : AR-N1 s'améliore mais reste sous le seuil), le moteur ne dispose d'aucune règle de sortie partielle. Il peut osciller entre "diagnostique résolu" et "escalade" sans état intermédiaire défini.

#### 3.3 Régime adaptatif oscillatoire et conditions de sortie

**Scénario :** Consolidation + Exploration activés simultanément. Le régime oscillatoire est déclenché. Après 1 session consolidation satisfaisante → 1 session exploration. L'exploration échoue. La règle ne précise pas si l'on revient en Consolidation ou si on reste en Exploration. État de transition ambigu.

#### 3.4 KU créative en régime autonome sans chemin de feedback déterministe

**Scénario :** Une KU créative est déployée en mode autonome. `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` l'interdit si aucun feedback déterministe n'est disponible. Mais la détection de cette absence est à la charge du designer au moment du déploiement — aucun mécanisme de vérification runtime n'est décrit. Si le designer oublie, le moteur déploie quand même.

#### 3.5 AR-N1 absent ET proxy non disponible (double absence)

**Scénario :** AR-N1 absent (réfractaire) ET proxys tous sous seuil (moins de 2 proxys franchissent leur seuil, `PARAM_REFERENTIEL_ADAPTIVE_REGIME_PROXY_MIN`). `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` s'applique (scaffolding léger réversible). Mais dans quel régime adaptatif se trouve le moteur ? La règle conservatrice est-elle un état de la matrice adaptative ou un meta-comportement qui s'y superpose ? Non explicité.

---

### Axe 4 — Dépendances IA implicites

#### 4.1 Détection de misconceptions lors de la construction du graphe

**Élément :** `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` [Constitution, S3/S18]  
**Problème :** La détection d'une KU comme "misconception" nécessite une analyse sémantique du corpus. Or `INV_RUNTIME_FULLY_LOCAL` interdit toute inférence en usage. La détection ne peut donc avoir lieu qu'hors session, lors de la phase Analyse. Mais aucun outillage déterministe local n'est décrit pour identifier les misconceptions sans IA continue.  
**Alternative locale :** La misconception pourrait être déclarée explicitement par le designer (flag dans le graphe), éliminant toute inférence. La Constitution ne l'interdit pas, mais ne l'impose pas non plus — ambiguïté sur le vecteur de détection admis.

#### 4.2 Évaluation de la "satisfaction" d'une session de consolidation (régime oscillatoire)

**Élément :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` [Référentiel]  
**Problème :** Le régime oscillatoire déclare "1 session consolidation satisfaisante". La notion de "satisfaisante" n'est pas définie par un critère déterministe. Cela présuppose une évaluation qualitative de la session.  
**Alternative locale :** Remplacer "satisfaisante" par un critère P-threshold atteint sur les KU de la session de consolidation — critère déterministe disponible.

#### 4.3 Validation de l'authenticité du contexte authentique

**Élément :** `TYPE_AUTHENTIC_CONTEXT` [Constitution, S17e/S18]  
**Problème :** La validation qu'un contexte est "authentique" présuppose un jugement sémantique externe (ou humain). Aucun critère déterministe ni liste de critères objectifs n'est déclaré.  
**Alternative locale :** Checklist de validation explicite déclarée par le designer (contexte = situation réelle, apprenant reconnaissable, enjeu non fictif). Non implémentable automatiquement en local sans cette checklist.

---

### Axe 5 — Gouvernance

#### 5.1 Trou de couverture LINK sur l'arbitrage 2026-04-01

Le LINK V1_9__V1_0_FINAL a été mis à jour pour intégrer `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` (source_anchor `[ARBITRAGE_2026_04_01][AR3-01][SIG-01]`) et `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (source_anchor `[ARBITRAGE_2026_04_01][MATRIX-01]`). En revanche, les éléments issus du même arbitrage (`[DIVMSC-01]`) ne sont pas couverts par le LINK. L'arbitrage 2026-04-01 a donc été partiellement intégré au LINK. Risque de désynchronisation de versions.

#### 5.2 Versioning asymétrique

La Constitution est en V1_9_FINAL et le Référentiel en V1_0_FINAL. Avec deux patchs d'arbitrage déjà intégrés (`[PATCH_V1_0]`, `[ARBITRAGE_2026_04_01]`), le Référentiel reste à V1_0 alors que son contenu a évolué. Si les versions ne sont pas incrémentées après chaque arbitrage intégré, la traçabilité de "quel état est actuellement déployé" devient opaque.

#### 5.3 Paramètre `PARAM_AR_N1_INTERACTION_BUDGET` — non patchable mais parameterizable:true

**Élément :** `PARAM_AR_N1_INTERACTION_BUDGET` [Constitution]  
**Nature :** patchable:false, parameterizable:true. Cette combinaison est cohérente avec la philosophie (Constitution déclare le paramètre mais ne peut pas être patchée directement). Cependant, aucune règle constitutionnelle ni référentielle ne précise comment ce budget est opérationnalisé — la valeur concrète est implicite ("concis et local"). Paramètre partiellement orphelin.

#### 5.4 `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` — invariant sans mécanisme d'enforcement runtime

**Élément :** `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` [Constitution, S12/S17/PATCH_V1_9]  
**Nature :** Cet invariant interdit le régime autonome pour une KU créative sans chemin de feedback déterministe. Mais il n'y a ni EVENT ni ACTION associés — l'enforcement est déclaratif, pas implémentable automatiquement. La validation ne peut être que manuelle (design review).

---

### Axe 6 — Scénarios adversariaux

#### Scénario A — L'apprenant souverain-calibré et perceptivement figé

**Contexte :** Un apprenant a atteint P+R+A sur une KU formelle. Il répond systématiquement "je suis bloqué" sur AR-N1 session après session. Le système déclenche `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`.

**Mécanismes activés :** MSC AND strict, EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED, RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL.

**Limite non documentée :** Sans `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`, le déclenchement est indéterminé. Si le paramètre était présent (ex : 3 sessions), la phase diagnostique est déclenchée. Si la phase diagnostique confirme P+R+A mais que AR-N1 persiste en "blocage total", le moteur déclenche une escalade vers "révision du design du contenu" — mais aucun STATE de l'apprenant n'est documenté pendant cette escalade. L'apprenant continue-t-il des sessions normales ? Le moteur se fige ? Boucle non terminée.

#### Scénario B — Le profil Exploration/Consolidation en plateau

**Contexte :** Un apprenant atteint simultanément un état de sous-défi (KU trop faciles) ET un état de consolidation insuffisante sur d'autres KU. La matrice détecte Consolidation + Sous-défi → la règle dit "Sous-défi si R est atteint, sinon Consolidation". R n'est pas atteint → Consolidation prime. Mais l'apprenant est en sous-défi déclaré sur certaines KU et en consolidation sur d'autres.

**Mécanismes activés :** TYPE_REFERENTIEL_ADAPTIVE_REGIME_MATRIX, RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION, TYPE_MASTERY_COMPONENT_R.

**Limite non documentée :** La règle de conflit opère au niveau global du moteur mais les KU sont individuelles. La règle ne précise pas si le conflit est résolu KU par KU ou pour l'ensemble de la session. Un moteur implémentant "Consolidation prime globalement" va ignorer le sous-défi déclaré sur des KU où R est atteint — frustation probable.

#### Scénario C — Déploiement multicouche avec patch de sollicitation AR simultané

**Contexte :** L'apprenant est en profil AR-réfractaire (non-réponse AR-N1 sur la fenêtre). Un patch de sollicitation est en cours (`ACTION_TRIGGER_AR_SOLLICITATION_PATCH`). Simultanément, le moteur détecte une divergence MSC/perçu (`EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED`) — mais comme AR-N1 ne répond pas, la source de "blocage total perçu" est absente.

**Mécanismes activés :** RULE_AR_REFRACTORY_PROFILE_TRIGGERS_SOLLICITATION_PATCH, RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL, INV_CONSERVATIVE_RULE_WITHOUT_AR_N1.

**Limite non documentée :** L'event `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` a comme condition `AR-N1 signale un blocage total persistant`. Si AR-N1 est absent (réfractaire), la condition ne peut jamais être évaluée. La question est : le moteur doit-il alors ignorer la potentielle divergence MSC/perçu tant que le profil AR-réfractaire est actif ? Ce cas d'exclusion mutuelle n'est pas documenté.

---

### Axe 7 — Priorisation des risques

| Priorité | Identifiant du risque | Élément principal | Nature |
|---|---|---|---|
| **CRITIQUE** | R01 | `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` manquant | Complétude + Implémentabilité |
| **ÉLEVÉ** | R02 | Binding LINK manquant pour `DIVMSC-01` | Gouvernance |
| **ÉLEVÉ** | R03 | Régime oscillatoire non formalisé comme état de la matrice | Implémentabilité |
| **ÉLEVÉ** | R04 | Condition de déclenchement `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` sans seuil → état moteur indéfini | Implémentabilité |
| **MODÉRÉ** | R05 | Sortie du protocole diagnostique post-divergence non définie | Complétude |
| **MODÉRÉ** | R06 | Confusion/frustration/anxiété non différenciés au niveau moteur malgré la déclaration AR-N1 | Théorique + Complétude |
| **MODÉRÉ** | R07 | Authenticité du contexte non validable déterministiquement | Implémentabilité |
| **MODÉRÉ** | R08 | Seuil P uniforme pour tous types de KU — créatif et perceptuel potentiellement sous-optimal | Théorique |
| **MODÉRÉ** | R09 | KU créative en mode autonome sans enforcement runtime de `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` | Gouvernance |
| **FAIBLE** | R10 | Source_anchor `[MATRIX-01]` non référencé comme table formelle | Gouvernance (traçabilité) |
| **FAIBLE** | R11 | `PARAM_AR_N1_INTERACTION_BUDGET` sans valeur opérationnelle déclarée | Complétude |
| **FAIBLE** | R12 | Versioning asymétrique Constitution V1_9 / Référentiel V1_0 après arbitrages multiples | Gouvernance |

---

## Corrections à arbitrer avant patch

### C01 — Créer `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` dans le Référentiel

**Élément concerné :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` [Constitution]  
**Nature du problème :** Paramètre référencé mais absent  
**Type :** Complétude + Implémentabilité  
**Impact moteur :** Déclencheur non évaluable  
**Correction :** Ajouter dans `referentiel.yaml` → PARAMETERS :
- id: `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`
- authority: primary, patchable: true, parameterizable: true
- source_anchor: `[ARBITRAGE_2026_04_01][DIVMSC-01]`
- human_readable: Nombre de sessions consécutives de blocage AR-N1 persistant requis pour déclencher EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED
- Valeur de référence suggérée : 3, fourchette 2–5

### C02 — Ajouter binding LINK pour `DIVMSC-01`

**Élément concerné :** LINK CORE — couverture arbitrage 2026-04-01  
**Nature du problème :** Binding inter-Core manquant  
**Type :** Gouvernance  
**Impact moteur :** Traçabilité inter-Core incomplète  
**Correction :** Ajouter `TYPE_BINDING_MSC_PERCEPTION_DIVERGENCE_TO_REFERENTIEL_THRESHOLD` dans le LINK reliant `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` (Constitution) à `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` (Référentiel)

### C03 — Formaliser le régime oscillatoire

**Élément concerné :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` [Référentiel]  
**Nature du problème :** Comportement moteur décrit mais non formalisé comme état de la matrice  
**Type :** Implémentabilité  
**Impact moteur :** Incapacité d'implémentation déterministe  
**Correction à arbitrer :** Choisir entre (a) déclarer le régime oscillatoire comme état #10 de la matrice avec conditions d'entrée/maintien/sortie déterministes, ou (b) reformuler comme règle de planification séquentielle explicite sans état supplémentaire. Arbitrer si cela nécessite une révision de `PARAM_REFERENTIEL_ADAPTIVE_REGIME_TARGET_STATES`.

### C04 — Documenter la condition de sortie du protocole diagnostique post-divergence

**Élément concerné :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` [Constitution]  
**Nature du problème :** Condition de sortie du régime diagnostique non spécifiée  
**Type :** Complétude  
**Impact moteur :** Boucle potentiellement non terminée  
**Correction :** Ajouter une condition de sortie explicite dans la règle : ex. "si après N sessions diagnostiques P+R+A reste validé et AR-N1 se normalise → retour en régime normal ; si AR-N1 ne se normalise pas → escalade maintenue". Définir la valeur N par paramètre référentiel.

### C05 — Différencier le traitement moteur confusion / frustration / anxiété

**Élément concerné :** `TYPE_SELF_REPORT_AR_N1` [Constitution, S11]  
**Nature du problème :** Distinction déclarée mais non opérationnalisée  
**Type :** Théorique + Complétude  
**Impact moteur :** AR-N1 ne différencie pas les réponses adaptatives appropriées par type d'état émotionnel  
**Correction à arbitrer :** Soit différencier les actions moteur (ex : confusion → scaffolding cognitif, frustration → réduction de charge / variété, anxiété → déescalade), soit documenter explicitement que la distinction déclarée est réservée à la future évolution et que la version actuelle traite les trois comme "détresse" générique. Décision d'architecture à arbitrer.

---

*Rapport produit par : ClaudeWoThink (Perplexity, Sonnet 4.6) — STAGE_01_CHALLENGE — pipeline constitution*
