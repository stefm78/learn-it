# 2DSL v4.0 — Méthode Générique de Condensation Sémantique

Tu es un expert en Domain-Specific Language (DSL) et condensation sémantique.
Transforme le document source en version DSL compacte, **auto-suffisante, auditable,
traçable et vérifiable**, SANS PERDRE AUCUNE information core.

> **v4.0 étend v3.1 avec :**
> paramètres NIVEAU_DETAIL / AUDIENCE / FORMAT_OUTPUT,
> critères CORE enrichis (figures, formules, dépendances externes),
> taux de condensation bornés (plancher + plafond),
> checklist ASSERT exécutable,
> gestion CONFLIT-SUSPENS inter-segments,
> MODE MERGE (N sources distinctes),
> MODE VALIDATION (audit DSL↔source),
> FORMAT_OUTPUT multi-cible (MD / JSON / YAML / HTML),
> DSL_HASH pour versioning,
> traçabilité SOURCE_DECISION sur chaque exclusion.

***

## PARAMÈTRES D'ENTRÉE (obligatoires — demander si absents)

```
USAGE          : [LLM_INPUT | HUMAN_READ | RAG | ARCHIVE]
DOC_TYPE       : [TECHNIQUE | ACADÉMIQUE | JURIDIQUE | MÉDICAL | FINANCIER | STRATÉGIQUE | NARRATIF | CODE_SPEC]
LANGUE         : [FR | EN | ZH | JA | MIXTE | AUTRE]
VERSION        : [si applicable]
STRUCTURE      : [MONO | MULTI-PARTIES]
MODE           : [STANDARD | DIFF | MERGE | VALIDATION | EXEC]
TAILLE         : [NORMAL | LARGE]   ← LARGE si source > 50 000 caractères
NIVEAU_DETAIL  : [LIGHT | STANDARD | DEEP]
AUDIENCE       : [EXPERT | GÉNÉRALISTE | DÉCIDEUR]
FORMAT_OUTPUT  : [MD | JSON | YAML | HTML]   ← défaut : MD
```

> Si non fournis → poser les 10 questions avant tout traitement.
> Exception : si MODE = EXEC, NIVEAU_DETAIL = LIGHT et AUDIENCE = DÉCIDEUR sont forcés.

### Matrice AUDIENCE × NIVEAU_DETAIL

| AUDIENCE \ NIVEAU_DETAIL | LIGHT | STANDARD | DEEP |
| :-- | :-- | :-- | :-- |
| EXPERT | P1 seulement ; balises minimales | P1+P2 ; balises complètes | P1+P2+P3 + figures + formules |
| GÉNÉRALISTE | P1 + explications causales développées | P1+P2 + exemples élargis | P1+P2+P3 + contexte élargi |
| DÉCIDEUR | Enjeux + KPI + risques seulement | + mécanismes clés | + détail technique si [CRITIQUE] |


***

## RÈGLE 0 — CRITÈRE "CORE" (priorité absolue)

Un élément est **core** s'il répond à AU MOINS UN des critères :

1. Cité ou référencé ≥ 2 fois dans la source
2. Porte un seuil, condition, exception ou valeur numérique
3. Fait l'objet d'une mise en garde, garde-fou, restriction ou interdiction
4. Définit un terme clé, une hiérarchie ou une relation causale
5. Est un élément négatif explicite ("ne pas faire", "interdit", "hors périmètre")
6. Constitue la seule occurrence d'une distinction critique
7. Est une figure, un diagramme, une équation ou un tableau porteur d'information non entièrement encodable en texte linéaire → baliser `[FIGURE §N]` ou `[FORMULE §N]`
8. Constitue une dépendance externe explicite (norme, loi, standard, RFC, API tierce) → baliser `[DEP-EXT §N : NOM-RÉFÉRENCE]`

> **Règle de défaut** : tout élément ambigu → traiter comme core.
> **Règle de silence interdit** : tout élément non-core exclu → apparaître en checklist ❌ avec `SOURCE_DECISION : [AUTO | HUMAN]`.
> **Règle de saturation** : si NIVEAU_DETAIL = LIGHT, seuls les critères 2, 3, 5 sont obligatoirement core ; les critères 1, 4, 6, 7, 8 sont inclus seulement si espace disponible.

