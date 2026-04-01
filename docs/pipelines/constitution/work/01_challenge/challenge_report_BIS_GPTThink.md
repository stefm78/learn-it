# CHALLENGE REPORT — BIS

**ID:** GPTThink
**Pipeline:** constitution
**Stage:** STAGE_01_CHALLENGE
**Date:** 2026-04-01
**Cores analysés:**
- `CORE_LEARNIT_CONSTITUTION_V1_9_FINAL`
- `CORE_LEARNIT_REFERENTIEL_V1_0_FINAL`
- `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0`

---

## Résumé exécutif

Le système Constitution/Référentiel/LINK constitue une architecture de gouvernance pédagogique remarquablement disciplinée. La séparation des couches est réelle et globalement respectée. Les invariants critiques (AND strict MSC, 1-saut graphe, local-only, no-generation) sont correctement protégés par des `patchable: false`.

**Cependant, l'audit révèle six zones de fragilité sérieuses** :

1. **L'état `unknown` des axes apprenant est structurellement sous-gouverné** : plusieurs règles moteur présupposent un état disponible sans specifier le comportement lorsque tous les axes sont simultaneously à `unknown/absent/non-observable`.
2. **Le mécanisme MSC-Perception-Divergence est théoriquement valide mais opérationnellement incomplet** : le paramètre seuil `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` est cité par la Constitution mais absent du Référentiel.
3. **La matrice des régimes adaptatifs (9 états) est déclarée mais sa résolution de conflits de frontière, bien que partiellement couverte par l'arbitrage du 2026-04-01, reste incomplète pour deux cellules.**
4. **Le profil AR-réfractaire crée un angle mort sur les proxys** : en combinaison avec `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`, une fenêtre existe où le moteur doit décider sans signal fiable.
5. **Le binding `TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN` dans le LINK dépend d'un `core_ref` pour identifier les targets, mais la syntaxe de résolution de ce `core_ref` n'est pas définie dans le DSL.**
6. **L'invariant `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` est non-patchable mais crée un blocage de déploiement potentiellement illimité** pour les KU créatives sans mécanisme d'escalade déclaré.

---

## Analyse détaillée par axe

---

### Axe 1 — Cohérence interne

#### 1.1 Paramètre orphelin : `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`

