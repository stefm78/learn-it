# CHALLENGE REPORT — Constitution / Référentiel / LINK
## Pipeline: constitution | Stage: 01_CHALLENGE
## Date: 2026-03-31

---

## Résumé exécutif

Le système Constitution V1.8 / Référentiel V0.6 / LINK V1.8__V0.6 présente une architecture
de gouvernance solide et bien structurée. Cependant, l'audit adversarial identifie plusieurs
zones de risque non négligeables, notamment des **dépendances IA implicites masquées**,
des **états moteur potentiellement indéfinis** sur les axes activation/VC, une **charge
cognitive élevée** du modèle MSC AND strict, et quelques **incohérences de placement**
entre Constitution et Référentiel. Aucun cycle de dépendance explicite n'est détecté.
La gouvernance patch est bien protégée.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

**1.1 — Contradiction de version dans les références inter-Core**

- `CORE_LEARNIT_REFERENTIEL_V0_6` contient `REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL`
  avec `human_readable: "Référence explicite vers le Core Constitution Learn-it v1.7"`
  → La version citée en human_readable est **v1.7** mais le Core cible est **v1.8**.
- Symétrie : `CORE_LEARNIT_CONSTITUTION_V1_8` contient
  `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION` avec
  `human_readable: "Référence explicite vers le Core Référentiel Learn-it v0.6"` → OK.
- Le LINK pointe vers `LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_8` avec
  `human_readable: "Référence explicite vers le Core Constitution Learn-it v1.7"` → **v1.7 encore**.
- **Risque : incohérence de version dans les labels human_readable**. Pas bloquant au plan
  logique (les ids sont corrects), mais constitue une dette documentaire qui peut induire
  en erreur un auditeur ou un outil de validation automatique.

**1.2 — Bindings manquants dans le LINK**

- Le LINK ne documente **aucun binding** pour `TYPE_SELF_REPORT_AR_N3`
  (Constitution) ↔ `TYPE_REFERENTIEL_AR_N3_CONFIGURATION` / `PARAM_REFERENTIEL_AR_N3_FREQUENCY_REFERENCE`
  (Référentiel), alors que `TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN` bind AR-N1 et AR-N2
  mais **omet AR-N3** de la chaîne d'autorité signal.
- De même, `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS` modifie le poids
  d'AR-N1 sur signal AR-N3, mais ce binding croisé (AR-N3 → poids AR-N1) n'est pas explicité
  dans le LINK.
- **Risque : fermeture système incomplète sur AR-N3**, opacité de la chaîne de reweighting.

**1.3 — Conflit d'autorité latent sur la révocation post-maîtrise**

- `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION` (Référentiel) introduit
  une distinction rétrogradation courante / révocation post-maîtrise, avec une fenêtre
  temporelle et des répétitions configurées pour la révocation.
- La Constitution (`INV_MSC_AND_STRICT`, `EVENT_MSC_DOWNGRADE`) ne fait aucune mention de
  cette distinction : elle définit uniquement la rétrogradation sur défaillance de P, R ou A.
- **Risque : logique opérationnelle de révocation post-maîtrise introduite dans le Référentiel
  sans ancrage constitutionnel explicite**. Le Référentiel semble avoir absorbé une décision
  de gouvernance qui devrait relever de la Constitution.

**1.4 — Dépendance implicite entre `PARAM_REFERENTIEL_DEGRADATION_FAILURE_COUNT`
et `PARAM_REFERENTIEL_MSC_ROBUSTNESS_DELAY_SHORT`**

- `PARAM_REFERENTIEL_DEGRADATION_FAILURE_COUNT` déclare `depends_on:
  [PARAM_REFERENTIEL_MSC_ROBUSTNESS_DELAY_SHORT]` dans sa logique, mais cette dépendance
  n'est pas explicitée dans un binding LINK.
- **Risque mineur** : couplage opaque, non auditable via le LINK.

