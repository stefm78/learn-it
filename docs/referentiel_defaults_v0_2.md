# Référentiel de defaults pédagogiques – Learn-it (v0.2)

> **Statut et gouvernance** : Ce document est le complément opérationnel de la Constitution v1.3. Il contient l'ensemble des seuils, valeurs de référence, opérationnalisations et décisions de déploiement. Il est **librement révisable** à partir des données terrain, sans modification de la constitution, dans la limite du cadre conceptuel que celle-ci fixe. Chaque entrée indique son ancrage constitutionnel.

> **Modifications v0.2 par rapport à v0.1** : (1) Ajout P0-3 — état *maîtrise provisoire héritée* et protocole de vérification prioritaire ; (2) Ajout P5-4 — proxys comportementaux explicites de l'axe régime d'activation et version dégradée à trois régimes ; (3) Révision P5-3 — vocabulaire aligné sur la reformulation P5 (constitution v1.3) ; (4) Fermeture de DA-2 — budget cognitif : Option B retenue comme défaut dès le MVP, avec annotations de charge obligatoires dans le graphe de design ; (5) Ajout DA-4 — algorithme d'espacement explicite (décision d'architecture fermée) ; (6) Ajout section 11 — Paramètres des patchs IA (déclencheurs, périmètre, garde-fous, fréquence maximale) ; (7) Ajout ADDIE-0 — protocole de validation du graphe produit par la chaîne IA de conception.

> **Comment lire ce document** : chaque paramètre est présenté avec (1) sa valeur de référence, (2) sa fourchette de variation légitime, (3) la justification de la valeur de référence, (4) le signal terrain qui devrait déclencher une révision. Un paramètre sans signal de révision défini est un paramètre mal spécifié.