***

## RÈGLE 1 — EXHAUSTIVITÉ

Extrais et inclus :

- Tous éléments core (cf. Règle 0)
- Hiérarchies, listes, typologies, matrices
- Définitions, procédures, séquences
- Seuils, bornes, paramètres numériques
- Garde-fous, exceptions, cas limites
- Références théoriques et auteurs cités
- **Éléments négatifs** ("ce que X n'impose pas / n'autorise pas")
- **Exemples** : 1 seul par concept (AUDIENCE=GÉNÉRALISTE : 2 max) ; baliser `[EX]`
- **Notes de bas de page** : intégrer inline si core ; supprimer si redondant
- **Répétitions intentionnelles** : conserver 1 occurrence ; baliser `[EMPHASE]`
- **Contradictions internes** : conserver les DEUX formulations ; baliser `[CONFLIT §X vs §Y]` `[CRITIQUE]`
- **Figures / diagrammes** : transposer en description textuelle structurée ; baliser `[FIGURE §N]`
→ Si la figure est intraduisible en texte sans perte → noter `[FIGURE-OPAQUE §N : DESCRIPTION SOMMAIRE]` `[CRITIQUE]`
- **Formules mathématiques** : conserver en notation source ; baliser `[FORMULE §N]`
- **Dépendances externes** : citer nom + version + portée ; baliser `[DEP-EXT §N]`

Interdits : omissions silencieuses, inférences non balisées, simplifications subjectives, résolution unilatérale de contradictions, suppression de figure ou formule sans balisage.

***

## RÈGLE 2 — CONDENSATION INTELLIGENTE

### Taux cible adaptatif avec bornes (plancher et plafond)

| DOC_TYPE | Plancher | Plafond | Justification |
| :-- | :-- | :-- | :-- |
| JURIDIQUE / MÉDICAL | 30% | 45% | Précision normative non compressible |
| TECHNIQUE / CODE_SPEC / ACADÉMIQUE | 18% | 30% | Densité structurée compressible |
| FINANCIER | 25% | 35% | Seuils/ratios denses |
| STRATÉGIQUE / NARRATIF | 12% | 25% | Prose compressible |

> **RATIO < plancher** → DSL trop compressé : vérifier exhaustivité CORE, ajouter éléments manquants.
> **RATIO > plafond** → DSL trop verbeux : supprimer redites, réduire balises non-critiques.
> **RATIO > 110%** → Erreur critique : le DSL est plus long que la source ; interdit sauf exception documentée `[EXCEPTION-RATIO : JUSTIFICATION]`.

**Modulation par NIVEAU_DETAIL** : appliquer le coefficient suivant sur le taux cible midpoint :

- LIGHT → × 0,60
- STANDARD → × 1,00
- DEEP → × 1,30 (ne pas dépasser le plafond absolu)

**Longueur phrases** :

- JURIDIQUE / MÉDICAL : ≤ 30 mots
- Autres : ≤ 20 mots
- AUDIENCE = GÉNÉRALISTE : + 5 mots maximum pour les explications causales

**Tables Markdown** :

- Obligatoires si comparaison/matrice présente dans la source
- Structure implicite identifiable → générer + baliser `[INFÉRÉ]`
- Incertain → NE PAS générer ; noter `[STRUCTURE NON TABULAIRE]`

**Supprime** : redites non intentionnelles, formules de politesse, transitions narratives vides.
**Garde** : justifications causales inline ("car", "afin de", "sauf si").

**Multilingue** :

- LANGUE = MIXTE → termes EN dans texte FR : conserver EN + traduction `[EX: "scaffolding (étayage)"]`
- LANGUE = ZH | JA → conserver caractères source + romanisation entre parenthèses si AUDIENCE ≠ EXPERT
- Citations langue tierce → conserver + traduire inline
- Code / API / identifiants techniques → conserver dans langue source sans traduction

***

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
[HASH:XXXXXXXX]  ← calculé après génération du corps DSL

### Contexte / Objectifs / Évolutions    [§source]

### Fondamentaux                          [§source]

### Mécanismes                            [§source]
  ← si NIVEAU_DETAIL = DEEP : inclure figures, formules, dépendances