- **Élément concerné :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` (Constitution, `[ARBITRAGE_2026_04_01]`)
- **Nature :** Le texte de l'EVENT et de la RULE `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` cite explicitement `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` comme paramètre de seuil. Ce paramètre n'existe pas dans le Référentiel V1.0.
- **Type de problème :** Complétude + Implémentabilité
- **Impact moteur :** Le moteur ne peut pas évaluer la condition de déclenchement de la divergence MSC/perçu. En pratique, soit le mécanisme ne se déclenche jamais, soit il requiert une valeur hardcodée implicite — deux comportements non documentés.
- **Correction à arbitrer :** Créer `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` dans le Référentiel avec valeur de référence, fourchette et scope `runtime_evaluation`. Ajouter le binding LINK correspondant.

---

#### 1.2 Syntaxe `core_ref` non définie dans le LINK

- **Élément concerné :** `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` et `TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN` (LINK)
- **Nature :** Certaines relations dans le LINK utilisent une clé `core_ref:` à l'intérieur du bloc `target:`, alors que la structure canonique des autres bindings utilise uniquement `id:`. Ce champ `core_ref` n'est pas défini dans le Patch DSL ni dans la spec LINK.
- **Type de problème :** Gouvernance + Implémentabilité
- **Impact moteur :** Un parser de LINK qui implémente strictement le DSL ignorerait ces `core_ref`, rendant ces bindings partiellement résolus.
- **Correction à arbitrer :** Soit formaliser `core_ref` comme champ optionnel du bloc `target` dans le Patch DSL et la spec des TYPES LINK, soit supprimer le champ et n'utiliser que `id:` avec un commentaire documentaire.

---

#### 1.3 `INV_AR_N2_SHORT_FORM_REQUIRES_EXPLICIT_PRIORITY` sans mécanisme de déclaration

- **Élément concerné :** `INV_AR_N2_SHORT_FORM_REQUIRES_EXPLICIT_PRIORITY` (Constitution)
- **Nature :** L'invariant exige qu'une "priorité déclarée et stable" soit présente sur toute version courte d'AR-N2. Aucun TYPE, PARAMETER ni champ de schéma n'existe pour porter cette déclaration de priorité dans le Core ou dans un artefact de design.
- **Type de problème :** Complétude + Implémentabilité
- **Impact moteur :** Impossible de valider automatiquement la conformité d'un AR-N2 simplifié : l'invariant est déclaré mais non vérifiable localement.
- **Correction à arbitrer :** Créer un champ `ar_n2_short_form_priority` ou un TYPE de déclaration permettant au moteur de résoudre la priorité VC vs intention de retour de manière déterministe.

---

#### 1.4 `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` incomplète pour les cellules de frontière Sous-défi + Exploration simultané avec Conservateur

- **Élément concerné :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` (Référentiel, `[ARBITRAGE_2026_04_01][MATRIX-01]`)
- **Nature :** La table de priorité couvre 6 paires. La matrice 3×3 génère potentiellement C(5,2)=10 paires de frontière avec le 5ème régime (Détresse). Les paires `Exploration + Conservateur` et `Sous-défi + Détresse` sont couvertes mais la paire `Sous-défi + Consolidation + Exploration` (trois régimes simultanés) n'est pas explicitement résolue.
- **Type de problème :** Complétude
- **Impact moteur :** Oscillation possible si les trois régimes s'activent simultanément. La règle actuelle résout les paires mais pas les triplets.
- **Correction à arbitrer :** Ajouter une règle de résolution pour les conflits à 3 régimes (priorité stricte linéaire ou règle de clôture : appliquer la paire la plus prioritaire et ignorer le troisième régime).

---

### Axe 2 — Solidité théorique

#### Charge cognitive (Sweller / CLT)

- **Point solide :** L'invariant `INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL` et la matrice de feedback obligatoire pour les KU formelles/procédurales limitent l'effet split-attention.
- **Zone de risque :** Aucun mécanisme ne contrôle la charge cognitive *inter-session* : le nombre de KU activées simultanément dans une session n'est pas borné constitutionnellement. La composante R implique des rappels espacés, mais la densité intra-session n'a pas de plafond déclaré.
- **Angle mort :** L'interleaving peut augmenter la charge extrinsèque si plusieurs KU à types hétérogènes (procédurale + créative + formelle) sont mélangées dans la même session. `RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A` conditionne l'interleaving à la composante A, ce qui est partiellement protecteur, mais pas sur la dimension charge.

#### Mémoire / Consolidation (Ebbinghaus / spaced repetition)

- **Point solide :** La composante R est architecturalement robuste. Les multiplicateurs temporels par type de KU (`PARAM_REFERENTIEL_R_MULTIPLIER_*`) sont bien différenciés. La règle de reprise diagnostique après interruption (`RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME`) est correcte.
- **Zone de risque :** Le fallback `×1` pour les KU créatives (`INV_REFERENTIEL_CREATIVE_R_FALLBACK_IS_X1`) signifie que la robustesse temporelle est minimale pour ce type. Si une KU créative est fréquemment sélectionnée mais jamais espacée, la composante R peut être validée sans consolidation réelle.
- **Angle mort :** Aucun mécanisme ne détecte le "massed practice" déguisé : un apprenant qui complète rapidement les 3 réussites consécutives pour A dans la même session, sans espacement, satisfait P et A mais pas R — la logique AND devrait protéger, mais si R est `×1` (créative) le délai peut être très court.

#### Motivation (SDT / expectancy-value)

