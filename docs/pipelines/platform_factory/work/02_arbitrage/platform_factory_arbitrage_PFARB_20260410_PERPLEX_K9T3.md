# Proposition d'arbitrage — STAGE_02_FACTORY_ARBITRAGE

## arbitrage_run_id
`PFARB_20260410_PERPLEX_K9T3`

## Date
2026-04-10

## Challenge reports considérés

- `challenge_report_PFCHAL_20260410_GPT54_Z4N8.md`
- `challenge_report_PFCHAL_20260410_PERPLEX_9KR4M.md`
- `challenge_report_PFCHAL_20260410_PERPLX_8ZQA.md`
- `challenge_report_PFCHAL_20260410_PERPLX_9KR3.md`
- `challenge_report_PFCHAL_20260410_PERPLX_K7R2.md`

---

## Résumé exécutif

Les cinq challenge reports convergent sur un diagnostic cohérent : la Platform Factory V0.4 est une baseline fondatrice crédible, bien séparée du socle canonique, avec une posture normative saine. Elle n'est pas trop faible pour être gouvernée, mais elle ne peut pas encore soutenir les deux affirmations les plus fortes du dispositif — conformité constitutionnelle probante d'une application produite, et validation auditée d'une projection dérivée.

Les risques critiques sont unanimes (conformance matrix absente, validators absents, bootstrap_contract TBD). Les risques élevés sont également très convergents (multi-IA non opérationnel, wording maturité surdéclaré, script STAGE_04 absent). Quelques points divergent sur la formulation ou le lieu de traitement ; ces points sont tranchés ci-dessous.

L'arbitrage propose de traiter maintenant les corrections qui débloqueront un cycle de patch propre et borné, de reporter ce qui relève d'une itération dédiée, et de ne pas surcharger la V0 avec des exigences prématurées.

---

## Synthèse des constats convergents

Les cinq rapports s'accordent sur les points suivants :

1. **Conformance matrix absente** (`PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT`) — unanime, gravité critique dans tous les rapports. Toute projection et tout signal `constitutional_invariants_checked` sont non auditables.
2. **Validator dédié absent** (`PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` absent) — unanime. Signaux PASS non probants.
3. **Bootstrap_contract TBD** (`PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED`) — unanime, gravité élevée à critique. Aucune application ne peut passer la validation complète du contrat minimal.
4. **Multi-IA non opérationnel** (`PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED`) — unanime, signalé comme BLOCKER OPÉRATIONNEL dans tous les rapports, mais classé `known_gap` et non `blocker` formel dans le state.
5. **Wording `exécutable manuellement` dans `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`** — signalé dans 4 rapports comme maturité surdéclarée pour les stages avec script obligatoire.
6. **Script `validate_platform_factory_patchset.py` absent** — signalé dans 4 rapports. STAGE_04 non exécutable dans sa forme canonique.
7. **`usage_as_sole_context: blocked` sans garde-fou technique** — signalé dans 4 rapports. Politique déclarative sans enforcement.
8. **Séparation prescriptif/constatif solide, non-duplication normative bien tenue** — point de consensus fort positif dans tous les rapports.
9. **Gouvernance de promotion vers `current/` non outillée** — unanime. Rule 6 pipeline déclarative sans garde-fou.
10. **Convention de nommage challenge reports incohérente entre `pipeline.md` et launch prompt** — signalé dans 2 rapports.

---

## Propositions d'arbitrage par thème

---

### THEME-01 — Conformance matrix constitutionnelle absente

**ARB-01**
- **Élément concerné** : `constitutional_conformance_matrix_ref` dans architecture + blocker `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` dans state
- **Sources** : GPT54_Z4N8 (R1), PERPLEX_9KR4M (C1), PERPLX_8ZQA (C1), PERPLX_9KR3 (R2/C1 upgrade blocker), PERPLX_K7R2 (C1)
- **Statut proposé** : **retained**
- **Gravité** : Critique
- **Justification** : Convergence unanime. Sans cette matrice, toute conformité constitutionnelle déclarée dans une projection ou une application produite est non auditable. C'est le précondition de déblocage de `usage_as_sole_context`. Ne pas traiter maintenant condamne l'ensemble de la chaîne de validation.
- **Lieu probable de correction** : validator/tooling (création de l'artefact) + architecture (note de disponibilité) + state (mise à jour du blocker avec exit_condition et date cible)
- **Niveau de consensus** : strong
- **Décision** : Créer `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` dans un cycle dédié (peut être STAGE_03 ou un cycle off-pipeline). Ajouter dans l'architecture une note de disponibilité sur `conformance_matrix_ref` (signaler l'indisponibilité). Ajouter dans le state une `exit_condition` et une `target_date` indicative pour `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT`.
- **Dépendance** : Précondition de ARB-05 (déblocage usage_as_sole_context) et de ARB-02 (validator).