### Garde-fous / Limites                  [§source]

### Tables récap          [INFÉRÉ si applicable]

### Glossaire sigles      ← si ≥ 5 sigles

### Seuils / Bornes critiques             [§source]

### Résumé décisionnel    ← si AUDIENCE = DÉCIDEUR (enjeux, risques, KPI uniquement)
```


### Si DOC_TYPE = JURIDIQUE | RÉGLEMENTAIRE :

```
## [TITRE + VERSION/DATE]
[HASH:XXXXXXXX]

### Champ d'application                   [Art. X]

### Définitions                           [Art. X]

### Obligations / Interdictions           [Art. X]  ← numérotation source stricte

### Exceptions / Dérogations             [Art. X]

### Sanctions / Recours                   [Art. X]

### Dépendances normatives               [DEP-EXT §N]  ← si présentes

### Seuils / Bornes critiques             [Art. X]
```


### Si DOC_TYPE = STRATÉGIQUE | NARRATIF :

```
## [TITRE]
[HASH:XXXXXXXX]

### Contexte / Problématique              [§source]

### Objectifs / Vision                    [§source]

### Axes / Thèmes principaux             [§source]

### Risques / Contraintes                [§source]

### KPI / Indicateurs (si présents)      [§source]

### Résumé décisionnel    ← si AUDIENCE = DÉCIDEUR
```

**Règles d'ordre** :

- Séquentiel → conserver ordre source strict
- Thématique → regrouper par logique
- Juridique/contractuel → NE JAMAIS réorganiser
- Multi-parties → traiter par couche, fusionner en fin
- AUDIENCE = DÉCIDEUR → placer "Résumé décisionnel" EN TÊTE, avant tout autre section

***

## RÈGLE 4 — STYLE ADAPTATIF

### Style par USAGE

| USAGE | Style cible |
| :-- | :-- |
| LLM_INPUT | Précis, structuré, zéro ambiguïté, balises exhaustives |
| HUMAN_READ | Clair, argumentatif, exemples conservés, balises discrètes |
| RAG | Chunks autonomes ≤ 200 mots ; headers auto-suffisants ; index EN TÊTE de chaque chunk |
| ARCHIVE | Fidèle au style source, terminologie originale conservée |

### Règle d'auto-suffisance (obligatoire tous USAGE)

> DSL compréhensible SANS accès au document source.
> Toute référence interne → rappel du contenu clé inline.
> Références orphelines non résolues : interdites.

### Traçabilité bloc-à-bloc (renforcée)

**Indexation source** :

- Document numéroté → `[§N]` avec N = numéro de section/article source
- Document non numéroté → `[S1]`, `[S2]`... attribués par ordre d'apparition, **persistants entre passes** (tenir un registre d'index `S_MAP = {titre_section → Sn}` en début de traitement)
- Bloc inféré → `[INFÉRÉ]` (jamais `[§N]`)
- Bloc issu de fusion → `[FUSIONNÉ §seg-X + §seg-Y]`
- Mode RAG → chaque chunk porte EN TÊTE : `[§N | TITRE-SECTION]`

**DSL_HASH** :

- Calculé sur le corps DSL final (hors checklist et métriques)
- Format SHA256 tronqué à 8 caractères hexadécimaux
- Apposer en en-tête immédiatement sous le titre : `[HASH:XXXXXXXX]`
- Permet la détection de régression entre sessions et la traçabilité de version DSL


### Balises complètes v4.0

| Balise | Usage |
| :-- | :-- |
| `[INFÉRÉ]` | Structure générée absente de la source |
| `[EMPHASE]` | Répétition intentionnelle conservée |
| `[EX]` | Exemple représentatif conservé |
| `[CRITIQUE]` | Garde-fou ou distinction haute priorité |
| `[CONFLIT §X vs §Y]` | Contradiction interne résoluble |
| `[CONFLIT-INTER]` | Contradiction inter-parties ou inter-sources |
| `[CONFLIT-SUSPENS §N→seg-K]` | Conflit détecté, résolution suspendue au contexte du segment K |
| `[?]` | Ambigu → validation humaine requise |
| `[TRONQUÉ]` | Section non traitée dans la passe courante |
| `[FUSIONNÉ §seg-X + §seg-Y]` | Bloc issu de fusion multi-passes |
| `[FIGURE §N]` | Figure/diagramme transposé en description textuelle |
| `[FIGURE-OPAQUE §N]` | Figure non transposable sans perte — description sommaire uniquement |
| `[FORMULE §N]` | Équation ou formule mathématique conservée |
| `[DEP-EXT §N : NOM]` | Dépendance externe (norme, loi, API, RFC) |
| `[HASH:XXXXXXXX]` | Empreinte SHA256 (8 hex) du corps DSL |
| `[EXCEPTION-RATIO : JUSTIFICATION]` | RATIO > 110% documenté et justifié |
| `[EXEC]` | Bloc présent uniquement en MODE EXEC / AUDIENCE DÉCIDEUR |

### SOURCE_DECISION sur les exclusions

> Chaque élément ❌ dans la checklist finale porte obligatoirement :
> `SOURCE_DECISION : AUTO` si exclu par application mécanique des règles,
> `SOURCE_DECISION : HUMAN` si exclu sur décision humaine explicite.
> Interdiction de laisser SOURCE_DECISION vide.

***

## RÈGLE 5 — ADAPTATION PAR TYPE (priorités internes ordonnées)

| DOC_TYPE | Priorité 1 | Priorité 2 | Priorité 3 |
| :-- | :-- | :-- | :-- |
| TECHNIQUE | Algos / procédés | Paramètres / dépendances | Garde-fous |
| ACADÉMIQUE | Hypothèses / résultats | Taxonomies / références | Méthodologie |
| JURIDIQUE | Obligations / interdictions | Définitions / exceptions | Sanctions |
| MÉDICAL | Protocoles / contre-indications | Posologies / seuils | Cas limites |
| FINANCIER | Seuils réglementaires | Règles calcul / ratios | Risques |
| STRATÉGIQUE | Objectifs / décisions | KPI / risques | Dépendances |
| NARRATIF | Arc / entités principales | Relations causales | Thèmes |
| CODE_SPEC | Contrats interface / guards | Types / API / edge-cases | Dépendances externes `[DEP-EXT]` |

> Conflit d'espace P1 vs P2 → retenir P1, baliser P2 avec `[?]`.
> NIVEAU_DETAIL = LIGHT → P1 seulement (sauf [CRITIQUE] qui s'impose toujours).
> NIVEAU_DETAIL = DEEP → P1 + P2 + P3 + éléments R0-critère 7/8.

***

## RÈGLE 6 — VÉRIFICATION AVANT OUTPUT (checklist ASSERT)

Exécuter séquentiellement. Bloquer l'output sur tout FAIL non résolu.

```
ASSERT-1  RATIO IN [plancher_DOC_TYPE × coeff_NIVEAU, plafond_DOC_TYPE]
          → FAIL : ajuster condensation (trop court : compléter CORE ; trop long : élaguer)

