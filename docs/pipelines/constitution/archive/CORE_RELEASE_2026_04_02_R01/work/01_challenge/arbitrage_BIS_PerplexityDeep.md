# ARBITRAGE — BIS

**ID arbitrage :** PerplexityDeep  
**Pipeline :** constitution  
**Stage :** STAGE_02_ARBITRAGE  
**Date :** 2026-04-01  
**Scope des entrées :** consolidation des rapports `challenge_report_BIS_*.md` produits par ClaudeThink, ClaudeWoThink, GPTThink, GPTwoThink, Gemini, NemoTron et PerplexityDeep.

---

## 1. Mandat et règle d’arbitrage

- Tous les rapports `challenge_report_BIS_*.md` présents en `docs/pipelines/constitution/work/01_challenge/` ont été pris en compte conformément à la règle de pipeline.
- L’arbitrage vise à :
  - regrouper les constats convergents en un **noyau commun de risques** ;
  - trancher les divergences de lecture ou de sévérité ;
  - qualifier chaque point en **Retenu / Rejeté / Différé / Hors-scope** pour ce run de patch ;
  - produire une base unique pour STAGE_03_PATCH_SYNTHESIS.

Les sections ci-dessous suivent une structure par thèmes plutôt que par agent afin d’éviter les doublons.

---

## 2. Noyau commun — risques convergents

### 2.1 Paramètre de divergence MSC-perçu manquant

**Constat consolidé**  
Plusieurs rapports (ClaudeThink, ClaudeWoThink, GPTThink, PerplexityDeep) identifient l’absence de `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` alors que `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` et `RULE_MSC_PERCEPTION_DIVERGENCE_PROTOCOL` y font référence dans la Constitution.[cite:3][cite:4][cite:5][cite:9]

**Décision : RETENU (Critique)**  
- Créer ce paramètre dans le Référentiel (PARAMETERS) avec :
  - valeur de référence (ordre de grandeur suggéré : 3 sessions consécutives) ;
  - fourchette paramétrable (ex. 2–5) ;
  - source_anchor aligné sur `[ARBITRAGE_2026_04_01][DIVMSC-01]`.
- Lier ce paramètre explicitement à l’événement et à la règle via le LINK au STAGE_03.

---

### 2.2 États moteur totally-unknown non gouvernés

**Constat consolidé**  
GPTThink, NemoTron et PerplexityDeep soulignent que le modèle d’état apprenant autorise `unknown` pour chaque axe, mais ne définit pas de comportement spécifique quand **tous les axes sont unknown ou non observables simultanément** (AR-N1 absent, AR-N2/AR-N3 non renseignés, proxys sous-seuil).[cite:5][cite:8][cite:9]

**Décision : RETENU (Critique)**  
- Introduire en Constitution une règle explicite de démarrage/fallback, du type :
  - sélection prioritaire de KU racines du graphe ;
  - Bloom minimal disponible ;
  - durée de session limitée et planifiée comme "séquence de prise de repères".
- Cette règle devra être paramétrable côté Référentiel (ex. durée de cette phase, nombre maximum de KU).

---

### 2.3 Régime oscillatoire Consolidation ↔ Exploration incomplet

**Constat consolidé**  
ClaudeWoThink, GPTThink, GPTwoThink et Gemini pointent que `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` introduit un régime oscillatoire Consolidation/Exploration dont :
- la notion de "session de consolidation satisfaisante" n’est pas définie ;
- les conditions de sortie sont mal bornées ;
- certains cas de multi-activation (3 régimes ou plus) ne sont pas couverts.[cite:4][cite:5][cite:6][cite:7]

**Décision : RETENU (Élevé)**  
- Conserver le principe d’oscillation mais :
  - définir dans le Référentiel les critères déterministes d’une session de consolidation "satisfaisante" (par ex. au moins un seuil P atteint, ou A ≥ 1 sur la KU cible) ;
  - ajouter un paramètre de **nombre maximal de cycles d’oscillation** avant escalade vers un régime plus conservateur ;
  - clarifier le traitement des cas à 3 régimes actifs simultanément (priorité stricte : Détresse > Conservateur > Oscillation, par exemple).

---

### 2.4 Escalade du mode conservateur et EVENT manquant

