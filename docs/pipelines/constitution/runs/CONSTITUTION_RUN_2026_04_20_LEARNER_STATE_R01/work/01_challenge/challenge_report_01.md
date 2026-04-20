# STAGE_01_CHALLENGE — learner_state
run_id: CONSTITUTION_RUN_2026_04_20_LEARNER_STATE_R01
scope_key: learner_state
mode: bounded_local_run

## executive_summary

Le scope `learner_state` présente une cohérence locale assez forte sur la philosophie de prudence pédagogique : état `unknown` autorisé, refus des inférences forcées, priorité structurelle de la détresse, et distinction nette entre signaux AR, proxys et VC :contentReference[oaicite:1]{index=1}

En revanche, trois fragilités gouvernantes ressortent :

1. **Discordance inter-Core de références/versionnement**.  
   Le voisin demandé par le run est `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` :contentReference[oaicite:2]{index=2}, alors que le `link.yaml` courant expose des références `LINK_REF_CORE_LEARNIT_REFERENTIEL_v3.0` :contentReference[oaicite:3]{index=3} et que le `referentiel.yaml` courant est `CORE_LEARNIT_REFERENTIEL_v3.0` avec `REF_CORE_LEARNIT_CONSTITUTION_V4_0_IN_REFERENTIEL` côté Référentiel :contentReference[oaicite:4]{index=4}.  
   Cette chaîne n’est donc pas fermée proprement pour le run.

2. **Fallback voisin nécessaire dès STAGE_01**.  
   `neighbor_extract.yaml` signale explicitement l’ID voisin manquant `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` :contentReference[oaicite:5]{index=5}, ce qui a forcé une lecture canonique ciblée hors extract, autorisée par le skill mais révélatrice d’un problème de matérialisation ou de nommage inter-Core :contentReference[oaicite:6]{index=6}

3. **Dépendances opérationnelles hors périmètre de lecture déclaré**.  
   Des règles du scope déclenchent des actions qui ne figurent ni dans les IDs du scope, ni dans le voisinage déclaré du run. Par exemple `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME` cible `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK` :contentReference[oaicite:7]{index=7}, et `RULE_CONSERVATIVE_SCAFFOLDING_ESCALATION_REQUIRES_OFFSESSION_REVIEW` ainsi que `RULE_ACTIVATION_DISTRESS_PERSISTENCE_ESCALATION_OFFSESSION` ciblent `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION` :contentReference[oaicite:8]{index=8}.  
   Cela suggère une sous-déclaration du voisinage logique ou une fermeture locale incomplète du scope.

## challenge_scope

### read_surface_declared

Lecture primaire effectivement utilisée :
- `run_context.yaml` :contentReference[oaicite:9]{index=9}
- `scope_extract.yaml` :contentReference[oaicite:10]{index=10}
- `neighbor_extract.yaml` :contentReference[oaicite:11]{index=11}
- `scope_manifest.yaml` :contentReference[oaicite:12]{index=12}
- `impact_bundle.yaml` :contentReference[oaicite:13]{index=13}
- `integration_gate.yaml` :contentReference[oaicite:14]{index=14}

### fallback_ids_declared_if_any

Fallback explicite utilisé pour :
- `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` — absent de `neighbor_extract.yaml` :contentReference[oaicite:15]{index=15}

Fallback canoniques effectivement lus pour ce besoin :
- `docs/cores/current/link.yaml` :contentReference[oaicite:16]{index=16}
- `docs/cores/current/referentiel.yaml` :contentReference[oaicite:17]{index=17}

### writable_scope

Le périmètre modifiable autorisé reste borné à `docs/cores/current/constitution.yaml` et aux IDs listés dans `scope_manifest.yaml` ; toute extension exige décision explicite :contentReference[oaicite:18]{index=18}

## detailed_analysis_by_axis

### 1. internal_coherence

