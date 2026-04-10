# Proposition d’arbitrage — STAGE_02_FACTORY_ARBITRAGE

**arbitrage_run_id :** `PFARB_20260410_GPT54_N8Q2`  
**Date :** 2026-04-10

## Challenge reports considérés

- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_K7R2.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_9KR3.md`
- `docs/pipelines/platform_factory/work/01_challenge/challenge_report_PFCHAL_20260410_PERPLX_8ZQA.md`

## Résumé exécutif

Les trois challenge reports convergent fortement sur le diagnostic principal : la baseline V0.4 est structurellement solide, mais elle n’est pas encore probante sur les points de conformité constitutionnelle qui dépendent d’une matrice de conformité, de validateurs dédiés, et d’un cadrage plus opératoire du régime multi-IA.

La présente proposition d’arbitrage retient immédiatement six axes de correction avant patch :  
1. matérialiser la `constitutional_conformance_matrix.yaml` ;  
2. traiter l’absence de validateurs comme un problème de force probatoire explicite ;  
3. borner le `bootstrap_contract` pour éviter une validation minimale impossible ;  
4. rendre opérationnelle l’interdiction V0 de `usage_as_sole_context` pour les projections dérivées ;  
5. rehausser la gouvernance du protocole multi-IA ;  
6. aligner le pipeline et le state sur les conventions réellement utilisées.

Cette proposition rejette les sur-corrections qui déplaceraient prématurément de l’autorité normative vers la factory ou vers un nouveau système de statuts ad hoc. Elle diffère enfin un sujet réel mais non consensuel : l’extension immédiate du contrat minimal factory à d’autres invariants constitutionnels récemment ajoutés.

## Synthèse des constats convergents

### Consensus fort

- L’absence de `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` est un bloqueur réel et non un simple manque documentaire.
- Le `bootstrap_contract` obligatoire mais `TBD` empêche toute validation complète du contrat minimal d’une application produite.
- L’absence de validateurs dédiés rend non probants :
  - tout `validation_status: validated` sur une projection dérivée ;
  - tout signal `constitutional_invariants_checked`.
- Le régime cible des projections dérivées est décrit, mais la politique V0 actuelle (`usage_as_sole_context: blocked`) n’est pas encore suffisamment gardée par le pipeline ou l’outillage.
- Le protocole multi-IA n’est pas opérationnel alors même que le travail parallèle est érigé en exigence structurante.
- Le pipeline et le state surestiment ou documentent imparfaitement certains points d’exécutabilité et de conventions de stage.

### Consensus moyen

- Le mécanisme de dérive / comparaison associé à `version_fingerprint` doit être mieux défini.
- Le wording `declared_autonomy_regime_respected` gagnerait à être mieux relié à une source normative ou mieux borné.
- Le suivi de l’exécutabilité réelle de STAGE_04 devrait apparaître plus explicitement dans le state.

### Faible consensus / divergence

- Faut-il intégrer dès maintenant au contrat minimal factory des invariants supplémentaires comme :
  - `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`
  - `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION`
  - `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION`
  
  Le sujet est légitime, mais un seul challenge report le pousse de façon structurée. L’arbitrage proposé est donc de le différer pour consolidation finale, plutôt que de l’imposer immédiatement dans le patch.

## Propositions d’arbitrage par thème

### Thème 1 — Conformité constitutionnelle et force probatoire

| Decision ID | Élément concerné | Localisation | Problème / question | Statut proposé | Gravité | Source(s) | Justification | Dépendance éventuelle | Lieu probable de correction | Consensus |
|---|---|---|---|---|---|---|---|---|---|---|
| ARB-01 | `constitutional_conformance_matrix.yaml` | `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` | Artefact référencé obligatoire mais absent | retained | critique | K7R2, 9KR3, 8ZQA | Sans matrice, toute projection ou application qui y réfère reste constitutionnellement non auditable | aucune | architecture + validator/tooling + state | strong |
| ARB-02 | Force probatoire des validations | `platform_factory_architecture.yaml` / `platform_factory_state.yaml` | `validation_status: validated` et `constitutional_invariants_checked` ne sont pas probants sans validator | retained | critique | K7R2, 9KR3, 8ZQA | Il faut arbitrer explicitement qu’aucun de ces signaux n’a de valeur probante avant outillage dédié | ARB-01 renforce mais n’est pas le seul prérequis | state + validator/tooling + architecture | strong |
| ARB-03 | `bootstrap_contract` | `platform_factory_architecture.yaml` → `runtime_entrypoint_contract` | Champ obligatoire encore `TBD` | retained | critique | K7R2, 9KR3, 8ZQA | Le contrat minimal d’une application produite reste incomplet tant que ce champ n’est pas défini ou explicitement neutralisé | aucune | architecture | strong |
| ARB-04 | `declared_autonomy_regime_respected` | `platform_factory_architecture.yaml` | Obligation utile mais source normative insuffisamment explicite | deferred | modéré | K7R2 | Le sujet est valable, mais ne bloque pas le patch prioritaire ; à traiter lors de la consolidation du contrat minimal | aucune | architecture | medium |

### Thème 2 — Projections dérivées et régime d’usage

| Decision ID | Élément concerné | Localisation | Problème / question | Statut proposé | Gravité | Source(s) | Justification | Dépendance éventuelle | Lieu probable de correction | Consensus |
|---|---|---|---|---|---|---|---|---|---|---|
| ARB-05 | `usage_as_sole_context: blocked` | architecture + prompts/stages utilisant des projections | Politique V0 correcte en principe mais insuffisamment contrainte en pratique | retained | élevé | K7R2, 8ZQA, 9KR3 | Le blocage V0 doit être rappelé et rendu opératoire dans le pipeline, pas seulement décrit dans l’architecture | ARB-01 et ARB-02 restent les prérequis de déblocage futur | pipeline + validator/tooling + architecture | strong |
| ARB-06 | `version_fingerprint` et régénération | `platform_factory_architecture.yaml` | Mécanisme de comparaison / détection de dérive insuffisamment défini | retained | élevé | K7R2, 9KR3, 8ZQA | Le principe existe, mais la dérive des projections ne peut pas être traitée proprement sans règle de comparaison | aucune | architecture + pipeline | medium |
| ARB-07 | Reclassement de `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` vers un statut ad hoc | `platform_factory_state.yaml` | Proposition de créer une taxonomie plus fine type `blocked_pending_conditions` | rejected | faible | 9KR3 | Le problème réel est un problème de wording et de gouvernance, pas d’invention d’une nouvelle taxonomie de state dans ce cycle | aucune | state | medium |

### Thème 3 — Multi-IA et assemblage

| Decision ID | Élément concerné | Localisation | Problème / question | Statut proposé | Gravité | Source(s) | Justification | Dépendance éventuelle | Lieu probable de correction | Consensus |
|---|---|---|---|---|---|---|---|---|---|---|
| ARB-08 | `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` | `platform_factory_state.yaml` + `pipeline.md` | Gap reconnu comme “BLOCKER OPÉRATIONNEL” mais insuffisamment formalisé | retained | élevé | K7R2, 9KR3, 8ZQA | Le fond du problème est consensuel. Il faut le traiter comme une dépendance de gouvernance réelle avant travail multi-IA effectif | aucune | state + pipeline | strong |
| ARB-09 | Sévérité exacte et classification formelle du gap multi-IA | `platform_factory_state.yaml` | Faut-il le passer en blocker `high`, `medium`, ou le conserver en gap renforcé ? | deferred | modéré | 9KR3, 8ZQA, K7R2 (implicite) | Le sujet doit être discuté en consolidation finale : consensus sur le problème, pas encore sur la bonne taxonomie ni la sévérité exacte | ARB-08 | state | conflicting |

### Thème 4 — Pipeline, naming et traçabilité d’exécution

| Decision ID | Élément concerné | Localisation | Problème / question | Statut proposé | Gravité | Source(s) | Justification | Dépendance éventuelle | Lieu probable de correction | Consensus |
|---|---|---|---|---|---|---|---|---|---|---|
| ARB-10 | STAGE_04 et wording “exécutable manuellement” | `platform_factory_state.yaml` | La description actuelle sous-estime la dépendance à un script obligatoire pour STAGE_04 | retained | modéré | K7R2, 9KR3 | Le state doit refléter plus honnêtement l’exécutabilité réelle du pipeline | aucune | state | strong |
| ARB-11 | Référencement STAGE_01 / conventions de nommage | `pipeline.md` | Incohérence entre `challenge_report_##.md`, le vrai format `PFCHAL_...`, et le niveau prompt métier vs launch prompt | retained | modéré | K7R2, 9KR3, 8ZQA | Ce sujet ne touche pas le canonique, mais il dégrade la lisibilité et le travail parallèle | aucune | pipeline | strong |
| ARB-12 | Lecture obligatoire du manifest release courant et des specs STAGE_07/08 en challenge | launch prompt STAGE_01 | Sujet utile mais non indispensable au patch prioritaire | deferred | faible à modéré | 8ZQA | Amélioration plausible du challenge, mais non prérequise pour fermer les blockers critiques déjà identifiés | aucune | pipeline | weak |