> **Décisions d'architecture** : les décisions d'architecture sont documentées en fin de document. DA-1 (typage des arêtes) et DA-3 (composante G) restent ouvertes. DA-2 (budget cognitif) et DA-4 (algorithme d'espacement) sont désormais fermées.

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

### P0-3 — Protocole de vérification de la maîtrise provisoire héritée

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Vérification prioritaire de R et A lors des 3 premières sessions actives suivant le calibrage, pour chaque concept initialisé en *maîtrise provisoire héritée* |
| **Modalité de vérification R** | Au moins une occurrence du concept sans guidage après un délai ≥ seuil MSC-R court terme (3 jours par défaut) depuis le calibrage |
| **Modalité de vérification A** | Au moins 2 réussites consécutives sans aide sur le concept au niveau Bloom calibré |
| **Issue positive** | R et A confirmées → passage en *maîtrise d'entraînement* ; T non validé génère une mission de transfert prioritaire |
| **Issue négative** | R ou A non confirmées → passage en état *en consolidation* avec parcours de réactivation (et non en état *nouveau*) |
| **Fourchette** | Fenêtre de vérification ∈ [2, 5] premières sessions |
| **Justification** | Un pré-test évalue la performance actuelle ; il ne valide ni la robustesse temporelle ni l'autonomie sans aide répétée. La présomption de maîtrise sans vérification crée un risque de sur-déclaration qui compromet la planification de l'espacement. La fenêtre de 3 sessions permet une vérification rapide sans surcharger les premières sessions avec des items de vérification uniquement. |
| **Signal de révision** | Si plus de 50% des concepts en *maîtrise provisoire héritée* échouent la vérification R ou A lors du pilote, revoir le protocole de calibrage (augmenter les items P0-1 ou renforcer les critères du pré-test). |

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

### P5-3 — Régimes d'activation prioritaires (matrice apprenant composite)

| Attribut | Valeur |
|---|---|
| **Version de déploiement initial (3 régimes)** | Régime de détresse / Régime neutre / Régime de sous-défi |
| **Version intermédiaire (5 états)** | Bien calibré / neutre, Surestimateur / neutre, Sous-estimateur / neutre, Bien calibré / détresse, Bien calibré / sous-défi |
| **Cible de couverture complète** | Matrice 3×3 — 9 états (conditionnée à validation empirique des règles d'inférence sur données terrain, voir P5-4) |
| **Justification** | La version à 3 régimes est implémentable dès le MVP avec des règles déterministes simples sur les proxys comportementaux. La version à 5 états ajoute l'axe Calibration, inférable de façon déterministe à partir de l'écart prédiction/performance. La matrice complète à 9 états suppose que les quatre états combinant axe Calibration non-neutre et axe Activation non-neutre aient été validés empiriquement. |
| **Signal de déploiement de la matrice complète** | Lorsque les données terrain permettent de valider empiriquement les politiques adaptatives des 5 états prioritaires sur l'univers pilote, et que les règles d'inférence des 4 états restants sont documentées et testées. |

---

### P5-4 — Proxys comportementaux de l'axe régime d'activation

*Ce paramètre opérationnalise l'axe 2 (Régime d'activation) de la matrice apprenant composite. Il est obligatoire — les états affectifs du moteur ne peuvent pas être laissés à une inférence implicite.*

| Proxy | Mesure | Seuil régime de détresse | Seuil régime de sous-défi |
|---|---|---|---|
| **Taux d'erreur** | % d'échecs sur fenêtre glissante de N=5 dernières tentatives au niveau Bloom cible | > 60% | < 15% |
| **Ratio d'abandon** | Abandons intra-mission / (Abandons intra-mission + Complétions) sur la session | > 40% | — |
| **Fréquence des demandes d'aide** | Nombre d'aides demandées / nombre de tâches complétées sur la session | > 1,5 | < 0,05 avec temps de réponse courts |
| **Temps de réponse relatif** | Ratio temps de réponse moyen session / médiane personnelle historique | > 2,0 (lenteur inhabituelle) | < 0,4 (accélération inhabituelle) |
| **Auto-déclaration simplifiée** | Réponse en fin de session à une question à 3 options (trop facile / adapté / trop difficile) | Déclaration "trop difficile" | Déclaration "trop facile" |

**Règle de combinaison** : un régime est déclaré si **au moins 2 proxys** sur 5 franchissent leur seuil dans le même sens, ou si l'auto-déclaration est disponible et concordante avec au moins 1 proxy. Un seul proxy en dehors des seuils ne déclenche pas de changement de régime — le moteur applique une réponse conservatrice en attendant confirmation.

**Fourchette des seuils** : les valeurs ci-dessus sont des valeurs de référence. Elles peuvent être ajustées par univers dans les fourchettes suivantes : taux d'erreur ∈ [50%, 70%] pour la détresse, ∈ [10%, 25%] pour le sous-défi ; ratio d'abandon ∈ [30%, 50%] ; fréquence d'aide ∈ [1.0, 2.0] ; temps de réponse ∈ [1.5, 2.5] pour la lenteur, ∈ [0.3, 0.5] pour l'accélération.

**Statut de validation** : ces proxys sont des *hypothèses supposées* au déploiement initial. Leur statut de validation doit être mis à jour en phase Évaluation à partir des données observées. Un proxy dont la corrélation avec le régime déclaré n'est pas confirmée après 3 évaluations consécutives est suspendu et documenté comme invalidé pour cet univers.

**Signal de révision** : si le changement de régime déclenché par ces proxys génère des politiques adaptatives jugées inadéquates par l'apprenant (auto-rapport discordant ≥ 40% des cas), réviser les seuils ou le nombre de proxys requis.

---

### P5-5 — Niveau de confiance minimal avant adaptation à fort impact

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Au moins 2 proxys concordants sur 5, ou 1 proxy + 1 auto-déclaration concordante |
| **Fourchette** | [1 proxy seul (minimum absolu, adaptation conservatrice uniquement), 3 proxys (pour adaptations à fort impact)] |
| **Justification** | Une inférence reposant sur un seul proxy comportemental est trop ambiguë pour déclencher une adaptation significative (changement de parcours, modification de la difficulté de plus d'un niveau). Les adaptations conservatrices (message d'encouragement, réduction mineure du guidage) peuvent être déclenchées par un seul signal. |
| **Signal de révision** | Si le moteur déclenche systématiquement des adaptations à fort impact non confirmées par les sessions suivantes, augmenter le seuil de confiance. |

---

## 5. Paramètres de l'adaptation à l'environnement d'usage (P7)

*Ancrage constitutionnel : Principe 7*

---

### P7-1 — Seuil de fatigue cognitive intra-session (proxy temporel)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | 25 minutes de travail actif (garde-fou de dernier ressort) |
| **Fourchette** | [15 min, 40 min] |
| **Justification** | 25 minutes correspond à une durée de travail cognitif soutenu cohérente avec la littérature sur la fatigue attentionnelle. Ce seuil temporel est le garde-fou de dernier ressort : en l'absence de calcul de budget cognitif pondéré (DA-2), il constitue le seul signal disponible. En présence du budget pondéré (DA-2, désormais Option B par défaut), le seuil temporel intervient uniquement si le budget cognitif calculé n'a pas déclenché de bascule avant 25 min. |
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

### P9-2 — Seuil de détection de l'évitement métacognitif

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Évitement confirmé si : (a) temps passé sur les écrans de réflexion < 30% du temps médian observé sur les apprenants comparables, ET (b) taux d'erreur post-prompt inchangé (variation < 5 points de pourcentage) sur 3 sessions consécutives |
| **Fourchette** | Seuil de temps ∈ [20%, 50%] de la médiane ; nombre de sessions consécutives ∈ [2, 5] |
| **Justification** | Le critère temporel seul est insuffisant (un apprenant rapide peut répondre vite sans éviter). La combinaison avec l'absence d'effet sur la performance post-prompt distingue un apprenant qui internalise (réponse rapide + amélioration mesurable) d'un apprenant qui évite (réponse rapide + pas d'amélioration). |
| **Conséquence** | Retour à des prompts plus guidés et plus courts — non suppression des prompts. Évitement persistant (≥ 5 sessions) → candidat à un patch IA (voir section 11). |
| **Signal de révision** | Si le taux de faux positifs (apprenants classés en évitement mais progressant bien) dépasse 20%, relever le seuil de temps ou allonger la fenêtre d'observation. |

