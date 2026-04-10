# LAUNCH PROMPT — STAGE_03_FACTORY_PATCH_SYNTHESIS

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_03_FACTORY_PATCH_SYNTHESIS` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Inputs obligatoires

Source décisionnelle principale :
- `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`

Artefacts gouvernés à patcher :
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Socle canonique de contrôle :
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

Contexte d'exécution :
- `docs/pipelines/platform_factory/pipeline.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- éventuellement une note de focalisation patch dans `docs/pipelines/platform_factory/inputs/`

## Contexte d'exécution obligatoire

- `platform_factory_arbitrage.md` est la source de vérité du stage.
- Les challenge reports historiques peuvent être relus si nécessaire pour traçabilité, mais ils ne doivent pas supplanter l'arbitrage final.
- Le résultat attendu doit être écrit dans le repo, dans le fichier YAML de sortie imposé ci-dessous.
- Il ne faut pas considérer qu'une réponse dans le chat suffit à accomplir la tâche.
- Le but est de produire un patchset exploitable au Stage 04, pas de réouvrir l'arbitrage.

## Fichier de sortie obligatoire

Écrire exactement un fichier dans le repo :
- `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`

## Ordre de lecture obligatoire

1. `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`
2. `docs/cores/current/constitution.yaml`
3. `docs/cores/current/referentiel.yaml`
4. `docs/cores/current/link.yaml`
5. `docs/cores/current/platform_factory_architecture.yaml`
6. `docs/cores/current/platform_factory_state.yaml`
7. `docs/pipelines/platform_factory/pipeline.md`
8. `docs/prompts/shared/Make22PlatformFactoryPatch.md`
9. éventuellement la note de focalisation patch

## Objectif exact

Produire directement le patchset YAML final du stage, sous forme d'un fichier :
- borné
- traçable
- cohérent avec l'arbitrage final
- sans réouverture des décisions
- sans mélange illégitime entre :
  - architecture
  - state
  - pipeline
  - validator/tooling
  - manifest/release governance

## Exigences de contenu

Le patchset doit :
- ne contenir que des changements supportés explicitement par `platform_factory_arbitrage.md`
- exclure explicitement les sujets :
  - rejetés
  - différés
  - hors périmètre
  - relevant d'un validator/tooling plutôt que du canonique
  - relevant du pipeline plutôt que du canonique
  - relevant de la gouvernance release/manifest plutôt que du canonique
  - nécessitant encore une clarification humaine
- préserver strictement la séparation entre :
  - `platform_factory_architecture.yaml`
  - `platform_factory_state.yaml`
- rester proportionné à une baseline V0 déjà released
- être directement exploitable au Stage 04 de validation

## Règles de synthèse obligatoires

Pour chaque changement inclus dans le patchset, il faut pouvoir retrouver implicitement ou explicitement :
- la source décisionnelle dans `platform_factory_arbitrage.md`
- l'artefact cible principal
- la localisation probable
- le type d'opération attendu
- l'effet recherché
- le risque évité

Si un sujet est ambigu ou insuffisamment arbitré :
- ne pas improviser
- ne pas l'ajouter au patchset
- le laisser hors du patchset courant

## Contraintes

- Ne pas réouvrir l'arbitrage.
- Ne pas produire une simple analyse markdown à la place du YAML attendu.
- Ne pas écrire plusieurs fichiers.
- Ne pas modifier `docs/cores/current/` directement.
- Ne pas introduire un besoin de patch non arbitré.
- Ne pas faire porter au canonique ce qui relève d'un validator, du pipeline ou de la gouvernance de release.
- Le livrable attendu est le fichier YAML écrit dans le repo. Le retour chat doit être très succinct.

---

## CONTRAINTES DSL OBLIGATOIRES — ops et paths

> Ces contraintes sont non négociables. Tout patchset qui les viole sera rejeté en STAGE_04
> (check-paths) ou en STAGE_05 (dry-run).

### Opérations atomiques supportées

Le script `apply_platform_factory_patchset.py` supporte exactement ces `op` :