### Thème 5 — Extension éventuelle du contrat minimal factory

| Decision ID | Élément concerné | Localisation | Problème / question | Statut proposé | Gravité | Source(s) | Justification | Dépendance éventuelle | Lieu probable de correction | Consensus |
|---|---|---|---|---|---|---|---|---|---|---|
| ARB-13 | Ajout immédiat de `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` au contrat minimal factory | `platform_factory_architecture.yaml` | Invariant constitutionnel réel, mais pertinence au niveau du contrat minimal générique encore à trancher | deferred | élevé potentiel | 8ZQA | Ne pas surcharger la V0 sans validation consolidée sur la bonne couche de traitement | aucune | architecture + consolidation finale | weak |
| ARB-14 | Ajout immédiat de `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` au contrat minimal factory | `platform_factory_architecture.yaml` | Invariant réel et pertinent, mais non encore consensuellement intégré au contrat minimal générique | deferred | élevé potentiel | 8ZQA | Sujet sérieux ; différé pour éviter une extension non consolidée du contrat minimal | aucune | architecture + consolidation finale | weak |
| ARB-15 | Ajout immédiat de `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION` au contrat minimal factory | `platform_factory_architecture.yaml` | Lien plausible avec les applications produites, mais sujet encore plus indirect | out_of_scope | modéré | 8ZQA | Relevé valable pour l’écosystème Learn-it, mais pas assez directement factory-minimal pour ce patch | aucune | futur pipeline d’instanciation / validation aval | weak |

