# Arbitrage Report — Platform Factory Baseline V0.1

| Champ | Valeur |
|---|---|
| **arbitrage_run_id** | `PFARB_20260404_PERPLX_K9M2` |
| **date** | 2026-04-04 |
| **pipeline** | docs/pipelines/platform_factory/pipeline.md — STAGE_02_FACTORY_ARBITRAGE |
| **agent** | PERPLX (Perplexity AI — Sonnet 4.6) |
| **challenge_reports_sources** | PFCHAL_20260404_PERPLX_A1J77P · PFCHAL_20260404_PERP_K7X2 · PFCHAL_20260404_PPLXAI_5LVBSV · PFCHAL_20260404_PXADV_BB1MZX |
| **destinataire_stage_suivant** | STAGE_03_FACTORY_PATCH_SYNTHESIS |

---

## Résumé d'arbitrage

Quatre challenge reports ont été produits par des instances PERPLX distinctes sur la baseline Platform Factory V0.1. Les findings sont remarquablement convergents : absence d'attestation constitutionnelle runtime dans le contrat minimal, projections dérivées non opérationnalisées, protocole multi-IA absent, maturité surdéclarée dans l'état, ambiguïté de gouvernance release. Un cinquième sujet (atomicité STAGE_05) est identifié par un seul rapport (PXADV) avec une gravité élevée légitime.

**Décision globale d'arbitrage** : 11 décisions sont rendues dans ce rapport. 6 sont retenues pour patch immédiat. 2 sont reportées avec wording corrigé. 1 est partiellement retenue avec clarification préalable. 1 est rejetée comme hors périmètre factory au niveau architecture. 1 est transformée en exigence pipeline sans patch YAML.

La baseline reste patchable et ne nécessite pas de refonte. Le périmètre du patchset est borné.

---

## Findings consolidés

### FC-01 — Absence d'attestation constitutionnelle runtime dans le contrat minimal d'application

**Sources** : tous les 4 rapports — A1J77P (Axe 4), K7X2 (C1), 5LVBSV (C-01), BB1MZX (C1)

**Consensus** : unanime. La factory déclare ses dépendances constitutionnelles mais ne les projette pas dans les axes de validation du `produced_application_minimum_contract`. Une application produite peut être déclarée conforme sans attester `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`.

**Nuance de formulation** : A1J77P soulève spécifiquement l'absence de binding sur `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` comme point distinct ; 5LVBSV et BB1MZX l'incluent dans la famille « runtime ». Ces deux formulations sont compatibles — elles seront fusionnées dans la décision.

**Désaccord de gravité** : K7X2 classe ce risque « critique » mais dans la catégorie des défauts à arbitrer avant patch ; 5LVBSV et BB1MZX le classent aussi « critique ». A1J77P le traite dans les « faiblesses structurelles dépassant le seuil V0 ». **Arbitrage : critique confirmé**.

---

### FC-02 — Projections dérivées : emplacement TBD, validateur absent, protocole de régénération absent

**Sources** : tous les 4 rapports — A1J77P (Axe 5), K7X2 (C2), 5LVBSV (C-02), BB1MZX (C2)

**Consensus** : unanime. L'emplacement des `validated_derived_execution_projections` est TBD dans l'architecture. Il n'existe pas de validator, pas de protocole de régénération déterministe, pas de mécanisme d'invalidation post-patch.

**Désaccord mineur** : 5LVBSV et A1J77P signalent que le risque est « actif dès le premier usage IA » et refusent de le classer comme « défaut V0 acceptable ». K7X2 et BB1MZX acceptent le déférement de l'outillage mais insistent sur la décision d'emplacement et d'un protocole minimal. **Arbitrage** : la décision d'emplacement et un protocole minimal de validation sont retenus maintenant ; le validator automatisé complet est reporté.

---

### FC-03 — Protocole d'assemblage multi-IA absent

**Sources** : tous les 4 rapports — A1J77P (Axe 7), K7X2 (C3), 5LVBSV (E-02), BB1MZX (C3)

**Consensus** : unanime. L'absence de `decomposition_protocol`, `ai_output_assembly_protocol` et `conflict_resolution_protocol` est reconnue. La factory déclare multi-IA comme exigence de premier rang mais l'opérationnalisation est absente.

