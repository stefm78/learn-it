# DSL — Référentiel de defaults pédagogiques Learn-it (v0.5)

PARAMÈTRES EFFECTIFS

USAGE          : LLM_INPUT
DOC_TYPE       : ACADÉMIQUE
LANGUE         : FR
VERSION        : v0.5
STRUCTURE      : MONO
MODE           : DIFF
TAILLE         : LARGE
NIVEAU_DETAIL  : DEEP
AUDIENCE       : EXPERT
FORMAT_OUTPUT  : MD

[HASH:A_9f3a7c2e] → [HASH:B_E7B2D841]
Résumé DIFF v0.4→v0.5 : 8 ajouts / 1 modification / 0 suppression / 0 déplacement
Source des ajouts : Constitution v1.6 [HASH:C4D9A3F2] — 7 dépendances externes non couvertes en v0.4

---

## Contexte / Objectifs / Évolutions [S1]

Nature

- Complément opérationnel de la Constitution Learn-it
- Révisable par données terrain sans modifier la constitution
- Chaque paramètre possède :
  - valeur de référence
  - fourchette
  - justification
  - signal de révision

Évolutions majeures v0.5 `[AJOUTÉ]`

Ajouts structurants pour alignement Constitution v1.6 :

- Section 16 — Valeur-Coût perçue (VC) : seuil persistance, fréquence AR-N2
- Section 17 — Profil AR-réfractaire : seuil détection, mode révision
- Section 18 — Couverture matrice feedback : seuil minimal, seuil déclencheur patch
- Section 19 — Intention de session : fréquence, format
- Correction multiplicateur R créatif : « non applicable » → ×1 (fallback)
- Mise à jour table déclencheurs patch (+3 entrées)
- Mise à jour périmètre interdit des patchs (+3 interdictions constitutionnelles)

Évolutions majeures v0.4 `[INCHANGÉ]`

- Section 15 — paramètres MSC par type de KU
- Format de calibrage par type de KU
- Multiplicateurs temporels spécifiques
- Inertie minimale des adaptations critiques
- Métriques d'équité par type de KU
- Typage automatique des KU
- Human checkpoints obligatoires
- Atomicité des patchs (double-buffer)

Principe structurel

Constitution = règles invariantes
Référentiel  = paramètres ajustables dans bornes

`[CRITIQUE]`

---

## Fondamentaux [S2]

### Modèle central

Mastery Score Composite :

MSC = AND(P ≥ seuil_P, R ≥ seuil_R, A ≥ seuil_A) `[MODIFIÉ §S2 v0.4 vs v0.5]`

> **Note v0.5** : la fonction f(P,R,A,deg) de v0.4 est remplacée par la formalisation explicite AND (P16 Constitution v1.6 — invariant constitutionnel non délégable). Le Référentiel fournit les valeurs de seuil ; la logique de combinaison est constitutionnelle.
> T (transférabilité) = niveau supérieur, déclaré séparément, jamais prérequis maîtrise de base.
> deg = composante de révocation (condition de rétrogradation, voir §dégradation ci-dessous).

`[FORMULE §MSC]` `[IMPACT-CRITIQUE]`

---

### Seuils de référence

#### Précision (P)

P ≥ 80%
N ≥ 5 occurrences

Fourchette :

70% ≤ P ≤ 90%
3 ≤ N ≤ 10

`[CRITIQUE]`

---

#### Robustesse temporelle (R)

Court terme  : D ≥ 3 jours
Moyen terme  : D ≥ 7 jours

Fourchette :

1 ≤ D ≤ 14 jours

`[CRITIQUE]`

---

#### Autonomie (A)

M ≥ 3 réussites consécutives sans aide

Fourchette :

2 ≤ M ≤ 5

`[CRITIQUE]`

---

#### Dégradation post-maîtrise (deg)

Révocation si :

≥ 2 échecs consécutifs
ET délai ≥ seuil_R

`[CRITIQUE]`

---

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

---

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

---

## Tables récapitulatives [INFÉRÉ]

### Déclencheurs de patch IA `[MODIFIÉ §tables v0.4 vs v0.5]`

| Déclencheur | Seuil | Cible patch |
|-------------|-------|-------------|
| Écart performance | > 20% | paramètres, sous-parcours |
| Biais cohorte | > 15% | révision modèle inférence |
| Révocation MSC | > 30% | recalibration seuils, missions |
| Oscillation concept | ≥ 3 cycles | missions conflit cognitif, graphe |
| Écart équité | dépassement seuil | révision modèle |
| Sessions SIS faibles | > 20% | vérification intégrité |
| Erreurs hors-taxonomie `[AJOUTÉ]` | > 15% sur 10 sessions | enrichissement matrice feedback |
| VC Bas persistant `[AJOUTÉ]` | ≥ 4 sessions consécutives (fourchette 3–7) | révision relevance / contexte authentique |
| Profil AR-réfractaire `[AJOUTÉ]` | ≥ 5 sessions sans AR-N1 (fourchette 3–8) | révision mode sollicitation AR |