## Points retenus

- **ARB-01** — créer et gouverner la `constitutional_conformance_matrix.yaml`.
- **ARB-02** — expliciter que les signaux de validation et de conformité constitutionnelle sont non probants sans validators dédiés.
- **ARB-03** — définir le `bootstrap_contract` ou formaliser explicitement le statut des axes qui en dépendent.
- **ARB-05** — rendre contraignante la politique V0 `usage_as_sole_context: blocked`.
- **ARB-06** — définir un mécanisme clair de comparaison / dérive pour `version_fingerprint` et la régénération.
- **ARB-08** — formaliser le sujet multi-IA comme dépendance de gouvernance réelle.
- **ARB-10** — corriger le wording du state sur l’exécutabilité pipeline.
- **ARB-11** — aligner le pipeline sur les conventions effectives de prompt et de nommage.

## Points rejetés

- **ARB-07** — ne pas créer dans ce cycle une nouvelle taxonomie de maturité du state pour résoudre un problème essentiellement de wording.
- Rejet implicite de toute correction qui déplacerait l’autorité normative primaire du socle canonique vers la factory.
- Rejet implicite de toute tentative de faire porter à `platform_factory` la conception détaillée du pipeline d’instanciation aval.

## Points différés

- **ARB-04** — rattachement normatif exact de `declared_autonomy_regime_respected`.
- **ARB-09** — sévérité exacte et taxonomie formelle du gap multi-IA.
- **ARB-12** — extension des lectures obligatoires en STAGE_01.
- **ARB-13** — ajout de `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` au contrat minimal factory.
- **ARB-14** — ajout de `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` au contrat minimal factory.

## Points hors périmètre

- **ARB-15** — intégration immédiate de `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION` au contrat minimal factory.
- Détail du futur pipeline d’instanciation d’application.
- Logique métier spécifique, feedbacks de domaine, runtime d’une application particulière.
- Refonte transverse complète du schéma `current manifest` au-delà de ce qui est strictement requis pour tracer la promotion factory.

## Points sans consensus ou nécessitant discussion finale

1. **Classification formelle du risque multi-IA**  
   Le besoin de correction est consensuel ; la bonne traduction dans le `state` ne l’est pas encore complètement.

2. **Périmètre exact du contrat minimal factory**  
   Les invariants supplémentaires cités par le rapport `PFCHAL_20260410_PERPLX_8ZQA` existent bien dans la Constitution, mais leur intégration immédiate au contrat minimal factory n’est pas encore corroborée par les autres rapports.

3. **Niveau exact de correction autour de `declared_autonomy_regime_respected`**  
   Faut-il ajouter un `invariant_ref`, reformuler l’item, ou le laisser au niveau de politique déclarée ? Discussion finale requise.

4. **Lecture obligatoire du manifest release courant dès STAGE_01**  
   Amélioration plausible, mais pas encore une condition reconnue comme indispensable par les autres rapports.

## Répartition par lieu probable de correction

