# Scope redesign arbitration summary

Status: PARTIALLY_ARBITRATED

## Accepted macro-decisions

### MACRO_001_REFERENTIEL_LINK_UNOWNED_CLASSIFICATION

- Title: Classify currently UNOWNED referentiel/link areas
- Selected option: `declare_referentiel_and_link_as_read_only_external_cores`
- Canonicalization action: Introduire une politique explicite de classification des IDs referentiel/link : external_read_only_core pour les IDs lus mais non possédés par la Constitution, shared/global seulement si nécessaire, et ownership par un scope constitution uniquement lorsqu'il existe une responsabilité de gouvernance réelle. Le validateur de bijection devra distinguer les IDs constitution-owned des IDs external_read_only.

### MACRO_002_PATCH_LIFECYCLE_CORE_STRUCTURE

- Title: Decide whether patch lifecycle structural core remains a canonical scope/subcluster
- Selected option: `name_as_patch_structure_subcluster`
- Canonicalization action: Conserver ces IDs dans patch_lifecycle. Ajouter une classification ou note de sous-grappe nommée patch_structure_and_quality dans les artefacts de Scope Lab, puis éventuellement dans la policy de scoping si la méthode est validée.

### MACRO_003_PATCH_TRIGGER_BOUNDARY

- Title: Decide boundary for patch triggers and learner/runtime signals
- Selected option: `keep_triggers_in_patch_lifecycle_with_neighbors`
- Canonicalization action: Conserver les règles/événements/actions de déclenchement dans patch_lifecycle. Déclarer explicitement les IDs learner_state nécessaires comme neighbors. Créer si besoin une sous-grappe diagnostique patch_trigger_governance.

### MACRO_006_SCOPE_BOUNDARY_REVIEW

- Title: Review all existing scope boundaries
- Selected option: `redesign_patch_lifecycle_first`
- Canonicalization action: Utiliser patch_lifecycle comme premier scope pilote pour valider la méthode graph-based. Les autres scopes restent temporairement inchangés, avec leurs anomalies conservées comme backlog d'arbitrage.

## Pending macro-decisions

- MACRO_004_MULTI_OWNER_CLUSTER_REVIEW — Review multi-owner graph clusters
- MACRO_005_NEIGHBOR_DECLARATION_REVIEW — Review explicit neighbor declarations
