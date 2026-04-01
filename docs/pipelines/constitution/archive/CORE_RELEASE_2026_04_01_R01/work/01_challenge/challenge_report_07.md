# CHALLENGE REPORT — Run 07

**Pipeline:** constitution  
**Stage:** STAGE_01_CHALLENGE  
**Date:** 2026-03-31  
**Cores analysés:** Constitution v1.8 · Référentiel v0.6 · LINK V1_8__V0_6_FINAL  

---

## Résumé exécutif

Le système Constitution v1.8 / Référentiel v0.6 / LINK est architecturalement solide et bien structuré. La séparation des couches est respectée, les invariants clés (AND strict MSC, propagation 1-saut, localité runtime) sont protégés. Cependant, **six zones de risque significatives** ont été identifiées, dont deux de niveau critique et deux de niveau élevé, touchant principalement les états indéfinis moteur, les dépendances IA implicites résiduelles, et certaines lacunes de fermeture dans les bindings LINK.

---

## Axe 1 — Cohérence interne

### Anomalie 1.1 — Désynchronisation de version inter-Core [ÉLEVÉ]

La Constitution `V1_8_FINAL` contient `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` qui pointe correctement vers `v0.6`. Mais le Référentiel `V0_6_FINAL` contient `REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL` avec le libellé `human_readable: Référence explicite vers le Core Constitution Learn-it v1.7.` — la version mentionnée est **v1.7** alors que le Core cible est v1.8. C'est une désynchronisation de label qui peut induire une confusion de traçabilité lors d'un audit.

### Anomalie 1.2 — Même désynchronisation dans le LINK [ÉLEVÉ]

`LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_8` a pour `human_readable` : *"Référence explicite vers le Core Constitution Learn-it **v1.7**"*. Le LINK a été partiellement mis à jour dans son `id` (v1.8) mais pas dans son libellé descriptif, créant une incohérence documentaire systémique.

### Anomalie 1.3 — Binding LINK partiel sur la composante T [MODÉRÉ]

`TYPE_MASTERY_COMPONENT_T` (transférabilité) est déclarée dans la Constitution et dépend de `TYPE_MASTERY_MODEL`, mais elle est **absente des bindings LINK** (`TYPE_BINDING_MSC_COMPONENTS_TO_REFERENTIEL_PARAMETERS` ne couvre que P, R, A). Il n'existe pas non plus de paramètre Référentiel pour T. La fermeture inter-Core de T est donc implicite : elle repose sur le fait qu'aucun paramètre n'est nécessaire, mais ce n'est pas explicitement justifié ni documenté dans le LINK.

### Anomalie 1.4 — `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` sans binding Référentiel [MODÉRÉ]

Ce paramètre est déclaré dans la Constitution (`[S2][S20]`, `patchable: true`) mais n'a aucun correspondant dans le Référentiel ni dans le LINK. Son seuil opérationnel (nombre de sessions, fenêtre temporelle) est donc entièrement indéterminé à l'exécution.

### Anomalie 1.5 — `RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A` sans référence croisée [FAIBLE]

Cette règle Référentiel exige que la composante A soit "au seuil sur les KU concernées", mais ne croise pas `PARAM_REFERENTIEL_MSC_AUTONOMY_SUCCESS_COUNT`. Elle duplique partiellement la logique sans binding explicite.

---

## Axe 2 — Solidité théorique

### Anomalie 2.1 — Manque d'un mécanisme de charge cognitive cumulée en session [ÉLEVÉ]

Le garde-fou `PARAM_REFERENTIEL_COGNITIVE_FATIGUE_MINUTES_GUARDRAIL` (25 min) est déclaré comme *"garde-fou de dernier recours"*, mais aucun mécanisme intermédiaire progressif de charge cognitive n'est modélisé. La Constitution déclare bien la composante A (autonomie) mais ne dispose d'aucune règle de ralentissement adaptatif basée sur la fatigue in-session avant le seuil de 25 min. Il y a un saut conceptuel entre l'état apprenant composite (3 axes) et la gestion de la charge cognitive intra-session.

### Anomalie 2.2 — Consolidation mémorielle : pas de lien entre R et la structure des pauses [MODÉRÉ]

La robustesse R est bien définie avec des délais courts/moyens, mais aucune règle ne prescrit une structure de session minimale assurant la consolidation (ex. : espacement des rappels, interleaving de renforcement). L'interleaving est bien couvert, mais son lien à la consolidation mémorielle à long terme (courbe d'oubli, effet test) n'est pas explicitement ancré dans un invariant.

### Anomalie 2.3 — Métacognition et SRL : AR-N3 est le seul vecteur, sans feedback en boucle [MODÉRÉ]

Le SRL (Self-Regulated Learning) n'est activé que par AR-N3 (bilan périodique) et l'intention de session (AR-N2 partiel). Il n'existe pas de mécanisme constitutionnel de feedback de progrès visible à l'apprenant entre deux bilans AR-N3. Le `RULE_SESSION_INTENTION_NON_BLOCKING` est bien posé mais aucune règle ne garantit que l'apprenant reçoit un signal de progression régulier pour alimenter sa métacognition.

