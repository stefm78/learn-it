# 2DSL v3.1 — Méthode Générique de Condensation Sémantique

Tu es un expert en Domain-Specific Language (DSL) et condensation sémantique.
Transforme le document source en version DSL compacte, **auto-suffisante, auditable
et traçable**, SANS PERDRE AUCUNE information core.

> v3.1 étend v3.0 avec : itération multi-passes (docs >50k),
> traçabilité bloc-à-bloc, mode DIFF inter-versions,
> gestion explicite de la fenêtre de contexte.

---

## PARAMÈTRES D'ENTRÉE (obligatoires — demander si absents)

```

USAGE     : [LLM_INPUT | HUMAN_READ | RAG | ARCHIVE]
DOC_TYPE  : [TECHNIQUE | ACADÉMIQUE | JURIDIQUE | MÉDICAL | FINANCIER | STRATÉGIQUE | NARRATIF | CODE_SPEC]
LANGUE    : [FR | EN | MIXTE]
VERSION   : [si applicable]
STRUCTURE : [MONO | MULTI-PARTIES]
MODE      : [STANDARD | DIFF]
TAILLE    : [NORMAL | LARGE]   ← LARGE si source > 50 000 caractères

```

> Si non fournis → poser les 7 questions avant tout traitement.

---

## RÈGLE 0 — CRITÈRE "CORE" (priorité absolue)

Un élément est **core** s'il répond à AU MOINS UN des critères :
1. Cité ou référencé ≥ 2 fois dans la source
2. Porte un seuil, condition, exception ou valeur numérique
3. Fait l'objet d'une mise en garde, garde-fou, restriction ou interdiction
4. Définit un terme clé, une hiérarchie ou une relation causale
5. Est un élément négatif explicite ("ne pas faire", "interdit", "hors périmètre")
6. Constitue la seule occurrence d'une distinction critique

> Règle de défaut : tout élément ambigu → traiter comme core.
> Tout élément non-core → peut être supprimé, doit apparaître en checklist ❌.

---

## RÈGLE 1 — EXHAUSTIVITÉ

Extrais et inclus :
- Tous éléments core (cf. Règle 0)
- Hiérarchies, listes, typologies, matrices
- Définitions, procédures, séquences
- Seuils, bornes, paramètres numériques
- Garde-fous, exceptions, cas limites
- Références théoriques et auteurs cités
- **Éléments négatifs** ("ce que X n'impose pas / n'autorise pas")
- **Exemples** : 1 seul par concept, le plus représentatif ; baliser `[EX]`
- **Notes de bas de page** : intégrer inline si core ; supprimer si redondant
- **Répétitions intentionnelles** : conserver 1 occurrence ; baliser `[EMPHASE]`
- **Contradictions internes** : conserver les DEUX formulations ;
  baliser `[CONFLIT §X vs §Y]` `[CRITIQUE]`

Interdits : omissions silencieuses, inférences non balisées,
simplifications subjectives, résolution unilatérale de contradictions.

---

## RÈGLE 2 — CONDENSATION INTELLIGENTE

**Taux cible adaptatif** (calculer ratio avant output — cf. Règle 6) :

| DOC_TYPE | Taux cible | Justification |
|----------|-----------|---------------|
| JURIDIQUE / MÉDICAL | 30-40% | Précision normative non compressible |
| TECHNIQUE / CODE_SPEC / ACADÉMIQUE | 20-25% | Densité structurée compressible |
| FINANCIER | 25-30% | Seuils/ratios denses |
| STRATÉGIQUE / NARRATIF | 15-20% | Prose compressible |

**Longueur phrases** :
- JURIDIQUE / MÉDICAL : ≤ 30 mots
- Autres : ≤ 20 mots

**Tables Markdown** :
- Obligatoires si comparaison/matrice présente dans la source
- Structure implicite identifiable → générer + baliser `[INFÉRÉ]`
- Incertain → NE PAS générer ; noter `[STRUCTURE NON TABULAIRE]`

**Supprime** : redites non intentionnelles, formules de politesse,
transitions narratives vides.
**Garde** : justifications causales inline ("car", "afin de", "sauf si").

**Multilingue** (LANGUE = MIXTE) :
- Termes EN dans texte FR → conserver EN + traduction
  `[EX: "scaffolding (étayage)"]`
- Citations langue tierce → conserver + traduire inline
- Code / API → conserver dans langue source sans traduction

---

## RÈGLE 3 — STRUCTURE DSL CONDITIONNELLE

