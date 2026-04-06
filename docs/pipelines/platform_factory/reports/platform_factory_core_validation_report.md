# STAGE_06 — Platform Factory Core Validation Report

## Résumé exécutif

Le validateur automatique `validate_platform_factory_core.py` retourne **`PASS`** sur les 31 checks structurels, sans anomalie ni warning dans son périmètre.

Toutefois, une **anomalie structurelle logique** a été identifiée lors de la revue humaine des artefacts patchés, hors périmètre du validateur automatique : les opérations `op: add` et `op: replace` du patchset ont écrit des clés **en dehors du bloc racine canonique** (`PLATFORM_FACTORY_ARCHITECTURE` / `PLATFORM_FACTORY_STATE`), au lieu d'agir à l'intérieur de ces blocs.

Cela produit des **clés dupliquées au niveau racine YAML** dans les deux artefacts patchés.

Le verdict global du Stage 06 est donc : **`WARN`** — le couple patché est structurellement recevable par le validateur automatique, mais présente une anomalie logique de structure YAML qui doit être corrigée avant tout passage au Stage 07.

---

## Qualification du contexte de validation

- **Mode** : `POST_APPLY_CORE_VALIDATION`
- **Artefacts validés** :
  - `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml`
  - `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml`
- **Script automatique** : `validate_platform_factory_core.py` — exécuté réellement en local
- **Trace d'exécution** : `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml` — `status: PASS`, `operations_applied: 10/10`

---

## Décision globale

| Dimension | Résultat |
|---|---|
| Validateur automatique (31 checks) | ✅ PASS |
| Anomalie structurelle logique hors scope validateur | ⚠️ WARN |
| **Verdict Stage 06 global** | **⚠️ WARN — correction requise avant Stage 07** |

---

## Vérifications par axe

### 1. Adéquation au mode POST_APPLY
✅ PASS — Les artefacts soumis sont bien les artefacts patchés issus du Stage 05 apply réel.

### 2. Fidélité à l'arbitrage et au patchset appliqué
✅ PASS — Les 10 opérations du patchset (PFARB-DEC-01, 02, 03, 06) sont reflétées dans les artefacts. Les exclusions (DEC-04, 05, 07) ne sont pas introduites.

### 3. Séparation architecture / state
✅ PASS — `PLATFORM_FACTORY_ARCHITECTURE` reste prescriptif. `PLATFORM_FACTORY_STATE` reste constatif. Aucune confusion de rôle détectée dans les blocs canoniques.

### 4. Cohérence interne et cohérence croisée
⚠️ WARN — Les blocs canoniques internes sont cohérents. Cependant, les clés racine dupliquées constituent une incohérence structurelle YAML :
- Dans `platform_factory_architecture.yaml` : `contracts`, `generated_projection_rules` et `build_and_packaging_rules` apparaissent deux fois — une fois dans le bloc `PLATFORM_FACTORY_ARCHITECTURE`, une fois hors bloc en racine absolue.
- Dans `platform_factory_state.yaml` : `produced_application_contract_status`, `derived_projection_conformity_status` et `capabilities_absent` apparaissent deux fois — une fois dans le bloc `PLATFORM_FACTORY_STATE`, une fois hors bloc en racine absolue.

Cause identifiée : le patcher écrit les modifications en résolvant les chemins path depuis la racine YAML absolue, non depuis la racine du bloc canonique déclaré dans `target_artifact`.

### 5. Compatibilité avec Constitution / Référentiel / LINK
✅ PASS — Les dépendances canoniques sont déclarées et inchangées.

### 6. Cohérence du contrat minimal d'application produite
✅ PASS dans les blocs canoniques. La duplication racine n'introduit pas de contradiction de règle, mais fragmente la lisibilité et pourrait induire un loader YAML en erreur ou en comportement ambigu.

### 7. Gouvernabilité des projections dérivées
✅ PASS — La liste `minimum_requirements` dans le bloc canonique contient bien les 8 items attendus, dont les 3 nouveaux issus de PFARB-DEC-02.

### 8. Maintien de la posture multi-IA
✅ PASS — Aucun invariant multi-IA n'a été altéré dans le bloc canonique.

### 9. Stabilité et gouvernabilité de l'état patché
⚠️ WARN — L'état patché est gouvernable sur le fond, mais la duplication de clés racine fragilise la robustesse de tout outil qui chargerait le YAML (loader Python `yaml.safe_load` retient la dernière valeur en cas de doublon, ce qui masque les modifications du patchset plutôt que de les appliquer visiblement).

---

## Anomalies bloquantes

Aucune anomalie n'a été signalée par le validateur automatique.

Anomalie logique identifiée hors scope validateur (revue humaine) :

| ID | Sévérité | Description |
|---|---|---|
| PF_ANOM_STAGE06_RACINE_DUPLIQUEE | BLOQUANT avant Stage 07 | Les opérations du patchset écrivent en racine YAML absolue au lieu d'agir dans le bloc canonique. Clés dupliquées dans les deux artefacts patchés. |

---

## Warnings

Aucun warning signalé par le validateur automatique.

Warning logique hors scope validateur :

| ID | Description |
|---|---|
| PF_WARN_YAML_LOADER_BEHAVIOR | Un loader YAML standard (`yaml.safe_load`) résout les doublons de clés en retenant la dernière valeur. La duplication actuelle signifie que les modifications patchées écrasent silencieusement les blocs canoniques pour les champs concernés. Comportement non conforme à l'intention du patchset. |

---

## Conditions avant Stage 07

**Condition bloquante :** corriger la structure YAML des deux artefacts patchés avant de procéder au Stage 07.

Les corrections attendues sont :
- Dans `platform_factory_architecture.yaml` : supprimer les blocs racine dupliqués `contracts`, `generated_projection_rules`, `build_and_packaging_rules` et intégrer leurs valeurs correctement à l'intérieur du bloc `PLATFORM_FACTORY_ARCHITECTURE`.
- Dans `platform_factory_state.yaml` : supprimer les blocs racine dupliqués `produced_application_contract_status`, `derived_projection_conformity_status`, `capabilities_absent` et intégrer leurs valeurs correctement à l'intérieur du bloc `PLATFORM_FACTORY_STATE`.

Ces corrections peuvent se faire :
1. En corrigeant le comportement du patcher (résolution de chemin depuis le bloc canonique et non depuis la racine YAML absolue).
2. Ou en produisant directement les artefacts patchés corrigés à la main et en les replaçant dans `work/05_apply/patched/`.

**Une fois les artefacts corrigés**, un nouveau passage du validateur automatique doit confirmer `status: PASS` avant d'autoriser le Stage 07.

---

*Stage 06 exécuté le 2026-04-06. Validateur automatique : PASS 31/31. Verdict global Stage 06 : WARN — correction structurelle requise avant Stage 07.*