---

## Axe 3 — États indéfinis moteur

### Anomalie 3.1 — Maîtrise provisoire non vérifiée à l'expiration [CRITIQUE]

`PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` déclare une fenêtre de vérification, mais aucun événement ni règle ne définit ce que le moteur fait **à l'expiration** de cette fenêtre si la vérification n'a pas eu lieu (ex. : session annulée, apprenant inactif). Le moteur peut osciller entre maintenir la maîtrise provisoire indéfiniment ou la révoquer sans règle explicite.

### Anomalie 3.2 — Conflit entre `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` et `RULE_REFERENTIEL_ADAPTIVE_REGIME_DETECTION_MIN_PROXIES` [CRITIQUE]

L'invariant constitutionnel exige un scaffolding léger conservateur en absence d'AR-N1. La règle Référentiel exige **au moins 2 proxys franchissant leur seuil** pour détecter un régime adaptatif. Si aucun proxy ne franchit son seuil ET qu'AR-N1 est absent, le moteur est dans un état potentiellement bloquant : ni régime adaptatif détectable, ni AR-N1 disponible. La réponse conservatrice s'applique, mais sa définition opérationnelle (quel scaffolding ? quelle durée ?) n'est pas fermée dans le Référentiel. Il s'agit d'un état de sous-déterminisme résiduel.

### Anomalie 3.3 — Propagation secondaire : délai "1 session" indéfini en inactivité réelle [MODÉRÉ]

`PARAM_REFERENTIEL_PROPAGATION_CHECK_MAX_DELAY_SESSIONS` impose "1 session" de délai maximal pour la vérification de propagation. Mais si l'apprenant ne revient pas dans le système, le délai est indéfini en termes réels. Il n'existe aucun mécanisme d'expiration ou de reclassification après une inactivité prolongée dépassant ce 1-session théorique.

### Anomalie 3.4 — Investigation systémique sans trigger défini [ÉLEVÉ]

`RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR` prescrit un comportement (gel des ajustements agressifs, mode minimal) pendant une investigation systémique active, mais aucun élément du système ne définit **qui ou quoi déclenche l'ouverture** d'une investigation systémique. Il n'existe ni event, ni rule, ni paramètre dans la Constitution ou le LINK qui produise un trigger pour ce mode. Il s'agit d'un état invocable uniquement par une décision humaine externe non tracée dans les Cores.

---

## Axe 4 — Dépendances IA implicites

### Anomalie 4.1 — Détection de misconception non opérationnalisée [ÉLEVÉ]

`RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` est bien posée (une misconception → mission de conflit cognitif obligatoire), mais nulle part dans la Constitution ou le Référentiel n'est précisé **comment le moteur détecte** une misconception de manière locale et déterministe. En l'absence d'un sous-type `KU_MISCONCEPTION` avec une source de signal déterministe (flag explicite en design, pattern d'erreur récurrent), la détection reste dépendante d'une inférence sémantique ou d'un flag humain externe. L'invariant `INV_NO_RUNTIME_CONTENT_GENERATION` protège le contenu, mais pas la logique de détection.

### Anomalie 4.2 — `TYPE_CORPUS_CONFIDENCE_ICC` sans méthode de calcul bornée [MODÉRÉ]

L'ICC (Indice de confiance du corpus) qualifie la confiance d'analyse, mais son mode de calcul n'est défini ni dans la Constitution ni dans le Référentiel. Il n'y a pas de paramètre ICC_THRESHOLD, pas de règle de fallback si ICC est bas, et aucun binding LINK associé. Si l'ICC est bas, le système peut continuer sans signal d'alerte structuré.

### Anomalie 4.3 — `TYPE_FEEDBACK_COVERAGE_MATRIX` : signal non bloquant en déploiement [FAIBLE]

La matrice est obligatoire en Design, mais si elle est absente ou incomplète au runtime, le fallback générique s'applique (`RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK`). Aucun invariant ne bloque le déploiement d'une KU formelle ou procédurale sans matrice suffisamment couverte. La couverture minimale (seuil 70% Référentiel) ne constitue qu'un signal, pas un bloquant de déploiement.

---

## Axe 5 — Gouvernance

### Anomalie 5.1 — `patchable: false` sur des bindings LINK limitant l'évolution de T [FAIBLE]

Plusieurs éléments portant `patchable: false` dans le LINK (tous les bindings) semblent corrects par construction, mais `TYPE_BINDING_MSC_COMPONENTS_TO_REFERENTIEL_PARAMETERS` devrait pouvoir être étendu si une composante T devient paramétrisée. L'immuabilité des bindings LINK est une décision de gouvernance volontaire, mais elle peut devenir un frein si T évolue.

### Anomalie 5.2 — Absence de versioning du LINK indépendant [MODÉRÉ]

