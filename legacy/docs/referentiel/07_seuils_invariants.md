## Seuils / Bornes critiques [S5] `[MODIFIÉ §S5 v0.4 vs v0.5]`

Précision                     ≥ 80%
Robustesse                    ≥ 3 jours
Autonomie                     ≥ 3 réussites
Révocation                    ≥ 2 échecs
Interleaving                  ≥ 2 réussites
Fatigue cognitive             25 minutes
Adaptation critique           48 heures
Patch fréquence               1 / 14 jours
Multiplicateur R créatif      ×1 (fallback) `[MODIFIÉ]`
VC Bas persistant             ≥ 4 sessions (fourchette 3–7) `[AJOUTÉ]`
AR-réfractaire                ≥ 5 sessions sans AR-N1 (fourchette 3–8) `[AJOUTÉ]`
Couverture feedback prod.     ≥ 70% patterns couverts (fourchette 60%–90%) `[AJOUTÉ]`
Hors-taxonomie patch          > 15% erreurs / 10 sessions (fourchette 10%–25%) `[AJOUTÉ]`
Propagation graphe            1 saut max — invariant constitutionnel `[AJOUTÉ]`
Agrégation MSC                AND strict P∧R∧A — invariant constitutionnel `[AJOUTÉ]`

`[CRITIQUE]`

---

## Invariants structurels [S6]

### Atomicité des patchs

Principe :

application tout-ou-rien

Mécanisme :

double-buffer
snapshot
swap

Durée conservation :

30 jours

Fourchette :

7 à 90 jours

`[CRITIQUE]`

---

### Vérification locale obligatoire `[MODIFIÉ §S6 v0.4 vs v0.5]`

Condition (étendue v0.5) :

tous paramètres ∈ bornes
ET impact_scope calculable `[AJOUTÉ]`
ET liste contrôle qualité pédagogique satisfaite (P12 Constitution) `[AJOUTÉ]`

Sinon :

rejet total

`[CRITIQUE]` `[IMPACT-CRITIQUE]`

---

## Résumé structurel (niveau système) `[INCHANGÉ]`

Le référentiel définit :

un système adaptatif paramétré
avec invariants constitutionnels
et paramètres ajustables bornés

Architecture implicite :

Constitution
↓
Référentiel
↓
Moteur adaptatif
↓
Apprenant

`[INFÉRÉ]`
