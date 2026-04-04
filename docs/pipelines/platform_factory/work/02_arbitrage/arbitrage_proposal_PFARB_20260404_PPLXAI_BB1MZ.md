# Proposition d'arbitrage — Platform Factory V0

- **arbitrage_run_id**: `PFARB_20260404_PPLXAI_BB1MZ`
- **date**: `2026-04-04`
- **stage**: `STAGE_02_FACTORY_ARBITRAGE`
- **pipeline**: `docs/pipelines/platform_factory/pipeline.md`

## Challenge reports considérés

- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_GPT54_X7K2Q.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_7K2R.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERPLX_A1J77P.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PERP_K7X2.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PPLXAI_5LVBSV.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260404_PXADV_BB1MZX.md`

## Résumé exécutif

Les six challenge reports convergent sur la légitimité de la baseline `platform_factory` V0 comme socle de départ, tout en pointant une fermeture insuffisante pour industrialiser sans risque la production d’applications Learn-it constitutionnellement compatibles.[cite:2] Les constats majeurs portent sur la non-opérationnalisation des invariants constitutionnels dans le contrat minimal d’une application produite, la faiblesse du dispositif autour des `validated_derived_execution_projections`, et un trou de gouvernance entre `current/` et le manifest officiel.[cite:3]

La présente proposition d’arbitrage recommande de :
- renforcer le contrat minimal d’application pour rendre auditable la conformité aux invariants critiques (runtime 100 % local, absence de génération runtime, déterminisme de validation, atomicité des patchs) ;
- encadrer l’usage des projections dérivées par un cycle de vie outillé (stockage, validator, régénération, emplacement) avant de les utiliser comme artefact unique ;
- clarifier la frontière entre factory générique, pipeline d’instanciation et gouvernance de release, en introduisant un contrat de handoff explicite ;
- réaligner le state sur un niveau de maturité plus honnête là où des capacités sont encore au stade d’intention.

Ces arbitrages sont proposés comme base de travail pour un patch ultérieur, sans préjuger de la décision humaine finale.

## Synthèse des constats convergents

### Compatibilité constitutionnelle et contrat minimal

- Tous les rapports constatent que plusieurs invariants de sécurité (runtime local, absence de génération de contenu et de feedback runtime, déterminisme de validation, absence d’état partiel interdit) ne sont pas projetés en obligations auditables dans le `produced_application_minimum_contract` ni dans les axes de validation minimale.[cite:2][cite:3]
- Il en résulte la possibilité qu’une application soit « conforme factory » tout en violant des invariants constitutionnels forts, ce qui crée un faux sentiment de complétude de validation.[cite:3]

### Validated derived execution projections

- Les rapports décrivent un mécanisme conceptuellement bien posé mais opérationnellement trop ouvert : projections autorisées comme unique artefact d’entrée pour une IA, alors que le lieu de stockage, les validators et les règles de régénération sont encore `TBD` ou absents.[cite:3]
- L’architecture déclare des invariants de conformité des projections, mais aucun mécanisme de vérification ou de traçabilité n’est encore instrumenté, ce qui ouvre un risque de dérive normative silencieuse.[cite:2]

### Gouvernance release / current / manifest

- Les fichiers `platform_factory_architecture.yaml` et `platform_factory_state.yaml` sont posés en `docs/cores/current/` mais explicitement hors du manifest courant, créant un angle mort entre « artefact présent en current » et « artefact officiellement gouverné par le dispositif de release ».[cite:2]
- Les rapports convergent pour considérer ce point comme un risque de traçabilité et de gouvernance plus qu’un défaut conceptuel d’architecture.[cite:3]

### Maturité et surdéclaration dans le state

- Plusieurs capacités sont déclarées `present` alors qu’elles correspondent davantage à des intentions correctement formulées qu’à des mécanismes outillés (schémas, validators, règles de projection).[cite:3]
- Les rapports soulignent un risque de lecture trop optimiste du state, qui pourrait laisser croire à une disponibilité opérationnelle plus avancée que la réalité.[cite:2]

### Multi-IA et protocole d’assemblage

- Le besoin de travail multi-IA est explicite, mais la granularité modulaire des sorties IA, la résolution de conflits entre contributions parallèles et le protocole de consolidation ne sont pas définis.[cite:3]
- Les rapports convergent sur l’absence de contrat d’assemblage, ce qui rend fragile l’exploitation sécurisée de productions IA multiples sur la factory.[cite:3]

## Propositions d’arbitrage par thème

### Thème 1 — Contrat minimal d’application produite

**Élément concerné** : `produced_application_minimum_contract` et `minimum_validation_contract` dans `platform_factory_architecture.yaml`.

**Constats consolidés** :
- Obligations présentes mais trop haut niveau (identité, manifest, dépendances canoniques, entrypoint, configuration, validation, packaging, observabilité).[cite:2]
- Absence d’axes de validation explicites pour : localité runtime, absence d’appel réseau temps réel, absence de génération de contenu et de feedback runtime, atomicité des patchs, déterminisme de validation locale, conformité stricte aux invariants de sécurité.[cite:3]

**Statut proposé** : retained (à corriger maintenant).

**Lieu probable de correction** :
- principal : architecture (`platform_factory_architecture.yaml`) ;
- secondaire : state (`platform_factory_state.yaml`) pour refléter la nouvelle exigence et la maturité actuelle.

**Gravité** : critique.

**Justification** :
- Sans projection opérationnelle des invariants critiques dans le contrat minimal, la factory ne permet pas de prouver la compatibilité constitutionnelle d’une application produite.[cite:2]
- Le risque majeur identifié dans plusieurs rapports est celui d’une application « conforme factory » mais violant des invariants de sécurité.[cite:3]

**Dépendances** :
- Lié aux arbitrages sur les projections dérivées (Thème 2) et sur la gouvernance de release (Thème 4).

**Niveau de consensus perçu** : strong.

---

### Thème 2 — Validated derived execution projections

**Élément concerné** : bloc `validated_derived_execution_projections` dans `platform_factory_architecture.yaml` et statut associé dans `platform_factory_state.yaml`.

**Constats consolidés** :
- Mécanisme conçu comme puissant (projections comme unique artefact pour IA) mais non instrumenté : pas de stockage, pas de validator, pas de protocole de régénération, emplacement non tranché.[cite:3]
- Tension entre une déclaration d’usage autorisé et un state reconnaissant l’absence de capacité outillée.[cite:2]

**Statut proposé** :
- retained pour la nécessité d’encadrer le mécanisme ;
- deferred pour la mise en œuvre complète des outils, sous réserve de clarification.[cite:3]

**Lieu probable de correction** :
- principal : architecture (définition des contrats et invariants des projections) ;
- secondaires : pipeline (étapes de génération/validation), validator/tooling (implémentation effective), state (niveau de maturité).[cite:3]

**Gravité** : élevé.

**Justification** :
- Tant que les projections dérivées sont utilisées sans garde-fous instrumentés, elles peuvent devenir un vecteur de dérive normative silencieuse.[cite:2]
- Le décalage entre capacité déclarée et outillage effectif crée un risque de mauvaise interprétation par des IA ou des humains.

**Pré-conditions de patch** :
- Clarifier la politique d’emplacement (factory vs instanciation vs infra) et le format des projections ;
- Définir le niveau minimal de validator requis avant tout usage de projection comme artefact unique.

**Niveau de consensus perçu** : strong sur le problème, medium sur la séquence de traitement.

---

### Thème 3 — Gouvernance release / current / manifest

**Élément concerné** : positionnement de `platform_factory_architecture.yaml` et `platform_factory_state.yaml` dans `docs/cores/current/` et leur absence du manifest officiel.

**Constats consolidés** :
- Tous les rapports notent que la factory est posée en `docs/cores/current/` mais pas intégrée au manifest courant.[cite:2]
- Le state explicite ce décalage, mais sans mécanisme de gouvernance pour le résorber.[cite:3]

**Statut proposé** : retained.

**Lieu probable de correction** :
- principal : manifest / release governance ;
- secondaire : state (clarification du statut tant que la situation n’est pas résolue).

**Gravité** : modéré à élevé.

**Justification** :
- L’angle mort de traçabilité entre artefacts posés et artefacts officiellement gouvernés fragilise la lecture de conformité globale.[cite:2]
- Ce point bloque une industrialisation sereine, même si la V0 reste exploitable à titre expérimental.

**Niveau de consensus perçu** : strong.

---

### Thème 4 — Maturité déclarée dans le state

**Élément concerné** : `platform_factory_state.yaml` (sections `capabilities_present`, `capabilities_partial`, `capabilities_absent`).

**Constats consolidés** :
- Certains items marqués `present` correspondent en réalité à des intentions bien posées mais non instrumentées (absence de schémas, de validators, de règles de projection ou de signaux d’observabilité).[cite:3]
- Les rapports pointent un risque de distorsion entre maturité déclarée et maturité effective.[cite:2]

**Statut proposé** : retained.

**Lieu probable de correction** :
- principal : state ;
- secondaire : éventuellement architecture pour clarifier les critères de passage d’intention à capacité présente.

**Gravité** : modéré.

**Justification** :
- Un state trop optimiste brouille la priorisation des patchs et peut conduire à sous-estimer le travail restant avant une V1 réellement gouvernable.[cite:3]

**Niveau de consensus perçu** : strong.

---

### Thème 5 — Multi-IA et protocole d’assemblage

**Élément concerné** : architecture factory (principes multi-IA) et pipeline d’exécution.

**Constats consolidés** :
- La nécessité d’un travail multi-IA est assumée, mais le contrat d’assemblage (granularité des fragments, résolution des conflits, workflow de consolidation) est absent.[cite:3]
- Les rapports soulignent que l’absence de protocole explicite peut conduire à des productions incompatibles ou incohérentes.[cite:3]

**Statut proposé** : deferred.

**Lieu probable de correction** :
- principal : pipeline (définition des étapes et de la gouvernance d’assemblage) ;
- secondaires : architecture (principes structurants) et tooling (outils de diff/merge contrôlé).

**Gravité** : modéré.

**Justification** :
- Le sujet est important pour la scalabilité multi-IA, mais il est moins bloquant, à court terme, que la fermeture des invariants de sécurité et du contrat minimal.[cite:3]

**Niveau de consensus perçu** : medium.

---

## Points retenus

- Renforcement du contrat minimal d’application pour projeter les invariants constitutionnels critiques en obligations auditables (runtime local, absence de génération runtime, déterminisme de validation, atomicity des patchs).[cite:2]
- Encadrement opérationnel des `validated_derived_execution_projections` avant usage comme artefact unique (stockage, validators, régénération, emplacement).[cite:3]
- Clarification de la gouvernance release entre `current/` et manifest officiel pour les artefacts `platform_factory`.[cite:2]
- Révision du state pour aligner le niveau de maturité déclaré sur la réalité outillée.[cite:3]

## Points rejetés

Aucun challenge report ne propose de renverser les principes structurants suivants :
- séparation nette architecture / state ;
- principe de non-duplication normative entre Constitution et factory ;
- usage de projections dérivées comme outil de travail IA ;
- posture de challenge d’une baseline released plutôt qu’audit de découverte.[cite:2]

Ces fondations sont donc **rejetées comme cibles de patch** dans le cadre de ce stage, sauf si un arbitrage humain ultérieur décide d’un repositionnement plus radical.

## Points différés

- Définition détaillée du protocole multi-IA (granularité des fragments, résolution de conflits, workflow de consolidation).[cite:3]
- Conception fine des schémas de projections dérivées et de leurs validators spécifiques.
- Mise en place complète de l’outillage d’observabilité minimal pour auditer l’absence d’appels réseau ou de génération runtime (format précis des signaux, seuils, tableaux de bord).

Ces sujets sont jugés importants mais peuvent être reportés à un patch ultérieur, après fermeture des écarts critiques sur le contrat minimal et la gouvernance release.

## Points hors périmètre

- Détails d’implémentation des applications spécifiques produites par la factory (logique métier, UX, contenu pédagogique, etc.).
- Arbitrage exhaustif des invariants applicables aux futurs pipelines d’instanciation domaine par domaine ; ces arbitrages relèvent de la couche aval.
- Refondation de la Constitution ou du Référentiel eux-mêmes, qui restent pris comme socle donné dans ce stage.[cite:2]

## Points sans consensus ou nécessitant discussion finale

- **Degré de contrainte souhaité sur le contrat minimal** : certains rapports suggèrent une projection très serrée des invariants constitutionnels, d’autres privilégient une approche plus progressive fondée sur l’observabilité et la gouvernance de release ; ce point devra être tranché humainement.[cite:3]
- **Emplacement exact des validators de projections dérivées** : factory vs infra vs pipeline d’instanciation ; les rapports n’aboutissent pas tous à la même répartition.[cite:3]
- **Granularité de la priorisation** : classement critique/élevé/modéré/faible parfois différent entre rapports pour un même point, en fonction de la sensibilité aux risques de dérive normative.[cite:2]

Ces sujets sont signalés pour discussion en consolidation finale plutôt que tranchés unilatéralement à ce stade.

## Corrections à arbitrer avant patch

Pour permettre un patch propre et cohérent avec la baseline released actuelle, les corrections suivantes sont proposées comme **pré-requis d’arbitrage** :

1. **Projeter explicitement les invariants constitutionnels critiques dans le contrat minimal**
   - Décider la liste minimale d’invariants qui doivent être reflétés dans le manifest, la validation minimale et l’observabilité d’une application produite.[cite:2]
   - Trancher la forme des garde-fous (champs obligatoires, signaux, validators, règles de projection).

2. **Définir le niveau minimal d’outillage pour les `validated_derived_execution_projections`**
   - Trancher l’emplacement principal de stockage et le protocole de régénération ;
   - Définir les invariants que chaque projection doit respecter et la manière de les vérifier ;
   - Clarifier la place des projections dans la gouvernance release (quelle version est considérée canonique, comment la traçabilité est assurée).[cite:3]

3. **Résoudre le trou de gouvernance entre `current/` et manifest**
   - Décider si la factory entre dans le manifest courant et à quelles conditions ;
   - Ou formaliser un statut intermédiaire explicite avec des garde-fous (par exemple : « expérimental current non-gouvernant ») ;
   - Aligner le state sur la décision prise.

4. **Recaler le niveau de maturité déclaré dans le state**
   - Reclasser les capacités aujourd’hui marquées `present` mais non instrumentées ;
   - Documenter les gaps restants de manière à guider la priorisation des patchs.

Ces corrections constituent le socle d’un patch ultérieur, qui devra rester strictement aligné sur la séparation des couches (canonique, architecture, state, pipeline, validators, release governance) et ne pas tenter de tout résoudre en une seule itération.