| op | Cible attendue | Comportement |
|---|---|---|
| `add` | Clé absente → crée la clé. Clé existante liste → appende. | FAIL si la clé existe et n'est pas une liste |
| `replace` | Clé existante ou absente → écrase/crée | Toujours sûr |
| `update` | Identique à `replace` | Toujours sûr |
| `remove` | Clé de mapping uniquement | FAIL si path non résolvable ; WARN si clé absente |
| `list_remove_item` | Liste de strings — retire un item par valeur exacte | WARN si absent |
| `list_remove_mapping` | Liste de mappings — retire un mapping par clé discriminante | WARN si absent |
| `list_replace_mapping` | Liste de mappings — remplace un mapping par clé discriminante | FAIL si absent |

### Syntaxe des paths

- Séparateur : **point `.`** uniquement.
- Les paths sont résolus depuis le **bloc racine canonique** du document (ex. depuis `PLATFORM_FACTORY_ARCHITECTURE`, pas depuis la racine absolue du YAML).
- **Interdit** : index entre crochets (`[capability_id=...]`, `[0]`, etc.) — le script ne les interprète pas.
- **Interdit** : path vers un item d'une liste de mappings sans utiliser `list_remove_mapping` ou `list_replace_mapping`.

### Règles par type d'opération

#### Pour `add` sur une liste
- S'assurer que la cible est bien une **liste** dans l'artefact source.
- Si la clé n'existe pas encore, elle sera créée avec la valeur comme valeur directe (pas une liste). Si l'intention est de créer une liste, utiliser `replace` avec une liste complète.
- Si on veut ajouter plusieurs items indépendants à la même liste, déclarer autant d'opérations `add` distinctes.

#### Pour `remove` sur un item de liste
- **Ne jamais utiliser `remove` pour supprimer un item d'une liste** (strings ou mappings).
- Utiliser `list_remove_item` (strings) ou `list_remove_mapping` (mappings).
- Ou utiliser `replace` sur la liste entière avec la valeur cible (liste sans l'item).

#### Pour `replace` sur une liste entière
- Déclarer la liste complète attendue après patch dans `value`.
- Lire l'artefact source pour connaître les items existants avant de produire la liste.

#### Pour `list_remove_mapping` et `list_replace_mapping`
- Déclarer `match_key` : la clé discriminante dans chaque mapping (ex. `capability_id`).
- Déclarer `match_value` : la valeur discriminante.
- Pour `list_replace_mapping`, déclarer `value` : le mapping complet de remplacement.

### Exemples conformes

```yaml
# Ajouter un item à une liste de strings existante
- op: add
  path: contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes
  value: runtime_policy_conformance

# Retirer un item d'une liste de strings
- op: list_remove_item
  path: open_points_for_challenge
  value: exact_location_of_validated_derived_execution_projections

# Retirer un mapping d'une liste par clé discriminante
- op: list_remove_mapping
  path: capabilities_present
  match_key: capability_id
  match_value: PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED

# Remplacer un mapping dans une liste par clé discriminante
- op: list_replace_mapping
  path: capabilities_present
  match_key: capability_id
  match_value: PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED
  value:
    capability_id: PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED
    description: >-
      L'intention de pipeline platform_factory est explicitement posée
      (intent only, not yet tooled execution framework).

# Ajouter un mapping à une liste de mappings existante
- op: add
  path: capabilities_partial
  value:
    capability_id: PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED
    description: >-
      La règle d'usage des projections dérivées est définie. ...
```

---

## Structure attendue du fichier YAML

Produire un patchset YAML structuré, directement exploitable au stage suivant.

Le patchset doit au minimum :
- identifier clairement le patchset
- déclarer les fichiers cibles
- décrire des opérations suffisamment atomiques
- permettre de comprendre sans ambiguïté :
  - quoi changer
  - où
  - pourquoi
  - dans quel ordre si nécessaire

## Résultat terminal attendu

À la fin de l'exécution, afficher uniquement :
1. le chemin exact du fichier écrit
2. un résumé ultra-court
