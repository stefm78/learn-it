# STAGE_01_CHALLENGE — challenge_report_2026_04_20_kd_r02

## executive_summary

Le périmètre `knowledge_and_design` apparaît globalement cohérent sur son cœur métier : typage obligatoire des Knowledge Units, acyclicité du graphe, interdiction du Bloom élevé sans contexte authentique, fallback sûr sur erreurs non couvertes, et obligation d’un chemin de feedback déterministe pour les KU créatives. Cet ensemble dessine une architecture de design prudente et lisible.

Le principal point faible n’est pas une contradiction interne majeure du périmètre lui-même, mais une fragilité de fermeture système en mode borné : le run attend comme lecture voisine l’ID `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`, mais cet ID n’est trouvé dans aucun extract voisin et le `LINK` courant expose à la place des références `LINK_REF_CORE_LEARNIT_CONSTITUTION_V4_0` et `LINK_REF_CORE_LEARNIT_REFERENTIEL_v3.0`. Cela signale un drift de version / de convention d’identifiants entre le scope catalog dérivé et le Core courant. Tant que ce drift n’est pas arbitré, le challenge borné lit correctement le cœur du scope mais ne ferme pas proprement l’axe inter-Core attendu.

Deuxième tension importante : `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION` dépend d’un invariant `INV_NO_RUNTIME_CONTENT_GENERATION` qui n’apparaît ni dans le scope extract ni dans les lectures voisines demandées. Cette dépendance implicite rend le périmètre moins autosuffisant qu’annoncé et peut dégrader la qualité des arbitrages ultérieurs.

## challenge_scope

