# Référentiel de defaults pédagogiques – Learn-it (v0.3)

> **Statut et gouvernance** : Complément opérationnel de la Constitution v1.4. Librement révisable à partir des données terrain sans modification de la constitution. Chaque entrée indique son ancrage constitutionnel, sa valeur de référence, sa fourchette de variation légitime, la justification de la valeur, et le signal terrain déclenchant une révision.

> **Modifications v0.3 par rapport à v0.2** : Ajout de la **section 12 — Paramètres de l'auto-rapport affectif (AR)**, couvrant les trois niveaux d'auto-rapport (micro-sondage événementiel, mini-sondage de fermeture, bilan de trajectoire), la hiérarchie de confiance auto-rapport/proxys, le protocole de discordance et de recalibration des proxys, et la détection du biais de désirabilité sociale. Ajout de la **section 13 — Paramètres de l'intégrité du modèle apprenant**, couvrant le calcul du SIS, les règles d'intégration selon SIS, le Niveau de Confiance MSC, les paramètres du mode Invité, du mode Évaluation Externe, de la vérification déclarative périodique, et du multi-profil. Mise à jour de P5-3, P5-4 et P5-5 pour intégrer la hiérarchie auto-rapport/proxys. Mise à jour de PATCH-1 pour ajouter les déclencheurs SIS.

---

## 1. Paramètres du Mastery Score Composite (MSC)

*Ancrage constitutionnel : Glossaire MSC, P2, P3, P6, P13*

### MSC-P — Seuil de précision (composante P)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | ≥ 80% sur N ≥ 5 occurrences au niveau Bloom cible |
| **Fourchette** | N ∈ [3, 10] ; taux ∈ [70%, 90%] |
| **Justification** | N=5 offre un signal statistiquement suffisant. 80% correspond au seuil mastery learning (Bloom). |
| **Signal de révision** | Si taux de dégradation post-maîtrise > 25%, abaisser N ou relever le taux. |

### MSC-R — Seuil de robustesse temporelle (composante R)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | D ≥ 3 jours (court terme) ; D ≥ 7 jours (moyen terme) |
| **Fourchette** | Court terme ∈ [1, 5 jours] ; moyen terme ∈ [5, 14 jours] |
| **Justification** | 3 jours = consolidation minimale LTM documentée. 7 jours = test hebdomadaire cohérent avec scolarité standard. |
| **Signal de révision** | Si simulations d'examen révèlent des oublis sur des concepts R-validés à 7 jours, augmenter le délai moyen terme. |

### MSC-A — Seuil d'autonomie (composante A)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | M ≥ 3 réussites consécutives sans aide ni indice |
| **Fourchette** | M ∈ [2, 5] |
| **Justification** | 3 occurrences consécutives = signal minimal de non-dépendance. |
| **Signal de révision** | Si fading déclenché par A génère systématiquement des demandes de réactivation du guidage, augmenter M. |

### MSC-deg — Seuil de dégradation post-maîtrise

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Révocation si ≥ 2 occurrences consécutives en échec après absence ≥ seuil_R |
| **Fourchette** | Nombre d'occurrences ∈ [1, 3] |
| **Signal de révision** | Si taux de révocation > 30%, revoir les seuils P ou R. |

---

## 2. Paramètres du calibrage initial (P0)

*Ancrage constitutionnel : Principe 0*

### P0-1 — Longueur du diagnostic adaptatif

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | ≤ 10 items |
| **Fourchette** | [5, 15] items |
| **Signal de révision** | Si états MSC initialisés révisés > 40% dans les 3 premières sessions, augmenter le nombre d'items. |

### P0-2 — Granularité des prédictions de performance

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | 1 prédiction par item ou groupe de 2-3 items de même type |
| **Fourchette** | De "1 prédiction par item" à "1 prédiction par bloc thématique" |
| **Signal de révision** | Si taux d'abandon en calibrage > 20%, passer à une granularité par bloc. |

### P0-3 — Protocole de vérification de la maîtrise provisoire héritée

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Vérification de R et A lors des 3 premières sessions actives suivant le calibrage |
| **Modalité R** | ≥ 1 occurrence sans guidage après délai ≥ seuil MSC-R court terme depuis le calibrage |
| **Modalité A** | ≥ 2 réussites consécutives sans aide au niveau Bloom calibré |
| **Issue positive** | R et A confirmées → maîtrise d'entraînement ; mission de transfert T générée |
| **Issue négative** | R ou A non confirmées → en consolidation avec parcours de réactivation |
| **Fourchette** | Fenêtre de vérification ∈ [2, 5] premières sessions |
| **Signal de révision** | Si > 50% des concepts en maîtrise provisoire héritée échouent la vérification, revoir le protocole de calibrage. |

---

## 3. Paramètres de la temporalité et de l'interleaving (P3)

*Ancrage constitutionnel : Principe 3*

### P3-1 — Condition de bascule vers l'interleaving de contenus

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | ≥ 2 réussites consécutives sans aide sur ≥ 3 tâches distinctes du niveau Bloom cible, pour chaque contenu |
| **Fourchette** | Réussites ∈ [1, 3] ; tâches ∈ [2, 5] |
| **Signal de révision** | Si interleaving déclenché génère chute précision > 20 pp, relever les seuils. |

### P3-2 — Seuil de rééquilibration de la couverture (interleaving par catégories)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Rééquilibration si un item n'a pas été présenté depuis ≥ 2× le délai moyen des autres items de la même catégorie |
| **Fourchette** | Multiplicateur ∈ [1.5×, 3×] |
| **Signal de révision** | Si retrieval-induced forgetting mesuré en évaluation, abaisser le multiplicateur. |

### P3-3 — Longueur du diagnostic de session de reprise

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | 3 à 5 tâches de rappel sur les concepts récemment maîtrisés |
| **Fourchette** | [2, 8] tâches |
| **Signal de révision** | Si dégradations sous-estimées, augmenter le nombre de tâches. |

---

## 4. Paramètres de la personnalisation (P5)

*Ancrage constitutionnel : Principe 5*

### P5-1 — Profils d'apprenants surveillés par défaut (équité algorithmique)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | A minima : niveau initial (calibrage P0) et régularité d'usage. Profils étendus : définis par univers. |
| **Signal de révision** | Si écart systématique non anticipé détecté en évaluation, ajouter l'attribut concerné. |

