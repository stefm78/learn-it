# Référentiel de defaults pédagogiques – Learn-it (v0.1)

> **Statut et gouvernance** : Ce document est le complément opérationnel de la Constitution v1.2. Il contient l'ensemble des seuils, valeurs de référence, opérationnalisations et décisions de déploiement qui ont été extraits de la constitution lors du passage en v1.2. Il est **librement révisable** à partir des données terrain, sans modification de la constitution, dans la limite du cadre conceptuel que celle-ci fixe. Chaque entrée indique son ancrage constitutionnel.

> **Comment lire ce document** : chaque paramètre est présenté avec (1) sa valeur de référence, (2) sa fourchette de variation légitime, (3) la justification de la valeur de référence, (4) le signal terrain qui devrait déclencher une révision. Un paramètre sans signal de révision défini est un paramètre mal spécifié.

> **Décisions d'architecture ouvertes** : en fin de document, les trois propositions délibérément écartées de la constitution lors de la v1.1 (typage des arêtes, budget cognitif, composante G) sont documentées comme décisions ouvertes, avec leur état de réflexion actuel.

---

## 1. Paramètres du Mastery Score Composite (MSC)

*Ancrage constitutionnel : Glossaire MSC, P2, P3, P6*

---

### MSC-P — Seuil de précision (composante P)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | ≥ 80% sur N ≥ 5 occurrences au niveau Bloom cible |
| **Fourchette** | N ∈ [3, 10] ; taux ∈ [70%, 90%] |
| **Justification** | N=5 offre un signal statistiquement suffisant sans surcoût de sessions. 80% correspond au seuil classique du mastery learning (Bloom) ; en deçà de 70%, le risque de faux positifs devient élevé ; au-delà de 90%, le coût en sessions devient prohibitif pour un bénéfice marginal. |
| **Signal de révision** | Si le taux de dégradation post-maîtrise (voir MSC-deg) dépasse 25% des concepts déclarés maîtrisés, abaisser N ou relever le taux. |

---

### MSC-R — Seuil de robustesse temporelle (composante R)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | D ≥ 3 jours (robustesse court terme) ; D ≥ 7 jours (robustesse moyen terme) |
| **Fourchette** | Court terme ∈ [1, 5 jours] ; moyen terme ∈ [5, 14 jours] |
| **Justification** | 3 jours correspond à la consolidation minimale de la mémoire à long terme documentée en sciences cognitives. 7 jours garantit un premier test de rétention hebdomadaire, cohérent avec une scolarité standard. |
| **Signal de révision** | Si les simulations d'examen révèlent systématiquement des oublis sur des concepts déclarés R-validés à 7 jours, augmenter le délai moyen terme. |

---

### MSC-A — Seuil d'autonomie (composante A)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | M ≥ 3 réussites consécutives sans aide ni indice d'aucune sorte |
| **Fourchette** | M ∈ [2, 5] |
| **Justification** | 3 occurrences consécutives sans aide constituent un signal minimal de non-dépendance au guidage. En dessous de 2, le risque de faux positif est élevé. Au-delà de 5, le coût en sessions n'est pas justifié par un gain de robustesse documenté. |
| **Signal de révision** | Si la composante A est déclarée atteinte mais que le fading déclenché génère systématiquement des demandes de réactivation du guidage, augmenter M. |

---

