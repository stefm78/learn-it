# Arbitrage Platform Factory — Proposition indépendante

arbitrage_run_id: PFARB_20260410_PPLX_M3F8

Date: 2026-04-10

## Challenge reports considérés

- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_01_Nemotron.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_GPT54_8KQ2.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PPLX_7KQ2.md`

---

## Résumé d’arbitrage

Les trois challenge reports convergent fortement sur les mêmes zones de faiblesse. Aucune contradiction majeure entre eux n’a été identifiée. Le niveau de sévérité varie légèrement (Nemotron est le plus détaillé et le plus précis sur le détail normatif, GPT54 et PPLX apportent des formulations complémentaires), mais les décisions d’arbitrage proposées ici sont appuyées sur un consensus fort.

La baseline V0.3 est acceptable comme fondation. Elle ne viole pas activement la Constitution. Ses problèmes portent essentiellement sur la fermeture des chaînes de preuve, la cohérence interne entre architecture et state, la gouvernance release/manifest, et la sur-lecture possible des projections dérivées.

Cette proposition identifie 5 blocs de décisions à retenir maintenant, 2 points à différer, et 1 point à mettre hors périmètre. Les préconditions de patch sont explicitées pour chaque décision.

---

## Synthèse des constats convergents

### Convergence C-01 — Chaîne de preuve constitutionnelle non fermée

Les trois rapports s’accordent : l’architecture vise les invariants constitutionnels (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`) mais ne fournit pas de mécanisme auditable pour qu’une application produite prouve sa conformité. Le `constitutional_conformance_matrix.yaml` est référencé mais absent. L’axe `runtime_policy_conformance` de la validation minimale est creux. Le signal `constitutional_invariants_checked` dans l’observabilité minimale est non auditable.

- Sources : Nemotron COR-01, COR-04 ; GPT54 PF-CHAL-01 ; PPLX Axe 1 et Axe 4.
- Niveau de consensus : fort.

### Convergence C-02 — Projections dérivées : ambigüité `usage_as_sole_context` + absence de validator

Les trois rapports identifient la tension entre `generated_projection_rules.minimum_requirements` qui permet l’usage en contexte unique et `execution_projection_contract.usage_as_sole_context: blocked`. Cette contradiction est dangereuse : une IA peut se baser sur l’une des deux lectures. De plus, aucun validator dédié ne permet de marquer `validation_status: validated` de manière déterministe.

- Sources : Nemotron COR-02, COR-03, Problème 2.1, 5.1 ; GPT54 PF-CHAL-02 ; PPLX Axe 5.
- Niveau de consensus : fort.

### Convergence C-03 — `constitutional_conformance_matrix.yaml` absent, référence morte

Les trois rapports signalent que `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` est référencé dans deux emplacements de l’architecture (`mandatory_fields_per_projection.conformance_matrix_ref` et `dependencies_to_constitution.constitutional_conformance_matrix_ref`) mais n’existe pas dans le repo. Il n’est pas listé comme blocker ni comme capacité absente dans le state.

- Sources : Nemotron Problème 2.3, COR-03 ; GPT54 PF-CHAL-01 ; PPLX Axe 4.
- Niveau de consensus : fort.

### Convergence C-04 — Gouvernance release/manifest : fenêtre ouverte

