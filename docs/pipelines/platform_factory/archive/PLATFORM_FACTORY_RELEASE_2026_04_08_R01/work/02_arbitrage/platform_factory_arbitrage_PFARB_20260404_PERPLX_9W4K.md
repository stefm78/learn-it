# Arbitrage Proposal — Platform Factory Baseline V0

## Métadonnées

| Champ | Valeur |
|---|---|
| **arbitrage_run_id** | `PFARB_20260404_PERPLX_9W4K` |
| **date** | 2026-04-04 |
| **stage** | STAGE_02_FACTORY_ARBITRAGE |
| **pipeline** | docs/pipelines/platform_factory/pipeline.md |
| **prompt principal** | docs/prompts/shared/Make21PlatformFactoryArbitrage.md |
| **nature** | Proposition d'arbitrage — contribution multi-IA — non canonique |

---

## Challenge reports considérés

| challenge_run_id | Taille |
|---|---|
| PFCHAL_20260404_GPT54_X7K2Q | 31 440 octets |
| PFCHAL_20260404_PERPLX_7K2R | 37 616 octets |
| PFCHAL_20260404_PERPLX_A1J77P | 33 541 octets |
| PFCHAL_20260404_PERP_K7X2 | 22 155 octets |
| PFCHAL_20260404_PPLXAI_5LVBSV | 36 592 octets |
| PFCHAL_20260404_PXADV_BB1MZX | 35 528 octets |

Tous les reports ont été lus. Aucun ignoré.

---

## Résumé exécutif

Six challenge reports convergent sur un diagnostic commun : la Platform Factory V0 est **conceptuellement solide et honnête dans son auto-diagnostic**, mais **insuffisamment fermée sur trois zones structurantes** qui bloquent l'entrée en patch propre.

Le consensus inter-rapports est fort sur les priorités. Aucun rapport ne remet en cause la viabilité de la baseline ni n'exige une réécriture. Tous convergent sur le fait que V0 est **acceptable pour continuer mais pas acceptable pour industrialiser sans arbitrage**.