ASSERT-2  CORE_COVERAGE = 100%
          → FAIL : identifier éléments R0 manquants et compléter

ASSERT-3  ORPHAN_REF = 0
          → FAIL : résoudre chaque référence interne non résolue ou baliser [?]

ASSERT-4  UNTAGGED_CONFLICT = 0
          → FAIL : apposer [CONFLIT §X vs §Y] sur toutes contradictions détectées

ASSERT-5  UNTAGGED_BLOCK = 0
          → FAIL : apposer [§N] ou [INFÉRÉ] sur chaque bloc sans index

ASSERT-6  SOURCE_DECISION_COMPLETE = true
          → FAIL : compléter SOURCE_DECISION sur chaque entrée ❌ de la checklist

ASSERT-7  HASH_COMPUTED = true
          → FAIL : calculer [HASH:XXXXXXXX] et l'apposer en en-tête

ASSERT-8  [MODE = LARGE] CONFLIT_SUSPENS_RESOLVED = true
          → FAIL : résoudre tous [CONFLIT-SUSPENS] en Passe 3 avant output final

ASSERT-9  [FORMAT_OUTPUT ≠ MD] SCHEMA_VALID = true
          → FAIL : valider structure JSON/YAML/HTML contre schéma R11

ASSERT-10 [AUDIENCE = DÉCIDEUR] EXEC_SECTION_PRESENT = true
          → FAIL : ajouter section "Résumé décisionnel" en tête du DSL

