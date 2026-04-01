# ARBITRAGE — Constitution pipeline

```yaml
stage: STAGE_02_ARBITRAGE
pipeline: constitution
date: 2026-04-01
inputs:
  - challenge_report.md
  - challenge_report_01.md
  - challenge_report_02.md
  - challenge_report_03.md
  - challenge_report_04.md
  - challenge_report_05.md
  - challenge_report_07.md
human_arbitrage_notes: "oui — séance d'arbitrage humain complète du 2026-03-31 au 2026-04-01"
```

---

## Résumé exécutif

7 rapports de challenge consolidés. 8 runs Perplexity + 1 run ChatGPT utilisés comme base comparative pour établir le consensus.

Sur l'ensemble des constats identifiés :
- **corriger_maintenant** : 14 points
- **reporter** : 3 points
- **rejeter** : 2 points
- **hors_perimetre** : 1 point

Les corrections immédiates couvrent :
- la désynchronisation de versioning (convergence totale des 7 rapports)
- les conflits d'autorité signal AR-N1 / reweighting AR-N3
- les états moteur critiques (maîtrise provisoire, boucle conservatrice, LINK absent)
- les points de séparation des couches (révocation post-maîtrise, investigation systémique)
- les angles morts de gouvernance (VC unknown, désactivation axe VC, flagging misconception)
- les lacunes de binding inter-Core (AR3-01, LINK-02)
- les comportements non déterministes sur les cas de frontière de la matrice des régimes adaptatifs (MATRIX-01, DIVMSC-01)

---

## Périmètre analysé

### Fichiers de challenge considérés
- `challenge_report.md` (run non numéroté, 2026-03-31)
- `challenge_report_01.md` (run 01, 2026-03-31)
- `challenge_report_02.md` (run 02, 2026-03-31)
- `challenge_report_03.md` (run 03, 2026-03-31)
- `challenge_report_04.md` (run 04, 2026-03-31)
- `challenge_report_05.md` (run 05, 2026-03-31)
- `challenge_report_07.md` (run 07, 2026-03-31)

### Notes humaines d'arbitrage
Séance d'arbitrage humain complète — 2026-03-31 au 2026-04-01.
Décisions prises par arbitrage humain explicite sur tous les points contestés ou à préciser.
Aucune décision n'est automatiquement héritée d'un run de challenge.

### Limites de périmètre
- GOV-01 (release multi-Core atomique) : hors périmètre — relevant des STAGE_07 / STAGE_08.
- SRL-01 (feedback SRL inter-bilans AR-N3) : reporté — chantier de design pédagogique distinct.
- BIND-AR2 (bindings AR-N2 créatifs) : reporté — patch LINK dédié à planifier.

---

## Points consolidés

### Regroupements effectués
- `VER-01` : fusion de 6 occurrences de désynchronisation `human_readable` v1.7 → v1.8 sur `referentiel.yaml`, `link.yaml`, `constitution.yaml`.
- `SIG-01` : fusion R-MOT-01 (run 00) + critique run 01 + point 3.2 run 07 — même conflit `RULE_LEARN_AR_N1_OVERRIDES_PROXY` vs `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`.
- `MOT-01` : fusion run 00, run 03, run 07 — boucle conservatrice sans sortie définie.
- `PROV-01` : fusion run 03, run 05, run 07 — maîtrise provisoire sans événement d'expiration.
- `AR3-01` : fusion runs 00, 01, 02, 03, 07 — AR-N3 orphelin constitutionnel.
- `MISC-01` (IA-01) : fusion runs 00, 02, 05, 07 — flagging misconception sans source définie.
- `MATRIX-01` : porté par run 04 uniquement, retenu sans fusion.
- `DIVMSC-01` : porté par run 04 uniquement, retenu sans fusion.

### Contradictions résolues
- **SIG-01** : run 05 et ChatGPT recommandaient de reporter. Décision humaine : corriger maintenant avec exception constitutionnelle bornée (option a).
- **SYST-01** : divergence entre option trigger humain (ChatGPT, run 05) et trigger automatique (autres runs). Décision humaine : trigger automatique + bilan AR-N3 guidé obligatoire avec l'apprenant.
- **GOV-02** : ChatGPT et run 05 recommandaient de reporter. Décision humaine : corriger maintenant, fenêtre paramétrable (Curseur 1-B), réversibilité immédiate (Curseur 2-i).