### P5-2 — Métriques d'équité de référence

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Taux MSC atteint, temps moyen jusqu'au MSC, taux d'abandon — comparés entre groupes P5-1 |
| **Signal de révision** | Écart entre groupes dépassant le seuil défini par univers → révision obligatoire du modèle adaptatif. |

### P5-3 — Régimes d'activation prioritaires (matrice apprenant composite)

| Attribut | Valeur |
|---|---|
| **Version initiale (3 régimes moteur autonome)** | Détresse / Neutre / Sous-défi — implémentables par règles déterministes sur proxys + auto-rapport AR-N1/N2 |
| **Version intermédiaire (5 états)** | + axe Calibration déterministe (bien calibré / surestimateur / sous-estimateur) × régime neutre |
| **Cible complète (9 états)** | Matrice 3×3 conditionnée à validation empirique des règles d'inférence sur données terrain |
| **Signal de déploiement complet** | Validation empirique des politiques adaptatives des 5 états prioritaires + règles d'inférence des 4 états restants documentées et testées |

### P5-4 — Proxys comportementaux de l'axe régime d'activation

*Ces proxys constituent le signal de fond permanent. Ils sont complétés et corrigés par l'auto-rapport (section 12). Un proxy dont le taux de discordance avec les auto-rapports dépasse le seuil AR-5 est reclassé comme invalidé pour cet apprenant.*

| Proxy | Mesure | Seuil régime de détresse | Seuil régime de sous-défi |
|---|---|---|---|
| **Taux d'erreur** | % d'échecs sur fenêtre glissante N=5 tentatives au niveau Bloom cible | > 60% | < 15% |
| **Ratio d'abandon** | Abandons intra-mission / (abandons + complétions) sur la session | > 40% | — |
| **Fréquence des demandes d'aide** | Aides demandées / tâches complétées sur la session | > 1,5 | < 0,05 avec temps de réponse courts |
| **Temps de réponse relatif** | Ratio temps moyen session / médiane personnelle historique | > 2,0 | < 0,4 |

**Règle de combinaison proxy seuls** : régime déclaré si ≥ 2 proxys franchissent leur seuil dans le même sens. Un seul proxy → réponse conservatrice en attente de confirmation (auto-rapport ou session suivante).

**Règle de combinaison avec auto-rapport** : si un auto-rapport AR-Niveau 1 est disponible, il prime sur la combinaison proxy seuls pour la déclaration de régime (voir AR-4 section 12).

**Fourchettes des seuils** : taux d'erreur ∈ [50%, 70%] pour détresse, ∈ [10%, 25%] pour sous-défi ; ratio d'abandon ∈ [30%, 50%] ; fréquence aide ∈ [1,0, 2,0] ; temps de réponse ∈ [1,5, 2,5] pour lenteur, ∈ [0,3, 0,5] pour accélération.

**Statut de validation** : proxys supposés au déploiement initial. Statut mis à jour en phase Évaluation. Proxy dont la corrélation avec le régime AR n'est pas confirmée après 3 évaluations → suspendu et documenté comme invalidé.

**Signal de révision** : si changements de régime proxy jugés inadéquats par l'apprenant (auto-rapport discordant ≥ 40%), réviser les seuils ou le nombre de proxys requis.

### P5-5 — Niveau de confiance minimal avant adaptation à fort impact

| Attribut | Valeur |
|---|---|
| **Adaptation conservatrice** (message, légère variation de guidage) | ≥ 1 proxy OU 1 auto-rapport AR-N1 |
| **Adaptation standard** (changement de type de mission, ajustement de difficulté ±1 niveau) | ≥ 2 proxys concordants OU auto-rapport AR-N1 ou AR-N2 concordant |
| **Adaptation à fort impact** (reconfiguration de parcours, changement de difficulté > 1 niveau) | ≥ 3 proxys concordants ET auto-rapport AR-N1 ou AR-N2 concordant, OU auto-rapport AR-N2 + confirmation proxy |
| **Fourchette** | Adaptations conservatrices : 1 signal suffit. Adaptations à fort impact : seuil non réductible sous 2 signaux concordants. |
| **Signal de révision** | Si le moteur déclenche des adaptations à fort impact non confirmées par les sessions suivantes, augmenter le seuil de confiance. |

---

## 5. Paramètres de l'adaptation à l'environnement d'usage (P7)

*Ancrage constitutionnel : Principe 7*

### P7-1 — Seuil de fatigue cognitive intra-session (proxy temporel)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | 25 minutes de travail actif (garde-fou de dernier ressort) |
| **Fourchette** | [15 min, 40 min] |
| **Rôle** | Garde-fou uniquement. Le budget cognitif pondéré (DA-2) est le pilote principal. Le seuil temporel intervient si le budget n'a pas déclenché de bascule avant 25 min. |
| **Signal de révision** | Si chute de performance avant 25 min, abaisser pour ce profil. |

---

## 6. Paramètres de la gamification éthique (P8)

*Ancrage constitutionnel : Principe 8*

### P8-1 — Indicateurs opérationnels du test de non-nuisance

| Indicateurs | Au moins l'un des trois : (a) absence de dégradation du MSC moyen sur sessions avec l'élément vs sans ; (b) absence de corrélation positive entre exposition à l'élément et réduction de composante A ; (c) absence de corrélation positive entre exposition et abandon des missions complexes. |
|---|---|
| **Condition de validation** | 1 indicateur suffit pour lever la période probatoire — les 3 devraient être mesurés. |
| **Signal de révision** | Si aucun des trois indicateurs n'est mesurable, l'élément reste en période probatoire. |

---

## 7. Paramètres de la métacognition et du lien social (P9)

*Ancrage constitutionnel : Principe 9*

### P9-1 — Seuil d'activation de la fonctionnalité sociale

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | 5 sessions complétées |
| **Fourchette** | [3, 10] sessions |
| **Signal de révision** | Si taux d'activation < 20% après le seuil, revoir le timing ou la forme. |

### P9-2 — Seuil de détection de l'évitement métacognitif

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Évitement confirmé si : (a) temps sur les écrans de réflexion < 30% de la médiane observée sur apprenants comparables, ET (b) taux d'erreur post-prompt inchangé (variation < 5 pp) sur 3 sessions consécutives |
| **Fourchette** | Seuil temps ∈ [20%, 50%] de la médiane ; fenêtre ∈ [2, 5] sessions |
| **Conséquence** | Retour à des prompts plus guidés et plus courts. Évitement persistant ≥ 5 sessions → candidat à un patch (section 11). |
| **Signal de révision** | Si taux de faux positifs > 20%, relever le seuil de temps ou allonger la fenêtre. |

