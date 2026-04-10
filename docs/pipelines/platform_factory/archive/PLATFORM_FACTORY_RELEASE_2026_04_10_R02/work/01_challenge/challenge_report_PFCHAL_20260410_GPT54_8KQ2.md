# Challenge Report — Platform Factory Baseline V0

## challenge_run_id
`PFCHAL_20260410_GPT54_8KQ2`

## Date
2026-04-10

## Artefacts challengés
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

## Socle canonique lu
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

## Pipeline lu
- `docs/pipelines/platform_factory/pipeline.md`

## Résumé exécutif

La baseline `platform_factory` est désormais assez structurée pour entrer dans une gouvernance réelle de pipeline. En revanche, elle n’est pas encore probante sur les points qui comptent le plus : preuve de conformité constitutionnelle, fermeture release/manifest, et sûreté d’usage des `validated_derived_execution_projections`.

Le point fort principal est la séparation explicite entre :
- le socle canonique primaire ;
- l’architecture prescriptive de factory ;
- l’état constatif de maturité ;
- le futur pipeline d’instanciation aval.

Le point faible principal est que plusieurs mécanismes sont déjà décrits comme gouvernés, traçables ou auditables alors que les pièces probatoires correspondantes restent absentes ou incomplètes. Le risque majeur n’est pas une contradiction frontale avec la Constitution ; le risque majeur est une sur-lecture de maturité qui laisserait croire que la factory peut déjà garantir la conformité d’une application produite ou d’une projection dérivée alors que la chaîne de preuve n’est pas encore fermée.

Verdict :
- baseline fondationnelle et exploitable pour `STAGE_02_FACTORY_ARBITRAGE` ;
- pas encore suffisamment fermée pour revendiquer une conformité probante des applications produites ;
- plusieurs corrections de gouvernance doivent être arbitrées avant patch.

---

## Carte de compatibilité constitutionnelle

### 1. Runtime 100 % local
- Élément factory concerné : `produced_application_minimum_contract`, `minimum_validation_contract`, `runtime_policy_conformance`, `dependencies_to_constitution.local_runtime_constraints`.
- Statut : visé explicitement mais insuffisamment prouvable.
- Lecture : la factory pointe bien la contrainte, mais elle ne fournit pas encore le schéma, le validator ni la matrice de conformité permettant de démontrer qu’une application produite respecte effectivement `INV_RUNTIME_FULLY_LOCAL`.

### 2. Absence d’appel IA continu / dépendance réseau temps réel
- Élément factory concerné : `minimum_validation_contract.runtime_policy_conformance`, `minimum_observability_contract.constitutional_invariants_checked`.
- Statut : protection implicite mais faible.
- Lecture : la factory reconnaît qu’il faut vérifier la conformité runtime, mais elle ne ferme pas encore le protocole de preuve qui empêcherait une application apparemment valide d’introduire une dépendance réseau ou LLM.

### 3. Absence de génération runtime interdite
- Élément factory concerné : `dependencies_to_constitution.forbidden_behaviors`, `runtime_policy_conformance`.
- Statut : visé mais non opérationnalisé.
- Lecture : la factory n’entre pas en conflit avec `INV_NO_RUNTIME_CONTENT_GENERATION` ni avec `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION`, mais elle ne donne pas encore de mécanisme auditable montrant comment une application produite prouve cette conformité.

### 4. Séparation Constitution / Référentiel
- Élément factory concerné : `source_of_authority`, `design_principles.PF_PRINCIPLE_NO_NORM_DUPLICATION`, `dependencies_to_constitution`, `dependencies_to_referentiel`, pipeline Rule 1.
- Statut : globalement solide.
- Lecture : c’est un point fort de la baseline. La factory se présente bien comme couche HOW générique et non comme seconde Constitution.