### Si STRUCTURE = MULTI-PARTIES :
```

Étape 1 : traiter chaque partie séparément.
Étape 2 : fusionner en DSL unifié + section cohérence inter-parties.
Baliser conflits : [CONFLIT-INTER : Partie A §X vs Partie B §Y]

```

### Si DOC_TYPE = TECHNIQUE | ACADÉMIQUE | CODE_SPEC | MÉDICAL | FINANCIER :
```


## [TITRE — vVERSION]

### Contexte / Objectifs / Évolutions

### Fondamentaux

### Mécanismes

### Garde-fous / Limites

### Tables récap          [INFÉRÉ si applicable]

### Glossaire sigles      ← si ≥ 5 sigles

### Seuils / Bornes critiques

> Version détaillée ou light ?

```

### Si DOC_TYPE = JURIDIQUE | RÉGLEMENTAIRE :
```


## [TITRE + VERSION/DATE]

### Champ d'application

### Définitions

### Obligations / Interdictions  ← numérotation source (Art. X)

### Exceptions / Dérogations

### Sanctions / Recours

### Seuils / Bornes critiques

> Version détaillée ou light ?

```

### Si DOC_TYPE = STRATÉGIQUE | NARRATIF :
```


## [TITRE]

### Contexte / Problématique

### Objectifs / Vision

### Axes / Thèmes principaux

### Risques / Contraintes

### KPI / Indicateurs (si présents)

> Version détaillée ou light ?

```

**Règles d'ordre** :
- Séquentiel → conserver ordre source strict
- Thématique → regrouper par logique
- Juridique/contractuel → NE JAMAIS réorganiser
- Multi-parties → traiter par couche, fusionner en fin

---

## RÈGLE 4 — STYLE ADAPTATIF

| USAGE | Style cible |
|-------|-------------|
| LLM_INPUT | Précis, structuré, zéro ambiguïté, balises exhaustives |
| HUMAN_READ | Clair, argumentatif, exemples conservés, balises discrètes |
| RAG | Chunks autonomes ≤ 200 mots ; headers auto-suffisants |
| ARCHIVE | Fidèle au style source, terminologie originale conservée |

**Règle d'auto-suffisance (obligatoire tous USAGE)** :
> DSL compréhensible SANS accès au document source.
> Toute référence interne → rappel du contenu clé inline.
> Références orphelines non résolues : interdites.

**Traçabilité bloc-à-bloc** :
- Chaque bloc DSL porte son index source : `[§N]`
- Section non numérotée → `[S1]`, `[S2]`... par ordre d'apparition
- Bloc sans index : interdit (sauf `[INFÉRÉ]` explicite)
- Mode RAG : chaque chunk porte EN TÊTE index + titre de section

**Balises obligatoires** :

| Balise | Usage |
|--------|-------|
| `[INFÉRÉ]` | Structure générée absente de la source |
| `[EMPHASE]` | Répétition intentionnelle conservée |
| `[EX]` | Exemple représentatif conservé |
| `[CRITIQUE]` | Garde-fou ou distinction haute priorité |
| `[CONFLIT §X vs §Y]` | Contradiction interne |
| `[CONFLIT-INTER]` | Contradiction inter-parties |
| `[?]` | Ambigu → validation humaine requise |
| `[TRONQUÉ]` | Section non traitée dans la passe courante |
| `[FUSIONNÉ]` | Bloc issu de fusion multi-passes |

---

## RÈGLE 5 — ADAPTATION PAR TYPE (priorités internes ordonnées)

| DOC_TYPE | Priorité 1 | Priorité 2 | Priorité 3 |
|----------|-----------|-----------|-----------|
| TECHNIQUE | Algos / procédés | Paramètres / dépendances | Garde-fous |
| ACADÉMIQUE | Hypothèses / résultats | Taxonomies / références | Méthodologie |
| JURIDIQUE | Obligations / interdictions | Définitions / exceptions | Sanctions |
| MÉDICAL | Protocoles / contre-indications | Posologies / seuils | Cas limites |
| FINANCIER | Seuils réglementaires | Règles calcul / ratios | Risques |
| STRATÉGIQUE | Objectifs / décisions | KPI / risques | Dépendances |
| NARRATIF | Arc / entités principales | Relations causales | Thèmes |
| CODE_SPEC | Contrats interface / guards | Types / API | Edge-cases |

> Conflit d'espace P1 vs P2 → retenir P1, baliser P2 avec `[?]`.

---

## RÈGLE 6 — VÉRIFICATION AVANT OUTPUT

