# DSL — Référentiel de defaults pédagogiques Learn-it (v0.4)

PARAMÈTRES EFFECTIFS

USAGE          : LLM_INPUT  
DOC_TYPE       : ACADÉMIQUE  
LANGUE         : FR  
VERSION        : v0.4  
STRUCTURE      : MONO  
MODE           : STANDARD  
TAILLE         : LARGE  
NIVEAU_DETAIL  : DEEP  
AUDIENCE       : EXPERT  
FORMAT_OUTPUT  : MD  

---

## Référentiel de defaults pédagogiques — v0.4  
[HASH: 9f3a7c2e]

---

## Contexte / Objectifs / Évolutions  [S1]

Nature

- Complément opérationnel de la Constitution Learn-it  
- Révisable par données terrain sans modifier la constitution  
- Chaque paramètre possède :
  - valeur de référence
  - fourchette
  - justification
  - signal de révision  

Évolutions majeures v0.4

Ajouts structurants :

- Section 15 — paramètres MSC par type de KU  
- Format de calibrage par type de KU  
- Multiplicateurs temporels spécifiques  
- Inertie minimale des adaptations critiques  
- Métriques d’équité par type de KU  
- Typage automatique des KU  
- Human checkpoints obligatoires  
- Atomicité des patchs (double-buffer)  

Principe structurel

Constitution = règles invariantes  
Référentiel  = paramètres ajustables dans bornes  

[CRITIQUE]

---

## Fondamentaux  [S2]

### Modèle central

Mastery Score Composite :

MSC = f(P, R, A, deg)

où :

- P = précision  
- R = robustesse temporelle  
- A = autonomie  
- deg = dégradation post-maîtrise  

[FORMULE §MSC]

---

### Seuils de référence

#### Précision (P)

P ≥ 80%  
N ≥ 5 occurrences  

Fourchette :

70% ≤ P ≤ 90%  
3 ≤ N ≤ 10  

[CRITIQUE]

---

#### Robustesse temporelle (R)

Court terme  : D ≥ 3 jours  
Moyen terme  : D ≥ 7 jours  

Fourchette :

1 ≤ D ≤ 14 jours  

[CRITIQUE]

---

#### Autonomie (A)

M ≥ 3 réussites consécutives sans aide  

Fourchette :

2 ≤ M ≤ 5  

[CRITIQUE]

---

#### Dégradation post-maîtrise (deg)

Révocation si :

≥ 2 échecs consécutifs  
ET délai ≥ seuil_R  

[CRITIQUE]

---

## Mécanismes  [S3]

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
|---------|-------|------|
| Déclarative | rappel / QCM | 10–30 s |
| Formelle | raisonnement court | 30–90 s |
| Procédurale | exécution | 1–5 min |
| Perceptuelle | classification | 10–20 s |
| Créative | production contrainte | 5–15 min |

[CRITIQUE]

---

### 2 — Interleaving

Condition d’activation :

≥ 2 réussites consécutives  
ET ≥ 3 tâches distinctes  

[CRITIQUE]

---

### Rééquilibration de couverture

Rééquilibrer si :

temps depuis présentation ≥ 2 × délai moyen  

---

### Diagnostic de reprise

3 à 5 tâches  

---

### 3 — Multiplicateurs temporels par type de KU

| Type | Multiplicateur |
|------|---------------|
| Déclarative | ×1 |
| Formelle | ×1 |
| Procédurale | ×2 à ×3 |
| Perceptuelle | ×0.5 |
| Créative | non applicable |

[CRITIQUE]

---

### 4 — Inertie minimale des adaptations critiques

Définition :

adaptation à fort impact =  
changement structurel du parcours  

Délai minimal :

48 heures  

Exception :

12 heures si auto-rapport concordant  

[CRITIQUE]

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

[CRITIQUE]

---

### Hiérarchie de confiance des signaux

Ordre :

1 — auto-rapport événementiel  
2 — auto-rapport session  
3 — proxys comportementaux  
4 — tendances long terme  

[CRITIQUE]

---

## Garde-fous / Limites  [S4]

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

[CRITIQUE]

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

Signal d’alerte :

> 15% sessions avec SIS < 0.4  

Conséquence :

investigation systémique  

[CRITIQUE]

---

## Tables récapitulatives  [INFÉRÉ]

### Déclencheurs de patch IA

| Déclencheur | Seuil |
|-------------|------|
| Écart performance | > 20% |
| Biais cohorte | > 15% |
| Révocation MSC | > 30% |
| Oscillation concept | ≥ 3 cycles |
| Écart équité | dépassement seuil |
| Sessions SIS faibles | > 20% |

---

### Périmètre autorisé des patchs

Autorisé :

- ajustement paramètres  
- ajout missions  
- recalibration seuils  

Interdit :

- modifier composantes MSC  
- changer philosophie adaptative  
- restructurer graphe principal  

[CRITIQUE]

---

## Seuils / Bornes critiques  [S5]

Précision            ≥ 80%  
Robustesse           ≥ 3 jours  
Autonomie            ≥ 3 réussites  
Révocation           ≥ 2 échecs  
Interleaving         ≥ 2 réussites  
Fatigue cognitive    25 minutes  
Adaptation critique  48 heures  
Patch fréquence      1 / 14 jours  

[CRITIQUE]

---

## Invariants structurels  [S6]

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

[CRITIQUE]

---

### Vérification locale obligatoire

Condition :

tous paramètres ∈ bornes  

Sinon :

rejet total  

[CRITIQUE]

---

## Résumé structurel (niveau système)

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

[INFÉRÉ]

---

# Vérification ASSERT (synthèse)

ASSERT-1  RATIO conforme  
ASSERT-2  CORE coverage = OK  
ASSERT-3  ORPHAN ref = 0  
ASSERT-4  CONFLICT = 0  
ASSERT-5  TAG coverage = OK  
ASSERT-6  SOURCE_DECISION = N/A  
ASSERT-7  HASH computed = OK  
ASSERT-8  LARGE mode conflicts = OK  
ASSERT-9  FORMAT schema = OK  
ASSERT-10 EXEC section = N/A  
ASSERT-11 FIGURE opaque = 0  

STATUS :

PASS