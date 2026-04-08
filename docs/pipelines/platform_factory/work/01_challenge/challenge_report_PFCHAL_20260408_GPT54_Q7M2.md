# Challenge Report — Platform Factory Stage 01

## challenge_run_id

`PFCHAL_20260408_GPT54_Q7M2`

## Date

2026-04-08

## Artefacts challengés

- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Socle canonique lu avant challenge :
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

Pipeline lu :
- `docs/pipelines/platform_factory/pipeline.md`

## Résumé exécutif

La baseline `platform_factory` est suffisamment structurée pour justifier un cycle de gouvernance dédié, mais elle n’est pas encore assez probante pour soutenir sans risque une factory réellement exécutable par plusieurs IA ni pour prouver constitutionnellement la conformité d’une application produite.

Les forces V0 sont réelles : séparation architecture/state, périmètre générique plutôt bien borné, dépendances canoniques explicites, reconnaissance explicite de plusieurs lacunes, et cadrage clair de la distinction entre générique et spécifique.

Les fragilités prioritaires sont toutefois nettes :

1. **Le contrat minimal d’application produite n’est pas encore probant vis-à-vis des invariants constitutionnels critiques** : il impose un manifest, un entrypoint, de la validation et de l’observabilité, mais ne force pas encore de preuve explicite de conformité sur le runtime 100 % local, l’absence d’appel réseau temps réel, l’absence de génération runtime interdite, ni la qualification off-session des signaux sensibles.
2. **Le mécanisme de `validated_derived_execution_projection` est normativement affirmé mais pas encore suffisamment fermé** : pas de validator défini, pas d’emplacement arrêté, pas de protocole de régénération détaillé, pas de mécanisme probant contre omission, paraphrase dangereuse ou promotion implicite comme source primaire.
3. **La gouvernance release/manifest est ambiguë** : le pipeline traite la baseline comme released, mais les artefacts se déclarent `RELEASE_CANDIDATE`, et ils sont présents dans `docs/cores/current/` tout en étant explicitement hors du manifest courant officiel.
4. **La readiness multi-IA est reconnue comme exigence, mais pas encore gouvernée comme capacité opérable** : il manque le protocole de décomposition, d’assemblage, de résolution de conflits et de granularité modulaire.
5. **Le pipeline V0 est gouvernable, mais pas encore assez outillé pour empêcher l’improvisation de l’IA sur les points sensibles**, notamment sur la validation probante des projections dérivées et du contrat minimal d’application produite.

Conclusion : la baseline est **fondatrice mais incomplète**. Elle peut légitimement entrer en arbitrage, mais elle ne doit pas encore être considérée comme une factory released au sens fort tant que les points de preuve normative, de manifest gouverné et de tooling minimal ne sont pas refermés.

## Carte de compatibilité constitutionnelle

