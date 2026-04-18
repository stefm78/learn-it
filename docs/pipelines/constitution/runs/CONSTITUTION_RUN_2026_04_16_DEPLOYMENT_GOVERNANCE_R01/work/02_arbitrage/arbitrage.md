# ARBITRAGE — Constitution pipeline

```yaml
stage: STAGE_02_ARBITRAGE
pipeline: constitution
run_id: CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01
mode: bounded_local_run
date: 2026-04-18
inputs:
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/run_context.yaml
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/scope_manifest.yaml
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/impact_bundle.yaml
  - docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_16_DEPLOYMENT_GOVERNANCE_R01/inputs/integration_gate.yaml
  - docs/cores/current/referentiel.yaml
human_arbitrage_notes: none
execution_note: >-
  Arbitrage produit en respectant le contrat STAGE_02_ARBITRAGE.skill.yaml.
  Aucun script n'a été simulé. Le connecteur n'a pas permis de relire directement
  le ou les fichiers challenge_report_<id>.md du run sur cette branche ; l'arbitrage
  s'appuie donc sur la surface de run exécutable, sur les watchpoints du gate,
  sur le scope manifest, sur l'impact bundle, sur la lecture obligatoire du Référentiel,
  et sur la trace canonique déjà présente dans run_manifest.
```

---

## Executive summary

Arbitrage borné sur le scope `deployment_governance`.

Décision consolidée :
- **corriger_maintenant** : 3 points
- **reporter** : 0 point
- **rejeter** : 0 point
- **hors_perimetre** : 0 point
- **necessite_extension_scope** : 1 point

L'arbitrage retient trois corrections locales, toutes strictement compatibles avec le périmètre modifiable du run :
1. clarifier la frontière entre contraintes d'architecture locale et règles pédagogiques ;
2. renforcer la séparation Constitution/Référentiel et empêcher toute dérive des régimes d'autonomie vers une logique adaptative implicite ;
3. verrouiller la non-contamination des règles top-level de gouvernance (GF-08, probation gamification) vers le patch_lifecycle.

Un point supplémentaire est retenu comme **needs_scope_extension** : la dépendance inter-Core explicite vers le Référentiel doit être restaurée ou re-matérialisée de façon traçable, mais ce run ne donne pas de droit d'écriture sur le Référentiel ni sur un voisin inter-Core.

---

## Scope analysed

