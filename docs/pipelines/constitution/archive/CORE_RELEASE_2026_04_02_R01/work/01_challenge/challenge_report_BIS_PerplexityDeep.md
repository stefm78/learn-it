# CHALLENGE REPORT — BIS

**ID:** PerplexityDeep
**Pipeline:** constitution
**Stage:** STAGE_01_CHALLENGE
**Date:** 2026-04-01
**Cores analysés:**
- `CORE_LEARNIT_CONSTITUTION_V1_9`
- `CORE_LEARNIT_REFERENTIEL_V1_0`
- `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0`

---

## Résumé exécutif

Le triptyque Constitution / Référentiel / LINK forme un cadre de gouvernance pédagogique solide, avec une séparation des couches globalement bien tenue et des invariants critiques correctement protégés (AND strict MSC, propagation 1-saut, exécution 100 % locale, absence de génération de contenu en usage).

L’audit adversarial met toutefois en évidence plusieurs fragilités qui peuvent dégrader la sûreté du moteur et la lisibilité de sa gouvernance :

1. Des paramètres et références orphelins autour du protocole de divergence MSC-perçu et de la matrice des régimes adaptatifs.
2. Des états moteur mal définis lorsque les axes d’état apprenant restent unknown ou quand plusieurs mécanismes correctifs se déclenchent en parallèle.
3. Des points de friction théoriques sur la charge cognitive inter-session, la remédiation SRL et la distinction valeur / coût dans l’axe VC.
4. Des dépendances IA implicites (détection de misconceptions, évaluation de corpus, qualification de contexte authentique) qui ne sont pas encore complètement ancrées dans des critères déterministes hors session.
5. Des maillons de gouvernance inachevés : escalades non câblées, absence de triggers périodiques de révision et vérification de versioning inter-Core non systématisée.

Les sections suivantes détaillent ces constats selon les axes imposés, puis priorisent les risques et listent les corrections à arbitrer avant tout patch.

---

## Analyse détaillée par axe

---

### Axe 1 — Cohérence interne

#### 1.1 Paramètre de divergence MSC-perçu manquant dans le Référentiel