- **Point solide :** L'axe VC et le patch de relevance en cas de VC basse persistante constituent une réponse raisonnée à la théorie expectancy-value (Eccles). L'invariant `INV_VC_NOT_GENERAL_MOTIVATION_PROXY` protège contre la sur-interprétation.
- **Zone de risque :** Le système n'a pas de mécanisme pour distinguer une VC basse liée au coût perçu (surcharge) d'une VC basse liée à la valeur perçue (non-pertinence). Les deux déclenchent le même patch de relevance, mais les interventions appropriées sont différentes.
- **Angle mort :** La dimension autonomy (SDT) est absente du modèle d'état apprenant. Le degré de choix laissé à l'apprenant n'est capturé par aucun axe ni par aucune règle d'adaptation. `TYPE_AUTONOMY_REGIME` concerne le déploiement, pas le vécu d'autonomie de l'apprenant.

#### Métacognition / SRL (Zimmerman / Pintrich)

- **Point solide :** L'intention de session (forethought SRL) est bien implémentée comme signal non-bloquant. AR-N3 dérivé d'AEQ cible explicitement le self-monitoring.
- **Zone de risque :** La phase de self-reflection SRL (révision post-performance) n'est pas formalisée au-delà d'AR-N2. Un apprenant qui ne complète jamais AR-N2 n'a aucun support structuré de réflexion post-session.
- **Angle mort :** Le mécanisme de divergence MSC/perçu (`RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`) est une excellente base pour détecter la miscalibration, mais il n'inclut pas de mécanisme de rétroaction formatrice à l'apprenant sur cette divergence — le protocole déclenche une action moteur, pas une action pédagogique explicite de sensibilisation métacognitive.

#### Émotions / Engagement (Pekrun / AEQ)

- **Point solide :** La distinction confusion/frustration/anxiété dans AR-N1 est alignée avec l'AEQ et permet une réponse adaptative différenciée.
- **Zone de risque :** Le régime "détresse" est déclaré mais son opérationnalisation concrète (quelle action moteur exacte déclenche-t-il ?) n'est pas documentée dans les ACTIONS de la Constitution. `ACTION_APPLY_LIGHT_REVERSIBLE_SCAFFOLDING` est générique et ne distingue pas détresse de sous-défi.
- **Angle mort :** L'émotion "ennui" (boredom, central dans l'AEQ) n'apparaît pas comme état nominal nommé. Le régime "sous-défi" en est l'approximation, mais la granularité est insuffisante pour distinguer ennui par facilité excessive vs ennui par désengagement thématique.

#### Mastery Learning (Bloom 1968 / Guskey)

- **Point solide :** Le MSC AND strict est théoriquement cohérent avec le mastery learning : maîtrise conditionnelle sur toutes les dimensions.
- **Zone de risque :** La révocation post-maîtrise (`RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`) est paramétrée à 2 échecs consécutifs par défaut. En mastery learning strict, 2 échecs après stabilisation représente un signal faible — le seuil est bas.
- **Angle mort :** Le mastery learning classique prévoit une remédiation différenciée par type d'erreur avant la réitération. La matrice de feedback couvre cela mais son obligation porte uniquement sur les KU formelles et procédurales — les KU déclaratives peuvent être sans matrice de remédiation structurée.

#### Ingénierie pédagogique (ADDIE / Dick & Carey)

- **Point solide :** La séparation Analyse/Design/Runtime est cohérente avec ADDIE. L'obligation d'un contexte authentique pour Bloom ≥ 4 est une contrainte pédagogique solide.
- **Zone de risque :** La phase Évaluation d'ADDIE (formative et sommative continue) est implicitement capturée par le MSC, mais aucune règle ne force une révision périodique du graphe de KU une fois déployé. Un graphe peut vieillir sans déclencheur de révision.
- **Angle mort :** La phase Développement (production des artefacts de feedback et des missions) est hors scope du Core mais constitue le goulot d'étranglement réel du système. Le Core suppose que les artefacts sont préexistants mais ne gouverne pas leur qualité ni leur exhaustivité — uniquement leur existence pour les KU formelles/procédurales.