### MSC-deg — Seuil de dégradation post-maîtrise

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Révocation si ≥ 2 occurrences consécutives en échec après une absence ≥ seuil_R |
| **Fourchette** | Nombre d'occurrences ∈ [1, 3] |
| **Justification** | 1 seul échec peut être accidentel (mauvaise compréhension de l'énoncé, distraction). 2 occurrences consécutives constituent un signal de rétrogradation réelle. Au-delà de 3, le système risque de laisser un apprenant en échec réel sans intervention. |
| **Signal de révision** | Si le taux de révocation après 2 occurrences dépasse 30% des concepts maîtrisés, revoir les seuils P ou R. |

---

## 2. Paramètres du calibrage initial (P0)

*Ancrage constitutionnel : Principe 0*

---

### P0-1 — Longueur du diagnostic adaptatif

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | ≤ 10 items par diagnostic |
| **Fourchette** | [5, 15] items |
| **Justification** | En dessous de 5 items, la précision de l'estimation initiale est insuffisante (trop de variance). Au-delà de 15 items, le coût attentionnel et la charge affective du calibrage risquent de nuire à l'engagement initial. |
| **Signal de révision** | Si les états MSC initialisés par calibrage sont révisés dans plus de 40% des cas lors des 3 premières sessions, augmenter le nombre d'items. |

---

### P0-2 — Granularité des prédictions de performance

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Une prédiction par item ou par groupe de 2-3 items de même type |
| **Fourchette** | De "une prédiction par item" à "une prédiction par bloc thématique" |
| **Justification** | La prédiction item par item est plus précise pour initialiser l'axe Calibration mais peut alourdir l'expérience. La prédiction par groupe est moins précise mais plus fluide. La valeur de référence cherche un équilibre entre les deux. |
| **Signal de révision** | Si le taux d'abandon en phase de calibrage dépasse 20%, passer à une granularité par bloc. |

---

## 3. Paramètres de la temporalité et de l'interleaving (P3)

*Ancrage constitutionnel : Principe 3*

---

### P3-1 — Condition opérationnelle de bascule vers l'interleaving de contenus

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | ≥ 2 réussites consécutives sans aide sur ≥ 3 tâches distinctes du niveau Bloom cible, pour chaque contenu concerné |
| **Fourchette** | Réussites consécutives ∈ [1, 3] ; tâches distinctes ∈ [2, 5] |
| **Justification** | Le principe constitutionnel (bascule conditionnée à P + A atteints) est opérationnalisé ici. 2 réussites consécutives sans aide ≈ composante A minimale atteinte. 3 tâches distinctes évite que P soit atteinte sur un seul format. |
| **Signal de révision** | Si l'interleaving déclenché génère une chute de précision > 20 points de pourcentage sur les sessions suivantes, relever les seuils. |

---

### P3-2 — Seuil de rééquilibration de la couverture (interleaving par catégories)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Rééquilibration déclenchée si un item n'a pas été présenté depuis ≥ 2× le délai moyen des autres items de la même catégorie |
| **Fourchette** | Multiplicateur ∈ [1.5×, 3×] |
| **Justification** | En dessous de 1.5×, la rééquilibration est trop fréquente et perturbe la planification. Au-delà de 3×, le risque de retrieval-induced forgetting sur les items peu pratiqués devient réel. |
| **Signal de révision** | Si le retrieval-induced forgetting est mesuré en phase Évaluation sur des items de catégories actives, abaisser le multiplicateur. |

---

### P3-3 — Longueur du diagnostic de la session de reprise

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | 3 à 5 tâches de rappel sur les concepts récemment maîtrisés |
| **Fourchette** | [2, 8] tâches |
| **Justification** | Le but est diagnostique, pas formatif. 3-5 tâches permettent d'identifier les concepts dont R est dégradée sans surcharger une session de reprise dont la motivation est déjà fragilisée par l'interruption. |
| **Signal de révision** | Si le diagnostic de reprise sous-estime les dégradations (révélées ensuite par les performances), augmenter le nombre de tâches. |

---

## 4. Paramètres de la personnalisation (P5)

*Ancrage constitutionnel : Principe 5*

---

### P5-1 — Profils d'apprenants surveillés par défaut (équité algorithmique)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | A minima : niveau initial estimé (via calibrage P0) et régularité d'usage (fréquence hebdomadaire moyenne). Profils étendus : à définir par univers selon le contexte d'usage (niveau scolaire, langue principale, contexte d'accès). |
| **Fourchette** | Non applicable — à définir par univers |
| **Justification** | Niveau initial et régularité sont les deux sources de biais les plus documentées dans les systèmes adaptatifs. Les attributs protégés supplémentaires dépendent du contexte légal et éducatif de l'univers. |
| **Signal de révision** | Si un écart systématique non anticipé est détecté lors de la phase Évaluation, ajouter l'attribut concerné à la liste surveillée. |

---

### P5-2 — Métriques d'équité de référence

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Taux de maîtrise MSC atteint, temps moyen jusqu'au MSC, taux d'abandon — comparés entre groupes définis en P5-1 |
| **Fourchette** | Non applicable |
| **Justification** | Ces trois métriques couvrent les trois dimensions principales d'un écart d'équité : résultat (MSC), efficience (temps), persistance (abandon). |
| **Signal de révision** | Si un écart entre groupes dépasse le seuil défini par univers, la révision du modèle adaptatif est obligatoire (pas seulement un signalement). |

---

### P5-3 — États prioritaires de la matrice apprenant composite

| Attribut | Valeur |
|---|---|
| **Valeur de référence (déploiement initial)** | 5 états : bien calibré/productif, surestimateur/productif, sous-estimateur/productif, bien calibré/anxiogène, bien calibré/ennui |
| **Cible de couverture complète** | 9 états (matrice 3×3 complète) |
| **Justification** | Les 5 états prioritaires couvrent les situations les plus fréquentes et les plus impactantes. Les 4 états restants (surestimateur/anxiogène, sous-estimateur/anxiogène, surestimateur/ennui, sous-estimateur/ennui) représentent des combinaisons moins fréquentes mais documentées. |
| **Signal de déploiement de la matrice complète** | Lorsque les données terrain de l'univers pilote permettent de valider empiriquement les politiques adaptatives des 5 états prioritaires. |

---

## 5. Paramètres de l'adaptation à l'environnement d'usage (P7)

*Ancrage constitutionnel : Principe 7*

---

### P7-1 — Seuil de fatigue cognitive intra-session

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | 25 minutes de travail actif |
| **Fourchette** | [15 min, 40 min] |
| **Justification** | 25 minutes correspond à une durée de travail cognitif soutenu cohérente avec la littérature sur la fatigue attentionnelle (Pomodoro-like) et la Cognitive Load Theory. En deçà de 15 min, la session est trop courte pour atteindre la charge germinale nécessaire à la formation de schémas. Au-delà de 40 min, les données terrain sur la fatigue scolaire suggèrent un rendement décroissant. |
| **Signal de révision** | Si les données de performance intra-session montrent une chute significative avant 25 min sur un profil d'apprenant donné, abaisser le seuil pour ce profil. |

---

## 6. Paramètres de la gamification éthique (P8)

*Ancrage constitutionnel : Principe 8*

---

### P8-1 — Indicateurs opérationnels du test de non-nuisance

| Attribut | Valeur |
|---|---|
| **Indicateurs de référence** | Au moins l'un des trois : (a) absence de dégradation du MSC moyen sur les sessions contenant l'élément vs sessions sans l'élément ; (b) absence de corrélation positive entre exposition à l'élément et réduction de la composante A du MSC ; (c) absence de corrélation positive entre exposition à l'élément et abandon des missions complexes. |
| **Condition de validation** | Un seul indicateur suffit pour lever la période probatoire — mais les trois devraient être mesurés. |
| **Justification** | Ces trois indicateurs couvrent les trois risques principaux d'une mécanique de gamification : dégradation des performances (a), érosion de l'autonomie (b), évitement des tâches difficiles (c). Le critère (a) seul est insuffisant car une mécanique peut maintenir le MSC moyen en orientant l'usage vers les tâches faciles. |
| **Signal de révision** | Si aucun des trois indicateurs n'est mesurable avec les données disponibles, le test de non-nuisance ne peut pas être réalisé — l'élément reste en période probatoire indéfiniment jusqu'à ce que la collecte soit possible. |

---

## 7. Paramètres de la métacognition et du lien social (P9)

*Ancrage constitutionnel : Principe 9*

---

### P9-1 — Seuil d'activation de la fonctionnalité sociale

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | 5 sessions complétées |
| **Fourchette** | [3, 10] sessions |
| **Justification** | 5 sessions permettent à l'apprenant d'avoir une expérience suffisante du jeu pour évaluer son intérêt pour la dimension sociale. En dessous de 3, la proposition sociale peut être perçue comme intrusive ou prématurée. Au-delà de 10, le délai devient si long que certains apprenants n'atteignent jamais la fonctionnalité. |
| **Signal de révision** | Si le taux d'activation de la fonctionnalité sociale est inférieur à 20% après le seuil, revoir le timing ou la forme de la proposition. |

---

## 8. Paramètres du cycle ADDIE — Évaluation

*Ancrage constitutionnel : Cycle de design pédagogique, étape 5*

---

### ADDIE-1 — Seuil de biais systématique déclenchant une révision du modèle d'inférence

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Sur ≥ 3 évaluations consécutives, écart médian entre maîtrise estimée et performance réelle > 20% |
| **Fourchette** | Nombre d'évaluations ∈ [2, 5] ; écart ∈ [15%, 30%] |
| **Justification** | 3 évaluations consécutives évitent qu'un incident ponctuel déclenche une révision inutile. 20% est un seuil cliniquement significatif dans les systèmes de mastery learning. |
| **Signal de révision du seuil lui-même** | Si les révisions déclenchées à 20% ne produisent pas d'amélioration mesurable, le modèle d'inférence sous-jacent est probablement inadéquat — remonter le problème à la phase Analyse. |

---

### ADDIE-2 — Seuil de révision du modèle commun en usage cohorte

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Écart > 15% sur ≥ 10 apprenants d'une même cohorte |
| **Fourchette** | Écart ∈ [10%, 25%] ; N apprenants ∈ [5, 20] |
| **Justification** | Un écart collectif de 15% sur 10 apprenants constitue un signal que le modèle commun contient un biais systémique et non un effet individuel. En dessous de 5 apprenants, le signal est trop bruité. |
| **Signal de révision** | Si ce seuil déclenche des révisions trop fréquentes pour être traitées, augmenter N ou le seuil d'écart. |

---

## 9. Paramètre de P1 — Niveau cognitif minimum des concepts fondamentaux

*Ancrage constitutionnel : Principe 1*

---

### P1-1 — Niveau Bloom minimum pour les concepts fondamentaux hors annales

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Niveau *comprendre* (taxonomie Bloom révisée) |
| **Fourchette** | *mémoriser* (minimum absolu) à *appliquer* (maximum raisonnable sans annales) |
| **Justification** | *Mémoriser* seul ne garantit pas une compréhension utilisable. *Comprendre* correspond au seuil à partir duquel un concept peut être mobilisé dans un raisonnement. *Appliquer* sans annales risque de sur-spécifier les missions de concepts secondaires. |
| **Signal de révision** | Si les concepts fondamentaux maintenus à *comprendre* ne sont jamais mobilisés dans les missions d'intégration, baisser à *mémoriser*. |

---

## 10. Périmètre de déploiement (décisions de roadmap)

*Ces décisions ne sont pas des paramètres pédagogiques mais des engagements de déploiement par phase. Elles sont ici pour référence — non pour révision lors des itérations terrain.*

| Fonctionnalité | Statut initial | Condition de généralisation |
|---|---|---|
| **Flag Misconception** | Optionnel par univers au déploiement initial | Obligatoire pour tout domaine à fort taux de misconceptions documentées dès la deuxième version d'un univers |
| **Matrice état apprenant complète (9 états)** | 5 états prioritaires au déploiement initial | Extension aux 9 états conditionnée à la validation des politiques adaptatives des 5 états prioritaires sur l'univers pilote |
| **Équité algorithmique — attributs protégés étendus** | Surveillance a minima (niveau initial, régularité) au déploiement initial | Extension aux attributs protégés complets conditionnée à la disponibilité des données et au cadre légal de l'univers |
| **Apprentissage par les pairs** | Optionnel par univers | Justification obligatoire dans la documentation de design si inclus ou explicitement exclu |

---

## 11. Décisions d'architecture ouvertes

*Ces trois propositions ont été délibérément écartées de la constitution lors de la v1.1 car trop prescriptives à ce stade. Elles sont documentées ici comme décisions ouvertes, à trancher avant ou pendant le développement du moteur.*

---

### DA-1 — Typage des arêtes du graphe de connaissances

**Problème** : la constitution dit que le graphe gère les "relations de prérequis" (P2), mais ne spécifie pas si toutes les arêtes sont du même type ou si elles sont typées (prérequis strict, prérequis partiel, relation de renforcement, relation de transfert, etc.).

**Options** :
- *Option A — Graphe homogène* : toutes les arêtes représentent une relation de prérequis. Simple à implémenter, limitant pour les missions de transfert et d'intégration.
- *Option B — Typage minimal (2 types)* : prérequis bloquant (le concept B ne peut pas être abordé sans A) vs prérequis facilitant (A aide B mais ne le bloque pas). Ajoute peu de complexité d'implémentation, améliore la granularité du moteur adaptatif.
- *Option C — Typage riche (3+ types)* : prérequis bloquant, prérequis facilitant, relation de transfert (A renforce T de B), relation de misconception (croyance A interfère avec apprentissage de B). Complexité d'annotation significative.

**Recommandation provisoire** : Option B pour le MVP. Option C à évaluer en v2.0 si les données terrain montrent que les missions de transfert bénéficieraient d'arêtes explicitement typées.

---

### DA-2 — Budget cognitif de session

**Problème** : la constitution pose le principe de fatigue cognitive intra-session et le seuil de 25 minutes (P7, référentiel P7-1), mais ne définit pas comment le système calcule dynamiquement la charge restante disponible pour choisir les tâches.

**Options** :
- *Option A — Proxy temporel seul* : le temps actif suffit comme proxy de la charge consommée. Simple, déjà spécifié. Ne distingue pas une session de 25 min de rappel facile d'une session de 25 min de résolution de problèmes multi-étapes.
- *Option B — Proxy basé sur le type de tâche* : chaque type de tâche est pondéré par une charge intrinsèque estimée (rappel simple = 1, problème multi-étapes = 4). Le budget est la somme pondérée des tâches complétées. Plus précis, nécessite une annotation de charge pour chaque type de mission dans le graphe de design.
- *Option C — Proxy mixte temps × type* : combines les deux. Le seuil temporel reste le garde-fou de dernier ressort, la somme pondérée pilote les décisions d'ordonnancement.

**Recommandation provisoire** : Option A pour le MVP (simple, cohérent avec P7-1). Option B à introduire si les données terrain montrent que le proxy temporel seul produit des planifications sous-optimales (tâches lourdes proposées en fin de session malgré le seuil atteint).

---

### DA-3 — Composante G (Généralisation) dans le MSC

**Problème** : la proposition d'ajouter une 5e composante G au MSC, mesurant la capacité à généraliser à de nouveaux contextes non encore présentés (distinction du transfert T, qui mesure la robustesse sur des formats structurellement différents mais connus du domaine).

**Arguments pour** : T mesure le transfert proche (intra-domaine). G mesurerait le transfert lointain, aligné avec P1 (objectif de transfert lointain). Cohérence conceptuelle forte avec la taxonomie Bloom (niveaux *évaluer* et *créer*).

**Arguments contre** : G est très difficile à mesurer en contexte jeu. Les tâches permettant de la mesurer sont rares et coûteuses à concevoir. Le risque d'ajouter une composante structurellement non mesurable dans le moteur est élevé.

**Décision actuelle** : composante G documentée ici comme cible conceptuelle pour les univers déclarant un objectif de transfert lointain (P1), sans intégration au MSC. La phase Évaluation de ces univers doit prévoir une mesure externe de généralisation ad hoc. Si des patterns récurrents de mesure émergent sur plusieurs univers, la formulation d'une composante G opérationnelle pourra être envisagée en v2.0 du MSC.

---

*Référentiel de defaults pédagogiques v0.1 — extrait de la Constitution v1.2. À réviser librement à partir des données terrain de l'univers pilote. Toute révision de ce document qui contreviendrait à un principe de la Constitution v1.2 doit être traitée comme une modification constitutionnelle, pas comme une révision du référentiel.*