Les trois rapports s’accordent : les artefacts factory sont dans `docs/cores/current/` mais hors manifest officiel, sans manifest dédié factory non plus. Le blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` est explicité dans le state, mais sans stratégie d’intérim (manifest dédié partiel, extension du manifest existant, ou simple note de gouvernance). La confusion possible entre artefacts `current/` et canoniques primaires est signalée par Nemotron (Problème 8.1) et GPT54 (PF-CHAL-04).

- Sources : Nemotron Problème 8.1, 8.2 ; GPT54 PF-CHAL-04 ; PPLX Axe 8.
- Niveau de consensus : fort.

### Convergence C-05 — Multi-IA : exigences sans protocole opérationnel

Les trois rapports s’accordent que le multi-IA est bien reconnu comme exigence de premier rang mais reste non opérationnalisé : granularité modulaire, assemblage, résolution de conflit, reports homogènes sont absents. Nemotron qualifie l’absence comme « impossibilité opérationnelle » (Problème 7.1) ; GPT54 parle de « protocoles absents » (PF-CHAL-05) ; PPLX (Axe 7) note que les principes sont posés sans les mécanismes.

- Sources : Nemotron 7.1, 7.2 ; GPT54 PF-CHAL-05 ; PPLX Axe 7.
- Niveau de consensus : fort.

### Convergence C-06 — Incohérences résiduelles architecture/state

GPT54 (PF-CHAL-03) et PPLX (Axe 2) signalent que l’emplacement des projections est décidé dans l’architecture mais encore listé comme manquant dans `derived_projection_conformity_status.missing` du state. GPT54 note aussi que `assessed_scope.excludes` contient encore `exact_projection_storage_location` alors que la décision est déjà inscrite.

- Sources : GPT54 PF-CHAL-03 ; PPLX Axe 2.
- Niveau de consensus : fort.

### Convergence C-07 — Surdeclarations mineures dans le state

Nemotron (Surdeclaration 6.1, 6.2) et PPLX (Axe 6) signalent que `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` est dans `capabilities_present` alors qu’il s’agit d’une intention non outillée. Nemotron signale aussi le nom trompeur `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` (capacité partielle, pas prête à l’emploi). GPT54 formule le même diagnostic plus généralement (Axe 6).

- Sources : Nemotron 6.1, 6.2 ; PPLX Axe 6 ; GPT54 Axe 6.
- Niveau de consensus : fort.

### Point spécifique Nemotron non repris par les autres — `authority_rank` dans les métadonnées

Nemotron (COR-07, Problème 8.1) propose d’ajouter un champ `authority_rank: factory_layer` dans les métadonnées des artefacts factory pour différencier explicitement leur statut de celui des canoniques primaires. GPT54 et PPLX soulèvent le même risque de confusion (Scénario D, Problème 8.1) mais ne formulent pas la même correction.

- Sources : Nemotron COR-07 ; GPT54 Scénario D ; PPLX Axe 8.
- Niveau de consensus : moyen (sujet partagé, solution spécifique Nemotron non encore endossée par les autres).

---

## Propositions d’arbitrage par thème

---

### Décision ARB-PF-01 — Fermer la chaîne de preuve constitutionnelle

- **Sujet** : Capacité de la factory à prouver qu’une application produite respecte `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`.
- **Source(s)** : C-01 ; Nemotron COR-01, COR-04 ; GPT54 PF-CHAL-01 ; PPLX Axe 1, Axe 4.
- **Décision proposée** : `retained_now`.
- **Lieu principal** : architecture (`produced_application_minimum_contract.minimum_validation_contract`, `minimum_observability_contract`).
- **Lieux secondaires** : state (ajouter un blocker pour la conformance matrix), validator/tooling (définir les critères de `runtime_policy_conformance`).
- **Priorité** : critique.
- **Justification** : Sans correction, la factory ne peut pas garantir la fonction fondamentale qu’elle revendique : une application produite constitutionnellement compatible. C’est le risque le plus haut du système.
- **Impact si non traité** : Applications produites potentiellement non locales ou génératives sans détection.
- **Précondition** : aucune, patchable maintenant.
- **Note de séquencement** : doit être traité avant ARB-PF-05 (multi-IA), car les protocoles multi-IA consommeront le contrat minimal.
- **Niveau de consensus** : fort.

---

### Décision ARB-PF-02 — Résoudre l’ambiguïté `usage_as_sole_context` + reconnaître l’absence de validator de projection

- **Sujet** : Tension interne dans `execution_projection_contract` + absence de protocole de validation déterministe pour les projections dérivées.
- **Source(s)** : C-02 ; Nemotron COR-02, Problème 2.1, 5.1, 5.2 ; GPT54 PF-CHAL-02 ; PPLX Axe 5.
- **Décision proposée** : `retained_now` pour la résolution de l’ambigüité normative ; `deferred` pour le validator outillé complet.
- **Lieu principal** : architecture (`contracts.execution_projection_contract`, `generated_projection_rules`).
- **Lieu secondaire** : state (recalibrer `derived_projection_conformity_status`).
- **Priorité** : élevée.
- **Justification** : L’ambiguïté normative doit être résolue maintenant car elle affecte toute IA qui lit l’architecture. La résolution attendue : clarifier que `usage_as_sole_context: blocked` est l’état V0 actuel et que `each_projection_can_be_used_as_single_context_for_targeted_task` décrit le régime cible, avec des conditions de déblocage explicites. Le validator dédié est un déferrement acceptable car son outillage dépend de maturités extérieures.
- **Impact si non traité** : Dérive normative silencieuse ; IA pouvant traiter comme validé ce qui ne l’est pas.
- **Précondition** : aucune, clarification wording patchable maintenant.
- **Niveau de consensus** : fort.

---

### Décision ARB-PF-03 — Enregistrer `constitutional_conformance_matrix.yaml` comme blocker et supprimer la référence morte

- **Sujet** : Référence à `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` dans l’architecture alors que le fichier n’existe pas.
- **Source(s)** : C-03 ; Nemotron Problème 2.3, COR-03 ; GPT54 PF-CHAL-01 ; PPLX Axe 4.
- **Décision proposée** : `retained_now`.
- **Lieu principal** : state (ajouter `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` avec exit condition).
- **Lieu secondaire** : architecture (annoter le champ comme `tbd_pending_blocker` ou équivalent ; ne pas supprimer la référence pour ne pas casser le design intent).
- **Priorité** : élevée.
- **Justification** : Une référence morte dans un contrat released crée une ambiguïté sur la valeur réelle du mécanisme de validation. Enregistrer l’absence comme blocker est la correction minimale propre, sans bloquer d’autres patchs.
- **Impact si non traité** : Toute projection ou application produite référençant cette matrix pointe un artefact inexistant, rendant la conformité non auditable.
- **Précondition** : aucune.
- **Niveau de consensus** : fort.

---

### Décision ARB-PF-04 — Clarifier la gouvernance release/manifest des artefacts factory

- **Sujet** : Artefacts factory dans `docs/cores/current/` sans intégration manifest officielle ni manifest alternatif dédié, et sans marquage explicite de leur autorité distincte des canoniques primaires.
- **Source(s)** : C-04 ; Nemotron Problème 8.1, 8.2, COR-07 ; GPT54 PF-CHAL-04, Scénario D ; PPLX Axe 8.
- **Décision proposée** : `retained_now` pour le marquage `authority_rank` dans les métadonnées et la stratégie de gouvernance intermédiaire ; `deferred` pour le manifest officiel complet (lié à STAGE_08).
- **Lieu principal** : architecture + state (ajouter `authority_rank: factory_layer` ou équivalent dans les métadonnées ; clarifier la stratégie de manifest d’intérim dans le state ou le pipeline).
- **Lieu secondaire** : pipeline (Rule 3, préciser la stratégie d’intérim manifest).
- **Priorité** : élevée.
- **Justification** : Le risque de confusion entre couche factory et couche canonique primaire est un risque de dérive d’autorité. Ajouter un champ `authority_rank` est une correction de wording/metadata très peu invasive mais avec un impact réel sur la lisibilité de gouvernance. La stratégie de manifest d’intérim doit être une décision humaine explícite.
- **Impact si non traité** : Une IA ou un opérateur peut traiter les artefacts factory comme canoniques primaires et produire des décisions errénées.
- **Précondition** : décision humaine sur la stratégie d’intérim manifest (extend manifest officiel vs manifest factory dédié).
- **Note de séquencement** : La stratégie d’intérim manifest doit être fixée avant STAGE_07/STAGE_08 du pipeline.
- **Niveau de consensus** : fort (sur le problème) ; moyen (sur la solution `authority_rank` spécifique à Nemotron, à trancher en consolidation).

---

### Décision ARB-PF-05 — Recaler l’état sur la décision d’emplacement des projections et corriger les surdéclarations mineures

- **Sujet** : Incohérences résiduelles architecture/state sur l’emplacement des projections + classement de deux capacités.
- **Source(s)** : C-06, C-07 ; GPT54 PF-CHAL-03 ; PPLX Axe 2, Axe 6 ; Nemotron 6.1, 6.2.
- **Décision proposée** : `retained_now`.
- **Lieu principal** : state.
  - Retirer `storage_location_decision` de `derived_projection_conformity_status.missing`.
  - Mettre à jour `assessed_scope.excludes` si nécessaire.
  - Déplacer `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` de `capabilities_present` vers `capabilities_partial` avec description précise.
  - Ajuster le libellé ou la description de `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` pour éviter la sur-lecture.
- **Priorité** : modérée.
- **Justification** : Des incohérences résiduelles dans l’artefact constatif fragilisent la fiabilité de l’ensemble du state. Ces corrections sont peu invasives et non ambigües.
- **Impact si non traité** : Lecture divergente du statut réel par des IA différentes.
- **Précondition** : aucune.
- **Niveau de consensus** : fort.

---

### Décision ARB-PF-06 — Multi-IA : définir un protocole minimal opérationnel

- **Sujet** : Transformation des exigences multi-IA en protocole exploitable (granularité, assemblage, résolution de conflit).
- **Source(s)** : C-05 ; Nemotron 7.1, 7.2 ; GPT54 PF-CHAL-05 ; PPLX Axe 7.
- **Décision proposée** : `deferred` — mais avec wording de state plus honnête sur la réalité opérationnelle actuelle.
- **Lieu principal** : state (mise à jour de `multi_ia_parallel_readiness_status` pour indiquer qu’aucun protocole d’exécution n’existe).
- **Lieu secondaire** : architecture (ajouter une note que les mécanismes opérationnels restent à définir, pour ne pas laisser croire que les principes suffisent).
- **Priorité** : modérée en V0 (différement justifié car le parallelisme multi-IA n’est pas encore pratiqué en production).
- **Justification** : Définir le protocole complet est une tâche de fond qui dépasse un patch de baseline V0. Mais le state doit être plus clair sur le fait que ce n’est pas encore utilisable en pratique.
- **Impact si non traité** : Collision et improvisation si plusieurs IA travaillent sans protocole.
- **Précondition** : décision humaine sur la feuille de route multi-IA.
- **Niveau de consensus** : fort.

---

### Décision ARB-PF-07 — `bootstrap_contract: TBD` — enregistrer comme blocker

- **Sujet** : Le `runtime_entrypoint_contract.bootstrap_contract` est obligatoire mais TBD, ce qui rend le contrat minimal incomplétable en validation.
- **Source(s)** : Nemotron Problème 4.2, COR-05 ; GPT54 Axe 4.
- **Décision proposée** : `retained_now` (enregistrement du blocker dans le state).
- **Lieu principal** : state (ajouter `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` avec exit condition lié à la définition de la typologie des runtimes).
- **Priorité** : élevée.
- **Justification** : Un champ obligatoire TBD non listé comme blocker crée une fausse impression de contrat complet. L’enregistrement du blocker est la correction minimale et suffisante en V0.
- **Impact si non traité** : Validation du contrat minimal impossible à terminer sans improvisation.
- **Précondition** : aucune.
- **Niveau de consensus** : fort.

---

## Points retenus

| ID | Sujet | Priorité | Lieu principal |
|---|---|---|---|
| ARB-PF-01 | Fermer la chaîne de preuve constitutionnelle (contrat minimal + conformance) | Critique | Architecture |
| ARB-PF-02 | Résoudre ambiguïté `usage_as_sole_context` | Élevée | Architecture |
| ARB-PF-03 | Enregistrer conformance matrix comme blocker | Élevée | State |
| ARB-PF-04 | Clarifier gouvernance release/manifest + `authority_rank` | Élevée | Architecture + State |
| ARB-PF-05 | Recaler state sur décision emplacement projections + surdéclarations | Modérée | State |
| ARB-PF-07 | Enregistrer `bootstrap_contract` TBD comme blocker | Élevée | State |

## Points différés

| ID | Sujet | Justification du déferrement |
|---|---|---|
| ARB-PF-06 | Définir protocole multi-IA opérationnel | Travail de fond dépassant un patch V0 ; state à recalibrer maintenant |
| ARB-PF-02 (validator) | Implémenter le validator de projection dédié | Dépend de maturités extérieures et de decisions aval |

## Points rejetés

Aucun finding des challenge reports n’a été rejeté comme non valide. Les différences de formulation entre rapports ne constituent pas de contradictions à rejeter.

## Points hors périmètre

| Sujet | Justification |
|---|---|
| Comportement runtime d’une application spécifique | Relevé par Nemotron mais correctement identifié comme hors scope factory |
| Contenu du graph domaine | Hors scope par construction |

## Points sans consensus ou nécessitant discussion finale

1. **Forme exacte du champ `authority_rank`** : Nemotron propose `authority_rank: factory_layer` ; les autres rapports soulèvent le problème sans proposer de champ spécifique. La solution exacte (champ de métadonnées, note de couche, ou autre marquage) doit être décidée en consolidation.
2. **Stratégie d’intérim manifest** : Etendre le manifest officiel existant ou créer un `docs/cores/platform_factory/manifest.yaml` dédié ? Ce choix est une décision humaine qui conditionne le contenu du patch ARB-PF-04.
3. **Schéma du `runtime_policy_conformance`** : Les trois rapports s’accordent que l’axe est creux, mais aucun ne propose un schéma complet. La définition minimale de cet axe (liste d’items à vérifier) doit être arbitrée en consolidation avant patch.

---

## Corrections à arbitrer avant patch

### CORR-ARB-01 — Ajouter des axes de validation explicites pour les invariants constitutionnels critiques

- **Élément concerné** : `produced_application_minimum_contract.minimum_validation_contract.minimum_axes` + `minimum_observability_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION` ne sont pas vérifiables à partir du contrat minimal actuel.
- **Statut proposé** : retained_now
- **Gravité** : critique
- **Justification** : Correction fondamentale. Sans elle, la factory ne peut pas certifier ce qu’elle est censée garantir.
- **Dépendance** : dépend de la définition du schéma de `runtime_policy_conformance` (point de discussion finale).
- **Lieu** : architecture
- **Consensus** : fort

### CORR-ARB-02 — Résoudre la contradiction `usage_as_sole_context` dans `execution_projection_contract`

- **Élément concerné** : `generated_projection_rules.minimum_requirements` + `contracts.execution_projection_contract`
- **Localisation** : `platform_factory_architecture.yaml`
- **Problème** : deux énoncés contradictoires dans le même artefact sur l’usage en contexte unique.
- **Statut proposé** : retained_now
- **Gravité** : élevée
- **Justification** : Correction de wording sans ambigüité ni risque de régression. Formulation recommandée : distinguer régime cible et politique V0 actuelle avec conditions de déblocage explicites.
- **Dépendance** : aucune
- **Lieu** : architecture
- **Consensus** : fort

### CORR-ARB-03 — Ajouter `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` dans le state

- **Élément concerné** : `blockers`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : `constitutional_conformance_matrix.yaml` est référencé dans l’architecture mais absent et non enregistré comme blocker.
- **Statut proposé** : retained_now
- **Gravité** : élevée
- **Justification** : Correction d’état propre. Non invasive.
- **Dépendance** : aucune
- **Lieu** : state
- **Consensus** : fort

### CORR-ARB-04 — Ajouter `authority_rank` dans les métadonnées factory (ou solution équivalente)

- **Élément concerné** : `metadata` de `platform_factory_architecture.yaml` et `platform_factory_state.yaml`
- **Problème** : absence de marquage différenciant le statut de ces artefacts de celui des canoniques primaires.
- **Statut proposé** : retained_now, mais forme exacte à décider en consolidation.
- **Gravité** : élevée
- **Justification** : Risque de confusion d’autorité lors d’une lecture automatisée des artefacts de `docs/cores/current/`.
- **Dépendance** : décision humaine sur la forme du champ
- **Lieu** : architecture + state
- **Consensus** : moyen (problème fort, forme à valider)

### CORR-ARB-05 — Recaler le state sur la décision d’emplacement + corriger les surdéclarations

- **Élément concerné** : `derived_projection_conformity_status.missing`, `assessed_scope.excludes`, `capabilities_present`, `capabilities_partial`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : incohérences résiduelles après décisions déjà actées + classement trop optimiste de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`.
- **Statut proposé** : retained_now
- **Gravité** : modérée
- **Justification** : Corrections d’état pures, non invasives, nécessaires pour la fiabilité du state.
- **Dépendance** : aucune
- **Lieu** : state
- **Consensus** : fort