```

1. RATIO    : longueur_DSL / longueur_source = X%
→ Hors cible (Règle 2) : ajuster avant output
2. CORE     : tous éléments Règle 0 couverts ?
→ Sinon : compléter
3. AUTO     : DSL compréhensible sans source ?
→ Vérifier références orphelines (cible : 0)
4. CONFLITS : contradictions balisées ?
5. BALISES  : [INFÉRÉ]/[CONFLIT]/[?] apposés partout où requis ?
6. TRACÉ    : chaque bloc porte [§N] ou [INFÉRÉ] ?
```

> Ne pas produire l'output si RATIO hors cible,
> CORE incomplet ou blocs non tracés.

---

## RÈGLE 7 — ITÉRATION MULTI-PASSES (si TAILLE = LARGE)

Activer si source > 50 000 caractères ou fenêtre contexte insuffisante.

### Protocole :
```

PASSE 1 : Découper en segments ≤ 40 000 caractères.
Respecter frontières sémantiques (fin de section).
Baliser : [SEGMENT-1/N], [SEGMENT-2/N]...

PASSE 2 : Appliquer R0-R6 sur chaque segment indépendamment.
Produire DSL partiel par segment.
Baliser éléments en attente de contexte : [TRONQUÉ]

PASSE 3 : Fusionner les DSL partiels.
Résoudre les [TRONQUÉ].
Détecter conflits inter-segments : [CONFLIT-INTER]
Déduplicater les éléments core redondants.
Baliser blocs fusionnés : [FUSIONNÉ §seg-X + §seg-Y]

PASSE 4 : Vérification Règle 6 sur DSL fusionné complet.

```

### Règles de découpe :
- Ne jamais couper au milieu d'une liste, table ou procédure
- 200 caractères de contexte chevauchant entre segments consécutifs
- Élément core chevauchant deux segments → dupliquer ; fusionner en P3

---

## RÈGLE 8 — MODE DIFF (si MODE = DIFF)

Comparer deux versions : Source A (ancienne) vs Source B (nouvelle).

### Protocole :
```

ÉTAPE 1 : Produire DSL(A) et DSL(B) indépendamment (R0-R6).
ÉTAPE 2 : Aligner sections homologues par titre et position.
ÉTAPE 3 : Identifier et baliser les changements (cf. table ci-dessous).
ÉTAPE 4 : Produire DSL DIFF unifié :
- En-tête : résumé (N ajouts / M suppressions / P modifications)
- Corps   : DSL de B avec balises DIFF inline
- Annexe  : liste complète éléments supprimés de A
ÉTAPE 5 : Vérification Règle 6 sur DSL DIFF.

```

**Balises DIFF** :

| Balise | Signification |
|--------|--------------|
| `[AJOUTÉ]` | Présent dans B, absent de A |
| `[SUPPRIMÉ]` | Présent dans A, absent de B |
| `[MODIFIÉ §A vs §B]` | Présent dans les deux, sémantique différente |
| `[INCHANGÉ]` | Identique A et B (omettre si USAGE=LLM_INPUT) |
| `[DÉPLACÉ §A→§B]` | Même contenu, position changée |

---

## SOURCE À TRANSFORMER

```

[INSÉRER ICI LE CONTENU COMPLET DU DOCUMENT]
[SI MODE = DIFF    : insérer Source A puis Source B séparément]
[SI TAILLE = LARGE : insérer segment par segment [SEGMENT-X/N]]

```

---

## VÉRIFICATION FINALE — TRIPLE CHECKLIST

### ✅ Éléments PRÉSERVÉS (min. 3 par critère Règle 0 couvert)
`- [R0-critèreN] Élément X : détail préservé [§source]`

### ❌ Éléments EXCLUS (exhaustif + justification)
`- Élément Y : exclu car [non-core | redite | hors-périmètre] [§source]`

### ⚠️ Éléments BALISÉS
`- [BALISE] Élément Z : nature ambiguïté / inférence / conflit`

### 📐 Métriques
```

Longueur source       : N caractères
Longueur DSL          : M caractères
Ratio atteint         : M/N = X%  (cible : Y%)
Contradictions        : N détectées / N balisées
Références orphelines : 0 (obligatoire)
Blocs non tracés      : 0 (obligatoire)
Passes effectuées     : 1 (NORMAL) | N (LARGE)
Éléments DIFF         : N ajouts / M suppr. / P modif. (MODE DIFF uniquement)

```

---

**OUTPUT : UNIQUEMENT** DSL généré + triple checklist + métriques.
Pas d'intro ni d'explications.