**1.5 — Mauvais placement potentiel : `RULE_REFERENTIEL_SYSTEMIC_INVESTIGATION_RUNTIME_BEHAVIOR`**

- Cette règle introduit un "régime minimal et réversible" pendant une investigation systémique,
  incluant "gel des ajustements agressifs" et "journalisation renforcée".
- Elle ne dépend que de `REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL` mais n'a **aucun
  ancrage constitutionnel** (aucun TYPE/RULE/INV constitutionnel ne définit la notion
  d'investigation systémique).
- **Risque : logique de gouvernance de crise introduite dans le Référentiel sans
  concept-parent dans la Constitution**.

---

### Axe 2 — Solidité théorique

**2.1 — Charge cognitive du MSC AND strict**

- L'agrégation AND stricte sur P∧R∧A (`INV_MSC_AND_STRICT`) crée une surface de frustration
  élevée pour l'apprenant : un apprenant ayant P=1, R=1 mais A=0.99 est traité identiquement
  à un total débutant.
- La Constitution ne prévoit **aucun état intermédiaire graduable** (ex : "maîtrise partielle",
  "en consolidation") autre que le binaire maîtrisé/non-maîtrisé.
- **Risque théorique modéré** : fort risque de démotivation proche du seuil, notamment pour
  les KU procédurales ou créatives à forte variance.

**2.2 — Modèle émotionnel sous-spécifié**

- `TYPE_STATE_AXIS_ACTIVATION` distingue "productif / détresse / sous-défi" mais la Constitution
  ne définit **aucun mécanisme de réponse différenciée** entre détresse et sous-défi (hormis
  le scaffolding léger de `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1`).
- Le Référentiel délègue la détection au proxy set, mais sans garantir une couverture différenciée
  détresse vs sous-défi.
- **Risque modéré** : un moteur réel risque de traiter détresse et sous-défi de manière
  indistincte, ce qui va à l'encontre des principes de charge émotionnelle/SRL.

**2.3 — Mastery learning : seuil P à 80% non justifié pour tous les types de KU**

- `PARAM_REFERENTIEL_MSC_PRECISION_THRESHOLD` fixe P à 80% (fourchette 70-90%) de manière
  uniforme.
- Aucun différenciateur par type de KU n'est prévu pour P (contrairement à R qui dispose
  de multiplicateurs par type).
- **Risque modéré** : pour les KU créatives ou perceptuelles, un seuil P uniforme à 80%
  peut être théoriquement non pertinent (performance peu répétable sur KU créative).

**2.4 — Métacognition / SRL : AR-N3 sous-connecté**

- AR-N3 est censé produire un "indice de calibration auto-rapport" exploitable par le moteur,
  mais son effet sur l'adaptation fine n'est tracé que dans
  `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`.
- L'effet sur la **trajectoire d'apprentissage** (sélection de contenu, rééquilibrage)
  n'est pas documenté.
- **Risque faible-modéré** : AR-N3 reste un signal dont le périmètre d'action est opaque.

---

### Axe 3 — États indéfinis moteur

**3.1 — Oscillation sur l'axe activation sans AR-N1**

- Si AR-N1 est absent et que les proxys sont insuffisants (< 2 proxys franchissant leur seuil
  : `RULE_REFERENTIEL_ADAPTIVE_REGIME_DETECTION_MIN_PROXIES`), le moteur applique
  `INV_CONSERVATIVE_RULE_WITHOUT_AR_N1` → scaffolding léger réversible.
- Mais si ce scaffolding léger ne résout pas la détresse non détectée, **aucun mécanisme
  d'escalade temporelle n'est prévu** : le moteur peut rester indéfiniment en réponse
  conservatrice sans trigger d'escalade.
- **Risque élevé** : boucle silencieuse sans sortie définie.

**3.2 — État VC non-observable et désactivation non encadrée constitutionnellement**

- `RULE_REFERENTIEL_VC_UNOBSERVABLE_DISABLING` peut désactiver l'axe VC si absent sur
  une fenêtre suffisante.