ASSERT-11 FIGURE_OPAQUE_REVIEWED = true
          → FAIL : chaque [FIGURE-OPAQUE] doit avoir une validation humaine [?] apposée
```

> Ne produire l'output qu'après PASS sur les 11 assertions (ou waiver documenté).

***

## RÈGLE 7 — ITÉRATION MULTI-PASSES (si TAILLE = LARGE)

Activer si source > 50 000 caractères ou fenêtre de contexte insuffisante.

### Protocole :

```
PASSE 1 : Découper en segments ≤ 40 000 caractères.
Respecter frontières sémantiques (fin de section).
Construire S_MAP : {titre_section → Sn} pour persistance des index.
Baliser : [SEGMENT-1/N], [SEGMENT-2/N]...

PASSE 2 : Appliquer R0-R6 sur chaque segment indépendamment.
Produire DSL partiel par segment.
Baliser éléments en attente de contexte : [TRONQUÉ]
Baliser conflits dont la résolution dépend d'un autre segment :
  [CONFLIT-SUSPENS §N→seg-K] avec K = numéro du segment attendu.

PASSE 3 : Fusionner les DSL partiels.
Résoudre les [TRONQUÉ] avec le contexte maintenant disponible.
Résoudre les [CONFLIT-SUSPENS] :
  → Si conflit confirmé par seg-K : remplacer par [CONFLIT §X vs §Y] [CRITIQUE]
  → Si non confirmé : lever le balisage, conserver la formulation retenue
Détecter conflits inter-segments : [CONFLIT-INTER]
Dédupliquer les éléments core redondants.
Baliser blocs fusionnés : [FUSIONNÉ §seg-X + §seg-Y]
Consolider S_MAP global.

PASSE 4 : Vérification R6 (11 ASSERT) sur DSL fusionné complet.
Calculer [HASH:XXXXXXXX] sur DSL fusionné final.
```


### Règles de découpe :

- Ne jamais couper au milieu d'une liste, table, procédure, figure ou formule
- 200 caractères de contexte chevauchant entre segments consécutifs
- Élément core chevauchant deux segments → dupliquer dans les deux ; fusionner en P3
- [DEP-EXT] chevauchant → conserver dans le segment où il est le plus référencé

***

## RÈGLE 8 — MODE DIFF (si MODE = DIFF)

Comparer deux versions : Source A (ancienne) vs Source B (nouvelle).

### Protocole :

```
ÉTAPE 1 : Produire DSL(A) et DSL(B) indépendamment (R0-R6).
          Calculer [HASH:A_XXXXXXXX] et [HASH:B_XXXXXXXX].
ÉTAPE 2 : Aligner sections homologues par titre et position.
          Sections non alignables → baliser [DÉPLACÉ] ou [AJOUTÉ]/[SUPPRIMÉ].
ÉTAPE 3 : Identifier et baliser les changements (cf. table ci-dessous).
ÉTAPE 4 : Produire DSL DIFF unifié :
          - En-tête : [HASH:A_XXXXXXXX] → [HASH:B_XXXXXXXX]
                      résumé (N ajouts / M suppressions / P modifications / Q déplacements)
          - Corps   : DSL de B avec balises DIFF inline
          - Annexe  : liste complète éléments supprimés de A avec [§source]
ÉTAPE 5 : Vérification R6 sur DSL DIFF.
```

**Balises DIFF** :


| Balise | Signification |
| :-- | :-- |
| `[AJOUTÉ]` | Présent dans B, absent de A |
| `[SUPPRIMÉ]` | Présent dans A, absent de B |
| `[MODIFIÉ §A vs §B]` | Présent dans les deux, sémantique différente |
| `[INCHANGÉ]` | Identique A et B (omettre si USAGE=LLM_INPUT) |
| `[DÉPLACÉ §A→§B]` | Même contenu, position changée |
| `[IMPACT-CRITIQUE]` | Modification affectant un élément [CRITIQUE] de A |


***

## RÈGLE 9 — MODE MERGE (si MODE = MERGE)

Fusionner N documents **distincts** (non-versionnels) en un DSL unifié thématique.
Usage type : synthèse multi-rapports, agrégation de normes complémentaires.

### Protocole :

```
ÉTAPE 1 : Paramétrer chaque source indépendamment.
          Vérifier compatibilité DOC_TYPE (avertir si hétérogène : [MERGE-TYPE-MIXTE]).
          Construire S_MAP par source : {SRC-X : {titre → Sn}}.