| Invariant / exigence | Élément factory concerné | Binding | Lecture | Risque principal |
|---|---|---|---|---|
| Runtime 100 % local | `produced_application_minimum_contract`, `dependencies_to_constitution.local_runtime_constraints` | implicite faible | La contrainte est rappelée au niveau dépendance, mais pas encore matérialisée comme obligation probante dans le contrat minimal | Une application produite peut sembler conforme sans preuve explicite d’absence d’appel réseau temps réel |
| Absence d’appel IA continu / dépendance réseau temps réel | `runtime_entrypoint_contract`, `minimum_validation_contract` | ambigu | L’entrypoint est exigé, mais aucune validation explicite de politique runtime n’est imposée | Application validée structurellement mais non constitutionnelle en usage |
| Absence de génération de contenu runtime | `minimum_validation_contract`, `minimum_observability_contract` | ambigu | Les exigences restent trop génériques pour prouver l’interdiction de génération runtime | Faux sentiment de conformité constitutionnelle |
| Absence de génération de feedback runtime hors templates autorisés | `generated_projection_rules`, `minimum_validation_contract` | absent/indirect | Rien n’impose encore un axe de validation dédié au feedback runtime interdit | Une application peut réintroduire une logique générative locale ou distante sans être bloquée |
| Séparation Constitution / Référentiel | `source_of_authority`, `design_principles.PF_PRINCIPLE_NO_NORM_DUPLICATION` | explicite | Point plutôt solide dans l’architecture | Risque limité à ce stade |
| Validation locale déterministe des patchs / transformations | `PF_PRINCIPLE_DETERMINISTIC_TRANSFORMATIONS`, `transformation_chain` | explicite mais incomplet | Le principe est là, le protocole outillé ne l’est pas encore | Déterminisme déclaré mais non démontré |
| Artefacts de patch précomputés, validés et empaquetés hors session | `build_and_packaging_rules`, `observability_requirements.factory_level.patch_execution_trace` | implicite faible | La factory trace le patch mais ne démontre pas encore la séparation probante off-session/runtime | Risque de glissement de logique de préparation vers l’exécution |
| Traçabilité explicite des dépendances canoniques | `source_of_authority`, `manifest.minimum_contents.canonical_dependencies` | explicite | Solide au niveau intentionnel | Besoin d’un schéma probant pour devenir auditable |
| Absence d’état partiel interdit | `PF_PRINCIPLE_DETERMINISTIC_TRANSFORMATIONS`, pipeline Stage 05 sandbox + Stage 08 promotion distincte | explicite partiel | Bonne direction de gouvernance | Pas encore prouvé par validator factory dédié |
| Signaux runtime sensibles explicites ou off-session | `minimum_observability_contract`, `dependencies_to_constitution` | insuffisant | Rien ne force encore explicitement la preuve que misconception/ICC/contexte authentique, etc., ne sont pas inférés illicitement en runtime | Brèche constitutionnelle importante |

## Analyse détaillée par axe

### Axe 1 — Compatibilité constitutionnelle

#### Problème 1 — Contrat minimal non encore probant sur les contraintes runtime constitutionnelles
- **Élément concerné** : `produced_application_minimum_contract.minimum_validation_contract`
- **Localisation** : `docs/cores/current/platform_factory_architecture.yaml`
- **Nature du problème** : les axes minimaux de validation couvrent `structure`, `minimum_contract_conformance`, `traceability`, `packaging`, `structure_and_state_alignment`, mais pas explicitement la conformité aux contraintes runtime constitutionnelles les plus fortes.
- **Type de problème** : compatibilité constitutionnelle / complétude / gouvernance
- **Gravité** : critique
- **Impact sur la factory** : la factory peut produire un objet bien tracé mais insuffisamment contraint.
- **Impact sur une application produite** : risque de laisser passer un runtime non 100 % local, une dépendance réseau, une génération interdite ou une qualification sémantique illégitime.
- **Impact sur le travail des IA** : une IA peut croire qu’un build “validé” est constitutionnel alors que la validation ne couvre pas les bons interdits.
- **Impact sur la gouvernance/release** : release potentiellement trompeuse.
- **Correction à arbitrer** : ajouter un axe probant explicite de `runtime_policy_conformance` couvrant au minimum localité, absence d’appel réseau temps réel, absence de génération runtime interdite, absence d’inférence implicite de signaux interdits.
- **Lieu probable de correction** : architecture + validator/tooling

