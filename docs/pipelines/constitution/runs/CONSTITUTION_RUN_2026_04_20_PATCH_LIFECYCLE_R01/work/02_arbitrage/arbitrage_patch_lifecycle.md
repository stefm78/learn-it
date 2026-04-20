# Arbitrage Report — patch_lifecycle
run_id: CONSTITUTION_RUN_2026_04_20_PATCH_LIFECYCLE_R01
scope_key: patch_lifecycle
stage_id: STAGE_02_ARBITRAGE
mode: bounded_local_run

## executive_summary

L’arbitrage retient une ligne conservatrice et exploitable.

Le scope `patch_lifecycle` reste globalement sain. Les garde-fous sur la validation déterministe, la précomputation hors session, l’interdiction de modifier silencieusement la philosophie adaptative et l’obligation d’escalade hors session en cas de dérive persistante non patchable sont jugés solides.

En revanche, deux constats dépassent le correctif local borné :
1. la dépendance inter-Core vers le Référentiel est incohérente entre les artefacts lus par le run et l’état courant du LINK ;
2. la frontière entre `patch_lifecycle` et `learner_state` mérite un traitement de partition ou de backlog gouvernant plutôt qu’un patch local immédiat.

Un seul point est retenu comme prêt pour `STAGE_03_PATCH_SYNTHESIS` :
- raccorder explicitement la journalisation des conflits non couverts à une sortie gouvernante traçable.

Aucun patch YAML n’est produit ici. L’arbitrage décide seulement quoi corriger maintenant, quoi reporter, et quoi remonter vers le backlog de gouvernance.

## scope_analysed

### Mode et surface effectivement consommée
- `run_context.yaml` lu en premier
- `scope_manifest.yaml`
- `impact_bundle.yaml`
- `integration_gate.yaml`
- challenge report unique : `challenge_report_patch_lifecycle.md`
- supporting reads repris :
  - `scope_extract.yaml`
  - `neighbor_extract.yaml`
- fallback ciblé repris explicitement sur la dépendance voisine manquante, avec lecture du Core `link.yaml`

### Constat clé de fallback
Le challenge déclarait un fallback ciblé sur `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`.  
Le fallback confirme que le `LINK` canonique courant fédère désormais :
- Constitution V4.0
- Référentiel v3.0

La dépendance voisine attendue par le run n’est donc pas seulement absente de `neighbor_extract.yaml` ; elle paraît aussi stale par rapport à l’état inter-Core actuel. La correction de ce point dépasse le patch local borné sur `constitution.yaml`.

### Challenge reports considered
- `challenge_report_patch_lifecycle.md` : consommé comme source principale unique de STAGE_02

## detailed_arbitrage_by_finding

### Finding A1 — dépendance référentielle inter-Core incohérente

- challenge_finding_id: CH_F01_REFERENTIAL_DEPENDENCY_ALIGNMENT
- challenge_scope_status: out_of_scope_but_relevant
- arbitrage_decision: necessite_extension_scope
- arbitrage_justification: >-
    Le challenge a correctement signalé une fragilité sur la dépendance aux seuils
    et paramètres délégués au Référentiel. Le run attend une ancre voisine
    `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`, tandis que l’état inter-Core
    courant lu via le LINK pointe vers un couplage Constitution V4.0 / Référentiel v3.0.
    Cette remise en cohérence dépasse un patch local borné sur les IDs du scope
    `patch_lifecycle` et relève d’un traitement de gouvernance/partition ou d’une
    réconciliation inter-Core plus large.
- patch_readiness: blocked_by_scope_extension
- related_gate_checks: []
- gate_effect: no_effect
- human_decision_required_flag: false
- conservative_default: >-
    Ne pas tenter de corriger localement cette ancre dans STAGE_03.
    Ouvrir un candidat backlog gouvernant et traiter la remise en cohérence via
    Stage 00 / revue de partition / politique de génération des scopes.
- options_considered:
  - aligner localement le run sur l’ancre attendue
  - corriger uniquement le texte constitutionnel dans le scope
  - traiter la dérive comme un problème inter-Core / partition
