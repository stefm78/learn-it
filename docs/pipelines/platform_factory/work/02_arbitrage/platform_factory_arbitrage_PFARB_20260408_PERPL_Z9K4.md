# ARBITRAGE PROPOSAL — STAGE_02_FACTORY_ARBITRAGE — Platform Factory

## arbitrage_run_id

`PFARB_20260408_PERPL_Z9K4`

## Date

2026-04-08

## Challenge reports considérés

| ID | Auteur | Taille | Référentiel/LINK chargés |
|---|---|---|---|
| `PFCHAL_20260408_GPT54_Q7M2` | GPT-4o | ~29 Ko | Oui |
| `PFCHAL_20260408_PERPLEX_K7M3` | Perplexity | ~23 Ko | Non (signalé) |
| `PFCHAL_20260408_PERPLX_K7M3` | Perplexity/Claude | ~29 Ko | Non (signalé) |
| `PFCHAL_20260408_PERPL_X7T2` | Perplexity | ~38 Ko | Oui |
| `PFCHAL_20260408_PERPX_7KQ2` | Perplexity | ~16 Ko | Oui |

**Note sur la couverture :** Deux runs (PERPLEX_K7M3, PERPLX_K7M3) n'ont pas chargé Référentiel.yaml et link.yaml. Les findings touchant les seuils délégués (INV_REFERENTIEL_VALIDITY_REQUIRED) et la résolution inter-Core (LINK) sont couverts par les 3 autres runs. L'arbitrage peut donc traiter tous les axes sans lacune structurelle.

---

## Résumé d'arbitrage

La convergence des 5 challenge reports est **forte et cohérente**. Les mêmes quatre zones de risque sont identifiées dans tous les rapports, avec des formulations et des niveaux de détail variables mais sans contradiction structurelle entre eux. L'arbitrage peut être rendu sur la quasi-totalité des findings sans clarification supplémentaire.

Les quatre thèmes de correction majeurs sont :

1. **Invariants constitutionnels runtime non traçables dans le contrat minimal d'application produite** — correction à retenir maintenant, dans l'architecture.
2. **Mécanisme de projections dérivées déclaré mais non instrumenté, avec emplacement TBD** — correction à retenir maintenant, dans l'architecture et en attente de décision de localisation.
3. **Gouvernance release/manifest hybride sans procédure de fermeture** — correction à retenir maintenant, dans le pipeline et la gouvernance de release.
4. **Multi-IA : exigences posées, protocole d'assemblage absent** — à différer V1 mais avec condition de blocage formalisée.

L'ensemble des manques V0 (schémas fins, outillage, pipeline non entièrement matérialisé) reste acceptable et ne doit pas être surchargé par ce patch.

---

## Findings consolidés

### FC-01 — Contrat minimal d'application produite ne couvre pas les invariants constitutionnels runtime

**Sources :** tous les 5 rapports (GPT54-P1, PERPLEX-C01, PERPLX-C01, PERPL_X7T2-1.1, PERPX-2)

**Formulations convergentes :**
- Absence d'axe de validation couvrant : runtime 100 % local, absence d'appel réseau temps réel, absence de génération de contenu runtime, absence de feedback runtime hors templates, validation locale déterministe des patchs, artefacts de patch précomputés hors session.
- Le contrat minimal actuel couvre `structure`, `minimum_contract_conformance`, `traceability`, `packaging`, `structure_and_state_alignment` — sans aucun axe constitutionnel runtime.
- Une application peut passer le contrat minimal et violer silencieusement `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_NO_RUNTIME_FEEDBACK_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION`.

**Formulation non consensuelle (à noter) :** GPT54 propose une «matrice de correspondance invariant → preuve attendue → artefact porteur → validator attendu». Les autres rapports se limitent à un axe additionnel `constitutional_runtime_conformance` ou `runtime_policy_conformance`. Ces deux formulations sont **compatibles** : la matrice peut être une implémentation de cet axe, mais la décision sur le format exact relève du patch.