#### Problème 2 — Dépendances à la Constitution explicitées, mais bindings de preuve insuffisants
- **Élément concerné** : `dependencies_to_constitution`, `produced_application_minimum_contract`
- **Localisation** : `docs/cores/current/platform_factory_architecture.yaml`
- **Nature du problème** : la factory dit dépendre explicitement des `governing_invariants`, `forbidden_behaviors`, `local_runtime_constraints`, `canonical_traceability_requirements`, mais elle ne relie pas encore chaque obligation du contrat minimal à des preuves attendues dans le manifest, la configuration, la validation et l’observabilité.
- **Type de problème** : compatibilité constitutionnelle / implémentabilité
- **Gravité** : élevé
- **Impact sur la factory** : dépendances bien nommées mais encore peu probantes.
- **Impact sur une application produite** : la conformité constitutionnelle peut rester narrative au lieu d’être audit-able.
- **Impact sur le travail des IA** : risque de paraphrase fidèle en apparence mais non démontrable.
- **Impact sur la gouvernance/release** : difficulté à certifier une application produite comme constitutionnellement compatible.
- **Correction à arbitrer** : imposer une matrice de correspondance `invariant -> preuve attendue -> artefact porteur -> validator attendu`.
- **Lieu probable de correction** : architecture + validator/tooling

### Axe 2 — Cohérence interne architecture/state

#### Problème 3 — Statut released baseline vs statuts artefacts `RELEASE_CANDIDATE`
- **Élément concerné** : pipeline vs metadata des artefacts
- **Localisation** : `docs/pipelines/platform_factory/pipeline.md` et `docs/cores/current/platform_factory_architecture.yaml` / `platform_factory_state.yaml`
- **Nature du problème** : le pipeline pose en doctrine que les artefacts courants sont une baseline released, tandis que les deux artefacts se déclarent `RELEASE_CANDIDATE` et que l’état reconnaît en plus une présence hors manifest officiel.
- **Type de problème** : cohérence architecturale / gouvernance / faux niveau de maturité
- **Gravité** : élevé
- **Impact sur la factory** : ambiguïté de posture de départ du pipeline.
- **Impact sur une application produite** : possible confusion sur le niveau réel d’autorité de la factory utilisée comme base.
- **Impact sur le travail des IA** : une IA peut traiter comme released un artefact qui ne l’est pas pleinement.
- **Impact sur la gouvernance/release** : affaiblit la sémantique de release et promotion.
- **Correction à arbitrer** : aligner explicitement le vocabulaire entre pipeline, architecture et state : soit baseline “released under governance exception”, soit “current baseline under challenge”, soit vraie intégration release/manifest.
- **Lieu probable de correction** : state + architecture + pipeline + manifest/release governance

#### Problème 4 — Incohérence partielle entre validation minimale et short-list des validateurs prioritaires
- **Élément concerné** : `minimum_validation_contract` vs `PF_CAPABILITY_FACTORY_PRIORITY_VALIDATORS_SHORTLIST_MATERIALIZED`
- **Localisation** : architecture + state
- **Nature du problème** : l’état cite comme validateurs prioritaires `derived_projection_conformance`, `minimum_contract_conformance`, `runtime_policy_conformance`, mais l’architecture ne fait pas encore apparaître `runtime_policy_conformance` dans les axes minimaux obligatoires.
- **Type de problème** : cohérence architecturale / implémentabilité
- **Gravité** : élevé
- **Impact sur la factory** : l’état reconnaît un besoin que l’architecture ne rend pas encore normatif.
- **Impact sur une application produite** : validation potentiellement incomplète malgré un diagnostic juste dans l’état.
- **Impact sur le travail des IA** : zone d’improvisation sur ce qui est réellement “minimum”.
- **Impact sur la gouvernance/release** : validation non complètement fermée.
- **Correction à arbitrer** : faire remonter `runtime_policy_conformance` au niveau du contrat minimal architectural.
- **Lieu probable de correction** : architecture + state

### Axe 3 — Portée et frontières

**Point solide** : la frontière entre générique et spécifique est globalement bien posée. `does_not_govern`, `out_of_scope`, `variant_governance.allowed_variability` et `forbidden_variability` vont dans le bon sens.

**Zone de risque** : la factory gouverne le contrat minimal générique d’une application produite, mais sans encore borner assez précisément la frontière entre ce qui doit être prouvé par la factory et ce qui relèvera plus tard du pipeline d’instanciation. Sans cela, le futur pipeline aval peut absorber des obligations qui auraient dû rester garanties génériquement.