Les trois zones critiques unanimement identifiées :
1. **Contrat minimal d'application produite** — ne projette pas les invariants constitutionnels de runtime dans ses axes de validation.
2. **Projections dérivées** — mécanisme fort déclaré, entièrement non outillé (pas de validator, pas d'emplacement, pas de protocole de régénération).
3. **Gouvernance release/current/manifest** — artefacts présents en `docs/cores/current/` mais hors manifest officiel.

Deux zones élevées font également consensus :
4. **Protocole d'assemblage multi-IA** — exigence de premier rang non opérationnalisée.
5. **Maturité surdéclarée dans le state** — particulièrement `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED`.

Un point de divergence notable existe entre les rapports sur la criticité de la gouvernance manifest : GPT54 et PXADV la cotent « élevé » là où PERPLX_7K2R, PERPLX_A1J77P et PPLXAI_5LVBSV la cotent « critique ». L'arbitrage retient la cotation **critique** compte tenu de l'impact sur la cohérence release formelle.

Un point additionnel soulevé par PXADV_BB1MZX mais absent des autres : **STAGE_05 sans contrat d'atomicité/rollback** en lien avec `INV_NO_PARTIAL_PATCH_STATE`. Ce point est retenu au niveau **élevé** car il concerne le pipeline et non les artefacts canoniques.

---

## Synthèse des constats convergents

### Consensus fort (5 ou 6 rapports)

| Constat | Rapports |
|---|---|
| Contrat minimal ne couvre pas INV_RUNTIME_FULLY_LOCAL ni INV_NO_RUNTIME_CONTENT_GENERATION | Tous les 6 |
| Projections dérivées : pas de validator, stockage TBD, pas de protocole de régénération | Tous les 6 |
| Artefacts factory dans current mais hors manifest officiel | Tous les 6 |
| Absence de protocole d'assemblage multi-IA | Tous les 6 |
| PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED surdéclarée en capabilities_present | 5/6 (GPT54, PERPLX_7K2R, PERPLX_A1J77P, PPLXAI_5LVBSV, PXADV) |
| Séparation architecture/state correctement tenue | Tous les 6 |
| Séparation générique/spécifique globalement saine | Tous les 6 |
| PF_PRINCIPLE_NO_NORM_DUPLICATION : solide | Tous les 6 |
| Pipeline V0 suffisant pour démarrer un cycle crédible | Tous les 6 |

### Consensus modéré (3–4 rapports)

| Constat | Rapports |
|---|---|
| STAGE_07 et STAGE_08 délèguent à des specs potentiellement absentes | PERPLX_7K2R, PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV |
| Même prompt Make23 pour STAGE_04 et STAGE_06 — ambiguïté | PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PXADV |
| Absence de critères de sortie de maturité V0→V0.2 | PERP_K7X2, PPLXAI_5LVBSV |
| INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION absent du contrat minimal | PERPLX_7K2R, PERPLX_A1J77P, PPLXAI_5LVBSV, PXADV |
| Handoff contract factory → instanciation trop implicite | GPT54, PERPLX_7K2R, PERPLX_A1J77P |

### Points soulevés par un seul rapport

| Constat | Rapport | Statut arbitrage |
|---|---|---|
| STAGE_05 sans contrat d'atomicité/rollback (INV_NO_PARTIAL_PATCH_STATE) | PXADV_BB1MZX | Retenu élevé (lien constitutionnel direct) |
| Absence de lien d'appartenance run dans les challenge reports | PPLXAI_5LVBSV | Reporté — pipeline governance |
| Absence de critère de succès global du cycle pipeline | PPLXAI_5LVBSV | Reporté — pipeline governance |
| Prompt partagé STAGE_04/STAGE_06 soulevé comme bug potentiel | PERPLX_A1J77P, PPLXAI_5LVBSV | Retenu modéré |
| INV_DISTRESS_REGIME_PRIORITY_CANNOT_BE_OVERRIDDEN absent contrat | PERPLX_7K2R | Retenu modéré — hors périmètre factory pour V0 |

---

## Propositions d'arbitrage par thème

---

### ARB-01 — Contrat minimal : absence de binding constitutionnel sur les invariants runtime

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-01 |
| **Sujet** | Le contrat minimal d'une application produite (`produced_application_minimum_contract`) ne projette pas les invariants constitutionnels de runtime dans ses axes de validation minimaux ni dans son observabilité minimale. Une application peut être déclarée conforme par la factory tout en violant `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC`. |
| **Sources** | Tous les 6 challenge reports |
| **Décision** | `retained_now` |
| **Lieu principal** | architecture (`platform_factory_architecture.yaml`) |
| **Lieu secondaire** | — |
| **Priorité** | Critique |
| **Justification** | Trou normatif actif : la factory peut certifier une application inconstitutionnelle sur ses invariants les plus fondamentaux. Ce n'est pas un défaut de schéma fin (acceptable V0) mais un défaut de binding de conformité constitutionnelle explicite. Invariants touchés : au moins 5 invariants constitutionnels forts. |
| **Impact si non traité** | La factory peut produire et promouvoir des applications violant les invariants constitutionnels de runtime sans détection. Conformité constitutionnelle non certifiable. |
| **Pré-condition** | Aucune — le fond normatif est clair, la correction se fait dans les axes de validation et dans le manifest minimum. |
| **Note de séquencement** | Ce point doit être traité en premier dans le patchset. Les autres corrections le référencent. |
| **Éléments à corriger** | Ajouter dans `minimum_validation_contract.minimum_axes` un axe `constitutional_runtime_compliance` couvrant au minimum `INV_RUNTIME_FULLY_LOCAL` et `INV_NO_RUNTIME_CONTENT_GENERATION`. Ajouter dans `minimum_observability_contract.minimum_signals` un signal `runtime_locality_attestation`. L'arbitrage recommande une déclaration **probatoire** (le manifest doit asserter la conformité par ID d'invariant) et non simplement déclarative. |

