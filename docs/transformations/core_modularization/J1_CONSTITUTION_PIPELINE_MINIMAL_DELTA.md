# J1 — delta minimal pour rendre `constitution` scope-aware

## Intention

Ce document décrit le **plus petit changement utile** à apporter au pipeline `docs/pipelines/constitution/pipeline.md` pour supporter un premier run borné, sans réécriture complète du pipeline.

Le principe est conservateur :
- garder le pipeline existant ;
- garder ses stages ;
- garder sa logique de promotion explicite ;
- introduire seulement les points nécessaires pour un scope borné.

---

## Ce qu'il ne faut pas faire à ce stade

- Ne pas créer un deuxième pipeline `constitution_scoped`.
- Ne pas créer un prompt de challenge différent par sous-module.
- Ne pas remplacer les Core actuels par une nouvelle structure source dès cette étape.
- Ne pas faire dépendre la réussite d'un nouveau compileur encore absent.

---

## Delta minimal recommandé

### 1. Ajouter la notion de `scope_manifest` dans les inputs du pipeline

Le pipeline doit accepter, en plus des Core courants et des notes optionnelles, un artefact optionnel puis recommandé :
- `inputs/scope_manifest.yaml`

Effet attendu :
- si absent, le pipeline continue en mode global nominal ;
- si présent, le pipeline passe en mode borné.

### 2. Ajouter la notion de `impact_bundle` dans les inputs de challenge/arbitrage

Le pipeline doit pouvoir accepter :
- `inputs/impact_bundle.yaml`

Effet attendu :
- l'IA sait quels artefacts et voisins logiques relire ;
- le scope modifiable reste gouverné par `scope_manifest`.

### 3. Ajouter une règle de bornage au Stage 01_CHALLENGE

Le Stage 01 doit expliciter :
- challenge ciblé sur le scope déclaré ;
- signalement obligatoire de tout impact hors scope détecté ;
- aucune recommandation de modification hors scope sans escalade explicite.

### 4. Ajouter une règle de bornage au Stage 02_ARBITRAGE

Le Stage 02 doit distinguer clairement :
- findings retenus **dans le scope** ;
- findings retenus mais **hors scope** ;
- findings différés faute d'élargissement de scope.

### 5. Ajouter une règle de bornage au Stage 03_PATCH_SYNTHESIS

Le patch produit doit :
- être limité au scope autorisé ;
- signaler explicitement toute dépendance hors scope nécessaire ;
- refuser les modifications silencieuses hors scope.

### 6. Ajouter un `integration_gate` avant release/promotion

Avant Stage 07/08, le pipeline doit pouvoir référencer :
- `inputs/integration_gate.yaml`
  ou
- un artefact généré en cours de run si ce gate est produit par le pipeline lui-même.

Effet attendu :
- aucun succès local ne peut être traité comme une promotion globale acquise ;
- le pipeline doit faire rejouer les contrôles globaux avant release/promotion.

---

## Impact minimal par stage

### STAGE_01_CHALLENGE
Ajout :
- lecture optionnelle de `inputs/scope_manifest.yaml`
- lecture optionnelle de `inputs/impact_bundle.yaml`
- mention explicite du mode `global` ou `bounded`

### STAGE_02_ARBITRAGE
Ajout :
- section obligatoire `out_of_scope_findings`
- section obligatoire `scope_extension_needed` ou `deferred_due_to_scope`

### STAGE_03_PATCH_SYNTHESIS
Ajout :
- vérification de conformité du patch au scope
- section obligatoire `scope_compliance`

### STAGE_04_PATCH_VALIDATION
Ajout :
- vérification que le patch n'écrit pas hors du scope déclaré
- signalement si le patch outrepasse le périmètre

### STAGE_05_APPLY
Ajout :
- aucun changement structurel majeur à ce stade
- l'apply reste sandboxé comme aujourd'hui

### STAGE_06_CORE_VALIDATION
Ajout :
- distinguer validation locale du scope et validation globale complète

### STAGE_07_RELEASE_MATERIALIZATION / STAGE_08_PROMOTE_CURRENT
Ajout :
- blocage conditionnel si le `integration_gate` n'est pas clairé

---

## Pourquoi ce delta est suffisant pour commencer

Parce qu'il permet déjà :
- un challenge borné ;
- un patch borné ;
- une discipline de non-dérive hors scope ;
- un point d'arrêt explicite avant promotion.

Et surtout, il évite deux erreurs :
- refondre trop tôt le pipeline ;
- croire qu'un patch local valide suffit à préserver la cohérence globale.

---

## Première expérimentation recommandée

Faire un pilote sur un sous-ensemble de la Constitution :
- assez petit pour être lisible ;
- assez relié pour tester les dépendances ;
- sans toucher encore à la structure physique des artefacts.

Sous-ensemble suggéré :
- `learner_state`
- avec ses règles de prudence et ses dépendances immédiates.

---

## Décision J1 associée

La première évolution du pipeline `constitution` doit être :

**l'ajout d'un mode borné piloté par artefacts de scope, sans duplication du pipeline.**