**Angle mort** : le traitement du runtime policy contract reste trop diffus. Il ne relève ni clairement du seul aval d’instanciation, ni clairement d’une exigence générique déjà fermée dans la factory.

#### Problème 5 — Frontière insuffisamment probante entre factory et pipeline d’instanciation
- **Élément concerné** : `PF_LAYER_APPLICATION_INSTANTIATION`, `PF_CHAIN_05_INSTANTIATE_DOMAIN_SPECIFIC_PARTS`, `produced_application_minimum_contract`
- **Nature du problème** : la frontière conceptuelle est bonne, mais la répartition des obligations probantes ne l’est pas encore assez.
- **Type de problème** : mauvais placement de couche / implémentabilité
- **Gravité** : modéré
- **Impact sur la factory** : risque de trous de responsabilité.
- **Impact sur une application produite** : certains invariants peuvent n’être garantis nulle part de façon ferme.
- **Impact sur le travail des IA** : responsabilité floue entre équipe/factory et équipe/instanciation.
- **Impact sur la gouvernance/release** : arbitrages plus difficiles.
- **Correction à arbitrer** : lister les obligations “must be guaranteed by factory before downstream instantiation” vs “must be completed by instantiation pipeline”.
- **Lieu probable de correction** : architecture

### Axe 4 — Contrat minimal d’une application produite

#### Problème 6 — Contrat utile mais encore trop haut niveau pour prouver la conformité
- **Élément concerné** : `produced_application_minimum_contract`
- **Nature du problème** : le contrat est structurellement bien pensé, mais ses blocs restent encore trop intentionnels pour devenir probants.
- **Type de problème** : complétude / implémentabilité
- **Gravité** : élevé
- **Impact sur la factory** : contrat difficile à transformer en validators déterministes.
- **Impact sur une application produite** : manifest, configuration, packaging et validation peuvent exister sans être assez normalisés pour audit.
- **Impact sur le travail des IA** : générer “quelque chose de plausible” restera trop facile.
- **Impact sur la gouvernance/release** : difficile d’affirmer une conformité reproductible.
- **Correction à arbitrer** : renforcer le contrat par des blocs probants minimums obligatoires, notamment : preuves de dépendances canoniques, fingerprints des projections utilisées, déclaration explicite de politique runtime, statut de complétude, et statut de conformité constitutionnelle auditable.
- **Lieu probable de correction** : architecture

### Axe 5 — Validated derived execution projections

#### Problème 7 — Mécanisme central affirmé, mais encore non fermé contre divergence normative
- **Élément concerné** : `execution_projection_contract`, `generated_projection_rules`, `derived_projection_conformity_status`
- **Nature du problème** : le principe est fort, mais il manque précisément les mécanismes qui empêchent les dérives réelles : validator, emplacement, protocole de régénération, protocole d’usage runtime/off-session, traçabilité forte des sources et des omissions interdites.
- **Type de problème** : exploitabilité IA / gouvernance / complétude
- **Gravité** : critique
- **Impact sur la factory** : la projection dérivée reste l’endroit le plus exposé à la dérive normative.
- **Impact sur une application produite** : une application ou un sous-travail IA peut être construit sur une projection incomplète ou trop paraphrasée.
- **Impact sur le travail des IA** : une IA peut travailler “en autonomie bornée” sur un artefact qui n’est pas encore suffisamment garanti.
- **Impact sur la gouvernance/release** : impossible de prétendre à une conformité stricte sans outillage minimal.
- **Correction à arbitrer** : définir un protocole minimal obligatoire pour toute projection : scope déclaré, liste de sources exactes, fingerprint des sources, timestamp/version de régénération, validator de conformité, statut de promotion interdit vers canonique, et politique d’usage explicite.
- **Lieu probable de correction** : architecture + state + validator/tooling