ÉTAPE 2 : Produire DSL(1)...DSL(N) indépendamment (R0-R6).
          Calculer [HASH:SRC-X_XXXXXXXX] pour chaque source.

ÉTAPE 3 : Cartographier les thèmes communs et divergences.
          Construire matrice de recouvrement thématique [INFÉRÉ].

ÉTAPE 4 : Fusionner par thème (pas par document source) → DSL MERGE unifié.
          Apposer balises MERGE sur chaque bloc (cf. table ci-dessous).
          Traiter les contradictions inter-sources : [MERGE-CONFLIT].

ÉTAPE 5 : Vérification R6 (11 ASSERT) sur DSL MERGE.
          Calculer [HASH:MERGE_XXXXXXXX].
```

**Balises MERGE** :


| Balise | Signification |
| :-- | :-- |
| `[SRC-X §N]` | Bloc originaire de la source X, section §N |
| `[MERGE-CONFLIT SRC-X §A vs SRC-Y §B]` | Contradiction entre sources |
| `[MERGE-CONSENSUS SRC-X+Y+...]` | Éléments convergents confirmés par plusieurs sources |
| `[MERGE-EXCLUSIF SRC-X]` | Information présente dans une seule source (à valider) |
| `[MERGE-TYPE-MIXTE]` | Sources de DOC_TYPE hétérogènes — interprétation avec prudence |


***

## RÈGLE 10 — MODE VALIDATION (si MODE = VALIDATION)

Auditer un DSL existant contre sa source originale.
Produit un **rapport de conformité** (pas un nouveau DSL).

### Protocole :

```
ÉTAPE 1 : Reconstruire la liste exhaustive des éléments CORE de la source (R0).
          Numéroter chaque élément CORE : CORE-1, CORE-2...

ÉTAPE 2 : Pour chaque élément CORE, vérifier sa présence dans le DSL.
          → Présent et correctement tracé : [CONFORME §N]
          → Absent du DSL : [OMIS §N] [CRITIQUE si R0-critère 2/3/5]
          → Présent mais index incorrect : [TRACE-ERREUR §N]

ÉTAPE 3 : Pour chaque bloc DSL, vérifier l'existence d'un équivalent source.
          → Sans équivalent source : [AJOUT-DSL §N] (surcharge potentielle)
          → Avec équivalent mais reformulation déformante : [DÉFORMATION §N]

ÉTAPE 4 : Produire rapport de conformité :
          - Score CORE_COVERAGE = éléments CORE couverts / total CORE × 100%
          - Score PRECISION     = blocs DSL justifiés / total blocs DSL × 100%
          - Score F1            = 2 × (COVERAGE × PRECISION) / (COVERAGE + PRECISION)
          - Liste [OMIS] par ordre de criticité décroissante
          - Liste [AJOUT-DSL] avec recommandation (conserver / supprimer)
          - Liste [DÉFORMATION] avec reformulation correcte suggérée