### 5. Validation locale déterministe et artefacts précomputés
- Élément factory concerné : `PF_PRINCIPLE_DETERMINISTIC_TRANSFORMATIONS`, pipeline stage map, validator Stage 04.
- Statut : direction correcte mais fermeture partielle.
- Lecture : l’intention est alignée avec `INV_PATCH_LOCAL_VALIDATION_MUST_BE_DETERMINISTIC` et `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`, mais la chaîne outillée spécifique factory reste encore incomplète.

### 6. Traçabilité canonique explicite
- Élément factory concerné : `source_of_authority`, `manifest.minimum_contents`, `reproducibility_fingerprints`, `build_and_packaging_rules`, `observability_requirements`.
- Statut : fort au niveau principe, encore incomplet au niveau preuve.
- Lecture : la traçabilité est très présente dans l’architecture. En revanche, tant que les schémas, validators et manifest officiel restent incomplets, cette traçabilité reste déclarative plus que probante.

---

## Analyse détaillée par axe

### Axe 1 — Compatibilité constitutionnelle

La baseline respecte bien la hiérarchie d’autorité. Les dépendances vers la Constitution, le Référentiel et le LINK sont explicites, et la factory ne tente pas de redéfinir les invariants. C’est le bon placement de couche.

Le problème n’est donc pas une violation explicite, mais une insuffisance de fermeture. L’architecture impose un `conformance_matrix_ref` pour chaque projection dérivée et référence aussi `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` dans `dependencies_to_constitution`, mais cette pièce probatoire n’est pas présente. Cela affaiblit fortement toute affirmation de “conformité validée”.

Conséquence : une application produite pourrait afficher un manifest propre et des validations minimales passées tout en restant insuffisamment auditée vis-à-vis des invariants les plus sensibles : local-only, no-runtime-generation, no-implicit-LLM-inference.

### Axe 2 — Cohérence interne architecture/state

La séparation prescriptif/constatif est saine et constitue un point solide.

En revanche, plusieurs signaux montrent une cohérence encore imparfaite :
- l’architecture décide désormais l’emplacement des projections (`docs/cores/platform_factory/projections/`) ;
- l’état reconnaît aussi cette décision dans `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` et dans la résolution du blocker `PF_BLOCKER_PROJECTION_LOCATION_PENDING` ;
- mais `derived_projection_conformity_status.missing` contient encore `storage_location_decision`.

Cette divergence n’est pas catastrophique, mais elle révèle que l’artefact d’état n’est pas encore complètement recalé sur l’architecture actuelle. Même logique pour `assessed_scope.excludes.exact_projection_storage_location`, qui paraît désormais obsolète au vu de la décision déjà inscrite dans l’architecture.

### Axe 3 — Portée et frontières

La frontière générique / spécifique est globalement bien posée :
- la factory gouverne le HOW générique ;
- l’instanciation domaine reste aval ;
- le contenu métier n’est pas absorbé dans la factory.

C’est un point fort.

La zone de risque porte moins sur la frontière domaine que sur la frontière “factory prescriptive” vs “preuve d’exécution réelle”. L’architecture décrit correctement ce qu’une application produite doit comporter, mais elle n’indique pas encore assez fermement comment prouver qu’une application concrète respecte ces obligations.

Angle mort identifié : le lien précis entre le contrat minimal générique d’application et la future chaîne d’instanciation reste encore trop abstrait pour empêcher des interprétations hétérogènes par plusieurs IA ou plusieurs opérateurs.

### Axe 4 — Contrat minimal d’une application produite

Le contrat minimal est bien conçu comme intention structurante. Il couvre déjà :
- identité logique ;
- identité d’instance produite ;
- fingerprints de reproductibilité ;
- manifest ;
- dépendances canoniques ;
- point d’entrée runtime ;
- configuration minimale ;
- validation minimale ;
- packaging minimal ;
- observabilité minimale.

C’est une vraie avancée.

