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

Contexte d'exécution et outillage obligatoire :
- `docs/pipelines/platform_factory/pipeline.md`
- `docs/prompts/shared/Make22PlatformFactoryPatch.md`
- `docs/patcher/shared/patchset_schema_reference.yaml`
- `docs/patcher/shared/build_platform_factory_patchset.py`
- `docs/patcher/shared/repair_platform_factory_patchset.py`
- `docs/patcher/shared/validate_platform_factory_patchset.py`
- éventuellement une note de focalisation patch dans `docs/pipelines/platform_factory/inputs/`

## Contexte d'exécution obligatoire

- `platform_factory_arbitrage.md` est la source de vérité du stage. [Nouvelle exigence] le patchset final ne doit plus être rédigé directement à la main par l'IA si un fichier d'intention intermédiaire permet d'éviter une dérive de schéma.
- Les challenge reports historiques peuvent être relus si nécessaire pour traçabilité, mais ils ne doivent pas supplanter l'arbitrage final.
- Le résultat attendu doit être écrit dans le repo, dans le fichier YAML de sortie imposé ci-dessous.
- Il ne faut pas considérer qu'une réponse dans le chat suffit à accomplir la tâche.
- Le but est de produire un patchset exploitable au Stage 04, pas de réouvrir l'arbitrage.
- Le schéma normatif du patchset est défini par `docs/patcher/shared/patchset_schema_reference.yaml` et contrôlé par `docs/patcher/shared/validate_platform_factory_patchset.py`.
- Si le patchset final est produit sans utiliser le builder et qu'il échoue au validateur pour un problème de forme, la run est considérée comme incomplète.

## Fichiers de sortie autorisés

Écrire au maximum ces fichiers dans le repo :
- `docs/pipelines/platform_factory/work/03_patch/patchset_intent.yaml` (recommandé)
- `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml` (obligatoire)

Le fichier obligatoire du stage reste :
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
9. `docs/patcher/shared/patchset_schema_reference.yaml`
10. `docs/patcher/shared/build_platform_factory_patchset.py`
11. `docs/patcher/shared/repair_platform_factory_patchset.py`
12. `docs/patcher/shared/validate_platform_factory_patchset.py`
13. éventuellement la note de focalisation patch

## Objectif exact

Produire le patchset YAML final du stage, sous forme d'un fichier :
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

## Stratégie de production obligatoire

### Principe général

Le patchset final **ne doit pas être rédigé directement en YAML contraint** si cela peut être évité.

La stratégie par défaut est :
1. synthétiser l'intention de patch sous une forme IA-friendly
2. écrire `patchset_intent.yaml`
3. générer le patchset final via `build_platform_factory_patchset.py`
4. valider le patchset généré via `validate_platform_factory_patchset.py`
5. si la validation échoue pour des anomalies récupérables de forme, passer par `repair_platform_factory_patchset.py`, puis revalider
6. ne considérer la tâche accomplie que si `platform_factory_patchset.yaml` final est conforme au schéma attendu

### Format recommandé du fichier intermédiaire `patchset_intent.yaml`

Le fichier intermédiaire recommandé est :
- `docs/pipelines/platform_factory/work/03_patch/patchset_intent.yaml`

Il peut utiliser la structure IA-friendly suivante :

```yaml
intent_metadata:
  patchset_id: PFPATCH_YYYYMMDD_INITIALES_ID
  date: 'YYYY-MM-DD'
  source_decision_record: docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md
  scope: Description libre du périmètre
  notes:
  - Note 1

patch_intents:
- id: PFPATCH_A1
  decision: CONS-04
  target: arch
  op_type: add
  change_type: metadata_enrichment
  sequence: 1
  priority: eleve
  rationale: Justification libre
  effect: Effet libre
  risk_avoided: Risque évité
  section: PLATFORM_FACTORY_ARCHITECTURE.metadata
  granularity: field
  keys_to_update:
  - authority_rank
  operations:
  - op: add
    path: PLATFORM_FACTORY_ARCHITECTURE.metadata.authority_rank
    value: factory_layer
```

### Commandes de production recommandées

```bash
python docs/patcher/shared/build_platform_factory_patchset.py \
  ./docs/pipelines/platform_factory/work/03_patch/patchset_intent.yaml \
  ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml

python docs/patcher/shared/validate_platform_factory_patchset.py \
  ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml
```

Si nécessaire, en cas d'échec de forme récupérable :

```bash
python docs/patcher/shared/repair_platform_factory_patchset.py \
  ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml

python docs/patcher/shared/validate_platform_factory_patchset.py \
  ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset_repaired.yaml
```

### Politique de fallback

- Le builder est la voie nominale.
- Le repair script est une voie de rattrapage, pas la voie principale.
- Si le builder ne peut pas être utilisé, l'IA doit alors respecter strictement `patchset_schema_reference.yaml`.
- Il est interdit de livrer un patchset non validé au motif qu'il est "structurellement proche".

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
- Ne pas modifier `docs/cores/current/` directement.
- Ne pas introduire un besoin de patch non arbitré.
- Ne pas faire porter au canonique ce qui relève d'un validator, du pipeline ou de la gouvernance de release.
- Le livrable attendu est le fichier YAML écrit dans le repo. Le retour chat doit être très succinct.
- Le patchset final doit avoir été soit généré par le builder, soit validé explicitement contre le schéma de référence.

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

La structure normative exacte est celle de `docs/patcher/shared/patchset_schema_reference.yaml`.

## Résultat terminal attendu

À la fin de l'exécution, afficher uniquement :
1. le chemin exact du fichier écrit
2. le statut de validation obtenu (`PASS`, `WARN`, `FAIL`)
3. un résumé ultra-court
