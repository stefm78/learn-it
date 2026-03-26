Oui, et votre intuition est bonne : **si on fait un runner spécifique par pipeline, ça va devenir lourd**.

La bonne approche n’est pas :

* `run_governance.py`
* `run_release.py`
* `run_constitution.py`
* etc.

La bonne approche est plutôt :

* un **runner générique de pipeline**
* un **contrat standard** pour tous les pipelines
* et un `state.yaml` piloté de façon uniforme

Voici un markdown prêt à enregistrer, par exemple sous :

`docs/architecture/Pipeline_Runtime_Model.md`

---

# Pipeline Runtime Model

## Objectif

Ce document spécifie le modèle d’exécution des pipelines du repo Learn-it.

Il ne décrit pas le contenu métier des pipelines.
Il décrit comment les pipelines doivent être **pilotés**, **observés** et **maintenus**.

## Problème

Le repo contient plusieurs pipelines :
- `constitution`
- `release`
- `migration`
- `governance`
- et potentiellement d’autres à venir

Si chaque pipeline reçoit :
- son propre script d’exécution
- sa propre logique de transition
- sa propre manière de gérer `state.yaml`

alors le système devient :
- lourd
- difficile à maintenir
- incohérent
- fragile lors de l’ajout de nouveaux pipelines

## Principe directeur

Le repo ne doit pas multiplier les runners spécifiques.

Le modèle cible est :

- **un runner générique**
- **des pipelines décrits par convention**
- **un état standardisé**
- **des artefacts produits dans des emplacements prévisibles**

## Décision d’architecture

### À éviter
- un script d’orchestration différent par pipeline
- une logique d’état différente selon le pipeline
- des transitions implicites
- des scripts ad hoc non documentés

### À privilégier
- un **runner générique** du type :
  - `docs/patcher/shared/run_pipeline.py`
- des pipelines qui suivent un contrat commun
- un `state.yaml` standard
- une détection uniforme des artefacts à appliquer

## Contrat minimal d’un pipeline

Chaque pipeline actif doit contenir au minimum :

- `pipeline.md`
- `state.yaml`

Et peut contenir :

- `inputs/`
- `outputs/`
- `reports/`
- `work/01_*`
- `work/02_*`
- `work/03_*`
- etc.

## Contrat du runner générique

Le runner générique doit pouvoir :

1. charger un pipeline à partir de son dossier
2. lire son `state.yaml`
3. déterminer le stage courant ou le prochain stage
4. détecter les artefacts présents dans `work/`
5. choisir automatiquement le bon moteur d’exécution
6. écrire les rapports au bon endroit
7. mettre à jour `state.yaml`
8. signaler proprement les erreurs

## Règle importante

### `state.yaml` n’est pas un document décoratif

Il doit être considéré comme le **journal minimal d’orchestration** du pipeline.

### `state.yaml` est géré uniquement par le runner

Les prompts :
- produisent des artefacts
- n’écrivent pas dans `state.yaml`

Les patchers :
- appliquent des patchs
- n’orchestrent pas le pipeline

Le seul composant autorisé à maintenir `state.yaml` est le runner de pipeline.

## Modèle cible : runner générique

Le modèle recommandé est :

- `docs/patcher/shared/run_pipeline.py`

Ce runner doit être capable de traiter plusieurs pipelines via une logique commune.

## Pourquoi un runner générique ?

Parce que la variabilité entre pipelines doit rester faible.

Ce qui change d’un pipeline à l’autre :
- les prompts utilisés
- les stages présents
- les types d’artefacts produits
- les chemins de staging

Ce qui ne doit pas changer :
- la logique de lecture d’état
- les transitions de stage
- l’écriture des rapports
- la gestion des erreurs
- la mise à jour de `state.yaml`

## Standardisation du `state.yaml`

Format minimal recommandé :

