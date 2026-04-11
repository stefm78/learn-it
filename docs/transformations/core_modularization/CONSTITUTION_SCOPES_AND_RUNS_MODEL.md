# Constitution — modèle `scope catalog` + `run instances`

## Pourquoi ce document

Le premier pilote borné a montré une limite structurelle importante :
placer `scope_manifest.yaml`, `impact_bundle.yaml` et `integration_gate.yaml` à plat dans `docs/pipelines/constitution/inputs/` revient de fait à piloter **un seul scope actif à la fois**.

Ce document fixe donc le modèle cible exact pour `constitution` :

- des **scopes prédéfinis et versionnés** ;
- des **runs instanciés** à partir de ces scopes ;
- un layout compatible avec plusieurs runs parallèles ;
- une distinction explicite entre **définition de scope** et **instance de run**.

---

## Distinction structurante

### 1. Définition de scope
Une définition de scope décrit un périmètre logique stable du Core.

Exemples :
- `learner_state`
- `mastery_model`
- `knowledge_graph`
- `patch_governance`

Une définition de scope n'est **pas** encore un run.
C'est un objet de gouvernance réutilisable, versionné, régénérable.

### 2. Instance de run
Une instance de run est l'activation d'un scope pour un cycle donné.

Exemples :
- challenge borné ;
- arbitrage borné ;
- patch borné ;
- no-patch decision ;
- demande d'extension de scope.

Un run porte donc :
- un `run_id` ;
- un `scope_id` sélectionné ;
- des artefacts d'entrée matérialisés ;
- son propre `work/`, ses `reports/`, ses `outputs/`.

---

## Réponse de fond à la question de gouvernance

Oui, la bonne cible est bien la suivante :

1. les scopes doivent être **définis à partir de l'état courant gouverné** de la Constitution ;
2. ils doivent être **prédéfinis et versionnés** dans un catalogue ;
3. un challenge peut conduire à :
   - aucun changement de scope ;
   - un ajustement du scope concerné ;
   - une demande de redécoupage ;
4. après promotion d'une nouvelle version de la Constitution, le catalogue des scopes doit être **recalculé ou revalidé**.

Mais il faut ajouter une nuance importante :

**l'extraction de scopes doit être au moins hybride, pas aveuglément automatique.**

Pourquoi :
- certains regroupements sont structurels et facilement dérivables des IDs et dépendances ;
- d'autres relèvent d'une gouvernance sémantique ou pédagogique qui mérite validation humaine.

Conclusion :
- **extraction automatique assistée** comme mécanisme cible ;
- **validation/correction gouvernée** avant publication du catalogue.

---

## Modèle cible

### Couche A — catalogue de scopes
Le repo contient un catalogue versionné des scopes connus pour `constitution`.

Le catalogue est dérivé de :
- `docs/cores/current/constitution.yaml`
- et, si nécessaire pour les dépendances de lecture, de :
  - `docs/cores/current/referentiel.yaml`
  - `docs/cores/current/link.yaml`

Le catalogue décrit pour chaque scope :
- son périmètre nominal ;
- ses IDs principaux ;
- ses voisins logiques par défaut ;
- ses règles de lecture ;
- ses points de vigilance ;
- son origine de génération (`auto`, `hybrid`, `curated`).

### Couche B — runs instanciés
Chaque run matérialise :
- un scope choisi depuis le catalogue ;
- éventuellement des overrides bornés ;
- les artefacts d'entrée du run ;
- son espace de travail propre.

Cette séparation permet :
- plusieurs runs en parallèle ;
- plusieurs runs sur un même scope ;
- plusieurs runs sur des scopes différents ;
- une meilleure traçabilité.

---

## Layout exact cible

```text
 docs/pipelines/constitution/
   pipeline.md
   STAGE_07_RELEASE_MATERIALIZATION.md
   STAGE_08_PROMOTE_CURRENT.md

   scope_catalog/
     README.md
     manifest.yaml
     scope_definitions/
       learner_state.yaml
       mastery_model.yaml
       knowledge_graph.yaml
       patch_governance.yaml
       ...

   templates/
     scope_definition.template.yaml
     run_manifest.template.yaml

   runs/
     README.md
     CONSTITUTION_RUN_YYYY_MM_DD_<scope_key>_<R##>/
       run_manifest.yaml
       inputs/
         scope_manifest.yaml
         impact_bundle.yaml
         integration_gate.yaml
       work/
         01_challenge/
         02_arbitrage/
         03_patch/
         04_patch_validation/
         05_apply/
         06_core_validation/
         07_release/
       reports/
       outputs/
       archive/
```

