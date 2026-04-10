# Proposition d’arbitrage — STAGE_02_FACTORY_ARBITRAGE

## arbitrage_run_id
`PFARB_20260410_GPT54_Q7M4`

## Date
2026-04-10

## Liste des challenge reports considérés

1. `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_GPT54_8KQ2.md`
2. `docs/pipelines/platform_factory/work/01_challenge/challenge_report_01_Nemotron.md`

## Résumé exécutif

Les deux challenge reports convergent fortement sur un diagnostic central : la baseline `platform_factory` est bien placée en couche, honnête sur son caractère V0, et suffisamment structurée pour entrer en gouvernance ; en revanche, elle n’est pas encore assez fermée pour soutenir une prétention forte de conformité probante.

Le consensus fort porte sur quatre sujets à traiter avant patch :
- fermeture de la preuve de compatibilité constitutionnelle pour les applications produites ;
- fermeture de la gouvernance des `validated_derived_execution_projections` ;
- fermeture de la gouvernance `current/manifest/release` ;
- transformation du multi-IA de principe reconnu en mécanisme exploitable.

L’arbitrage proposé retient ces quatre sujets comme prioritaires. Il retient aussi un recalage ciblé de `platform_factory_state.yaml` là où l’état n’est plus parfaitement synchronisé avec l’architecture actuelle.

En revanche, il ne retient pas à ce stade une refonte lourde de taxonomie des métadonnées factory ni un durcissement prématuré de la V0 sur des schémas d’instanciation domaine encore hors périmètre.

---

## Synthèse des constats convergents

### Consensus fort

**CF-01 — Gap de preuve constitutionnelle**
Les deux rapports jugent que la factory vise la conformité constitutionnelle mais ne fournit pas encore une chaîne de preuve assez fermée pour rendre cette conformité réellement auditable, en particulier sur les invariants runtime les plus sensibles.

Sources :
- `challenge_report_PFCHAL_20260410_GPT54_8KQ2.md`
- `challenge_report_01_Nemotron.md`

**CF-02 — Mécanisme de projection dérivée insuffisamment fermé**
Consensus fort sur l’absence de validator dédié, l’absence de protocole de régénération et l’ambiguïté actuelle sur l’usage d’une projection comme contexte unique.

Sources :
- `challenge_report_PFCHAL_20260410_GPT54_8KQ2.md`
- `challenge_report_01_Nemotron.md`

**CF-03 — Gouvernance release/current/manifest incomplète**
Consensus fort sur le caractère encore partiellement ouvert du statut des artefacts `platform_factory_*` présents dans `docs/cores/current/` mais hors manifest officiel courant.

Sources :
- `challenge_report_PFCHAL_20260410_GPT54_8KQ2.md`
- `challenge_report_01_Nemotron.md`

**CF-04 — Multi-IA encore surtout déclaratif**
Consensus fort sur le fait que le multi-IA est bien reconnu comme exigence, mais qu’il reste non opérationnalisé faute de protocole de décomposition, d’assemblage et de résolution de conflit.

Sources :
- `challenge_report_PFCHAL_20260410_GPT54_8KQ2.md`
- `challenge_report_01_Nemotron.md`

### Consensus moyen

**CM-01 — Le contrat minimal d’application produite est bien orienté mais encore trop haut niveau**
Les deux rapports estiment que la structure générale du contrat est bonne, mais qu’elle reste encore insuffisamment probante pour garantir la conformité d’une application réelle.

**CM-02 — `platform_factory_state.yaml` doit être recalé sans être disqualifié**
Les deux rapports ne décrivent pas un state massivement trompeur. Ils décrivent plutôt un state globalement honnête, avec quelques décalages ou légères surdéclarations à corriger.

---

## Propositions d’arbitrage par thème

### Thème 1 — Compatibilité constitutionnelle des applications produites