---

### Axe 3 — États indéfinis moteur

#### 3.1 Tous les axes simultanément unknown

- **Scénario :** AR-N1 absent, AR-N2 non complété, proxys sous le seuil minimum de 2, calibration non disponible.
- **Comportement attendu selon Constitution :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise l'état unknown. `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` impose un scaffolding léger.
- **Comportement non défini :** Que sélectionne le moteur comme contenu ? Quelle KU est prioritaire ? Le régime adaptatif n'est pas défini pour un état totalement unknown. La Constitution ne donne pas de règle de sélection de KU en absence de tout signal.
- **Type de problème :** Complétude / États indéfinis

#### 3.2 KU créative + régime conservateur + AR-N1 absent

- **Scénario :** Apprenant en détresse (conservateur) sur une KU créative, AR-N1 absent (réfractaire), pas de feedback déterministe disponible (`INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH`).
- **Comportement attendu :** KU créative bloquée en mode autonome, scaffolding conservateur appliqué.
- **Comportement non défini :** Si l'unique KU disponible dans la session est créative, le moteur ne peut ni l'exécuter en mode autonome ni proposer un contenu alternatif (aucune règle de fallback de contenu en cas de blocage de toutes les KU). Le moteur oscille ou se bloque.
- **Type de problème :** États indéfinis / Implémentabilité

#### 3.3 Patch relevance + Investigation systémique simultanés

- **Scénario :** `RULE_REFERENTIEL_VC_PERSISTENCE_TRIGGERS_RELEVANCE_PATCH` déclenche un patch relevance pendant une investigation systémique active (`RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR`).
- **Comportement attendu :** L'investigation systémique gèle les ajustements agressifs.
- **Comportement non défini :** Le patch relevance est-il un "ajustement agressif" ou un ajustement borné autorisé pendant l'investigation ? La règle ne qualifie pas le patch relevance dans ce contexte.
- **Type de problème :** États indéfinis / Gouvernance

#### 3.4 `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` + `EVENT_MSC_DOWNGRADE` simultanés

- **Scénario :** MSC se dégrade en même temps qu'une divergence perçue est en cours de résolution.
- **Comportement attendu :** Deux protocoles de diagnostic devraient se déclencher.
- **Comportement non défini :** Aucune règle ne définit la priorité entre la résolution de divergence et la réponse à une rétrogradation active. Le moteur pourrait déclencher deux séquences diagnostiques sur la même KU simultanément.
- **Type de problème :** États indéfinis / Complétude

---

### Axe 4 — Dépendances IA implicites

#### 4.1 Détection de "misconception" (`RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT`)

- **Élément :** `TYPE_KNOWLEDGE_UNIT` + `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT`
- **Dépendance IA implicite :** La Constitution exige qu'une KU soit "flaggée misconception" mais ne définit pas comment ce flag est posé au runtime. En phase design, c'est humain. Au runtime, détecter une misconception à partir des réponses erronées nécessite une classification sémantique des erreurs — ce qui dépasse les règles déterministes.
- **Alternative sans IA continue :** Le flag `misconception` doit être posé exclusivement en phase Analyse/Design (hors session) et encodé dans le graphe. Ajouter un invariant rendant explicite que ce flag est design-time only et non inféré au runtime.

#### 4.2 Évaluation du `ICC` (Corpus Confidence Index)

- **Élément :** `TYPE_CORPUS_CONFIDENCE_ICC`
- **Dépendance IA implicite :** L'ICC qualifie la confiance d'analyse du corpus, mais la procédure de calcul est absente. Dans tout système réel, évaluer un corpus nécessite soit une IA, soit une procédure manuelle explicite.
- **Alternative sans IA continue :** Définir une grille déterministe de critères (exhaustivité thématique, ancienneté, diversité des sources) produisant un score ICC calculable sans inférence sémantique.

