## Mécanismes [S3]

### 1 — Calibrage initial

Longueur maximale :

≤ 10 unités diagnostiques

Fourchette :

5 ≤ unités ≤ 15

Objectif :

Initialiser le graphe rapidement

---

### Format de calibrage par type de KU

| Type KU | Format | Durée |
|---------|--------|-------|
| Déclarative | rappel / QCM | 10–30 s |
| Formelle | raisonnement court | 30–90 s |
| Procédurale | exécution | 1–5 min |
| Perceptuelle | classification | 10–20 s |
| Créative | production contrainte | 5–15 min |

`[CRITIQUE]`

---

### 2 — Interleaving

Condition d'activation :

≥ 2 réussites consécutives
ET ≥ 3 tâches distinctes

`[CRITIQUE]`

---

### Rééquilibration de couverture

Rééquilibrer si :

temps depuis présentation ≥ 2 × délai moyen

---

### Diagnostic de reprise

3 à 5 tâches

---

### 3 — Multiplicateurs temporels par type de KU `[MODIFIÉ §S3 v0.4 vs v0.5]`

| Type | Multiplicateur | Note |
|------|---------------|------|
| Déclarative | ×1 | référence |
| Formelle | ×1 | référence |
| Procédurale | ×2 à ×3 | rétention lente |
| Perceptuelle | ×0.5 | oubli précoce |
| Créative | **×1 (fallback)** `[MODIFIÉ]` | absence de calibration empirique disponible — pas d'exemption espacement. Révisable par données terrain. |

> **Règle** : « non applicable » supprimé — l'espacement s'applique à toutes les KU. Valeur fallback ×1 jusqu'à calibration cohorte créative (signal de révision : N ≥ 30 apprenants avec KU créative complétée).

`[CRITIQUE]` `[IMPACT-CRITIQUE]`

---

### 4 — Inertie minimale des adaptations critiques

Définition :

adaptation à fort impact =
changement structurel du parcours

Délai minimal :

48 heures

Exception :

12 heures si auto-rapport concordant

`[CRITIQUE]`

---

### 5 — Régimes adaptatifs

Version cible :

9 états

Structure :

3 régimes × 3 calibrations

Activation progressive :

3 → 5 → 9 états

---

### Détection du régime

Condition :

≥ 2 proxys franchissent leur seuil

Sinon :

réponse conservatrice

`[CRITIQUE]`

---

### Hiérarchie de confiance des signaux

Ordre :

1 — auto-rapport événementiel (AR-N1)
2 — auto-rapport session (AR-N2)
3 — proxys comportementaux
4 — tendances long terme

`[CRITIQUE]`

---

### 6 — Fréquence AR-N2 et items additionnels `[AJOUTÉ]`

Fréquence AR-N2 de référence :

1 sondage / session

Fourchette :

1 sondage / 1 session ≤ fréq ≤ 1 sondage / 3 sessions

Adaptation : réduire fréquence si taux complétion AR-N2 < 60% sur 5 sessions consécutives.

Items AR-N2 obligatoires (≤ 3 au total) :

- difficulté perçue (CVT contrôle)
- progrès perçu (CVT valeur)
- intention retour

Item AR-N2 optionnel — Valeur-Coût (VC) :

Activé si axe VC déclaré en phase Analyse (P18).
Position : dernier item du sondage AR-N2.
Format : binaire ou ternaire visuel (≤ 5 s).
Jamais ajouté si AR-N2 déjà à 3 items sans retrait d'un autre — auquel cas remplace « intention retour » si VC est axe prioritaire déclaré.

`[CRITIQUE]`

---

### 7 — Intention de session `[AJOUTÉ]`

Fréquence de référence :

1 proposition / 3 sessions inter-sessions

Fourchette :

1 / 1 session ≤ fréq ≤ 1 / 7 sessions

Format :

≤ 1 item visuel, sélection parmi 3–4 options proposées par le moteur (options dérivées du graphe KU courant)
OU champ libre optionnel (≤ 20 mots) si niveau autonomie moteur ≥ Hybride recommandé.

Règle moteur :

Non bloquant. Non pénalisé si non renseigné. Non exposé comme métrique de performance.
Confrontation intention / réalisation : calculée en AR-N2 (item « progrès perçu » existant suffit — pas d'item supplémentaire requis).

Signal de révision :

Taux de complétion < 40% sur 10 sessions → réduire fréquence ou simplifier format.

`[CRITIQUE]`