**Désaccord de classification** : BB1MZX signale que l'absence n'est pas classée comme blocker de niveau suffisant dans le state malgré l'importance de l'exigence. A1J77P identifie l'absence de borne temporelle ou de condition déclenchante. **Arbitrage** : `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` doit être promu en blocker (severity: medium) dans le state ; un protocole minimal d'assemblage est retenu pour patch architecture (scope minimal, pas de spec complète) ; granularité modulaire reportée.

---

### FC-04 — Maturité surdéclarée dans capabilities_present

**Sources** : A1J77P (Axe 6), K7X2 (E-03), 5LVBSV (E-03), BB1MZX (C6)

**Consensus** : fort. `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` est classée `capabilities_present` alors que le mécanisme est entièrement absent. Formulations concordantes dans les 4 rapports.

**Extension** : A1J77P identifie aussi `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` comme surdéclarée (6 open_points non résolus). K7X2 identifie `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`. 5LVBSV identifie `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` et `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`. BB1MZX se concentre sur `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`.

**Arbitrage** : `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` est retenue pour reclassification en `capabilities_partial`. `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` : la surdéclaration est réelle mais la formulation de A1J77P est trop sévère — le scope est défini dans ses bornes génériques même si ses composants sont ouverts ; **reclassification non retenue** pour cette capacité, mais un commentaire doit clarifier les open_points. `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` : acceptable en `present` si lue strictement comme intention ; **pas de reclassification** mais ajout d'une note.

---

### FC-05 — Artefacts V0 dans docs/cores/current/ hors manifest officiel

**Sources** : tous les 4 rapports — A1J77P (Axe 8), K7X2 (C6), 5LVBSV (C-03), BB1MZX (C7)

**Consensus** : unanime. Les artefacts sont dans `docs/cores/current/` mais n'apparaissent pas dans le manifest officiel courant. La Rule 3 du pipeline les déclare « released baseline » sans matérialisation formelle.

**Désaccord de gravité** : 5LVBSV classe ce point « critique » ; les autres le classent « modéré » ou « basse-moyenne ». **Arbitrage** : la situation est un bloqueur de gouvernance réel mais non bloquant pour le patch lui-même. Elle ne sera pas corrigée par un patch YAML de contenu mais par une décision de gouvernance explicite et un bloqueur promu dans le state.

---

### FC-06 — Atomicité de STAGE_05 (apply) non documentée

**Source unique** : BB1MZX (C4)

**Non repris** par les 3 autres rapports. Point légitime : l'absence de contrat d'atomicité dans STAGE_05 crée un risque de violation de `INV_NO_PARTIAL_PATCH_STATE` lors d'un patch partiellement appliqué.

**Arbitrage** : finding confirmé, légitime. Correction appartient au pipeline, pas à l'architecture ou au state. Retenu comme exigence pipeline.

---

### FC-07 — Fingerprints de reproductibilité non définis

**Sources** : 5LVBSV (E-01), BB1MZX (C5)