- retained_option: traiter la dérive comme un problème inter-Core / partition

### Finding A2 — risque de glissement du patch vers l’adaptation runtime

- challenge_finding_id: CH_F02_PATCH_VS_RUNTIME_ADAPTATION_BOUNDARY
- challenge_scope_status: in_scope
- arbitrage_decision: reporter
- arbitrage_justification: >-
    Le risque signalé par le challenge est réel, mais les garde-fous déjà présents
    dans le scope sont jugés substantiels : interdiction du changement de philosophie
    adaptative par patch, refus de l’inférence psychologique autonome, validation locale
    déterministe et watchpoint explicite contre le glissement vers l’adaptation runtime.
    À ce stade, aucun défaut textuel suffisamment précis ne justifie un patch local
    immédiat sans risque de sur-correction.
- patch_readiness: decision_only_no_patch_yet
- related_gate_checks:
  - WP_03
  - FORBIDDEN_OPS_ENFORCEMENT
- gate_effect: keeps_open
- human_decision_required_flag: false
- conservative_default: >-
    Conserver le garde-fou comme point de vigilance explicite, sans produire de patch
    local à ce stade.
- options_considered:
  - renforcer immédiatement les formulations du scope
  - considérer les garde-fous existants comme suffisants pour l’instant
- retained_option: considérer les garde-fous existants comme suffisants pour l’instant

### Finding A3 — frontière patch_lifecycle vs learner_state insuffisamment nette

- challenge_finding_id: CH_F03_PATCH_LIFECYCLE_LEARNER_STATE_BOUNDARY
- challenge_scope_status: out_of_scope_but_relevant
- arbitrage_decision: necessite_extension_scope
- arbitrage_justification: >-
    Le challenge a raison de distinguer les signaux d’état apprenant, qui relèvent
    structurellement de `learner_state`, des mécanismes de réponse par patch ou escalade,
    qui relèvent de `patch_lifecycle`. Le gate du run signale déjà cette frontière comme
    sensible. Toute correction robuste dépasse le simple patch local : elle peut demander
    un redécoupage de partition, une clarification inter-scope, ou une policy de lecture
    plus explicite.
- patch_readiness: blocked_by_scope_extension
- related_gate_checks:
  - WP_04
  - WP_05
- gate_effect: keeps_open
- human_decision_required_flag: false
- conservative_default: >-
    Ne pas élargir silencieusement le scope local. Préserver ce point comme candidat
    backlog de partition et traiter la clarification dans un cadre inter-scope.
- options_considered:
  - corriger localement seulement le texte du scope
  - déplacer une partie du problème vers `learner_state`
  - traiter le sujet comme problème de frontière de partition
- retained_option: traiter le sujet comme problème de frontière de partition

### Finding A4 — journalisation des conflits non couverts sans issue gouvernante assez explicite

- challenge_finding_id: CH_F04_UNCOVERED_CONFLICT_GOVERNED_EXIT_PATH
- challenge_scope_status: in_scope
- arbitrage_decision: corriger_maintenant
- arbitrage_justification: >-
    Ce point est bien localisable dans le scope. `ACTION_LOG_UNCOVERED_CONFLICT`
    existe déjà, mais le challenge a correctement noté que sa sortie gouvernante
    n’est pas assez explicitée. Une clarification locale minimale, sans réécriture
    large du système, est jugée légitime et utile : le log doit déboucher plus
    clairement sur une issue gouvernée, traçable et non passive.
- patch_readiness: ready_for_local_patch
- related_gate_checks:
  - FORBIDDEN_OPS_ENFORCEMENT
- gate_effect: helps_clear
- human_decision_required_flag: false
- conservative_default: >-
    Synthétiser en STAGE_03 un patch local minimal qui explicite le raccord entre
    conflit non couvert, traitement conservateur et sortie gouvernante traçable.
- options_considered:
  - ne rien changer
  - ajouter une clarification locale minimale
  - ouvrir seulement un backlog sans patch local
- retained_option: ajouter une clarification locale minimale

## consolidated_points

