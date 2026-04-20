# Challenge Report — STAGE_01_CHALLENGE
Run ID: CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01
Scope: mastery_evaluation
Mode: bounded_local_run

## Executive summary

Le scope `mastery_evaluation` est globalement cohérent sur ses invariants métier centraux : MSC reste un AND strict sur P/R/A, T reste séparé de la maîtrise de base, la propagation graphe reste limitée à un saut, les cas de non-calculabilité et de sécurité sont explicitement traités, et les watchpoints du gate sont bien alignés avec cette architecture.

Le principal problème détecté n’est pas une incohérence locale du noyau métier du scope, mais une incohérence inter-core et inter-artefacts de run : les objets du scope utilisent déjà des références référentielles de génération récente (`REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`), tandis que l’`impact_bundle` et le `neighbor_extract` attendent encore `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`, identifiant absent du Référentiel courant. Cette divergence fragilise la règle de lecture ids-first, peut rendre certaines analyses de dépendances incomplètes, et suggère un problème de partitionnement ou de génération de voisins plus qu’un problème de logique métier dans le scope lui-même.

En conséquence, le stage peut produire un challenge utile, mais il doit signaler explicitement cette dette de cohérence avant arbitrage. La correction à arbitrer porte prioritairement sur le chaînage inter-core et sur la génération des voisins référentiels du scope.

## Challenge scope

### Read surface declared

Primary reads used:
- run_context.yaml
- scope_extract.yaml
- neighbor_extract.yaml
- scope_manifest.yaml
- impact_bundle.yaml
- integration_gate.yaml

Explicit fallback used:
- docs/cores/current/referentiel.yaml

### Fallback IDs declared

Neighbor extract missing ID:
- `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`

Fallback reason:
- `neighbor_extract.yaml` signale explicitement cet ID comme manquant ; lecture ciblée du Référentiel courant effectuée uniquement pour cette dépendance.

### Scope status for major findings

1. Inter-core reference mismatch  
   Status: `in_scope`

2. Local MSC logic remains strict and separated from transfer  
   Status: `in_scope`

3. Graph propagation boundary appears preserved locally  
   Status: `in_scope`

4. Session integrity logic remains inside mastery_evaluation and should not drift to learner_state  
   Status: `in_scope`

5. Potential scope-catalog / impact-bundle obsolescence for referential neighbors  
   Status: `needs_scope_extension` only if the correction requires changing scope generation or neighbor derivation outside the writable perimeter; otherwise `in_scope` if handled as a local reference correction within constitution artifacts later in pipeline.

## Detailed analysis by axis

### 1. Internal coherence

Le cœur logique du scope est cohérent.

- `TYPE_MASTERY_MODEL` agrège P, R, A et T, mais l’invariant `INV_MSC_AND_STRICT` borne explicitement la maîtrise de base à P/R/A simultanément satisfaits.  
- `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY` confirme que T ne fait pas partie du noyau de maîtrise de base.  
- `RULE_MSC_COMPONENT_NON_CALCULABLE_DEFERS_BASE_MASTERY` interdit toute chute implicite à `false` lorsqu’une composante requise n’est pas calculable.  
- `RULE_LOW_SIS_NEVER_AUTO_PENALIZES` protège la logique d’intégrité contre une pénalisation automatique.  
- `RULE_PROVISIONAL_MASTERY_WINDOW_EXPIRY_SAFE_FALLBACK` et `RULE_T_EVALUATION_OVERDUE_REQUIRES_SIGNAL_OR_FOLLOWUP` ferment proprement deux états moteurs classiquement dangereux : expiration silencieuse d’un provisoire et oubli silencieux de T.

Aucune contradiction locale évidente n’a été trouvée entre ces règles. Le scope tient bien ses frontières métier internes.

### 2. Theoretical soundness

L’architecture conceptuelle est saine.

