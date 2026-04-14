# Handover — raccordement canonique `MATERIALIZE_NEW_RUN`

Branche de travail : `feat/core-modularization-bootstrap`

## État atteint

Le fichier suivant a été ajouté avec succès :

- `docs/pipelines/constitution/entry_actions/MATERIALIZE_NEW_RUN.action.yaml`

Commit déjà présent dans la branche :

- `bae4f06543f9ddb0817a196c9a9a42a8ee6429a5`

## But restant

Rendre le chemin d'entrée explicitement autoportant dans :

- `docs/pipelines/constitution/AI_PROTOCOL.yaml`
- `docs/pipelines/constitution/pipeline.md`

Le connecteur actuel a permis la création du nouveau fichier mais pas la mise à jour directe de fichiers existants via la voie simple. Voici donc le patch logique exact à reporter.

---

## 1. Patch logique à appliquer à `docs/pipelines/constitution/AI_PROTOCOL.yaml`

Insérer juste après `primary_entrypoint:` le bloc suivant :

```yaml
  entry_actions:
    decision_action_ref: docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml
    materialization_action_ref: docs/pipelines/constitution/entry_actions/MATERIALIZE_NEW_RUN.action.yaml
    sequencing_rule: >-
      En no_run_id_mode, l'ouverture d'un nouveau run suit deux actes canoniques distincts :
      d'abord OPEN_NEW_RUN pour résoudre la décision d'entrée sans écriture de tracking,
      puis MATERIALIZE_NEW_RUN pour matérialiser le run via update_run_tracking.py et
      materialize_run_inputs.py, sans démarrer STAGE_01_CHALLENGE.
```

### Intention

- conserver `OPEN_NEW_RUN` comme action de **décision** ;
- rendre visible `MATERIALIZE_NEW_RUN` comme action de **bootstrap matériel** ;
- expliciter la séquence canonique en `no_run_id_mode`.

---

## 2. Patch logique à appliquer à `docs/pipelines/constitution/pipeline.md`

### 2.1 Dans la section `## AI startup note`

Remplacer :

```md
For AI startup and run resolution, use `docs/pipelines/constitution/AI_PROTOCOL.yaml` as the authoritative entrypoint.
```

par :

```md
For AI startup and run resolution, use `docs/pipelines/constitution/AI_PROTOCOL.yaml` as the authoritative entrypoint.
In no-run-id entry mode, the canonical sequence is: `OPEN_NEW_RUN.action.yaml` for entry decision, then `MATERIALIZE_NEW_RUN.action.yaml` for deterministic run materialization, then stop before `STAGE_01_CHALLENGE` unless explicit continuation is requested.
```

### 2.2 Ajouter une petite section avant `## Stages`

```md
## Canonical entry actions

When the user does not provide a `run_id`, entry is resolved through two distinct canonical actions:

- `docs/pipelines/constitution/entry_actions/OPEN_NEW_RUN.action.yaml`
  - resolves whether opening a new run is authorized
  - must stop after the entry decision
  - must not write tracking files directly

- `docs/pipelines/constitution/entry_actions/MATERIALIZE_NEW_RUN.action.yaml`
  - materially opens the run through deterministic tracking
  - materially generates run inputs via `materialize_run_inputs.py`
  - must stop before `STAGE_01_CHALLENGE`

Structured rule:
- no-run-id startup must not jump directly from entry decision to STAGE_01
- run tracking materialization and input materialization are separate mandatory bootstrap acts
- STAGE_01_CHALLENGE may start only after the run has been materially opened and its inputs materially generated
```

### Intention

- rendre visible depuis `pipeline.md` que l'entrée canonique n'est pas un acte monolithique ;
- empêcher les IA de croire qu'un `open_new_run_authorized` vaut démarrage du pipeline ;
- réaligner `pipeline.md` avec la nouvelle action `MATERIALIZE_NEW_RUN.action.yaml`.

---

## 3. Résultat attendu après raccordement

Le chemin canonique devient lisible sans inférence :

1. `OPEN_NEW_RUN` → décision d'entrée
2. `MATERIALIZE_NEW_RUN` → tracking + inputs
3. arrêt avant `STAGE_01_CHALLENGE`
4. démarrage de stage seulement sur demande explicite

---

## 4. Pourquoi c'est le bon correctif

Sans ce raccordement, le repo reste dans un état où :

- l'action `OPEN_NEW_RUN` autorise seulement une décision puis impose l'arrêt ;
- `AI_PROTOCOL.yaml` mentionne les briques de tracking mais sans séquencement canonique explicite ;
- `pipeline.md` exige les inputs avant STAGE_01 mais ne dit pas clairement quel contrat d'entrée les matérialise.

Le nouveau fichier `MATERIALIZE_NEW_RUN.action.yaml` corrige la couture logique, mais il faut encore rendre cette couture visible depuis les deux points d'entrée centraux.
