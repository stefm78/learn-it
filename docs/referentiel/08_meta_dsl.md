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