#### DEC-PFARB-01
- Sujet : rendre probante la conformité aux invariants runtime critiques
- Source(s) : GPT54 + Nemotron
- Élément concerné : `produced_application_minimum_contract`, `minimum_validation_contract`, `minimum_observability_contract`
- Localisation : `docs/cores/current/platform_factory_architecture.yaml`
- Problème ou question : la conformité à `INV_RUNTIME_FULLY_LOCAL` et à l’absence de génération runtime interdite n’est pas encore rendue explicitement vérifiable
- Statut proposé : **retained**
- Patchability : **clarification_required_before_patch**
- Gravité : **critique**
- Justification : il s’agit d’un sujet de compatibilité constitutionnelle, pas d’un simple raffinement V0
- Dépendance éventuelle : liée à DEC-PFARB-02 et DEC-PFARB-04
- Lieu principal de traitement : **architecture**
- Lieu(x) secondaire(s) : **validator/tooling**, **manifest/release governance**
- Niveau de consensus perçu : **strong**

Arbitrage :
Le diagnostic est retenu. La factory doit expliciter, dans son contrat minimal et dans sa validation minimale, comment une application prouve qu’elle reste 100 % locale et sans génération runtime interdite. En revanche, l’arbitrage ne fixe pas encore la forme exacte du test ni la structure finale de la preuve ; cette définition doit être clarifiée avant patch pour éviter un wording creux.

### Thème 2 — Gouvernance des validated_derived_execution_projections

#### DEC-PFARB-02
- Sujet : lever l’ambiguïté sur l’usage des projections comme contexte unique
- Source(s) : GPT54 + Nemotron
- Élément concerné : `execution_projection_contract`
- Localisation : `docs/cores/current/platform_factory_architecture.yaml`
- Problème ou question : tension entre `rule_of_use` et `usage_as_sole_context: blocked`
- Statut proposé : **retained**
- Patchability : **immediate**
- Gravité : **élevé**
- Justification : contradiction interne de lecture, directement dangereuse pour une IA
- Dépendance éventuelle : aucune
- Lieu principal de traitement : **architecture**
- Lieu(x) secondaire(s) : **state**
- Niveau de consensus perçu : **strong**

Arbitrage :
Le diagnostic est retenu. L’architecture doit distinguer explicitement le régime cible et le régime V0 actuellement bloqué. Ce point peut être patché immédiatement par clarification de wording et synchronisation du state.

#### DEC-PFARB-03
- Sujet : fermer la chaîne de validation des projections dérivées
- Source(s) : GPT54 + Nemotron
- Élément concerné : lifecycle, validator, régénération, preuve de conformité
- Localisation : architecture + state + pipeline
- Problème ou question : le mécanisme est défini au niveau principe mais pas encore au niveau probant
- Statut proposé : **retained**
- Patchability : **clarification_required_before_patch**
- Gravité : **élevé**
- Justification : sujet central pour éviter la dérive normative multi-IA
- Dépendance éventuelle : liée à DEC-PFARB-01 et DEC-PFARB-05
- Lieu principal de traitement : **validator/tooling**
- Lieu(x) secondaire(s) : **architecture**, **pipeline**, **state**
- Niveau de consensus perçu : **strong**

Arbitrage :
Le diagnostic est retenu. Le bon lieu principal n’est pas seulement le contenu canonique : la fermeture passe surtout par validator/tooling et par pipeline. L’architecture doit seulement porter les règles minimales nécessaires ; le state doit constater l’absence et l’avancement ; le pipeline doit gouverner la production/validation.

#### DEC-PFARB-04
- Sujet : traiter la référence à `constitutional_conformance_matrix.yaml`
- Source(s) : GPT54 + Nemotron
- Élément concerné : `conformance_matrix_ref`, `constitutional_conformance_matrix_ref`
- Localisation : `docs/cores/current/platform_factory_architecture.yaml`
- Problème ou question : artefact référencé mais absent à ce stade
- Statut proposé : **retained**
- Patchability : **clarification_required_before_patch**
- Gravité : **élevé**
- Justification : référence morte dans une zone contractuelle sensible
- Dépendance éventuelle : liée à DEC-PFARB-01 et DEC-PFARB-03
- Lieu principal de traitement : **manifest/release governance**
- Lieu(x) secondaire(s) : **architecture**, **validator/tooling**, **state**
- Niveau de consensus perçu : **strong**