- La séparation entre maîtrise de base et transférabilité est bien pensée et défendable.
- La non-calculabilité ne devient pas une sanction implicite, ce qui évite un biais structurel.
- La sécurité est traitée de façon conservatrice : investigation systémique bornée, maîtrise provisoire expirée avec fallback sûr, SIS bas non punitif, contraintes fortes sur la surveillance.

Le point théorique le plus fragile n’est pas la logique métier mais la dépendance à un Référentiel valide pour les seuils délégués. Cette fragilité est toutefois déjà reconnue explicitement par `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION`.

### 3. Undefined engine states

Le scope ferme plusieurs états indéfinis, mais pas tous.

États bien fermés :
- composante MSC non calculable → `deferred`, pas de faux négatif implicite
- maîtrise provisoire expirée → fallback sûr explicite
- T non évalué à temps → signal ou suivi explicite
- investigation systémique ouverte → clôture explicite requise dans une fenêtre bornée

État encore fragile :
- décalage entre les identifiants référentiels attendus par le scope / impact bundle et ceux réellement présents dans le Référentiel courant.  
  Ici, le moteur sait qu’un Référentiel valide est requis, mais l’artefact voisin fourni ne pointe pas vers la bonne génération. Cela crée un état pratique de “voisin déclaré mais non résoluble” qui n’est pas un état moteur théorique, mais un état d’exécution pipeline mal fermé.

### 4. Implicit AI dependencies

Le scope dépend fortement de la qualité des artefacts dérivés produits avant STAGE_01.

Le meilleur exemple est ici :
- `impact_bundle.yaml` demande `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`
- `neighbor_extract.yaml` ne le trouve pas
- le fallback ciblé montre un Référentiel courant en `v3.0`
- plusieurs entrées du scope référencent déjà `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`

Cela signifie que l’IA pourrait raisonner sur une image incomplète ou obsolète du voisinage si elle suivait naïvement les extraits sans contrôle critique. Le stage révèle donc une dépendance implicite à la fraîcheur et à la cohérence du partitionnement/générateur d’artefacts.

### 5. Governance

Le périmètre de modification est clair : seul `docs/cores/current/constitution.yaml` est dans le writable perimeter du scope manifest. Le gate interdit explicitement toute promotion directe, toute modification silencieuse hors scope et toute réallocation implicite cross-core.

Les watchpoints du gate sont bons et alignés :
- ne pas diluer MSC AND strict
- préserver la séparation base/T
- vérifier les frontières évaluation / propagation / référentiel
- garder `non calculable -> deferred`
- maintenir `one hop` ici
- ne pas faire glisser SIS / NC_MSC vers learner_state

Le vrai sujet de gouvernance est que l’artefact de voisinage semble désaligné de l’état courant des cores. Cela relève soit :
- d’un problème de génération du scope catalog / impact bundle,
- soit d’une obsolescence des références inter-core dans la Constitution.

### 6. Adversarial scenarios

Scénarios adversariaux plausibles :

#### A. Faux diagnostic de dépendance référentielle
Un pipeline aval ou une IA peu prudente pourrait conclure que le Référentiel requis est absent, alors que le vrai problème est un identifiant inter-core obsolète dans les artefacts de voisinage.

#### B. Réécriture abusive du problème comme patch local
On pourrait être tenté de corriger localement une règle métier du scope alors que la source du défaut est le couplage inter-core ou le générateur d’artefacts. Ce serait une correction hors cible.

#### C. Dilution implicite du garde-fou référentiel
Face à la difficulté de résoudre l’ID référentiel, un correctif pourrait chercher à affaiblir l’invariant `INV_REFERENTIEL_VALIDITY_REQUIRED_FOR_DELEGATED_THRESHOLD_EVALUATION`. Ce serait une très mauvaise direction, contraire au safety model du scope.

#### D. Glissement de périmètre
La logique SIS / NC_MSC ou la logique de propagation pourrait être déplacée hors de ce scope pour “réparer” la cohérence perçue. Le gate indique explicitement que ce glissement serait suspect.

