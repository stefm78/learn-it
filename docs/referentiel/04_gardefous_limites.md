## Garde-fous / Limites [S4]

### Fatigue cognitive

Seuil :

25 minutes

Fourchette :

15 à 40 minutes

Rôle :

garde-fou de dernier recours

---

### Test de non-nuisance gamification

Condition :

au moins 1 indicateur validé

Sinon :

période probatoire maintenue

`[CRITIQUE]`

---

### Évitement métacognitif

Détection :

temps réflexion < 30% médiane
ET
erreur stable
sur 3 sessions

Conséquence :

retour guidage

---

### Intégrité du modèle

Signal d'alerte :

> 15% sessions avec SIS < 0.4

Conséquence :

investigation systémique

`[CRITIQUE]`

---

### Couverture matrice feedback `[AJOUTÉ]` `[CRITIQUE]`

Définition :

proportion de patterns d'erreurs typiques couverts par au moins 1 template feedback indexé,
calculée par univers (KU formelles + procédurales uniquement).

Seuil minimal de référence :

≥ 70% patterns couverts à la mise en production

Fourchette :

60% ≤ seuil ≤ 90%

Seuil déclencheur patch :

taux `erreur-hors-taxonomie` > 15% des erreurs enregistrées sur 10 sessions consécutives
→ candidat prioritaire patch enrichissement matrice

Fourchette seuil patch :

10% ≤ seuil ≤ 25%

Signal de révision :

taux hors-taxonomie stable > seuil_patch sur 3 patchs consécutifs
→ revoir taxonomie d'erreurs en phase Design (pas seulement patch)

Justification :

P2 Constitution v1.6 — moteur sélectionne parmi templates ; erreur non couverte = dégradation silencieuse qualité feedback.
