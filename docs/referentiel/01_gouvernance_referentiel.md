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
