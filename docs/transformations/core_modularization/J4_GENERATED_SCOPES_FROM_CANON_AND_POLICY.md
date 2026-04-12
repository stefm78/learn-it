# J4 — scopes générés à partir du canon et de fichiers de politique

## Décision structurante

Le chantier adopte explicitement le modèle suivant :

**les `scope_definitions/*.yaml` doivent être des artefacts générés, et non des fichiers source maintenus manuellement.**

La chaîne cible devient donc :

1. **Core canoniques gouvernés**
2. **fichiers de politique et de décision**
3. **génération déterministe des scopes**
4. **matérialisation des runs**
5. **intégration globale**
6. **reconstruction canonique déterministe**

---

## Pourquoi cette décision

Si les scopes restent édités manuellement, la modularisation conserve une zone grise importante :
- le découpage logique peut dériver du canon sans trace explicite ;
- deux IA ou deux opérateurs peuvent faire évoluer les scopes différemment ;
- la régénération après évolution du canon devient fragile ;
- la reconstruction bidirectionnelle perd sa symétrie.

À l'inverse, si les scopes sont générés :
- le processus devient rejouable ;
- les arbitrages humains deviennent des entrées gouvernées ;
- les changements de canon peuvent déclencher un recalcul contrôlé ;
- le modèle aller-retour gagne en cohérence.

---

## Nouvelle architecture cible

### A. Sources de vérité publiées
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

### B. Politique de découpage et de lecture
Des fichiers déclaratifs versionnés portent :
- les règles de partition ;
- les règles de fermeture des dépendances ;
- les exceptions de voisinage ;
- les bindings critiques à relire ;
- les décisions d'arbitrage humain normalisées.

### C. Générateur déterministe de scopes
Le générateur lit :
- le canon courant ;
- les fichiers de politique ;
- les fichiers de décision normalisés.

Il produit :
- `scope_catalog/manifest.yaml`
- `scope_catalog/scope_definitions/*.yaml`
- fingerprints et rapports éventuels.

### D. Runs générés à partir des scopes
Les runs ne définissent plus les scopes.
Ils consomment les scopes générés.

---

## Distinction structurante

Il faut maintenant séparer quatre couches.

### 1. Canon
Le canon reste la vérité publiée.

### 2. Politique
La politique dit comment dériver les scopes.

### 3. Scopes générés
Les scopes sont des sorties déterministes dérivées du canon et de la politique.

### 4. Runs
Les runs consomment ces scopes générés dans un cycle d'exécution borné.

---

## Rôle exact des arbitrages humains

Les arbitrages humains restent légitimes, mais ils ne doivent pas rester implicites.

Le principe retenu est :

**tout arbitrage humain qui influence le découpage, la lecture, l'intégration ou la reconstruction doit être matérialisé dans un fichier de paramètre versionné.**

La conversation avec une IA peut :
- préparer l'analyse ;
- challenger les options ;
- expliciter les conséquences ;

mais la sortie retenue doit devenir une donnée structurée.

---

## Types de fichiers de gouvernance attendus

### A. Fichier de politique durable
Contient les règles stables ou semi-stables :
- règles d'assignation des IDs à des scopes ;
- règles de voisinage logique ;
- règles de lecture primaire ;
- règles de fallback ;
- règles de partition inter-scope.

### B. Fichier de décisions d'arbitrage
Contient les décisions humaines explicites qui complètent la politique :
- exceptions de partition ;
- exceptions de dépendance ;
- regroupements imposés ;
- exclusions imposées ;
- priorités de résolution de collisions.

Ces décisions doivent être elles-mêmes structurées, identifiées, et versionnées.

---

## Ce qui doit être déterministe

Doivent être calculés de manière déterministe :
- l'extraction des IDs ;
- la fermeture des dépendances ;
- le regroupement selon les règles ;
- la génération des scopes ;
- la matérialisation des plans de lecture ;
- l'ordre de sérialisation ;
- le fingerprint du résultat.

Doivent être fournis comme entrées gouvernées :
- les règles de partition sémantique non déductibles du canon seul ;
- les exceptions humaines ;
- les politiques transverses de lecture ou de merge.

---

## Forme cible minimale des fichiers de politique

Sans figer définitivement le schéma, la cible minimale est la suivante :

### `scope_generation_policy.yaml`
Doit pouvoir exprimer :
- `scope_partition_rules`
- `dependency_closure_rules`
- `primary_read_rules`
- `fallback_read_rules`
- `cross_scope_boundary_rules`
- `serialization_policy`

### `scope_generation_decisions.yaml`
Doit pouvoir exprimer :
- `decision_id`
- `status`
- `scope_keys_affected`
- `target_ids` ou `target_patterns`
- `decision_type`
- `decision_payload`
- `justification`
- `applies_from`

---

## Conséquence sur le catalogue de scopes

Le `scope_catalog/manifest.yaml` et les `scope_definitions/*.yaml` ne doivent plus être pensés comme la politique source.

Ils doivent être pensés comme :
- **artefacts générés** ;
- régénérables ;
- comparables ;
- revalidables après changement du canon ou des règles.

Donc, si le canon ou la politique change :
- le catalogue doit être recalculé ;
- le diff de génération doit devenir observable ;
- la publication du catalogue doit rester explicite.

---

## Conséquence sur la reconstruction canonique

Cette décision renforce J3 :
- si les scopes sont générés à partir du canon et de la politique ;
- et si le canon est reconstruit à partir de résultats intégrés ;

alors la chaîne devient réellement bidirectionnelle et gouvernée par données.

Le système cible n'est donc plus :
- canon -> scopes manuels -> runs -> patchs -> canon

mais :
- canon -> politique + décisions -> scopes générés -> runs -> résultats intégrés -> canon reconstruit

---

## Strict nécessaire recommandé

1. Poser le principe : scopes générés = oui.
2. Définir les fichiers de politique et de décisions.
3. Introduire un générateur déterministe comme cible explicite.
4. Éviter toute maintenance manuelle durable des `scope_definitions/*.yaml`.
5. Garder les artefacts déjà présents comme bootstrap transitoire tant que le générateur n'est pas branché.

---

## Proposition de séquence d'implémentation

### Étape 1 — niveau transformation
Documenter le modèle `generated scopes` et les fichiers d'entrée gouvernés.

### Étape 2 — niveau templates
Créer :
- un template de politique de génération ;
- un template de décisions d'arbitrage ;
- éventuellement un template de rapport de génération.

### Étape 3 — niveau outillage
Créer un générateur déterministe capable de lire :
- le canon ;
- les règles ;
- les décisions.

Puis de produire :
- le manifeste de catalogue ;
- les scope definitions ;
- un fingerprint ;
- un rapport.

### Étape 4 — niveau migration
Faire passer progressivement les scopes bootstrap existants sous régime généré.

---

## Garde-fous

1. Les scopes générés ne deviennent pas une seconde source de vérité.
2. La politique et les décisions doivent être lisibles, auditables et versionnées.
3. Le générateur ne doit pas cacher d'arbitrage implicite dans son code.
4. Toute décision humaine significative doit être externalisée dans des fichiers d'entrée.
5. La chaîne doit rester compréhensible et rejouable par une autre IA ou un autre opérateur.

---

## Décision structurante de J4

Le chantier adopte la règle suivante :

**les scopes sont des sorties générées de manière déterministe à partir du canon courant et de fichiers de politique/décision versionnés ; ils ne doivent plus constituer à terme une couche éditoriale maintenue manuellement.**