#### 4.3 Sélection du "contexte authentique" pour Bloom ≥ 4

- **Élément :** `TYPE_AUTHENTIC_CONTEXT` + `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4`
- **Dépendance IA implicite :** Vérifier qu'un contexte est "authentique" au sens pédagogique implique un jugement sémantique. Le Core ne définit pas les critères de validation d'un contexte authentique.
- **Alternative sans IA continue :** Ajouter une liste de critères déterministes (référence à une situation réelle documentée, datée, identifiable) permettant une validation formelle hors session.

---

### Axe 5 — Gouvernance

#### 5.1 Absence de déclencheur de révision périodique du graphe de KU

- **Élément :** `TYPE_KNOWLEDGE_GRAPH` (Constitution)
- **Nature :** Aucune règle ni événement ne force une révision périodique du graphe une fois déployé. Un graphe produit en phase Analyse peut devenir obsolète sans signal de révision systémique.
- **Type de problème :** Gouvernance / Complétude
- **Correction à arbitrer :** Ajouter un EVENT `EVENT_GRAPH_STALENESS_REVIEW` ou un PARAM de fenêtre de validité du graphe déclenchant une notification de révision.

#### 5.2 `patchable: false` sur `TYPE_MASTERY_COMPONENT_T` sans CONSTRAINT explicite

- **Élément :** `TYPE_MASTERY_COMPONENT_T` (Constitution)
- **Nature :** La composante T est `patchable: false` et `parameterizable: true`. Mais aucune CONSTRAINT ne documente explicitement ce qui est interdit de modifier sur T. À la différence de P, R et A qui ont des paramètres référentiels nommés, T n'a aucun paramètre dans le Référentiel.
- **Type de problème :** Gouvernance / Complétude
- **Correction à arbitrer :** Soit ajouter des paramètres référentiels pour T (critères de validation de transférabilité), soit documenter explicitement que T est intentionnellement hors-paramétrage avec une CONSTRAINT explicative.

#### 5.3 `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` sans canal d'escalade défini

- **Élément :** `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` (Constitution)
- **Nature :** L'invariant exige une "escalade hors session" mais ne définit pas le canal, la forme ni le récepteur de cette escalade. L'escalade est déclarée obligatoire mais inopérable.
- **Type de problème :** Gouvernance / Implémentabilité
- **Correction à arbitrer :** Ajouter une ACTION `ACTION_ESCALATE_UNRESOLVABLE_DRIFT` avec un scope et un canal d'escalade définis (notification humaine, queue de révision, etc.).

#### 5.4 Versioning inter-Core non automatiquement validé

- **Élément :** LINK `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0`
- **Nature :** Le LINK encode les versions des deux Cores dans son `id`. En cas de patch d'un Core (passage à V1.10 ou V2.0), le LINK devient automatiquement obsolète mais aucun mécanisme ne détecte ni ne bloque cet état. Le Patch DSL ne semble pas inclure de validation inter-Core de version.
- **Type de problème :** Gouvernance / Versioning
- **Correction à arbitrer :** Ajouter dans le pipeline de validation (STAGE_04) une vérification que les versions citées dans l'ID du LINK correspondent aux versions courantes des Cores dans `manifest.yaml`.

---

### Axe 6 — Scénarios adversariaux

#### Scénario A : L'apprenant "fantôme AR" + graphe linéaire

**Description :** Un apprenant ne répond jamais aux AR-N1, AR-N2, ni AR-N3 (profil réfractaire confirmé sur la fenêtre configurée). Le graphe est linéaire (chaque KU dépend de la précédente). L'apprenant progresse sur les KU mais avec des performances médiocres.

**Mécanismes activés :**
1. `RULE_REFERENTIEL_AR_REFRACTORY_DETECTION` → flag `profil-ar-refractaire`
2. `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` → régime minimal
3. `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` → scaffolding léger
4. Propagation graphe sur rétrogradation → `INV_GRAPH_PROPAGATION_ONE_HOP`