---

## Rôle exact de chaque couche

### `scope_catalog/manifest.yaml`
Index du catalogue :
- version du catalogue ;
- fingerprint de la Constitution source ;
- liste des scopes publiés ;
- méthode d'extraction ;
- date de génération/validation.

### `scope_catalog/scope_definitions/*.yaml`
Définition stable d'un scope.
Ce n'est pas un run.

### `runs/<run_id>/run_manifest.yaml`
Carte d'identité du run :
- `run_id`
- `pipeline_id`
- `scope_id`
- source scope definition
- mode (`bounded_local_run`)
- état du run
- politique d'override
- liens vers les inputs, reports, outputs.

### `runs/<run_id>/inputs/scope_manifest.yaml`
Matérialisation d'exécution du scope pour ce run.
Il peut être strictement identique à la scope definition ou intégrer des overrides explicitement tracés.

### `runs/<run_id>/inputs/impact_bundle.yaml`
Voisinage logique matérialisé pour ce run précis.

### `runs/<run_id>/inputs/integration_gate.yaml`
Gate d'intégration spécifique au run.

---

## Qui génère quoi

### A. Génération du catalogue de scopes
Cible recommandée :
- générateur automatique ou semi-automatique ;
- validation humaine ou humaine+IA ;
- publication du catalogue dans `scope_catalog/`.

### B. Création d'un run
Un run est créé à partir :
- d'une scope definition publiée ;
- d'un `run_id` ;
- d'une éventuelle note de focalisation ;
- d'overrides explicites et bornés si nécessaires.

### C. Matérialisation des inputs de run
Les trois inputs ne devraient pas être saisis à la main à chaque fois en régime cible.
Ils devraient être **matérialisés automatiquement** à partir de :
- la scope definition ;
- la version active des artefacts canoniques ;
- une politique de gate par défaut ;
- des overrides validés s'il y en a.

Donc, oui :
- **les définitions de scope** doivent être extraites de l'état gouverné ;
- **les inputs de run** doivent idéalement être générés à partir de ces scopes.

---

## Cycle de vie recommandé

### Étape 1 — publier ou revalider le catalogue de scopes
Après promotion d'une nouvelle Constitution :
- recalculer ou revalider le catalogue de scopes ;
- publier `scope_catalog/manifest.yaml` ;
- publier les `scope_definitions/*.yaml`.

### Étape 2 — ouvrir un run
Créer :
- `runs/<run_id>/run_manifest.yaml`
- `runs/<run_id>/inputs/...`

### Étape 3 — exécuter le pipeline dans le répertoire de run
Le pipeline lit dans ce run :
- inputs ;
- work ;
- reports ;
- outputs.

### Étape 4 — intégrer globalement
Une fois le run local fini :
- relire le `integration_gate` ;
- arbitrer les collisions ou extensions de scope ;
- décider de l'intégration globale.

### Étape 5 — si une nouvelle release modifie la structure logique
Alors :
- régénérer ou ajuster les scope definitions ;
- republier le catalogue.

---

## Conséquence directe sur le parallélisme

Avec ce modèle :
- plusieurs runs peuvent exister en parallèle ;
- plusieurs challenges peuvent exister en parallèle ;
- plusieurs scopes peuvent être travaillés simultanément ;
- chaque run a son propre `work/01_challenge/`.

Donc la limite du layout plat disparaît.

Exemple :

```text
 docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01/
 docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_PATCH_GOVERNANCE_R01/
 docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_11_KNOWLEDGE_GRAPH_R01/
```

---

## Décision de design

La règle retenue pour `constitution` est donc :

**les scopes sont des objets catalogués et versionnés ; les runs sont des instances séparées de ces scopes.**

Les trois fichiers :
- `scope_manifest.yaml`
- `impact_bundle.yaml`
- `integration_gate.yaml`

ne doivent plus être pensés comme des fichiers globaux du pipeline, mais comme des **artefacts d'un run donné**.

---

## Strict nécessaire pour la prochaine étape

1. créer le layout `scope_catalog/` ;
2. créer le layout `runs/` ;
3. poser une première `scope_definition` pour `learner_state` ;
4. poser un premier `run_manifest.yaml` ;
5. déplacer conceptuellement le pilote actuel depuis `inputs/` vers `runs/<run_id>/inputs/`.

C'est la prochaine étape structurelle logique.
