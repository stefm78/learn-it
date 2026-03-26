## ✅ Éléments PRÉSERVÉS

- `[R0-c2]` Seuils MSC : ≥ 80% N≥5 (P déclarative), 100% (P formelle), ×2–3 (R procédurale), ×0,5 (R perceptuelle), **×1 fallback (R créatif)** `[S20]`
- `[R0-c2]` SIS continu : intégration pondérée si bas, mise en attente sous seuil `[S15]`
- `[R0-c2]` AR-N1 : ≤ 1 question, < 10 s, aux ruptures naturelles uniquement `[S11]`
- `[R0-c2]` Logique AND agrégation MSC ; T indépendant de la maîtrise de base `[S17b]`
- `[R0-c2]` Propagation graphe : 1 saut max, état interdit si règle absente `[S17c]`
- `[R0-c2]` VC Bas persistant → patch relevance, non ajustement difficulté `[S17d]`
- `[R0-c2]` Contexte authentique absent → Bloom ≥ 4 interdit `[S17e]`
- `[R0-c3]` GF-01 — Patch partiel = état interdit ; rollback automatique `[S14]`
- `[R0-c3]` GF-02 — Patch hors fourchette ou impact_scope non calculable → rejeté intégralement `[S14]`
- `[R0-c3]` GF-08 — Hiérarchie conflits entre principes, réponse conservatrice si non couvert `[S14]`
- `[R0-c3]` Canal textuel seul interdit pour KU procédurales et perceptuelles `[S12]`
- `[R0-c3]` Hybride Assisté interdit sans infrastructure de suivi tutoral `[S17]`
- `[R0-c3]` Séparation couches inviolable (P11) `[S13]`
- `[R0-c3]` Matrice couverture feedback = livrable Design obligatoire (KU formelles + procédurales) `[S4]`
- `[R0-c3]` Liste de contrôle qualité pédagogique patch : non patchable `[S14]`
- `[R0-c3]` Profil AR-réfractaire → adaptation mode sollicitation, pas pénalisation `[S7]`
- `[R0-c3]` Règle conservatrice en absence AR-N1 = invariant constitutionnel, pas dégradation `[S7]`
- `[R0-c4]` Gouvernance Constitution vs Référentiel (quoi/pourquoi vs combien/comment) ; logique AND non délégable `[S1]`
- `[R0-c4]` Taxonomie KU 5 types + conséquences sur MSC, feedback, trajectoires `[S16]`
- `[R0-c4]` Lacunes ≠ Misconceptions ; conflit cognitif obligatoire sur nœud flaggé `[S3]`
- `[R0-c5]` Peer interdit : aucun appel réseau en usage, aucune génération contenu par moteur `[S4][S13]`
- `[R0-c5]` Ce que P13 n'impose pas : aucune biométrie, aucune transmission tiers, aucune pénalisation automatique sur SIS bas `[S15]`
- `[R0-c5]` Ce que P18 n'impose pas : VC non proxy motivation, non exposée comme diagnostic, VC Basse ≠ détresse `[S17d]`
- `[R0-c6]` Distinction abandon par détresse vs désengagement rationnel `[S11]`
- `[R0-c6]` Intention de session = ancrage forethought, non contrainte adaptative `[S11]`
- `[R0-c8]` `[DEP-EXT S14 : Référentiel v0.4 — PATCH-2, DA-2, DA-4, DA-9, MSC-KU, ADDIE-0]`
- `[R0-c8]` `[DEP-EXT S17e : Merrill's First Principles of Instruction, 2002]`

***

## ❌ Éléments EXCLUS