### 7. Risk prioritization

#### Risk 1 — Critical
**Inter-core reference mismatch between scope logic and neighbor bundle**

Le scope contient des dépendances vers `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`, alors que le voisinage de run exige `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION`, absent du Référentiel courant.  
Impact : lecture ids-first partiellement trompeuse, arbitrage potentiellement biaisé, patch local mal ciblé.

#### Risk 2 — High
**Run context appears stale relative to actual extracted artifacts**

`run_context.yaml` affiche encore `scope_extract.present=false` et `neighbor_extract.present=false`, alors que les fichiers existent maintenant.  
Impact : reprise de run potentiellement ambiguë, outillage de launcher trompeur, risque de blocage ou de rework inutile.

#### Risk 3 — Medium
**Mastery-evaluation depends on referential validity but neighbor derivation is not robust enough**

Le scope est théoriquement bien protégé par l’invariant de validité référentielle, mais la matérialisation effective des voisins ne garantit pas encore cette cohérence.  
Impact : fragilité pipeline plutôt que logique métier.

#### Risk 4 — Medium
**Potential under-specification of cross-scope edges**

`neighbor_scopes` est vide dans l’`impact_bundle`, alors qu’il existe visiblement une dépendance forte au Référentiel et à la couche état apprenant.  
Impact : lecture de voisinage peut être correcte au niveau IDs mais pauvre au niveau de la cartographie sémantique.

## Corrections to arbitrate before patch

1. **Corriger l’identifiant de dépendance référentielle attendu par le scope/impact bundle**
   - Vérifier si `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` est un reliquat obsolète.
   - Aligner sur l’identifiant réellement attendu par les objets de `mastery_evaluation`, qui semblent viser `REF_CORE_LEARNIT_REFERENTIEL_V4_0_IN_CONSTITUTION`.

2. **Réviser la génération du voisinage pour `mastery_evaluation`**
   - Le problème peut être dans la scope definition, dans les décisions de partition, ou dans les artefacts générés.
   - À arbitrer : correction locale du scope catalog vs correction plus large du générateur ou des décisions de partition.

3. **Reconstruire le `run_context.yaml` après les extractions**
   - Ce n’est pas une correction métier du core, mais une correction de cohérence d’exécution du run.
   - À arbitrer comme action technique nécessaire pour éviter un raisonnement aval sur contexte dérivé obsolète.

4. **Ne pas corriger la logique MSC elle-même à ce stade**
   - Aucun élément du challenge ne justifie pour l’instant de modifier :
     - `INV_MSC_AND_STRICT`
     - la séparation de T
     - `RULE_MSC_COMPONENT_NON_CALCULABLE_DEFERS_BASE_MASTERY`
     - `INV_GRAPH_PROPAGATION_ONE_HOP`
     - les règles SIS/NC_MSC

## Human actions to execute

1. **Sauvegarder ce rapport**
   - Fichier cible :
     `docs/pipelines/constitution/runs/CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01/work/01_challenge/challenge_report_mastery_evaluation_r01.md`

2. **Rebuilder le contexte de run**
   - Commande :
     ```bash
     python docs/patcher/shared/build_run_context.py \
       --pipeline constitution \
       --run-id CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01
     ```

3. **Passer le tracking de STAGE_01 à done si tu valides ce rapport**
   - Commande canonique :
     ```bash
     python docs/patcher/shared/update_run_tracking.py \
       --pipeline constitution \
       --run-id CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01 \
       --stage-id STAGE_01_CHALLENGE \
       --stage-status done \
       --run-status active \
       --next-stage STAGE_02_ARBITRAGE \
       --summary "Challenge report produced; ready for arbitrage."
     ```

4. **Relancer ensuite**
   - Prompt suivant :
     `Continue le run CONSTITUTION_RUN_2026_04_20_MASTERY_EVALUATION_R01 — STAGE_01 est done, démarre STAGE_02_ARBITRAGE.`
