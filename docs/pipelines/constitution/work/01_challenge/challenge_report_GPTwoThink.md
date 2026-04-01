# CHALLENGE REPORT — Constitution Learn-it V1_9_FINAL

**pipeline:** constitution  
**stage:** STAGE_01_CHALLENGE  
**core_version:** CORE_LEARNIT_CONSTITUTION_V1_9  
**date:** 2026-04-01  
**challenger:** GPTwoThink  

---

## Résumé exécutif

La Constitution V1.9 FINAL présente un niveau de maturité structurelle élevé : séparation Constitution/Référentiel affirmée, invariants non-patchables verrouillés, logique AND du MSC protégée, architecture offline-first cohérente. Les PATCH_V1_9 apportent des corrections importantes (acyclicité, propagation secondaire, KU sans type, patch pré-sessionnel).

Cependant, cinq zones de risque subsistent, dont deux critiques :

1. **Délégation opaque au Référentiel sans borne constitutionnelle de sécurité** — plusieurs règles et événements ne s'activent que si un seuil Référentiel est atteint, mais la Constitution ne pose aucun plancher de sécurité si le Référentiel est absent ou malformé.
2. **Absence d'un événement/invariant couvrant la perte de cohérence du graphe à la mise à jour** — seule la *construction* initiale est protégée par `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` ; une modification incrémentale (patch sur le graphe) peut réintroduire un cycle sans déclenchement d'invariant.
3. Le protocole `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` est incomplet : la condition de fin de boucle n'est pas bornée constitutionnellement.
4. L'événement `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` crée une dépendance à `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` sans déclarer quel paramètre Référentiel est requis au niveau constitutionnel.
5. L'axe T est séparé de la maîtrise de base mais le `TYPE_MASTERY_MODEL` ne déclare aucune relation vers `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`, créant une dépendance logique implicite.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### 1.1 Dépendance circulaire implicite entre TYPE_MASTERY_MODEL et INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY

- **Élément concerné :** `TYPE_MASTERY_MODEL`, `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`
- **Problème :** `TYPE_MASTERY_MODEL` déclare `depends_on: [TYPE_MASTERY_COMPONENT_P, R, A, T]` et une relation `governs → INV_MSC_AND_STRICT`. Mais `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` qui contraint `TYPE_MASTERY_MODEL` n'est référencé *dans aucune relation depuis* `TYPE_MASTERY_MODEL`. La séparation T est donc un invariant "orphelin" du point de vue de la traversée graphe des relations.
- **Risque moteur :** Un moteur qui parcourt les relations depuis `TYPE_MASTERY_MODEL` ne verra pas `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` comme contrainte active. Risque de déploiement d'une implémentation qui inclut T dans le calcul AND sans être bloquée.
- **Couche :** Constitution
- **Priorité :** élevée

#### 1.2 INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC ne couvre pas les mises à jour incrémentielles