**Non repris** explicitement par A1J77P et K7X2 (ils l'intègrent dans la famille « obligations trop floues »).

**Arbitrage** : finding confirmé. Les `reproducibility_fingerprints` sont déclarés requis sans définition de contenu minimal. Correction d'architecture retenue mais classée modérée.

---

### FC-08 — Ambiguïté prompt STAGE_04 / STAGE_06 (même prompt partagé)

**Sources** : A1J77P (Axe 9), 5LVBSV (M-01), BB1MZX (implicite)

**Arbitrage** : finding confirmé, scope pipeline uniquement. Le fait que STAGE_04 et STAGE_06 partagent `Make23PlatformFactoryValidation.md` est acceptable en V0 si le pipeline précise le paramétrage différent. Correction : ajout d'une note dans `pipeline.md` distinguant l'objet des deux stages. Non retenu comme patch YAML.

---

### FC-09 — Absence de critères de sortie de maturité V0 → V0.2

**Sources** : K7X2 (C4), 5LVBSV (Axe 6)

**Arbitrage** : finding confirmé. Le state ne définit pas de `exit_criteria` ou `next_maturity_target` par couche. Sans cela, la progression de maturité ne peut pas être gouvernée. Retenu pour patch state, classé modéré.

---

### FC-10 — Absence de lien run_id entre challenge reports et exécutions pipeline

**Source** : 5LVBSV (M-02)

**Arbitrage** : finding légitime, scope pipeline et gouvernance. Non retenu comme patch YAML architecture/state. À traiter dans `pipeline.md` comme règle de nommage et de filtrage des reports par run_id.

---

### FC-11 — Contrat bootstrap_contract et runtime_entrypoint_contract non définis

**Sources** : A1J77P (Axe 4), K7X2 (C1 implicite), 5LVBSV (E-01), BB1MZX (C5 implicite)

**Arbitrage** : finding confirmé. `runtime_entrypoint_contract.bootstrap_contract` est déclaré obligatoire mais sans définition de contenu. C'est une lacune d'implémentabilité réelle pour les IA. Retenu pour patch architecture, classé modéré — le contenu minimal doit être défini même sommairement.

---

## Décisions immédiates

### D-01 — Axe de validation constitutionnel runtime

| Champ | Valeur |
|---|---|
| **Decision ID** | D-01 |
| **Sujet** | Absence d'axe de validation `constitutional_runtime_constraints` dans `minimum_validation_axes` du contrat minimal d'application |
| **Source(s)** | FC-01 — tous les 4 rapports |
| **Décision** | **retained_now** |
| **Lieu principal** | `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.minimum_validation_contract.minimum_axes` |
| **Lieu(x) secondaire(s)** | `platform_factory_state.yaml` → mise à jour du statut du contrat minimal |
| **Priorité** | **Critique** |
| **Justification** | Cinq invariants constitutionnels majeurs (`INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_NO_PARTIAL_PATCH_STATE`) ne sont pas couverts par les axes de validation du contrat minimal. La factory peut certifier une application non conforme à la Constitution. Ce n'est pas un défaut V0 acceptable. |
| **Forme du patch** | Ajouter un axe `constitutional_runtime_constraints` dans `minimum_axes`. Cet axe doit exiger une attestation **déclarative** dans le manifest (l'application déclare positivement sa conformité aux invariants listés). L'attestation probatoire (validateur automatique) est reportée. |
| **Impact si non traité** | Application produite potentiellement non constitutionnelle sans détection possible. La certification factory est trompeuse. |
| **Pré-condition** | Aucune. La liste des invariants concernés est connue et fermée. |
| **Note de séquencement** | À traiter en premier dans le patchset — conditionne la cohérence des autres corrections du contrat minimal. |

---

### D-02 — Décision d'emplacement des projections dérivées + protocole minimal de validation

| Champ | Valeur |
|---|---|
| **Decision ID** | D-02 |
| **Sujet** | `emplacement_policy.status: TBD` pour les validated_derived_execution_projections + absence de protocole minimal de validation avant usage |
| **Source(s)** | FC-02 — tous les 4 rapports |
| **Décision** | **retained_now** (emplacement + protocole minimal) — validator automatisé complet : **deferred** |
| **Lieu principal** | `platform_factory_architecture.yaml` → `generated_projection_rules.emplacement_policy` |
| **Lieu(x) secondaire(s)** | `platform_factory_state.yaml` → `derived_projection_conformity_status` ; mise à jour de `capabilities_partial` |
| **Priorité** | **Élevé** |
| **Justification** | Une projection sans emplacement stable ne peut pas être utilisée de façon déterministe par plusieurs IA. Le principe « une projection peut être l'unique artefact fourni à une IA » est intenable sans emplacement fixe. Le validator automatique complet est accepté comme déféré V0, mais la décision d'emplacement et un critère minimal de validation (ex. : déclaration de version et de SHA du canonique source au moment de la génération) doivent être posés maintenant. |
| **Forme du patch** | (a) Décider d'un chemin de stockage dans architecture (proposition : `docs/pipelines/platform_factory/projections/`) ; (b) Définir dans `execution_projection_contract` un `minimal_validation_requirement` : toute projection doit porter en en-tête le SHA du canonique source et la date de génération ; (c) Mettre à jour `derived_projection_conformity_status` dans le state. |
| **Impact si non traité** | Drift normatif silencieux entre projections et canonique. Les IA travaillent sur des projections périmées ou non localisables. |
| **Pré-condition** | Aucune bloquante. |
| **Note de séquencement** | Traiter après D-01. L'emplacement des projections est indépendant du contrat minimal d'application. |

---

### D-03 — Protocole minimal d'assemblage multi-IA + reclassification du gap en blocker

| Champ | Valeur |
|---|---|
| **Decision ID** | D-03 |
| **Sujet** | Absence de protocole d'assemblage des sorties IA ; `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` non classé en blocker |
| **Source(s)** | FC-03 — tous les 4 rapports |
| **Décision** | **retained_now** (protocole minimal + reclassification en blocker) — spec complète de granularité modulaire : **deferred** |
| **Lieu principal** | `platform_factory_architecture.yaml` → `multi_ia_parallel_readiness` (nouveau bloc `minimum_assembly_protocol`) |
| **Lieu(x) secondaire(s)** | `platform_factory_state.yaml` → promotion de `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en `blockers` (severity: medium) |
| **Priorité** | **Élevé** |
| **Justification** | La factory déclare multi-IA comme exigence de premier rang. L'absence complète de tout protocole d'assemblage rend cette promesse non tenue de façon dangereuse si des IA parallèles sont lancées. Un protocole minimal (règles de nommage des outputs, source de vérité unique pour la version canonique déclarée, point d'assemblage désigné) est nécessaire maintenant. La granularité modulaire fine est acceptée comme déférée. |
| **Forme du patch** | Ajouter un bloc `minimum_assembly_protocol` dans `multi_ia_parallel_readiness` de l'architecture, avec : (a) règle d'identification unique des outputs IA (naming convention) ; (b) source de vérité canonique unique (version déclarée une seule fois dans un artefact maître) ; (c) point d'assemblage désigné (fichier ou répertoire de merge) ; (d) règle de précédence humaine en cas de conflit non résolvable. Promouvoir le gap en blocker dans le state. |
| **Impact si non traité** | Deux IA en parallèle peuvent produire des outputs incompatibles sans mécanisme de détection. |
| **Pré-condition** | Aucune bloquante. |
| **Note de séquencement** | Peut être traité en parallèle avec D-01 et D-02. |

---

### D-04 — Reclassification de PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED

| Champ | Valeur |
|---|---|
| **Decision ID** | D-04 |
| **Sujet** | `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` classée `capabilities_present` alors que le mécanisme est absent |
| **Source(s)** | FC-04 — tous les 4 rapports |
| **Décision** | **retained_now** |
| **Lieu principal** | `platform_factory_state.yaml` → déplacer de `capabilities_present` vers `capabilities_partial` |
| **Lieu(x) secondaire(s)** | Aucun |
| **Priorité** | **Élevé** |
| **Justification** | Une règle définie mais non outillée n'est pas une capacité opérationnelle présente. Le wording actuel peut amener une IA à sur-estimer la maturité des projections. La reclassification est une correction de wording de maturité, pas un changement normatif. |
| **Forme du patch** | Déplacer l'entrée dans `capabilities_partial` avec description distinguant « règle d'usage déclarée dans l'architecture » (présent) et « mécanisme de validation et de stockage » (absent). |
| **Impact si non traité** | IA peut traiter les projections comme validables alors qu'aucun mécanisme ne l'assure. |
| **Pré-condition** | Aucune. |

---

### D-05 — Gouvernance release : clarification du statut des artefacts V0 en current

| Champ | Valeur |
|---|---|
| **Decision ID** | D-05 |
| **Sujet** | Artefacts V0 dans `docs/cores/current/` hors manifest officiel — ambiguïté de gouvernance |
| **Source(s)** | FC-05 — tous les 4 rapports |
| **Décision** | **retained_now** (documentation explicite de la voie de régularisation dans le state) — intégration au manifest officiel : **deferred** (STAGE_07/08) |
| **Lieu principal** | `platform_factory_state.yaml` → `blockers.PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` (enrichir avec voie de régularisation explicite) |
| **Lieu(x) secondaire(s)** | `pipeline.md` (note dans Rule 3 et STAGE_08 sur la régularisation des artefacts V0) |
| **Priorité** | **Modéré** |
| **Justification** | La situation est reconnue dans le state mais sans voie de résolution documentée. La différence de gravité entre les rapports (« critique » dans 5LVBSV vs « modéré » dans les autres) est arbitrée en faveur de « modéré » car la Rule 3 du pipeline pose une décision narrative explicite qui suffit en V0 — la correction principale est de documenter que la régularisation formelle passera par STAGE_07/08 lors du premier run complet. |
| **Forme du patch** | Enrichir `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` dans le state avec un champ `resolution_path` décrivant la voie (régularisation via STAGE_07/08 du premier run complet de pipeline). |
| **Impact si non traité** | Ambiguïté persistante sur le statut officiel. Un agent IA peut interpréter les artefacts comme non autorisés ou comme officiels, selon sa lecture. |
| **Pré-condition** | Aucune pour la documentation. L'intégration au manifest est conditionnée à la complétion de STAGE_07/08. |

---

### D-06 — Fingerprints de reproductibilité : définition du contenu minimal

| Champ | Valeur |
|---|---|
| **Decision ID** | D-06 |
| **Sujet** | `reproducibility_fingerprints` déclaré requis sans définition de contenu minimal |
| **Source(s)** | FC-07 — 5LVBSV, BB1MZX |
| **Décision** | **retained_now** |
| **Lieu principal** | `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.identity` |
| **Lieu(x) secondaire(s)** | Aucun |
| **Priorité** | **Modéré** |
| **Justification** | Une obligation sans définition de contenu minimal n'est pas vérifiable. Une IA peut satisfaire l'obligation avec un bloc vide. La définition minimale peut rester légère (ex. : SHA des artefacts canoniques sources + version des projections dérivées utilisées) sans bloquer la V0. |
| **Forme du patch** | Ajouter dans l'architecture une définition minimale des `reproducibility_fingerprints` : contenu requis = SHA des artefacts canoniques sources, identifiants des projections dérivées utilisées (si applicables), hash du manifest lui-même. |
| **Impact si non traité** | Reproductibilité déclarée mais non auditable. Traçabilité de release incomplète. |

---

### D-07 — Bootstrap contract : définition minimale obligatoire

| Champ | Valeur |
|---|---|
| **Decision ID** | D-07 |
| **Sujet** | `runtime_entrypoint_contract.bootstrap_contract` déclaré requis mais non défini |
| **Source(s)** | FC-11 — A1J77P, 5LVBSV, BB1MZX |
| **Décision** | **retained_now** |
| **Lieu principal** | `platform_factory_architecture.yaml` → `contracts.produced_application_minimum_contract.runtime_entrypoint_contract` |
| **Lieu(x) secondaire(s)** | Aucun |
| **Priorité** | **Modéré** |
| **Justification** | Une obligation contractuelle non définie empêche une IA de produire un artefact conforme. Le bootstrap_contract doit avoir à minima une définition de ses blocs attendus (ex. : liste des prérequis runtime, déclaration des modules activés au démarrage, déclaration de localité). La spec détaillée de la typology reste hors scope V0. |
| **Forme du patch** | Définir dans l'architecture un `minimum_bootstrap_contract_blocks` listant les blocs minimaux requis : déclaration de prérequis runtime, liste des modules activés, déclaration de localité du runtime. |
| **Impact si non traité** | IA ne sait pas quoi produire pour satisfaire cette obligation. Manifests divergents entre IA. |

---

## Reports assumés

### R-01 — Validator automatisé de projections dérivées

| Champ | Valeur |
|---|---|
| **Sujet** | Implémentation d'un validateur automatique de conformité des projections dérivées |
| **Source(s)** | FC-02 |
| **Décision** | **deferred** |
| **Justification** | L'emplacement et le protocole minimal sont retenus (D-02). Le validator automatisé nécessite un investissement de tooling non justifié pour un V0. Reconnu dans `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent`. Report assumé explicitement. |
| **Condition de déclenchement** | Avant tout usage opérationnel des projections dérivées comme seul artefact IA pour un travail de production. |
| **Wording dans l'état** | Maintenir `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED: absent` ; ajouter une note sur la condition de déclenchement du développement. |

---

### R-02 — Granularité modulaire multi-IA

| Champ | Valeur |
|---|---|
| **Sujet** | Définition de la granularité optimale des modules pour le travail multi-IA |
| **Source(s)** | FC-03 |
| **Décision** | **deferred** |
| **Justification** | Correctement identifié dans `deferred_challenges`. Le protocole minimal d'assemblage (D-03) est retenu. La granularité fine nécessite une connaissance des cas d'usage réels d'instanciation qui n'existent pas encore en V0. |
| **Condition de déclenchement** | Dès que le premier pipeline d'instanciation domaine est en préparation. |

---

### R-03 — Intégration au manifest officiel courant

| Champ | Valeur |
|---|---|
| **Sujet** | Extension du manifest officiel pour inclure les artefacts platform_factory |
| **Source(s)** | FC-05 |
| **Décision** | **deferred** (STAGE_07/08 du premier run complet) |
| **Justification** | La décision de régularisation est documentée (D-05). L'intégration effective au manifest nécessite la complétion du cycle release/promote. Report borné dans le temps (prochain run complet de pipeline). |

---

### R-04 — Critères de sortie de maturité par couche

| Champ | Valeur |
|---|---|
| **Sujet** | Définition de `exit_criteria` ou `next_maturity_target` par couche dans le state |
| **Source(s)** | FC-09 |
| **Décision** | **deferred** avec wording corrigé dans state |
| **Justification** | Les critères de progression ne peuvent pas être définis de façon utile avant la complétion d'au moins un cycle de patch. Mais le state doit explicitement noter l'absence de critères de sortie pour éviter tout faux sentiment de fermeture. Correction : ajouter une note `progression_criteria_status: not_yet_defined` dans `last_assessment`. |
| **Condition de déclenchement** | Après le premier cycle de patch complet (V0.2). |

---

## Clarifications requises avant patch

### CL-01 — Forme de l'attestation constitutionnelle runtime (déclarative vs probatoire)

| Champ | Valeur |
|---|---|
| **Sujet** | Pour l'axe `constitutional_runtime_constraints` (D-01) : l'attestation doit-elle être déclarative (assertion dans le manifest) ou probatoire (résultat d'un validateur) ? |
| **Statut** | **Clarification requise avant patch final — arbitrage recommandé ici** |
| **Arbitrage PERPLX** | En V0, l'attestation **déclarative** est la seule forme implémentable sans validator outillé. L'attestation probatoire est reportée avec le validator (R-01). Le patch doit donc introduire dans le manifest une section `constitutional_runtime_assertions` avec des déclarations booléennes (ex. : `runtime_fully_local: true`, `no_runtime_content_generation: true`). **Décision : déclarative maintenant, probatoire déférée.** |
| **Impact sur le patch** | Le patcher peut procéder sans clarification humaine supplémentaire sur ce point, en appliquant la décision ci-dessus. |

---

### CL-02 — Périmètre exact du minimum_bootstrap_contract_blocks (D-07)

| Champ | Valeur |
|---|---|
| **Sujet** | La définition minimale du bootstrap_contract doit-elle couvrir la localité du runtime ou rester à un niveau purement structurel (blocs) ? |
| **Arbitrage PERPLX** | Le bootstrap_contract doit inclure une déclaration de localité comme bloc minimal requis, conformément à D-01 (constitution runtime). Ce n'est pas une surcharge — c'est la conséquence directe de D-01. **Décision : inclure `runtime_locality_declaration` dans les blocs minimaux du bootstrap_contract.** |
| **Impact sur le patch** | Coordonner le patch D-07 avec D-01 pour éviter la redondance. |

---

## Rejet

### REJ-01 — Reclassification de PF_CAPABILITY_FACTORY_SCOPE_DEFINED

| Champ | Valeur |
|---|---|
| **Sujet** | A1J77P propose de reclasser `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` hors `capabilities_present` au motif que 6 open_points structurants sont non résolus |
| **Décision** | **rejected** |
| **Justification** | La portée de la factory (ce qu'elle est et n'est pas) est correctement définie dans ses bornes génériques. Les 6 open_points concernent des composants internes (schemas, validators) et non la définition de la portée elle-même. La capacité est présente dans son sens strict. Reclasser cette capacité introduirait une confusion entre « portée définie » et « portée outillée ». Une note de clarification dans le state est suffisante. |
| **Alternative** | Ajouter dans la description de `PF_CAPABILITY_FACTORY_SCOPE_DEFINED` une note : « La portée est définie dans ses bornes génériques. 6 composants internes restent non résolus (cf. open_points_for_challenge dans l'architecture). » |

---

## Répartition par lieu de correction

| Decision | Lieu principal | Lieu(s) secondaire(s) |
|---|---|---|
| D-01 | architecture | state |
| D-02 | architecture | state |
| D-03 | architecture | state, pipeline |
| D-04 | state | — |
| D-05 | state | pipeline |
| D-06 | architecture | — |
| D-07 | architecture | — |
| R-04 (wording) | state | — |
| REJ-01 (note alternative) | state | — |
| FC-06 (atomicité STAGE_05) | pipeline | — |
| FC-08 (ambiguïté STAGE_04/06) | pipeline | — |
| FC-10 (run_id challenge reports) | pipeline | — |

---

## Séquencement recommandé

1. **Bloc 1 (architecture)** — D-01, D-02, D-03, D-06, D-07 : patcher architecture en un seul STAGE_03. Ces cinq décisions touchent l'architecture et peuvent être traitées dans le même patchset.
2. **Bloc 2 (state)** — D-04, D-05, R-04 (wording), note REJ-01 : patcher state en même temps ou immédiatement après architecture.
3. **Bloc 3 (pipeline)** — FC-06, FC-08, FC-10 : corrections de pipeline.md — peuvent être traitées dans le même run de STAGE_03 ou dans un run séparé dédié au pipeline.
4. **STAGE_04 → STAGE_06 → STAGE_07 → STAGE_08** : cycle normal après validation du patchset.

---

## Priorités de patch

| Priorité | Decision ID | Sujet | Lieu |
|---|---|---|---|
| **Critique** | D-01 | Axe de validation constitutionnel runtime dans le contrat minimal | architecture |
| **Élevé** | D-02 | Emplacement projections dérivées + protocole minimal de validation | architecture + state |
| **Élevé** | D-03 | Protocole minimal assemblage multi-IA + reclassification en blocker | architecture + state |
| **Élevé** | D-04 | Reclassification PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED | state |
| **Modéré** | D-05 | Voie de régularisation release/manifest documentée dans state | state |
| **Modéré** | D-06 | Définition minimale fingerprints de reproductibilité | architecture |
| **Modéré** | D-07 | Définition minimale bootstrap_contract blocks | architecture |
| **Modéré** | FC-06 | Atomicité STAGE_05 (apply) | pipeline |
| **Faible** | R-04 | Note progression_criteria_status dans state | state |
| **Faible** | FC-08 | Note STAGE_04 vs STAGE_06 dans pipeline | pipeline |
| **Faible** | FC-10 | Lien run_id dans challenge reports | pipeline |
| **Rejeté** | REJ-01 | Reclassification PF_CAPABILITY_FACTORY_SCOPE_DEFINED | — |

---

## Notes finales

Ce rapport ne contient aucun patch YAML.
Il ne contient aucune réécriture des artefacts canoniques.
Il constitue l'input de STAGE_03_FACTORY_PATCH_SYNTHESIS.

Les décisions D-01 à D-07 sont prêtes à patcher sans clarification humaine supplémentaire.
Les reports R-01 à R-04 sont assumés et bornés en condition de déclenchement.
Le rejet REJ-01 est expliqué et une alternative de wording est proposée.

---

_Rapport généré par PERPLX (Perplexity AI — Sonnet 4.6) — STAGE_02_FACTORY_ARBITRAGE — 2026-04-04_
_challenge_run_ids consommés : PFCHAL_20260404_PERPLX_A1J77P · PFCHAL_20260404_PERP_K7X2 · PFCHAL_20260404_PPLXAI_5LVBSV · PFCHAL_20260404_PXADV_BB1MZX_
_Destiné à STAGE_03_FACTORY_PATCH_SYNTHESIS._