Arbitrage :
Le diagnostic est retenu. En revanche, l’arbitrage ne tranche pas encore si cette matrice doit vivre comme artefact canonique factory permanent, comme artefact de release gouverné, ou comme cible future explicitement bloquée. Cette question doit être clarifiée avant patch.

### Thème 3 — Contrat minimal d’une application produite

#### DEC-PFARB-05
- Sujet : rendre `runtime_policy_conformance` non creux
- Source(s) : surtout Nemotron, confirmé implicitement par GPT54
- Élément concerné : `minimum_validation_contract`
- Localisation : `docs/cores/current/platform_factory_architecture.yaml`
- Problème ou question : axe de validation présent mais insuffisamment défini
- Statut proposé : **retained**
- Patchability : **immediate**
- Gravité : **élevé**
- Justification : un axe vide ne doit pas rester dans un contrat minimal released
- Dépendance éventuelle : liée à DEC-PFARB-01
- Lieu principal de traitement : **architecture**
- Lieu(x) secondaire(s) : **validator/tooling**
- Niveau de consensus perçu : **medium**

Arbitrage :
Retenu. Même sans figer le schéma final de validation, l’architecture doit au moins expliciter le périmètre couvert par `runtime_policy_conformance`.

#### DEC-PFARB-06
- Sujet : traiter `bootstrap_contract_tbd_condition`
- Source(s) : GPT54 + Nemotron
- Élément concerné : `runtime_entrypoint_contract.bootstrap_contract_tbd_condition`
- Localisation : `docs/cores/current/platform_factory_architecture.yaml`
- Problème ou question : obligation reconnue mais encore non fermée
- Statut proposé : **deferred**
- Patchability : **clarification_required_before_patch**
- Gravité : **modéré**
- Justification : important mais encore légitimement V0 si honnêtement borné
- Dépendance éventuelle : liée à la future typologie de runtimes d’application
- Lieu principal de traitement : **state**
- Lieu(x) secondaire(s) : **architecture**
- Niveau de consensus perçu : **medium**

Arbitrage :
Le sujet est réel mais n’exige pas nécessairement une fermeture complète maintenant. En revanche, il doit être mieux borné comme blocage ou gap explicite dans le state si son absence empêche une validation complète.

### Thème 4 — Gouvernance release / current / manifest

#### DEC-PFARB-07
- Sujet : fermer le statut officiel des artefacts factory présents dans `current/`
- Source(s) : GPT54 + Nemotron
- Élément concerné : `pipeline.md`, `platform_factory_state.yaml`, gouvernance manifeste
- Localisation : pipeline + state
- Problème ou question : split-brain possible entre “présent en current” et “officiellement gouverné / manifesté”
- Statut proposé : **retained**
- Patchability : **clarification_required_before_patch**
- Gravité : **élevé**
- Justification : sujet de gouvernance transverse, à ne pas laisser au simple wording des YAML
- Dépendance éventuelle : liée à DEC-PFARB-04
- Lieu principal de traitement : **manifest/release governance**
- Lieu(x) secondaire(s) : **pipeline**, **state**
- Niveau de consensus perçu : **strong**

Arbitrage :
Le diagnostic est retenu. Le lieu principal de traitement n’est pas l’architecture mais la gouvernance de release/manifest, avec inscription explicite dans le pipeline et le state de la stratégie retenue.

### Thème 5 — Recalage de `platform_factory_state.yaml`