Mais le contrat reste encore trop haut niveau pour être probant. Les champs les plus sensibles sont encore “TBD” ou non schématisés :
- schéma exact du manifest ;
- typologie exacte du runtime entrypoint ;
- schéma exact de configuration ;
- schéma exact de packaging ;
- protocole précis de validation de conformité runtime.

Le point le plus sensible est `bootstrap_contract_tbd_condition`. Tant que ce contrat n’est pas défini, la factory ne peut pas prouver de manière ferme comment un runtime d’application démarre tout en restant conforme au cadre constitutionnel.

### Axe 5 — Validated derived execution projections

La baseline a bien compris la nature du risque : une projection dérivée ne doit pas devenir un quasi-canonique.

Les bons garde-fous sont présents :
- `no_new_rule`
- `no_normative_divergence`
- `no_omission_within_declared_scope`
- `canonical_source_remains_primary_authority`
- `deterministic_regeneration_required`
- `promotion_to_canonical_forbidden = true`

Mais la fermeture reste incomplète sur trois points majeurs :
1. absence de validator dédié ;
2. absence de protocole de régénération outillé ;
3. absence de matrice de conformité constitutionnelle réellement présente.

Il existe aussi une ambiguïté à clarifier dans l’architecture :
- `generated_projection_rules.minimum_requirements` contient `each_projection_can_be_used_as_single_context_for_targeted_task` ;
- mais dans `execution_projection_contract`, le champ `usage_as_sole_context` est fixé à `blocked`.

La lecture charitable est : l’architecture vise cette capacité comme cible finale mais la bloque en V0. La lecture dangereuse est : deux formulations contradictoires coexistent dans le même artefact, ce qui peut induire une IA ou un opérateur en erreur.

### Axe 6 — État reconnu, maturité et preuves

`platform_factory_state.yaml` a la bonne posture générale : il ne prétend pas à une maturité finale et parle bien de baseline initiale.

Le jugement `foundational_but_incomplete` est juste.

Le problème n’est pas une survente massive ; le problème est une survente ponctuelle par friction sémantique. Certains items donnent une impression de fermeture plus avancée qu’elle ne l’est vraiment :
- emplacement des projections annoncé comme finalisé mais encore listé dans les “missing” ;
- intention pipeline reconnue comme présente alors que la matérialisation complète est listée absente ;
- conformité des projections définie “with explicit conditions” alors que plusieurs prérequis critiques manquent encore.

Le state doit donc être légèrement recalibré pour devenir un constat parfaitement synchronisé avec l’architecture et avec la réalité outillée.

### Axe 7 — Multi-IA en parallèle

Le sujet est bien reconnu comme contrainte de premier rang, ce qui est très positif.

Les exigences minimales sont bonnes :
- scopes bornés ;
- identifiants stables ;
- dépendances explicites ;
- points d’assemblage clairs ;
- reports homogènes ;
- pas de dépendances cachées ;
- projections régénérables.

Mais la readiness réelle reste encore faible parce que les mécanismes opérationnels sont absents :
- protocole de décomposition ;
- convention de granularité modulaire ;
- protocole d’assemblage des sorties IA ;
- protocole de résolution de conflit.

Autrement dit : la factory reconnaît correctement le problème, mais elle ne sait pas encore l’orchestrer sans improvisation.

### Axe 8 — Gouvernance release, manifest et traçabilité

C’est l’un des vrais points rouges de gouvernance.

Les artefacts `platform_factory_*` sont déjà présents dans `docs/cores/current/`, mais le pipeline et l’état reconnaissent explicitement qu’ils ne sont pas intégrés au manifest officiel courant. Le pipeline fait même de cette intégration un acte explicite de Stage 08. Cette lucidité est saine, mais elle confirme qu’il existe aujourd’hui une gouvernance partiellement ouverte.

Le challenge relève aussi l’absence d’artefact alternatif de fermeture manifeste :
- aucun `docs/cores/platform_factory/manifest.yaml` n’est présent ;
- la matrice `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` n’est pas présente non plus.