**Limite révélée :** Le régime minimal et la réponse conservatrice se cumulent indéfiniment. Sans AR, aucun signal ne peut déverrouiller le moteur vers plus de défi. La règle de régime conservateur borné par MOT-01 n'est pas définie dans les Cores actuels — MOT-01 est référencé dans `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` sans exister comme TYPE ou RULE propre.

---

#### Scénario B : Pic de maîtrise provisoire héritée + interruption longue

**Description :** Un apprenant reprend après une interruption longue avec une maîtrise provisoire héritée (`PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`) sur 5 KU. La session diagnostique de reprise couvre 3 KU. Les 2 autres ne sont pas diagnostiquées dans la fenêtre de vérification.

**Mécanismes activés :**
1. `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME` → session diagnostique
2. `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` → fenêtre de confirmation
3. `INV_MSC_AND_STRICT` → si la vérification échoue, rétrogradation

**Limite révélée :** Si les 2 KU non diagnostiquées restent en maîtrise provisoire après la fenêtre, leur statut n'est pas résolu. La Constitution ne définit pas ce qui se passe à l'expiration de la `PROVISIONAL_MASTERY_VERIFICATION_WINDOW` sans vérification : maintien, rétrogradation automatique, ou signal d'alerte ?

---

#### Scénario C : Double déclenchement VC-basse + divergence MSC/perçu

**Description :** Un apprenant atteint le seuil MSC de base (P, R, A validés) sur une KU complexe. Il exprime simultanément une VC basse persistante (axe VC) et un AR-N1 signalant un blocage total (divergence MSC/perçu).

**Mécanismes activés :**
1. `EVENT_PERSISTENT_LOW_VC` → `RULE_PERSISTENT_LOW_VC_TRIGGERS_RELEVANCE_PATCH`
2. `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` → `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`
3. `RULE_REFERENTIEL_VC_PATCH_ESCALATION_AFTER_TWO_CYCLES`

**Limite révélée :** Deux patchs de natures différentes (relevance et diagnostic) sont déclenchés simultanément. Le système n'a pas de règle de séquencement entre eux. Le patch de relevance modifie le contenu contextuel, tandis que le protocole de divergence remet en cause la maîtrise — les deux peuvent se contredire si le diagnostic révèle que la maîtrise est réelle et que la VC basse est purement affective. Aucune règle ne tranche ce conflit.

---

### Axe 7 — Priorisation

| Priorité | ID du problème | Description | Type |
|---|---|---|---|
| **Critique** | 1.1 | `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` absent du Référentiel | Complétude |
| **Critique** | 3.1 | État moteur indéfini quand tous les axes sont unknown simultanément | États indéfinis |
| **Critique** | MOT-01 orphelin | MOT-01 cité dans la règle de conflits adaptatifs sans existence Core | Complétude |
| **Élevé** | 1.2 | Syntaxe `core_ref` non définie dans le DSL LINK | Gouvernance |
| **Élevé** | 3.2 | KU créative + régime conservateur + AR absent = blocage moteur | États indéfinis |
| **Élevé** | Scénario B | Expiration de `PROVISIONAL_MASTERY_VERIFICATION_WINDOW` sans résolution | Complétude |
| **Élevé** | 5.3 | Canal d'escalade `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION` non défini | Implémentabilité |
| **Modéré** | 1.3 | `INV_AR_N2_SHORT_FORM_REQUIRES_EXPLICIT_PRIORITY` non vérifiable localement | Implémentabilité |
| **Modéré** | 3.3 | Patch relevance vs investigation systémique simultanés | États indéfinis |
| **Modéré** | 3.4 | `EVENT_MSC_PERCEPTION_DIVERGENCE` + `EVENT_MSC_DOWNGRADE` simultanés | États indéfinis |
| **Modéré** | 4.1 | Flag misconception : détection runtime impliquant sémantique | Dépendance IA |
| **Modéré** | 5.4 | Versioning LINK non validé automatiquement lors d'un patch Core | Gouvernance |
| **Modéré** | Scénario C | Double déclenchement VC-basse + divergence MSC/perçu non séquencé | Complétude |
| **Faible** | 1.4 | Résolution de triplets de régimes adaptatifs non couverte | Complétude |
| **Faible** | 2-SRL | Absence de feedback formatif sur divergence MSC/perçu vers l'apprenant | Théorique |
| **Faible** | 5.1 | Absence de déclencheur de révision périodique du graphe | Gouvernance |
| **Faible** | 5.2 | Composante T sans paramètres ni CONSTRAINT documentée | Gouvernance |