---

### ARB-02 — Projections dérivées : mécanisme autorisé sans garde-fous opérationnels

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-02 |
| **Sujet** | La factory autorise l'usage des projections dérivées comme unique artefact fourni à une IA, alors que : (a) l'emplacement de stockage est `TBD`, (b) aucun validator n'est défini, (c) aucun protocole de régénération n'est spécifié, (d) aucun mécanisme d'invalidation post-patch canonique n'existe. Le risque de dérive normative silencieuse est immédiat dès le premier usage opérationnel. |
| **Sources** | Tous les 6 challenge reports |
| **Décision** | `retained_now` |
| **Lieu principal** | architecture (`platform_factory_architecture.yaml`) |
| **Lieu secondaire** | state (`platform_factory_state.yaml`), validator/tooling |
| **Priorité** | Critique |
| **Justification** | L'usage fort ("artefact unique pour une IA") est déclaré autorisé avant que les trois conditions de sécurité soient remplies. C'est une inversion de séquence : le droit d'usage précède la mise en place des gardes-fous. La V0 est acceptable sur les schémas fins, pas sur l'autorisation d'usage non gouverné d'un mécanisme central. |
| **Impact si non traité** | Dérive normative silencieuse dans les artefacts produits. Faux sentiment de conformité. Impossibilité d'auditer la fidélité d'une projection utilisée. |
| **Pré-condition** | L'emplacement doit être décidé avant que le protocole de validation puisse être spécifié. |
| **Note de séquencement** | (1) Décider l'emplacement (`emplacement_policy`) — arbitrage recommande `docs/projections/platform_factory/`. (2) Définir un schéma minimal d'identification de projection (id, version, source_hash, generated_at, scope). (3) Conditionner l'usage fort à la mise en place d'un protocole minimal de validation. En attente de ces trois sous-décisions : l'usage "artefact unique pour IA" doit être conditionnel et non actif. |
| **Éléments à corriger** | Ajouter dans `generated_projection_rules.emplacement_policy` un emplacement décidé. Ajouter dans l'architecture une note conditionnant l'usage fort à l'instrumentation. Mettre à jour `derived_projection_conformity_status` dans le state. |

---