Conséquence : il existe aujourd’hui un risque de split-brain entre “présent dans current” et “officiellement gouverné / manifesté”.

### Axe 9 — Implémentabilité pipeline

Le pipeline `platform_factory` est crédible comme squelette de gouvernance :
- stages clairs ;
- distinction release/promotion ;
- discipline de sandbox en apply ;
- closeout explicite ;
- pas de discovery audit inutile.

C’est bon.

De plus, la présence d’un validator dédié de Stage 04 (`validate_platform_factory_patchset.py`) montre que la pipeline n’est plus purement théorique.

Mais l’implémentabilité complète reste encore partielle parce que :
- plusieurs outputs finaux supposent des schémas non finalisés ;
- la gouvernance de manifest reste ouverte ;
- la conformité des projections et du contrat minimal n’a pas encore ses validators probants ;
- le pipeline se décrit lui-même comme “not yet a fully tooled execution framework”.

Conclusion : pipeline plausible et déjà utilisable, mais pas encore fermé au niveau industriel.

### Axe 10 — Scénarios adversariaux plausibles

#### Scénario A — Projection dérivée faussement sûre
Une IA reçoit uniquement une projection dérivée parce qu’un opérateur retient la formule “single context for targeted task”, alors que `usage_as_sole_context` est encore bloqué et qu’aucun validator de conformité stricte n’existe. La projection omet une contrainte constitutionnelle locale importante. L’IA produit une sortie cohérente mais normativement incomplète.

- Cause principale : projections dérivées
- Origine : architecture + absence de tooling
- Gravité : élevée

#### Scénario B — Application apparemment valide mais non locale
Une application produite renseigne un `runtime_entrypoint_id`, un manifest minimal et des signaux d’observabilité, mais le runtime concret introduit un appel réseau ou une dépendance IA non autorisée. Faute de matrice de conformité, de schéma runtime détaillé et de validator de conformité runtime, la violation n’est pas détectée.

- Cause principale : contrat minimal + validators manquants
- Origine : architecture incomplètement probante
- Gravité : élevée

#### Scénario C — Collision multi-IA à l’assemblage
Deux IA travaillent en parallèle sur des modules distincts. Les scopes sont annoncés comme bornés, mais ni protocole d’assemblage ni protocole de résolution de conflit ne sont définis. Les deux sorties restent individuellement plausibles mais incompatibles sur leurs hypothèses de dépendance ou leurs points d’intégration.

- Cause principale : multi-IA protocol gap
- Origine : state + architecture
- Gravité : modérée à élevée

#### Scénario D — Gouvernance current non fermée
Les artefacts factory vivent dans `docs/cores/current/` et sont consommés comme baseline, mais ils restent hors manifest officiel. Une future release ou promotion lit un current partiellement gouverné, et deux lecteurs du repo n’ont pas la même interprétation de ce qui est “officiellement current”.

- Cause principale : release / manifest / traçabilité
- Origine : pipeline + state + absence d’artefact de manifest alternatif
- Gravité : élevée

---

## Risques prioritaires

### Risque 1 — Chaîne de preuve constitutionnelle incomplète
- Gravité : élevée
- Pourquoi : la factory vise la conformité constitutionnelle mais la matrice de conformité référencée n’est pas présente et les validators probants ne sont pas encore matérialisés.
- Effet : une application ou une projection peut sembler gouvernée sans preuve suffisante.

### Risque 2 — Gouvernance des projections dérivées insuffisamment fermée
- Gravité : élevée
- Pourquoi : absence de validator, absence de protocole outillé, ambiguïté sur l’usage en contexte unique.
- Effet : risque direct de dérive normative ou d’omission de contrainte.

### Risque 3 — Gap manifest/current
- Gravité : élevée
- Pourquoi : artefacts présents en `current` mais hors manifest officiel, sans manifest alternatif de fermeture trouvé.
- Effet : traçabilité et statut officiel partiellement ambigus.

