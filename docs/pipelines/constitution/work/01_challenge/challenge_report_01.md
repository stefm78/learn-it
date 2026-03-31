# challenge_report.md

## Résumé exécutif

Le triplet actuel `CORE_LEARNIT_CONSTITUTION_V1_8` / `CORE_LEARNIT_REFERENTIEL_V0_6` / `CORE_LINK_LEARNIT_CONSTITUTION_V1_8__REFERENTIEL_V0_6` est **nettement plus fermé** que les versions antérieures.

Points solides :
- la séparation Constitution / Référentiel / LINK est désormais explicite et globalement cohérente ;
- le LINK contient bien des bindings inter-Core ciblés sur plusieurs zones critiques (`TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN`, `TYPE_BINDING_MSC_COMPONENTS_TO_REFERENTIEL_PARAMETERS`, `TYPE_BINDING_FEEDBACK_COVERAGE_TO_REFERENTIEL_THRESHOLD`, `TYPE_BINDING_PATCH_TRIGGER_GOVERNANCE_CHAIN`) ;
- la Constitution contient maintenant une règle de maintien explicite de l’inconnu (`RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED`), ce qui ferme une partie du risque d’oscillation précédemment visible.

En revanche, le système n’est pas encore entièrement propre ni totalement clos. Les principaux risques restants sont :

1. **Incohérences de versioning sémantique et de narration humaine** : plusieurs descriptions et `human_readable` parlent encore de `v1.7` alors que les IDs et versions sont en `v1.8`.
2. **Conflit potentiel non arbitré dans la chaîne d’autorité des signaux** entre `RULE_AR_N1_OVERRIDES_PROXY` (Constitution) et `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS` (Référentiel).
3. **Bindings encore incomplets sur certaines zones sensibles** : en particulier AR-N2 simplifié, fallback créatif, et certaines escalades patch spécifiques.
4. **Risque de fragilité outillage / release** lié à des conventions inter-Core pas totalement homogènes (`[S17B]` vs `[S17b]`, mentions narratives non synchronisées).
5. **LINK plus robuste qu’avant, mais pas encore assez démonstratif de complétude** : il couvre des chaînes critiques, sans encore prouver explicitement qu’il couvre *toutes* les dépendances inter-Core obligatoires.

Conclusion : **pas de faille critique de structure globale**, mais **deux risques élevés** et plusieurs **risques modérés** justifient un arbitrage avant patch.

---

## Analyse détaillée par axe

### Axe 1 — Cohérence interne

#### 1.1 Versions et cohérence de release

La structure formelle est cohérente :
- `CORE_LEARNIT_CONSTITUTION_V1_8`
- `CORE_LEARNIT_REFERENTIEL_V0_6`
- `CORE_LINK_LEARNIT_CONSTITUTION_V1_8__REFERENTIEL_V0_6`

Les références croisées existent aussi :
- `REF_CORE_LEARNIT_REFERENTIEL_V0_6_IN_CONSTITUTION`
- `REF_CORE_LEARNIT_CONSTITUTION_V1_8_IN_REFERENTIEL`
- `LINK_REF_CORE_LEARNIT_CONSTITUTION_V1_8`
- `LINK_REF_CORE_LEARNIT_REFERENTIEL_V0_6`

Mais plusieurs champs narratifs restent en décalage avec cette réalité :
- la description de `constitution.yaml` parle encore de « Constitution Learn-it v1.7 » ;
- la description de `referentiel.yaml` parle encore de « Constitution Learn-it v1.7 » côté référence ;
- la description de `link.yaml` parle encore de « Constitution Learn-it v1.7 » ;
- plusieurs `human_readable` de références inter-Core gardent la même trace.

**Risque moteur / gouvernance**
- pas un bug métier direct,
- mais un **risque élevé de release auditability** : une version peut être correcte structurellement tout en restant ambiguë pour un humain, pour un reviewer, ou pour un pipeline documentaire.

**Niveau**
- Élevé

#### 1.2 Séparation Constitution / Référentiel / LINK

La frontière des couches est bien mieux tenue qu’avant :
- la Constitution porte invariants, types de régime, règles structurantes et interdits ;
- le Référentiel porte seuils, tables, fenêtres et paramètres opératoires ;
- le LINK rappelle explicitement `CONSTRAINT_LINK_NO_BUSINESS_LOGIC`.