---

## 8. Paramètres du cycle ADDIE — Évaluation

*Ancrage constitutionnel : Cycle de design pédagogique, étape 5*

---

### ADDIE-0 — Protocole de validation du graphe produit par la chaîne IA de conception

| Critère | Condition minimale de validation |
|---|---|
| **Couverture Bloom** | Chaque objectif déclaré en phase Analyse est représenté par au moins un nœud au niveau cognitif cible dans le graphe |
| **Cohérence des prérequis** | Absence de cycles dans les arêtes de prérequis ; chaque arête est justifiée dans la documentation de design |
| **Flags misconception** | Tous les concepts identifiés comme à misconception documentée dans le corpus disciplinaire disposent d'un flag dans le graphe |
| **Couverture des missions** | Chaque nœud dispose d'au moins un template de mission de conflit cognitif (si flag misconception), au moins un template de mission générative, et au moins 3 templates de feedback couvrant les types d'erreurs principaux |
| **Validation des formats de récupération** | Le graphe distingue explicitement les missions de reconnaissance, rappel indicé, rappel libre et production longue — au moins deux formats distincts par nœud au niveau Bloom cible |

**Statut de déploiement** :
- Graphe satisfaisant tous les critères → déploiement standard autorisé.
- Graphe satisfaisant les critères de couverture Bloom et cohérence des prérequis mais incomplet sur les missions → déploiement en **mode pilote restreint** (N ≤ 30 apprenants) avec collecte obligatoire jusqu'à complétion.
- Graphe ne satisfaisant pas les critères minimaux de couverture Bloom ou présentant des cycles → **déploiement suspendu**, retour en phase Design.

**Signal de révision du protocole** : si plus de 30% des graphes validés en mode standard nécessitent une révision structurelle lors de la première phase Évaluation, renforcer les critères de validation.

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