### Risque 4 — Contrat minimal d’application encore trop déclaratif
- Gravité : modérée
- Pourquoi : plusieurs schémas critiques restent ouverts.
- Effet : contrat utile pour cadrer, mais insuffisant pour prouver la conformité d’une application réelle.

### Risque 5 — Multi-IA readiness encore surtout déclarative
- Gravité : modérée
- Pourquoi : principes présents, protocoles absents.
- Effet : parallélisme possible en théorie, encore fragile en exécution.

---

## Points V0 acceptables

- La séparation `architecture` / `state` est bien posée et saine.
- La factory ne se comporte pas comme une seconde Constitution.
- La frontière entre générique factory et spécifique domaine est globalement bien tenue.
- Le pipeline est suffisamment structuré pour enclencher une boucle challenge → arbitrage → patch → validation → release → promotion → closeout.
- Le fait de bloquer explicitement l’usage des projections comme contexte unique tant que la maturité n’est pas suffisante est une prudence saine.
- Le niveau global de maturité déclaré dans `platform_factory_state.yaml` reste honnête : la baseline se présente comme fondationnelle mais incomplète.

---

## Corrections à arbitrer avant patch

### PF-CHAL-01 — Fermer la preuve de conformité constitutionnelle

- Élément concerné : conformance constitutionnelle des projections et des applications produites
- Localisation :
  - `platform_factory_architecture.yaml > contracts.execution_projection_contract.mandatory_fields_per_projection`
  - `platform_factory_architecture.yaml > dependencies_to_constitution.constitutional_conformance_matrix_ref`
  - artefact référencé `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` absent
- Nature du problème : pièce probatoire référencée mais non présente
- Type de problème : compatibilité constitutionnelle / gouvernance / complétude
- Gravité : élevée
- Impact sur la factory : empêche de revendiquer une validation stricte réellement auditée
- Impact sur une application produite : peut paraître conforme sans preuve ferme sur local-only / no-runtime-generation
- Impact sur le travail des IA : augmente le risque de dérive silencieuse dans les projections
- Impact sur la gouvernance/release : empêche une fermeture probante
- Correction à arbitrer :
  - créer la matrice de conformité constitutionnelle minimale ;
  - définir le rôle exact de cette matrice dans la validation de projection et dans la validation du contrat minimal d’application ;
  - décider si cette matrice est canonique factory ou artefact de release gouverné
- Lieu probable de correction :
  - architecture
  - validator/tooling
  - manifest/release governance

### PF-CHAL-02 — Supprimer l’ambiguïté sur l’usage des projections comme contexte unique

- Élément concerné : gouvernance des `validated_derived_execution_projections`
- Localisation :
  - `platform_factory_architecture.yaml > generated_projection_rules.minimum_requirements`
  - `platform_factory_architecture.yaml > contracts.execution_projection_contract.mandatory_fields_per_projection.usage_as_sole_context`
- Nature du problème : tension entre capacité cible et politique actuelle bloquante
- Type de problème : cohérence architecturale / exploitabilité IA
- Gravité : élevée
- Impact sur la factory : ambiguïté normative de lecture
- Impact sur une application produite : peut induire une mauvaise utilisation des projections
- Impact sur le travail des IA : une IA peut croire qu’une projection suffit seule alors que la politique V0 la bloque encore
- Impact sur la gouvernance/release : rend plus difficile une validation cohérente des usages autorisés
- Correction à arbitrer :
  - expliciter dans l’architecture la distinction entre capacité cible et politique V0 actuelle ;
  - soit retirer temporairement l’exigence “single context”, soit la reformuler comme objectif futur ;
  - aligner le state sur cette décision
- Lieu probable de correction :
  - architecture
  - state

### PF-CHAL-03 — Recaler complètement l’état sur la décision d’emplacement des projections