#### DEC-PFARB-08
- Sujet : recalage de l’état sur l’emplacement des projections désormais décidé
- Source(s) : GPT54 + Nemotron
- Élément concerné : `derived_projection_conformity_status.missing`, `assessed_scope.excludes`, `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED`
- Localisation : `docs/cores/current/platform_factory_state.yaml`
- Problème ou question : résidus de wording et de synchronisation après décision déjà actée
- Statut proposé : **retained**
- Patchability : **immediate**
- Gravité : **modéré**
- Justification : problème constatif réel, mais non structurellement critique
- Dépendance éventuelle : aucune
- Lieu principal de traitement : **state**
- Lieu(x) secondaire(s) : none
- Niveau de consensus perçu : **strong**

Arbitrage :
Retenu. Il faut nettoyer l’état pour qu’il n’affiche plus comme “missing” une décision déjà prise. En revanche, il n’est pas nécessaire de déclasser la capacité d’emplacement en capacité absente : la décision est bien prise, c’est l’outillage qui reste absent.

#### DEC-PFARB-09
- Sujet : revoir certaines formulations de maturité partielle / présente
- Source(s) : surtout Nemotron, partiellement corroboré par GPT54
- Élément concerné : `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` et potentiellement d’autres formulations de maturité
- Localisation : `docs/cores/current/platform_factory_state.yaml`
- Problème ou question : légère surdéclaration ou wording trop flatteur pour une V0
- Statut proposé : **retained**
- Patchability : **immediate**
- Gravité : **modéré**
- Justification : il faut une photographie honnête, sans sur-corriger
- Dépendance éventuelle : aucune
- Lieu principal de traitement : **state**
- Lieu(x) secondaire(s) : none
- Niveau de consensus perçu : **medium**

Arbitrage :
Retenu, avec modération. L’objectif n’est pas de “punir” le state mais d’aligner les formulations sur la réalité outillée.

### Thème 6 — Multi-IA parallel readiness

#### DEC-PFARB-10
- Sujet : transformer le multi-IA de principe reconnu en protocole exploitable
- Source(s) : GPT54 + Nemotron
- Élément concerné : `multi_ia_parallel_readiness`, `multi_ia_parallel_readiness_status`
- Localisation : architecture + state + pipeline
- Problème ou question : manque de protocole de décomposition, d’assemblage et de résolution de conflit
- Statut proposé : **retained**
- Patchability : **deferred**
- Gravité : **modéré**
- Justification : sujet important, mais qui peut être durci par étapes sans bloquer tout patch immédiat
- Dépendance éventuelle : liée au mécanisme de projection dérivée
- Lieu principal de traitement : **pipeline**
- Lieu(x) secondaire(s) : **architecture**, **state**, **validator/tooling**
- Niveau de consensus perçu : **strong**

Arbitrage :
Retenu comme report assumé à traiter dans un lot gouvernance/outillage dédié. Il ne faut pas l’absorber trop vite dans le canonique si le pipeline et l’outillage ne suivent pas.

---

## Points retenus

1. Fermer la preuve de conformité constitutionnelle des applications produites.
2. Clarifier immédiatement la contradiction sur `usage_as_sole_context`.
3. Traiter explicitement la référence morte à `constitutional_conformance_matrix.yaml`.
4. Définir au moins à haut niveau le contenu de `runtime_policy_conformance`.
5. Fermer la gouvernance du statut `current/manifest/release` des artefacts factory.
6. Recaler `platform_factory_state.yaml` sur l’emplacement des projections et sur quelques formulations de maturité.
7. Reconnaître comme sujet réel, mais non à tout fermer maintenant, le protocole multi-IA.

---

## Points rejetés

### REJ-01
- Élément concerné : ajout immédiat d’un nouveau champ générique de type `authority_rank` dans les métadonnées factory
- Localisation : métadonnées des deux YAML factory
- Problème ou question : Nemotron propose un marqueur explicite pour distinguer la factory des canoniques primaires
- Statut proposé : **rejected**
- Gravité : **modéré**
- Justification : le besoin de clarification de statut est réel, mais le bon lieu principal est la gouvernance manifest/current/release plutôt qu’une invention locale de taxonomie metadata non encore ancrée dans le modèle global des artefacts du repo
- Dépendance éventuelle : liée à DEC-PFARB-07
- Lieu probable de correction : **manifest/release governance**
- Niveau de consensus perçu : **weak**