- La Constitution (`INV_VC_NOT_GENERAL_MOTIVATION_PROXY`) interdit de pénaliser VC basse,
  mais ne prévoit **pas explicitement la désactivation de l'axe**.
- **Risque modéré** : la désactivation référentielle d'un axe constitutionnel n'est pas
  gouvernée au niveau Constitution.

**3.3 — Conflit GF-08 potentiel entre `RULE_REFERENTIEL_INTERLEAVING_CONTENT_REQUIRES_A`
et `INV_MSC_AND_STRICT`**

- L'interleaving de contenus requiert P∧A mais pas nécessairement R.
- Dans la Constitution, la maîtrise de base requiert P∧R∧A.
- Un apprenant peut donc accéder à l'interleaving sans maîtrise de base formelle
  (A atteint, P atteint, R non encore validé).
- **Risque modéré** : incohérence de gouvernance entre condition d'interleaving
  et condition de maîtrise.

**3.4 — Perte d'information lors d'une rétrogradation secondaire déférée**

- `RULE_REFERENTIEL_SECONDARY_RETROGRADATION_DEFERRED_REENTRY` marque et réengage la
  rétrogradation secondaire "au prochain cycle autorisé".
- Mais aucune limite de durée maximale de déférement n'est définie pour les KU marquées
  sans session suffisante (apprenant inactif longtemps).
- En complément, `PARAM_REFERENTIEL_PROPAGATION_CHECK_MAX_DELAY_SESSIONS` fixe "1 session"
  mais si l'apprenant ne revient jamais, **l'état de marquage peut persister indéfiniment**.
- **Risque faible** : dette d'état non nettoyée, mais sans impact fonctionnel immédiat.

---

### Axe 4 — Dépendances IA implicites

**4.1 — Détection de "profil AR-réfractaire" requiert une inférence continue**

- `RULE_REFERENTIEL_AR_REFRACTORY_DETECTION` détecte un profil sur une fenêtre de sessions.
- La notion de "non-réponse" vs "réponse nulle volontaire" vs "absence de trigger" requiert
  **une inférence comportementale continue** qui dépasse la logique purement locale.
- **Risque modéré** : dans un moteur purement local sans IA, cette règle peut produire
  des faux positifs systématiques.

**4.2 — `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` requiert la détection de misconception**

- La Constitution oblige une mission de conflit cognitif si une KU est "flaggée misconception".
- Mais **qui flague la misconception ?** Ce flagging semble supposer une analyse sémantique
  hors-session ou une IA de correction. Aucun mécanisme local de détection n'est décrit.
- **Risque élevé** : dépendance implicite à une IA hors-session ou à une saisie manuelle
  pour que la règle soit applicable.

**4.3 — `TYPE_CORPUS_CONFIDENCE_ICC` non connecté au moteur**

- L'indice de confiance du corpus est déclaré dans la Constitution mais **aucun élément
  du Référentiel ni du LINK ne consomme cet indice** pour influencer une décision moteur.
- **Risque faible** : dead node non exploité, dette de design.

---

### Axe 5 — Gouvernance

**5.1 — Versioning du LINK non aligné sur les labels internes**

- `CORE_LINK` a `version: V1_8__V0_6_FINAL`, ce qui est cohérent avec les versions des
  Core liés. Mais les `human_readable` internes référencent encore "v1.7" (voir Axe 1).
- **Risque faible** : dette documentaire mais pas bloquant.

**5.2 — Patchabilité du LINK**

- Tous les TYPES du LINK ont `patchable: false`. C'est intentionnel selon la règle
  `CONSTRAINT_LINK_NO_BUSINESS_LOGIC`.
- Cependant, en cas de montée de version d'un des Core (ex : Constitution V1.9),
  **le LINK devra être entièrement réécrit** sans procédure de patch disponible.
- **Risque modéré** : rigidité du cycle de release inter-Core.

**5.3 — Absence de procédure formelle de release coordonnée multi-Core**