Le binding `TYPE_BINDING_CONSTITUTION_REFERENTIEL_LAYER_SEPARATION` renforce utilement cette frontière.

**Risque restant**
- certains objets référentiels sont très proches d’une gouvernance logique sensible, par exemple :
  - `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`
  - `RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`
  - `TYPE_REFERENTIEL_PATCH_TRIGGER_TABLE`
- ces objets ne sont pas forcément mal placés, mais ils exigent un arbitrage explicite quand ils peuvent infléchir une règle constitutionnelle ou sa lecture.

**Niveau**
- Modéré

#### 1.3 Dépendances implicites restantes

Le LINK couvre désormais plusieurs dépendances fines. C’est un net progrès.

Cependant, tout n’est pas encore explicitement bindé. Exemples notables :
- la Constitution impose `INV_AR_N2_SHORT_FORM_REQUIRES_EXPLICIT_PRIORITY` ;
- le Référentiel expose `TYPE_REFERENTIEL_AR_N2_CONFIGURATION`, `PARAM_REFERENTIEL_AR_N2_MAX_ITEMS`, `PARAM_REFERENTIEL_AR_N2_FREQUENCY_REFERENCE` ;
- il n’existe pas de binding ciblé aussi explicite que pour MSC ou feedback coverage entre cette contrainte constitutionnelle et cette configuration référentielle.

Même logique pour :
- `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH`
- `PARAM_REFERENTIEL_R_MULTIPLIER_CREATIVE_FALLBACK`

**Risque**
- dépendances encore partiellement implicites,
- angle mort de traçabilité lors d’un patch ou d’une release.

**Niveau**
- Élevé

---

### Axe 2 — Solidité théorique

#### 2.1 États apprenant, activation et incertitude

Le système a progressé :
- `TYPE_LEARNER_STATE_MODEL` structure les axes ;
- `TYPE_SELF_REPORT_AR_N1`, `TYPE_SELF_REPORT_AR_N2`, `TYPE_SELF_REPORT_AR_N3` clarifient les sources ;
- `RULE_LEARNER_STATE_AXIS_UNKNOWN_ALLOWED` ferme explicitement le cas où un axe doit rester `unknown/absent/non-observable`.

C’est une amélioration importante par rapport à une architecture qui forcerait toujours une valeur.

**Risque théorique restant**
- la fermeture n’est pas encore parfaite quand il y a arbitrage entre primauté d’AR-N1 et reweighting en cas de calibration AR faible.
- `RULE_AR_N1_OVERRIDES_PROXY` dit clairement que AR-N1 prévaut sur les proxys.
- `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS` dit qu’une calibration AR basse réduit temporairement le poids d’AR-N1 et restaure les proxys.

Il ne suffit pas que le LINK relie ces objets ; il faut aussi savoir **quelle règle gagne** et dans quelles conditions.

**Niveau**
- Élevé

#### 2.2 Mémoire / robustesse / transfert

Le modèle MSC reste conceptuellement solide :
- `INV_MSC_AND_STRICT`
- `INV_TRANSFER_SEPARATE_FROM_BASE_MASTERY`
- composants `P`, `R`, `A`, `T`
- binding inter-Core vers les paramètres référentiels minimaux.

C’est une bonne architecture de séparation entre principe et paramétrage.

**Risque théorique restant**
- le Référentiel introduit des raffinements temporels et des distinctions fines (`RULE_REFERENTIEL_CURRENT_RETROGRADATION_VS_POSTMASTERY_REVOCATION`, multiplicateurs par type de KU), mais le LINK ne prouve pas encore une cartographie exhaustive entre tous ces raffinements et les invariants constitutionnels concernés.

**Niveau**
- Modéré

#### 2.3 Feedback et couverture

Le couple :
- `TYPE_FEEDBACK_COVERAGE_MATRIX`
- `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK`

est bien relié côté LINK à :
- `PARAM_REFERENTIEL_FEEDBACK_COVERAGE_REFERENCE_THRESHOLD`
- `RULE_REFERENTIEL_LOW_FEEDBACK_COVERAGE_SIGNALS_REVISION`
- `EVENT_REFERENTIEL_FEEDBACK_COVERAGE_LOW`

C’est une vraie amélioration de fermeture.