- Élément concerné : synchronisation architecture/state
- Localisation :
  - `platform_factory_architecture.yaml > generated_projection_rules.emplacement_policy`
  - `platform_factory_state.yaml > derived_projection_conformity_status.missing`
  - `platform_factory_state.yaml > assessed_scope.excludes`
- Nature du problème : incohérence résiduelle après décision déjà actée
- Type de problème : faux niveau de maturité / cohérence architecturale
- Gravité : modérée
- Impact sur la factory : fragilise la fiabilité de l’artefact constatif
- Impact sur une application produite : indirect
- Impact sur le travail des IA : peut générer des lectures divergentes du statut réel
- Impact sur la gouvernance/release : faible à modéré mais inutilement perturbant
- Correction à arbitrer :
  - retirer `storage_location_decision` des éléments manquants ;
  - mettre à jour `assessed_scope` si nécessaire ;
  - vérifier que tous les champs state reflètent bien la décision ARB-04 / ARB-05
- Lieu probable de correction :
  - state

### PF-CHAL-04 — Fermer la gouvernance manifest/current des artefacts factory

- Élément concerné : statut officiel des artefacts `platform_factory_*`
- Localisation :
  - `pipeline.md > Rule 3`
  - `platform_factory_state.yaml > PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`
  - absence observée de `docs/cores/platform_factory/manifest.yaml`
- Nature du problème : présence en `current` sans fermeture manifeste officielle
- Type de problème : gouvernance / release / traçabilité
- Gravité : élevée
- Impact sur la factory : statut “current gouverné” partiellement ambigu
- Impact sur une application produite : traçabilité de dépendance fragilisée
- Impact sur le travail des IA : peut créer deux lectures concurrentes du canon “actif”
- Impact sur la gouvernance/release : élevé
- Correction à arbitrer :
  - décider si la première fermeture passe par extension du manifest officiel courant ;
  - ou par un manifest factory dédié temporaire ;
  - puis inscrire explicitement la stratégie dans le pipeline et dans le state
- Lieu probable de correction :
  - pipeline
  - manifest/release governance
  - state

### PF-CHAL-05 — Transformer la readiness multi-IA en protocole exploitable

- Élément concerné : travail parallèle multi-IA
- Localisation :
  - `platform_factory_architecture.yaml > multi_ia_parallel_readiness`
  - `platform_factory_state.yaml > multi_ia_parallel_readiness_status`
- Nature du problème : readiness déclarée sans protocole d’exécution
- Type de problème : exploitabilité IA / implémentabilité
- Gravité : modérée
- Impact sur la factory : limite la capacité réelle à industrialiser le parallélisme
- Impact sur une application produite : risque de collisions d’assemblage
- Impact sur le travail des IA : fort
- Impact sur la gouvernance/release : modéré
- Correction à arbitrer :
  - définir un protocole minimal de décomposition ;
  - définir un protocole minimal d’assemblage ;
  - définir un protocole minimal de résolution de conflit ;
  - décider si ces éléments vivent dans l’architecture, dans des projections dérivées dédiées, ou dans le pipeline
- Lieu probable de correction :
  - architecture
  - pipeline
  - validator/tooling

---

## Conclusion

La baseline V0 de `platform_factory` est globalement bien placée en couche et suffisamment sérieuse pour être challengée puis durcie par pipeline. Elle ne souffre pas d’un problème majeur de philosophie architecturale. Elle souffre surtout d’un problème de fermeture : certaines promesses de conformité, de traçabilité et de multi-IA sont mieux décrites qu’elles ne sont encore démontrées.

Le travail à arbitrer avant patch doit donc se concentrer prioritairement sur :
1. la chaîne de preuve constitutionnelle ;
2. la fermeture de gouvernance manifest/current ;
3. la fermeture réelle du mécanisme de projections dérivées ;
4. la transformation du multi-IA de “principe reconnu” en protocole exploitable.