- **Élément concerné :** `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` — `source_anchor: [S4][S18][PATCH_V1_9]`
- **Problème :** Le trigger est `Validation design ou chargement du graphe`. Un patch qui *modifie* le graphe après le chargement initial (ajout d'arête ou de KU) ne déclenche pas cet invariant selon la logique actuelle.
- **Risque moteur :** Un cycle peut être réintroduit via un patch de graphe approuvé localement (impact_scope calculable, structure valide) sans que le moteur soit bloqué.
- **Couche :** Constitution
- **Priorité :** critique

#### 1.3 Délégation sans plancher de sécurité constitutionnel pour les seuils Référentiel

- **Éléments concernés :**
  - `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME` — condition : `durée > seuil_R`
  - `EVENT_PERSISTENT_LOW_VC` — condition : `seuil référentiel atteint`
  - `EVENT_AR_REFRACTORY_PROFILE_DETECTED` — condition : `seuil référentiel atteint`
  - `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` — dépend de `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`
- **Problème :** Aucun invariant constitutionnel ne définit ce qui se passe si le Référentiel ne fournit pas ces seuils (Référentiel absent, version incompatible, paramètre manquant). La Constitution délègue mais ne pose pas de règle de fallback constitutionnelle pour l'absence du seuil.
- **Risque moteur :** Le moteur peut osciller indéfiniment sur un trigger conditionnel dont la condition est indéterminable. Ou ne jamais déclencher une règle de sécurité critique (diagnostique de reprise, escalade VC).
- **Couche :** Constitution/Référentiel (placement à arbitrer)
- **Priorité :** critique

#### 1.4 RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL — absence de borne de fin de boucle constitutionnelle

- **Élément concerné :** `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` — `source_anchor: [ARBITRAGE_2026_04_01][DIVMSC-01]`
- **Problème :** Le protocole en deux étapes (diagnostique → escalade si persistance) ne définit pas constitutionnellement ce qui constitue "persistance après diagnostique". Ce seuil est implicitement délégué au Référentiel mais non déclaré dans `depends_on` ni dans la logique.
- **Risque moteur :** Boucle potentielle diagnostique → escalade → diagnostique si l'escalade ne modifie pas le design dans une fenêtre définie. État oscillatoire non borné.
- **Couche :** Constitution
- **Priorité :** élevée

#### 1.5 TYPE_MASTERY_COMPONENT_P, R, A — depends_on REF_CORE sans précision du paramètre requis

- **Éléments concernés :** `TYPE_MASTERY_COMPONENT_P`, `TYPE_MASTERY_COMPONENT_R`, `TYPE_MASTERY_COMPONENT_A`
- **Problème :** Ces composantes déclarent `depends_on: [REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION]` sans préciser *quel(s) paramètre(s) Référentiel* sont requis pour leur calcul. La Constitution sait que P, R, A dépendent du Référentiel pour les seuils, mais n'explicite pas cette interface.
- **Risque moteur :** Un Référentiel partiellement défini ou d'une version ultérieure peut omettre un paramètre utilisé par P ou R sans que la fédération inter-Core détecte le problème au niveau constitutionnel.
- **Couche :** Constitution/Référentiel (interface à préciser)
- **Priorité :** modérée

---

### Axe 2 — Solidité théorique

#### 2.1 Charge cognitive — absence de contrainte constitutionnelle sur la densité de sollicitation AR dans une session

- **Élément concerné :** `TYPE_SELF_REPORT_AR_N1`, `PARAM_AR_N1_INTERACTION_BUDGET`
- **Problème :** `PARAM_AR_N1_INTERACTION_BUDGET` est décrit comme "question concise et locale". Mais aucune règle constitutionnelle ne borne la *fréquence maximale* d'AR-N1 dans une session, ni ne protège contre une accumulation de micro-sondages nuisant à l'immersion cognitive (charge extrinsèque).
- **Risque moteur :** En présence de nombreux événements déclencheurs simultanés, le moteur peut légitimement empiler des AR-N1 sans limite.
- **Couche :** Constitution (borne de fréquence) / Référentiel (valeur exacte)
- **Priorité :** modérée

#### 2.2 Mastery learning — INV_MSC_AND_STRICT sans mécanisme de dégradation partielle documenté

- **Élément concerné :** `INV_MSC_AND_STRICT`, `EVENT_MSC_DOWNGRADE`
- **Problème :** Le AND strict est justifié pédagogiquement, mais la Constitution ne décrit pas le comportement du moteur lorsqu'une seule composante (ex : R seul) passe sous seuil après une longue interruption. L'`EVENT_MSC_DOWNGRADE` se déclenche, mais l'état intermédiaire ("maîtrise partielle R dégradée, P et A toujours valides") n'est pas formalisé.
- **Risque moteur :** Implémentations divergentes selon que "toute la maîtrise est révoquée" ou "seul R est marqué insuffisant" lors de la rétrogradation partielle.
- **Couche :** Constitution
- **Priorité :** élevée

#### 2.3 Émotions / engagement — INV_CONSERVATIVE_RULE_WITHOUT_AR_N1 ne distingue pas les types d'activation négative

- **Élément concerné :** `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`
- **Problème :** En absence d'AR-N1, le scaffolding léger réversible est appliqué uniformément. Mais les trois états négatifs distinguables par AR-N1 (confusion, frustration, anxiété) appellent des interventions différentes. La règle conservatrice n'est pas stratifiée selon la détectabilité des proxys comportementaux disponibles.
- **Couche :** Constitution
- **Priorité :** faible

#### 2.4 Ingénierie pédagogique — TYPE_FEEDBACK_COVERAGE_MATRIX obligatoire uniquement pour KU formelles ou procédurales

- **Élément concerné :** `TYPE_FEEDBACK_COVERAGE_MATRIX` — condition : `KU formelles ou procédurales présentes`
- **Problème :** Les KU perceptuelles ne sont pas explicitement listées dans la condition d'obligation de la matrice. Or `INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL` les identifie comme nécessitant un traitement spécifique.
- **Risque moteur :** Une KU perceptuelle peut être déployée sans matrice feedback complète alors que son feedback multimodal est obligatoire.
- **Couche :** Constitution
- **Priorité :** modérée

---

### Axe 3 — États indéfinis moteur

#### 3.1 État indéfini : graphe avec cycle post-patch (cf. 1.2)

Voir 1.2 — état critique non couvert.

#### 3.2 État indéfini : Référentiel absent lors de l'évaluation d'un seuil conditionnel (cf. 1.3)

Voir 1.3 — état critique non couvert.

#### 3.3 État indéfini : KU avec type invalide (non absent, mais invalide)

- **Élément concerné :** `INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK`
- **Problème :** L'invariant couvre `type absent, indéterminé ou invalide`. Mais la logique ne précise pas ce qu'est un "type invalide" — valeur hors taxonomie acceptée ? version dépréciée ? Ce critère d'invalidité n'est pas défini constitutionnellement.
- **Risque moteur :** Deux implémentations peuvent diverger sur ce qui constitue un type invalide.
- **Couche :** Constitution
- **Priorité :** modérée

#### 3.4 État indéfini : AR-N2 forme courte sans priorité déclarée

- **Élément concerné :** `INV_AR_N2_SHORT_FORM_REQUIRES_EXPLICIT_PRIORITY`
- **Problème :** L'invariant impose une priorité déclarée et stable. Mais il ne décrit pas le comportement du moteur si aucune priorité n'a été déclarée (au déploiement ou au design). Absence de règle de fallback ou d'état d'erreur explicite.
- **Risque moteur :** Le moteur peut inférer implicitement une priorité par défaut, violant l'invariant.
- **Couche :** Constitution
- **Priorité :** faible

---

### Axe 4 — Dépendances IA implicites

#### 4.1 RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT — détection de la misconception

- **Élément concerné :** `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT`
- **Problème :** La règle se déclenche sur `KU flaggée misconception`. Mais le *processus de flagging* n'est pas décrit dans la Constitution. Si ce flagging est automatique (inférence sémantique depuis le corpus), cela constitue une dépendance IA implicite au stade de l'analyse.
- **Risque :** La Constitution implique un jugement qualitatif (identifier une misconception) sans le contraindre à être humain ou déterministe.
- **Couche :** Constitution/Analyse (à clarifier)
- **Priorité :** modérée

#### 4.2 TYPE_CORPUS_CONFIDENCE_ICC — critères d'évaluation non définis

- **Élément concerné :** `TYPE_CORPUS_CONFIDENCE_ICC`
- **Problème :** L'effet est "qualifie la confiance d'analyse" mais les critères de calcul sont entièrement délégués. Aucune borne constitutionnelle ne définit ce qu'est un corpus "insuffisant" pour déploiement.
- **Risque :** Un ICC très bas peut autoriser un déploiement pédagogiquement non fiable sans invariant constitutionnel bloquant.
- **Couche :** Constitution (seuil minimal de déploiement)
- **Priorité :** modérée

#### 4.3 RULE_AR_N1_OVERRIDES_PROXY — proxys comportementaux non définis constitutionnellement

- **Élément concerné :** `RULE_AR_N1_OVERRIDES_PROXY`
- **Problème :** La règle mentionne les "proxys" comme source alternative à AR-N1, mais la Constitution ne liste ni ne contraint ces proxys. Leur nature reste implicite, laissant ouvert le recours à une inférence continue non encadrée.
- **Couche :** Constitution / Référentiel (à arbitrer)
- **Priorité :** modérée

---

### Axe 5 — Gouvernance

#### 5.1 PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW — paramètre patchable sans contrainte de rollback

- **Élément concerné :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` — `patchable: true`
- **Problème :** Ce paramètre est déclaré patchable. Mais aucune contrainte ne protège contre un patch qui étendrait la fenêtre indéfiniment (ou à zéro). La CONSTRAINT_NO_ADAPTIVE_PHILOSOPHY_CHANGE ne couvre pas explicitement ce paramètre, et la borne valide n'est pas définie constitutionnellement.
- **Risque :** Dérive possible de la politique de maîtrise provisoire par patch non contrôlé.
- **Couche :** Constitution
- **Priorité :** modérée

#### 5.2 TYPE_FEEDBACK_COVERAGE_MATRIX et TYPE_AUTHENTIC_CONTEXT — patchable: true sans protection contre régression

- **Éléments concernés :** `TYPE_FEEDBACK_COVERAGE_MATRIX` (`patchable: true`), `TYPE_AUTHENTIC_CONTEXT` (`patchable: true`)
- **Problème :** Ces deux types sont patchables. Pour `TYPE_FEEDBACK_COVERAGE_MATRIX`, un patch pourrait réduire la couverture d'erreurs. Pour `TYPE_AUTHENTIC_CONTEXT`, un patch pourrait affaiblir la condition d'autorisation de Bloom ≥ 4. Aucune règle constitutionnelle ne protège contre un patch régressif sur ces éléments (hors le mécanisme générique de QA pédagogique).
- **Couche :** Constitution
- **Priorité :** élevée

#### 5.3 Absence de versionning inter-Core — la Constitution référence V1_0 du Référentiel

- **Élément concerné :** `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION`
- **Problème :** La référence est fixée à `V1_0`. Si le Référentiel évolue (V1_1, V2_0), la Constitution ne décrit pas le processus de mise à jour de cette référence. Le champ `patchable: false` interdit un patch simple de la référence, mais aucun mécanisme de release coordonnée n'est décrit au niveau constitutionnel.
- **Couche :** Gouvernance inter-Core
- **Priorité :** élevée

#### 5.4 ACTION_TRIGGER_RELEVANCE_PATCH et ACTION_TRIGGER_AR_SOLLICITATION_PATCH — patchable: true sans borne de fréquence

- **Éléments concernés :** `ACTION_TRIGGER_RELEVANCE_PATCH`, `ACTION_TRIGGER_AR_SOLLICITATION_PATCH` (tous deux `patchable: true`)
- **Problème :** Ces actions peuvent être déclenchées par des événements récurrents. Si un patch de relevance est déclenché plusieurs fois dans une courte fenêtre, aucune règle constitutionnelle ne limite la fréquence ou n'impose un délai de stabilisation entre deux patches.
- **Couche :** Constitution / Référentiel (à arbitrer)
- **Priorité :** modérée

---

### Axe 6 — Priorisation

| Priorité | ID faille | Axe | Titre court |
|----------|-----------|-----|-------------|
| **critique** | F-1.2 | 1 / 3 | Cycle graphe non détecté post-patch |
| **critique** | F-1.3 | 1 / 3 | Délégation seuil Référentiel sans fallback constitutionnel |
| **élevée** | F-1.1 | 1 | INV_TRANSFER orphelin dans les relations TYPE_MASTERY_MODEL |
| **élevée** | F-1.4 | 1 / 3 | Boucle diagnostique divergence MSC non bornée |
| **élevée** | F-2.2 | 2 | Rétrogradation MSC partielle — état intermédiaire non défini |
| **élevée** | F-5.2 | 5 | Patch régressif sur FEEDBACK_COVERAGE_MATRIX et AUTHENTIC_CONTEXT |
| **élevée** | F-5.3 | 5 | Pas de mécanisme de mise à jour de référence inter-Core |
| **modérée** | F-1.5 | 1 | Interface paramètres P/R/A→Référentiel non déclarée |
| **modérée** | F-2.4 | 2 | Matrice feedback non obligatoire pour KU perceptuelles |
| **modérée** | F-3.3 | 3 | Critères de validité du type KU non définis |
| **modérée** | F-4.1 | 4 | Flagging misconception — risque d'inférence IA implicite |
| **modérée** | F-4.2 | 4 | ICC sans seuil minimal de déploiement constitutionnel |
| **modérée** | F-4.3 | 4 | Proxys comportementaux non définis constitutionnellement |
| **modérée** | F-5.1 | 5 | PARAM_PROVISIONAL_MASTERY sans borne anti-dérive |
| **modérée** | F-5.4 | 5 | Fréquence de déclenchement des patches relevance/AR non bornée |
| **faible** | F-2.1 | 2 | Fréquence AR-N1 non bornée constitutionnellement |
| **faible** | F-2.3 | 2 | Scaffolding conservatif non stratifié par type d'activation |
| **faible** | F-3.4 | 3 | AR-N2 sans priorité — absence de fallback d'état d'erreur |

---

## Corrections à arbitrer avant patch

1. **[critique] Étendre INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC** pour couvrir les modifications incrémentielles du graphe (trigger à ajouter : validation post-patch de graphe), ou introduire un invariant dédié.

2. **[critique] Introduire un invariant de sécurité pour les seuils Référentiel non fournis** — soit une règle constitutionnelle de fallback (comportement défini sans seuil), soit une précondition de déploiement exigeant que tous les paramètres requis soient fournis avant l'activation du moteur.

3. **[élevée] Ajouter une relation depuis TYPE_MASTERY_MODEL vers INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY** pour que la contrainte de séparation de T soit traversable depuis le type racine.

4. **[élevée] Borner constitutionnellement la fin de boucle de RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL** — introduire un paramètre (ou référence Référentiel déclarée) délimitant "persistance après diagnostique", avec un état terminal constitutionnel clair.

5. **[élevée] Définir le comportement moteur lors d'une rétrogradation MSC partielle** — préciser si la maîtrise est entièrement révoquée ou si seule la composante échouante est marquée insuffisante, et l'état intermédiaire de l'apprenant pendant la phase diagnostique.

6. **[élevée] Protéger TYPE_FEEDBACK_COVERAGE_MATRIX et TYPE_AUTHENTIC_CONTEXT contre les patchs régressifs** — introduire une contrainte ou un critère de QA spécifique à ces types patchables.

7. **[élevée] Définir un mécanisme de release coordonnée inter-Core** — pour permettre la mise à jour de `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` sans violer l'immuabilité du champ `patchable: false`.

8. **[modérée] Étendre la condition d'obligation de TYPE_FEEDBACK_COVERAGE_MATRIX aux KU perceptuelles** (alignement avec INV_NO_TEXT_ONLY_FOR_PROCEDURAL_OR_PERCEPTUAL).

9. **[modérée] Définir constitutionnellement les critères de validité d'un type KU** (à distinguer de l'absence de type).

10. **[modérée] Déclarer l'interface paramétrique Constitution→Référentiel pour les composantes P, R, A** — nommer les paramètres Référentiel attendus dans les depends_on ou dans un bloc DEPENDENCIES dédié.