---

### THEME-02 — Validator dédié absent

**ARB-02**
- **Élément concerné** : `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` absent dans state ; signal `constitutional_invariants_checked` non probant
- **Sources** : tous les rapports, convergence forte
- **Statut proposé** : **retained** pour la correction de gouvernance dans le state ; **deferred** pour l'implémentation effective des validators
- **Gravité** : Critique (constat) / Élevée (patch immédiat)
- **Justification** : L'absence de validator est reconnue et documentée. Il n'est pas possible de créer les validators dans ce cycle de patch (périmètre trop large). En revanche, il est possible et nécessaire de : (a) élever l'absence de validator au rang de blocker `high` dans le state avec exit_condition explicite (trois validators prioritaires : `derived_projection_conformance`, `minimum_contract_conformance`, `runtime_policy_conformance`) ; (b) ajouter dans l'architecture une contrainte explicite interdisant l'émission de `constitutional_invariants_checked: PASS` tant que `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` est absent, sauf pour les vérifications statiques documentées comme protocole manuel minimal.
- **Lieu probable de correction** : state (blocker) + architecture (note contrainte d'émission)
- **Niveau de consensus** : strong
- **Point de divergence traité** : PERPLX_9KR3 propose d'élever dans les blockers avec sévérité `high` ; PERPLEX_9KR4M propose une interdiction d'émission dans l'architecture. Les deux sont retenus cumulativement : correction state ET correction architecture.

---

### THEME-03 — Bootstrap_contract TBD

**ARB-03**
- **Élément concerné** : `runtime_entrypoint_contract.bootstrap_contract` dans architecture ; `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` dans state
- **Sources** : GPT54_Z4N8 (R3), PERPLEX_9KR4M (C4), PERPLX_8ZQA (A4-1), PERPLX_9KR3 (R5), PERPLX_K7R2 (C2)
- **Statut proposé** : **retained** pour arbitrage de traitement V0 ; **deferred** pour la définition complète de la typology runtime
- **Gravité** : Élevée à Critique
- **Justification** : Convergence unanime. L'arbitrage retient l'option proposée par PERPLEX_9KR4M et PERPLX_K7R2 : plutôt que de laisser TBD sans borne, arbitrer entre (a) définir un scope minimal V0 du bootstrap avec interdiction explicite d'appel réseau/LLM, ou (b) inscrire explicitement que les axes de validation dépendants sont en état `DEFERRED_UNTIL_BOOTSTRAP_DEFINED`. L'option (a) est préférable car elle ferme le risque de brèche sans bloquer la V0.
- **Lieu probable de correction** : architecture
- **Niveau de consensus** : strong
- **Décision** : Patch architecture pour ajouter une contrainte minimale V0 du bootstrap : "aucun appel réseau autorisé au bootstrap, aucun appel LLM, dépendances uniquement locales". La définition complète de la typology runtime reste différée.

---

### THEME-04 — Multi-IA : reclassification du gap en blocker

**ARB-04**
- **Élément concerné** : `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` dans state
- **Sources** : GPT54_Z4N8 (R4), PERPLEX_9KR4M (C6), PERPLX_8ZQA (A7-1/C4), PERPLX_9KR3 (R4/C2), PERPLX_K7R2 (axe 7)
- **Statut proposé** : **retained**
- **Gravité** : Élevée
- **Justification** : Le gap se désigne lui-même comme "BLOCKER OPÉRATIONNEL" dans sa description mais n'est pas listé dans `blockers`. Cette asymétrie de classification est unanimement signalée. La correction est simple et non risquée : déplacer vers `blockers` avec sévérité `medium`, exit condition = spec du protocole multi-IA (décomposition, assemblage, résolution de conflit). Cela ne crée pas d'obligation d'implémentation immédiate mais ferme l'asymétrie de gouvernance.
- **Lieu probable de correction** : state
- **Niveau de consensus** : strong
- **Dépendance** : indépendant des autres corrections.

---

### THEME-05 — Politique `usage_as_sole_context: blocked` non contraignante

**ARB-05**
- **Élément concerné** : `execution_projection_contract.usage_as_sole_context: blocked` dans architecture
- **Sources** : GPT54_Z4N8 (R2), PERPLEX_9KR4M (risque élevé), PERPLX_8ZQA (A5-1/C5), PERPLX_9KR3 (R3)
- **Statut proposé** : **retained** (renforcement normatif dans l'architecture et dans le pipeline)
- **Gravité** : Élevée
- **Justification** : Le blocage est déclaratif sans garde-fou technique. Il n'est pas possible de créer un garde-fou technique dans ce cycle, mais il est possible d'ajouter dans chaque launch prompt de stage utilisant des projections une instruction explicite rappelant ce blocage, et d'ajouter dans l'architecture une note de condition de déblocage liée à ARB-01 et ARB-02.
- **Lieu probable de correction** : architecture (note condition de déblocage) + pipeline (instructions launch prompts)
- **Niveau de consensus** : strong

---

### THEME-06 — Wording `exécutable manuellement` dans state

**ARB-06**
- **Élément concerné** : `capabilities_partial.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`
- **Sources** : PERPLEX_9KR4M (axe 2), PERPLX_8ZQA (A2-1), PERPLX_9KR3 (axe 6), PERPLX_K7R2 (C3)
- **Statut proposé** : **retained**
- **Gravité** : Modérée
- **Justification** : La formulation "exécutable manuellement" est inexacte pour les stages à script obligatoire (notamment STAGE_04). Patch minimal dans state pour préciser explicitement que STAGE_04 est bloqué par l'absence de `validate_platform_factory_patchset.py`.
- **Lieu probable de correction** : state
- **Niveau de consensus** : strong

---

### THEME-07 — Script `validate_platform_factory_patchset.py` absent

**ARB-07**
- **Élément concerné** : STAGE_04 dans pipeline.md ; `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` absent dans state
- **Sources** : PERPLEX_9KR4M (C3), PERPLX_8ZQA (axe 9), PERPLX_9KR3 (C4/R6), PERPLX_K7R2 (C3)
- **Statut proposé** : **retained** pour le tracking dans le state ; **deferred** pour la création du script
- **Gravité** : Élevée (blocage pipeline) / Modérée pour la correction de traçabilité
- **Justification** : La création du script est hors périmètre d'un cycle d'arbitrage de contenu YAML/Markdown. Mais il est nécessaire de (a) rendre explicite dans le state que `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` absent implique un blocage STAGE_04, (b) documenter un protocole de validation manuelle fallback V0 dans le pipeline, acceptable avec limitation explicite.
- **Point de divergence traité** : PERPLEX_9KR4M propose trois options (créer script, fallback manuel, blocage STAGE_04). L'arbitrage retient l'option fallback manuel documenté explicitement, avec blocage formel en l'absence de script ET en l'absence du protocole fallback.
- **Lieu probable de correction** : state + pipeline
- **Niveau de consensus** : strong (sur la nécessité de tracer) / medium (sur l'option retenue)

---

### THEME-08 — Invariants constitutionnels absents du contrat minimal

**ARB-08**
- **Élément concerné** : `minimum_validation_contract.minimum_axes` dans architecture
- **Sources** : PERPLX_8ZQA (A1-1, A1-2, C2, C3), PERPLX_9KR3 (carte constitutionnelle)
- **Statut proposé** : **retained** pour deux invariants ; **deferred** pour les autres
- **Gravité** : Élevée
- **Justification** : Deux invariants forts signalés principalement par PERPLX_8ZQA sont absents du contrat minimal : `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` et `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION`. Le premier est particulièrement important car il touche directement le cycle de patch. Le second est un arbitrage récent (ARBITRAGE_2026_04_01) non encore répercuté. Ces deux ajouts sont retenus pour le patch car ils ne demandent que l'ajout d'axes de validation dans l'architecture, sans créer de nouveaux artefacts.
- **Lieu probable de correction** : architecture
- **Niveau de consensus** : medium (signalé principalement par PERPLX_8ZQA ; les autres rapports couvrent partiellement ces invariants via leur carte constitutionnelle)

---

### THEME-09 — Gouvernance manifest et promotion vers `current/`

**ARB-09**
- **Élément concerné** : `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` dans state ; Rule 6 pipeline
- **Sources** : tous les rapports convergent sur l'absence de garde-fou technique
- **Statut proposé** : **deferred** pour le garde-fou technique ; **retained** pour l'exit_condition existante
- **Gravité** : Modérée à Élevée
- **Justification** : Le blocker est correctement documenté avec exit_condition liée à STAGE_08. L'absence de garde-fou technique (protection de branche, hook) est un risque réel mais hors périmètre d'un patch YAML/Markdown. Aucun patch de contenu ne peut fermer ce risque. L'arbitrage retient la correction existante comme suffisante pour V0, sous condition que la dépendance circulaire signalée par PERPLX_9KR3 soit documentée explicitement dans le state : le cycle complet (STAGE_04 → STAGE_08) est lui-même bloqué par plusieurs prérequis absents.
- **Lieu probable de correction** : state (note de dépendance circulaire)
- **Niveau de consensus** : strong (sur le diagnostic) / medium (sur l'absence de correction technique V0)

---

### THEME-10 — Incohérence pipeline.md STAGE_01 et convention nommage

**ARB-10**
- **Élément concerné** : `pipeline.md` STAGE_01_CHALLENGE (référence prompt) et convention nommage challenge reports
- **Sources** : PERPLX_8ZQA (A2-1/A2-2/C6), PERPLX_9KR3 (axe 9), PERPLX_K7R2 (C6)
- **Statut proposé** : **retained**
- **Gravité** : Modérée
- **Justification** : Deux corrections simples, sans ambiguïté : (a) aligner pipeline.md pour distinguer le prompt métier partagé (`Challenge_platform_factory.md`) et le launch prompt d'exécution (`LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md`) ; (b) aligner la convention de nommage des challenge reports dans pipeline.md sur le format `challenge_run_id` défini dans le launch prompt (supprimer le format `##`).
- **Lieu probable de correction** : pipeline
- **Niveau de consensus** : strong

---

### THEME-11 — `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` : classification trop optimiste

**ARB-11**
- **Élément concerné** : `capabilities_partial.PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` dans state
- **Sources** : PERPLX_9KR3 (C6), PERPLX_K7R2 (axe 2/6)
- **Statut proposé** : **retained** (correction wording)
- **Gravité** : Faible à Modérée
- **Justification** : Le classement `partial` est trop optimiste car le blocage est structurel (deux conditions absentes). La correction proposée par PERPLX_9KR3 (conserver `partial` mais avec note explicite que le blocage est structurel, pas progressif) est retenue. La création d'un nouveau statut `blocked_pending_conditions` est reportée : cela nécessite une décision d'architecture du state plus large.
- **Lieu probable de correction** : state
- **Niveau de consensus** : medium

---

### THEME-12 — Fingerprints de reproductibilité : axe de validation manquant

**ARB-12**
- **Élément concerné** : `minimum_validation_contract.minimum_axes` dans architecture + `reproducibility_fingerprints` dans contrat minimal
- **Sources** : PERPLEX_9KR4M (axe 5), PERPLX_8ZQA (C7), PERPLX_9KR3 (R10)
- **Statut proposé** : **retained** (ajout d'un axe de validation)
- **Gravité** : Modérée
- **Justification** : Les fingerprints sont définis en intention mais aucun axe de validation minimale ne vérifie explicitement leur présence. L'ajout d'un axe `reproducibility_fingerprints_present_and_valid` est une correction légère et sans ambiguïté.
- **Lieu probable de correction** : architecture
- **Niveau de consensus** : medium

---

### THEME-13 — Manifest release non lu dans le challenge

**ARB-13**
- **Élément concerné** : `LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md` (périmètre de lecture obligatoire)
- **Sources** : PERPLX_8ZQA (A8-1/C8), PERPLX_9KR3 (A8)
- **Statut proposé** : **retained** (correction launch prompt)
- **Gravité** : Modérée
- **Justification** : Le manifest release courant (`PLATFORM_FACTORY_RELEASE_2026_04_10_R01/manifest.yaml`) n'est pas dans la liste de lecture obligatoire du challenge. L'ajouter ferme un trou de traçabilité sans coût.
- **Lieu probable de correction** : pipeline (launch prompt STAGE_01)
- **Niveau de consensus** : medium

---

### THEME-14 — `declared_autonomy_regime_respected` sans invariant source

**ARB-14**
- **Élément concerné** : `runtime_policy_conformance_definition.items_to_verify.declared_autonomy_regime_respected` dans architecture
- **Sources** : PERPLX_K7R2 (C5)
- **Statut proposé** : **deferred** avec note
- **Gravité** : Modérée
- **Justification** : Le point est valide mais la correction (trouver ou créer un `invariant_ref` constitutionnel source) nécessite une analyse de la Constitution qui dépasse le périmètre du présent cycle. La correction est reportée à un cycle dédié. En attendant, ajouter une note `invariant_ref_pending` dans l'élément concerné.
- **Lieu probable de correction** : architecture (note) + clarification constitutionnelle préalable
- **Niveau de consensus** : weak (signalé par un seul rapport)

---

### THEME-15 — Angle mort double-buffer pour patches d'artefacts factory internes

**ARB-15**
- **Élément concerné** : absence de mention de l'obligation constitutionnelle de double-buffer/swap atomique pour les patches d'artefacts factory internes
- **Sources** : PERPLEX_9KR4M (carte constitutionnelle — angle mort)
- **Statut proposé** : **deferred**
- **Gravité** : Modérée
- **Justification** : Le mécanisme de sandboxing dans `work/05_apply/` couvre implicitement ce besoin via la séparation sandbox/promote. La correction explicite dans l'architecture nécessite une réflexion sur le bon niveau de description (principe general vs règle opératoire). Différer à un cycle dédié multi-IA/gouvernance.
- **Lieu probable de correction** : architecture (futur cycle)
- **Niveau de consensus** : weak (signalé par un seul rapport)

---

### THEME-16 — `conformance_matrix_availability_status` dans le contrat de projection

**ARB-16**
- **Élément concerné** : `execution_projection_contract.mandatory_fields_per_projection.conformance_matrix_ref` dans architecture
- **Sources** : PERPLX_9KR3 (C5)
- **Statut proposé** : **retained** (correction légère)
- **Gravité** : Modérée
- **Justification** : Ajouter dans le contrat de projection une note imposant que lorsque `conformance_matrix_ref` pointe un fichier absent (blocker enregistré), la projection doit indiquer explicitement `conformance_matrix_status: unavailable`. Cela permet à une IA réceptrice de savoir qu'elle ne peut pas valider la conformité.
- **Lieu probable de correction** : architecture
- **Niveau de consensus** : medium

---

## Points retenus

| ARB | Thème | Lieu principal | Gravité |
|---|---|---|---|
| ARB-01 | Créer constitutional_conformance_matrix + ajouter exit_condition dans state | validator/tooling + state + architecture | Critique |
| ARB-02 | Élever validator absent en blocker + contrainte émission signal dans architecture | state + architecture | Critique |
| ARB-03 | Bootstrap_contract : scope minimal V0 anti-réseau/LLM dans architecture | architecture | Élevée |
| ARB-04 | Reclasser multi-IA gap en blocker formel avec exit_condition | state | Élevée |
| ARB-05 | Renforcer note condition de déblocage usage_as_sole_context + instructions launch prompts | architecture + pipeline | Élevée |
| ARB-06 | Corriger wording STAGE_04 dans state (pipeline non exécutable pour ce stage) | state | Modérée |
| ARB-07 | Documenter fallback manuel STAGE_04 + traçabilité dans state | state + pipeline | Élevée |
| ARB-08 | Ajouter INV_PATCH_PRECOMPUTED et INV_RUNTIME_QUALIFICATION dans contrat minimal | architecture | Élevée |
| ARB-09 | Documenter dépendance circulaire manifest/STAGE_08 dans state | state | Modérée |
| ARB-10 | Aligner pipeline.md STAGE_01 prompt + convention nommage | pipeline | Modérée |
| ARB-11 | Note wording blocage structurel sur PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED | state | Faible |
| ARB-12 | Ajouter axe validation fingerprints dans contrat minimal | architecture | Modérée |
| ARB-13 | Ajouter manifest release dans périmètre lecture obligatoire STAGE_01 | pipeline | Modérée |
| ARB-16 | Ajouter conformance_matrix_status: unavailable dans contrat de projection | architecture | Modérée |

---

## Points rejetés

Aucun finding des challenge reports n'est rejeté. Tous les findings convergents ont été retenus ou différés avec justification explicite. Les points "V0 acceptables" dans les rapports ne sont pas des findings rejetés mais des non-problèmes reconnus.

---

## Points différés

| ARB | Thème | Justification du report | Lieu futur |
|---|---|---|---|
| ARB-02 (impl.) | Implémentation effective des validators | Périmètre trop large pour ce cycle | Cycle dédié validator/tooling |
| ARB-07 (script) | Création de `validate_platform_factory_patchset.py` | Hors périmètre patch YAML/Markdown | Cycle dédié outillage |
| ARB-14 | `declared_autonomy_regime_respected` sans invariant source | Nécessite analyse Constitution préalable | Cycle constitution/referentiel |
| ARB-15 | Double-buffer pour patches factory internes | Déjà couvert implicitement par sandboxing ; clarification architecturale à différer | Cycle multi-IA/gouvernance |

---

## Points hors périmètre

- Définition de la typology complète des runtimes (relève du pipeline d'instanciation aval).
- Schémas fins de manifest, configuration, packaging (V0 assumé, différé itérations suivantes).
- Création de `docs/cores/platform_factory/projections/` physiquement (décision prise, opérationnalisation à faire hors cycle actuel).
- Logique métier domaine Learn-it (explicitement hors scope factory).
- Garde-fous techniques de protection de branche / hooks Git (hors périmètre patch contenu canonique).

---

## Points sans consensus ou nécessitant discussion finale

| Thème | Point de désaccord ou ambiguïté | Recommandation |
|---|---|---|
| ARB-07 option fallback | GPT54 et PERPLEX_9KR4M divergent sur le traitement : (a) définir fallback manuel, (b) bloquer STAGE_04 pur. L'arbitrage retient (a) mais un humain devrait confirmer la tolérance du fallback manuel pour la V0. | Confirmation humaine requise avant patch pipeline. |
| ARB-11 classement | Un rapport propose un nouveau statut `blocked_pending_conditions` vs. simple note. L'arbitrage choisit la note pour préserver la compatibilité du state V0. | Consolidation finale peut arbitrer différemment si décision d'évolution du state schema. |
| STAGE_02/03 launch prompts absents | PERPLX_8ZQA signale l'asymétrie (STAGE_02/03 sans launch prompt dédié). Le present cycle ne crée pas les launch prompts. Ce point n'est pas un finding de contenu YAML mais de complétion pipeline. | À traiter dans un cycle de complétion pipeline si confirmé nécessaire. |

---

## Corrections à arbitrer avant patch

Séquencement recommandé :

1. **Patch architecture** : ajouter contrainte d'émission du signal `constitutional_invariants_checked` (ARB-02) + scope minimal bootstrap V0 (ARB-03) + deux invariants au contrat minimal (ARB-08) + axe fingerprints (ARB-12) + note conformance_matrix_status dans contrat projection (ARB-16) + note condition de déblocage usage_as_sole_context (ARB-05).

2. **Patch state** : élever validator absent en blocker (ARB-02) + reclasser multi-IA gap en blocker (ARB-04) + corriger wording pipeline exécutable (ARB-06) + documenter dépendance circulaire manifest (ARB-09) + note blocage structurel projection rule (ARB-11) + ajouter exit_condition conformance_matrix blocker (ARB-01).

3. **Patch pipeline** : aligner pipeline.md STAGE_01 (ARB-10) + convention nommage challenge reports (ARB-10) + instructions usage_as_sole_context dans launch prompts (ARB-05) + fallback manuel STAGE_04 (ARB-07) + ajouter manifest release dans périmètre lecture STAGE_01 (ARB-13).

4. **Cycle dédié** (hors présent cycle) : créer `constitutional_conformance_matrix.yaml` (ARB-01 création artefact) + créer script validation STAGE_04 (ARB-07 script) + implémentation validators (ARB-02 implémentation).

---

*Fin de la proposition d'arbitrage — PFARB_20260410_PERPLEX_K9T3*
