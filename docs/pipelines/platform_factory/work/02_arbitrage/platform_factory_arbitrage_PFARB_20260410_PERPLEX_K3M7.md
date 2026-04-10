# Proposition d'Arbitrage — STAGE_02_FACTORY_ARBITRAGE

## arbitrage_run_id
`PFARB_20260410_PERPLEX_K3M7`

## Date
2026-04-10

## IA
PERPLEX (Perplexity / Claude Sonnet 4.6)

---

## Challenge reports considérés

| challenge_run_id | IA source |
|---|---|
| `PFCHAL_20260410_GPT54_Z4N8` | GPT-4 |
| `PFCHAL_20260410_PERPLEX_9KR4M` | Perplexity / Claude Sonnet 4.6 |
| `PFCHAL_20260410_PERPLX_8ZQA` | Perplexity |
| `PFCHAL_20260410_PERPLX_9KR3` | Perplexity |
| `PFCHAL_20260410_PERPLX_K7R2` | Perplexity |

Tous les challenge reports présents dans `work/01_challenge/` ont été lus intégralement avant rédaction.

---

## Résumé exécutif

La baseline Platform Factory V0.4 est acceptée comme fondation de gouvernance. Sa séparation prescriptif/constatif est solide, la non-duplication normative est bien tenue, et les principales lacunes sont honnêtement documentées. Elle n'est cependant pas encore capable de produire des preuves opératoires de conformité constitutionnelle.

Cinq zones de risque convergent dans les cinq challenge reports avec un niveau de consensus fort :

1. **Conformité constitutionnelle non probante** : `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` absent → tout signal `constitutional_invariants_checked: PASS` et tout tag `validation_status: validated` sont non auditables.
2. **Matrice de conformité absente** : `constitutional_conformance_matrix.yaml` est référencée comme obligatoire mais inexistante — blocker critique direct sur toutes les projections et sur le contrat minimal d'application.
3. **`bootstrap_contract` TBD obligatoire** : aucune application ne peut passer la validation complète du contrat minimal ; brèche d'inventivité dangereuse sur `INV_RUNTIME_FULLY_LOCAL`.
4. **Multi-IA opérationnellement non gouvernée** : `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` est auto-déclaré BLOCKER OPÉRATIONNEL mais n'est pas classé comme blocker formel avec exit condition.
5. **STAGE_04 non exécutable** : `validate_platform_factory_patchset.py` absent, pipeline bloqué à partir de STAGE_04.

Le présent arbitrage propose les décisions nécessaires pour permettre un patch propre, borné et cohérent.

---

## Synthèse des constats convergents

Les cinq challenge reports convergent sur les points suivants sans contradiction significative :

### Consensus fort (présent dans 5/5 reports)

- `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` absent = chaîne de conformité constitutionnelle non probante.
- `constitutional_conformance_matrix.yaml` absent = projection et application inauditables constitutionnellement.
- `PF_BLOCKER_BOOTSTRAP_CONTRACT_UNDEFINED` (sévérité high) = contrat minimal d'application incomplet.
- `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` = BLOCKER OPÉRATIONNEL non classifié formellement comme blocker.
- Séparation architecture/state, non-duplication normative et frontières de portée : solides.

### Consensus fort (présent dans 4/5 reports)

- `validate_platform_factory_patchset.py` absent → STAGE_04 bloqué silencieusement.
- `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` classée partial avec le wording "exécutable manuellement" : inexact ou trompeur pour les stages à script obligatoire.
- `usage_as_sole_context: blocked` déclaratif sans garde-fou technique.
- Outputs STAGE_01/02 non normés en schéma → interprétation libre par les IA aval.
- Promotion directe de `docs/cores/current/` hors STAGE_08 non outillée.

### Consensus modéré (présent dans 3/5 reports)

- `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` sans plan de résolution, sans date, sans porteur : trou de gouvernance.
- `PF_CAPABILITY_DERIVED_PROJECTION_RULE_DEFINED` (partial) : wording potentiellement trompeur — blocage structurel, pas progression en cours.
- La release `PLATFORM_FACTORY_RELEASE_2026_04_10_R01` est mentionnée dans le state mais son manifest n'est pas inclus dans le périmètre de lecture obligatoire du challenge.
- STAGE_01 dans `pipeline.md` référence le prompt métier partagé plutôt que le launch prompt d'exécution dédié.