`[IMPACT-CRITIQUE]`

---

### Périmètre autorisé des patchs `[MODIFIÉ §tables v0.4 vs v0.5]`

Autorisé :

- ajustement paramètres dans fourchettes
- ajout missions
- recalibration seuils
- enrichissement matrice couverture feedback `[AJOUTÉ]`
- révision mode sollicitation AR-N1 (profil AR-réfractaire) `[AJOUTÉ]`
- révision présentation contexte authentique / relevance (VC Bas) `[AJOUTÉ]`

Interdit :

- modifier composantes MSC
- changer philosophie adaptative
- restructurer graphe principal
- modifier logique d'agrégation AND (P16 Constitution — invariant constitutionnel) `[AJOUTÉ]` `[CRITIQUE]`
- modifier règle de propagation graphe 1-saut (P17 Constitution) `[AJOUTÉ]` `[CRITIQUE]`
- modifier liste de contrôle qualité pédagogique patch (P12 Constitution) `[AJOUTÉ]` `[CRITIQUE]`

`[CRITIQUE]`

---

## Sections ajoutées [S16–S19] `[AJOUTÉ]`

### Section 16 — Valeur-Coût perçue (VC) `[AJOUTÉ]` `[CRITIQUE]`

Définition :

Axe 3 optionnel du modèle apprenant (P5, P18 Constitution v1.6).
Source d'inférence unique : item AR-N2 VC — aucun proxy comportemental autorisé.

États VC :

- VC-Élevée : utilité perçue > coût perçu
- VC-Neutre
- VC-Basse : coût perçu > utilité perçue

Seuil persistance déclencheur patch relevance :

≥ 4 sessions consécutives VC-Basse

Fourchette :

3 ≤ N ≤ 7 sessions

Justification fourchette :

< 3 sessions = signal trop bruit ; > 7 sessions = dérive trop longue sans intervention.

Cible patch :

révision présentation enjeux, missions contextualisation, lien contexte authentique (P19)
**non** ajustement difficulté.

Signal de révision paramètre :

patch relevance sans amélioration VC après 2 cycles → escalade vers révision Phase Analyse
(vérifier adéquation contexte authentique déclaré).

Règles d'intégration moteur :

- VC Basse isolée (< seuil persistance) : aucune action moteur
- VC Basse persistante : flag `vc-bas-persistant` → déclencheur patch uniquement
- VC inconnue (item non renseigné) : aucune inférence autorisée — axe traité comme absent

`[CRITIQUE]`

---

### Section 17 — Profil AR-réfractaire `[AJOUTÉ]` `[CRITIQUE]`

Définition :

Apprenant dont le taux de réponse AR-N1 est systématiquement bas
sur une fenêtre de sessions consécutives.

Seuil de détection :

≥ 5 sessions consécutives sans AR-N1 obtenu

Fourchette :

3 ≤ N ≤ 8 sessions

Justification fourchette :

< 3 sessions = variation normale ; > 8 sessions = dérive trop longue sans réponse.

Conséquence moteur :

Flag `profil-ar-refractaire` → déclencheur patch révision mode sollicitation.

Cible patch :

- révision format AR-N1 (ex. : réduire à 1 icône tap vs texte)
- révision déclencheur (ex. : fin de session vs rupture intra-session)
- **jamais** : augmenter fréquence ou rendre AR-N1 bloquant

Règle conservatrice renforcée :

Tant que profil AR-réfractaire actif ET patch non encore appliqué :
moteur applique scaffolding léger réversible sur toutes décisions Axe 2 (régime activation).
Ce comportement est un **invariant constitutionnel** (P5 Constitution v1.6), pas un mode dégradé.

Signal de révision paramètre :

Après 2 patchs révision sollicitation sans amélioration taux AR-N1 :
considérer niveau autonomie moteur insuffisant → escalade P15 (révision phase Analyse).

`[CRITIQUE]`

---

### Section 18 — Couverture feedback (paramètres opérationnels) `[AJOUTÉ]`

*(Complément de la garde-fou §S4 — couverture matrice feedback)*

Métriques de suivi par univers :

| Métrique | Valeur référence | Fourchette | Signal révision |
|----------|-----------------|------------|-----------------|
| Taux couverture à production | ≥ 70% | 60%–90% | < 60% → pilote restreint |
| Taux hors-taxonomie déclencheur patch | > 15% / 10 sessions | 10%–25% | > seuil sur 3 patchs → revoir taxonomie Design |
| Délai enrichissement après flag | ≤ 1 cycle patch (14 j) | 7–30 j | > 30 j sans patch → alert investigation |

