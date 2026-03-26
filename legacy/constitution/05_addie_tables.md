### Mécanismes — Cycle ADDIE `[S18]` `[MODIFIÉ S18 v1.5→v1.6]`

1. **Analyse** : extraire KU, construire graphe, déclarer type KU dominant (P14) + ICC + niveau autonomie (P15) + axe de progression (P1) + alignement constructif (Biggs) + flags misconception + objectif transfert lointain + **[AJOUTÉ] contexte authentique de référence (P19)** + **[AJOUTÉ] activation axe VC si souhaité (P18)**. Définir proxys comportementaux + statut validation empirique + profils équité + conditions AR-N1. Déclarer arêtes dépendance graphe (requis P17). Valider graphe (couverture, cohérence arêtes, human_checkpoints requis). Graphe insuffisant → pilote restreint uniquement.
2. **Design** : trajectoire pédagogique par type KU. Missions conflit cognitif (nœuds flaggés), missions génératives, décision productive failure, templates feedback (P10), **[AJOUTÉ] matrice couverture feedback (P2 — livrable obligatoire pour KU formelles et procédurales)**, contenus AR-N1 (libellés + mapping régimes), **[AJOUTÉ] item AR-N2 VC (P18 si axe activé)**, **[AJOUTÉ] item AR-N2 intention session (P9)**, human_checkpoints. Transitions = seuils MSC définis en Analyse. Missions de niveau Bloom ≥ 4 liées au contexte authentique (P19).
3. **Développement** : contenus jouables respectant charge cognitive, motivation, métacognition, éthique. Formats sondages AR (N1, N2, N3) = livrables **obligatoires**.
4. **Implémentation** : déploiement + configuration. Gamification non vérifiée → **mode probatoire**. Configuration modes Invité, Évaluation Externe, multi-profil. Vérification règle de propagation graphe activée (P17).
5. **Évaluation** : déclencheurs (écart ponctuel, biais systématique, dérive hors-jeu, **[AJOUTÉ] VC Bas persistant (P18)**, **[AJOUTÉ] taux erreurs hors-taxonomie > seuil (P2)**). Inclut systématiquement : test non-nuisance gamification probatoire ; métriques équité ; confrontation règles inférence / données + mise à jour statut validation ; efficience par nœud ; concordance AR / proxys (proxy taux discordance élevé → "hypothèse invalidée" + retiré du modèle) ; distribution SIS cohorte ; **[AJOUTÉ] taux couverture matrice feedback par univers** ; **[AJOUTÉ] profils AR-réfractaires détectés**.

***

### Tables récap `[INFÉRÉ]`

**MSC — Opérandes par type de KU** `[S20]`

| Composante | Déclarative (réf.) | Formelle | Procédurale | Perceptuelle | Créative |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **P** | Taux ≥ 80% sur N≥5 | 100% chaîne complète | Score rubrique multi-dim ≥ seuil | d-prime (SDT) ≥ seuil | Critères formels + rubrique auto-déclaré calibré |
| **R** | Réussite après délai D | Idem déclarative | D × ×2–3 | D × ×0,5 | D × ×1 (fallback P3) |
| **A** | M réussites sans aide textuelle | Sans scaffolding formel | M exécutions, variabilité inter-essais < seuil, sans guidage physique | M discriminations sans étiquette ni contraste | M productions page blanche sans prompt ni template |
| **T** | Format structurellement différent | Problème isomorphe | Exécution sous contrainte modifiée | Conditions dégradées / exemplaires atypiques | Registre/contrainte radicalement différent |

> Agrégation : P AND R AND A ≥ seuils → maîtrise de base. T = niveau supérieur, indépendant. `[P16]` `[AJOUTÉ]`

---

**Modèle d'état apprenant — 3 axes** `[S7][INFÉRÉ]` `[MODIFIÉ]`

| Axe | États | Source d'autorité | Règle moteur en absence |
| :-- | :-- | :-- | :-- |
| 1 — Calibration | Bien calibré / Surestimateur / Sous-estimateur | Inférence déterministe | N/A (toujours calculable) |
| 2 — Régime d'activation | Productif / Détresse / Sous-défi | AR-N1 (autorité) + proxys (fond) | Conservatrice réversible |
| 3 — Valeur-Coût VC | VC-Élevée / VC-Neutre / VC-Basse | AR-N2 item VC uniquement | Inconnu — aucune inférence |

---

**Niveaux autonomie moteur** `[S17][INFÉRÉ]`

| Niveau | Jalons humains | KU applicables |
| :-- | :-- | :-- |
| Autonome | Aucun | Déclarative, Formelle, Perceptuelle, Procédurale P1 |
| Hybride recommandé | Suggérés, non bloquants | Procédurale P2 |
| Hybride bloquant | Bloquants (human_checkpoint) | Procédurale P3, Créative couche 3 |
| Assisté | Feedback délégué tuteur | Procédurale P4 |

---

**Hiérarchie GF-08 — Conflits entre principes** `[S14][INFÉRÉ]`

| Priorité | Principe dominant | Principe subordonné |
| :-- | :-- | :-- |
| 1 | Protection apprenant (P5, P8, P13) | Tout autre principe |
| 2 | Charge cognitive (P7) | Optimisation MSC court terme (P1) |
| 3 | Auto-rapport (P9) | Décisions adaptatives auto (P5) |
| 4 | Atomicité/intégrité modèle (P13, GF-01, P17) | Fluidité expérience (P8) |

---

**Déclencheurs patch — table complète** `[S14][INFÉRÉ]` `[MODIFIÉ]`

| Déclencheur | Origine | Cible patch |
| :-- | :-- | :-- |
| Écart performance > seuil | Moteur | Paramètres, sous-parcours |
| Biais cohorte systématique | Métriques équité | Révision modèle inférence |
| Révocation MSC > seuil | Moteur | Recalibration seuils, missions |
| Oscillation concept ≥ 3 cycles | Moteur | Missions conflit cognitif, graphe |
| Sessions SIS bas > seuil | Moteur | Vérification intégrité |
| Taux erreurs hors-taxonomie > seuil | Moteur | Enrichissement matrice feedback `[AJOUTÉ]` |
| VC Bas persistant ≥ N sessions | AR-N2 | Révision relevance / contexte `[AJOUTÉ]` |
| Profil AR-réfractaire détecté | AR-N1 | Révision mode sollicitation `[AJOUTÉ]` |

***