---

## 8. Paramètres du cycle ADDIE — Évaluation

*Ancrage constitutionnel : Cycle de design pédagogique, étape 5*

### ADDIE-0 — Protocole de validation du graphe produit par la chaîne IA de conception

| Critère | Condition minimale |
|---|---|
| **Couverture Bloom** | Chaque objectif déclaré = ≥ 1 nœud au niveau cognitif cible |
| **Cohérence des prérequis** | Absence de cycles ; chaque arête justifiée dans la documentation |
| **Flags misconception** | Tous les concepts à misconception documentée sont flaggés |
| **Couverture des missions** | Chaque nœud : ≥ 1 mission conflit cognitif (si flaggé), ≥ 1 mission générative, ≥ 3 templates de feedback par type d'erreur principal |
| **Formats de récupération** | ≥ 2 formats distincts (reconnaissance, rappel indicé, rappel libre, production longue) par nœud au niveau Bloom cible |
| **Contenus AR-Niveau 1** | Libellés et options de réponse des micro-sondages événementiels définis pour les principaux types d'événements de l'univers |

**Statuts de déploiement** : tous critères satisfaits → déploiement standard. Critères Bloom + prérequis OK, reste incomplet → pilote restreint (N ≤ 30). Critères Bloom ou cycles non satisfaits → déploiement suspendu.

### ADDIE-1 — Seuil de biais systématique déclenchant révision du modèle d'inférence

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Sur ≥ 3 évaluations consécutives, écart médian maîtrise estimée / performance réelle > 20% |
| **Fourchette** | Évaluations ∈ [2, 5] ; écart ∈ [15%, 30%] |
| **Signal de révision du seuil** | Si révisions déclenchées à 20% ne produisent pas d'amélioration, remonter à la phase Analyse. |

### ADDIE-2 — Seuil de révision du modèle commun en usage cohorte

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Écart > 15% sur ≥ 10 apprenants d'une même cohorte |
| **Fourchette** | Écart ∈ [10%, 25%] ; N ∈ [5, 20] |
| **Signal de révision** | Si révisions trop fréquentes, augmenter N ou le seuil. |

### ADDIE-3 — Seuil d'efficience par nœud (révision structurelle du graphe)

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Nœud signalé si temps médian > 2× la valeur cible documentée en phase Analyse |
| **Fourchette** | Multiplicateur ∈ [1.5×, 3×] |
| **Conséquence** | Révision structurelle du graphe (ajout/suppression/refactorisation de nœuds) par la chaîne IA de conception. |
| **Signal de révision** | Si révisions structurelles ne produisent pas d'amélioration, remettre en cause la valeur cible. |

### ADDIE-4 — Analyse de concordance auto-rapport / proxys comportementaux

*Nouveau en v0.3. Ancrage constitutionnel : Cycle ADDIE étape 5, P9, section 12.*

| Attribut | Valeur |
|---|---|
| **Mesure de concordance** | Pour chaque proxy P5-4, calculer le taux de concordance avec les auto-rapports AR-N1 et AR-N2 de même session : proportion de cas où proxy et auto-rapport indiquent le même régime |
| **Seuil de concordance minimale** | ≥ 60% de concordance pour considérer un proxy comme valide pour un univers donné |
| **Fourchette** | [50%, 75%] — en dessous de 50%, le proxy est probablement invalide pour cet univers ; au-dessus de 75%, le proxy est redondant avec l'auto-rapport et peut être dépriorisé |
| **Conséquence d'un proxy invalide** | Reclassé comme "invalidé pour cet univers" dans la documentation. Son poids dans la règle de combinaison P5-4 est mis à zéro pour cet univers. Il peut être conservé pour d'autres univers. |
| **Signal de révision** | Si aucun proxy n'atteint le seuil de concordance sur un univers donné, revoir les seuils P5-4 ou la formulation des auto-rapports AR. |

### ADDIE-5 — Analyse de la distribution SIS à l'échelle de la cohorte

*Nouveau en v0.3. Ancrage constitutionnel : P13, section 13.*

| Attribut | Valeur |
|---|---|
| **Mesure** | Distribution des SIS de toutes les sessions de la cohorte sur la période d'évaluation |
| **Signal d'alerte** | Si > 15% des sessions ont un SIS < 0,4 (seuil d'anomalie élevée), une dérive systémique d'intégrité est probable |
| **Signal de révision** | Si la distribution SIS se dégrade progressivement entre deux évaluations, investiguer les patterns de partage de dispositif et renforcer la communication sur le multi-profil |

---

## 9. Paramètre de P1 — Niveau cognitif minimum des concepts fondamentaux

### P1-1 — Niveau Bloom minimum pour concepts fondamentaux hors annales

| Attribut | Valeur |
|---|---|
| **Valeur de référence** | Niveau *comprendre* |
| **Fourchette** | *mémoriser* à *appliquer* |
| **Signal de révision** | Si concepts maintenus à *comprendre* jamais mobilisés dans les missions d'intégration, baisser à *mémoriser*. |

---

## 10. Périmètre de déploiement

| Fonctionnalité | Statut initial | Condition de généralisation |
|---|---|---|
| **Flag Misconception** | Optionnel | Obligatoire pour domaines à fort taux de misconceptions dès la deuxième version |
| **Matrice 3 régimes** | Implémentée (MVP) | — |
| **Matrice 5 états** | Conditionnée à l'axe Calibration déterministe | Dès validation de l'écart prédiction/performance comme signal fiable |
| **Matrice 9 états complète** | Conditionnée à validation empirique | Données terrain univers pilote (P5-3) |
| **Auto-rapport AR-N1** | Implémenté (MVP) — triggers de base | Extension aux triggers univers-spécifiques en phase Design |
| **Auto-rapport AR-N2** | Implémenté (MVP) | — |
| **Auto-rapport AR-N3** | Déploiement différé — après 30 apprenants avec ≥ 10 sessions | Extension des dimensions après validation AR-N2 |
| **SIS complet** | Version simplifiée MVP (trajectory consistency uniquement) | Extension aux 4 indicateurs dès baseline personnelle disponible (≥ 15 sessions) |
| **Mode Évaluation Externe** | Optionnel — conditonné à un partenariat institutionnel | — |
| **Équité — attributs étendus** | Niveau initial + régularité | Extension selon données disponibles et cadre légal |
| **Apprentissage par les pairs** | Optionnel par univers | Justification obligatoire |