Le noyau `learner_state` est philosophiquement cohérent sur ses garde-fous principaux :
- `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise explicitement qu’un axe reste inconnu/absent/non-observable plutôt que d’être forcé :contentReference[oaicite:19]{index=19}
- `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` impose une entrée conservative bornée en cas d’observabilité insuffisante, avec scaffolding léger réversible :contentReference[oaicite:20]{index=20}
- `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` et `ACTION_APPLY_LIGHT_REVERSIBLE_SCAFFOLDING` alignent bien prudence et non-pénalisation en absence d’AR-N1 :contentReference[oaicite:21]{index=21}
- `INV_VC_NOT_GENERAL_MOTIVATION_PROXY` évite l’abus interprétatif sur l’axe Valeur-Coût :contentReference[oaicite:22]{index=22}
- `INV_DISTRESS_REGIME_PRIORITY_CANNOT_BE_OVERRIDDEN` verrouille correctement la priorité de la détresse :contentReference[oaicite:23]{index=23}

Constat : la logique locale est solide sur la sûreté d’entrée et la non-inférence abusive.

### 2. theoretical_soundness

Le modèle sépare assez proprement :
- les axes constitutionnels d’état (`TYPE_STATE_AXIS_*`) :contentReference[oaicite:24]{index=24}
- les auto-rapports (`TYPE_SELF_REPORT_AR_N1/N2/N3`) :contentReference[oaicite:25]{index=25}
- les paramètres et hiérarchies opératoires délégués au Référentiel, comme `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY` et `RULE_REFERENTIEL_SIGNAL_PRECEDENCE_ORDER` :contentReference[oaicite:26]{index=26}

Mais la fermeture théorique inter-Core est fragilisée par une grammaire de référence incohérente :
- le run attend `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` :contentReference[oaicite:27]{index=27}
- le Link courant ne matérialise pas cette référence et utilise `LINK_REF_CORE_LEARNIT_REFERENTIEL_v3.0` :contentReference[oaicite:28]{index=28}
- le Référentiel courant est en `v3.0` et référence la Constitution `V4_0` depuis son propre côté :contentReference[oaicite:29]{index=29}

Constat : la séparation Constitution/Référentiel reste bonne en théorie, mais la fédération nominale entre les trois Core n’est pas assez proprement alignée.

### 3. undefined_engine_states

Le scope traite bien plusieurs états dangereux :
- unknown / absent / non-observable pour les axes d’état :contentReference[oaicite:30]{index=30}
- détresse persistante avec escalade hors session :contentReference[oaicite:31]{index=31}
- conservatisme prolongé avec escalade hors session :contentReference[oaicite:32]{index=32}
- reprise après interruption longue via diagnostic de reprise :contentReference[oaicite:33]{index=33}

Mais deux transitions moteur sont insuffisamment fermées localement :
- `RULE_LONG_INTERRUPTION_REQUIRES_DIAGNOSTIC_RESUME` dépend d’une action cible hors surface lue (`ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`) :contentReference[oaicite:34]{index=34}
- les deux chaînes d’escalade hors session ciblent `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`, également hors surface lue :contentReference[oaicite:35]{index=35}

Constat : les événements et règles sont présents, mais certaines sorties moteur concrètes ne sont pas localement auditables dans le run borné.

### 4. implicit_ai_dependencies

Le scope est plutôt bon sur ce point :
- il interdit les complétions implicites d’état par simple absence de donnée via `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` :contentReference[oaicite:36]{index=36}
- il explicite l’usage d’AR-N1 contre les proxys avec journalisation de discordance via `RULE_AR_N1_OVERRIDES_PROXY` et `ACTION_LOG_AR_PROXY_DISCORDANCE` :contentReference[oaicite:37]{index=37}
- côté Référentiel, la hiérarchie des signaux et le reweighting borné d’AR-N3 sont documentés explicitement, sans inverser la priorité structurelle d’AR-N1 :contentReference[oaicite:38]{index=38}

Point d’attention : si les références inter-Core restent incohérentes, l’IA risque d’interpréter silencieusement des paramètres référentiels sans chaîne de binding proprement auditée.

### 5. governance

Le `scope_manifest` est clair :
- opérations autorisées : `challenge`, `arbitrage`, `patch`, `local_validation` :contentReference[oaicite:39]{index=39}
- opérations interdites : promotion directe, modification silencieuse hors scope, réallocation implicite inter-Core :contentReference[oaicite:40]{index=40}

L’`integration_gate` est aussi bien cadré :
- ne pas transformer un seuil référentiel en règle constitutionnelle implicite :contentReference[oaicite:41]{index=41}
- ne pas déduire une inférence psychologique plus forte que le cadre autorisé :contentReference[oaicite:42]{index=42}
- vérifier les frontières entre unknown, détresse, conservatisme et escalade :contentReference[oaicite:43]{index=43}
- vérifier que les liens au Référentiel restent explicites et non silencieux :contentReference[oaicite:44]{index=44}

Constat : la gouvernance du run est bonne, mais précisément l’un des watchpoints majeurs — l’explicitation des liens au Référentiel — est aujourd’hui sous tension.

### 6. adversarial_scenarios

Scénario adversarial crédible :
- un moteur ou une IA peut continuer à “faire comme si” la référence référentielle existait, malgré l’absence de correspondance nominale dans les extraits et dans le Link courant :contentReference[oaicite:45]{index=45} :contentReference[oaicite:46]{index=46}
- cela ouvre la voie à une résolution silencieuse de paramètres inter-Core, non auditée

Deuxième scénario :
- les règles d’escalade semblent fermées localement, mais les actions cibles réelles sont hors surface ; une IA peut donc surestimer la complétude du scope et ignorer une dépendance structurelle à un autre scope ou à un autre core slice :contentReference[oaicite:47]{index=47}

### 7. risk_prioritization

#### R1 — critique — in_scope
**Discordance inter-Core de références/versionnement**
Le run matérialise un besoin vers `REF_CORE_LEARNIT_REFERENTIEL_V2_0_IN_CONSTITUTION` :contentReference[oaicite:48]{index=48}, alors que le Link et le Référentiel courants sont en logique `v3.0` / `V4_0` différente :contentReference[oaicite:49]{index=49} :contentReference[oaicite:50]{index=50}  
Risque : fédération inter-Core non audit-able, fallbacks silencieux, patchs ultérieurs mal ancrés.

#### R2 — élevé — out_of_scope_but_relevant
**Sous-déclaration du voisinage logique du scope**
Des règles du scope déclenchent des actions absentes du périmètre lisible du run :contentReference[oaicite:51]{index=51}  
Risque : sentiment de fermeture locale trompeur ; arbitrage ou patch incomplet.

#### R3 — moyen — in_scope
**Mismatch entre extracts et vrais besoins de lecture**
Le `neighbor_extract` est vide alors que le run a besoin d’un voisin référentiel explicite :contentReference[oaicite:52]{index=52}  
Risque : dégradation de l’approche ids-first et augmentation des lectures fallback.

## priority_risks

1. R1 — normaliser immédiatement la chaîne de références inter-Core sur learner_state.
2. R2 — décider si les actions de reprise diagnostique / escalade hors session doivent entrer dans le voisinage obligatoire ou relever d’un autre scope explicite.
3. R3 — réaligner `impact_bundle` et/ou l’extraction pour que le voisinage réel soit matérialisé correctement.

## corrections_to_arbitrate_before_patch

### C1 — in_scope
Arbitrer un **schéma canonique unique de référence inter-Core** pour learner_state :
- soit une référence Constitution → Référentiel nommée dans le style actuel du Link/Référentiel,
- soit une autre convention,
- mais une seule, alignée entre Constitution, Référentiel, Link, impact_bundle et extracts.

### C2 — in_scope puis potentiellement cross-scope
Décider si `impact_bundle.mandatory_reads.ids` doit porter :
- une référence “cœur” unique,
- ou les IDs référentiels réellement nécessaires au scope learner_state.  
En l’état, l’unique voisin déclaré n’est pas résolu proprement :contentReference[oaicite:53]{index=53} :contentReference[oaicite:54]{index=54}

### C3 — needs_scope_extension
Arbitrer la fermeture des sorties moteur suivantes :
- `ACTION_PLAN_SHORT_DIAGNOSTIC_TASK`
- `ACTION_ESCALATE_PERSISTENT_DRIFT_OFFSESSION`  
Soit elles doivent être ajoutées au voisinage/scope, soit leur statut cross-scope doit être documenté explicitement dans la chaîne learner_state.

## human_actions_to_execute

1. Valider ou corriger le diagnostic suivant :  
   **le vrai problème principal n’est pas la philosophie learner_state, mais la fermeture inter-Core et inter-scope de ses références et actions cibles.**

2. Arbitrer la convention de nommage/référence inter-Core à conserver :
   - Constitution
   - Référentiel
   - Link
   - impact_bundle
   - extracts

3. Si ce diagnostic est validé, passer à `STAGE_02_ARBITRAGE` avec focalisation prioritaire sur :
   - normalisation des références inter-Core
   - fermeture du voisinage logique
   - non-extension silencieuse du scope

## scope_status_declared_for_major_findings

- R1 / C1 : `in_scope`
- R2 / C3 : `needs_scope_extension`
- R3 / C2 : `in_scope`
