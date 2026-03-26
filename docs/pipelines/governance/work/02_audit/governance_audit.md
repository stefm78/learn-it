# Governance audit — Learn-it

## Résumé exécutif

Le repo présente une **structure opératoire globalement saine** :

- la séparation physique entre `docs/` et `legacy/` est réelle ;
- `docs/cores/current/` joue correctement son rôle de zone canonique courante ;
- `docs/cores/releases/` matérialise bien l’historique promu ;
- le pipeline `governance` existe, est structuré par étapes, et dispose d’un espace de travail explicite ;
- `docs/README.md` et `docs/registry/operating_model.md` convergent bien sur le principe central : le repo est désormais gouverné par pipelines.

En revanche, l’audit montre que la **couche registry n’est pas encore complètement synchronisée avec la structure réelle du repo**. La dérive observée n’est pas celle d’un framework cassé ; c’est celle d’un framework **correct dans son intention mais encore inégal dans sa documentation opératoire**.

Constat synthétique :

- **aucune anomalie critique bloquante** n’a été identifiée ;
- plusieurs **anomalies majeures** touchent la précision des registres et la clarté de l’autorité ;
- quelques **anomalies mineures** affectent la lisibilité, la robustesse des scans et la stabilité des conventions ;
- le risque principal est qu’une IA ou un contributeur humain choisisse un **mauvais point d’entrée** ou une **mauvaise ressource de référence** alors même que l’architecture de fond est bonne.

En l’état, le repo est **opérable**, mais il ne raconte pas encore une vérité parfaitement unique sur :

- ce qui est actif,
- ce qui est seulement conservé,
- ce qui est la vraie source de vérité,
- et quels outils partagés sont réellement ceux à utiliser.

---

## Inventaire des anomalies

### Anomalies critiques

Aucune anomalie critique bloquante détectée sur les entrées auditées.

Le repo distingue bien, au niveau de l’arborescence, les zones suivantes :

- operating : `docs/registry/`, `docs/pipelines/`, `docs/prompts/shared/`, `docs/patcher/shared/`
- canonical current : `docs/cores/current/`
- releases : `docs/cores/releases/`
- legacy : `legacy/`
- architecture/support : `docs/architecture/`

La structure de base n’est donc pas en contradiction frontale avec l’operating model.

### Anomalies majeures

#### MAJ-01 — `docs/registry/pipelines.md` contient des règles globales incomplètes et partiellement obsolètes

**Localisation** : `docs/registry/pipelines.md`

**Constat** :
Le registre pipelines annonce des règles globales qui ne reflètent pas exactement le repo réel ni le pipeline `governance` lui-même.

Points observés :

1. la règle globale parle de `archive/`, alors que le repo réel met en avant `legacy/` comme couche non canonique ;
2. la liste des ressources qu’un pipeline peut consommer n’inclut pas `docs/specs/release-patch/current.md`, pourtant référencé comme ressource canonique du pipeline `governance` ;
3. cette même liste n’inclut pas `docs/cores/releases/` ni `docs/architecture/`, alors que le pipeline `governance` gouverne explicitement ces couches ;
4. la règle globale semble plus restrictive que la réalité opératoire du repo.

**Pourquoi c’est majeur** :
Le registre `pipelines.md` est censé être une couche déclarative stable. S’il raconte une portée inexacte, il devient une source de confusion pour :

- un contributeur humain,
- une IA de navigation,
- un audit automatique de conformité.

**Effet concret** :
Le repo dit que `governance` doit surveiller certaines couches, mais le registre global ne formalise pas correctement cette portée.

---

#### MAJ-02 — `docs/registry/resources.md` ne reflète pas fidèlement les ressources réellement présentes

**Localisation** : `docs/registry/resources.md`

**Constat** :
Le registre des ressources contient plusieurs décalages avec l’inventaire réel du repo.

Points observés :