---

## 11. Paramètres des patchs IA (P12)

*Ancrage constitutionnel : Principe 12*

### PATCH-1 — Déclencheurs de patch

| Déclencheur | Seuil | Priorité |
|---|---|---|
| Écart individuel maîtrise estimée / performance réelle | > 20% sur ≥ 3 évaluations consécutives (ADDIE-1) | Haute |
| Biais systématique cohorte | > 15% sur ≥ 10 apprenants (ADDIE-2) | Haute |
| Taux de révocation MSC | > 30% des concepts déclarés maîtrisés (MSC-deg) | Haute |
| Oscillation récurrente d'un concept | ≥ 3 cycles maîtrisé → révoqué → remaîtrisé | Haute |
| Écarts d'équité entre groupes | Dépassement seuil P5-2 | Haute |
| Proportion de sessions SIS < 0,3 | > 20% des sessions d'un apprenant sur 30 jours | Haute |
| Proxy invalidé par concordance AR (ADDIE-4) | Taux de concordance proxy < 50% sur un univers | Moyenne |
| Échec test de non-nuisance gamification | Non-satisfaction des indicateurs P8-1 | Moyenne |
| Évitement métacognitif persistant | ≥ 5 sessions en état d'évitement confirmé (P9-2) | Moyenne |
| Biais de désirabilité sociale AR élevé | Indice de calibration AR-N3 ≤ seuil AR-6 | Moyenne |
| Abandon calibrage | > 20% des apprenants n'atteignent pas la fin du calibrage | Moyenne |
| Série d'overrides apprenant | ≥ 5 overrides consécutifs signalant désalignement adaptatif | Basse |

### PATCH-2 — Périmètre autorisé des modifications par patch

| Catégorie | Autorisé | Interdit |
|---|---|---|
| **Paramètres du référentiel** | Ajustement dans les fourchettes définies | Modification hors fourchettes constitutionnelles |
| **Graphe de connaissances** | Révision des poids, ajout/désactivation de nœuds secondaires | Modification de la structure principale sans retour en Analyse/Design |
| **Missions et contenus** | Ajout de variantes de missions, templates de feedback, sous-parcours | Génération de contenu fondamentalement nouveau sans validation chaîne de conception |
| **Politiques adaptatives** | Révision du mapping régimes → politiques, ajustement des seuils | Redéfinition des composantes MSC, modification philosophie d'adaptation (P5, P8, P13) |
| **Matrice apprenant** | Activation version étendue (5 ou 9 états) si données suffisantes | Introduction de nouveau mécanisme d'inférence sans statut probatoire |
| **Auto-rapport** | Ajustement des seuils de déclenchement AR-N1 dans les fourchettes | Suppression d'un niveau d'auto-rapport ou substitution par inférence comportementale seule |
| **Proxys comportementaux** | Recalibration des seuils P5-4 dans les fourchettes, mise à zéro du poids d'un proxy invalidé | Suppression de la règle de concordance minimale ou de la hiérarchie auto-rapport/proxy |

### PATCH-3 — Attributs obligatoires de tout patch

| Attribut | Description |
|---|---|
| **Versionné** | Numéro de version, date, identifiant du signal déclencheur |
| **Justifié** | Référence explicite au déclencheur PATCH-1 |
| **Borné** | Liste des paramètres modifiés avec valeurs avant/après |
| **Réversible** | Condition de rollback définie avec délai d'observation |
| **Transparent** | Description lisible par l'apprenant : ce qui change, pourquoi |
| **Conforme** | Vérification de non-contradiction avec P5, P8, P13 avant déploiement |

### PATCH-4 — Fréquence maximale et propagation des patchs

| Attribut | Valeur |
|---|---|
| **Fréquence individuelle** | 1 patch / 14 jours (sauf déclencheur haute priorité) |
| **Fréquence cohorte** | 1 patch / 30 jours |
| **Signal d'alerte** | Fréquence moyenne > 1 patch / 14 jours → révision de la couche conception. |

---

## 12. Paramètres de l'auto-rapport affectif (AR)