---

## Arbitrage détaillé

---

### Point VER-01 — Désynchronisation labels `human_readable` v1.7 → v1.8

- **Source(s) :** runs 00, 01, 02, 03, 05, 07 (6/7)
- **Constat synthétique :** Les champs `human_readable` de `REF_CORE_LEARN_IT_CONSTITUTION_V1.8_IN_REFERENTIEL` (`referentiel.yaml`) et `LINK_REF_CORE_LEARN_IT_CONSTITUTION_V1.8` (`link.yaml`), ainsi que les descriptions générales des trois Cores, mentionnent encore v1.7 alors que l'ID et la version cible sont V1.8.
- **Nature :** éditoriale — versioning, traçabilité
- **Gravité :** élevée
- **Impact :** auditabilité, validation automatique de fédération non déterministe, release ambigu
- **Décision :** `corriger_maintenant`
- **Justification :** convergence de 6 rapports sur 7, correction minimale sans impact logique, bloquante pour la traçabilité de release.
- **Conséquence attendue pour l'étape patch :** remplacer `v1.7` par `v1.8` dans les champs `human_readable` concernés de `referentiel.yaml` et `link.yaml`, et dans les descriptions générales des trois Cores si elles le mentionnent. Patch `replace_text` ou `replace_field` ciblé.

---

### Point SIG-01 — Conflit autorité AR-N1 vs reweighting calibration AR-N3

- **Source(s) :** runs 00 (R-MOT-01), 01 (critique), 07 (3.2 critique)
- **Constat synthétique :** `RULE_LEARN_AR_N1_OVERRIDES_PROXY` (Constitution) établit la primauté d'AR-N1. `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS` (Référentiel) réduit temporairement le poids d'AR-N1 quand AR-N3 détecte une mauvaise calibration. Le LINK documente le binding mais ne tranche pas la hiérarchie opérationnelle en cas de conflit simultané. Résolution non déterministe selon l'ordre d'évaluation.
- **Nature :** logique — cohérence inter-couches, état moteur
- **Gravité :** critique
- **Impact :** décisions moteur oscillantes, opacité de la résolution de conflit
- **Décision :** `corriger_maintenant`
- **Justification :** risque critique convergent. Décision humaine : option (a) — exception constitutionnelle bornée. AR-N1 garde la primauté formelle. Le reweighting Référentiel s'applique uniquement si AR-N3 confirme une faible calibration sur N bilans consécutifs (N paramétrable dans le Référentiel).
- **Conséquence attendue pour l'étape patch :** amender `TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN` dans le LINK pour inclure une clause de précédence explicite : *"AR-N1 prime, sauf si AR-N3 confirme calibration faible sur N bilans consécutifs, auquel cas le reweighting Référentiel s'applique."* Si ce binding est `patchable: false`, la correction passe par la Constitution : ajout d'une exception bornée à `RULE_LEARN_AR_N1_OVERRIDES_PROXY`.

---

### Point MOT-01 — Boucle conservatrice silencieuse sans AR-N1 et sans proxy

- **Source(s) :** runs 00 (R-MOT-01), 03 (modéré), 07 (critique 3.2)
- **Constat synthétique :** En absence d'AR-N1 ET si moins de 2 proxys franchissent leur seuil, `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` s'applique mais aucun mécanisme d'escalade temporelle n'est défini. Le moteur peut rester indéfiniment en mode conservateur sans signal d'anomalie.
- **Nature :** état moteur — gouvernance, complétude
- **Gravité :** critique
- **Impact :** stabilité système, expérience apprenant, absence de sortie définie de la boucle
- **Décision :** `corriger_maintenant`
- **Justification :** convergence de 3 rapports. État sans sortie explicite = risque opérationnel.
- **Conséquence attendue pour l'étape patch :** ajouter dans la Constitution ou le Référentiel un paramètre `PARAM_REFERENTIEL_CONSERVATIVE_SCAFFOLDING_ESCALATION_SESSIONS` et une règle associée déclenchant une escalade (ex : notification hors-session, trigger investigation systémique) si le mode conservateur persiste au-delà de la fenêtre définie sans résolution.

---

### Point PROV-01 — Maîtrise provisoire : expiration sans comportement défini