#### Problème 8 — Emplacement des projections `TBD` trop central pour rester longtemps ouvert
- **Élément concerné** : `generated_projection_rules.emplacement_policy`
- **Nature du problème** : l’emplacement est explicitement `TBD`, alors que la bonne séparation entre `docs/cores/current/`, outputs de pipeline et projections de travail IA est une condition de gouvernance importante.
- **Type de problème** : gouvernance / traçabilité
- **Gravité** : élevé
- **Impact sur la factory** : flou de stockage et de cycle de vie.
- **Impact sur une application produite** : risque d’utiliser une projection non officielle ou obsolète.
- **Impact sur le travail des IA** : collisions de lecture/écriture et confusion d’autorité.
- **Impact sur la gouvernance/release** : traçabilité incomplète.
- **Correction à arbitrer** : arrêter une zone explicite de stockage, distincte du canonique current, avec convention de nommage, statut et régénération.
- **Lieu probable de correction** : architecture + manifest/release governance

### Axe 6 — État reconnu, maturité et preuves

#### Problème 9 — L’état est globalement honnête, mais la posture “current baseline” reste plus forte que la preuve disponible
- **Élément concerné** : `platform_factory_state.yaml`
- **Nature du problème** : l’état reconnaît bien plusieurs manques, ce qui est sain. Mais la combinaison `current/` + baseline doctrinalement released + absence de manifest officiel + validators absents produit malgré tout une maturité perçue supérieure à la maturité probante réelle.
- **Type de problème** : faux niveau de maturité / gouvernance
- **Gravité** : élevé
- **Impact sur la factory** : risque d’usage prématuré comme socle fiable.
- **Impact sur une application produite** : une chaîne aval peut s’appuyer trop tôt sur cette baseline.
- **Impact sur le travail des IA** : biais de confiance excessif.
- **Impact sur la gouvernance/release** : dilution du sens des termes `current`, `release`, `candidate`.
- **Correction à arbitrer** : expliciter un statut transitoire gouverné distinct d’un “released current official manifest-integrated artifact”.
- **Lieu probable de correction** : state + manifest/release governance

### Axe 7 — Multi-IA en parallèle

#### Problème 10 — Multi-IA reconnue comme exigence de premier rang, mais non encore rendue opérable
- **Élément concerné** : `multi_ia_parallel_readiness`, `multi_ia_parallel_readiness_status`
- **Nature du problème** : les principes nécessaires sont présents, mais il manque précisément les protocoles qui évitent les collisions et la dérive à l’échelle multi-IA.
- **Type de problème** : exploitabilité IA / implémentabilité
- **Gravité** : élevé
- **Impact sur la factory** : la revendication “multi-IA ready” reste surtout programmatique.
- **Impact sur une application produite** : assemblage fragile et dépendances implicites.
- **Impact sur le travail des IA** : scopes trop larges, collisions de responsabilités, hétérogénéité des sorties.
- **Impact sur la gouvernance/release** : consolidation plus coûteuse et moins fiable.
- **Correction à arbitrer** : définir un protocole minimal de décomposition modulaire, d’assembly points, d’IDs stables, de format homogène de report et de résolution de conflit.
- **Lieu probable de correction** : architecture + pipeline

### Axe 8 — Gouvernance release, manifest et traçabilité

#### Problème 11 — Présence en `docs/cores/current/` sans intégration au manifest officiel courant
- **Élément concerné** : metadata des artefacts + blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
- **Nature du problème** : les artefacts sont placés dans la zone symboliquement la plus forte du repo (`current/`) tout en étant explicitement hors manifest officiel.
- **Type de problème** : gouvernance / traçabilité
- **Gravité** : critique
- **Impact sur la factory** : zone d’autorité ambiguë.
- **Impact sur une application produite** : un lecteur ou outil peut considérer à tort ces artefacts comme officiellement promus.
- **Impact sur le travail des IA** : ingestion non alignée entre artefacts visibles et artefacts officiellement gouvernés.
- **Impact sur la gouvernance/release** : rupture de fermeture du dispositif de release.
- **Correction à arbitrer** : soit étendre rapidement la gouvernance manifest/release pour intégrer platform_factory, soit déplacer temporairement la baseline dans une zone distincte de `current/` tant qu’elle n’est pas officiellement intégrée.
- **Lieu probable de correction** : manifest/release governance

