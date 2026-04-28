# J2 — réduction de la surface de lecture effective

## Objet

J1 a défini le contrat minimal d'un run borné :
- `scope_manifest`
- `impact_bundle`
- `integration_gate`

Le modèle `scope catalog + run instances` a ensuite clarifié le périmètre gouverné et la séparation entre définition de scope et instance de run.

Mais une limite structurelle reste ouverte :

**les scopes réduisent déjà le droit d'action, mais pas encore assez le payload documentaire réellement relu par une IA.**

Ce document définit donc le prochain incrément minimal de modularisation :

**passer d'un modèle principalement `files-first` à un modèle de lecture plus fin, sans casser la traçabilité vers les artefacts canoniques.**

---

## Problème exact

Aujourd'hui, un scope peut déjà :
- borner les fichiers modifiables ;
- borner les modules et IDs principaux ;
- imposer un voisinage logique ;
- distinguer `in_scope`, `out_of_scope_but_relevant` et `needs_scope_extension`.

Mais si le modèle continue à dire implicitement :
- lire `constitution.yaml` complet ;
- lire `referentiel.yaml` complet ;
- lire `link.yaml` complet ;

alors le gain de contexte reste partiel.

Le chantier de modularisation ne doit donc pas seulement améliorer la gouvernance des scopes.
Il doit aussi améliorer la **granularité de lecture**.

---

## Distinction structurante

Il faut désormais séparer explicitement trois notions.

### 1. Provenance canonique
Répond à la question :
- d'où ce scope est-il dérivé ?

Cette notion peut rester large.
Par exemple :
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

### 2. Périmètre d'écriture autorisé
Répond à la question :
- que le run a-t-il le droit de modifier ?

Cette notion est gouvernée par :
- `scope_manifest`

### 3. Surface de lecture effective
Répond à la question :
- que faut-il vraiment relire pour travailler sûrement avec un coût de contexte minimal ?

Cette notion doit devenir beaucoup plus fine que la simple liste de fichiers complets.

---

## Décision de design

La transformation adopte la règle suivante :

**`source_artifacts` reste un champ de provenance ; la réduction réelle de contexte doit être portée par un contrat de lecture plus fin.**

Autrement dit :
- on ne commence pas par réduire artificiellement `source_artifacts` ;
- on introduit un niveau de lecture plus précis pour les scopes et les runs.

---

## Cible J2

La cible minimale de J2 est un régime **ids-first** ou **projection-first**.

### Option A — ids-first
Le scope est lu principalement via :
- ses `target.ids`
- les `logical_neighbors_to_read.ids`
- les invariants et bindings critiques nécessaires

Les fichiers complets deviennent un **fallback** ou une **trace de provenance**, pas l'unité normale de lecture.

### Option B — projection-first
Le scope est lu via une projection dérivée minimale et stable :
- projection par module ;
- projection par famille d'IDs ;
- projection par bundle d'extraits validés.

Les fichiers canoniques restent la source de vérité, mais le payload opérationnel devient plus compact.

### Option C — hybride recommandé à ce stade
Pour le strict nécessaire, la meilleure cible intermédiaire est :
- provenance canonique complète conservée ;
- IDs comme unité primaire de lecture ;
- fichiers complets conservés comme fallback ;
- projections minimales introduites plus tard si le besoin est confirmé.

---

## Conséquence sur les `scope_definitions`

Les `scope_definitions/*.yaml` devraient évoluer progressivement pour distinguer :

### A. Ce qui décrit la provenance
Exemple :
- `source_artifacts`

### B. Ce qui décrit la cible gouvernée
Exemple :
- `target.files`
- `target.modules`
- `target.ids`

### C. Ce qui décrit la lecture minimale recommandée
Nouveau niveau à introduire, par exemple :
- `primary_read_units.ids`
- `primary_read_units.invariants`
- `primary_read_units.bindings`
- `fallback_read_files`
- `projection_policy`

L'idée n'est pas encore de figer le nom exact du champ.
L'idée est de rendre explicite la différence entre :
- ce qui fonde le scope ;
- ce qui est modifiable ;
- ce qui doit être relu de manière minimale.

---

## Conséquence sur les runs

Le `impact_bundle` d'un run ne devrait plus seulement lister des fichiers voisins.

Il devrait devenir la matérialisation d'un **plan de lecture minimal** pour le run.

Exemples de contenu cible :
- IDs principaux à relire ;
- voisins logiques par ID ;
- invariants transverses ;
- bindings inter-Core critiques ;
- fichiers fallback si une ambiguïté ou un conflit apparaît.

Cela permettrait :
- un challenge plus léger ;
- un arbitrage plus ciblé ;
- moins de dépendance à une relecture large des trois Core ;
- une meilleure reproductibilité entre IA.

---

## Strict nécessaire recommandé

J2 ne doit pas lancer une refonte complète des artefacts.

Le strict nécessaire recommandé est :

1. **Clarifier le modèle**
   - provenance ≠ écriture ≠ lecture minimale.

2. **Ajouter un contrat de lecture fine**
   - d'abord dans les documents de transformation ;
   - ensuite dans le catalogue de scopes ;
   - puis dans la matérialisation des runs.

3. **Conserver une voie de repli**
   - les fichiers complets restent relisibles en fallback ;
   - aucune perte de traçabilité vers le canon.

4. **Tester sur `constitution` avant généralisation**
   - d'abord `learner_state` ;
   - ensuite éventuellement `mastery_model`.

---

## Proposition de séquence d'implémentation

### Étape 1 — niveau transformation
Documenter le contrat de lecture fine dans `docs/transformations/core_modularization/`.

### Étape 2 — niveau catalogue
Faire évoluer un ou deux scopes `constitution` pour qu'ils déclarent explicitement :
- provenance canonique ;
- cible gouvernée ;
- lecture primaire par IDs ;
- fallback par fichiers.

### Étape 3 — niveau run
Faire évoluer la matérialisation du `impact_bundle` pour un run pilote afin qu'il embarque un vrai plan de lecture minimal.

### Étape 4 — niveau pipeline
Adapter le startup/run protocol pour encourager ce niveau de lecture plus fin avant relecture large.

---

## Bénéfices attendus

1. Réduction réelle du coût de contexte.
2. Meilleure reproductibilité inter-IA.
3. Meilleure séparation entre gouvernance et payload opérationnel.
4. Préparation d'un futur régime de projections dérivées validées.

---

## Garde-fous

1. Les scopes ne deviennent pas une seconde source de vérité.
2. Le canon publié reste dans `docs/cores/current/` tant que la chaîne de compilation n'est pas validée.
3. Une lecture fine ne doit jamais masquer une dépendance critique inter-Core.
4. Les fichiers complets restent disponibles comme fallback explicite.
5. Le modèle doit rester compréhensible et exploitable par une IA sans contexte implicite de conversation.

---

## Décision structurante de J2

Le chantier adopte la règle suivante :

**la prochaine vraie marche de modularisation n'est pas de changer la provenance des scopes, mais de réduire explicitement la surface de lecture effective des runs bornés.**

C'est cette réduction qui permettra de passer d'une gouvernance bornée à une exécution réellement plus légère et plus parallèle.