**Constat consolidé**  
GPTwoThink, Gemini et NemoTron signalent qu’un paramètre référentiel d’escalade (`PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS`) est défini, mais que l’événement constitutionnel correspondant (`EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION`) n’existe pas à ce stade.[cite:6][cite:7][cite:8]

**Décision : RETENU (Élevé)**  
- Créer en Constitution `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION`, conditionné par ce paramètre.
- Ajouter une règle associée : au déclenchement, escalade formelle vers supervision hors session (ou investigation systémique) avec **trace explicite**.

---

### 2.5 Maîtrise provisoire : fenêtre de vérification sans sortie définie

**Constat consolidé**  
GPTwoThink, Gemini, NemoTron et PerplexityDeep convergent sur le fait que `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` est déclaré mais n’est lié ni à un EVENT ni à une RULE de clôture en cas de non-vérification dans le temps imparti.[cite:6][cite:7][cite:8][cite:9]

**Décision : RETENU (Élevé)**  
- Créer un `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` en Constitution.
- Décider, au patch, d’un comportement par défaut conservateur :
  - soit rétrogradation préventive des KU concernées ;
  - soit bascule en "maîtrise à confirmer" avec obligation de session de diagnostic dédiée.

---

### 2.6 Escalade de dérive persistante non câblée

**Constat consolidé**  
Plusieurs rapports (GPTThink, GPTwoThink, PerplexityDeep, NemoTron) rappellent qu’`INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED` impose une escalade hors session sans définir le canal, le support ni l’action concrète.[cite:5][cite:6][cite:8][cite:9]

**Décision : RETENU (Élevé)**  
- Introduire une `ACTION_ESCALATE_UNRESOLVABLE_DRIFT` en Constitution, avec :
  - cible explicite (artefact de suivi dans le pipeline, ex. ticket, log dédié) ;
  - format minimal de payload (identifiants de KU, contexte de dérive, historique des patchs bloqués).

---

### 2.7 Dépendances IA implicites : misconceptions, ICC, contexte authentique

**Constat consolidé**  
Tous les rapports BIS mentionnent des dépendances IA implicites sur :
- la détection / flaggage des misconceptions ;
- l’estimation de l’ICC (corpus confidence) ;
- la qualification du contexte authentique pour Bloom ≥ 4.[cite:3][cite:4][cite:5][cite:6][cite:7][cite:8][cite:9]

**Décision : RETENU (Modéré)**  
- Ne pas tenter de régler ces points par patch immédiat de logique moteur.
- Cadrer au STAGE_03 un **patch minimal** visant à :
  - rendre explicite que le flag "misconception" est strictement design-time ;
  - transformer ICC et contexte authentique en scores/documentations explicitement remplis hors session, avec une grille d’indicateurs déterministes minimale.
- Différer les raffinements plus fins (ex. outillage d’analyse) à un run ultérieur.

---

## 3. Références orphelines et incohérences de gouvernance

### 3.1 Références à MOT-01

**Constat**  
GPTThink, GPTwoThink, Gemini, NemoTron et PerplexityDeep identifient que MOT-01 est mentionné (notamment dans la gestion de l’exception au régime conservateur) sans exister comme élément formel dans les Cores.[cite:5][cite:6][cite:7][cite:8][cite:9]

**Décision : RETENU (Modéré)**  
- Pour ce run, ne pas créer une nouvelle entité MOT-01 isolée.
- Aligner au STAGE_03 un patch de clarification textuelle dans la règle concernée, en retirant la référence MOT-01 et en exprimant l’exception directement via une condition structurée (par ex. combinaison explicite d’axes apprenant).

---

### 3.2 Syntaxe `core_ref` dans le LINK

**Constat**  
Plusieurs rapports (GPTThink, Gemini, NemoTron, PerplexityDeep) notent que certains bindings LINK utilisent un champ `core_ref` non défini dans la spec, alors que d’autres s’en passent.[cite:5][cite:7][cite:8][cite:9]

**Décision : RETENU (Modéré)**  
- Harmoniser la spec au STAGE_03 :
  - soit promouvoir `core_ref` comme champ optionnel du DSL, avec sémantique claire ;
  - soit le supprimer des bindings existants et maintenir l’info de provenance autrement.
- Décision de détail (choix A/B) à trancher lors de la synthèse de patch, mais la nécessité de normalisation est actée.

---

### 3.3 Désactivation de l’axe VC et autorisation constitutionnelle