| Sujet | Lieu principal | Lieu(x) secondaire(s) |
|---|---|---|
| Matrice de conformité | architecture | validator/tooling, state |
| Force probatoire des validations | state | architecture, validator/tooling |
| `bootstrap_contract` | architecture | — |
| Garde opérationnelle de `usage_as_sole_context` | pipeline | architecture, validator/tooling |
| Dérive / `version_fingerprint` | architecture | pipeline |
| Protocole multi-IA | pipeline | state |
| Wording sur STAGE_04 et exécutabilité | state | pipeline |
| Référencement STAGE_01 et nommage reports | pipeline | — |

## Séquencement recommandé si patch confirmé

1. **Fermer les blockers probatoires**  
   ARB-01, ARB-02, ARB-03.

2. **Éviter les usages dangereux avant maturité**  
   ARB-05, puis ARB-08.

3. **Nettoyer la gouvernance documentaire et l’exécutabilité réelle du pipeline**  
   ARB-10, ARB-11.

4. **Traiter les renforcements non critiques après consolidation finale**  
   ARB-04, ARB-09, ARB-12, ARB-13, ARB-14.

## Corrections à arbitrer avant patch

### CAP-01 — Matérialiser la matrice de conformité constitutionnelle
- **Élément concerné :** `constitutional_conformance_matrix.yaml`
- **Localisation :** `docs/cores/platform_factory/constitutional_conformance_matrix.yaml`
- **Problème :** référence obligatoire actuellement vide
- **Statut proposé :** retained
- **Gravité :** critique
- **Justification :** prérequis à toute auditabilité constitutionnelle sérieuse
- **Dépendances :** aucune
- **Lieu probable de correction :** architecture + validator/tooling
- **Consensus :** strong

### CAP-02 — Borner explicitement la non-probativité des statuts de validation
- **Élément concerné :** `validation_status: validated`, `constitutional_invariants_checked`
- **Localisation :** architecture + state
- **Problème :** signaux trop faciles à lire comme “validés” alors que l’outillage manque
- **Statut proposé :** retained
- **Gravité :** critique
- **Justification :** évite une fausse fermeture normative
- **Dépendances :** CAP-01 souhaitable mais non indispensable
- **Lieu probable de correction :** state principal, puis validator/tooling
- **Consensus :** strong

### CAP-03 — Définir le `bootstrap_contract` ou neutraliser explicitement les axes dépendants
- **Élément concerné :** `runtime_entrypoint_contract`
- **Localisation :** `platform_factory_architecture.yaml`
- **Problème :** obligation impossible à satisfaire en l’état
- **Statut proposé :** retained
- **Gravité :** critique
- **Justification :** sans cela, aucune application produite ne peut passer une validation complète honnête
- **Dépendances :** aucune
- **Lieu probable de correction :** architecture
- **Consensus :** strong

### CAP-04 — Rendre opératoire l’interdiction V0 `usage_as_sole_context`
- **Élément concerné :** projections dérivées
- **Localisation :** pipeline + launch prompts + validator
- **Problème :** politique correcte mais encore seulement déclarative
- **Statut proposé :** retained
- **Gravité :** élevé
- **Justification :** évite un usage prématuré des projections comme contexte unique
- **Dépendances :** CAP-01 et CAP-02 pour le déblocage futur
- **Lieu probable de correction :** pipeline
- **Consensus :** strong

### CAP-05 — Formaliser le minimum multi-IA exploitable
- **Élément concerné :** protocole d’assemblage, granularité, résolution de conflits
- **Localisation :** `pipeline.md` + `platform_factory_state.yaml`
- **Problème :** exigence multi-IA sans protocole d’exécution réel
- **Statut proposé :** retained
- **Gravité :** élevé
- **Justification :** empêche les collisions normatives entre sorties parallèles
- **Dépendances :** aucune
- **Lieu probable de correction :** pipeline principal, state secondaire
- **Consensus :** strong

### CAP-06 — Aligner le pipeline et le state sur la réalité d’exécution
- **Élément concerné :** STAGE_04, STAGE_01, conventions de fichiers
- **Localisation :** `pipeline.md` + `platform_factory_state.yaml`
- **Problème :** incohérences de prompt, naming et wording d’exécutabilité
- **Statut proposé :** retained
- **Gravité :** modéré
- **Justification :** réduit les ambiguïtés opérationnelles avant STAGE_03
- **Dépendances :** aucune
- **Lieu probable de correction :** pipeline + state
- **Consensus :** strong

---
*Fin du rapport — `PFARB_20260410_GPT54_N8Q2`*