**Risque restant**
- la politique minimale quand une erreur n’est pas couverte est encore surtout portée par le fallback générique ;
- il reste à arbitrer si ce fallback suffit dans tous les cas, notamment pour des KU créatives ou des chemins de feedback dont la déterminisation est difficile.

**Niveau**
- Modéré

---

### Axe 3 — États indéfinis moteur

#### 3.1 Conflit de priorité des signaux

C’est aujourd’hui le point le plus sensible.

Objets concernés :
- `RULE_AR_N1_OVERRIDES_PROXY`
- `TYPE_REFERENTIEL_SIGNAL_CONFIDENCE_HIERARCHY`
- `RULE_REFERENTIEL_SIGNAL_PRECEDENCE_ORDER`
- `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`
- `TYPE_BINDING_LEARNER_STATE_SIGNAL_AUTHORITY_CHAIN`

**État indéfini possible**
- AR-N1 est présent mais jugé peu calibré via AR-N3,
- les proxys deviennent repondérés,
- un conflit survient entre signal auto-rapporté ponctuel et signaux comportementaux convergents,
- la Constitution dit « AR-N1 prime »,
- le Référentiel dit « le poids d’AR-N1 peut être réduit temporairement ».

Sans règle d’arbitrage explicite, le moteur peut :
- osciller,
- produire des décisions différentes selon l’ordre d’évaluation,
- ou masquer le statut d’incertitude au lieu de le conserver.

**Niveau**
- Critique

#### 3.2 AR-N2 simplifié

La Constitution exige :
- `INV_AR_N2_SHORT_FORM_REQUIRES_EXPLICIT_PRIORITY`

Le Référentiel permet :
- un AR-N2 borné en nombre d’items (`PARAM_REFERENTIEL_AR_N2_MAX_ITEMS`),
- un item VC optionnel,
- une fréquence adaptable.

**État indéfini possible**
- AR-N2 est simplifié à 1–2 items,
- VC et intention de retour ne peuvent plus être mesurés ensemble,
- la priorité de mesure n’est pas explicitée dans le chaînage inter-Core.

**Niveau**
- Élevé

#### 3.3 Cas créatifs

La Constitution protège le déploiement autonome des KU créatives via :
- `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH`

Le Référentiel introduit :
- `PARAM_REFERENTIEL_R_MULTIPLIER_CREATIVE_FALLBACK`

**État indéfini possible**
- un fallback temporel existe,
- mais le chemin déterministe de feedback n’est pas explicitement relié à ce fallback,
- ce qui peut laisser croire qu’un fallback paramétrique suffit à lui seul pour autoriser un comportement moteur.

**Niveau**
- Élevé

---

### Axe 4 — Dépendances IA implicites

Le runtime est plus local et plus déterministe qu’avant. Toutefois, certaines zones de conception restent potentiellement dépendantes d’une interprétation sémantique hors modèle.

#### 4.1 KU typing et chemins de feedback

La Constitution impose :
- `INV_KU_TYPING_REQUIRED`
- `INV_MISSING_KU_TYPE_FORCES_SAFE_FALLBACK`
- `TYPE_FEEDBACK_COVERAGE_MATRIX`

Mais le triplet ne prouve pas encore entièrement comment on passe de façon reproductible de :
- type de KU,
- patron d’erreur,
- couverture feedback,
- chemin de feedback déterministe.

**Risque**
- une partie de cette fermeture peut encore résider dans un raisonnement de design externe,
- acceptable hors session,
- mais encore insuffisamment objectivé dans le système canonique.

**Niveau**
- Modéré à élevé

#### 4.2 Patch governance spécialisée

Le binding `TYPE_BINDING_PATCH_TRIGGER_GOVERNANCE_CHAIN` améliore clairement la traçabilité.

Mais il reste générique.

Exemples à risque :
- `INV_PERSISTENT_DRIFT_REQUIRES_ESCALATION_IF_PATCH_BLOCKED`
- `RULE_REFERENTIEL_VC_PATCH_ESCALATION_AFTER_TWO_CYCLES`
- `ACTION_REFERENTIEL_SIGNAL_ANALYSIS_REVISION`

La chaîne spécifique « patch impossible → dérive persistante → escalade d’analyse » existe conceptuellement, mais n’est pas encore reliée par un binding aussi explicite que sur la chaîne signaux ou MSC.

**Niveau**
- Modéré

---

### Axe 5 — Gouvernance

#### 5.1 Qualité de release et auditabilité