Le LINK porte une version composite `V1_8__V0_6_FINAL` qui couple sa version aux deux Cores qu'il relie. Si l'un des deux Cores patch sans modification du LINK, la version reste cohérente. Mais si le LINK doit évoluer indépendamment (ex. : correction d'un binding), il n'existe pas de mécanisme de version LINK autonome, ce qui peut compliquer la traçabilité des releases combinées.

### Anomalie 5.3 — Absence de promotion conditionnelle du LINK lors d'un patch Core [MODÉRÉ]

Le pipeline constitution traite les patches des Cores indépendamment, mais si un patch Constitution crée un nouveau type ou paramètre nécessitant un binding LINK, rien dans la pipeline ne force une révision synchronisée du LINK. La règle `CONSTRAINT_LINK_NO_BUSINESS_LOGIC` protège la structure, mais n'exige pas de révision du LINK lors d'une promotion de Core.

---

## Synthèse des risques

| Priorité | ID | Libellé court | Core concerné |
|---|---|---|---|
| **CRITIQUE** | 3.1 | Maîtrise provisoire : état indéfini à expiration | Constitution |
| **CRITIQUE** | 3.2 | Conflit conservateur / régime adaptatif sans proxy ni AR-N1 | Constitution + Référentiel |
| **ÉLEVÉ** | 1.1 + 1.2 | Désynchronisation label v1.7 dans Référentiel et LINK | Référentiel, LINK |
| **ÉLEVÉ** | 3.4 | Investigation systémique sans trigger défini | Référentiel |
| **ÉLEVÉ** | 4.1 | Détection misconception non opérationnalisée localement | Constitution |
| **ÉLEVÉ** | 2.1 | Charge cognitive intra-session non modélisée progressivement | Constitution + Référentiel |
| **MODÉRÉ** | 1.3 | Composante T sans binding LINK ni paramètre Référentiel | LINK |
| **MODÉRÉ** | 1.4 | `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` sans paramètre Référentiel | Constitution + Référentiel |
| **MODÉRÉ** | 2.2 | Consolidation mémorielle R sans lien à structure des pauses | Constitution + Référentiel |
| **MODÉRÉ** | 2.3 | SRL sans feedback de progrès inter-AR-N3 | Constitution |
| **MODÉRÉ** | 3.3 | Propagation secondaire : "1 session" indéfini en inactivité réelle | Référentiel |
| **MODÉRÉ** | 4.2 | ICC sans méthode de calcul ni seuil | Constitution |
| **MODÉRÉ** | 5.2 | Absence de versioning LINK autonome | LINK |
| **MODÉRÉ** | 5.3 | Pas de révision LINK forcée lors d'un patch Core | Pipeline |
| **FAIBLE** | 1.5 | `RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A` sans binding croisé | Référentiel |
| **FAIBLE** | 4.3 | Matrice feedback : signal non bloquant en déploiement | Constitution + Référentiel |
| **FAIBLE** | 5.1 | Bindings LINK immuables limitent l'évolution de T | LINK |

---

## Corrections à arbitrer avant STAGE_02

1. **[CRITIQUE 3.1]** Définir un event `EVENT_PROVISIONAL_MASTERY_VERIFICATION_EXPIRED` et une règle de reclassification.  
   Arbitrage requis : révoquer automatiquement → retour au dernier état stable, ou seulement marquer "à vérifier" → reprise diagnostique obligatoire à la prochaine session ?

2. **[CRITIQUE 3.2]** Définir dans le Référentiel une règle/action pour le cas `absence AR-N1 + 0 proxy franchissant seuil`.  
   Arbitrage requis : le mode conservateur est-il suffisant comme état stable documenté, ou faut-il introduire un paramètre `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_DEFINITION` pour fermer opérationnellement ce cas ?

3. **[ÉLEVÉ 1.1 + 1.2]** Corriger les libellés `human_readable` dans `REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL` et `LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_8` de "v1.7" → "v1.8". Patch mineur, mais bloquant pour la traçabilité d'audit.

4. **[ÉLEVÉ 3.4]** Arbitrage requis : faut-il un event `EVENT_SYSTEMIC_INVESTIGATION_OPENED` déclenché par un critère déterministe (ex. : N dérives non résolues sur M cycles), ou ce déclenchement reste-t-il intentionnellement hors-système (décision humaine uniquement) ?

5. **[ÉLEVÉ 4.1]** Arbitrage requis : la détection de misconception doit-elle être un flag de Design (KU taguée `misconception: true` explicitement par le concepteur), ou peut-elle être inférée à partir d'un pattern d'erreur récurrent ? Si inférée, définir les critères déterministes dans le Référentiel.

6. **[ÉLEVÉ 2.1]** Arbitrage requis : faut-il introduire un paramètre `PARAM_REFERENTIEL_COGNITIVE_FATIGUE_SOFT_GUARDRAIL_MINUTES` intermédiaire (ex. 15 min) avec une action de réduction adaptative de difficulté avant le garde-fou disjonctif de 25 min ?

7. **[MODÉRÉ 1.3 + 1.4]** Décider si T et `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` nécessitent des entrées Référentiel et des bindings LINK, ou si leur absence paramétrique est intentionnelle (T entièrement qualitative, fenêtre laissée au design local).
