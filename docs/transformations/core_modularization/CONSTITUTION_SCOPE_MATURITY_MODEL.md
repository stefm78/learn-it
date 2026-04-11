# Constitution — modèle de maturité des scopes

## Pourquoi ce document

Une fois qu'un catalogue de scopes existe, il apparaît un nouveau risque :

- certains scopes sont très bien découpés, bien bornés et bien reliés ;
- d'autres sont flous, déséquilibrés ou trop dépendants d'un voisinage implicite.

Sans modèle de maturité, le catalogue risque donc de dériver progressivement vers des scopes de qualité inégale.

Ce document définit un **scoring de maturité des scopes** afin de :
- comparer les scopes entre eux ;
- détecter les scopes trop fragiles avant de les utiliser ;
- guider les ajustements après challenge ;
- homogénéiser le catalogue au fil des releases.

---

## Position de design

Le scoring de maturité d'un scope ne remplace pas son contenu.

Il sert à qualifier :
- la qualité du découpage ;
- la netteté des frontières ;
- la qualité des dépendances ;
- la capacité du scope à supporter un run borné sûr.

Donc, oui :
- les scopes doivent être prédéfinis ;
- leur définition doit être revalidée après évolution de la Constitution ;
- et ils doivent porter un **signal de maturité** comparable d'un scope à l'autre.

---

## Où placer ce scoring

Le scoring doit exister à deux niveaux :

### 1. Niveau scope individuel
Chaque `scope_definition` porte son propre bloc `maturity`.

### 2. Niveau catalogue
Le `scope_catalog/manifest.yaml` doit agréger :
- la liste des scopes ;
- leur score global ;
- leur niveau ;
- les scopes sous le seuil minimal de publication.

---

## Axes de maturité

Chaque scope est évalué sur 6 axes.

### A1 — Clarté du périmètre
Question : le scope est-il clairement borné ?

Score :
- 0 = périmètre flou ou implicite
- 1 = périmètre partiellement exprimé
- 2 = périmètre lisible mais avec ambiguïtés
- 3 = périmètre clair
- 4 = périmètre très clair et stable

### A2 — Cohérence interne
Question : les éléments du scope vont-ils naturellement ensemble ?

Score :
- 0 = agrégat artificiel
- 1 = regroupement fragile
- 2 = cohérence moyenne
- 3 = bonne cohérence
- 4 = très forte cohérence logique

### A3 — Frontières inter-scope
Question : la frontière avec les scopes voisins est-elle nette ?

Score :
- 0 = frontières très confuses
- 1 = nombreux recouvrements implicites
- 2 = séparation partielle
- 3 = séparation claire avec quelques points de vigilance
- 4 = séparation très propre

### A4 — Dépendances explicites
Question : les dépendances amont/aval et cross-core sont-elles explicites et lisibles ?

Score :
- 0 = dépendances surtout implicites
- 1 = dépendances critiques incomplètes
- 2 = dépendances partiellement visibles
- 3 = dépendances bien explicitées
- 4 = dépendances très bien cartographiées

### A5 — Exécutabilité en run borné
Question : peut-on raisonnablement lancer un challenge/arbitrage/patch borné sur ce scope sans dérive immédiate ?

Score :
- 0 = run borné non viable
- 1 = run très risqué
- 2 = run possible mais fragile
- 3 = run borné viable
- 4 = run borné robuste

### A6 — Stabilité inter-release
Question : le scope reste-t-il globalement stable à travers les releases, ou change-t-il trop souvent de forme ?

Score :
- 0 = instable
- 1 = très mouvant
- 2 = stabilité moyenne
- 3 = plutôt stable
- 4 = stable et réutilisable

---

## Score global

Score global recommandé :
- somme des 6 axes, donc total sur 24.

Niveaux :
- `L0_experimental` : 0–8
- `L1_fragile` : 9–12
- `L2_usable_with_care` : 13–16
- `L3_operational` : 17–20
- `L4_strong` : 21–24

---

## Règles d'usage

### Publication dans le catalogue
- un scope peut exister à tout niveau ;
- mais un scope ne devrait pas être recommandé pour runs parallèles répétés s'il est sous `L2_usable_with_care`.

### Préparation d'un run
- si un scope est `L0_experimental` ou `L1_fragile`, le `run_manifest` doit le signaler explicitement ;
- le `integration_gate` doit être plus strict pour ces scopes.

### Révision post-challenge
Après un challenge, l'une des issues possibles est :
- scope confirmé ;
- scope ajusté ;
- scope scindé ;
- scope fusionné ;
- scope à redéfinir.

Le scoring de maturité doit être réévalué dans tous ces cas.

---

## Qui produit le score

Cible recommandée :
- pré-score automatique ou semi-automatique ;
- validation ou correction gouvernée ;
- publication du score validé avec le scope.

Cela évite :
- les écarts invisibles entre scopes ;
- les scopes pseudo-propres mais difficilement exécutables ;
- l'ouverture de runs sur des périmètres mal définis.

---

## Position sur le pipeline

Le `scope_definition` ne doit pas être un sous-produit improvisé d'un challenge borné.

Il doit appartenir à un cycle distinct :
- soit un **pré-stage** de publication du catalogue de scopes ;
- soit un cycle compagnon exécuté après promotion d'une nouvelle release ;
- soit un pipeline dédié de `scope catalog refresh`.

Autrement dit :
- le challenge borné consomme normalement un scope publié ;
- il peut recommander d'ajuster un scope ;
- mais la redéfinition officielle du scope revient à la couche catalogue.

---

## Décision de design

Pour `constitution`, la règle retenue est :

**un scope publié doit porter un score de maturité explicite ; le catalogue doit agréger ces scores ; et les runs doivent consommer des scopes catalogués, pas inventer silencieusement leur propre périmètre.**