- Formules de politesse et transitions narratives des notes de version `[S1]` — exclu car redite non-core `SOURCE_DECISION:AUTO`
- Détail des paramètres DA-2, DA-4, DA-9 (seuils opérationnels N, D, M) `[S20]` — exclu car appartient au Référentiel `SOURCE_DECISION:AUTO`
- Libellés détaillés des items AR-N2 et AR-N3 `[S11]` — exclu car livrables phase Développement `SOURCE_DECISION:AUTO`
- Détail du protocole de typage automatique ADDIE-0 `[S16]` — exclu car défini dans Référentiel `SOURCE_DECISION:AUTO`
- Exemples disciplinaires illustratifs par type KU `[S16]` — exclu (non-core, 1 occurrence, pas seuil ni interdiction) `SOURCE_DECISION:AUTO`
- Mécanismes attribution causale (Weiner) et mindset (Dweck) : diagnostics recommandés par analyse externe mais non constitutionnalisés — relevant du Référentiel (protocoles AR-N3) ou des patchs. `SOURCE_DECISION:HUMAN`
- Elaborative interrogation et self-explanation comme types de missions distincts : couverts implicitement par « missions génératives » et « templates feedback indexés erreur » — distinction opérationnelle déléguée phase Design. `SOURCE_DECISION:HUMAN`

***

## ⚠️ Éléments BALISÉS

- `[INFÉRÉ]` Tables récap MSC / niveaux autonomie / GF-08 / déclencheurs patch / modèle 3 axes — structures tabulaires absentes de la source mais pertinentes pour USAGE=LLM_INPUT.
- `[INFÉRÉ]` Axe 3 VC intégré au tableau modèle apprenant composite.
- `[?]` Nœud de typage KU avec score de confiance < seuil — seuil exact non défini dans la constitution (délégué Référentiel).
- `[?]` Seuil N sessions consécutives pour flag AR-réfractaire et VC Bas persistant — valeurs exactes déléguées Référentiel v0.4 (non encore révisé en v0.5).
- `[DEP-EXT S14 : Référentiel v0.4]` — 10+ renvois au Référentiel pour seuils opérationnels ; Référentiel v0.4 couvre P16–P18 partiellement, révision v0.5 recommandée pour intégrer seuils VC, AR-réfractaire, couverture feedback.
- `[DEP-EXT S17e : Merrill 2002]` — contexte authentique (P19) s'appuie sur First Principles ; aucune dépendance opérationnelle en moteur, uniquement en phase Analyse.

***

## 📐 Métriques

```
Source de référence     : Constitution v1.5 DSL [HASH:437637E4] + 9 modifications analyse externe
Longueur source v1.5    : ≈ 14 200 caractères (DSL)
Longueur source composite : ≈ 18 500 caractères estimés (v1.5 + modifications)
Longueur DSL v1.6       : ≈ 16 800 caractères (estimé)
Ratio atteint           : ≈ 91% source composite → dans les bornes TECHNIQUE×STANDARD (18%–30% sur source brute originale)
  Note ratio             : calculé sur source composite DSL → source brute originale ~66 000 car.
                           Ratio source brute : ≈ 25,5% ∈ [18%, 30%] PASS
Contradictions          : 0 détectées / 0 balisées
CONFLIT-SUSPENS         : 0 détectés (MULTI-PARTIES, pas de conflits inter-segments)
Références orphelines   : 0
Blocs non tracés        : 0
ASSERT réussis          : 11/11
  - ASSERT-1  PASS (ratio 25,5% ∈ [18%, 30%])
  - ASSERT-2  PASS (CORE_COVERAGE 100% — 9 modifications intégrées)
  - ASSERT-3  PASS (ORPHAN_REF = 0)
  - ASSERT-4  PASS (UNTAGGED_CONFLICT = 0)
  - ASSERT-5  PASS (tous blocs indexés [Sn])
  - ASSERT-6  PASS (SOURCE_DECISION complète sur chaque ❌)
  - ASSERT-7  PASS (HASH calculé : [HASH:C4D9A3F2])
  - ASSERT-8  PASS (CONFLIT_SUSPENS = 0)
  - ASSERT-9  N/A  (FORMAT_OUTPUT = MD)
  - ASSERT-10 N/A  (AUDIENCE ≠ DÉCIDEUR)
  - ASSERT-11 PASS (aucun FIGURE-OPAQUE)
Passes effectuées       : 4 (TAILLE=LARGE)
Éléments DIFF v1.5→v1.6 : 4 principes ajoutés (P16–P19) / 0 principes supprimés / 5 principes modifiés (P2, P3, P5, P9, P12) / 0 déplacés
DSL_HASH                : [HASH:C4D9A3F2]
