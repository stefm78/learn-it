**P16 — Règle d'agrégation MSC** `[S17b]` `[AJOUTÉ]` `[CRITIQUE]`

- La déclaration de maîtrise d'une KU requiert la satisfaction **simultanée** des composantes P, R et A au-dessus de leurs seuils respectifs — **logique AND**.
- La composante T (transférabilité) constitue une maîtrise de niveau supérieur, déclarée séparément et **jamais prérequise** pour la maîtrise de base.
- Cette règle d'agrégation est un **invariant constitutionnel non délégable au Référentiel** : le Référentiel ne définit que les valeurs de seuil, non la logique de combinaison.
- Toute modification de la logique AND (vers pondération, minimum, ou autre) constitue une **révision constitutionnelle** nécessitant délibération explicite.
- Conséquence sur révocation : la défaillance de **n'importe laquelle** des composantes P, R ou A (cf. seuils Référentiel) suffit à rétrograder l'état MSC.

---

**P17 — Propagation d'incertitude sur le graphe** `[S17c]` `[AJOUTÉ]` `[CRITIQUE]`

- Toute rétrogradation MSC d'une KU (passage `maîtrisé → en consolidation` ou `en consolidation → lacune`) déclenche automatiquement un **marquage de vérification prioritaire** sur l'ensemble des KU dépendantes (arêtes sortantes directes du graphe).
- Les KU marquées ne sont pas rétrogradées automatiquement, mais leur prochaine occurrence de consolidation est planifiée avec **priorité maximale** et intègre une tâche diagnostique courte (format calibrage par type KU, Référentiel).
- La propagation couvre **au maximum 1 saut de dépendance** (pas de cascade illimitée au-delà des arcs directs).
- **État interdit** : absence de cette règle dans le moteur pour un graphe comportant des arêtes de dépendance. Équivalent GF-01 pour l'intégrité du graphe.
- Condition de mise en œuvre : les arêtes de dépendance doivent être déclarées en phase Analyse (P2 / ADDIE-0) — graphe sans arêtes déclarées → état Hybride bloquant minimum requis (P15).

---

**P18 — Valeur-Coût perçue** `[S17d]` `[AJOUTÉ]`

- Axe optionnel du modèle d'état apprenant (P5, Axe 3). Inféré uniquement par item AR-N2 — **aucun proxy comportemental autonome autorisé** pour cet axe.
- **États VC** : VC-Élevée (utilité perçue > coût perçu), VC-Neutre, VC-Basse (coût perçu > utilité perçue).
- VC Bas persistant sur N sessions consécutives (seuil Référentiel) = déclencheur de patch *relevance* : révision de la présentation des enjeux, des missions de contextualisation, du lien explicite avec le contexte authentique (P19) — **non** d'ajustement de difficulté.
- **Ce que P18 n'impose pas** : VC non utilisée comme proxy de motivation générale, non exposée à l'apprenant comme diagnostic, non corrélée mécaniquement au régime d'activation (Axe 2). VC Basse ≠ détresse ≠ désengagement rationnel — réponse adaptative distincte.
- Si l'item AR-N2 VC n'est pas obtenu (apprenant non-répondant) : axe VC considéré inconnu, aucune inférence autorisée.

---

**P19 — Contexte authentique** `[S17e]` `[AJOUTÉ]` `[CRITIQUE]`

- Toute application Learn-it déclare en phase Analyse un **contexte authentique de référence** : la situation-problème réelle dans laquelle les KU maîtrisées sont mobilisées (examen, situation professionnelle, projet concret).
- Ce contexte est le cadre narratif implicite du graphe de KU. Il conditionne la formulation des tâches de transfert (composante T du MSC) et des missions de feuille blanche (P6).
- **Absence de contexte authentique déclaré** → missions de niveau Bloom ≥ 4 (application, analyse, évaluation, création) **interdites**. Les KU concernées restent plafonnées au niveau compréhension (Bloom 2) jusqu'à déclaration explicite du contexte. `[CRITIQUE]`
- Le contexte authentique est un livrable obligatoire de la phase Analyse (ADDIE). Il est révisable par patch si le contexte cible de l'apprenant évolue, dans le périmètre autorisé P12.
- Conformité Merrill (5e principe — Problem-Centered) : le contexte authentique est l'ancrage de tous les niveaux Bloom supérieurs. `[DEP-EXT S17e : Merrill's First Principles of Instruction, 2002]`

***