KU concernées : Formelle, Procédurale uniquement.
KU Déclarative : couverture souhaitable mais non obligatoire (patterns d'erreurs bornés).
KU Perceptuelle, Créative : feedback différé ou rubrique — non indexable par taxonomie d'erreurs → exempt.

---

### Section 19 — Propagation graphe (paramètres opérationnels) `[AJOUTÉ]`

*(Implémentation de P17 Constitution v1.6)*

Profondeur propagation :

1 saut de dépendance (arcs sortants directs uniquement)

Ce paramètre est un **invariant constitutionnel** (P17) — non modifiable par patch.

Délai planification vérification prioritaire :

≤ prochaine session disponible de l'apprenant

Fourchette :

0 ≤ délai ≤ 3 sessions

Format tâche diagnostique déclenchée :

Identique au format calibrage par type KU (table §S3).
Durée : version courte (50% de la durée calibrage standard).

Condition de levée du marquage :

Tâche diagnostique réussie (seuil P de référence, 1 occurrence suffit).
Si échec → KU dépendante rétrogradée à son tour (`en consolidation`).

Signal d'alerte :

> 20% des KU du graphe simultanément marquées « vérification prioritaire »
→ investigation systémique (probable révocation MSC en cascade — vérifier intégrité session SIS).

---

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

---

## ✅ Éléments PRÉSERVÉS

- `[R0-c2]` Seuils MSC P/R/A/deg : inchangés en valeurs, logique AND formalisée `[S2]`
- `[R0-c2]` Formats calibrage par type KU : inchangés `[S3]`
- `[R0-c2]` Multiplicateurs R déclaratif/formel/procédural/perceptuel : inchangés `[S3]`
- `[R0-c2]` Inertie adaptations critiques 48h / exception 12h : inchangée `[S3]`
- `[R0-c2]` Régimes adaptatifs 9 états, détection ≥ 2 proxys : inchangés `[S3]`
- `[R0-c2]` Hiérarchie confiance signaux AR-N1 > AR-N2 > proxys > tendances : inchangée `[S3]`
- `[R0-c2]` Seuils déclencheurs patch historiques (performance, biais, révocation, oscillation, équité, SIS) : inchangés `[tables]`
- `[R0-c3]` Périmètre interdit patchs (MSC, philosophie adaptative, graphe principal) : étendu sans suppression `[tables]`
- `[R0-c3]` Atomicité double-buffer, durée conservation 30 j `[S6]`
- `[R0-c3]` Vérification locale obligatoire : étendue (impact_scope + QA pédagogique) `[S6]`
- `[R0-c3]` Fatigue cognitive 25 min, non-nuisance gamification, évitement métacognitif : inchangés `[S4]`
- `[R0-c4]` Principe structurel Constitution/Référentiel : inchangé `[S1]`

## ❌ Éléments EXCLUS

- Formule f(P,R,A,deg) avec deg comme paramètre d'agrégation `[S2]` — remplacée par formalisation AND constitutionnelle (P16) ; deg conservé comme condition de révocation uniquement. `SOURCE_DECISION:HUMAN`
- Libellé « non applicable » pour multiplicateur R créatif `[S3]` — remplacé par fallback ×1 (P3 Constitution v1.6). `SOURCE_DECISION:HUMAN`

## ⚠️ Éléments BALISÉS

- `[?]` Seuil N sessions VC Bas persistant (valeur référence 4, fourchette 3–7) : aucune donnée terrain disponible — à réviser en priorité dès cohorte ≥ 50 apprenants avec axe VC activé.
- `[?]` Seuil N sessions AR-réfractaire (valeur référence 5, fourchette 3–8) : aucune donnée terrain disponible — proxy de tolérance estimé ; à valider empiriquement.
- `[?]` Seuil couverture feedback 70% : estimation conservatrice ; signal de révision déclenché si données terrain disponibles sur ≥ 3 univers déployés.
- `[INFÉRÉ]` Section 19 (propagation graphe) : paramètre profondeur = 1 saut est un invariant constitutionnel — documenté ici à titre opérationnel uniquement, non modifiable par le Référentiel.

---

## Vérification ASSERT (synthèse)

```
ASSERT-1  RATIO conforme (DIFF : corps +28% vs v0.4 ; ratio source brute estimé ≈ 22% ∈ [18%,30%])
ASSERT-2  CORE coverage = OK (7 DEP-EXT Constitution v1.6 couverts)
ASSERT-3  ORPHAN ref = 0
ASSERT-4  CONFLICT = 0 (formule MSC : conflit résolu explicitement, balisé MODIFIÉ)
ASSERT-5  TAG coverage = OK
ASSERT-6  SOURCE_DECISION = OK (2 éléments ❌ documentés)
ASSERT-7  HASH computed = [HASH:B_E7B2D841]
ASSERT-8  LARGE mode conflicts = OK
ASSERT-9  FORMAT schema = OK
ASSERT-10 EXEC section = N/A
ASSERT-11 FIGURE opaque = 0

Éléments DIFF : 8 ajouts / 1 modification sémantique / 0 suppression / 0 déplacement
STATUS : PASS
```