### ADDIE-3 — Seuil d'efficience par nœud (révision structurelle du graphe)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Un nœud est signalé comme défaut de design si son temps médian d'apprentissage jusqu'au MSC dépasse le double de la valeur cible documentée en phase Analyse |
| **Fourchette** | Multiplicateur ∈ [1.5×, 3×] |
| **Justification** | La valeur cible est définie en phase Analyse à partir de la complexité du concept et du niveau Bloom. Un dépassement au double signale un problème de design (décomposition insuffisante, prérequis manquants, formats de mission inadaptés) plutôt qu'un simple besoin de reparamétrage. |
| **Conséquence** | Déclenchement d'une révision structurelle du graphe (ajout, suppression ou refactorisation de nœuds) distincte de la révision paramétrique. La révision structurelle relève de la chaîne IA de conception, pas du moteur autonome. |
| **Signal de révision** | Si les révisions structurelles déclenchées sur ce seuil n'améliorent pas l'efficience sur les sessions suivantes, remettre en cause la valeur cible définie en phase Analyse. |

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
| **Matrice état apprenant — version 3 régimes** | Implémentée au déploiement initial (moteur autonome) | — |
| **Matrice état apprenant — version 5 états** | Conditionnée à l'intégration de l'axe Calibration déterministe | Dès validation de l'écart prédiction/performance comme signal fiable |
| **Matrice état apprenant — version 9 états complète** | Conditionnée à la validation empirique des règles d'inférence | Extension conditionnée aux données terrain de l'univers pilote (voir P5-3) |
| **Équité algorithmique — attributs protégés étendus** | Surveillance a minima (niveau initial, régularité) au déploiement initial | Extension aux attributs protégés complets conditionnée à la disponibilité des données et au cadre légal de l'univers |
| **Apprentissage par les pairs** | Optionnel par univers | Justification obligatoire dans la documentation de design si inclus ou explicitement exclu |

---

## 11. Paramètres des patchs IA (P12)

*Ancrage constitutionnel : Principe 12*

---

### PATCH-1 — Déclencheurs de patch

| Déclencheur | Seuil | Priorité |
|---|---|---|
| Écart individuel maîtrise estimée / performance réelle | > 20% sur ≥ 3 évaluations consécutives (ADDIE-1) | Haute |
| Biais systématique cohorte | > 15% sur ≥ 10 apprenants (ADDIE-2) | Haute |
| Taux de révocation MSC | > 30% des concepts déclarés maîtrisés (MSC-deg) | Haute |
| Oscillation récurrente d'un concept | ≥ 3 cycles maîtrisé → révoqué → remaîtrisé sur le même concept | Haute |
| Écarts d'équité entre groupes | Dépassement du seuil défini en P5-2 | Haute |
| Échec du test de non-nuisance d'un élément de gamification | Non-satisfaction des indicateurs P8-1 | Moyenne |
| Évitement métacognitif persistant | ≥ 5 sessions en état d'évitement confirmé (P9-2) | Moyenne |
| Abandon calibrage | > 20% des apprenants n'atteignent pas la fin du calibrage (P0-2) | Moyenne |
| Série d'overrides apprenant | ≥ 5 overrides consécutifs signalant un désalignement de la politique adaptative | Basse |

---

### PATCH-2 — Périmètre autorisé des modifications par patch

| Catégorie | Autorisé | Interdit |
|---|---|---|
| **Paramètres du référentiel** | Ajustement dans les fourchettes définies (N, D, M, seuils, multiplicateurs) | Modification hors fourchettes constitutionnelles |
| **Graphe de connaissances** | Révision des poids, ajout ou désactivation de nœuds secondaires, correction d'arêtes | Modification de la structure principale du graphe sans retour en phase Analyse/Design |
| **Missions et contenus** | Ajout de variantes de missions, de templates de feedback supplémentaires, de sous-parcours | Génération de contenu pédagogique fondamentalement nouveau sans validation de la chaîne de conception |
| **Politiques adaptatives** | Révision du mapping régimes observables → politiques, ajustement des seuils de déclenchement | Redéfinition des composantes du MSC, modification de la philosophie d'adaptation (P5, P8) |
| **Matrice apprenant** | Activation de la version étendue (5 ou 9 états) si données suffisantes | Introduction d'un nouveau mécanisme d'inférence psychologique sans statut probatoire |

---

### PATCH-3 — Attributs obligatoires de tout patch