*Ancrage constitutionnel : Principe 9 (système d'auto-rapport à trois niveaux)*

---

### AR-1 — Conditions de déclenchement du micro-sondage événementiel (AR-Niveau 1)

*Le AR-Niveau 1 est le seul mécanisme permettant de distinguer confusion productive, frustration et anxiété en temps réel. Son déclenchement est événementiel — jamais périodique — pour maximiser la pertinence contextuelle et minimiser la réactivité d'évaluation.*

| Événement déclencheur | Condition précise | Priorité |
|---|---|---|
| **Série d'échecs consécutifs** | ≥ 3 échecs consécutifs sur le même nœud du graphe, au même niveau Bloom | Haute |
| **Complétion d'un boss** | Fin de toute mission de type boss (réussite ou échec) | Haute |
| **Série de réussites en autonomie** | ≥ 5 réussites consécutives sans aide, toutes au niveau Bloom cible | Moyenne |
| **Session significativement prolongée** | Durée de session > 1,5× la médiane personnelle des 10 dernières sessions | Moyenne |
| **Premier contact avec un type de mission nouveau** | Première occurrence d'un type de mission non encore rencontré par cet apprenant | Basse |

**Contraintes de déclenchement** :
- Jamais en milieu de tâche active : uniquement aux points de rupture naturelle (entre missions, après un feedback, à la clôture d'une séquence).
- Maximum 2 déclenchements de AR-Niveau 1 par session. Si un 3e événement survient, il est logué mais n'affiche pas de sondage.
- Délai minimal entre deux déclenchements AR-Niveau 1 : 5 minutes de temps actif de session.
- Déclencheurs définis par univers en phase Design : la liste ci-dessus est la liste de référence ; chaque univers peut ajouter des déclencheurs spécifiques à ses types de missions.

**Format obligatoire** :
- 1 question, format visuel (pictogrammes ou libellés courts), 2 ou 3 options de réponse.
- Temps de réponse attendu : < 10 secondes.
- Ancrage sur l'événement, pas sur le soi : *"Cette mission était..."* et non *"Tu te sens..."*
- Formulation non anxiogène : les options doivent être perçues comme toutes légitimes.

**Question de référence pour les séries d'échecs** (le cas le plus critique) :

> *"Ces erreurs, ça te semble... [Je cherche encore] / [J'ai envie de passer à autre chose]"*

- *"Je cherche encore"* → confusion productive → intervention : scaffolding maintenu, difficulté conservée, message de normalisation de l'effort.
- *"J'ai envie de passer à autre chose"* → frustration/épuisement → intervention : réduction de charge ou changement de format.
- Si auto-rapport non disponible (événement non déclenché, réponse ignorée) → régime inféré par proxys seuls → intervention conservatrice par défaut.

**Fourchette** : nombre maximal de déclenchements ∈ [1, 3] par session ; délai minimal ∈ [3, 10] minutes de temps actif.

**Signal de révision** : si taux d'ignorance du sondage (fermé sans réponse) > 30% sur 10 sessions, revoir le format ou réduire la fréquence des déclencheurs.

---

### AR-2 — Mini-sondage de fermeture (AR-Niveau 2)

*Le AR-Niveau 2 fournit une lecture rétrospective de la session. Il est sujet au peak-end rule (Kahneman) — l'apprenant pondère excessivement le moment le plus intense et les dernières minutes. Le système tient compte de ce biais en croisant AR-N2 avec les proxys intra-session et les AR-N1 disponibles.*

**Dimensions mesurées (3 items maximum) :**

| Dimension | Libellé de référence | Format | Ancrage théorique |
|---|---|---|---|
| **Difficulté perçue** | *Cette session était pour toi...* → ← trop facile / juste bien / trop difficile → | Slider 5 positions ou 3 pictogrammes | Control appraisal (CVT Pekrun) |
| **Sentiment de progrès** | *Tu as l'impression d'avoir progressé ?* → Non / Un peu / Oui clairement | 3 pictogrammes | Value appraisal (CVT Pekrun) |
| **Envie de revenir** | *Envie de refaire une session bientôt ?* → Pas vraiment / Pourquoi pas / Oui | 3 pictogrammes | Intention comportementale — indicateur SDT |

**Fréquence adaptative de déclenchement :**

| Condition | Déclenchement AR-N2 |
|---|---|
| Un AR-N1 a été répondu pendant la session | Systématique — validation de la lecture de session |
| Les proxys P5-4 ont déclenché un régime non-neutre pendant la session | Systématique |
| Première session de la semaine | Systématique |
| Session suivant une interruption ≥ 7 jours | Systématique |
| Première session sur un nouveau type de mission | Systématique |
| Sinon (session routinière, proxys neutres) | Toutes les 4 sessions (± 1 pour éviter la prédictibilité) |
| Maximum en toute circonstance | 1 fois par session |

**Contraintes de format** :
- Affiché uniquement à la fermeture volontaire de la session — jamais comme condition pour quitter.
- Optionnel : l'apprenant peut ignorer sans pénalité. Le taux de réponse est suivi comme métrique de qualité.
- Temps de réponse attendu : < 20 secondes.
- Pas de champ texte libre : toutes les options sont visuelles ou à choix limité.

**Fourchette** : fréquence routinière ∈ [toutes les 3 sessions, toutes les 6 sessions].

**Signal de révision** : si taux de réponse AR-N2 < 50% sur 20 sessions, revoir le format ou le moment de déclenchement.

---

### AR-3 — Bilan de trajectoire périodique (AR-Niveau 3)

*Le AR-Niveau 3 mesure des tendances, pas des états ponctuels. Il sert à calibrer la fiabilité des auto-rapports des deux autres niveaux (détection du biais de désirabilité sociale) et à fournir une vue longitudinale que les sessions individuelles ne permettent pas.*

**Fréquence** : 1 fois par semaine si ≥ 3 sessions dans la semaine, ou toutes les 5 sessions si la fréquence hebdomadaire est inférieure.

**Modalité** : Déclenché au début d'une session (pas à la fermeture) dans un moment de faible charge. Format bref (5 à 7 items, < 2 minutes). Questions portant sur *les dernières sessions* et non sur la session en cours.

**Dimensions du AR-N3 :**

| Dimension | Libellé de référence | Format |
|---|---|---|
| **Tendance de difficulté** | *Ces derniers jours, les sessions te semblent...* → Plus faciles qu'avant / Pareil / Plus difficiles | 3 options |
| **Tendance d'engagement** | *Tu as envie de faire des sessions...* → Moins qu'avant / Pareil / Plus qu'avant | 3 options |
| **Clarté des progrès** | *Tu vois que tu progresses ?* → Pas vraiment / Un peu / Oui clairement | 3 options |
| **Pertinence perçue** | *Ce que tu travailles te semble utile pour l'examen ?* → Pas trop / Moyennement / Oui | 3 options |
| **Calibration check** | *Ta dernière simulation d'examen s'est passée mieux, pareil, ou moins bien que tu ne pensais ?* | 3 options + "je n'en ai pas fait" |

**Utilisation du AR-N3** :
- Alimente le modèle de tendance long terme de l'axe Calibration (P5, axe 1).
- Génère l'indice de calibration de l'auto-rapport (voir AR-6).
- N'est pas utilisé directement pour des adaptations immédiates de session : il informe les révisions périodiques du parcours (planification vers date cible, P4).

**Fourchette** : fréquence ∈ [toutes les 4 sessions, hebdomadaire selon fréquence d'usage].

**Signal de révision** : si taux de complétion AR-N3 < 40%, revoir le moment de déclenchement (début de session vs moment dédié séparé).

---

### AR-4 — Hiérarchie de confiance et règles d'intégration auto-rapport / proxys

*Cette section est la clé d'intégration du système d'auto-rapport dans le modèle P5. Elle est normative — les règles définies ici s'imposent au moteur autonome.*

**Hiérarchie de confiance décroissante :**

1. **AR-Niveau 1 concurrent à l'événement** : validité maximale. L'apprenant rapporte son état au moment où il se produit — biais de rappel minimal. *Écrase la lecture proxy pour la décision immédiate.*
2. **AR-Niveau 2 de fermeture** : validité haute pour l'état de fin de session, modérée pour le pic de session (biais peak-end). *Valide ou corrige la lecture proxy de session ; prime sur les proxys si discordant.*
3. **Proxys comportementaux P5-4** : validité moyenne, signal permanent, utile en l'absence d'auto-rapport. *Source de base et signal de déclenchement des sondages.*
4. **AR-Niveau 3 de trajectoire** : validité haute pour les tendances long terme, non pertinent pour les décisions immédiates. *Informe les révisions de parcours et la calibration des proxys.*

**Règles d'intégration opérationnelles :**

| Situation | Règle |
|---|---|
| AR-N1 disponible et concordant avec les proxys | Régime confirmé → politique adaptative standard associée déclenchée |
| AR-N1 disponible et discordant avec les proxys | AR-N1 prime → régime mis à jour selon AR-N1 → discordance consignée |
| AR-N1 non disponible, ≥ 2 proxys concordants | Régime déclaré par proxys → intervention conservatrice (pas d'adaptation à fort impact) |
| AR-N1 non disponible, 1 seul proxy hors seuil | Régime neutre maintenu → surveillance renforcée → AR-N2 déclenché en fin de session |
| AR-N2 discordant avec la lecture proxy de session | AR-N2 prime → régime de session révisé → discordance consignée |
| AR-N2 et proxys concordants sur régime non-neutre | Régime confirmé → peut déclencher une adaptation à fort impact si cohérent sur ≥ 2 sessions |

**Règle de non-surcharge** : si un AR-N1 vient d'être répondu, aucune adaptation comportementale lourde n'est déclenchée pendant les 10 minutes suivantes. Le moteur observe si l'intervention conservatrice imédiate modifie le comportement avant d'aller plus loin.

---

### AR-5 — Protocole de discordance et recalibration des proxys

*Une discordance survient quand l'auto-rapport et le proxy indiquent des régimes différents. Les discordances sont des données précieuses : elles signalent que le proxy est mal calibré pour cet apprenant ou cet univers.*

**Calcul de la discordance par proxy :**

Pour chaque proxy P (taux d'erreur, ratio abandon, fréquence aide, temps de réponse) :
- À chaque session où un AR-N1 ou AR-N2 est disponible : comparer le régime indiqué par P seul vs le régime auto-rapporté.
- Discordance = P et AR indiquent des régimes opposés (ex : proxy → détresse, AR → neutre ou sous-défi).
- Calculer le **taux de discordance cumulé** de P pour cet apprenant sur les N dernières sessions documentées.

| Taux de discordance cumulé | Action |
|---|---|
| < 25% | Proxy valide — poids standard dans la règle de combinaison P5-4 |
| 25% – 50% | Proxy dégradé — poids réduit à 50% dans la règle de combinaison. Alerte documentée. |
| > 50% | Proxy invalidé pour cet apprenant — poids mis à zéro. Consigné dans le modèle. Déclenche un AR-N2 systématique jusqu'à accumulation de 10 nouvelles sessions. |

**Recalibration possible** : si un proxy invalidé redevient concordant (taux de discordance < 25%) sur 10 sessions après invalidation, son poids est restauré progressivement (50%, puis 100% après 10 sessions supplémentaires concordantes).

**Signal de révision** : si ≥ 2 proxys sont invalidés simultanément pour un même apprenant, et que les AR restent cohérents et non biaisés, la cause est probablement un changement de contexte d'usage (nouveau environnement, changement de dispositif, partage non signalé). Le moteur consigne l'anomalie et programme une vérification déclarative (INTEGRITE-5).

---

### AR-6 — Détection du biais de désirabilité sociale et indice de calibration AR

*Certains apprenants rapportent systématiquement des états positifs indépendamment de leur performance réelle — réponse automatique, évitement du jugement perçu, ou incompréhension des questions. Ce biais rend leurs auto-rapports peu fiables comme signal d'état. Le moteur doit le détecter et ajuster le poids accordé aux AR.*

**Calcul de l'indice de calibration AR (ICAR) :**

Sur les N dernières sessions avec AR-N2 disponible :

- Corrélation entre "sentiment de progrès" déclaré (AR-N2 dimension 2) et progression MSC réelle mesurée sur la même période.
- Corrélation entre "difficulté perçue" déclarée (AR-N2 dimension 1) et taux d'erreur moyen de session.

| Valeur ICAR | Interprétation | Action |
|---|---|---|
| ≥ 0,4 (corrélation modérée) | Auto-rapport calibré — fiable | Poids AR standard |
| 0,2 – 0,4 | Calibration partielle | Poids AR réduit à 75% — proxys gagnent de l'importance relative |
| < 0,2 | Auto-rapport potentiellement biaisé | Poids AR réduit à 50% — les proxys et l'AR-N1 (plus ancré dans l'événement) sont prioritaires. Déclenche un regard particulier en phase Évaluation. |

**Conditions de calcul** : ICAR calculable uniquement avec ≥ 10 sessions documentées avec AR-N2 ET données MSC. En dessous de 10 sessions, l'ICAR est non calculé et le poids AR est standard (bénéfice du doute).

**Signal de révision** : si ICAR < 0,2 persiste sur 20 sessions et que les proxys comportementaux semblent cohérents, envisager un retour au format de questions AR (reformulation, changement d'ancrage) via un patch.

---

## 13. Paramètres de l'intégrité du modèle apprenant

*Ancrage constitutionnel : Principe 13*

---

### INTEGRITE-1 — Calcul du Score d'Intégrité de Session (SIS)

*Le SIS est un score continu [0, 1] calculé pour chaque session. Un SIS proche de 1 indique un profil comportemental cohérent avec la baseline personnelle. Un SIS bas indique une anomalie — sans en présupposer la cause.*

**Composantes du SIS et leurs poids :**

| Composante | Description | Poids |
|---|---|---|
| **Cohérence de trajectoire** | Absence de saut de performance incompatible avec la courbe d'apprentissage (voir INTEGRITE-1a) | 40% |
| **Empreinte de latence** | Proximité de la distribution des temps de réponse de la session avec la baseline personnelle (voir INTEGRITE-1b) | 25% |
| **Profil d'erreurs** | Cohérence du type d'erreurs avec le profil historique de misconceptions de l'apprenant (voir INTEGRITE-1c) | 20% |
| **Fingerprint multidimensionnel** | Z-score multidimensionnel session vs baseline (accuracy, aide, abandon) | 15% |

**Déploiement progressif** : au MVP (baseline personnelle < 15 sessions), seule la cohérence de trajectoire est calculée (version SIS simplifiée = SIS-t). Les autres composantes s'activent automatiquement lorsque la baseline personnelle est suffisante.

**INTEGRITE-1a — Cohérence de trajectoire :**

Pour chaque concept C avec historique H(C) = accuracy moyenne sur les 5 dernières sessions :

- Si accuracy en session > H(C) + 40 pp en une session unique → anomalie de trajectoire sur C
- Si anomalie sur ≥ 3 concepts distincts dans la même session → signal de substitution probable

Score de cohérence = 1 - (nombre de concepts avec anomalie de trajectoire / nombre de concepts testés dans la session), plafonné à 1.

**INTEGRITE-1b — Empreinte de latence :**

Baseline personnelle de latence : distribution des temps de réponse sur les 10 dernières sessions (médiane, variance, percentile 10, percentile 90).

Pour la session courante, calculer l'écart entre la distribution de session et la baseline :
- Variance divisée par 2 ou plus ET médiane divisée par 1,5 ou plus → signature d'expert (réponses très rapides et très régulières) → SIS latence abaissé
- Médiane × 3 ou plus → session très lente (fatigue extrême ou contexte inhabituel) → anomalie de type "état intra-individuel" → SIS latence abaissé modérément mais pas en sens "substitution"

Score de latence = 1 si écart < 1 écart-type ; décroit linéairement vers 0 pour les écarts > 3 écarts-types dans le sens "expert".

**INTEGRITE-1c — Profil d'erreurs :**

Pour chaque nœud du graphe avec flag misconception ou historique d'erreurs typées :
- Comparer le type d'erreurs de la session avec le profil historique de l'apprenant.
- Si les erreurs de session ne correspondent pas aux erreurs historiques ET que la précision est anormalement haute → signal de substitution.

Score de profil = 1 si ≥ 80% des erreurs de session correspondent au profil historique ou si aucune erreur (et SIS cohérence de trajectoire normal) ; 0,5 si profil d'erreurs entièrement nouveau ; 0 si profil d'erreurs entièrement nouveau + précision anormalement haute.

**Calcul final du SIS :**

```
SIS = 0,40 × score_trajectoire + 0,25 × score_latence + 0,20 × score_profil_erreurs + 0,15 × score_fingerprint
```

En version simplifiée MVP (baseline < 15 sessions) :
```
SIS-t = score_trajectoire
```

**Fourchette des poids** : les poids ci-dessus peuvent être ajustés ∈ [30%, 50%] pour la trajectoire, ∈ [15%, 35%] pour la latence, ∈ [10%, 30%] pour le profil d'erreurs, ∈ [10%, 20%] pour le fingerprint — sous réserve que la somme reste = 100%.

**Signal de révision** : si plus de 10% des sessions d'apprenants vérifiés (par déclaration) ont un SIS < 0,5 sans substitution réelle, les seuils de calcul sont trop stricts — réviser les fourchettes d'anomalie.

---

### INTEGRITE-2 — Règles d'intégration des sessions selon SIS dans le MSC

| SIS | Statut de la session | Mode d'intégration |
|---|---|---|
| ≥ 0,8 | **Session normale** | Intégration complète dans les composantes MSC |
| 0,5 – 0,8 | **Session atypique** | Intégration pondérée : chaque point de performance compte pour SIS × valeur nominale |
| 0,3 – 0,5 | **Session en attente de confirmation** | Mise en attente : données non intégrées immédiatement. Si la session suivante a SIS ≥ 0,6 ET performance dans la fourchette habituelle → session en attente intégrée à 50%. Sinon → session écartée du MSC (données archivées, non supprimées). |
| < 0,3 | **Session fortement anomale** | Mise en attente. L'apprenant est informé de manière neutre (voir INTEGRITE-3). Choix proposé : comptabiliser ou non. Si pas de réponse dans 48h → session intégrée à 20% uniquement. |

**Règle de protection contre la pénalisation** : les anomalies dans le sens "moins bon que d'habitude" (fatigue, maladie) ne réduisent JAMAIS le MSC déjà acquis. Elles peuvent déclencher une révision de la composante R (vérification de robustesse temporelle) mais ne révoquent pas P ou A déjà validés sur la base de sessions normales.

**Signal de révision** : si plus de 15% des sessions d'un apprenant sur 30 jours sont en attente ou fortement anomales, déclencher le patch PATCH-1 (priorité haute).

---

### INTEGRITE-3 — Niveau de Confiance MSC (NC-MSC)

| NC-MSC | Condition | Conséquence pour le moteur |
|---|---|---|
| **Élevé** | Toutes les sessions contribuant à cette composante ont SIS ≥ 0,8 | Planification normale |
| **Moyen** | Au moins une session contribuante avec SIS ∈ [0,5, 0,8], pondérée dans le calcul | Planification normale ; vérification supplémentaire programmée au prochain cycle espacé |
| **Bas** | Au moins une session contribuante avec SIS < 0,5 a contribué significativement (poids ≥ 20% du score P ou A) | Composante traitée comme provisoire : vérification prioritaire dans les 2 sessions suivantes ; pas d'utilisation pour déclencher le fading (composante A) ni l'interleaving de contenus |

**Signal de révision** : si plus de 20% des composantes MSC d'un apprenant ont NC-MSC Bas, l'intégrité globale du modèle est compromise — déclencher la vérification déclarative (INTEGRITE-5) immédiatement.

---

### INTEGRITE-4 — Paramètres du Mode Invité

| Attribut | Valeur |
|---|---|
| **Accessibilité** | Bouton visible sur l'écran de sélection de session, niveau 1 de navigation (pas dans les paramètres) |
| **Indicateur visuel** | Bandeau persistant en haut de l'écran pendant toute la session, couleur distincte (non rouge/alarme) ; libellé : *"Mode exploration — cette session ne sera pas enregistrée"* |
| **Données enregistrées** | Aucune. Ni MSC, ni baseline comportementale, ni historique AR. Les données de session sont effacées à la fermeture. |
| **Durée maximale sans rappel** | 30 minutes : après 30 min en mode Invité sans activité, un rappel non bloquant s'affiche ("Tu es toujours en mode exploration") |
| **Désactivation** | Uniquement par le titulaire du profil (pas par un tiers en cours de session) |
| **Contenu accessible** | Identique à une session normale — aucune restriction de contenu |
| **Fourchette durée du rappel** | [20 min, 45 min] selon préférence univers |
| **Signal de révision** | Si taux d'utilisation du mode Invité > 20% des sessions d'un profil, investiguer si un profil multi-utilisateur n'est pas en réalité nécessaire. |

---

### INTEGRITE-5 — Vérification déclarative périodique

*Mécanisme de protection basé sur la bonne foi de l'apprenant. Non accusatoire, présenté comme une aide à la fiabilité du modèle.*

| Attribut | Valeur |
|---|---|
| **Fréquence** | Toutes les 8 sessions (± 2 pour éviter la prédictibilité) |
| **Moment** | Au démarrage d'une session (jamais à la fermeture ni en cours de session) |
| **Format** | 1 question, 3 options : *"Ces dernières sessions, c'était bien toi ?"* → [Oui] / [Pas toujours] / [Non] |
| **Option "Pas toujours" ou "Non"** | Affichage d'un menu sobre listant les N dernières sessions avec leur date ; possibilité de décocher les sessions non conduites par l'apprenant. Recalcul du MSC sans les sessions décochées. Message : *"Pas de problème ! Ton modèle est mis à jour."* |
| **Aucune conséquence pénalisante** | Le refus de répondre ou la réponse "Oui" ne déclenche aucune alerte. |
| **Fourchette de fréquence** | ∈ [5, 15] sessions |
| **Signal de révision** | Si taux de réponse "Pas toujours" ou "Non" > 10% sur la cohorte, renforcer la communication sur le multi-profil au démarrage. |

---

### INTEGRITE-6 — Mode Évaluation Externe

| Attribut | Valeur |
|---|---|
| **Déclenchement** | Par l'enseignant/institution (nécessite un code ou lien spécifique) ou par l'apprenant depuis son interface |
| **Données enregistrées** | Oui — taguées "évaluation externe" avec date, contexte et identifiant de l'évaluateur si renseigné |
| **Impact MSC** | Alimente uniquement la composante T (Transférabilité) — n'impacte pas P, R, A |
| **SIS en mode Évaluation Externe** | Non calculé — les conditions d'évaluation formelle produisent des anomalies légitimes (stress, conditions différentes) |
| **Indicateur visuel** | Bandeau persistant distinct du mode Invité : *"Session d'évaluation — résultats enregistrés pour la composante T"* |
| **Partage des résultats** | Uniquement avec consentement explicite de l'apprenant ; partage limité aux résultats T, pas au reste du modèle |
| **Signal de révision** | Si les résultats T obtenus en mode Évaluation Externe sont systématiquement inférieurs à la maîtrise d'entraînement, revoir le design des missions de transfert (composante T) dans le graphe. |

---

### INTEGRITE-7 — Architecture multi-profil

| Attribut | Valeur |
|---|---|
| **Nombre de profils par dispositif** | Illimité |
| **Isolation des modèles** | Totale — chaque profil dispose de son propre MSC, baseline comportementale, historique AR, état apprenant composite, et paramètres SIS |
| **Sélection au démarrage** | Obligatoire si plusieurs profils existent : écran de sélection de profil avant toute session |
| **Création d'un profil** | Sans compte email obligatoire pour les profils secondaires — nom ou surnom suffit. Un profil principal reste lié à un compte (pour la persistance cloud si disponible). |
| **Suppression d'un profil** | Possible avec confirmation — supprime toutes les données associées. |
| **Communication recommandée** | Au premier démarrage et lors de toute session en mode Invité prolongée : rappel de l'existence du multi-profil et de son usage recommandé pour le partage de dispositif |
| **Signal de révision** | Si moins de 30% des foyers utilisant un dispositif partagé ont créé plusieurs profils (données d'usage agrégées), renforcer le prompt de création au démarrage. |

---

## 14. Décisions d'architecture

### DA-1 — Typage des arêtes du graphe de connaissances

**Statut** : Décision ouverte. Option B (typage minimal 2 types) recommandée pour le MVP.

### DA-2 — Budget cognitif de session *(décision fermée — Option B retenue)*

**Décision** : Budget cognitif = somme pondérée des tâches complétées par type.

| Type de tâche | Poids de charge |
|---|---|
| Reconnaissance / QCM | 1 |
| Rappel indicé | 2 |
| Rappel libre court | 3 |
| Application procédurale simple | 3 |
| Problème multi-étapes | 5 |
| Mission générative | 4 |
| Boss / simulation d'examen | 6 |

Budget de référence : 20 unités (fourchette ∈ [12, 30]). Proxy temporel de 25 min = garde-fou de dernier ressort.

**Annotations obligatoires** : tout type de mission annoté de son poids dans le graphe de design.

### DA-3 — Composante G (Généralisation) dans le MSC

**Statut** : Décision ouverte. G documentée comme cible conceptuelle pour univers avec objectif de transfert lointain, sans intégration au MSC.

### DA-4 — Algorithme d'espacement *(décision fermée — SM-2 simplifié)*

| Paramètre | Valeur de référence | Fourchette |
|---|---|---|
| Intervalle initial | 1 jour | [1, 3 jours] |
| Deuxième intervalle | 3 jours | [2, 5 jours] |
| Facteur de facilité de base (EF) | 2,5 | [1,3 ; 3,0] |
| Incrément EF / réussite sans aide | +0,1 | [+0,05 ; +0,15] |
| Décrement EF / échec | -0,2 | [-0,3 ; -0,1] |
| EF minimum | 1,3 | Non modifiable |
| Intervalle si réussite | Intervalle précédent × EF | — |
| Intervalle si échec | Retour à l'intervalle initial | — |

**Note** : le SIS d'une session influence les paramètres EF de la session : pour SIS < 0,5, la mise à jour EF (incrément ou décrément) est pondérée par le SIS. Une réussite avec SIS = 0,3 incrémente EF de 0,03 seulement, pas de 0,1.

---

*Référentiel de defaults pédagogiques v0.3 — complément opérationnel de la Constitution v1.4. À réviser librement à partir des données terrain. Toute révision contrevenant à un principe de la Constitution v1.4 doit être traitée comme modification constitutionnelle.*