### Axe 9 — Implémentabilité pipeline

#### Problème 12 — Pipeline crédible pour démarrer, mais pas encore assez fermé pour éviter l’improvisation IA sur les étapes critiques
- **Élément concerné** : `docs/pipelines/platform_factory/pipeline.md`
- **Nature du problème** : le squelette est bon, mais il reste V0. Les zones de validation spécifique à la factory et des projections dérivées dépendent encore de prompts et de jugement, plus que d’un outillage minimal déterministe.
- **Type de problème** : implémentabilité / gouvernance
- **Gravité** : modéré à élevé
- **Impact sur la factory** : le pipeline gouverne mieux qu’un chantier libre, mais moins qu’un cycle de correction réellement fermé.
- **Impact sur une application produite** : les failles de la factory peuvent se propager en aval.
- **Impact sur le travail des IA** : l’IA doit encore compléter des vides de contrat.
- **Impact sur la gouvernance/release** : qualité dépendante de la discipline opérateur.
- **Correction à arbitrer** : prioriser les validateurs minimums et les rapports normalisés avant d’augmenter la surface fonctionnelle de la factory.
- **Lieu probable de correction** : pipeline + validator/tooling

### Axe 10 — Scénarios adversariaux plausibles

#### Scénario A — Projection dérivée conforme en apparence, divergente en pratique
Une IA reçoit une `validated_derived_execution_projection` stockée dans un emplacement non encore gouverné. La projection a un scope déclaré, mais aucune empreinte de sources ni validator de conformité effectif. Une contrainte canonique importante a été omise lors d’une régénération partielle. L’IA produit un artefact cohérent localement mais normativement incomplet.
- **Origine principale** : projections dérivées + tooling absent

#### Scénario B — Application “validée” mais non 100 % locale
Une application produite déclare un `runtime_entrypoint`, un manifest, un packaging et une observabilité minimale. Pourtant, son runtime appelle un service distant pour classifier un signal sensible ou générer un feedback de secours. La validation minimale actuelle ne l’interdit pas explicitement.
- **Origine principale** : contrat minimal + validation incomplète

#### Scénario C — Collision multi-IA sur modules et assembly points
Deux IA travaillent en parallèle sur des sous-scopes supposés indépendants. Faute de protocole de décomposition et d’assemblage stabilisé, elles produisent deux conventions différentes pour les modules, ou réécrivent un même point de jonction sans le savoir. L’assemblage final paraît plausible mais détruit la traçabilité.
- **Origine principale** : multi-IA readiness non opérationalisée

#### Scénario D — Baseline consommée comme released alors qu’elle reste hors manifest officiel
Un outil, une IA ou un opérateur lit `docs/cores/current/platform_factory_architecture.yaml` et considère automatiquement la factory comme officiellement promue. Or le manifest officiel courant ne l’intègre pas encore. Une chaîne aval traite alors comme canonique un artefact dont le statut réel est encore transitoire.
- **Origine principale** : gouvernance release / manifest / current ambiguity

### Axe 11 — Priorisation

#### Critique
1. Contrat minimal non encore probant sur les contraintes runtime constitutionnelles.
2. Mécanisme des `validated_derived_execution_projections` non fermé contre divergence normative.
3. Présence en `docs/cores/current/` sans intégration au manifest officiel courant.

#### Élevé
4. Contradiction released baseline vs `RELEASE_CANDIDATE`.
5. Incohérence partielle entre short-list des validateurs prioritaires et axes minimaux du contrat.
6. Readiness multi-IA reconnue mais non opérationalisée.
7. Dépendances constitutionnelles explicitées sans matrice de preuve.
8. Emplacement des projections encore `TBD`.