| Attribut | Description |
|---|---|
| **Versionné** | Numéro de version du patch, date de génération, identifiant du signal déclencheur |
| **Justifié** | Référence explicite au déclencheur PATCH-1 ayant motivé le patch |
| **Borné** | Liste exhaustive des paramètres modifiés et de leur valeur avant/après |
| **Réversible** | Condition de rollback définie : métrique cible et délai d'observation au-delà duquel le rollback est déclenché si aucune amélioration n'est mesurée |
| **Transparent** | Description lisible par l'apprenant (en langage non technique) de ce qui change dans son parcours et pourquoi |
| **Conforme** | Vérification de non-contradiction avec P5 (équité), P8 (non-nuisance gamification), P9 (autonomie apprenant) avant déploiement |

---

### PATCH-4 — Fréquence maximale et propagation des patchs

| Attribut | Valeur |
|---|---|
| **Fréquence maximale individuelle** | 1 patch par apprenant par période de 14 jours (sauf déclencheur de priorité haute) |
| **Fréquence maximale cohorte** | 1 patch cohorte par période de 30 jours |
| **Propagation d'un patch cohorte** | Un patch déclenché sur une cohorte est proposé (non imposé) aux apprenants individuels de cette cohorte dont les métriques sont dans la même direction de dérive |
| **Fourchette** | Fréquence individuelle ∈ [7 jours, 30 jours] selon sévérité de la dérive ; fréquence cohorte ∈ [14 jours, 60 jours] |
| **Justification** | Une fréquence trop élevée de patchs signale que le moteur autonome est mal calibré ou que les artefacts de conception sont insuffisants — et non que le mécanisme de patch fonctionne bien. Une fréquence de patch > 2 par mois sur un même apprenant doit déclencher une révision de la couche conception (pas seulement un nouveau patch). |
| **Signal de révision** | Si la fréquence moyenne de patchs individuels dépasse 1 par 14 jours sur l'ensemble de la cohorte, remonter le problème à la phase Analyse — la structure du graphe ou les artefacts de conception sont probablement insuffisants. |

---

## 12. Décisions d'architecture

---

### DA-1 — Typage des arêtes du graphe de connaissances

**Statut** : Décision ouverte — recommandation provisoire maintenue.

**Problème** : la constitution dit que le graphe gère les "relations de prérequis" (P2), mais ne spécifie pas si toutes les arêtes sont du même type ou si elles sont typées.

**Options** :
- *Option A — Graphe homogène* : toutes les arêtes représentent une relation de prérequis. Simple à implémenter, limitant pour les missions de transfert et d'intégration.
- *Option B — Typage minimal (2 types)* : prérequis bloquant (le concept B ne peut pas être abordé sans A) vs prérequis facilitant (A aide B mais ne le bloque pas). Ajoute peu de complexité d'implémentation, améliore la granularité du moteur adaptatif.
- *Option C — Typage riche (3+ types)* : prérequis bloquant, prérequis facilitant, relation de transfert (A renforce T de B), relation de misconception (croyance A interfère avec apprentissage de B). Complexité d'annotation significative.

**Recommandation provisoire** : Option B pour le MVP. Option C à évaluer en v2.0 si les données terrain montrent que les missions de transfert bénéficieraient d'arêtes explicitement typées.

---

### DA-2 — Budget cognitif de session *(décision fermée — Option B retenue)*

**Statut** : Décision fermée. Option B retenue comme défaut dès le MVP.

**Décision** : le budget cognitif de session est calculé comme **somme pondérée des tâches complétées**, chaque type de tâche étant annoté d'un poids de charge intrinsèque estimée dans le graphe de design. Le proxy temporel (P7-1, 25 min) reste le garde-fou de dernier ressort, mais ne constitue plus le pilote principal de l'ordonnancement.

**Poids de référence par type de tâche** :

| Type de tâche | Poids de charge |
|---|---|
| Reconnaissance / QCM | 1 |
| Rappel indicé | 2 |
| Rappel libre court | 3 |
| Application procédurale simple | 3 |
| Problème multi-étapes | 5 |
| Mission générative (auto-explication, cartographie) | 4 |
| Boss / simulation d'examen | 6 |