- La pipeline `STAGE_07_RELEASE_MATERIALIZATION` et `STAGE_08_PROMOTE_CURRENT` s'appliquent
  à un seul Core à la fois.
- En cas de co-évolution Constitution+Référentiel, **aucune procédure de release atomique
  multi-Core n'est documentée**.
- **Risque élevé** : risque d'état de version incohérent si les deux Core sont promus
  dans des cycles distincts.

---

## Risques prioritaires

| Priorité | ID risque | Description | Couche |
|----------|-----------|-------------|--------|
| **Critique** | R-GOV-01 | Release multi-Core non atomique : risque d'incohérence de version Constitution/Référentiel en production | Gouvernance |
| **Élevé** | R-MOT-01 | Boucle silencieuse en absence d'AR-N1 et proxys insuffisants, sans trigger d'escalade | Constitution/Référentiel |
| **Élevé** | R-IA-01 | Flagging misconception supposant une IA ou saisie manuelle non documentée | Constitution |
| **Élevé** | R-LAY-01 | Révocation post-maîtrise introduite dans le Référentiel sans ancrage constitutionnel | Référentiel / Séparation |
| **Modéré** | R-VER-01 | Labels human_readable version v1.7 dans Référentiel et LINK alors que cible est v1.8 | Documentation |
| **Modéré** | R-LINK-01 | AR-N3 absent du binding LINK sur la chaîne de signal autorité | LINK |
| **Modéré** | R-MSC-01 | Seuil P uniforme non différencié par type de KU | Référentiel |
| **Modéré** | R-GOV-02 | Désactivation axe VC par le Référentiel sans autorisation constitutionnelle explicite | Constitution/Référentiel |
| **Modéré** | R-MOT-02 | Interleaving activable sans maîtrise R formelle, incohérent avec AND strict | Référentiel/Constitution |
| **Faible** | R-DEAD-01 | TYPE_CORPUS_CONFIDENCE_ICC non consommé par le moteur | Constitution |
| **Faible** | R-STATE-01 | État de marquage propagation non nettoyé sur inactivité longue | Référentiel |

---

## Corrections à arbitrer avant patch

1. **R-GOV-01** : Définir une procédure de release atomique multi-Core (ex: transaction
   de promotion coordonnée Constitution+Référentiel+LINK), probablement dans STAGE_07/08.

2. **R-MOT-01** : Ajouter dans la Constitution ou le Référentiel un trigger d'escalade
   temporelle pour la boucle conservatrice sans AR-N1/proxys (ex: fenêtre de N sessions
   consécutives en réponse conservatrice → escalade hors-session).

3. **R-IA-01** : Clarifier dans la Constitution la source autorisée de flagging de
   misconception (analyse hors-session, import manuel, ou autre mécanisme). Sinon,
   la règle `RULE_MISCONCEPTION_REQUIRES_COGNITIVE_CONFLICT` reste non déclenchable
   de manière déterministe localement.

4. **R-LAY-01** : Décider si la révocation post-maîtrise est un principe constitutionnel
   (auquel cas : ajouter un TYPE ou INVARIANT dans la Constitution) ou un paramètre
   purement référentiel (auquel cas : documenter explicitement la délégation dans la Constitution).

5. **R-VER-01** : Corriger les labels human_readable dans Référentiel et LINK de "v1.7"
   vers "v1.8".

6. **R-LINK-01** : Ajouter un binding AR-N3 dans `TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN`
   incluant `TYPE_SELF_REPORT_AR_N3` ↔ `TYPE_REFERENTIEL_AR_N3_CONFIGURATION` et la
   règle de reweighting.

7. **R-MSC-01** : Arbitrer si un différenciateur de seuil P par type de KU est pertinent
   (ex: P_créatif < 80%) ou si l'uniformité est un choix délibéré à documenter.

8. **R-GOV-02** : Ajouter dans la Constitution une autorisation explicite de désactivation
   de l'axe VC (ou un invariant contraignant les conditions de désactivation).
