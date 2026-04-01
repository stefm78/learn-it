# CHALLENGE REPORT — Constitution CORE_LEARNIT_CONSTITUTION_V1_9
<!-- stage: STAGE_01_CHALLENGE -->
<!-- source_core: CORE_LEARNIT_CONSTITUTION_V1_9 -->
<!-- date: 2026-04-01 -->
<!-- auditor_role: adversarial_core_auditor -->

---

## Résumé exécutif

La Constitution V1_9_FINAL est structurellement solide et bien plus mûre que ses versions antérieures. Le naming est normalisé, la fermeture locale est assurée et les références inter-Core sont explicitement matérialisées. Cependant, l'audit adversarial révèle **sept zones de fragilité significatives** distribuées sur les axes de cohérence interne, solidité théorique, états indéfinis moteur, dépendances IA implicites et gouvernance. Deux risques sont classés **critiques**, trois **élevés**, deux **modérés**.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

**1.1 — Binding `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` → `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` : dépendance non réciproque**

La RULE `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` déclare `depends_on: [EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED]` mais l'EVENT ne déclare la RULE que via `relations.triggers`. La relation est unidirectionnelle dans la logique, ce qui est conforme à la convention, mais le `source_anchor` `[ARBITRAGE_2026_04_01][DIVMSC-01]` sur les deux éléments laisse entendre qu'ils ont été co-introduits par patch dans un cycle récent. Si un futur patch retire ou renomme l'EVENT sans vérifier la RULE, le moteur disposera d'une règle orpheline déclenchée par un événement inexistant. **Risque : modéré.**

**1.2 — Composantes MSC P, R, A : dépendances sur `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION` sans contrainte de version explicite**

Les composantes `TYPE_MASTERY_COMPONENT_P`, `TYPE_MASTERY_COMPONENT_R` et `TYPE_MASTERY_COMPONENT_A` dépendent toutes du type de référence inter-Core `REF_CORE_LEARNIT_REFERENTIEL_V1_0_IN_CONSTITUTION`. Ce type de référence est déclaré `patchable: false` et `parameterizable: false`, ce qui est protecteur. Cependant, la Constitution ne documente aucune contrainte de compatibilité de version inter-Core : si le Référentiel est promu en V1_1 ou V2_0, rien dans la Constitution n'exige une vérification explicite de compatibilité avant usage. Ce comportement est un **binding implicite de version**. **Risque : élevé.**

**1.3 — `TYPE_INTEGRITY_MODES` : dépendance circulaire implicite via `TYPE_SESSION_INTEGRITY_SCORE`**

`TYPE_INTEGRITY_MODES` déclare `depends_on: [TYPE_SESSION_INTEGRITY_SCORE]`. Or `TYPE_SESSION_INTEGRITY_SCORE` valide `TYPE_NC_MSC` qui lui-même dépend de `TYPE_SESSION_INTEGRITY_SCORE`. Il n'y a pas de cycle strict dans le YAML, mais la logique sémantique crée une boucle d'évaluation : le mode d'intégrité conditionne le score d'intégrité qui conditionne le niveau de confiance MSC qui influence les décisions du moteur qui déterminent le contexte du mode d'intégrité. Ce n'est pas un cycle YAML interdit, mais c'est un **état oscillant potentiel au niveau moteur**. **Risque : élevé.**

---

### Axe 2 — Solidité théorique

**2.1 — Absence de protocole de récupération pour la détresse persistante (axe Activation)**

La Constitution gère la détresse via `TYPE_STATE_AXIS_ACTIVATION` et l'invariant `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`. La réponse conservatrice est : scaffolding léger réversible. Cependant, aucun élément constitutionnel ne prévoit d'escalade si la détresse est **persistante sur N sessions consécutives** malgré le scaffolding. Le protocole `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` couvre la divergence MSC/perçu, mais la détresse activation n'est pas couverte au même niveau. Il y a une asymétrie de traitement : la divergence perçue est escaladée, la détresse émotionnelle chronique ne l'est pas. **Risque : élevé. Ancré en [S7][S11].**

**2.2 — `TYPE_MASTERY_COMPONENT_T` (transférabilité) : absence de contrainte de délai minimal**

La composante T est séparée de la maîtrise de base (`INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`) et ne constitue pas un prérequis inverse. Mais la Constitution ne contraint pas de fenêtre temporelle minimale entre l'acquisition de la maîtrise de base et la tentative d'évaluation de T. Un moteur pourrait théoriquement évaluer T immédiatement après P×R×A, sans consolidation mémorielle, ce qui contredit les fondements de la science de l'apprentissage (transfert requis après stabilisation). **Risque : modéré. Ancré en [S17b][S20].**

---

### Axe 3 — États indéfinis moteur

**3.1 — État `unknown` des axes learner state : règle de priorité inter-axes manquante**

`RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise explicitement qu'un axe reste `unknown`. Mais la Constitution ne définit pas de règle de **priorité ou de traitement combiné** lorsque plusieurs axes sont simultanément `unknown` (ex : Activation = unknown ET VC = unknown EN MÊME TEMPS). Dans ce cas, le moteur dispose de deux règles conservatrices indépendantes (`INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` pour Activation, VC inconnue pour Value-Cost) mais aucune règle ne couvre la **combinaison multi-axe unknown**. Le comportement composite est indéfini. **Risque : critique. Ancré en [S7][S11][PATCH_V1_9__STAGE03].**

**3.2 — `INV_MSC_AND_STRICT` : comportement non défini si l'une des composantes est `unknown` (non calculée)**

L'invariant AND strict sur P, R, A suppose que les trois composantes sont calculables. La Constitution protège l'évaluation via `INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK`, mais ce fallback couvre uniquement les KU sans type. Si une composante (ex : R, robustesse temporelle) est **non observable** faute de données temporelles (ex : première session, apprenant nouveau), le moteur ne peut pas satisfaire la condition AND. La Constitution ne définit pas si le résultat est : `mastery = false`, `mastery = unknown`, ou `mastery = deferred`. Ce comportement indéfini peut provoquer des oscillations de trajectoire. **Risque : critique. Ancré en [S17b][S20].**

---

### Axe 4 — Dépendances IA implicites

**4.1 — Détection de `misconception` dans `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT`**

La règle déclare : *"KU flaggée misconception → mission de conflit cognitif obligatoire."* Mais le flagging de misconception sur une KU requiert une inférence sémantique lors de la phase d'analyse. La Constitution ne précise pas si ce flag est : (a) posé par un humain lors du design, (b) inféré automatiquement par un outil d'analyse off-session, ou (c) détecté dynamiquement en runtime. Si (c), cela viole `INV_NO_RUNTIME_CONTENT_GENERATION` et `INV_RUNTIME_FULLY_LOCAL`. Le scope `design_runtime` du RULE laisse entendre les deux cas, ce qui est ambigu. **Risque : élevé. Ancré en [S3][S18].**

---

### Axe 5 — Gouvernance

**5.1 — Absence de politique de rétrocompatibilité du LINK dans la Constitution**

La Constitution déclare la séparation Constitution/Référentiel (`INV_CONSTITUTION_REFERENTIAL_SEPARATION`) mais ne mentionne pas le Core LINK comme entité soumise à des règles constitutionnelles de gouvernance. Le LINK est pourtant utilisé comme input de pipeline et ses bindings inter-Core peuvent être modifiés. La Constitution ne protège pas contre : une modification du LINK qui introduirait une logique métier autonome, ni contre une désynchronisation entre le LINK et la Constitution suite à un patch sélectif. **Risque : modéré. Ancré en [S1].**

---

## Risques prioritaires

| Priorité | ID de risque | Élément ancré | Description synthétique |
|----------|---|---|---|
| **CRITIQUE** | RISK-01 | `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` `[S7][S11]` | Comportement composite indéfini si plusieurs axes learner state sont simultanément unknown |
| **CRITIQUE** | RISK-02 | `INV_MSC_AND_STRICT` `[S17b][S20]` | Comportement indéfini du AND strict si une composante MSC est non-calculable (ex : R en première session) |
| **ÉLEVÉ** | RISK-03 | `TYPE_MASTERY_COMPONENT_P/R/A` `[S20]` | Binding inter-Core implicite de version : aucune contrainte de compatibilité Constitution→Référentiel lors d'une promotion de version |
| **ÉLEVÉ** | RISK-04 | `TYPE_INTEGRITY_MODES` `[S15]` | Boucle sémantique mode intégrité → SIS → NC-MSC → décisions moteur → contexte mode |
| **ÉLEVÉ** | RISK-05 | `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` `[S3][S18]` | Ambiguïté du scope `design_runtime` : le flagging de misconception peut impliquer une inférence runtime interdite |
| **ÉLEVÉ** | RISK-06 | Axe Activation détresse persistante `[S7][S11]` | Absence de protocole d'escalade constitutionnel pour la détresse chronique multi-sessions |
| **MODÉRÉ** | RISK-07 | `TYPE_MASTERY_COMPONENT_T` `[S17b]` | Absence de fenêtre temporelle minimale entre maîtrise de base et évaluation de T |
| **MODÉRÉ** | RISK-08 | `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` `[ARBITRAGE_2026_04_01]` | Risque de règle orpheline si l'EVENT est retiré sans vérification des RULE dépendantes |
| **MODÉRÉ** | RISK-09 | LINK absent de la Constitution `[S1]` | Absence de politique constitutionnelle de gouvernance du LINK |

---

## Corrections à arbitrer avant patch

1. **[RISK-01] — Définir la règle de traitement composite multi-axe unknown** : Ajouter une règle ou un invariant constitutionnel précisant le comportement du moteur lorsque ≥2 axes de l'état apprenant sont simultanément `unknown`. La réponse conservatrice maximale devrait être définie explicitement.

2. **[RISK-02] — Définir l'état MSC en cas de composante non calculable** : Préciser dans `INV_MSC_AND_STRICT` ou dans un invariant complémentaire que si une composante P, R ou A est `unknown` (non calculable), la maîtrise est `deferred` (ou `false` selon le choix d'arbitrage) et non un état indéterminé. Cela couvre notamment les premières sessions sans historique temporel.

3. **[RISK-03] — Introduire une contrainte de compatibilité de version inter-Core** : Ajouter un invariant ou une contrainte constitutionnelle stipulant qu'une promotion du Référentiel à une nouvelle version majeure requiert une validation explicite de compatibilité avec la Constitution avant activation.

4. **[RISK-05] — Clarifier le scope du flagging misconception** : Préciser dans `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` et/ou dans `TYPE_KNOWLEDGE_UNIT` que le flag `misconception` est exclusivement un attribut posé en phase design ou par outillage off-session — jamais inféré en runtime.

5. **[RISK-06] — Protocole d'escalade pour la détresse activation chronique** : Par symétrie avec `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL`, définir un mécanisme constitutionnel d'escalade lorsque l'axe Activation reste en détresse sur N sessions consécutives malgré le scaffolding conservateur.

6. **[RISK-04 / RISK-09] — À évaluer en arbitrage** : La boucle sémantique intégrité et l'absence de gouvernance LINK sont des risques modérés à élevés ; leur correction pourrait impliquer une restructuration significative. À trancher en arbitrage avant patch.