Le pipeline est propre, mais la release sémantique n’est pas encore entièrement auto-démonstrative.

Problèmes visibles :
- incohérences de version dans les descriptions ;
- variations de casse dans les anchors (`[S17B]`, `[S17C]` côté LINK versus `[S17b]`, `[S17c]` côté Constitution) ;
- pas de preuve explicite de complétude des bindings obligatoires.

**Risque**
- les outils humains ou automatiques peuvent valider la structure tout en laissant passer des écarts documentaires ou des liaisons implicites.

**Niveau**
- Élevé

#### 5.2 LINK : bon rôle, mais complétude encore implicite

Le LINK a maintenant le bon rôle.

Il ne porte pas de logique métier autonome et il explicite des chaînes utiles.

Mais il n’exprime pas encore clairement :
- une *liste minimale obligatoire* des bindings de fermeture système,
- ni une notion de couverture ou de complétude inter-Core.

**Risque**
- un reviewer peut voir des bindings pertinents sans pouvoir démontrer qu’aucun binding critique ne manque encore.

**Niveau**
- Modéré

---

## Risques prioritaires

### Critique

1. **Conflit d’autorité potentiel dans la résolution des signaux apprenant**  
   Conflit possible entre `RULE_AR_N1_OVERRIDES_PROXY` et `RULE_REFERENTIEL_LOW_AR_CALIBRATION_TEMPORARILY_REWEIGHTS_SIGNALS`, malgré le binding existant. Le système relie les objets mais ne tranche pas encore explicitement leur hiérarchie opérationnelle.

### Élevés

2. **Incohérences de versioning sémantique / human-readable**  
   Le système formel est en `v1.8`, mais plusieurs descriptions restent en `v1.7`, ce qui fragilise la release et l’auditabilité.

3. **Bindings incomplets sur AR-N2 simplifié et cas créatifs**  
   Les contraintes constitutionnelles existent, les paramètres référentiels existent, mais leur liaison explicite reste insuffisante.

4. **Fragilité possible des anchors et des conventions inter-Core**  
   Les variations de casse et de narration peuvent créer des écarts entre structure logique et lecture outillée.

### Modérés

5. **Chaîne d’escalade patch spécifique encore trop générique dans le LINK**

6. **Complétude du LINK non démontrée explicitement**

7. **Fermeture du design feedback encore partiellement externe au Core**

---

## Corrections à arbitrer avant patch

1. **Arbitrer explicitement la hiérarchie opérationnelle entre primauté d’AR-N1 et reweighting en cas de faible calibration AR.**  
   Deux options principales :
   - soit la Constitution garde une primauté stricte d’AR-N1 et le Référentiel ne peut agir que sur l’interprétation de second rang ;
   - soit une exception constitutionnelle bornée est formalisée.

2. **Corriger immédiatement toutes les traces narratives de version encore en `v1.7`** dans les descriptions et `human_readable` inter-Core, sans modifier la logique métier.

3. **Décider s’il faut ajouter des bindings LINK ciblés pour AR-N2 simplifié**, reliant explicitement :
   - `INV_AR_N2_SHORT_FORM_REQUIRES_EXPLICIT_PRIORITY`
   - `TYPE_REFERENTIEL_AR_N2_CONFIGURATION`
   - `PARAM_REFERENTIEL_AR_N2_MAX_ITEMS`
   - et, si nécessaire, l’item VC.

4. **Décider s’il faut ajouter un binding LINK ciblé sur le cas créatif**, reliant explicitement :
   - `INV_CREATIVE_KU_AUTONOMY_REQUIRES_DETERMINISTIC_FEEDBACK_PATH`
   - `PARAM_REFERENTIEL_R_MULTIPLIER_CREATIVE_FALLBACK`
   - et le chemin de feedback déterministe exigé.

5. **Arbitrer si la complétude du LINK doit devenir un objet explicite de release**, par exemple via une petite matrice de bindings obligatoires ou un invariant de couverture inter-Core.

6. **Vérifier et normaliser les `source_anchor` inter-Core**, en particulier sur la casse et les conventions, avant de laisser le pipeline produire un patch de fond.

7. **Arbitrer s’il faut enrichir la chaîne patch governance pour l’escalade spécifique**, afin de relier plus explicitement :
   - patch rejeté ou impossible,
   - dérive persistante,
   - escalade analyse.