1. il référence `legacy/referentiel/`, alors que l’inventaire réel montre `legacy/docs/referentiel/` ;
2. il n’inventorie pas certains fichiers présents dans `docs/patcher/shared/`, notamment :
   - `docs/patcher/shared/apply_patch_v4.py`
   - `docs/patcher/shared/validate_patchset_v4.py`
   - `docs/patcher/shared/README.md`
3. la section `Legacy active Core location` est sémantiquement dangereuse : un emplacement situé sous `legacy/` ne devrait pas être qualifié d’“active”.

**Pourquoi c’est majeur** :
Un registre de ressources imprécis dégrade directement la qualité de navigation et de sélection d’artefacts.

**Effet concret** :
Une IA ou un opérateur peut :

- pointer vers un mauvais chemin ;
- ignorer un outil réellement présent ;
- surestimer l’importance d’une ressource legacy en raison d’un libellé ambigu.

---

#### MAJ-03 — Des fichiers `.bak` subsistent dans la couche `docs/registry/`, ce qui brouille la source de vérité

**Localisation** :

- `docs/registry/operating_model.md.bak`
- `docs/registry/resources.md.bak`

**Constat** :
Des copies de sauvegarde sont visibles directement dans une couche déclarée comme structurante et autoritative.

**Pourquoi c’est majeur** :
L’operating model affirme qu’un artefact susceptible d’être confondu avec le canonique doit être déplacé, marqué ou archivé. Or une extension `.bak` dans `docs/registry/` reste proche, lisible et ambiguë.

**Effet concret** :
Ces fichiers :

- polluent la couche d’autorité,
- compliquent les scans automatiques,
- augmentent le risque de lecture ou d’édition au mauvais endroit,
- affaiblissent le message “une seule vérité opératoire”.

---

#### MAJ-04 — La doctrine sur les patchers partagés n’est pas complètement stabilisée dans les registres

**Localisation** :

- `docs/registry/resources.md`
- `docs/pipelines/governance/pipeline.md`

**Constat** :
Le repo contient à la fois des patchers génériques et des patchers explicitement versionnés en `v4` dans `docs/patcher/shared/`. Pourtant, la documentation opératoire ne formalise pas clairement :

- si les variantes `v4` remplacent la ligne standard,
- si elles sont complémentaires,
- ou si elles doivent rester des outils historiques encore visibles mais non privilégiés.

**Pourquoi c’est majeur** :
L’absence de doctrine explicite sur l’outil “à utiliser en premier” ouvre une zone grise dans une couche qui devrait être strictement déterministe.

**Effet concret** :
Deux opérateurs peuvent faire deux choix différents tout en pensant être conformes.

---

### Anomalies mineures

#### MIN-01 — `docs/registry/pipelines.md` présente `governance` après les règles globales, ce qui affaiblit la lisibilité du registre

**Localisation** : `docs/registry/pipelines.md`

**Constat** :
La section `governance` est listée après `## Global rules` alors qu’elle appartient logiquement à la section `## Available pipelines`.

**Impact** :
Ce n’est pas faux sur le fond, mais cela nuit à la cohérence de lecture et à la symétrie avec les autres pipelines.

---

#### MIN-02 — `docs/registry/conventions.md` mentionne des couches d’archive non visibles dans l’arborescence réelle auditée

**Localisation** : `docs/registry/conventions.md`

**Constat** :
Le document mentionne :

- `docs/specs/patch-dsl/archive/`
- `docs/prompts/archive/`
- `docs/patcher/archive/`

Ces emplacements ne figurent pas dans l’inventaire fourni.

**Impact** :
Deux interprétations deviennent possibles :

- soit ce sont des chemins réservés mais non encore instanciés ;
- soit la convention n’est plus strictement calée sur l’état réel du repo.

Le point est mineur mais mérite clarification.

---

#### MIN-03 — Le vocabulaire de hiérarchie d’autorité n’est pas encore totalement normalisé entre `README` et `operating_model`