Arbitrage :
Rejeté à ce stade. On traite le problème de statut officiel, mais pas par ajout opportuniste d’un nouveau champ metadata non gouverné à l’échelle du repo.

### REJ-02
- Élément concerné : reclassement de `PF_CAPABILITY_PROJECTION_STORAGE_LOCATION_FINALIZED` en capacité absente
- Localisation : `platform_factory_state.yaml`
- Problème ou question : surdéclaration supposée
- Statut proposé : **rejected**
- Gravité : **faible**
- Justification : la décision d’emplacement est bien prise ; ce qui manque est l’outillage et l’usage opérationnel, pas la décision elle-même
- Dépendance éventuelle : aucune
- Lieu probable de correction : **state**
- Niveau de consensus perçu : **medium**

Arbitrage :
Rejeté. Il faut nettoyer le wording, pas effacer la décision déjà actée.

---

## Points différés

1. Schéma exact du manifest d’application produite.
2. Typologie exacte du runtime entrypoint et fermeture complète du `bootstrap_contract`.
3. Schéma exact de packaging et de configuration.
4. Protocole complet multi-IA d’assemblage et de résolution de conflit.
5. Vérification fine de fraîcheur des `reproducibility_fingerprints`.
6. Schéma homogène de reporting multi-IA.

Justification commune : sujets valides, mais dont la fermeture complète maintenant surchargerait la V0 sans améliorer immédiatement la sûreté du prochain patchset autant que les décisions retenues prioritaires.

---

## Points hors périmètre

1. Logique détaillée du futur pipeline d’instanciation domaine.
2. Comportements runtime détaillés d’une application particulière.
3. Règles pédagogiques spécifiques au domaine produit.
4. Invariants constitutionnels de runtime qui ne relèvent pas du contrat minimal factory mais du moteur Learn-it lui-même, sauf lorsqu’ils doivent être rendus auditables par le contrat minimal générique.

---

## Points sans consensus ou nécessitant discussion finale

### DISC-01
- Sujet : nature exacte de `constitutional_conformance_matrix.yaml`
- Tension : artefact canonique factory, artefact de release, ou cible future bloquée
- Pourquoi discussion finale : le choix influence la gouvernance, le validator et la stratégie de manifest

### DISC-02
- Sujet : profondeur de correction à faire maintenant sur le contrat minimal d’application
- Tension : simple explicitation des axes critiques vs quasi-pré-spécification détaillée du schéma final
- Pourquoi discussion finale : éviter de surcharger la V0

### DISC-03
- Sujet : niveau exact de reclassement de certaines capacités du state
- Tension : légère correction de wording vs reclassement structurel plus sévère
- Pourquoi discussion finale : calibration de l’honnêteté du state sans le rendre artificiellement pessimiste

---

## Corrections à arbitrer avant patch

### ARB-PATCH-01
- Élément concerné : conformité runtime constitutionnelle des applications produites
- Localisation : architecture
- Problème ou question : invariants runtime critiques non encore rendus explicitement auditables
- Statut proposé : **retained**
- Gravité : **critique**
- Justification : conditionne la crédibilité constitutionnelle de la factory
- Dépendance éventuelle : DISC-01
- Lieu probable de correction : **architecture**
- Niveau de consensus perçu : **strong**

### ARB-PATCH-02
- Élément concerné : contradiction `usage_as_sole_context`
- Localisation : architecture
- Problème ou question : contradiction interne de lecture
- Statut proposé : **retained**
- Gravité : **élevé**
- Justification : ambiguïté directement dangereuse pour les IA
- Dépendance éventuelle : aucune
- Lieu probable de correction : **architecture** puis **state**
- Niveau de consensus perçu : **strong**