- **Élément concerné :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` dans la Constitution, qui citent explicitement `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` comme seuil de sessions.
- **Constat :** ce paramètre n’apparaît pas dans le Référentiel v1.0 alors que toute la logique de divergence MSC-perçu s’y réfère pour décider du déclenchement du protocole.
- **Type de problème :** Complétude + implémentabilité.
- **Impact moteur :** en l’état, le moteur ne peut évaluer la condition "divergence persistante sur N sessions" qu’en supposant une valeur implicite non documentée, ou en ne déclenchant jamais l’événement — deux comportements non traçables.
- **Correction à arbitrer :** introduire `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` dans le Référentiel (valeur de référence, fourchette, scope `runtime_evaluation`) et le lier explicitement via le LINK.

---

#### 1.2 Syntaxe de binding LINK hétérogène (`core_ref`)

- **Élément concerné :** `TYPE_BINDING_AR_N3_CALIBRATION_TO_SIGNAL_REWEIGHTING` et, plus largement, les bindings du LINK qui utilisent `core_ref:` dans leurs cibles.
- **Constat :** la plupart des bindings inter-Core ne référencent que des `id:` canoniques, alors que certains ajoutent une clé `core_ref` sans que cette syntaxe ne soit définie dans le DSL ni dans la spec LINK.
- **Type de problème :** Gouvernance + implémentabilité.
- **Impact moteur :** un interpréteur strict du DSL risque d’ignorer ou de rejeter ces cibles non conformes, ce qui casse la traçabilité explicite de certains flux (AR-N3 → calibration → reweighting de signaux).
- **Correction à arbitrer :** soit promouvoir `core_ref` au rang de champ optionnel formel du DSL (avec sémantique claire), soit le retirer et documenter l’appartenance Core via un commentaire ou un schéma externe.

---

#### 1.3 Référence à MOT-01 sans matérialisation Core

- **Élément concerné :** `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` qui fait référence à "MOT-01" comme borne motivationnelle de l’exception au régime conservateur.
- **Constat :** MOT-01 n’existe ni comme TYPE, ni comme RULE, ni comme PARAMETER dans aucun des Cores.
- **Type de problème :** Complétude.
- **Impact moteur :** le texte de la règle repose sur une exception motivée par MOT-01 qui est introuvable dans la base normative ; un implémenteur ne peut pas déterminer quand et comment cette exception s’applique.
- **Correction à arbitrer :** matérialiser MOT-01 (par exemple comme RULE ou PARAMETER référentiel) avec description et scope, ou supprimer cette référence de la règle et adopter une résolution purement conservative.

---

#### 1.4 Invariant AR-N2 court sans mécanisme de vérification

- **Élément concerné :** `INV_AR_N2_SHORT_FORM_REQUIRES_EXPLICIT_PRIORITY` dans la Constitution.
- **Constat :** l’invariant exige une "priorité déclarée et stable" entre VC et intention de retour pour toute version courte d’AR-N2, mais aucun champ, TYPE ou PARAMETER ne porte aujourd’hui cette priorité dans les Cores.
- **Type de problème :** Implémentabilité.
- **Impact moteur :** impossible de contrôler automatiquement qu’un AR-N2 simplifié respecte l’invariant ; la conformité devient purement documentaire.
- **Correction à arbitrer :** définir un conteneur explicite de cette priorité (par exemple un TYPE de configuration AR-N2 enrichi ou un champ dédié dans la configuration référentielle).

---

### Axe 2 — Solidité théorique

#### 2.1 Charge cognitive

- **Point solide :** l’interdiction du texte seul pour les KU procédurales et perceptuelles et l’obligation d’une matrice de feedback pour les KU formelles/procédurales s’alignent bien avec la théorie de la charge cognitive (CLT) en limitant la surcharge perceptive et les artefacts de split-attention.
- **Zone de risque :** la charge intra-session n’est pas plafonnée : aucun invariant ne borne le nombre de KU actives ou la diversité typologique dans une même session, alors même que l’interleaving peut mélanger des contenus de natures différentes.
- **Angle mort :** l’activation de l’interleaving dépend de la composante A et de quelques paramètres référentiels, mais ne tient pas explicitement compte de la charge cognitive totale (par exemple en fonction du mix de types de KU et de la durée cumulée).

#### 2.2 Mémoire et robustesse

- **Point solide :** la composante R repose sur des fenêtres temporelles différenciées par type de KU et sur une logique d’interruption longue bien cadrée.
- **Zone de risque :** le fallback `×1` pour les KU créatives, combiné à des durées de tâches longues, peut conduire à valider R sur la base d’une consolidation relativement superficielle.
- **Angle mort :** aucun mécanisme ne force la re-spatialisation des tentatives réussies d’une même KU sur plusieurs jours dans le cas créatif ; on peut théoriquement satisfaire P, A et R avec une dynamique très concentrée.

#### 2.3 Motivation et valeur-coût

- **Point solide :** l’axe VC et le patch de relevance en cas de VC basse persistante matérialisent une lecture sérieuse de l’expectancy-value.
- **Zone de risque :** la même réponse (patch relevance) est utilisée que la VC basse soit due à un coût perçu trop élevé ou à une valeur perçue trop faible, ce qui risque d’aboutir à des interventions mal ciblées.
- **Angle mort :** aucune articulation explicite avec le vécu d’autonomie (au sens SDT) n’existe dans le modèle d’état apprenant ; l’autonomie n’est traitée qu’au niveau du régime moteur, pas comme besoin psychologique.

#### 2.4 Métacognition / SRL

- **Point solide :** intention de session, AR-N2 et AR-N3 structurent correctement les trois temps SRL (forethought, performance, self-reflection).
- **Zone de risque :** en l’absence chronique d’AR-N2 (non-réponse), l’apprenant ne bénéficie plus d’aucun support de réflexion post-session ; la phase de self-reflection devient optionnelle.
- **Angle mort :** le protocole de divergence MSC-perçu est exploité uniquement comme correctif système ; il pourrait servir de base à un feedback formatif explicite sur la miscalibration, ce qui n’est pas aujourd’hui décrit.

---

### Axe 3 — États indéfinis moteur

#### 3.1 Tous les axes unknown ou non observables

- **Scénario :** AR-N1 absent (profil réfractaire), AR-N2 non complété, AR-N3 non lancé, proxys en-dessous du minimum, VC inobservable.
- **Constat :** `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` autorise l’état unknown, et `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` impose un scaffolding léger, mais aucune règle ne décrit la stratégie de sélection de contenu ni le régime adaptatif dans un état totalement vide de signaux.
- **Type de problème :** États indéfinis + complétude.

#### 3.2 Blocage sur KU créative en régime conservateur

- **Scénario :** une session centrée sur une KU créative, avec AR-N1 absent, VC basse et régime conservateur actif.
- **Constat :** `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH` interdit le déploiement autonome sans chemin de feedback déterministe ; combiné au conservatisme sans AR, le moteur peut se retrouver sans aucun contenu exécutable dans la session.
- **Type de problème :** États indéfinis / blocage moteur.

#### 3.3 Superposition investigation systémique + patch relevance

- **Scénario :** la persistance d’anomalies ouvre une investigation systémique (`RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR`) alors que VC basse déclenche un patch relevance.
- **Constat :** le texte de l’investigation parle de "régime minimal et réversible", sans expliciter si les patchs relevance déjà admissibles sont suspendus, différés ou autorisés dans ce régime.
- **Type de problème :** États indéfinis / gouvernance.

#### 3.4 Expiration de la fenêtre de maîtrise provisoire sans vérification complète

- **Scénario :** plusieurs KU héritent d’une maîtrise provisoire, mais seule une partie est diagnostiquée avant expiration de `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW`.
- **Constat :** aucun EVENT ni RULE ne décrit le sort de ces KU à expiration (maintien, rétrogradation automatique, signal d’alerte).
- **Type de problème :** États indéfinis / complétude.

---

### Axe 4 — Dépendances IA implicites

#### 4.1 Misconceptions

- **Élément :** `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT`.
- **Constat :** la Constitution exige qu’une KU soit flaggée "misconception" pour déclencher un conflit cognitif, mais ne précise pas comment ce flag est déterminé. Toute détection runtime réaliste de misconceptions à partir des erreurs nécessiterait une classification sémantique.
- **Alternative sans IA continue :** restreindre explicitement le flag misconception à la phase Analyse/Design, avec un invariant interdisant toute inférence runtime automatique de ce statut.

#### 4.2 ICC (indice de confiance de corpus)

- **Élément :** `TYPE_CORPUS_CONFIDENCE_ICC`.
- **Constat :** l’ICC est décrit comme un indice global, sans procédure déterministe de calcul. Une estimation réaliste de la qualité du corpus tend à faire intervenir des jugements sémantiques.
- **Alternative sans IA continue :** définir une grille de critères objectifs (fraîcheur, diversité de sources, alignement programme, taux de couverture du référentiel) et une fonction de scoring explicite.

#### 4.3 Contexte authentique

- **Élément :** `TYPE_AUTHENTIC_CONTEXT` et `INV_AUTHENTIC_CONTEXT_REQUIRED_FOR_BLOOM4`.
- **Constat :** le caractère "authentique" du contexte n’est pas opérationnalisé ; il reste implicite et potentiellement dépendant d’une évaluation IA.
- **Alternative sans IA continue :** exiger une description formelle (référence à une situation identifiée, critères de transférabilité, ancrage dans une pratique réelle) et un schéma de validation hors session.

---

### Axe 5 — Gouvernance

#### 5.1 Absence de trigger de révision du graphe

- **Élément :** `TYPE_KNOWLEDGE_GRAPH`.
- **Constat :** le graphe est posé comme structure de référence, mais aucun événement de "vieillissement" ou de révision périodique n’est prévu.
- **Type de problème :** Gouvernance / complétude.
- **Correction à arbitrer :** introduire un EVENT de revue de staleness du graphe avec fenêtre paramétrable dans le Référentiel.

#### 5.2 Escalades incomplètement câblées

- **Élément :** `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`.
- **Constat :** l’invariant exige une escalade hors session mais ne précise ni le canal, ni le destinataire, ni l’artefact cible.
- **Type de problème :** Gouvernance / implémentabilité.
- **Correction à arbitrer :** créer une ACTION d’escalade dédiée, reliée à un schéma d’artefact (log, ticket, file de révision) dans les outils de pipeline.

#### 5.3 Versioning inter-Core et LINK

- **Élément :** `CORE_LINK_LEARNIT_CONSTITUTION_V1_9__REFERENTIEL_V1_0`.
- **Constat :** l’ID du LINK encode les versions, mais aucune règle ne force leur alignement avec `manifest.yaml` et les versions courantes des Cores.
- **Type de problème :** Gouvernance / versioning.
- **Correction à arbitrer :** systématiser la validation inter-Core dans le pipeline (par exemple au STAGE_04 ou STAGE_07) pour bloquer tout run avec LINK désynchronisé.

#### 5.4 Composante T peu gouvernée

- **Élément :** `TYPE_MASTERY_COMPONENT_T`.
- **Constat :** T est non patchable mais paramétrable, sans paramètres référentiels ni contraintes explicites sur cette paramétrisation.
- **Type de problème :** Gouvernance / complétude.
- **Correction à arbitrer :** soit documenter que T doit rester largement qualitative et faiblement paramétrée, soit introduire un petit bloc paramétrique référentiel dédié encadrant ses usages.

---

### Axe 6 — Scénarios adversariaux

#### Scénario A — "Apprenant fantôme AR" sur graphe linéaire

- **Description :** l’apprenant ignore systématiquement AR-N1, AR-N2 et AR-N3 ; les proxys restent sous seuil ; le graphe est linéaire.
- **Mécanismes activés :** détection de profil AR-réfractaire, réponse conservatrice sans AR, éventuellement investigation systémique.
- **Limite révélée :** sans signaux auto-rapportés ni proxys suffisants, le moteur reste durablement en mode conservateur, sans sortie claire. L’exception MOT-01 — pourtant mentionnée — n’étant pas matérialisée, aucune borne motivationnelle explicite ne vient limiter la durée de ce régime.

#### Scénario B — Maîtrise provisoire + interruption longue partiellement couverte

- **Description :** plusieurs KU en maîtrise provisoire, interruption longue, reprise diagnostique partielle.
- **Limite révélée :** les KU non diagnostiquées à temps se retrouvent dans un état indéfini vis-à-vis du MSC, ce qui peut conduire soit à sur-accorder de la maîtrise, soit à sous-estimer la nécessité de remédiation.

#### Scénario C — VC basse persistante + divergence MSC/perçu

- **Description :** l’apprenant signale un blocage fort en AR-N1 et une VC basse persistante alors que le MSC calculé signale une maîtrise de base.
- **Limite révélée :** patch relevance et protocole de divergence peuvent se superposer sans séquencement prioritaire ; selon l’ordre effectif, on peut soit réécrire trop vite le contexte sans traiter une éventuelle miscalibration, soit réviser la trajectoire alors que le problème est essentiellement motivationnel.

---

### Axe 7 — Priorisation

| Priorité | Problème | Couche | Type |
|---|---|---|---|
| Critique | Paramètre MSC-perçu manquant (`PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`) | Référentiel | Complétude / implémentabilité |
| Critique | États totally-unknown non gouvernés (3.1) | Constitution / Référentiel | États indéfinis |
| Critique | Référence MOT-01 orpheline dans la résolution de conflits adaptatifs | Référentiel | Complétude |
| Élevé | Blocage possible sur KU créative en régime conservateur (3.2) | Constitution | États indéfinis |
| Élevé | Escalade de dérive persistent non câblée (5.2) | Constitution | Gouvernance |
| Élevé | Versioning inter-Core non vérifié systématiquement (5.3) | LINK / pipeline | Gouvernance |
| Modéré | Syntaxe `core_ref` non formalisée dans le LINK (1.2) | LINK / DSL | Gouvernance / implémentabilité |
| Modéré | Expiration de maîtrise provisoire sans règle explicite (3.4) | Constitution | États indéfinis |
| Modéré | Superposition investigation systémique / patch relevance (3.3) | Référentiel | Gouvernance |
| Modéré | Dépendance IA implicite sur misconceptions, ICC et contexte authentique | Constitution / Référentiel | Théorique / implémentabilité |
| Modéré | Composante T paramétrable mais peu gouvernée (5.4) | Constitution / Référentiel | Gouvernance |
| Faible | Borne explicite sur la charge cognitive inter-session absente | Constitution / Référentiel | Théorique |
| Faible | Feedback formatif explicite sur divergence MSC-perçu non spécifié | Constitution | Théorique |

---

## Corrections à arbitrer avant patch

### C1 — Compléter le couple Constitution / Référentiel sur la divergence MSC-perçu
- **Action proposée :** ajouter `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` dans le Référentiel et le lier explicitement à `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` via le LINK.
- **Objectif :** rendre le protocole de divergence opérationnel et auditable.

### C2 — Spécifier le comportement moteur en état totalement unknown
- **Action proposée :** introduire une RULE constitutionnelle définissant la stratégie de sélection de KU et le régime adaptatif lorsqu’aucun axe n’est renseigné (par exemple : démarrage par les racines du graphe avec Bloom minimal et durée courte).
- **Objectif :** éviter les blocages silencieux et rendre l’état "premier contact" déterministe.

### C3 — Résoudre le statut de MOT-01
- **Action proposée :** matérialiser MOT-01 comme élément Core ou retirer sa référence de la règle de conflit adaptatif.
- **Objectif :** clarifier les limites motivationnelles du régime conservateur et éviter les zones grises d’interprétation.

### C4 — Normaliser la syntaxe LINK
- **Action proposée :** décider si `core_ref` fait partie du modèle de données LINK. En cas de réponse positive, mettre à jour le Patch DSL et les specs ; sinon, le supprimer des bindings actuels.
- **Objectif :** sécuriser la parsabilité et la robustesse des outils autour du LINK.

### C5 — Fermer les boucles d’escalade et de révision
- **Action proposée :**
  - créer une ACTION d’escalade explicite pour `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` ;
  - introduire un EVENT de revue périodique du graphe de KU ;
  - formaliser, dans le pipeline, une vérification systématique de cohérence de versions entre Cores et LINK.
- **Objectif :** renforcer la gouvernance globale, en particulier sur les dérives lentes et la dette de design.

---

*Fin du rapport — challenge_report_BIS_PerplexityDeep.md*