#### Modéré
9. Frontière probante incomplète entre factory et futur pipeline d’instanciation.
10. Pipeline V0 encore trop dépendant du jugement de l’IA sur les étapes critiques.

#### Faible
11. Schémas détaillés manifest/configuration/packaging encore ouverts mais déjà reconnus comme V0 incomplets.

## Risques prioritaires

1. **Fausse conformité constitutionnelle** : une application produite peut être structurellement propre mais violer les invariants runtime essentiels.
2. **Dérive normative via projection dérivée** : la factory introduit précisément l’interface la plus exposée aux pertes de fidélité, sans l’avoir encore fermée par validator et protocole.
3. **Ambiguïté d’autorité** : `current/` visible mais hors manifest officiel, combiné à un vocabulaire de baseline released.
4. **Promesse multi-IA prématurée** : exigence juste, mais non encore instrumentée.

## Points V0 acceptables

Les points suivants sont acceptables à ce stade **à condition de rester explicitement reconnus comme non finalisés** :

- absence de schéma final du manifest d’application produite ;
- typologie runtime exacte encore ouverte ;
- schéma détaillé de configuration encore ouvert ;
- schéma détaillé de packaging encore ouvert ;
- granularité optimale du travail multi-IA encore ouverte ;
- pipeline d’instanciation aval encore absent ;
- validators factory encore non implémentés tant que leur priorité devient le chantier suivant.

Ce qui rend ces points acceptables en V0 est qu’ils sont globalement **reconnus comme manquants**, et non maquillés comme déjà opérationnels. Leur acceptabilité cesse toutefois dès lors qu’ils touchent la preuve normative, la fermeture release/manifest ou la gouvernance effective des projections dérivées.

## Corrections à arbitrer avant patch

### Priorité 1 — Fermer la preuve constitutionnelle minimale
- Ajouter au contrat minimal un axe explicite de `runtime_policy_conformance`.
- Déclarer les preuves minimum attendues pour :
  - runtime 100 % local ;
  - absence d’appel réseau temps réel ;
  - absence de génération runtime interdite ;
  - absence d’inférence implicite interdite de signaux sensibles ;
  - usage off-session des artefacts de patch / qualification.

### Priorité 2 — Fermer le mécanisme des projections dérivées
- Définir le protocole minimum de projection : scope, sources exactes, fingerprint, timestamp/version, validator, statut de conformité, interdiction de promotion implicite.
- Arrêter l’emplacement de stockage distinct du canonique.
- Définir le protocole de régénération et de revalidation.

### Priorité 3 — Assainir la gouvernance release / current / manifest
- Aligner la sémantique entre pipeline et statuts des artefacts.
- Décider si la baseline platform_factory doit :
  - être intégrée formellement au manifest courant ;
  - ou être sortie de `docs/cores/current/` tant qu’elle n’a pas ce statut.

### Priorité 4 — Rendre la multi-IA réellement gouvernable
- Définir un protocole minimal de décomposition modulaire.
- Définir un protocole d’assemblage, de résolution de conflit et de format de report homogène.
- Stabiliser les IDs et points d’assemblage.

### Priorité 5 — Prioriser le tooling minimal au lieu d’élargir trop tôt le périmètre
- Matérialiser la short-list de validators prioritaires.
- Normaliser les outputs de validation/report avant d’ajouter de nouvelles capacités factory.

## Verdict de challenge

La baseline V0 `platform_factory` est **pertinente, structurante et légitime à challenger**, mais **pas encore suffisamment fermée pour être considérée comme released au sens fort d’un socle probant, manifesté et multi-IA-opérable**.

Le chantier prioritaire n’est pas d’ajouter du contenu fonctionnel ; c’est de **fermer la preuve**, **fermer la gouvernance des projections**, et **fermer la sémantique de release/current/manifest**.