### ARB-PATCH-03
- Élément concerné : référence à la matrice de conformité constitutionnelle
- Localisation : architecture + gouvernance release
- Problème ou question : référence morte et rôle non tranché
- Statut proposé : **retained**
- Gravité : **élevé**
- Justification : bloque la fermeture probante du mécanisme de projection
- Dépendance éventuelle : DISC-01
- Lieu probable de correction : **manifest/release governance** avec impact secondaire **architecture** et **state**
- Niveau de consensus perçu : **strong**

### ARB-PATCH-04
- Élément concerné : `runtime_policy_conformance`
- Localisation : architecture
- Problème ou question : axe listé mais non défini
- Statut proposé : **retained**
- Gravité : **élevé**
- Justification : empêche une validation intelligible
- Dépendance éventuelle : ARB-PATCH-01
- Lieu probable de correction : **architecture** puis **validator/tooling**
- Niveau de consensus perçu : **medium**

### ARB-PATCH-05
- Élément concerné : état constatif des projections et de la maturité pipeline
- Localisation : state
- Problème ou question : quelques résidus de wording et de synchronisation
- Statut proposé : **retained**
- Gravité : **modéré**
- Justification : améliore la fidélité constatative sans changer la philosophie de la V0
- Dépendance éventuelle : aucune
- Lieu probable de correction : **state**
- Niveau de consensus perçu : **strong**

---

## Clarifications requises avant patch

1. Définir le statut exact attendu de `constitutional_conformance_matrix.yaml`.
2. Définir jusqu’où l’on va maintenant dans la preuve de conformité runtime sans sur-spécifier toute l’instanciation.
3. Définir si `bootstrap_contract` doit être seulement mieux borné dans le state ou partiellement structuré dès maintenant dans l’architecture.
4. Définir quel est le premier lot minimal réaliste pour la gouvernance des projections : simple verrouillage textuel, validator minimal, ou protocole pipeline plus large.

---

## Répartition par lieu de correction

### Architecture
- explicitation de la conformité runtime critique
- clarification `usage_as_sole_context`
- contenu minimal de `runtime_policy_conformance`
- éventuel bornage supplémentaire du contrat minimal

### State
- nettoyage des `missing` obsolètes
- recalage de certaines formulations de maturité
- éventuel enregistrement plus honnête de blockers ou gaps encore ouverts

### Pipeline
- gouvernance concrète de production/validation des projections
- futur protocole multi-IA par étapes
- articulation claire avec Stage 07/08/09 si nécessaire

### Validator/tooling
- validation des projections dérivées
- validation probante des axes runtime critiques
- fermeture de la chaîne de régénération et de conformité

### Manifest / release governance
- statut officiel des artefacts factory en `current/`
- rôle et place de la matrice de conformité constitutionnelle
- fermeture du lien entre current, release et manifest

---

## Séquencement recommandé si nécessaire

1. **Clarifier l’architecture** sur les points de contradiction immédiate et sur le périmètre de la conformité runtime.
2. **Recaler le state** en cohérence stricte avec l’architecture actuelle.
3. **Trancher la gouvernance** de la matrice de conformité et du statut current/manifest.
4. **Définir le minimum validator/tooling** nécessaire pour que les projections et la conformité runtime ne restent pas purement déclaratives.
5. **Reporter explicitement** le lot multi-IA avancé dans une étape ultérieure gouvernée, sans le laisser implicite.

---

## Priorités de patch

### Critique
- ARB-PATCH-01

### Élevé
- ARB-PATCH-02
- ARB-PATCH-03
- ARB-PATCH-04

### Modéré
- ARB-PATCH-05
- lot multi-IA opérationnel
- lot bootstrap/runtime entrypoint détaillé

---

## Conclusion

Cette proposition d’arbitrage confirme la robustesse conceptuelle générale de la baseline `platform_factory`, mais refuse de traiter comme “déjà fermé” ce qui reste seulement bien intentionné. Le patch suivant doit rester borné, cohérent, et concentré sur la fermeture des failles de preuve et de gouvernance les plus structurantes, sans transformer prématurément la V0 en spécification exhaustive.