1. Le challenge est globalement validé dans son diagnostic.
2. Le scope `patch_lifecycle` n’appelle pas une réécriture large.
3. Le défaut le plus directement patchable localement est la sortie gouvernante des conflits non couverts.
4. Les sujets de dépendance référentielle et de frontière avec `learner_state` doivent être traités comme sujets inter-Core / inter-scope, pas comme simples patchs locaux.
5. Le risque de glissement vers l’adaptation runtime reste un point de vigilance fort, mais pas un patch local retenu à ce stade.

## decisions_for_patch

### Décisions retenues pour STAGE_03_PATCH_SYNTHESIS

- **A4 / CH_F04_UNCOVERED_CONFLICT_GOVERNED_EXIT_PATH**
  - décision: `corriger_maintenant`
  - type de correctif attendu: clarification locale minimale
  - objectif: expliciter qu’un conflit non couvert journalisé ne reste pas un état passif, mais alimente une sortie gouvernante traçable
  - périmètre autorisé: IDs du scope `patch_lifecycle` uniquement
  - attente pour STAGE_03: produire un patch local minimal et traçable, sans extension silencieuse de scope

## decisions_not_retained

### Décisions explicitement non retenues comme patch local immédiat

- **A1 / CH_F01_REFERENTIAL_DEPENDENCY_ALIGNMENT**
  - non retenu pour patch local
  - raison: incohérence inter-Core / inter-version dépassant le scope borné

- **A2 / CH_F02_PATCH_VS_RUNTIME_ADAPTATION_BOUNDARY**
  - non retenu pour patch local
  - raison: garde-fous déjà présents ; risque réel mais pas de défaut textuel assez précis pour justifier un patch immédiat minimal

- **A3 / CH_F03_PATCH_LIFECYCLE_LEARNER_STATE_BOUNDARY**
  - non retenu pour patch local
  - raison: sujet de frontière de partition / répartition de responsabilité entre scopes

## governance_backlog_candidates

```yaml
governance_backlog_candidates:
  - candidate_id: GBC_PATCH_LIFECYCLE_REF_ALIGNMENT_2026_04_20
    backlog_entry_type: policy_conflict
    title: Réaligner l’ancrage inter-Core Référentiel attendu par patch_lifecycle
    related_scope_keys:
      - patch_lifecycle
    originating_run_id: CONSTITUTION_RUN_2026_04_20_PATCH_LIFECYCLE_R01
    source_finding_id: CH_F01_REFERENTIAL_DEPENDENCY_ALIGNMENT
    rationale: >-
      Le run attend une ancre voisine référentielle V2.0, alors que l’état inter-Core
      courant observé via le LINK fédère Constitution V4.0 et Référentiel v3.0.
      La correction dépasse un patch local sur constitution.yaml et doit être rejouée
      dans une chaîne gouvernante de réconciliation / partition.
    recommended_stage00_action: >-
      Réexaminer les politiques et décisions de génération des scopes, puis
      régénérer le scope catalog et ses dépendances voisines sur la base des
      ancres inter-Core courantes.
    candidate_status: candidate_open

  - candidate_id: GBC_PATCH_LIFECYCLE_LEARNER_STATE_BOUNDARY_2026_04_20
    backlog_entry_type: partition_angle_mort
    title: Clarifier la frontière de responsabilité entre patch_lifecycle et learner_state
    related_scope_keys:
      - patch_lifecycle
      - learner_state
    originating_run_id: CONSTITUTION_RUN_2026_04_20_PATCH_LIFECYCLE_R01
    source_finding_id: CH_F03_PATCH_LIFECYCLE_LEARNER_STATE_BOUNDARY
    rationale: >-
      Les déclencheurs de patch dépendent de signaux d’état apprenant, alors que les
      réponses par patch et les escalades hors session relèvent d’un autre scope.
      La frontière actuelle est surveillée par le gate mais mérite une clarification
      de partition.
    recommended_stage00_action: >-
      Réviser explicitement la séparation des responsabilités entre signaux d’état,
      déclencheurs référentiels, patch governance et escalades hors session, puis
      décider s’il faut ajuster la partition ou seulement ses documents de binding.
    candidate_status: candidate_open