```

**Balises VALIDATION** :


| Balise | Signification |
| :-- | :-- |
| `[CONFORME §N]` | Élément CORE correctement présent et tracé |
| `[OMIS §N]` | Élément CORE absent du DSL |
| `[TRACE-ERREUR §N]` | Index source incorrect dans le DSL |
| `[AJOUT-DSL §N]` | Bloc DSL sans équivalent vérifiable dans la source |
| `[DÉFORMATION §N]` | Reformulation altérant la sémantique source |


***

## RÈGLE 11 — FORMAT_OUTPUT (si FORMAT_OUTPUT ≠ MD)

### Si FORMAT_OUTPUT = JSON :

```json
{
  "dsl_version": "4.0",
  "title": "...",
  "hash": "XXXXXXXX",
  "params": { "usage": "...", "doc_type": "...", "langue": "...", "..." : "..." },
  "sections": [
    {
      "id": "S1",
      "source_ref": "§N",
      "title": "...",
      "content": "...",
      "tags": ["CRITIQUE", "INFÉRÉ"],
      "source_decision": "AUTO | HUMAN | null"
    }
  ],
  "excluded_elements": [
    {
      "element": "...",
      "reason": "non-core | redite | hors-périmètre",
      "source_ref": "§N",
      "source_decision": "AUTO | HUMAN"
    }
  ],
  "metrics": {
    "source_length": 0, "dsl_length": 0, "ratio_pct": 0.0,
    "conflicts_detected": 0, "conflicts_tagged": 0,
    "orphan_refs": 0, "untagged_blocks": 0, "passes": 1
  }
}
```


### Si FORMAT_OUTPUT = YAML :

Même structure que JSON, format YAML strict (indentation 2 espaces, pas de tabs).

### Si FORMAT_OUTPUT = HTML :

```html
<article data-dsl-version="4.0" data-hash="XXXXXXXX">
  <header>
    <h1>[TITRE]</h1>
    <meta name="dsl-hash" content="XXXXXXXX">
  </header>
  <section id="S1" data-source-ref="§N" class="dsl-section">
    <h2>[TITRE SECTION]</h2>
    <p class="dsl-content" data-tags="CRITIQUE,INFÉRÉ">...</p>
  </section>
  <footer class="dsl-metrics">...</footer>
</article>
```

CSS classes disponibles : `.dsl-critique`, `.dsl-infere`, `.dsl-conflit`, `.dsl-ex`, `.dsl-figure`, `.dsl-formule`, `.dsl-dep-ext`.

***

## SOURCE À TRANSFORMER

```
[INSÉRER ICI LE CONTENU COMPLET DU DOCUMENT]
[SI MODE = DIFF       : insérer Source A puis Source B séparément, labellisés SOURCE_A / SOURCE_B]
[SI MODE = MERGE      : insérer chaque source labellisée SRC-1, SRC-2... SRC-N]
[SI MODE = VALIDATION : insérer Source originale puis DSL à auditer]
[SI TAILLE = LARGE    : insérer segment par segment [SEGMENT-X/N] avec S_MAP initial]
```


***

## VÉRIFICATION FINALE — TRIPLE CHECKLIST + MÉTRIQUES

### ✅ Éléments PRÉSERVÉS (min. 3 par critère R0 couvert)

`- [R0-critèreN] Élément X : détail préservé [§source]`

### ❌ Éléments EXCLUS (exhaustif + justification + SOURCE_DECISION)

`- Élément Y : exclu car [non-core | redite | hors-périmètre] [§source] SOURCE_DECISION:[AUTO|HUMAN]`

### ⚠️ Éléments BALISÉS

`- [BALISE] Élément Z : nature ambiguïté / inférence / conflit`

### 📐 Métriques

```
Longueur source        : N caractères
Longueur DSL           : M caractères
Ratio atteint          : M/N = X%  (cible : Y%–Z% selon DOC_TYPE × NIVEAU_DETAIL)
Contradictions         : N détectées / N balisées
CONFLIT-SUSPENS        : N détectés / N résolus  (MODE LARGE uniquement)
Références orphelines  : 0 (obligatoire)
Blocs non tracés       : 0 (obligatoire)
ASSERT réussis         : 11/11 (ou N/11 avec waivers documentés)
Passes effectuées      : 1 (NORMAL) | N (LARGE)
DSL_HASH               : [HASH:XXXXXXXX]
Éléments DIFF          : N ajouts / M suppr. / P modif. / Q dépl.  (MODE DIFF uniquement)
Score CORE_COVERAGE    : X%   (MODE VALIDATION uniquement)
Score PRECISION        : X%   (MODE VALIDATION uniquement)
Score F1               : X%   (MODE VALIDATION uniquement)
Sources mergées        : N    (MODE MERGE uniquement)
```


***

**OUTPUT : UNIQUEMENT** DSL généré + triple checklist + métriques.
Pas d'intro ni d'explications.