### Constats différenciés (1–2 reports)

- `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` absent du contrat minimal (PERPLX_8ZQA uniquement, bien documenté).
- `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` absent du contrat minimal (PERPLX_8ZQA uniquement).
- Angle mort double-buffer pour les patches d'artefacts factory internes (PERPLEX_9KR4M uniquement).
- `declared_autonomy_regime_respected` sans invariant constitutionnel source (PERPLX_K7R2 uniquement).
- `version_fingerprint` sans mécanisme de détection de dérive canonique (PERPLX_K7R2 uniquement).
- Gate d'inéligibilité pour pipeline d'instanciation aval (PERPLX_9KR3 uniquement).
- `conformance_matrix_availability_status` dans le contrat de projection (PERPLX_9KR3 uniquement).

---

## Propositions d'arbitrage par thème

---

### Thème 1 — Chaîne de validation constitutionnelle (validator + matrice)

#### ARB-01 — Créer la `constitutional_conformance_matrix.yaml`

- **Élément concerné** : `constitutional_conformance_matrix_ref` dans l'architecture + signal `constitutional_invariants_checked` + champ `conformance_matrix_ref` dans le contrat de projection
- **Localisation principale** : `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` (à créer)
- **Sources** : tous les 5 challenge reports — consensus critique
- **Statut proposé** : **retained**
- **Gravité** : critique
- **Justification** : Le fichier est référencé comme obligatoire dans l'architecture (champ `conformance_matrix_ref` obligatoire par projection, signal `constitutional_invariants_checked` conditionné). Son absence rend toute projection et toute application produite constitutionnellement inauditables. Le blocker `PF_BLOCKER_CONFORMANCE_MATRIX_ABSENT` est reconnu high mais ne possède ni plan de résolution ni porteur. Ce trou de gouvernance doit être arbitré maintenant.
- **Lieu principal** : validator/tooling (création du fichier) + architecture (conserver la référence, ajouter un plan de résolution dans l'état)
- **Lieu secondaire** : state (enrichir le blocker avec exit_condition et target_date)
- **Dépendance** : précède l'implémentation du validator dédié
- **Consensus** : strong

#### ARB-02 — Élever l'absence de `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` au rang de blocker high

- **Élément concerné** : `capabilities_absent.PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` dans le state
- **Sources** : PFCHAL_20260410_PERPLX_9KR3, PFCHAL_20260410_PERPLX_8ZQA, PFCHAL_20260410_PERPLEX_9KR4M, PFCHAL_20260410_GPT54_Z4N8
- **Statut proposé** : **retained**
- **Gravité** : critique
- **Justification** : L'absence de validator a un impact direct sur la conformité constitutionnelle (signals non probants) et sur la validité de toute release d'application produite. Elle doit être traitée comme un blocker formel, pas comme une simple `capability_absent`. Exit condition proposée : implémentation des trois validators prioritaires — `derived_projection_conformance`, `minimum_contract_conformance`, `runtime_policy_conformance`.
- **Lieu principal** : state (reclassification en blocker + exit_condition)
- **Lieu secondaire** : validator/tooling (plan d'implémentation)
- **Consensus** : strong

#### ARB-03 — Interdire explicitement l'émission de `constitutional_invariants_checked: PASS` sans validator opérationnel

- **Élément concerné** : `minimum_observability_contract.constitutional_invariants_checked` dans l'architecture
- **Sources** : PFCHAL_20260410_PERPLEX_9KR4M (C2), PFCHAL_20260410_PERPLX_8ZQA (A1-3)
- **Statut proposé** : **retained**
- **Gravité** : critique
- **Justification** : En l'état, une application produite peut émettre `constitutional_invariants_checked: PASS` sans que le validator existe. La note dans l'architecture le documente mais ne l'interdit pas formellement. Il faut ajouter une contrainte explicite d'interdiction d'émission de ce signal à PASS tant que `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` est absent, sauf pour les vérifications statiques documentées comme protocole manuel minimal.
- **Lieu principal** : architecture
- **Consensus** : medium

---

### Thème 2 — Bootstrap contract

#### ARB-04 — Définir un scope minimal V0 du `bootstrap_contract` ou borner explicitement son absence

- **Élément concerné** : `runtime_entrypoint_contract.bootstrap_contract` dans l'architecture
- **Sources** : tous les 5 challenge reports — consensus élevé
- **Statut proposé** : **retained** (décision sur l'option à choisir déléguée au patch)
- **Gravité** : élevée
- **Justification** : Le champ `bootstrap_contract` est déclaré obligatoire (`required: true`) mais TBD. Deux options acceptables : (a) définir un scope minimal V0 (ex. "aucun appel réseau autorisé au bootstrap, aucun appel LLM, dépendances uniquement locales") sans finaliser la typologie complète ; (b) maintenir TBD mais ajouter une contrainte explicite d'interdiction d'appel réseau/LLM dans le bootstrap comme invariant architectural supplémentaire, ET marquer les axes de validation dépendants comme `DEFERRED_UNTIL_BOOTSTRAP_DEFINED`. L'option (b) est privilégiée si la définition de la typologie runtime n'est pas encore possible dans ce cycle.
- **Lieu principal** : architecture
- **Lieu secondaire** : state (mise à jour du blocker avec exit_condition)
- **Consensus** : strong

---

### Thème 3 — Projections dérivées

#### ARB-05 — Lever l'ambiguïté `usage_as_sole_context` : régime cible vs politique V0

- **Élément concerné** : tension dans l'architecture entre `execution_projection_contract.usage_as_sole_context: blocked` et `generated_projection_rules.minimum_requirements.each_projection_can_be_used_as_single_context_for_targeted_task`
- **Sources** : PFCHAL_20260410_GPT54_Z4N8 (R2), PFCHAL_20260410_PERPLX_8ZQA (A5-1)
- **Statut proposé** : **retained**
- **Gravité** : élevée
- **Justification** : La formulation crée une ambiguïté réelle entre le régime cible (design intent) et la politique V0 courante (blocked). Il faut distinguer textuellement les deux. La correction doit clarifier que `usage_as_sole_context: blocked` est la politique opérationnelle courante, et que la règle `each_projection_can_be_used_as_single_context` décrit le régime cible conditionné à la levée des blockers préalables.
- **Lieu principal** : architecture
- **Consensus** : medium

#### ARB-06 — Renforcer l'interdiction de `usage_as_sole_context: blocked` dans les launch prompts

- **Élément concerné** : politique déclarative sans garde-fou technique
- **Sources** : PFCHAL_20260410_PERPLX_8ZQA (C5), PFCHAL_20260410_PERPLEX_9KR4M (risque élevé), PFCHAL_20260410_GPT54_Z4N8
- **Statut proposé** : **retained**
- **Gravité** : élevée
- **Justification** : Ajouter dans chaque launch prompt de STAGE utilisant des projections une instruction explicite rappelant ce blocage. Envisager un header obligatoire dans tout fichier de projection indiquant `usage_as_sole_context: BLOCKED — politique V0 en vigueur`. Pas de garde-fou technique possible sans outillage, mais le garde-fou documentaire est immédiatement faisable.
- **Lieu principal** : pipeline (launch prompts)
- **Lieu secondaire** : architecture (header obligatoire dans les projections)
- **Consensus** : medium

#### ARB-07 — Documenter le signal d'indisponibilité de `constitutional_conformance_matrix.yaml` dans le contrat de projection

- **Élément concerné** : champ `conformance_matrix_ref` dans `execution_projection_contract.mandatory_fields_per_projection`
- **Sources** : PFCHAL_20260410_PERPLX_9KR3 (C5)
- **Statut proposé** : **retained**
- **Gravité** : modérée
- **Justification** : Une projection émise aujourd'hui pointe un fichier absent. L'IA réceptrice n'a aucun signal explicite d'indisponibilité dans la projection elle-même. Ajouter une note dans l'architecture imposant que lorsque `conformance_matrix_ref` pointe un fichier absent (blocker enregistré), la projection indique explicitement `conformance_matrix_status: unavailable`.
- **Lieu principal** : architecture
- **Consensus** : weak

---

### Thème 4 — Multi-IA

#### ARB-08 — Reclasser `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker formel

- **Élément concerné** : `known_gaps.PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` dans le state
- **Sources** : PFCHAL_20260410_PERPLX_9KR3 (C2), PFCHAL_20260410_PERPLX_8ZQA (C4), PFCHAL_20260410_PERPLEX_9KR4M (C6), PFCHAL_20260410_GPT54_Z4N8 (R4)
- **Statut proposé** : **retained**
- **Gravité** : élevée
- **Justification** : Le gap est auto-déclaré BLOCKER OPÉRATIONNEL dans sa description mais n'est pas dans la section `blockers`. Cette asymétrie masque son impact réel. Il faut le déplacer vers `blockers` avec sévérité medium-to-high, et définir une exit condition (spec du protocole multi-IA : décomposition, assemblage, résolution de conflit, granularité modulaire). Tant que ce blocker n'est pas levé, l'usage multi-IA réel doit être explicitement interdit dans les launch prompts.
- **Lieu principal** : state
- **Lieu secondaire** : architecture (clause d'interdiction d'usage multi-IA réel)
- **Consensus** : strong

---

### Thème 5 — Pipeline et implémentabilité

#### ARB-09 — Tracer le script STAGE_04 comme sous-condition de blocage dans le state

- **Élément concerné** : `validate_platform_factory_patchset.py` requis par STAGE_04 + `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` (absent)
- **Sources** : PFCHAL_20260410_PERPLEX_9KR4M (C3), PFCHAL_20260410_PERPLX_9KR3 (C4), PFCHAL_20260410_PERPLX_K7R2, PFCHAL_20260410_GPT54_Z4N8 (R6)
- **Statut proposé** : **retained**
- **Gravité** : élevée
- **Justification** : STAGE_04 est déclaré bloquant sur ce script. Son absence bloque tout le pipeline à partir de STAGE_04 (et donc STAGE_05 à STAGE_08, ce qui inclut la fermeture du blocker `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`). Ce blocage en cascade n'est pas visible dans le state. Il faut l'ajouter comme sous-condition dans `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` et définir un plan de résolution. En attendant, STAGE_04 doit définir explicitement un protocole de fallback V0 (validation manuelle structurée et documentée) acceptable comme dérogation temporaire.
- **Lieu principal** : state + pipeline
- **Consensus** : strong

#### ARB-10 — Corriger le wording de `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED`

- **Élément concerné** : `capabilities_partial.PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` — "exécutable manuellement"
- **Sources** : PFCHAL_20260410_PERPLEX_9KR4M, PFCHAL_20260410_PERPLX_8ZQA (A2-1), PFCHAL_20260410_PERPLX_K7R2 (C3), PFCHAL_20260410_PERPLX_9KR3 (Axe 6)
- **Statut proposé** : **retained**
- **Gravité** : modérée
- **Justification** : La formulation "exécutable manuellement" est inexacte pour les stages avec script obligatoire (notamment STAGE_04). Elle crée un faux sentiment de capacité opérationnelle. Corriger pour préciser que seuls les stages sans script obligatoire sont exécutables manuellement, et que STAGE_04 est bloqué.
- **Lieu principal** : state
- **Consensus** : strong

#### ARB-11 — Aligner `pipeline.md` STAGE_01 avec le launch prompt d'exécution réel

- **Élément concerné** : `pipeline.md` → STAGE_01_CHALLENGE.Prompt (pointe le prompt métier partagé, pas le launch prompt dédié)
- **Sources** : PFCHAL_20260410_PERPLX_8ZQA (A2-1, C6), PFCHAL_20260410_PERPLX_K7R2 (Axe 9)
- **Statut proposé** : **retained**
- **Gravité** : modérée
- **Justification** : Incohérence entre le prompt référencé dans `pipeline.md` (`docs/prompts/shared/Challenge_platform_factory.md`) et le vrai launch prompt d'exécution (`LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md`). Les deux niveaux sont distincts (cadre métier vs instruction d'exécution) mais non différenciés dans le pipeline. Mettre à jour `pipeline.md` pour référencer les deux, ou clarifier la relation entre eux.
- **Lieu principal** : pipeline
- **Consensus** : medium

#### ARB-12 — Corriger l'incohérence de convention de nommage des challenge reports dans `pipeline.md`

- **Élément concerné** : format `challenge_report_##.md` dans `pipeline.md` vs convention `PFCHAL_YYYYMMDD_AGENTTAG_RAND` dans le launch prompt
- **Sources** : PFCHAL_20260410_PERPLX_K7R2 (C6, Axe 9)
- **Statut proposé** : **retained**
- **Gravité** : modérée
- **Justification** : Le format `##` dans `pipeline.md` est obsolète par rapport au launch prompt. L'incohérence crée un risque de collision ou d'ambiguïté si le pipeline est lu sans le launch prompt. Aligner `pipeline.md` sur la convention `challenge_run_id` du launch prompt.
- **Lieu principal** : pipeline
- **Consensus** : medium

---

### Thème 6 — Gouvernance release/manifest

#### ARB-13 — Fermer explicitement la gouvernance manifest/promotion des artefacts `platform_factory`

- **Élément concerné** : `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` — artefacts dans `docs/cores/current/` hors manifest officiel
- **Sources** : tous les 5 challenge reports — consensus fort
- **Statut proposé** : **deferred** (exit condition liée à STAGE_08, déjà documentée, acceptable en V0)
- **Gravité** : élevée
- **Justification** : Ce blocker est déjà correctement documenté avec une exit condition (STAGE_08). Il n'exige pas de correction de contenu dans ce cycle. Cependant, il faut s'assurer que la dépendance en cascade vers le script STAGE_04 (ARB-09) est explicitée, car le chemin vers STAGE_08 est bloqué tant que STAGE_04 ne peut pas s'exécuter.
- **Lieu principal** : state (note de dépendance cascade)
- **Consensus** : strong

#### ARB-14 — Inclure la lecture du manifest release dans le périmètre de lecture obligatoire du challenge

- **Élément concerné** : `LAUNCH_PROMPT_STAGE_01_CHALLENGE_MULTI.md` → ordre de lecture obligatoire
- **Sources** : PFCHAL_20260410_PERPLX_8ZQA (C8), PFCHAL_20260410_PERPLX_9KR3 (Axe 8)
- **Statut proposé** : **retained**
- **Gravité** : modérée
- **Justification** : Le manifest release `PLATFORM_FACTORY_RELEASE_2026_04_10_R01/manifest.yaml` n'est pas inclus dans la liste de lecture obligatoire du challenge, ce qui laisse la traçabilité de la baseline partiellement aveugle. Il faut l'ajouter à l'ordre de lecture.
- **Lieu principal** : pipeline (launch prompt STAGE_01)
- **Consensus** : medium

---

### Thème 7 — Contrat minimal d'application — invariants constitutionnels manquants

#### ARB-15 — Ajouter `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` au contrat minimal

- **Élément concerné** : `minimum_validation_contract.minimum_axes`
- **Sources** : PFCHAL_20260410_PERPLX_8ZQA (C2, A1-1) — constat isolé mais solide
- **Statut proposé** : **retained**
- **Gravité** : élevée
- **Justification** : L'invariant constitutionnel `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` n'est pas couvert par les axes minimaux de validation. Une application produite pourrait satisfaire formellement le contrat minimal tout en violant cet invariant. Le constat est présent dans un seul report mais est bien argumenté constitutionnellement.
- **Lieu principal** : architecture
- **Consensus** : weak (constat isolé mais constitutionnellement fondé)

#### ARB-16 — Ajouter `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` au contrat minimal

- **Élément concerné** : `runtime_policy_conformance_definition.items_to_verify`
- **Sources** : PFCHAL_20260410_PERPLX_8ZQA (C3, A1-2) — constat isolé mais fondé
- **Statut proposé** : **retained**
- **Gravité** : élevée
- **Justification** : Invariant constitutionnel récent (`ARBITRAGE_2026_04_01`) non répercuté dans le contrat factory. Une application produite pourrait inférer des signaux de gouvernance localement via LLM.
- **Lieu principal** : architecture
- **Consensus** : weak (constat isolé, mais impact constitutionnel direct)

#### ARB-17 — Relier `declared_autonomy_regime_respected` à un invariant constitutionnel source

- **Élément concerné** : `runtime_policy_conformance_definition.items_to_verify.declared_autonomy_regime_respected`
- **Sources** : PFCHAL_20260410_PERPLX_K7R2 (C5) — constat isolé
- **Statut proposé** : **retained** avec clarification préalable
- **Gravité** : modérée
- **Justification** : L'item existe dans le contrat mais sans `invariant_ref` vers la Constitution. Il est non auditable constitutionnellement. Soit ajouter un `invariant_ref` explicite, soit supprimer l'item s'il ne correspond à aucun invariant constitutionnel source. La décision de fond (quel invariant source ?) requiert une clarification.
- **Lieu principal** : architecture
- **Pré-condition** : identifier l'invariant constitutionnel source applicable
- **Consensus** : weak

---

### Thème 8 — Sujets reportés

#### ARB-18 — Schémas détaillés du manifest, de la configuration et du packaging

- **Statut proposé** : **deferred**
- **Justification** : Incomplétudes V0 explicitement reconnues, sans risque immédiat de violation constitutionnelle. Bornées dans le state. Ne pas sur-corriger.
- **Consensus** : strong

#### ARB-19 — Définition du protocole multi-IA (décomposition, assemblage, résolution de conflit)

- **Statut proposé** : **deferred** (mais reclassification en blocker exigée : ARB-08)
- **Justification** : La définition du protocole elle-même est bien différée. En revanche, la reclassification en blocker formel (ARB-08) est retenue pour ce cycle.
- **Consensus** : strong

#### ARB-20 — Gate d'inéligibilité pour pipeline d'instanciation aval

- **Élément concerné** : frontière factory / pipeline d'instanciation — aucune condition préalable formelle pour démarrage du pipeline aval
- **Sources** : PFCHAL_20260410_PERPLX_9KR3 (C3)
- **Statut proposé** : **deferred** avec note
- **Gravité** : modérée
- **Justification** : La préoccupation est légitime mais le pipeline d'instanciation aval n'existe pas encore. Différer la définition de la gate d'inéligibilité à la création du pipeline aval. Ajouter une note dans l'architecture signalant que tout pipeline d'instanciation futur devra vérifier les blockers `high` de la factory avant démarrage.
- **Lieu principal** : architecture (note prospective)
- **Consensus** : weak

#### ARB-21 — Mécanisme de détection de dérive canonique pour les projections (`version_fingerprint`)

- **Élément concerné** : `version_fingerprint` sans mécanisme de comparaison
- **Sources** : PFCHAL_20260410_PERPLX_K7R2 (C4)
- **Statut proposé** : **deferred**
- **Gravité** : élevée (pour les projections futures) / V0-acceptable tant qu'aucune projection n'est produite
- **Justification** : Aucune projection n'existe en V0. Le risque est réel mais non actif. Différer à la création du premier cycle de projections dérivées.
- **Consensus** : medium

---

### Thème 9 — Sujets hors périmètre

#### ARB-22 — Angle mort double-buffer pour patches d'artefacts factory internes

- **Sources** : PFCHAL_20260410_PERPLEX_9KR4M — constat isolé
- **Statut proposé** : **out_of_scope** pour ce cycle
- **Justification** : La factory ne gère pas directement l'application de patches à elle-même via un double-buffer. Ce mécanisme relève du pipeline de patch (STAGE_05) et de la gouvernance de promotion (STAGE_08), qui disposent déjà d'un mécanisme de sandbox (`work/05_apply/`) avant promotion. Pas de correction de contenu canonique nécessaire.
- **Consensus** : weak (constat isolé)

#### ARB-23 — Frontière factory/instanciation non contrôlée activement

- **Sources** : PFCHAL_20260410_PERPLX_8ZQA (Axe 3, angle mort)
- **Statut proposé** : **out_of_scope** pour ce cycle (aucun pipeline d'instanciation existant)
- **Justification** : Sans pipeline d'instanciation existant, la frontière ne peut pas dériver de façon active. À surveiller lors de la création du premier pipeline d'instanciation domaine.
- **Consensus** : medium

---

## Points retenus

| ARB-ID | Sujet | Gravité | Lieu principal |
|---|---|---|---|
| ARB-01 | Créer `constitutional_conformance_matrix.yaml` | Critique | validator/tooling + state |
| ARB-02 | Élever absence validators en blocker high | Critique | state |
| ARB-03 | Interdire `constitutional_invariants_checked: PASS` sans validator | Critique | architecture |
| ARB-04 | Définir scope minimal V0 `bootstrap_contract` ou borner son absence | Élevée | architecture |
| ARB-05 | Lever ambiguïté `usage_as_sole_context` régime cible vs politique V0 | Élevée | architecture |
| ARB-06 | Renforcer interdiction `usage_as_sole_context` dans les launch prompts | Élevée | pipeline |
| ARB-07 | Signal indisponibilité `conformance_matrix` dans contrat projection | Modérée | architecture |
| ARB-08 | Reclasser `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker | Élevée | state |
| ARB-09 | Tracer script STAGE_04 comme sous-condition de blocage | Élevée | state + pipeline |
| ARB-10 | Corriger wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` | Modérée | state |
| ARB-11 | Aligner `pipeline.md` STAGE_01 avec launch prompt réel | Modérée | pipeline |
| ARB-12 | Corriger convention nommage challenge reports dans `pipeline.md` | Modérée | pipeline |
| ARB-14 | Inclure manifest release dans lecture obligatoire du challenge | Modérée | pipeline |
| ARB-15 | Ajouter `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` au contrat minimal | Élevée | architecture |
| ARB-16 | Ajouter `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` au contrat minimal | Élevée | architecture |
| ARB-17 | Relier `declared_autonomy_regime_respected` à invariant constitutionnel | Modérée | architecture |

---

## Points rejetés

Aucun finding des challenge reports n'est rejeté dans cette proposition. Tous les constats sont soit retenus, soit reportés, soit classés hors périmètre. La baseline V0.4 présente des lacunes réelles, non des faux positifs de challenge.

---

## Points différés

| ARB-ID | Sujet | Justification du report |
|---|---|---|
| ARB-13 | Fermeture manifest/promotion `platform_factory` | Exit condition liée à STAGE_08 déjà documentée ; dépendance cascade ARB-09 à noter |
| ARB-18 | Schémas détaillés manifest, configuration, packaging | Incomplétudes V0 normales, bornées |
| ARB-19 | Définition protocole multi-IA | Différé mais reclassification en blocker retenue (ARB-08) |
| ARB-20 | Gate d'inéligibilité pipeline d'instanciation aval | Pipeline aval inexistant |
| ARB-21 | Mécanisme détection dérive canonique (`version_fingerprint`) | Pas de projections en V0 |

---

## Points hors périmètre

| ARB-ID | Sujet | Justification |
|---|---|---|
| ARB-22 | Angle mort double-buffer patches factory internes | Couvert par sandbox STAGE_05 / STAGE_08 existant |
| ARB-23 | Frontière factory/instanciation non contrôlée | Aucun pipeline d'instanciation existant ; à surveiller |

---

## Points sans consensus ou nécessitant discussion finale

| Sujet | Nature du désaccord ou de l'ambiguïté |
|---|---|
| ARB-17 : `declared_autonomy_regime_respected` | Constat isolé. L'invariant source constitutionnel exact n'est pas encore identifié dans les challenge reports. Discussion finale nécessaire pour identifier ou éliminer le lien. |
| ARB-07 : signal d'indisponibilité dans le contrat de projection | Proposé par un seul report. Techniquement pertinent mais peut alourdir le contrat. À valider en consolidation humaine. |
| ARB-15 & ARB-16 : invariants constitutionnels manquants au contrat minimal | Proposés par un seul report (PERPLX_8ZQA). Bien fondés constitutionnellement, mais leur ajout au contrat minimal peut avoir un impact sur la complétude du cycle de validation. Discussion sur la séquence d'ajout recommandée. |

---

## Corrections à arbitrer avant patch

### Ordre de priorité recommandé

**Niveau 1 — Critiques (bloquent la probativité de toute release)**

1. ARB-01 : Créer la `constitutional_conformance_matrix.yaml` (hors patch YAML direct — nécessite un cycle dédié ou une action off-pipeline)
2. ARB-02 : Reclasser l'absence de `PF_CAPABILITY_FACTORY_VALIDATORS_IMPLEMENTED` en blocker high dans `platform_factory_state.yaml`
3. ARB-03 : Ajouter contrainte explicite d'interdiction `constitutional_invariants_checked: PASS` sans validator dans `platform_factory_architecture.yaml`

**Niveau 2 — Élevés (bloquent la fermeture propre du contrat minimal ou du multi-IA)**

4. ARB-04 : Traiter `bootstrap_contract` TBD dans `platform_factory_architecture.yaml`
5. ARB-08 : Reclasser `PF_GAP_PARALLEL_AI_PROTOCOL_UNDEFINED` en blocker dans `platform_factory_state.yaml`
6. ARB-09 : Tracer le script STAGE_04 comme sous-condition dans `platform_factory_state.yaml` + définir fallback V0 dans `pipeline.md`
7. ARB-15 : Ajouter `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` dans `platform_factory_architecture.yaml`
8. ARB-16 : Ajouter `INV_RUNTIME_QUALIFICATION_SIGNALS_MUST_BE_EXPLICIT_OR_OFFSESSION` dans `platform_factory_architecture.yaml`
9. ARB-05 : Lever l'ambiguïté `usage_as_sole_context` dans `platform_factory_architecture.yaml`
10. ARB-06 : Renforcer interdiction dans les launch prompts (`pipeline.md` ou launch prompts dédiés)

**Niveau 3 — Modérés (amélioration de la cohérence interne et de l'exploitabilité)**

11. ARB-10 : Corriger wording `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` dans `platform_factory_state.yaml`
12. ARB-11 : Aligner STAGE_01 dans `pipeline.md` avec launch prompt réel
13. ARB-12 : Corriger convention nommage dans `pipeline.md`
14. ARB-14 : Ajouter manifest release dans lecture obligatoire du challenge (launch prompt STAGE_01)
15. ARB-07 : Ajouter signal d'indisponibilité matrice dans `platform_factory_architecture.yaml` (après discussion finale ARB-07)
16. ARB-17 : Relier `declared_autonomy_regime_respected` à invariant source (après discussion finale ARB-17)

---

### Répartition par lieu de correction

| Lieu | ARB-IDs concernés |
|---|---|
| `platform_factory_architecture.yaml` | ARB-03, ARB-04, ARB-05, ARB-07, ARB-15, ARB-16, ARB-17, ARB-20 (note) |
| `platform_factory_state.yaml` | ARB-01 (note + plan), ARB-02, ARB-08, ARB-09, ARB-10, ARB-13 (note dépendance) |
| `pipeline.md` et/ou launch prompts | ARB-06, ARB-09 (fallback V0), ARB-11, ARB-12, ARB-14 |
| `docs/cores/platform_factory/constitutional_conformance_matrix.yaml` (à créer) | ARB-01 |
| validator/tooling | ARB-01, ARB-02 (plan) |

---

## Résultat terminal

1. **arbitrage_run_id** : `PFARB_20260410_PERPLEX_K3M7`
2. **Fichier écrit** : `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage_PFARB_20260410_PERPLEX_K3M7.md`
3. **Résumé ultra-court** : 5 challenge reports consolidés. Consensus critique sur 3 points (validator absent, conformance matrix absente, constitutional_invariants_checked non probant). 16 points retenus, 5 différés, 2 hors périmètre. Corrections prioritaires sur `platform_factory_architecture.yaml`, `platform_factory_state.yaml` et `pipeline.md`. Aucun constat rejeté. Trois sujets en discussion finale (ARB-07, ARB-15/16, ARB-17).