### ARB-03 — Gouvernance release/current/manifest : trou de traçabilité formelle

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-03 |
| **Sujet** | Les artefacts `platform_factory_architecture.yaml` et `platform_factory_state.yaml` sont dans `docs/cores/current/` mais hors manifest officiel courant. Le pipeline Rule 3 les déclare "released baseline" par voie narrative sans matérialisation formelle (pas de tag git, pas de release record, pas d'entrée manifest). Ce positionnement hybride crée un trou de gouvernance reconnu mais non résolu. |
| **Sources** | Tous les 6 challenge reports |
| **Décision** | `retained_now` |
| **Lieu principal** | manifest/release governance |
| **Lieu secondaire** | state (`platform_factory_state.yaml` — metadata et blockers) |
| **Priorité** | Critique |
| **Justification** | Un acteur humain ou IA lisant `docs/cores/current/` ne peut pas distinguer les artefacts officiellement promus de ceux en cours d'intégration. Ce trou rend la protection contre modification directe non opérationnelle. La cotation est élevée à critique (consensus des 3 rapports PERPLX + PPLXAI) en raison de l'impact sur la traçabilité de release. |
| **Impact si non traité** | Risque de promotion implicite. Ambiguïté d'interprétation de l'autorité des artefacts. Impossibilité d'audit de version courante officielle. |
| **Pré-condition** | Décision sur le mode d'intégration : soit extension du manifest existant, soit manifest séparé platform_factory, soit release record minimal. |
| **Note de séquencement** | Ce point est préalable à STAGE_07 et STAGE_08. L'arbitrage recommande de documenter un **régime transitoire explicite** (release record minimal dans `docs/releases/` ou entrée dans le manifest officiel) avant tout patch. |
| **Éléments à corriger** | Créer ou référencer un artefact de release minimal pour la baseline V0 (release record + note de régime transitoire). Mettre à jour `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` dans le state avec plan de résolution explicite. |

---

### ARB-04 — Protocole d'assemblage multi-IA : exigence de premier rang non opérationnalisée

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-04 |
| **Sujet** | La factory déclare le multi-IA comme exigence structurante de premier rang (`PF_DECISION_MULTI_IA_FIRST_CLASS`). Mais les quatre éléments nécessaires à son opérationnalisation sont absents : protocole de décomposition, convention de granularité modulaire, protocole d'assemblage, protocole de résolution de conflit. |
| **Sources** | Tous les 6 challenge reports |
| **Décision** | `retained_now` (pour la définition d'un protocole minimal) |
| **Lieu principal** | architecture (`platform_factory_architecture.yaml`) |
| **Lieu secondaire** | state (`platform_factory_state.yaml`), pipeline |
| **Priorité** | Élevé |
| **Justification** | Ce cycle d'arbitrage est lui-même multi-IA. La preuve que le gap est actif existe déjà dans les 6 challenge reports produits en parallèle. Sans protocole minimal d'assemblage, les outputs parallèles peuvent être incohérents. Le déférement est acceptable pour la granularité fine mais pas pour la convention minimale d'assemblage. |
| **Impact si non traité** | Collisions silencieuses entre outputs IA. Assemblages incohérents non détectés. Impossibilité de certifier un produit multi-IA. |
| **Pré-condition** | Aucune — le fond est clair. |
| **Note de séquencement** | Arbitrage recommande un protocole **minimal** : (1) convention de nommage et de versioning des projections par scope, (2) règle de précédence en cas de conflit (version la plus récente + validation humaine), (3) point d'assemblage désigné explicitement dans le pipeline. |
| **Éléments à corriger** | Ajouter dans l'architecture un bloc `multi_ia_decomposition_minimum_protocol`. Mettre à jour le state. Ajouter une règle dans le pipeline pour le point d'assemblage. |

---

### ARB-05 — Maturité surdéclarée : PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-05 |
| **Sujet** | `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` est classée en `capabilities_present` alors que le mécanisme opérationnel (validator, emplacement, protocole de régénération) est entièrement absent. Une règle déclarée sans outillage n'est pas une capacité présente — c'est une capacité intentionnelle. |
| **Sources** | GPT54, PERPLX_7K2R, PERPLX_A1J77P, PPLXAI_5LVBSV, PXADV (5/6) |
| **Décision** | `retained_now` |
| **Lieu principal** | state (`platform_factory_state.yaml`) |
| **Lieu secondaire** | — |
| **Priorité** | Élevé |
| **Justification** | Le classement faux crée un risque d'hallucination de capacité par une IA lisant l'état. Ce rapport lui-même (et les 5 autres) démontre que la lecture de l'état peut induire en erreur. Correction simple et sans ambiguïté. |
| **Impact si non traité** | IA sur-estimant les capacités disponibles. Décisions d'arbitrage ou de release basées sur une maturité incorrecte. |
| **Pré-condition** | Aucune. |
| **Note de séquencement** | Correction à inclure dans le même patchset qu'ARB-02 (cohérence état/architecture). |
| **Éléments à corriger** | Déplacer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` de `capabilities_present` vers `capabilities_partial`. Mettre à jour le wording pour distinguer "règle d'usage définie" (présent) et "mécanisme d'exécution opérationnel" (absent). |

---

### ARB-06 — STAGE_05 : absence de contrat d'atomicité et de rollback

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-06 |
| **Sujet** | STAGE_05 (apply patchset) ne définit aucun mécanisme garantissant l'atomicité de l'application ni le comportement en cas d'échec partiel. L'invariant constitutionnel `INV_NO_PARTIAL_PATCH_STATE` exige qu'un patch soit atomique (tout ou rien). En l'état, un patch partiellement appliqué crée un état interdit. |
| **Sources** | PXADV_BB1MZX (seul rapport à l'identifier explicitement) |
| **Décision** | `retained_now` |
| **Lieu principal** | pipeline (`pipeline.md`) |
| **Lieu secondaire** | — |
| **Priorité** | Élevé |
| **Justification** | Lien constitutionnel direct avec `INV_NO_PARTIAL_PATCH_STATE`. Même si un seul rapport l'identifie, le finding est valide et sans ambiguïté. La correction dans le pipeline est simple (ajout d'une règle d'atomicité dans STAGE_05). |
| **Impact si non traité** | Un patch partiellement appliqué crée un état interdit constitutionnellement. Aucun signal pour détecter ni résoudre cet état. |
| **Pré-condition** | Aucune. |
| **Note de séquencement** | Correction pipeline indépendante, peut être traitée en parallèle des corrections architecture/state. |
| **Éléments à corriger** | Ajouter dans `pipeline.md` STAGE_05 une règle minimale d'atomicité : "tout ou rien", instruction explicite en cas d'échec partiel (nommage du fichier d'état d'erreur, signal d'arrêt). |

---

### ARB-07 — STAGE_07/STAGE_08 : vérification des specs séparées

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-07 |
| **Sujet** | Les stages les plus critiques du cycle (release materialization et promote current) délèguent à des fichiers de spec séparés (`STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`, `STAGE_08_FACTORY_PROMOTE_CURRENT.md`) dont l'existence et la complétude n'ont pas été vérifiées dans le challenge. |
| **Sources** | PERPLX_7K2R, PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV |
| **Décision** | `clarification_required` |
| **Lieu principal** | pipeline |
| **Lieu secondaire** | — |
| **Priorité** | Élevé |
| **Justification** | Si ces fichiers n'existent pas ou sont incomplets, le cycle de correction ne peut pas être mené à terme de façon gouvernée. Condition nécessaire pour qu'ARB-03 soit résolu. |
| **Impact si non traité** | Impossibilité de faire une release formelle. Contournement implicite de la gouvernance release. |
| **Pré-condition** | Vérifier l'existence et la complétude de ces deux fichiers avant le patch. Si absents, créer des stubs minimaux. |
| **Note de séquencement** | À résoudre avant STAGE_03. |

---

### ARB-08 — Handoff contract factory → instanciation

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-08 |
| **Sujet** | La frontière entre le contrat minimal générique (factory) et les responsabilités du pipeline d'instanciation aval n'est pas formalisée. Il manque un artefact ou bloc contractuel de passation. |
| **Sources** | GPT54, PERPLX_7K2R, PERPLX_A1J77P |
| **Décision** | `deferred` |
| **Lieu principal** | architecture |
| **Lieu secondaire** | — |
| **Priorité** | Modéré |
| **Justification** | Le pipeline d'instanciation n'existe pas encore. Ce handoff contract ne peut pas être finalisé avant que ce pipeline soit initié. Déférement justifié par la dépendance à un livrable aval. |
| **Impact si non traité** | Confusion sur les responsabilités à la frontière. Risque de recouvrements ou de trous lors de l'instanciation. |
| **Pré-condition** | Existence d'un début de spécification du pipeline d'instanciation. |

---

### ARB-09 — Ambiguïté prompt Make23 partagé STAGE_04 / STAGE_06

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-09 |
| **Sujet** | Le même prompt `Make23PlatformFactoryValidation.md` est assigné à STAGE_04 (validation du patchset) et STAGE_06 (validation des artefacts core patchés). Les deux stages ont des objets distincts. |
| **Sources** | PERPLX_A1J77P, PERP_K7X2, PPLXAI_5LVBSV, PXADV |
| **Décision** | `retained_now` |
| **Lieu principal** | pipeline |
| **Lieu secondaire** | — |
| **Priorité** | Modéré |
| **Justification** | Ambiguïté réelle sur l'objet de validation. Correction simple : soit deux prompts distincts, soit un prompt avec deux modes documentés explicitement. |
| **Impact si non traité** | Validation inadaptée à l'objet du stage. Confusion IA et humaine sur ce qui est validé. |
| **Pré-condition** | Aucune. |
| **Note de séquencement** | Correction pipeline en même temps qu'ARB-06. |

---

### ARB-10 — Traçabilité des versions canoniques dans les artefacts produits

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-10 |
| **Sujet** | Le contrat minimal requiert `canonical_dependencies` dans le manifest mais sans obligation de versioning exact (version ID + hash ou commit ref) au moment de la production. Il est impossible de vérifier rétrospectivement avec quelle version de la Constitution une application a été produite. |
| **Sources** | PERPLX_7K2R, PPLXAI_5LVBSV |
| **Décision** | `deferred` |
| **Lieu principal** | architecture |
| **Lieu secondaire** | — |
| **Priorité** | Modéré |
| **Justification** | Point de traçabilité réel, mais sans impact immédiat tant qu'aucune application n'est encore produite. Déférement acceptable au prochain cycle si ARB-01 est traité (le bloc constitutional_compliance peut inclure la version canonique). |
| **Impact si non traité** | Impossibilité de détecter une dérive constitutionnelle entre deux builds. Traçabilité release incomplète. |

---

### ARB-11 — Critères de sortie de maturité V0 → V0.2

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-11 |
| **Sujet** | Aucun critère de progression de V0 vers un état plus mature n'est défini dans les artefacts. Le state risque de rester `foundational_but_incomplete` sans signal de progression. |
| **Sources** | PERP_K7X2, PPLXAI_5LVBSV |
| **Décision** | `deferred` |
| **Lieu principal** | state |
| **Lieu secondaire** | — |
| **Priorité** | Modéré |
| **Justification** | Non bloquant pour ce cycle de patch. À ajouter dans le state après application du patchset courant, comme première définition de `next_maturity_target`. |
| **Impact si non traité** | Gouvernance de maturité absente. Drift silencieux de version sans signal. |

---

### ARB-12 — Fingerprints de reproductibilité : contenu non défini

| Champ | Valeur |
|---|---|
| **Decision ID** | ARB-12 |
| **Sujet** | `reproducibility_fingerprints` est déclaré requis dans le contrat minimal mais aucune définition de son contenu minimal n'est fournie. Un manifest peut remplir ce bloc avec n'importe quoi. |
| **Sources** | PPLXAI_5LVBSV, PXADV_BB1MZX |
| **Décision** | `deferred` |
| **Lieu principal** | architecture |
| **Lieu secondaire** | — |
| **Priorité** | Modéré |
| **Justification** | Déférement acceptable en V0. La correction peut être intégrée au moment où les schémas fins sont finalisés (cycle suivant). |
| **Impact si non traité** | Reproductibilité non vérifiable. Traçabilité partielle. |

---

## Points retenus (retained_now)

| ID | Sujet | Priorité | Lieu principal |
|---|---|---|---|
| ARB-01 | Contrat minimal : binding constitutionnel runtime absent | Critique | architecture |
| ARB-02 | Projections dérivées : usage fort autorisé sans garde-fous | Critique | architecture + state |
| ARB-03 | Gouvernance release/current/manifest : trou formel | Critique | manifest/release governance |
| ARB-04 | Protocole d'assemblage multi-IA absent | Élevé | architecture + state + pipeline |
| ARB-05 | Maturité surdéclarée PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED | Élevé | state |
| ARB-06 | STAGE_05 sans contrat d'atomicité/rollback | Élevé | pipeline |
| ARB-09 | Ambiguïté prompt Make23 STAGE_04 / STAGE_06 | Modéré | pipeline |

## Points différés (deferred)

| ID | Sujet | Priorité | Justification |
|---|---|---|---|
| ARB-08 | Handoff contract factory → instanciation | Modéré | Pipeline d'instanciation inexistant |
| ARB-10 | Versioning canonique exact dans les artefacts produits | Modéré | Peut être intégré à ARB-01 au cycle suivant |
| ARB-11 | Critères de sortie de maturité V0 → V0.2 | Modéré | Post-patchset courant |
| ARB-12 | Fingerprints de reproductibilité : contenu non défini | Modéré | Lors de la finalisation des schémas fins |

## Points nécessitant clarification avant patch (clarification_required)

| ID | Sujet | Clarification requise |
|---|---|---|
| ARB-07 | STAGE_07/STAGE_08 : existence et complétude des specs | Vérifier existence des fichiers STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md et STAGE_08_FACTORY_PROMOTE_CURRENT.md |

## Points hors périmètre (out_of_scope)

| Sujet | Justification |
|---|---|
| INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC dans le contrat minimal | Correctement hors périmètre factory — appartient au domaine |
| Contenu domaine-spécifique dans les projections | Hors périmètre factory — relève du pipeline d'instanciation |
| Schémas fins exact_manifest_schema, exact_configuration_schema, etc. | Acceptables comme incomplétudes V0 normales — non bloquants pour le cycle actuel |
| Absence de tooling/validateurs implémentés | Reconnu, acceptable V0 |
| Définition du pipeline d'instanciation aval | Hors périmètre factory explicitement |

---

## Corrections à arbitrer avant patch — tableau récapitulatif

| ID | Correction | Lieu | Priorité | Pré-condition |
|---|---|---|---|---|
| ARB-01 | Ajouter axe `constitutional_runtime_compliance` dans `minimum_validation_contract.minimum_axes` + signal `runtime_locality_attestation` dans observabilité | architecture | Critique | Aucune |
| ARB-02 | Décider `emplacement_policy`, conditionner l'usage fort des projections, schéma minimal d'identification | architecture + state | Critique | Décision emplacement en premier |
| ARB-03 | Créer release record minimal V0 + clarifier régime transitoire | manifest/release governance + state | Critique | Décision sur mode d'intégration manifest |
| ARB-04 | Ajouter bloc `multi_ia_decomposition_minimum_protocol` dans architecture | architecture + state + pipeline | Élevé | Aucune |
| ARB-05 | Déplacer `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` vers `capabilities_partial` | state | Élevé | Aucune |
| ARB-06 | Ajouter règle d'atomicité dans STAGE_05 | pipeline | Élevé | Aucune |
| ARB-07 | Vérifier existence STAGE_07 et STAGE_08 specs | pipeline | Élevé | Vérification manuelle |
| ARB-09 | Clarifier/séparer prompts STAGE_04 vs STAGE_06 | pipeline | Modéré | Aucune |

---

## Séquencement recommandé pour le patch

**Séquence 1 (pré-requis) :**
- ARB-07 : vérifier existence des specs STAGE_07/STAGE_08
- ARB-03 : décider mode d'intégration manifest (décision humaine requise)
- ARB-02 (sous-décision) : décider emplacement des projections dérivées (décision humaine requise)

**Séquence 2 (patches architecture, parallélisables) :**
- ARB-01 : ajouter axes de validation constitutionnels dans le contrat minimal
- ARB-02 : conditionner l'usage fort des projections + schéma d'identification
- ARB-04 : définir protocole minimal d'assemblage multi-IA

**Séquence 3 (patches state, après séquence 2) :**
- ARB-05 : reclassifier PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED
- Mise à jour cohérente des capacités suite aux corrections architecture

**Séquence 4 (patches pipeline, parallélisables avec séquence 2) :**
- ARB-06 : atomicité STAGE_05
- ARB-09 : clarification prompts Make23

**Séquence 5 (release record) :**
- ARB-03 : créer le release record minimal V0

---

## Points sans consensus ou nécessitant discussion finale

| Sujet | Nature du désaccord | Recommandation pour consolidation |
|---|---|---|
| Cotation ARB-03 (critique vs élevé) | GPT54 et PXADV cotent "élevé", les 4 autres cotent "critique" | L'arbitrage retient **critique** mais la consolidation humaine peut décider de descendre à élevé si la décision manifest est planifiée avec date |
| Mode de correction ARB-01 (déclaratif vs probatoire) | PERPLX_7K2R propose un axe déclaratif (manifest doit asserter), PPLXAI_5LVBSV propose probatoire (validator doit vérifier) | L'arbitrage recommande **probatoire** en principe, **déclaratif** comme palier V0 acceptable, à décider humainement |
| Emplacement des projections dérivées (ARB-02) | PERPLX_A1J77P suggère `docs/projections/platform_factory/`, PERP_K7X2 suggère `docs/pipelines/platform_factory/projections/` | Décision humaine requise — les deux sont acceptables architecturalement |
| ARB-08 (deferred vs retained) | PERPLX_7K2R le classe en modéré immédiat, les autres l'acceptent comme déféré | L'arbitrage retient **deferred** mais la consolidation peut choisir de le retenir au modéré si un pipeline d'instanciation est en cours |

---

## Priorités de patch — vue synthétique

### Critique
- ARB-01 : Contrat minimal — binding constitutionnel runtime
- ARB-02 : Projections dérivées — usage fort sans garde-fous
- ARB-03 : Gouvernance release/current/manifest

### Élevé
- ARB-04 : Protocole d'assemblage multi-IA
- ARB-05 : Maturité surdéclarée state
- ARB-06 : STAGE_05 atomicité/rollback
- ARB-07 : Vérification specs STAGE_07/STAGE_08 (clarification requise)

### Modéré
- ARB-09 : Ambiguïté prompts STAGE_04/STAGE_06
- ARB-10 : Versioning canonique (déféré)
- ARB-11 : Critères de sortie maturité (déféré)
- ARB-12 : Fingerprints de reproductibilité (déféré)

### Faible (accepté V0)
- Schémas fins non finalisés
- Validateurs non implémentés
- Pipeline d'instanciation absent
- Granularité modulaire non définie
- Absence de critère de succès global pipeline

---

## Points V0 explicitement acceptables

Les éléments suivants sont des incomplétudes V0 normales, reconnues dans les artefacts, sans risque immédiat :

- `exact_manifest_schema`, `exact_runtime_typology`, `exact_configuration_schema`, `exact_packaging_schema` : correctement en `capabilities_absent` / `known_gaps`.
- `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` absent : reconnu, cohérent avec V0.
- Pipeline d'instanciation aval : hors périmètre assumé.
- Granularité modulaire fine : déférée, acceptable.
- Absence d'evidence externe (test, review pair) : normal pour un V0 initial.
- Séparation architecture/state : bien tenue, solide.
- Séparation générique/domaine : solide et bien bornée.
- `PF_PRINCIPLE_NO_NORM_DUPLICATION` : solide, pas de contamination.

---

*Proposition d'arbitrage générée par PERPLX (Perplexity AI — Sonnet 4.6) — STAGE_02_FACTORY_ARBITRAGE — 2026-04-04*
*Cette proposition n'est pas l'arbitrage canonique final. Elle est une contribution exploitable par une consolidation finale humaine-assistée.*
*Aucun patch YAML inclus. Aucune décision humaine substituée.*