### Run surface utilisée
- `run_context.yaml`
- `scope_manifest.yaml`
- `impact_bundle.yaml`
- `integration_gate.yaml`
- `referentiel.yaml` (lecture obligatoire étendue par l'impact bundle)

### Périmètre modifiable autorisé
- Fichier autorisé : `docs/cores/current/constitution.yaml`
- Modules autorisés : `deployment`, `runtime_architecture`, `runtime_governance`, `governance`, `initialization`, `system`
- 19 IDs explicitement inclus dans `writable_perimeter.ids`

### Contraintes de scope appliquées
- aucune correction silencieuse hors scope
- l'impact bundle étend la lecture, pas l'écriture
- aucune réécriture de Core
- aucune génération de patch YAML

### Limite méthodologique explicitée
Le ou les challenge reports de STAGE_01 ne sont pas relus directement dans cette exécution via le connecteur. Leur existence et leur consommation attendue sont néanmoins corroborées par l'état exécutable du run et par l'historique canonique de stage. Le présent arbitrage reste donc conservateur et strictement borné.

---

## Detailed arbitrage by finding

---

### Finding DG-01 — frontière runtime local / pédagogie à expliciter

- **Source de consolidation :** watchpoint `WP_01`, IDs in-scope `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION`
- **Constat synthétique :** le scope `deployment_governance` porte des contraintes d'architecture locale fortes. Le gate demande explicitement d'éviter tout glissement de ces contraintes vers des règles pédagogiques. Sans clarification, une contrainte technique de déploiement peut être interprétée comme une règle d'adaptation pédagogique ou de comportement moteur.
- **Scope status :** `in_scope`
- **Décision :** `corriger_maintenant`
- **Justification :** le point est directement couvert par les modules autorisés `deployment`, `runtime_architecture`, `runtime_governance` et par plusieurs IDs explicitement modifiables. La correction attendue est de nature gouvernance / clarification locale, sans extension de périmètre.
- **Compatibilité pipeline :** forte ; ne demande ni patch inter-Core ni changement de logique hors scope.
- **Conséquence attendue pour STAGE_03_PATCH_SYNTHESIS :** produire une correction minimale dans la Constitution qui rende explicite que les invariants de localité et de qualification des signaux restent des contraintes d'architecture/runtime et ne peuvent pas être réinterprétés comme des règles pédagogiques.

---

### Finding DG-02 — séparation Constitution/Référentiel et statut des régimes d'autonomie

- **Source de consolidation :** watchpoints `WP_02`, `WP_03`, `WP_05`, IDs in-scope `INV_CONSTITUTION_REFERENTIAL_SEPARATION`, `TYPE_AUTONOMY_REGIME`, `TYPE_INTEGRITY_MODES`, `CONSTRAINT_NO_CHANGE_TO_AND_LOGIC`, `CONSTRAINT_NO_CHANGE_TO_GRAPH_PROPAGATION_RULE`
- **Constat synthétique :** le gate exige simultanément (a) de préserver une séparation inviolable Constitution/Référentiel, (b) de maintenir les régimes d'autonomie comme des configurations et non comme des règles adaptatives implicites, et (c) de ne pas confondre invariant constitutionnel et paramètre référentiel. Le risque consolidé est une dérive de gouvernance : des choix de configuration opérationnelle pourraient absorber de la logique normative.
- **Scope status :** `in_scope`
- **Décision :** `corriger_maintenant`
- **Justification :** ce point relève du cœur du périmètre autorisé : `governance`, `runtime_governance`, `system`, plus les IDs explicites sur la séparation et les régimes. La correction peut rester locale à la Constitution en renforçant la frontière d'autorité, sans réallouer silencieusement de logique au Référentiel.
- **Compatibilité pipeline :** forte ; la correction est bornée et prépare un patch traçable.
- **Conséquence attendue pour STAGE_03_PATCH_SYNTHESIS :** introduire ou renforcer une formulation constitutionnelle qui :
  1. rappelle que les régimes d'autonomie sont des configurations gouvernées ;
  2. interdit qu'ils deviennent des règles adaptatives implicites ;
  3. trace explicitement que la logique AND et la propagation graphe ne bougent pas dans ce chantier.

---

### Finding DG-03 — gouvernance top-level et probation gamification à isoler du patch_lifecycle

- **Source de consolidation :** watchpoint `WP_04`, IDs in-scope `RULE_GF08_UNCOVERED_CONFLICT_CONSERVATIVE_RESPONSE`, `EVENT_GF08_UNCOVERED_CONFLICT`, `RULE_UNVERIFIED_GAMIFICATION_PROBATION`, `RULE_GAMIFICATION_PROBATION_MUST_CLOSE`, `EVENT_GAMIFICATION_PROBATION_MAX_DURATION_REACHED`
- **Constat synthétique :** le gate demande explicitement de vérifier que les règles top-level de gouvernance (GF-08, gamification) n'empiètent pas sur le patch_lifecycle. Le risque consolidé est une contamination de niveau : une règle de supervision ou de probation pourrait être utilisée comme mécanisme implicite de patch, de promotion ou de décision de changement structurel.
- **Scope status :** `in_scope`
- **Décision :** `corriger_maintenant`
- **Justification :** les événements et règles concernés sont tous dans le périmètre autorisé. La correction est locale et de gouvernance : elle consiste à verrouiller la séparation entre supervision constitutionnelle, probation gamification et lifecycle de patch.
- **Compatibilité pipeline :** forte ; correction minimale, sans promotion, sans opération interdite.
- **Conséquence attendue pour STAGE_03_PATCH_SYNTHESIS :** proposer une correction constitutionnelle qui clarifie que GF-08 et la probation gamification peuvent imposer une réponse conservatrice, une clôture ou un signal de gouvernance, mais ne valent ni patch implicite, ni réallocation inter-Core, ni autorisation de promotion.

---

### Finding DG-04 — référence inter-Core vers le Référentiel à restaurer explicitement

- **Source de consolidation :** `impact_bundle.yaml`, `run_context.yaml`, lecture obligatoire du `referentiel.yaml`
- **Constat synthétique :** le run porte une dépendance de lecture obligatoire vers `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`, mais `neighbor_extract` la signale manquante. En parallèle, le Référentiel courant expose bien une référence explicite inverse vers la Constitution (`REF_CORE_LEARNIT_CONSTITUTION_V3_0_IN_REFERENTIEL`). La symétrie inter-Core paraît donc incomplète ou désalignée sur la face Constitution.
- **Scope status :** `needs_scope_extension`
- **Décision :** `necessite_extension_scope`
- **Justification :** le besoin est réel et pertinent pour l'intégrité inter-Core, mais la correction n'est pas un simple ajustement local purement éditorial. Elle touche la matérialisation d'une dépendance inter-Core et doit être arbitrée explicitement pour éviter toute réallocation implicite. Le run est borné à `constitution.yaml` avec un devoir de lecture étendu, pas un droit silencieux de reconfiguration inter-Core.
- **Compatibilité pipeline :** moyenne ; ne doit pas être corrigé silencieusement dans un patch local sans décision de scope.
- **Conséquence attendue pour STAGE_03_PATCH_SYNTHESIS :** ne pas produire de patch sur ce point dans le patchset local. Le signaler explicitement comme dépendance à traiter par extension de scope ou par chantier inter-Core dédié.

---

## Consolidated points

### Regroupements effectués
- **Cluster A — Local runtime boundary** : WP_01 + invariants runtime locaux
- **Cluster B — Constitutional authority boundary** : WP_02 + WP_03 + WP_05 + IDs de séparation et d'autonomie
- **Cluster C — Top-level governance isolation** : WP_04 + GF-08 + probation gamification
- **Cluster D — Inter-Core anchor gap** : impact bundle + neighbor_extract missing + lecture du Référentiel

### Contradiction ou anomalie de tracking observée
Le run présente une anomalie de traçabilité : `run_context.yaml` et `run_manifest.yaml` portent déjà `STAGE_02_ARBITRAGE` dans `completed_stages` tout en exposant `STAGE_02_ARBITRAGE` comme prochain stage exécutable. Ce point n'appelle pas de correction de contenu dans le présent arbitrage, mais doit être gardé visible lors du tracking humain pour éviter une double validation ambiguë.

---

## Decisions for patch

### Points à transmettre à STAGE_03_PATCH_SYNTHESIS

| Priorité | Finding | Décision | Scope status | Surface visée |
|---|---|---|---|---|
| 1 | DG-02 | corriger_maintenant | in_scope | `constitution.yaml` — gouvernance / séparation / autonomie |
| 2 | DG-03 | corriger_maintenant | in_scope | `constitution.yaml` — gouvernance top-level / probation / patch boundary |
| 3 | DG-01 | corriger_maintenant | in_scope | `constitution.yaml` — runtime architecture / local deployment boundary |

### Contraintes de synthèse à respecter
- aucune correction silencieuse hors scope
- aucune réécriture du Référentiel
- aucune réallocation implicite de logique vers le Référentiel
- aucune génération de patch pour DG-04 sans extension explicite de scope
- les formulations doivent rester minimales, auditables et compatibles avec les checks du gate

---

## Decisions not retained

### Non retenu pour patch local immédiat

| Finding | Décision | Justification |
|---|---|---|
| DG-04 | necessite_extension_scope | dépendance inter-Core réelle mais non patchable silencieusement dans ce run borné |

### Aucun point rejeté
Aucun finding significatif n'est rejeté à ce stade.

### Aucun point classé hors périmètre simple
Aucun finding n'est simplement `hors_perimetre` : le point DG-04 est plus fort qu'un hors-périmètre informatif, car il appelle une décision explicite d'extension de scope.