**Localisation** :

- `docs/README.md`
- `docs/registry/operating_model.md`

**Constat** :
Les deux documents convergent sur le fond, mais ils ne formulent pas exactement la hiérarchie de la même manière.

Le `README` donne une liste d’autorité linéaire très opérationnelle. L’`operating_model` sépare davantage :

- l’autorité structurelle,
- l’autorité canonique courante,
- l’autorité release,
- la couche non autoritative.

**Impact** :
Il n’y a pas contradiction directe, mais il existe un léger écart de formulation qui peut gêner un lecteur ou une IA cherchant une seule taxonomie verbale.

---

#### MIN-04 — Le fichier d’inventaire de scan contient un préfixe de contrôle terminal parasite

**Localisation** : `docs/pipelines/governance/work/01_scan/repo_inventory.md`

**Constat** :
Le fichier commence par une séquence de contrôle issue du terminal avant le contenu Markdown utile.

**Impact** :
Le contenu reste exploitable, mais cette pollution :

- rend la lecture plus sale,
- peut perturber une chaîne de traitement automatisée,
- diminue la qualité du pipeline de gouvernance comme source d’entrée stable.

---

### Améliorations possibles

#### IMP-01 — Ajouter un marquage explicite du legacy au niveau des sous-zones les plus sensibles

Exemples pertinents :

- `legacy/Current_Constitution/`
- `legacy/docs/referentiel/`
- `legacy/make_constitution/`

L’objectif n’est pas de les supprimer, mais de réduire toute ambiguïté de lecture.

---

#### IMP-02 — Définir une politique explicite sur les fichiers de sauvegarde

Exemple de règle à arbitrer :

- aucun `.bak` toléré dans `docs/registry/`
- backups déplacés vers `legacy/` ou vers un espace de travail pipeline
- ou suppression après validation

---

#### IMP-03 — Stabiliser une doctrine unique sur le couple “standard vs versionné” pour les patchers

Il faut décider si la couche partagée doit exposer :

- des noms génériques seulement,
- des noms versionnés seulement,
- ou les deux avec une règle de priorité explicite.

---

#### IMP-04 — Introduire une règle de complétude du registre des ressources

Le registre pourrait préciser explicitement s’il vise :

- l’exhaustivité,
- les seules ressources canoniques prioritaires,
- ou un sous-ensemble minimal de navigation.

Sans cela, chaque omission peut être interprétée soit comme une erreur, soit comme un choix.

---

#### IMP-05 — Mieux expliciter le statut de `docs/architecture/`

La couche `docs/architecture/` est bien présente dans l’inventaire réel et clairement non canonique dans le `README`, mais elle gagnerait à être plus explicitement qualifiée comme :

- support de compréhension,
- documentation d’architecture,
- non source de vérité opératoire.

---

## Risques de dérive

### 1. Dérive de navigation

Le principal risque n’est pas une corruption du canonique, mais une mauvaise orientation.

Un contributeur ou une IA peut :

- lire le bon repo mais le mauvais registre,
- choisir le mauvais outil partagé,
- ou suivre un chemin théorique qui n’est pas exactement celui du repo réel.

### 2. Dérive de source de vérité

Les fichiers `.bak` dans `docs/registry/` créent une ambiguïté locale dans une zone qui devrait être exemplaire.

Même si un humain comprend la différence, une automatisation ou une lecture rapide peut échouer à la hiérarchiser proprement.

### 3. Dérive de portée des pipelines

Si `pipelines.md` reste incomplet sur les couches réellement gouvernées, le repo peut progressivement dériver vers deux représentations concurrentes :

- la portée réellement exercée par les pipelines,
- la portée officiellement racontée par les registres.

### 4. Dérive outillage

La coexistence de patchers standard et versionnés sans doctrine parfaitement nette peut conduire à :