---

## Corrections à arbitrer avant patch

### C1 — CRITIQUE : Créer `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`
- **Couche :** Référentiel
- **Nature :** Paramètre manquant cité par la Constitution
- **Correction :** Ajouter le paramètre avec valeur de référence (ex. 3 sessions), fourchette (2–5), et scope `runtime_evaluation`
- **Binding LINK :** Créer binding dans `TYPE_BINDING_MSC_COMPONENTS_TO_REFERENTIEL_PARAMETERS` ou nouveau TYPE LINK

### C2 — CRITIQUE : Définir le comportement moteur quand tous les axes sont unknown
- **Couche :** Constitution
- **Nature :** État indéfini moteur
- **Correction :** Ajouter une RULE ou une INVARIANT définissant la sélection de KU en état totalement unknown (ex. sélection prioritaire par graphe topologique depuis les KU racines, Bloom minimal, durée minimale)

### C3 — CRITIQUE : Définir ou supprimer MOT-01
- **Couche :** Référentiel (ou Constitution)
- **Nature :** Référence orpheline dans `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION`
- **Correction :** Soit créer MOT-01 comme RULE ou PARAM borné définissant l'exception motivationnelle au régime conservateur, soit supprimer la référence et adopter une règle conservative sans exception

### C4 — ÉLEVÉ : Formaliser `core_ref` dans le Patch DSL ou supprimer le champ
- **Couche :** Spec Patch DSL + LINK
- **Nature :** Syntaxe non définie
- **Correction :** Arbitrer si `core_ref` est un champ documentaire ou structurel, puis homogénéiser les bindings LINK

### C5 — ÉLEVÉ : Définir le sort de la `PROVISIONAL_MASTERY_VERIFICATION_WINDOW` à expiration sans vérification
- **Couche :** Constitution
- **Nature :** État indéfini
- **Correction :** Ajouter un EVENT `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` avec effet explicite (rétrogradation automatique ou notification humaine selon le niveau d'autonomie)

### C6 — ÉLEVÉ : Créer `ACTION_ESCALATE_UNRESOLVABLE_DRIFT`
- **Couche :** Constitution
- **Nature :** Invariant sans canal opérationnel
- **Correction :** Décrire le canal (queue, notification, flag hors-session) et le récepteur de l'escalade

### C7 — MODÉRÉ : Ajouter un RULE de séquencement entre patch relevance et protocole de divergence MSC/perçu
- **Couche :** Constitution ou Référentiel
- **Nature :** Conflit non résolu entre deux déclenchements simultanés
- **Correction :** Définir la priorité : divergence MSC/perçu prend la priorité sur le patch relevance (le diagnostic doit d'abord confirmer ou infirmer la maîtrise avant d'agir sur la contextualisation)

### C8 — MODÉRÉ : Rendre le flag misconception explicitement design-time only
- **Couche :** Constitution
- **Nature :** Dépendance IA implicite
- **Correction :** Ajouter un INVARIANT `INV_MISCONCEPTION_FLAG_IS_DESIGN_TIME_ONLY` interdisant toute inférence runtime de ce flag

---

*Fin du rapport — challenge_report_BIS_GPTThink.md*