**Verdict de fusion :** Finding confirmé, formulation unifiée possible.

---

### FC-02 — Mécanisme de projections dérivées non instrumenté et emplacement TBD

**Sources :** tous les 5 rapports

**Points convergents :**
- Le mécanisme `validated_derived_execution_projections` est correctement défini en principe (invariants, règle d'usage).
- Mais absence de : validateur, protocole de validation, protocole de régénération, emplacement de stockage défini.
- L'emplacement `TBD` dans `generated_projection_rules.emplacement_policy` est identifié comme bloquant central par tous les rapports.
- L'usage d'une projection non validée comme seul contexte IA est jugé prématurément activable et dangereux en l'état.
- Risque de dépôt dans `docs/cores/current/` si l'emplacement reste TBD (confusion avec canonique primaire).

**Nuance entre rapports :** PERPLEX-K7M3 propose `docs/cores/platform_factory/projections/` comme emplacement. PERPLX-K7M3 propose un gate d'activation formelle (Option A) ou une déclaration explicite de non-garantie dans chaque projection (Option B). Les autres rapports ne tranchent pas. Ces propositions sont **des options d'implémentation**, pas des divergences de fond.

**Verdict de fusion :** Finding confirmé. La décision d'emplacement est **pré-condition de patch** non encore tranchée par les rapports — doit être arbitrée ici.

---

### FC-03 — Gouvernance release/manifest hybride

**Sources :** tous les 5 rapports

**Points convergents :**
- Artefacts dans `docs/cores/current/` avec statut `RELEASE_CANDIDATE` mais hors manifest officiel courant.
- `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` reconnu dans le state mais sans procédure de fermeture dans le pipeline.
- Risque : IA ou opérateur traitant ces artefacts comme officiellement promus.
- Scénario D (PERPL_X7T2), SA-03 (PERPLEX), Scénario 4 (PERPLX, PERPX) tous activent ce même risque.

**Désaccord partiel :** GPT54 note une contradiction entre le vocabulaire «released baseline» du pipeline.md et le statut «RELEASE_CANDIDATE» des artefacts, et propose de les aligner. PERPLEX propose un déplacement physique vers `docs/cores/platform_factory/` ou un marqueur manifest. PERPLX propose un «signal de gouvernance externe au metadata» (fichier de statut, registry). Les autres rapports ne proposent pas de solution de déplacement physique.

**Verdict de fusion :** Finding confirmé. La solution exacte (alignement de vocabulaire vs déplacement physique vs marqueur manifest vs signal externe) constitue le seul point non consensuel. Doit être arbitré.

---

### FC-04 — Multi-IA : exigences posées, protocoles absents

**Sources :** tous les 5 rapports

**Points convergents :**
- Les 5 exigences minimales (`bounded_scopes`, `stable_identifiers`, `explicit_dependencies`, `clear_assembly_points`, `homogeneous_reports`) sont listées mais non instrumentées.
- Trois absences critiques pour un travail parallèle réel : `decomposition_protocol`, `ai_output_assembly_protocol`, `conflict_resolution_protocol`.
- La `module_granularity_convention` est dans `deferred_challenges` sans condition de déclenchement.
- Les scénarios multi-IA de collision (Scénario C - PERPL_X7T2, SA-03 - PERPLEX, Scénario 3 - PERPLX, Scénario 3 - PERPX) se recouvrent.

**Point de convergence fort :** Tous les rapports s'accordent pour dire que c'est un finding important mais **différable** en tant que protocole complet pour V1, **à condition** de formaliser une condition de blocage explicite sur l'usage multi-IA en production.

**Verdict de fusion :** Finding confirmé. Report V1 acceptable avec condition formalisée.

---

### FC-05 — Maturité partiellement surdéclarée dans `capabilities_present`

**Sources :** PERPL_X7T2, PERPLX_K7M3, GPT54 (modéré), PERPLEX_K7M3 (faible)

**Points convergents :**
- Cinq capacités listées comme `present` sont de nature déclarative/intentionnelle, non instrumentées.
- Le `PF_EVIDENCE_ARCHITECTURE_V0` pointe vers lui-même (auto-référence circulaire).
- `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` listée comme `present` alors que `PF_CAPABILITY_FACTORY_PIPELINE_FILES_COMPLETE` est `absent`.

**Note :** Gravité modérée, pas de contradiction avec le reste du state (qui reconnaît les limites). Finding à corriger dans le state mais sans urgence critique.

**Verdict de fusion :** Finding confirmé (modéré). Correction à retenir dans le state.

---

### FC-06 — Statut RELEASE_CANDIDATE sémantiquement trompeur

**Sources :** PERPLEX_K7M3 (C-05), PERPLX_K7M3 (Axe 6), GPT54 (Problème 3), PERPX_7KQ2 (Axe 2)

**Points convergents :**
- Le statut `RELEASE_CANDIDATE` est cohérent avec la posture de baseline challenged, mais peut induire en erreur une IA lisant ce champ isolément.
- La maturité réelle est V0 conceptuelle, non V0 instrumentée.

**Divergence de formulation :** PERPLEX propose `RELEASE_CANDIDATE_V0_CONCEPTUAL_ONLY`. PERPLX propose un champ `maturity_qualifier: v0_baseline`. GPT54 propose d'aligner sur `baseline_under_challenge`. Ces options sont toutes valides et mutuellement exclusives.

**Verdict de fusion :** Finding confirmé (faible à modéré). À corriger mais pas bloquant. Décision de wording à arbitrer.

---

### FC-07 — PF_CHAIN_05 et frontière factory/instanciation insuffisamment fermée

**Sources :** PERPL_X7T2 (Axe 3), PERPLX_K7M3 (C-04, Axe 3), GPT54 (Problème 5)

**Points convergents :**
- `PF_CHAIN_05_INSTANTIATE_DOMAIN_SPECIFIC_PARTS` est dans la `transformation_chain` factory alors qu'elle délègue à un pipeline aval non encore spécifié.
- La frontière est bien déclarée en intention mais sans mécanisme de détection de franchissement.

**Note :** Présent dans 3 rapports sur 5. Trouvaille cohérente mais moins universelle que FC-01 à FC-04.

**Verdict de fusion :** Finding confirmé (modéré). Correction à arbitrer.

---

### FC-08 — Double-buffer pour transformations factory non précisé

**Sources :** PERPL_X7T2 (Point 1.3) uniquement

**Verdict de fusion :** Finding isolé. À retenir pour suivi mais pas prioriser en patch.

---

### FC-09 — Fingerprints des artefacts factory eux-mêmes absents

**Sources :** PERPL_X7T2 (Point 8.2) uniquement

**Verdict de fusion :** Finding isolé, cohérence-intégrité. À retenir pour suivi.

---

### FC-10 — `canonical_dependency_contract` requis mais non schématisé

**Sources :** PERPL_X7T2 (Point 4.1), GPT54 (Problème 6 implicitement)

**Verdict de fusion :** Finding partiellement convergent. À retenir comme correction modérée.

---

### FC-11 — `runtime_entrypoint_type` non typé

**Sources :** PERPLEX_K7M3, PERPLX_K7M3 (Axe 4), PERPL_X7T2 (Point 4.2)

**Verdict de fusion :** Finding convergent (3 rapports). Correction modérée à retenir.

---

## Décisions immédiates

---

### DECISION ARB-01

**Sujet :** Axe de validation constitutionnelle runtime absent du contrat minimal d'application produite

**Source(s) :** FC-01 — tous les 5 rapports

**Décision : `retained_now`**

**Lieu principal de traitement :** architecture

**Lieu(x) secondaire(s) :** state (mise à jour `capabilities_partial` → progression), validator/tooling (à prévoir mais non bloquant pour ce patch)

**Priorité :** Critique

**Justification :** C'est le seul finding qui crée un risque de violation constitutionnelle silencieuse sur une application produite valide en apparence. Les 5 rapports l'identifient sans désaccord. Il touche directement `INV_RUNTIME_FULLY_LOCAL`, `INV_NO_RUNTIME_CONTENT_GENERATION`, `INV_PATCH_ARTIFACTS_MUST_BE_PRECOMPUTED_OFF_SESSION` — tous invariants de premier rang de la Constitution. Ne pas corriger maintenant revient à maintenir une factory qui peut certifier des applications non constitutionnellement conformes.

**Impact si non traité :** Release possible d'applications violant des invariants constitutionnels critiques sans détection.

**Correction à effectuer dans le patch :**
- Ajouter un axe `constitutional_runtime_conformance` (ou équivalent) dans `produced_application_minimum_contract.minimum_validation_contract.minimum_axes`.
- Cet axe doit couvrir au minimum : runtime 100 % local, absence d'appel réseau runtime, absence de génération de contenu runtime, absence de génération de feedback runtime hors templates préexistants, validation locale déterministe des patchs, artefacts de patch précomputés hors session.
- Ajouter également un signal correspondant dans `minimum_observability_contract.minimum_signals` (ex. : `constitutional_runtime_compliance_status`).
- **Ne pas** créer une matrice complète invariant → validateur dans ce patch (appartient à un cycle V1) ; ajouter uniquement l'axe et le signal minimaux.

**Pré-condition :** Aucune — faisable directement.

**Note de séquencement :** À traiter en premier dans le patch, car il conditionne la crédibilité de toutes les autres corrections.

---

### DECISION ARB-02

**Sujet :** Mécanisme de projections dérivées non instrumenté + emplacement TBD

**Source(s) :** FC-02 — tous les 5 rapports

**Décision : `retained_now` (partiellement conditionnel — voir pré-condition)**

**Lieu principal de traitement :** architecture

**Lieu(x) secondaire(s) :** state (mise à jour `emplacement_policy`), pipeline (condition d'usage formalisée), validator/tooling (hors scope de ce patch)

**Priorité :** Élevée

**Justification :** L'emplacement TBD des projections dérivées est un bloquant central identifié par tous les rapports. Il conditionne directement la séparation canonique/projections, le travail multi-IA, et la sécurité d'usage des projections comme seul contexte IA. La décision de localisation **peut être prise maintenant** ; le tooling n'est pas nécessaire dans ce patch.

**Impact si non traité :** Risque de dépôt de projections dans `docs/cores/current/`, confusion d'autorité, impossibilité d'auditer les projections utilisées.

**Correction à effectuer dans le patch :**

**(a) Décision d'emplacement :** Décider et inscrire dans `generated_projection_rules.emplacement_policy` :
- Emplacement retenu : `docs/pipelines/platform_factory/projections/` (zone de travail pipeline) pour les projections en cours de validation ; `docs/cores/projections/` (zone stable) pour les projections officiellement validées et promues.
- Interdire explicitement le dépôt de projections dans `docs/cores/current/`.
- Définir la convention de nommage minimale (ex. : `proj_<scope_id>_<version>_<status>.yaml`).

**(b) Condition d'usage comme seul contexte IA :** Ajouter dans `execution_projection_contract.rule_of_use` une condition préalable explicite : l'usage d'une projection comme seul artefact fourni à une IA est interdit tant que les trois conditions suivantes ne sont pas réunies :
- emplacement de stockage défini et respecté ;
- protocole de validation minimal défini (même sans outillage complet) ;
- projection marquée `validation_status: validated` dans son metadata.

**(c) Protocole de validation minimal :** Ajouter dans `generated_projection_rules` un bloc `minimum_validation_protocol` décrivant les étapes manuelles minimales acceptables jusqu'à ce qu'un validateur outillé soit disponible.

**Pré-condition :** La décision de localisation doit être prise par l'opérateur **avant** le patch. Options :
- Option 1 : `docs/pipelines/platform_factory/projections/` (work) + `docs/cores/projections/` (stable) — séparation claire
- Option 2 : `docs/projections/` unique avec sous-dossiers `work/` et `validated/`
- Option 3 : `docs/cores/platform_factory/projections/` — intégration plus forte sous cores mais avec sous-dossier factory

**Note de séquencement :** Dépend de la décision humaine sur l'emplacement. Le patch architecture peut être préparé sur les points (b) et (c) sans attendre cette décision, mais ne peut pas être finalisé sur (a) sans elle.

---

### DECISION ARB-03

**Sujet :** Gouvernance release/manifest hybride — artefacts dans `current/` mais hors manifest officiel, sans procédure de fermeture

**Source(s) :** FC-03 — tous les 5 rapports

**Décision : `retained_now` (sur le fond) + `clarification_required` (sur la solution exacte)**

**Lieu principal de traitement :** pipeline + manifest/release governance

**Lieu(x) secondaire(s) :** state (mise à jour de `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION`), architecture (vocabulaire de statut)

**Priorité :** Élevée

**Justification :** Le finding est confirmé par tous les rapports. La présence de ces artefacts dans `docs/cores/current/` sans intégration au manifest officiel est un trou de gouvernance réel qui peut induire confusion d'autorité et promotion implicite non gouvernée. La correction de fond est nécessaire maintenant. Mais la solution exacte (déplacement physique vs marqueur manifest vs signal externe) crée un point non consensuel entre rapports qui nécessite une décision humaine.

**Impact si non traité :** Adoption non gouvernée de la baseline, traçabilité rompue après une correction, confusion d'autorité pour tout outil ou IA lisant `docs/cores/current/`.

**Correction minimum à effectuer dans le patch (indépendante de la solution finale) :**
- Dans `platform_factory_state.yaml` : transformer `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` de simple blocker reconnu en **condition de blocage explicite** avec une liste de conditions de fermeture définies.
- Dans le `pipeline.md` STAGE_08_FACTORY_PROMOTE_CURRENT : formaliser explicitement la procédure de mise à jour du manifest (ou de création d'un manifest platform_factory dédié) comme étape obligatoire de la promotion.
- Dans les artefacts : ajouter un champ `integration_status: out_of_official_manifest` dans le metadata, distinct du champ `status`.

**Clarification requise avant patch complet :**
- **Question à trancher par l'opérateur :** La baseline platform_factory doit-elle (a) rester dans `docs/cores/current/` avec un manifest dédié étendu, (b) être déplacée vers `docs/cores/platform_factory/`, ou (c) rester en `current` avec un registry de factory dédié ?
- Cette décision conditionne le lieu de la correction de gouvernance permanente mais ne bloque pas les corrections de pipeline et de state ci-dessus.

**Note de séquencement :** Les corrections de state et de pipeline peuvent être effectuées sans attendre la décision architecturale de localisation.

---

### DECISION ARB-04

**Sujet :** Maturité surdéclarée dans `capabilities_present` + auto-référence circulaire dans evidence

**Source(s) :** FC-05 — PERPL_X7T2, PERPLX_K7M3, GPT54

**Décision : `retained_now`**

**Lieu principal de traitement :** state

**Lieu(x) secondaire(s) :** aucun

**Priorité :** Modérée

**Justification :** Le state est l'artefact constatif ; sa précision est un prérequis pour que les IA l'utilisent correctement. Une auto-référence circulaire dans l'evidence et une surestimation de la maturité opérationnelle créent un biais de confiance. Ce n'est pas critique mais c'est corrigible dans ce patch sans coût élevé.

**Correction à effectuer :**
- Introduire un attribut `evidence_level` sur chaque capacité `present` : `declared_only` | `defined` | `operational`.
- Requalifier les capacités `present` qui sont purement déclaratives en `declared_only`.
- Retirer ou qualifier `PF_EVIDENCE_ARCHITECTURE_V0` comme preuve auto-référentielle en le marquant `self_referential: true` avec note explicite.
- Séparer `PF_CAPABILITY_FACTORY_PIPELINE_INTENT_DEFINED` (intent) de la matérialisation réelle des fichiers pipeline.

---

### DECISION ARB-05

**Sujet :** Statut RELEASE_CANDIDATE sémantiquement trompeur pour une V0 conceptuelle

**Source(s) :** FC-06 — PERPLEX, PERPLX, GPT54, PERPX

**Décision : `retained_now` (correction légère)**

**Lieu principal de traitement :** architecture + state

**Lieu(x) secondaire(s) :** aucun

**Priorité :** Faible à modérée

**Justification :** Le risque de sur-confiance est réel mais limité. La correction est simple et peu risquée. Valeur ajoutée immédiate pour tout outil ou IA qui lit ce champ.

**Décision de wording :** Ajouter un champ `maturity_qualifier` dans le metadata de chaque artefact, avec la valeur `v0_conceptual_baseline`. Ne pas modifier le champ `status` (RELEASE_CANDIDATE) pour préserver la cohérence avec le cycle pipeline existant.

**Correction à effectuer :** Ajouter `maturity_qualifier: v0_conceptual_baseline` dans `metadata` des deux artefacts.

---

### DECISION ARB-06

**Sujet :** `canonical_dependency_contract` requis mais non schématisé

**Source(s) :** FC-10 — PERPL_X7T2, GPT54

**Décision : `retained_now`**

**Lieu principal de traitement :** architecture

**Priorité :** Élevée

**Justification :** Un contrat `required: true` mais sans champs minimaux est non auditable. Le schéma minimal peut être défini sans attendre un schéma complet.

**Correction à effectuer :** Définir les champs minimaux obligatoires du `canonical_dependency_contract` (au minimum : `constitution_version`, `referentiel_version`, `link_version`, `pinning_mode`).

---

### DECISION ARB-07

**Sujet :** `runtime_entrypoint_type` non typé

**Source(s) :** FC-11 — PERPLEX, PERPLX, PERPL_X7T2

**Décision : `retained_now` (correction partielle)**

**Lieu principal de traitement :** architecture

**Priorité :** Modérée

**Justification :** L'obligation est présente mais non auditable sans liste de types admissibles. Une liste provisoire non exhaustive peut être fournie sans bloquer le cycle.

**Correction à effectuer :** Ajouter dans `runtime_entrypoint_contract` une liste provisoire `known_entrypoint_types` (non exhaustive, extensible) avec note explicite de statut V0.

---

### DECISION ARB-08

**Sujet :** PF_CHAIN_05 et frontière factory/instanciation insuffisamment fermée

**Source(s) :** FC-07 — PERPL_X7T2, PERPLX_K7M3, GPT54

**Décision : `deferred` (avec note)**

**Lieu principal de traitement :** architecture (cycle suivant)

**Priorité :** Modérée

**Justification :** La frontière est bien posée en intention. Redéfinir PF_CHAIN_05 comme «point de délégation» est une amélioration de clarté, non un trou normatif immédiat. Différé V1 acceptable.

**Condition de déclenchement :** À traiter au début du pipeline d'instanciation domaine, avant que la première instanciation commence.

---

### DECISION ARB-09

**Sujet :** Multi-IA — protocole d'assemblage absent

**Source(s) :** FC-04 — tous les 5 rapports

**Décision : `deferred` (V1) avec condition de blocage**

**Lieu principal de traitement :** architecture + pipeline (cycle V1)

**Priorité :** Modérée (V0) / Élevée (si usage multi-IA activé)

**Justification :** Différer le protocole complet est raisonnable en V0. Mais la condition de blocage doit être formalisée maintenant pour éviter un usage multi-IA non gouverné.

**Correction à effectuer dans ce patch :** Ajouter dans `multi_ia_parallel_readiness` une condition de blocage explicite : «L'usage réel multi-IA en parallèle sur les projections dérivées ou sur la chaîne de transformation est interdit tant que `assembly_protocol_between_ai_outputs`, `module_granularity_convention` et `conflict_resolution_protocol` ne sont pas définis.» Enregistrer dans le state comme `PF_GAP_MULTI_IA_PROTOCOL_FORMALLY_BLOCKED`.

---

### DECISION ARB-10

**Sujet :** Double-buffer pour transformations factory non précisé

**Source(s) :** FC-08 — PERPL_X7T2 uniquement

**Décision : `clarification_required`**

**Justification :** Finding isolé sur un sujet constitutionnellement important. Avant de patcher, clarifier si le `CONSTRAINT_REFERENTIEL_DOUBLE_BUFFER_REQUIRED_FOR_PATCH` s'applique aux transformations internes factory ou seulement aux applications produites. Cette clarification conditionne le lieu et le contenu du patch.

**Clarification à apporter :** L'opérateur doit trancher : (a) la règle s'applique aux transformations internes factory → correction dans `build_and_packaging_rules` ; (b) la règle ne s'applique qu'aux applications produites → clarification dans `build_and_packaging_rules` que c'est une exigence du contrat minimal, pas une règle de gouvernance interne factory.

---

### DECISION ARB-11

**Sujet :** Fingerprints des artefacts factory eux-mêmes absents

**Source(s) :** FC-09 — PERPL_X7T2 uniquement

**Décision : `deferred`**

**Justification :** Finding pertinent mais isolé, de gravité modérée. Différé V1, à traiter lors du premier cycle release complet.

---

## Clarifications requises avant patch complet

| ID | Question | Impact |
|---|---|---|
| CLR-01 | Emplacement de stockage des projections dérivées (voir ARB-02 options 1/2/3) | Conditionne la finalisation du patch architecture sur `emplacement_policy` |
| CLR-02 | Solution de gouvernance release (rester dans `current` + manifest étendu vs déplacement physique vs registry dédié) (voir ARB-03) | Conditionne la correction permanente de gouvernance ; ne bloque pas les corrections pipeline/state |
| CLR-03 | Périmètre du double-buffer constitutionnel (transformations internes factory vs contrat minimal application produite) (voir ARB-10) | Conditionne le lieu et le contenu du patch sur `build_and_packaging_rules` |

---

## Reports assumés

| ID | Sujet | Condition de déclenchement |
|---|---|---|
| ARB-08 | PF_CHAIN_05 redéfini comme point de délégation | Avant première instanciation domaine |
| ARB-09 (complet) | Protocole d'assemblage multi-IA | Avant tout usage multi-IA en production |
| ARB-11 | Fingerprints des artefacts factory | Premier cycle release complet |

---

## Points hors périmètre

- Schémas YAML fins du manifest d'application produite, de la configuration, du packaging : manques V0 normaux, hors scope de ce patch.
- Outillage des validators (`derived_projection_conformance`, `minimum_contract_conformance`, `runtime_policy_conformance`) : recognus comme priorité de tooling, hors scope de ce patch.
- Pipeline d'instanciation domaine : frontière correctement posée, hors scope factory.
- Granularité modulaire optimale multi-IA : différée, hors scope V0.

---

## Points sans consensus ou nécessitant discussion finale

| ID | Point | Options en présence |
|---|---|---|
| NC-01 | Emplacement de stockage des projections dérivées | Option 1 (work + stable séparés) / Option 2 (docs/projections/ unique) / Option 3 (docs/cores/platform_factory/) |
| NC-02 | Solution de gouvernance release permanente | Déplacement physique / manifest dédié / registry externe / simple marqueur metadata |
| NC-03 | Wording final de l'axe constitutionnel runtime | Axe simple `constitutional_runtime_conformance` / matrice invariant→preuve→validator (GPT54) |
| NC-04 | Périmètre double-buffer (ARB-10) | Transformation interne factory / contrat minimal application uniquement |

---

## Répartition par lieu de correction

### Architecture (`platform_factory_architecture.yaml`)

- ARB-01 : Ajouter axe `constitutional_runtime_conformance` + signal observabilité
- ARB-02a : Inscrire décision d'emplacement projections (après CLR-01)
- ARB-02b : Ajouter condition d'usage projections comme seul contexte IA
- ARB-02c : Ajouter `minimum_validation_protocol` pour projections
- ARB-06 : Définir champs minimaux de `canonical_dependency_contract`
- ARB-07 : Ajouter liste provisoire `known_entrypoint_types`
- ARB-09 : Ajouter condition de blocage multi-IA dans `multi_ia_parallel_readiness`
- ARB-05 : Ajouter `maturity_qualifier: v0_conceptual_baseline` dans metadata

### State (`platform_factory_state.yaml`)

- ARB-04 : Introduire `evidence_level` sur `capabilities_present` + requalifier auto-référence
- ARB-03 : Renforcer `PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION` en condition de blocage formelle
- ARB-03 : Ajouter `integration_status: out_of_official_manifest` dans metadata
- ARB-05 : Ajouter `maturity_qualifier: v0_conceptual_baseline`
- ARB-09 : Enregistrer `PF_GAP_MULTI_IA_PROTOCOL_FORMALLY_BLOCKED`

### Pipeline (`pipeline.md`)

- ARB-03 : Formaliser étape de mise à jour manifest dans STAGE_08

### Manifest/Release governance

- ARB-03 (partiel — après CLR-02) : Décision de gouvernance permanente

### Validator/Tooling

- ARB-01 (secondaire), ARB-02 (secondaire) : Priorités de tooling hors scope patch mais à planifier

---

## Séquencement recommandé

1. **Clarifications humaines préalables :** CLR-01 (emplacement projections) + CLR-03 (double-buffer périmètre) — peuvent être résolues en parallèle.
2. **Patch architecture :** ARB-01 + ARB-02b + ARB-02c + ARB-06 + ARB-07 + ARB-09 (condition blocage) + ARB-05 — indépendant de CLR-01 pour les points (b) et (c).
3. **Finalisation patch architecture :** ARB-02a (emplacement) — après CLR-01.
4. **Patch state :** ARB-04 + ARB-03 (state) + ARB-05 + ARB-09 (state) — peut commencer en parallèle du patch architecture.
5. **Patch pipeline :** ARB-03 (pipeline) — peut commencer en parallèle.
6. **Correction double-buffer :** ARB-10 — après CLR-03.
7. **Décision gouvernance permanente :** CLR-02 → suit.

---

## Priorités de patch

| Priorité | Decision ID | Sujet | Lieu |
|---|---|---|---|
| Critique | ARB-01 | Axe constitutionnel runtime dans contrat minimal | architecture |
| Élevée | ARB-02 | Projections dérivées : emplacement + gate d'usage | architecture (b,c) + décision (a) |
| Élevée | ARB-03 | Gouvernance release : condition de blocage + pipeline STAGE_08 | state + pipeline |
| Élevée | ARB-06 | `canonical_dependency_contract` schématisé | architecture |
| Modérée | ARB-04 | Maturité surdéclarée dans state | state |
| Modérée | ARB-07 | `runtime_entrypoint_type` provisoirement typé | architecture |
| Modérée | ARB-09 | Condition de blocage multi-IA formalisée | architecture + state |
| Faible | ARB-05 | `maturity_qualifier` dans metadata | architecture + state |
| Différé | ARB-08 | PF_CHAIN_05 délégation | architecture (V1) |
| Différé | ARB-11 | Fingerprints artefacts factory | architecture (V1) |
| Clarif. req. | ARB-10 | Double-buffer périmètre | architecture (après CLR-03) |

---

*Fin de la proposition d'arbitrage PFARB_20260408_PERPL_Z9K4*
*Ce document est une proposition d'arbitrage indépendante. Il n'est pas l'arbitrage canonique final du stage. Il doit être consolidé avec les autres propositions d'arbitrage disponibles avant la synthèse finale de STAGE_02.*