- **Source(s) :** runs 03 (élevé), 05 (critique R-03 indirect), 07 (critique 3.1)
- **Constat synthétique :** `PARAM_PROVISIONAL_MASTERY_VERIFICATION_WINDOW` déclare une fenêtre de vérification mais aucun EVENT ni règle ne définit le comportement à l'expiration si la vérification n'a pas eu lieu. État de maîtrise potentiellement indéfini.
- **Nature :** état moteur — complétude
- **Gravité :** critique
- **Impact :** stabilité système, oscillation possible de l'état de maîtrise
- **Décision :** `corriger_maintenant`
- **Justification :** convergence de 3 rapports sur un état sans sortie définie. Décision humaine : option (b) — marquage "à vérifier" + reprise diagnostique obligatoire à la session suivante (pas de révocation automatique à l'expiration).
- **Conséquence attendue pour l'étape patch :** ajouter `EVENT_PROVISIONAL_MASTERY_VERIFICATION_EXPIRED` dans la Constitution avec une règle associée : à l'expiration, l'état de maîtrise est marqué `to_verify` (non révoqué), et une reprise diagnostique est obligatoirement déclenchée à la session suivante.

---

### Point LAY-01 — Révocation post-maîtrise sans ancrage constitutionnel

- **Source(s) :** runs 00 (R-LAY-01), 01 (modéré)
- **Constat synthétique :** `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POST_MASTERY_REVOCATION` introduit une logique de révocation post-maîtrise dans le Référentiel. La Constitution ne définit pas ce principe : aucun TYPE ni INVARIANT ne l'ancre constitutionnellement.
- **Nature :** gouvernance — séparation des couches
- **Gravité :** élevée
- **Impact :** cohérence gouvernance, logique opérationnelle absorbée par le Référentiel sans autorisation constitutionnelle
- **Décision :** `corriger_maintenant`
- **Justification :** le principe de révocation post-maîtrise est une décision de gouvernance qui doit être ancré constitutionnellement, ou la délégation doit être explicitement documentée.
- **Conséquence attendue pour l'étape patch :** ajouter dans la Constitution un `TYPE_POST_MASTERY_REVOCATION` ou un invariant déclarant que la révocation post-maîtrise est une extension de `INV_MSC_AND_STRICT` déléguée au Référentiel pour ses paramètres. Patch minimal.

---

### Point IA-01 — Flagging `misconception` non opérationnalisé

- **Source(s) :** runs 00, 02, 05, 07
- **Constat synthétique :** Une règle se déclenche si une KU est marquée `misconception: true`, mais aucun Core ne définit qui pose ce marquage. L'hypothèse implicite est une IA externe ou une saisie hors-système — non contractualisée, incompatible avec `INV_NO_RUNTIME_CONTENT_GENERATION`.
- **Nature :** logique — complétude opérationnelle
- **Gravité :** élevée
- **Impact :** règle jamais déclenchable de façon déterministe, risque de dérive silencieuse si une inférence automatique est ajoutée plus tard
- **Décision :** `corriger_maintenant`
- **Justification :** le marquage `misconception: true` doit être déclaré explicitement comme un attribut posé par le concepteur de contenu au moment du design, jamais inféré en runtime.
- **Conséquence attendue pour l'étape patch :** ajouter dans la Constitution ou le Référentiel une déclaration explicite : `misconception: true` est un attribut éditorial posé lors du design de la KU. Aucune inférence runtime n'est autorisée. Compatible avec `INV_NO_RUNTIME_CONTENT_GENERATION`.

---

### Point AR3-01 — AR-N3 absent de la hiérarchie de précédence des signaux

- **Source(s) :** runs 00, 01, 02, 03, 07
- **Constat synthétique :** `TYPE_SELF_REPORT_AR_N3` alimente `TYPE_STATE_AXIS_CALIBRATION` mais est absent de `RULE_REFERENTIEL_SIGNAL_PRECEDENCE_ORDER` et `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY`. Son effet sur la trajectoire n'est pas documenté dans la chaîne de signaux. Orphelin constitutionnel de fait.
- **Nature :** cohérence interne — binding LINK, traçabilité
- **Gravité :** modérée
- **Impact :** opacité de la chaîne de reweighting, angle mort d'auditabilité, risque de patch AR-N3 sans voir l'impact sur AR-N1
- **Décision :** `corriger_maintenant`
- **Justification :** convergence de 5 rapports. Correction purement documentaire et de binding.
- **Conséquence attendue pour l'étape patch :** intégrer AR-N3 dans `RULE_REFERENTIEL_SIGNAL_PRECEDENCE_ORDER` et `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY`. Ajouter un binding LINK documentant le lien AR-N3 → reweighting AR-N1. Pas de changement de logique.

---

### Point LINK-01 — Comportement moteur non spécifié si LINK absent ou corrompu

- **Source(s) :** run 03 (critique)
- **Constat synthétique :** Aucun invariant ne définit le comportement système si le LINK est absent, corrompu ou non chargé. Pas d'EVENT ni de règle de blocage. Fonctionnement en mode dégradé silencieux possible.
- **Nature :** gouvernance — contrat système, état critique
- **Gravité :** critique
- **Impact :** sécurité logique, fonctionnement sans contrat inter-Core
- **Décision :** `corriger_maintenant`
- **Justification :** risque critique retenu sur un seul rapport mais sans contre-argument dans les autres. Correction minimaliste possible.
- **Conséquence attendue pour l'étape patch :** ajout d'un `INV_LINK_REQUIRED_FOR_INTER_CORE_OPERATION` dans la Constitution, avec un `EVENT_LINK_MISSING_OR_CORRUPTED` associé et une action bloquante (chargement sans LINK = état bloquant).

---

### Point VC-01 — VC `unknown` indistinguable de VC basse persistante

- **Source(s) :** runs 02, 05
- **Constat synthétique :** `EVENT_PERSISTENT_LOW_VC` peut se déclencher si VC est `unknown`, confondu avec un état VC bas observé. Les deux états ont une sémantique radicalement différente : absence de donnée vs donnée basse confirmée.
- **Nature :** logique — état moteur, complétude
- **Gravité :** élevée
- **Impact :** faux positifs répétés, patch de pertinence déclenché sans raison valide
- **Décision :** `corriger_maintenant`
- **Justification :** correction minimaliste, impact direct sur la fiabilité du moteur. Décision humaine confirmée.
- **Conséquence attendue pour l'étape patch :** ajouter une règle ou invariant : `VC unknown` ne déclenche pas `EVENT_PERSISTENT_LOW_VC`. Seul `VC low observée` (valeur mesurée et confirmée basse) peut le déclencher. Patch `add_rule` ou `add_invariant` ciblé.

---

### Point GOV-02 — Désactivation axe VC sans autorisation constitutionnelle

- **Source(s) :** runs 00, 01, 03, 07
- **Constat synthétique :** Le Référentiel peut désactiver l'axe VC si aucune valeur observable n'a été produite. La Constitution interdit de pénaliser une VC basse mais ne mentionne pas la désactivation complète de l'axe. Asymétrie de gouvernance.
- **Nature :** gouvernance — séparation des couches
- **Gravité :** élevée
- **Impact :** désactivation unilatérale d'un axe sans fondement constitutionnel, incohérence latente
- **Décision :** `corriger_maintenant`
- **Justification :** décision humaine. Formulation retenue : le Référentiel est autorisé à désactiver l'axe VC si aucune valeur observable n'a été produite sur une **fenêtre consécutive paramétrable** (Curseur 1-B). La désactivation est **réversible dès réapparition d'une valeur observable** à la session suivante (Curseur 2-i).
- **Conséquence attendue pour l'étape patch :** ajouter dans la Constitution une autorisation explicite : *"Le Référentiel est autorisé à désactiver l'axe VC si aucune valeur observable n'a été produite sur une fenêtre consécutive définie dans ses paramètres (`PARAM_VC_UNOBSERVABLE_WINDOW_BEFORE_AXIS_DEACTIVATION`). La désactivation est réversible dès réapparition d'une valeur observable."*

---

### Point SYST-01 — Investigation systémique sans trigger défini

- **Source(s) :** runs 00 (placement `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION`), 07
- **Constat synthétique :** Un mode "investigation systémique" est décrit dans le Référentiel mais aucun trigger ne l'ouvre. Aucun EVENT, aucune condition d'entrée. Le mode existe mais est inatteignable de façon traçable.
- **Nature :** gouvernance — complétude, état moteur
- **Gravité :** élevée
- **Impact :** mode existant mais jamais activé, risque d'implémentation autonome non contractualisée ultérieure
- **Décision :** `corriger_maintenant`
- **Justification :** décision humaine. Option retenue : **trigger automatique sur seuils paramétrés + bilan AR-N3 guidé obligatoire avec l'apprenant** pour ouvrir l'investigation.
  - Calibrage retenu : **2 signaux simultanés en anomalie pendant 3 sessions consécutives**.
  - Signaux candidats : (1) divergence AR-N1 vs MSC persistante, (2) mode conservateur actif sans sortie, (3) VC inobservable, (4) maîtrise provisoire expirée non résolue.
  - À l'ouverture : séquence bilan AR-N3 guidé obligatoire (3 questions ciblées : VC, AR-N1, MSC perçu). Résultats intégrés comme bilan AR-N3 de référence.
  - Condition de fermeture : bilan complété ET au moins 2 des 4 signaux anomaliques revenus à l'état normal.
- **Conséquence attendue pour l'étape patch :** ajouter `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` dans la Constitution. Ajouter `PARAM_SYSTEMIC_INVESTIGATION_TRIGGER_CONDITIONS` dans le Référentiel (seuil : 2 signaux / 3 sessions). Ajouter une règle prescrivant le bilan AR-N3 guidé obligatoire en ouverture d'investigation. Ajouter les conditions de fermeture.

---

### Point MATRIX-01 — Cellules de frontière de la matrice des régimes adaptatifs non spécifiées

- **Source(s) :** run 04 uniquement
- **Constat synthétique :** La matrice des régimes adaptatifs (3×3 ou plus) ne définit pas le comportement du moteur quand deux régimes sont simultanément déclenchés sur des cellules de frontière. Comportement non déterministe selon l'ordre d'évaluation.
- **Nature :** logique — état moteur, complétude pédagogique
- **Gravité :** élevée
- **Impact :** régime pédagogique non déterministe sur les cas de frontière, expérience apprenant incohérente
- **Décision :** `corriger_maintenant`
- **Justification :** retenu sur un seul rapport mais sans contre-argument. Décision humaine : option (C) — table de priorité par paire de conflits. Table spécifiée ci-dessous.
- **Conséquence attendue pour l'étape patch :** ajouter dans le Référentiel une `RULE_REFERENTIEL_ADAPTIVE_REGIME_CONFLICT_RESOLUTION` implémentant la table de priorité suivante :

  | Conflit | Régime prioritaire | Règle |
  |---|---|---|
  | Détresse + Sous-défi | **Détresse** | Soutien émotionnel avant défi intellectuel |
  | Détresse + Exploration | **Détresse** | Stabiliser avant d'explorer |
  | Détresse + Consolidation | **Détresse** | Réduire la pression avant de consolider |
  | Conservateur + Sous-défi | **Conservateur** (borné par MOT-01) | Pas de challenge sans AR actif ; escalade si dépassement seuil MOT-01 |
  | Conservateur + Exploration | **Conservateur** | Pas d'exploration sans données AR suffisantes |
  | Consolidation + Sous-défi | **Sous-défi** | L'ennui pendant la consolidation la rend contre-productive |
  | Consolidation + Exploration | **Oscillatoire** | Régime oscillatoire : une session consolidation satisfaisante (R progresse) → une session exploration → retour consolidation. Sortie du cycle quand R est atteint. |
  | Sous-défi + Exploration | **Exploration** | Résolution naturelle du sous-défi |

  Règle synthétique : (1) la Détresse l'emporte toujours. (2) En l'absence de Détresse, le Conservateur l'emporte sur Exploration et Consolidation, sauf dépassement du seuil MOT-01. (3) La Consolidation l'emporte sur le Sous-défi sauf si R est déjà atteint. (4) L'Exploration l'emporte sur le Sous-défi. (5) Consolidation vs Exploration → régime oscillatoire piloté par la progression de R.

---

### Point DIVMSC-01 — Divergence MSC calculé vs état perçu AR-N1 discordant persistant

- **Source(s) :** run 04 uniquement
- **Constat synthétique :** Un apprenant peut avoir atteint techniquement le seuil de maîtrise calculé (P×R×A validés) tout en signalant un blocage total persistant via AR-N1. Ces deux états coexistent sans résolution. Aucun EVENT ne capture cette tension. Le moteur continue d'adapter normalement malgré des données fondamentalement contradictoires.
- **Nature :** logique — état moteur, expérience apprenant
- **Gravité :** élevée
- **Impact :** expérience apprenant profondément incohérente, risque de désengagement, aucune remontée d'anomalie
- **Décision :** `corriger_maintenant`
- **Justification :** retenu sur un seul rapport mais sans contre-argument. Décision humaine : option (b) → (a) — d'abord retour en phase diagnostique, si divergence persiste → escalade design.
- **Conséquence attendue pour l'étape patch :** ajouter `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` dans la Constitution. Ajouter dans le Référentiel `PARAM_MSC_PERCEPTION_DIVERGENCE_THRESHOLD` (nombre de sessions de divergence avant déclenchement). À l'atteinte du seuil : (1) retour obligatoire en phase diagnostique ciblée (révision de la notion supposément maîtrisée). Si la divergence persiste après la phase diagnostique : (2) escalade vers révision du design du contenu (notification externe).

---

## Décisions à transmettre au patch

Liste par ordre de priorité pour la synthèse de patch :

| Priorité | Point | Core(s) concerné(s) | Nature du patch |
|---|---|---|---|
| 1 | VER-01 | `referentiel.yaml`, `link.yaml`, `constitution.yaml` | `replace_text` / `replace_field` |
| 2 | LINK-01 | `constitution.yaml` | `add_invariant`, `add_event` |
| 3 | SIG-01 | `link.yaml` ou `constitution.yaml` | `add_clause` binding ou `add_exception` |
| 4 | MOT-01 | `constitution.yaml` ou `referentiel.yaml` | `add_param`, `add_rule` |
| 5 | PROV-01 | `constitution.yaml` | `add_event`, `add_rule` |
| 6 | VC-01 | `constitution.yaml` ou `referentiel.yaml` | `add_rule` ou `add_invariant` |
| 7 | GOV-02 | `constitution.yaml` + `referentiel.yaml` | `add_authorization`, `add_param` |
| 8 | SYST-01 | `constitution.yaml` + `referentiel.yaml` | `add_event`, `add_param`, `add_rule` |
| 9 | LAY-01 | `constitution.yaml` | `add_type` ou `add_invariant` |
| 10 | IA-01 | `constitution.yaml` ou `referentiel.yaml` | `add_declaration` |
| 11 | AR3-01 | `link.yaml`, `referentiel.yaml` | `add_binding`, `update_rule` |
| 12 | MATRIX-01 | `referentiel.yaml` | `add_rule` (table de priorité) |
| 13 | DIVMSC-01 | `constitution.yaml` + `referentiel.yaml` | `add_event`, `add_param`, `add_rule` |

### Contraintes de minimalité à respecter
- Aucun changement de logique pédagogique fondamentale non décidé explicitement.
- Toute correction dans la Constitution doit rester à portée minimale : ajout borné, pas de réécriture de sections entières.
- Les paramétrisations (seuils, fenêtres, N bilans) doivent toujours rester dans le Référentiel, jamais codées en dur dans la Constitution.
- Le LINK doit documenter tout nouveau binding inter-Core introduit par ce patch.

---

## Décisions explicitement non retenues

### Points reportés

| Point | Justification du report |
|---|---|
| **GOV-01** — Release multi-Core non atomique | Hors périmètre de ce patch. Relève des STAGE_07 / STAGE_08. Risque accepté : désynchronisation de versions lors de releases séparées. |
| **BIND-AR2** — Bindings AR-N2 simplifiés + cas créatifs | Non bloquant pour le moteur actuel. Reporter à un patch LINK dédié. |
| **SRL-01** — Phase forethought planification pré-session (SRL inter-AR-N3) | Chantier de design pédagogique distinct, trop large pour ce patch. Couverture SRL incomplète détectable mais non bloquante. |

### Points rejetés

| Point | Justification du rejet |
|---|---|
| **T-01** — Composante T sans trigger / binding / paramètre | Unanimement absent des rapports de challenge principaux ou classé hors-périmètre dans les runs qui le mentionnent. Aucune convergence suffisante pour un patch immédiat. |
| **A-01** — Composante A binaire (autonomie guidée vs complète) | Portée par 2 runs uniquement avec une formulation non convergente. Insuffisant pour constituer un point d'arbitrage actionnable à ce stade. |