```yaml
pipeline_id: governance
version: 1

current_run_id: null
status: idle
current_stage: null
last_successful_stage: null

mode: null
started_at: null
updated_at: null
finished_at: null

active_inputs: []
active_outputs: []
active_reports: []

detected_artifact_type: null
selected_input_file: null
selected_validation_file: null
selected_execution_report: null

last_error: null
notes: []
````

## Statuts normalisés

Les statuts autorisés doivent être limités et partagés :

* `idle`
* `running`
* `waiting_for_input`
* `validated`
* `applied`
* `failed`
* `completed`

## Règle

Aucun pipeline ne doit inventer ses propres statuts sans extension explicitement documentée.

## Stages normalisés

Les stages peuvent varier, mais ils doivent être identifiables de manière uniforme.

Convention recommandée :

* `01_scan`
* `02_audit`
* `03_arbitrage`
* `04_patch`
* `05_validation`
* `06_apply`
* `07_review`

Tous les pipelines n’ont pas besoin de tous les stages.
Mais les noms doivent rester lisibles et compatibles avec la logique du runner.

## Détection des artefacts

Le runner doit pouvoir détecter automatiquement des artefacts connus.

### Exemples

#### Patch standard

* `PATCH_SET`
* moteur :

  * `validate_patchset.py`
  * `apply_patch.py`

#### Release patch

* `RELEASE_PATCH_SET`
* moteur :

  * `validate_release_patch.py`
  * `apply_release_patch.py`

#### Artefact absent

* statut :

  * `waiting_for_input`

## Règle de dispatch

Le dispatch ne doit pas être codé “en dur” pipeline par pipeline.

Il doit être basé sur :

* le type d’artefact détecté
* les conventions du pipeline
* les outils canoniques de `docs/patcher/shared/`

## Interface recommandée du runner

Exemples de commandes possibles :

```bash
python docs/patcher/shared/run_pipeline.py --pipeline governance
python docs/patcher/shared/run_pipeline.py --pipeline governance --stage 05_validation
python docs/patcher/shared/run_pipeline.py --pipeline release --whatif
```

## Comportement attendu

Le runner :

1. charge `docs/pipelines/<pipeline>/state.yaml`
2. identifie le contexte courant
3. détecte les artefacts dans `work/`
4. sélectionne le moteur adapté
5. exécute
6. écrit les résultats dans :

   * `work/`
   * `reports/`
7. met à jour `state.yaml`

## Exemple de transitions

### Avant validation

```yaml
status: running
current_stage: 05_validation
updated_at: "..."
```

### Si validation réussie

```yaml
status: validated
last_successful_stage: 05_validation
selected_validation_file: docs/pipelines/governance/work/05_validation/...
updated_at: "..."
```

### Avant application

```yaml
status: running
current_stage: 06_apply
updated_at: "..."
```

### Si application réussie

```yaml
status: applied
last_successful_stage: 06_apply
selected_execution_report: docs/pipelines/governance/reports/...
updated_at: "..."
```

### En cas d’échec

```yaml
status: failed
last_error: "..."
updated_at: "..."
```

## Limites à poser dès maintenant

Le runner ne doit pas :

* générer de contenu métier
* arbitrer seul
* modifier un Core sans patch explicite
* inventer des fichiers cibles
* promouvoir un artefact hors du pipeline prévu

Il doit :

* exécuter
* tracer
* mettre à jour l’état
* et s’arrêter proprement si le contexte est insuffisant

## Pourquoi cette approche est plus maintenable

### Avec un runner spécifique par pipeline

Vous obtenez :

* duplication
* divergence
* maintenance multiple
* comportement incohérent

### Avec un runner générique

Vous obtenez :

* une seule logique d’orchestration
* une seule convention d’état
* un coût marginal faible quand on ajoute un pipeline
* un repo plus lisible pour une IA et pour un humain

## Recommandation de mise en œuvre

### Étape 1

Ne pas implémenter immédiatement tous les cas.

### Étape 2

Concevoir le runner comme **générique dès le départ**.

### Étape 3

Commencer par l’utiliser sur `governance`.

### Étape 4

Étendre ensuite à `release`, puis éventuellement à `constitution`.

## Règle de sobriété

Un pipeline ne doit devenir “smart” qu’à travers :

* ses prompts
* ses artefacts
* ses specs

Le runner, lui, doit rester :

* simple
* prévisible
* standardisé
* peu spécifique métier

## Conclusion

Le bon renforcement n’est pas d’ajouter un nouveau script spécifique à chaque pipeline.

Le bon renforcement est :

* un **modèle runtime commun**
* un **runner générique**
* un **`state.yaml` standard**
* une **logique de dispatch par type d’artefact**

C’est cette approche qui permettra au repo de rester maintenable quand le nombre de pipelines augmentera.

```

## Mon avis net

Oui, votre inquiétude est justifiée.  
Et justement, ce markdown doit servir à **éviter** que le système devienne trop lourd.

La bonne suite n’est pas :
- “faire tout de suite un gros runner governance”

La bonne suite est :
- **figer le modèle runtime**
- puis implémenter plus tard **un runner générique**, pas un runner par pipeline.

Si vous voulez, je peux maintenant vous proposer aussi un deuxième fichier plus court, du type :

- `docs/architecture/Runner_Requirements.md`

qui résume uniquement les exigences techniques du futur runner.
```