**Constat**  
Gemini et NemoTron pointent une référence à `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` dans un paramètre référentiel alors que cette règle n’existe pas dans la Constitution ; d’autres rapports, comme GPTThink et PerplexityDeep, soulignent la tension entre un axe d’état constitutionnel et sa désactivation pilotée par le Référentiel.[cite:5][cite:7][cite:8][cite:9]

**Décision : RETENU (Élevé)**  
- Créer une règle de gouvernance constitutionnelle minimale qui :
  - autorise explicitement la désactivation de l’axe VC dans des conditions bornées (fenêtre de non-observabilité, profil AR-réfractaire, etc.) ;
  - délègue au Référentiel le réglage fin des paramètres (durées, fenêtres) ;
  - est reliée au LINK pour assurer la traçabilité inter-Core.

---

## 4. Points différés ou hors-scope du run

### 4.1 Raffinement complet de la matrice de feedback et des seuils P/R/A

- Plusieurs rapports suggèrent d’affiner les seuils P/R/A par type de KU (ex. distinction créatives vs déclaratives) et de durcir les exigences sur la couverture de feedback.
- **Décision : DIFFÉRÉ**  
  - Le run courant se concentre sur la sûreté moteur et la gouvernance de divergence/états indéfinis.  
  - Ces ajustements, plus fins et potentiellement nombreux, seront traités dans un run dédié orienté calibration pédagogique.

### 4.2 Processus de révision constitutionnelle formel

- GPTwoThink propose de documenter explicitement un processus d’"amendement constitutionnel" pour les invariants non patchables.[cite:6]
- **Décision : DIFFÉRÉ**  
  - Point pertinent mais hors périmètre de patch minimal ; à adresser dans un travail de gouvernance plus large (peut-être au niveau d’un core meta-gouvernance distinct).

---

## 5. Décisions synthétiques par catégorie

### 5.1 Retenu — à adresser au STAGE_03_PATCH_SYNTHESIS

- Créer `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` + binding LINK et mise à jour de la règle de divergence.
- Introduire une règle constitutionnelle de fallback quand tous les axes d’état sont unknown/non observables.
- Compléter le régime oscillatoire Consolidation/Exploration (critère de session satisfaisante, bornes de cycles, résolution des cas multi-régimes).
- Matérialiser `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` et lui associer une règle d’escalade documentée.
- Créer `EVENT_PROVISIONAL_MASTERY_WINDOW_EXPIRED` et décider d’un comportement par défaut (conservateur) sur la maîtrise provisoire non vérifiée.
- Ajouter `ACTION_ESCALATE_UNRESOLVABLE_DRIFT` pour implémenter l’invariant d’escalade en cas de dérive persistante non patchable.
- Clarifier les dépendances IA implicites (misconceptions, ICC, contexte authentique) en les ramenant à des décisions design-time explicites et des critères déterministes minimaux.
- Normaliser la désactivation de l’axe VC via une règle de gouvernance constitutionnelle.
- Normaliser la syntaxe du LINK (champ `core_ref`).

### 5.2 Différé — à documenter mais non patché dans ce run

- Finer-grain sur les seuils P/R/A par type de KU et la matrice de feedback détaillée.
- Processus de révision constitutionnelle complet (au-delà des patchs de ce run).

### 5.3 Rejeté — non retenu pour patch

À ce stade, aucun point identifié par un seul rapport sans écho significatif dans les autres n’est retenu comme candidat de patch prioritaire. Ces observations restent utiles comme bruit de fond pour des runs ultérieurs, mais ne sont pas listées individuellement ici.

---

## 6. Lignes directrices pour STAGE_03_PATCH_SYNTHESIS

- **Priorité 1 :** restaurer la complétude opérationnelle des mécanismes déjà introduits (divergence MSC-perçu, maîtrise provisoire, escalade conservateur, dérive persistante).
- **Priorité 2 :** éliminer les états moteur indéfinis évidents (tout unknown, blocages créatifs, superposition investigation/patch sans séquencement).
- **Priorité 3 :** solidifier la gouvernance (versioning inter-Core, désactivation d’axes, normalisation du LINK) sans modifier la philosophie de base du Core.

Ces priorités guideront la production du patchset YAML au STAGE_03, en cherchant des corrections **minimales mais structurantes**, alignées sur l’intention originelle de la Constitution.