- Run: `CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02`
- Mode: `bounded_local_run`
- Read surface utilisée :
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/run_context.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/scope_extract.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/neighbor_extract.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/scope_manifest.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/impact_bundle.yaml`
  - `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02/inputs/integration_gate.yaml`
- Fallback ids déclarés explicitement :
  - `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` (absent du `neighbor_extract`, fallback ciblé sur `docs/cores/current/link.yaml` uniquement)
- Périmètre modifiable autorisé : uniquement les IDs et modules déclarés dans `scope_manifest.yaml`.
- Tout constat hors périmètre est signalé comme `out_of_scope_but_relevant` ou `needs_scope_extension` et non proposé comme correction silencieuse.

## detailed_analysis_by_axis

### 1. internal_coherence

**Constat principal.** Le sous-système `knowledge_and_design` est bien structuré autour d’un enchaînement logique fort :
- `TYPE_KNOWLEDGE_UNIT` impose le typage,
- `TYPE_KNOWLEDGE_GRAPH` + `INV_EXPLICIT_DEPENDENCY_EDGES_REQUIRED` + `INV_KNOWLEDGE_GRAPH_MUST_BE_ACYCLIC` verrouillent la topologie du graphe,
- `TYPE_FEEDBACK_COVERAGE_MATRIX` + `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK` + `EVENT_UNCOVERED_ERROR` cadrent le fallback d’erreur,
- `TYPE_AUTHENTIC_CONTEXT` + `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4` + `CONSTRAINT_NO_HIGH_BLOOM_WITHOUT_AUTHENTIC_CONTEXT` bloquent la dérive vers du Bloom élevé sans ancrage réel,
- `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` complète le dispositif en empêchant l’autonomie créative sans feedback local formalisé.

**Appréciation.** Cohérence interne élevée. Les invariants structurants et les règles de design ne se contredisent pas ; ils convergent vers une logique de sûreté et d’auditabilité.

**Statut scope.** `in_scope`

### 2. theoretical_soundness

**Point fort.** La séparation entre structure du graphe, design pédagogique et sécurité runtime est globalement saine. L’architecture ne cherche pas à résoudre les lacunes du design par génération opportuniste au runtime ; au contraire, elle force la préparation explicite des feedbacks et des dépendances.

**Point faible.** `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION` dépend de `INV_NO_RUNTIME_CONTENT_GENERATION`, mais cet invariant n’est pas visible dans le périmètre de lecture borné. Théoriquement, la contrainte de feedback semble donc reposer sur un principe plus large non rendu explicite localement. Le périmètre paraît cohérent pour un lecteur connaissant déjà le système, moins pour un run borné supposé autosuffisant.

**Statut scope.** `needs_scope_extension`

### 3. undefined_engine_states

**Risque détecté.** Le traitement des IDs manquants est bien prévu par le mécanisme de fallback des extracts, mais le contenu métier signale tout de même un état moteur partiellement sous-spécifié : si la résolution inter-Core dépend d’un binding dont l’ID attendu ne correspond plus au `LINK` courant, le système borné sait qu’il manque quelque chose sans savoir, localement, quelle substitution canonique est autorisée.

**Conséquence.** État de lecture dégradé mais non silencieux : bon pour la sûreté, mauvais pour la fluidité opérationnelle.

**Statut scope.** `out_of_scope_but_relevant`

### 4. implicit_ai_dependencies

**Constat.** Le scope est plutôt bon sur ce point : il préfère des artefacts déterministes (`feedback coverage matrix`, dépendances explicites, contraintes de Bloom, fallback générique) à des décisions implicites laissées au modèle.

**Mais** la dépendance implicite à un invariant hors surface (`INV_NO_RUNTIME_CONTENT_GENERATION`) et le drift d’ID côté voisin créent malgré tout une dépendance cognitive à un lecteur humain ou IA connaissant l’historique des versions du système.

**Statut scope.** `in_scope` pour le design local, `out_of_scope_but_relevant` pour la fermeture inter-Core.

### 5. governance

**Constat.** Le `scope_manifest` et l’`integration_gate` sont bien alignés :
- aucune modification silencieuse hors scope,
- aucune promotion directe,
- aucune réallocation implicite entre Cores,
- watchpoints explicites sur la frontière graphe / runtime, sur le placement de `INV_EXPLICIT_DEPENDENCY_EDGES_REQUIRED`, sur le statut design du contexte authentique, et sur la non-dérivation de règles adaptatives depuis des invariants structurels.

**Appréciation.** Gouvernance forte et bien ciblée.

**Vigilance.** Le watchpoint `WP_02` confirme justement la sensibilité de la frontière de scope autour de `INV_EXPLICIT_DEPENDENCY_EDGES_REQUIRED`. Le challenge ne relève pas d’erreur manifeste ici, mais considère cette frontière comme un point d’arbitrage à conserver sous contrôle strict.

**Statut scope.** `in_scope`

### 6. adversarial_scenarios

Scénarios adversariaux plausibles :

1. **Version drift silencieux des bindings inter-Core.** Un scope borné attend un ancien ID de référence, ne trouve rien, et l’IA improvise une lecture élargie non gouvernée. Ici le fallback explicite évite le pire, mais le drift lui-même reste un problème réel.
2. **Contournement du design par runtime.** Sans matrice de couverture suffisante, un système pourrait être tenté de générer du feedback à la volée. Les contraintes actuelles l’interdisent explicitement, ce qui est robuste.
3. **Glissement de sens entre design et runtime.** Le contexte authentique pourrait être réinterprété comme donnée runtime au lieu de contrainte de design. Le watchpoint `WP_03` montre que ce risque est déjà anticipé.
4. **Propagations sur graphe incomplètement explicité.** Sans arêtes de dépendance explicites, des mécanismes de propagation ou de recommandation pourraient déduire trop. L’invariant correspondant est correctement posé.

**Statut scope.** `in_scope`

### 7. risk_prioritization

#### Risque P1 — Drift d’ID/version entre impact bundle et LINK courant
- Symptôme : `neighbor_extract` attend `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`, mais le `LINK` courant expose `LINK_REF_CORE_LEARNIT_CONSTITUTION_V4_0` et `LINK_REF_CORE_LEARNIT_REFERENTIEL_v3.0`.
- Impact : fermeture inter-Core non fiable en mode borné ; risque d’arbitrage fondé sur une surface voisine obsolète.
- Scope status : `out_of_scope_but_relevant`

#### Risque P1 — Dépendance implicite hors surface sur `INV_NO_RUNTIME_CONTENT_GENERATION`
- Symptôme : une contrainte du scope dépend d’un invariant absent des extraits et des lectures voisines demandées.
- Impact : autosuffisance bornée incomplète ; difficulté à arbitrer proprement les corrections sans lecture complémentaire.
- Scope status : `needs_scope_extension`

#### Risque P2 — Frontière de responsabilité design / runtime potentiellement fragile
- Symptôme : plusieurs règles clefs reposent sur une distinction fine entre structure du graphe, design pédagogique et exécution runtime.
- Impact : déplacement futur d’une règle vers le mauvais scope possible lors des patches.
- Scope status : `in_scope`

#### Risque P3 — Absence de voisin explicite exploitable malgré présence d’un devoir de lecture
- Symptôme : `mandatory_reads.files` inclut `referentiel.yaml` et `link.yaml`, mais `mandatory_reads.ids` ne fournit qu’un unique ID voisin non résolu.
- Impact : lecture voisine formellement prescrite mais matériellement peu exploitable dans un run borné.
- Scope status : `out_of_scope_but_relevant`

## priority_risks

1. **P1 — Drift d’identifiants inter-Core entre scope catalog / impact bundle et LINK courant.**
2. **P1 — Dépendance implicite hors surface sur `INV_NO_RUNTIME_CONTENT_GENERATION`.**
3. **P2 — Fragilité potentielle de la frontière design / runtime / graphe.**
4. **P3 — Lecture voisine prescrite mais sous-spécifiée en mode borné.**

## corrections_to_arbitrate_before_patch

1. **Arbitrer la référence inter-Core canonique attendue par `knowledge_and_design`.**
   - Décider si le scope / impact bundle doit pointer vers les IDs `LINK_REF_CORE_*` actuels, ou si un alias / binding de compatibilité doit être introduit.
   - Ne pas corriger silencieusement dans ce stage.
   - Scope status : `out_of_scope_but_relevant`

2. **Arbitrer si `INV_NO_RUNTIME_CONTENT_GENERATION` doit rejoindre les lectures voisines ou le périmètre du scope.**
   - Deux voies possibles :
     - enrichir `impact_bundle` / voisinage avec cet invariant,
     - ou reconnaître que `CONSTRAINT_NO_RUNTIME_FEEDBACK_GENERATION` dépend d’un socle hors-scope qu’il faut rendre explicitement lisible en run borné.
   - Scope status : `needs_scope_extension`

3. **Confirmer explicitement que `INV_EXPLICIT_DEPENDENCY_EDGES_REQUIRED` reste bien dans `knowledge_and_design`.**
   - Le challenge ne demande pas de déplacement, mais recommande de sanctuariser cette décision d’architecture lors de l’arbitrage.
   - Scope status : `in_scope`

4. **Arbitrer la qualité attendue des lectures voisines en mode borné.**
   - Un unique ID voisin non résolu est probablement insuffisant pour une lecture inter-Core robuste.
   - Scope status : `out_of_scope_but_relevant`

## human_actions_to_execute

1. **Valider humainement ce challenge report.**
2. **Si le rapport est accepté, mettre à jour le tracking :**

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02 \
  --stage-id STAGE_01_CHALLENGE \
  --stage-status done \
  --run-status active \
  --next-stage STAGE_02_ARBITRAGE \
  --summary "Challenge report produced; ready for arbitrage."
```

3. **Après exécution confirmée, relancer avec :**

```text
Continue le run CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R02 — STAGE_01 est done, démarre STAGE_02_ARBITRAGE.
```

4. **Action de gouvernance annexe recommandée, hors clôture de stage :**
   examiner le run cassé `CONSTITUTION_RUN_2026_04_20_KNOWLEDGE_AND_DESIGN_R01` encore visible dans `runs/index.yaml`, afin d’éviter de futures ambiguïtés d’entrée.