- des exécutions hétérogènes,
- des audits incohérents,
- une maintenance plus coûteuse des couches partagées.

### 5. Dérive sémantique du legacy

L’expression `Legacy active Core location` brouille la séparation fondamentale du repo.

Même si l’intention historique est compréhensible, le vocabulaire employé rapproche inutilement legacy et actif.

### 6. Dérive de qualité du pipeline governance lui-même

Un pipeline de gouvernance ne doit pas produire des entrées polluées ou partiellement ambiguës.

Le préfixe terminal parasite dans `repo_inventory.md` montre que la chaîne de scan n’est pas encore entièrement propre.

---

## Corrections à arbitrer

### ARB-01 — Nettoyage ou déplacement des `.bak` hors de `docs/registry/`

Décision à prendre :

- suppression,
- déplacement vers `legacy/`,
- ou stockage dans un espace de travail pipeline.

### ARB-02 — Mise à niveau de `docs/registry/pipelines.md`

À arbitrer :

- remplacement de la référence générique à `archive/` par une doctrine alignée sur `legacy/` ;
- extension explicite de la portée globale aux ressources réellement utilisées (`release-patch`, `docs/cores/releases/`, éventuellement `docs/architecture/` pour `governance`) ;
- repositionnement de `governance` dans la liste principale des pipelines.

### ARB-03 — Mise à niveau de `docs/registry/resources.md`

À arbitrer :

- correction des chemins legacy erronés ;
- intégration ou exclusion explicitée des patchers `v4` ;
- renommage de la section `Legacy active Core location` vers un libellé non ambigu.

### ARB-04 — Clarification de la doctrine outillage partagé

Question à trancher :

- quel outil est la référence par défaut ?
- quel outil est historique ?
- quelle version est normative pour les prochains pipelines ?

### ARB-05 — Assainissement du scan d’inventaire

Décision à prendre :

- corriger le mode de génération du `repo_inventory.md` pour supprimer les séquences de contrôle terminal ;
- garantir que l’entrée d’audit soit du Markdown propre et stable.

### ARB-06 — Normalisation verbale entre `README` et `operating_model`

Décision à prendre :

- conserver deux niveaux de langage complémentaires,
- ou réduire l’écart en alignant plus explicitement les termes de hiérarchie et de statut.

---

## Priorités

### Priorité 1 — Corriger la couche registry pour qu’elle reflète exactement le repo réel

Fichiers concernés :

- `docs/registry/pipelines.md`
- `docs/registry/resources.md`

Pourquoi :
Ce sont les documents les plus structurants pour la navigation humaine et IA.

### Priorité 2 — Retirer les ambiguïtés visibles de la couche autoritative

Fichiers concernés :

- `docs/registry/operating_model.md.bak`
- `docs/registry/resources.md.bak`

Pourquoi :
Une couche autoritative doit être exemplaire et sans doublons quasi canoniques.

### Priorité 3 — Clarifier la doctrine sur les patchers partagés

Fichiers concernés :

- `docs/registry/resources.md`
- `docs/pipelines/governance/pipeline.md`
- éventuellement `docs/patcher/shared/README.md`

Pourquoi :
L’outillage partagé ne doit laisser aucune hésitation sur l’exécutable ou la version à employer.

### Priorité 4 — Assainir l’entrée `repo_inventory.md`

Fichier concerné :

- `docs/pipelines/governance/work/01_scan/repo_inventory.md`

Pourquoi :
Le pipeline de gouvernance doit produire des intrants propres, sinon il affaiblit sa propre fiabilité.

### Priorité 5 — Harmoniser les formulations de gouvernance sans re-ouvrir l’architecture

Fichiers concernés :

- `docs/README.md`
- `docs/registry/operating_model.md`
- `docs/registry/conventions.md`

Pourquoi :
Le framework est déjà bien posé ; il s’agit maintenant de réduire les micro-zones grises, pas de refondre la structure.