**Budget de session de référence** : 20 unités de charge (fourchette ∈ [12, 30] selon profil d'usage). La session bascule vers des formats à faible charge (poids ≤ 2) lorsque le budget est atteint.

**Signal de révision** : si les données terrain montrent que les poids sont systématiquement sous ou sur-estimés (chute de performance en fin de session malgré budget non atteint, ou absence de bascule malgré budget dépassé), ajuster les poids par type de tâche.

**Annotations obligatoires** : tout type de mission doit être annoté de son poids de charge dans le graphe de design produit par la chaîne IA de conception. Un graphe sans annotations de charge est un graphe incomplet au sens du protocole ADDIE-0.

---

### DA-3 — Composante G (Généralisation) dans le MSC

**Statut** : Décision ouverte — maintenue.

**Problème** : la proposition d'ajouter une 5e composante G au MSC, mesurant la capacité à généraliser à de nouveaux contextes non encore présentés (distinction du transfert T, qui mesure la robustesse sur des formats structurellement différents mais connus du domaine).

**Arguments pour** : T mesure le transfert proche (intra-domaine). G mesurerait le transfert lointain, aligné avec P1 (objectif de transfert lointain). Cohérence conceptuelle forte avec la taxonomie Bloom (niveaux *évaluer* et *créer*).

**Arguments contre** : G est très difficile à mesurer en contexte jeu. Les tâches permettant de la mesurer sont rares et coûteuses à concevoir. Le risque d'ajouter une composante structurellement non mesurable dans le moteur est élevé.

**Décision actuelle** : composante G documentée ici comme cible conceptuelle pour les univers déclarant un objectif de transfert lointain (P1), sans intégration au MSC. La phase Évaluation de ces univers doit prévoir une mesure externe de généralisation ad hoc. Si des patterns récurrents de mesure émergent sur plusieurs univers, la formulation d'une composante G opérationnelle pourra être envisagée en v2.0 du MSC.

---

### DA-4 — Algorithme d'espacement explicite *(décision fermée — SM-2 simplifié retenu)*

**Statut** : Décision fermée. Algorithme SM-2 simplifié retenu comme défaut pour le MVP.

**Problème** : la constitution (P3, v1.3) pose l'espacement comme mécanique centrale et exige un algorithme d'espacement local explicitement choisi. Cette décision n'était pas fermée dans le référentiel v0.1.

**Décision** : le moteur implémente un **algorithme de type SM-2 simplifié**, exécutable localement sans dépendance à un service externe.

**Paramètres de référence de l'algorithme** :

| Paramètre | Valeur de référence | Fourchette |
|---|---|---|
| Intervalle initial (première révision après apprentissage) | 1 jour | [1, 3 jours] |
| Deuxième intervalle (si réussite à la première révision) | 3 jours | [2, 5 jours] |
| Facteur de facilité de base (EF) | 2,5 | [1,3 ; 3,0] |
| Incrément EF par réussite sans aide | +0,1 | [+0,05 ; +0,15] |
| Décrement EF par échec | -0,2 | [-0,3 ; -0,1] |
| EF minimum | 1,3 | Non modifiable |
| Intervalle suivant (si réussite) | Intervalle précédent × EF | — |
| Intervalle suivant (si échec) | Retour à l'intervalle initial | — |

**Articulation avec le MSC** : la composante R du MSC sert de garde-fou. Un concept non validé sur R ne peut pas être déclaré maîtrisé indépendamment de P. L'algorithme SM-2 simplifié calcule quand proposer les révisions ; la composante R valide que l'intervalle minimum a bien été respecté avant déclaration de maîtrise.

**Un patch peut ajuster** les paramètres de l'algorithme (EF, intervalles initiaux) dans les fourchettes ci-dessus pour un apprenant dont les patterns d'oubli s'éloignent significativement des prédictions de l'algorithme.

**Signal de révision** : si les simulations d'examen révèlent systématiquement des oublis sur des concepts dont l'intervalle de révision a été validé par l'algorithme, augmenter le facteur de décrement EF ou réduire l'intervalle initial.

**Alternative à envisager en v2.0** : algorithme FSRS (Free Spaced Repetition Scheduler) si les données terrain montrent que SM-2 simplifié sous-estime la stabilité mémorielle des apprenants réguliers.

---

*Référentiel de defaults pédagogiques v0.2 — complément opérationnel de la Constitution v1.3. À réviser librement à partir des données terrain de l'univers pilote. Toute révision de ce document qui contreviendrait à un principe de la Constitution v1.3 doit être traitée comme une modification constitutionnelle, pas comme une révision du référentiel.*