### CORR-ARB-06 — Ajouter `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` dans le state

- **Élément concerné** : `blockers`
- **Localisation** : `platform_factory_state.yaml`
- **Problème** : `bootstrap_contract` est obligatoire dans l’architecture mais TBD et non enregistré comme blocker.
- **Statut proposé** : retained_now
- **Gravité** : élevée
- **Justification** : Correction d’état propre et non invasive. Rend transparente l’incomplétude du contrat minimal.
- **Dépendance** : aucune
- **Lieu** : state
- **Consensus** : fort

### CORR-ARB-07 — Préciser la stratégie d’intérim manifest pour les artefacts factory (décision humaine)

- **Élément concerné** : `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`, pipeline Rule 3
- **Problème** : absence de stratégie explicitée pour gérer les artefacts factory « current mais hors manifest officiel » en attendant STAGE_08.
- **Statut proposé** : `clarification_required` avant patch.
- **Gravité** : élevée
- **Justification** : Décision architecturale nécessitant un choix humain explicit (extend manifest officiel ou créer un manifest factory dédié temporaire).
- **Dépendance** : décision humaine préalable
- **Lieu** : pipeline + manifest/release governance
- **Consensus** : fort (sur le problème), à trancher

---

## Répartition par lieu de correction

| Lieu | Corrections liées |
|---|---|
| Architecture | CORR-ARB-01, CORR-ARB-02, CORR-ARB-04 |
| State | CORR-ARB-03, CORR-ARB-04, CORR-ARB-05, CORR-ARB-06 |
| Pipeline | CORR-ARB-07 |
| Manifest/release governance | CORR-ARB-07 |
| Validator/tooling | ARB-PF-02 (partie différée), ARB-PF-06 (différé) |

---

## Séquencement recommandé

1. **Clarifications humaines préalables au patch** : décision sur la stratégie manifest d’intérim (CORR-ARB-07), décision sur le schéma minimal de `runtime_policy_conformance`, décision sur la forme du champ `authority_rank` ou équivalent.
2. **Patch state d’abord** : CORR-ARB-03, CORR-ARB-05, CORR-ARB-06 (corrections pures, sans ambigüité).
3. **Patch architecture ensuite** : CORR-ARB-01, CORR-ARB-02, CORR-ARB-04 (dépendances de décisions humaines pour certains détails).
4. **Patch pipeline/governance** : CORR-ARB-07 (après décision humaine).

---

## Priorités de patch

| Priorité | Corrections |
|---|---|
| Critique | CORR-ARB-01 |
| Élevée | CORR-ARB-02, CORR-ARB-03, CORR-ARB-04, CORR-ARB-06, CORR-ARB-07 |
| Modérée | CORR-ARB-05 |
| Différée | ARB-PF-06, ARB-PF-02 (validator) |
