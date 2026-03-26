# arbitrage.md

## Objet

Arbitrer les corrections à retenir avant synthèse de patch, en distinguant :
- ce qui doit être renforcé dans la Constitution ;
- ce qui doit rester dans le Référentiel ;
- ce qui doit être explicité dans le LINK ;
- ce qui peut être laissé en l’état.

Le principe directeur retenu est conservateur :
- ne pas déplacer inutilement de logique entre couches ;
- fermer les zones d’ambiguïté moteur ;
- renforcer prioritairement les bindings inter-Core et les règles de dégradation explicites.

---

## Décisions d’arbitrage

### ARB_01 — Gestion des signaux contradictoires

**Décision**
- Ne pas remonter toute la logique de pondération dans la Constitution.
- Conserver dans la Constitution le principe d’autorité et d’existence d’états inconnus / absents.
- Conserver dans le Référentiel les pondérations, hiérarchies et reweightings opérationnels.
- Renforcer le LINK pour binder explicitement :
  - `TYPE_STATE_AXIS_ACTIVATION`
  - `TYPE_STATE_AXIS_VALUE_COST`
  - `TYPE_SELF_REPORT_AR_N1`
  - `TYPE_SELF_REPORT_AR_N2`
  - `TYPE_SELF_REPORT_AR_N3`
  avec la hiérarchie de confiance et la règle de reweighting temporaire.

**Justification**
La Constitution porte déjà l’existence du modèle d’état apprenant et l’autorité de `AR-N1` sur l’axe activation, tandis que le Référentiel porte déjà une hiérarchie de confiance des signaux ainsi qu’une règle explicite de reweighting quand la calibration AR est basse. Il est donc plus cohérent de fermer la chaîne par binding que de dupliquer la logique dans la Constitution. :contentReference[oaicite:1]{index=1}

**Effet attendu**
- fermeture plus nette des cas “absent / contradictoire / bruité” ;
- séparation des couches préservée ;
- meilleure auditabilité inter-Core.

**Action patch à préparer**
- Ajouter un binding LINK explicite “learner state signal authority chain”.
- Ajouter, côté Constitution ou LINK selon granularité disponible, une explicitation du fait qu’un axe peut rester `unknown` plutôt que d’être forcé.

**Priorité**
- Critique

---

### ARB_02 — MSC et délégation paramétrique au Référentiel

**Décision**
- Ne pas modifier la logique constitutionnelle du MSC.
- Renforcer le LINK pour binder explicitement les composantes `P`, `R`, `A` vers leurs paramètres référentiels minimaux obligatoires.

**Justification**
La Constitution déclare déjà que `P`, `R` et `A` dépendent du Référentiel, et le Référentiel pose explicitement qu’il ne peut pas modifier la logique AND du MSC, uniquement ses seuils et paramètres. Le problème est donc moins un problème de fond qu’un problème de traçabilité inter-Core. :contentReference[oaicite:2]{index=2}

**Effet attendu**
- traçabilité explicite composant → paramètre ;
- réduction des dépendances implicites ;
- meilleure base pour validation release.

**Action patch à préparer**
- Ajouter dans le LINK un binding minimal pour :
  - `TYPE_MASTERY_COMPONENT_P` ↔ seuils de précision ;
  - `TYPE_MASTERY_COMPONENT_R` ↔ délais / multiplicateurs R ;
  - `TYPE_MASTERY_COMPONENT_A` ↔ seuils d’autonomie.

**Priorité**
- Élevée

---

### ARB_03 — Couverture feedback et politique de dégradation

**Décision**
- Conserver dans la Constitution l’exigence d’une matrice de couverture feedback.
- Conserver dans le Référentiel le seuil de référence de couverture.
- Renforcer la fermeture système par une politique minimale explicite de dégradation :
  - feedback générique autorisé en fallback ;
  - mais obligation de signaler l’insuffisance de couverture comme dette de design ;
  - interdiction d’interprétation libre non bornée au runtime.

**Justification**
La Constitution déclare déjà la `TYPE_FEEDBACK_COVERAGE_MATRIX` et la rattache à `RULE_UNCOVERED_ERROR_GENERIC_FEEDBACK`, tandis que le Référentiel porte un seuil de couverture de référence à 70%. Le bon arbitrage est donc de rendre le fallback explicite et borné, pas de changer de couche. :contentReference[oaicite:3]{index=3}

**Effet attendu**
- fermeture claire en cas d’erreur non couverte ;
- maintien de la contrainte “moteur local” ;
- limitation de la tentation d’inférence sémantique implicite.

**Action patch à préparer**
- Renforcer la règle de fallback générique ou son binding.
- Ajouter dans le LINK un binding :
  - `TYPE_FEEDBACK_COVERAGE_MATRIX`
  - seuil référentiel de couverture
  - événement ou condition de “low coverage”.

**Priorité**
- Élevée

---

### ARB_04 — Statut du `creative fallback`

**Décision**
- Conserver le `creative fallback` dans le Référentiel.
- Le traiter comme **fallback borné et explicitement non extensible par défaut**, pas comme une logique ouverte.
- Demander un binding LINK ou une note référentielle plus explicite indiquant quand ce fallback s’applique.

**Justification**
Le Référentiel fixe déjà un invariant fort : `INV_REFERENTIEL_CREATIVE_R_FALLBACK_IS_X1`, ce qui montre que ce fallback n’est pas actuellement laissé à l’interprétation libre. Le risque principal n’est donc pas son existence, mais le manque d’explicitation de ses conditions d’usage dans la fédération inter-Core. :contentReference[oaicite:4]{index=4}

**Effet attendu**
- maintien d’une solution simple ;
- meilleure lisibilité du statut “cas borné” plutôt que “zone grise ouverte”.

**Action patch à préparer**
- Ajouter soit un binding LINK, soit un renforcement du `human_readable`/`logic.condition` référentiel pour expliciter l’usage admissible du fallback créatif.

**Priorité**
- Modérée

---

### ARB_05 — Gouvernance des patch triggers

**Décision**
- Laisser les seuils et tables de déclenchement côté Référentiel.
- Ne pas remonter les valeurs ou la taxonomie détaillée des triggers dans la Constitution.
- En revanche, renforcer dans le LINK la chaîne :
  - métrique observée ;
  - seuil référentiel ;
  - trigger de patch ;
  - admissibilité constitutionnelle du patch artifact.

**Justification**
La Constitution porte déjà `TYPE_PATCH_ARTIFACT` et les invariants de validité locale et de rejet des patchs invalides. Le Référentiel porte déjà des paramètres de persistance VC basse et de cycles avant escalade analyse. La séparation des couches est donc bonne ; ce qui manque surtout est l’explicitation de la chaîne d’autorité entre elles. :contentReference[oaicite:5]{index=5}

**Effet attendu**
- gouvernance de patch plus auditable ;
- moins d’ambiguïté entre “simple alerte” et “motif de patch”.

**Action patch à préparer**
- Ajouter au LINK un binding “patch trigger governance chain”.
- Vérifier qu’aucun trigger opérationnel n’empiète sur un invariant constitutionnel non patchable.

**Priorité**
- Élevée

---

### ARB_06 — Release closure et preuve de fermeture

**Décision**
- Conserver la cohérence de version actuelle.
- Ajouter une exigence de validation plus explicite sous forme de bindings minimaux obligatoires, sans créer une nouvelle couche.

**Justification**
Le pipeline prévoit déjà une séquence propre challenge → arbitrage → patch → validation → apply → core validation → release plan, et interdit toute modification directe de `current/`. La faiblesse restante est donc la preuve sémantique de fermeture, pas la gouvernance procédurale. :contentReference[oaicite:6]{index=6}

**Effet attendu**
- release candidate plus facile à auditer ;
- validation plus robuste au-delà de la simple cohérence de version.

**Action patch à préparer**
- Étendre le LINK avec un petit noyau de bindings “obligatoires à la fermeture système”.

**Priorité**
- Modérée à élevée

---

## Arbitrages retenus pour patch synthesis

### À patcher en priorité

1. **LINK**
   - bindings explicites sur :
     - signaux état apprenant ;
     - composantes MSC ↔ paramètres référentiels ;
     - couverture feedback ↔ seuil ↔ fallback ;
     - patch triggers ↔ patch artifact.

2. **Constitution**
   - seulement si nécessaire, explicitation minimale du statut `unknown` / `absent` pour les axes d’état afin d’éviter tout forçage implicite.

3. **Référentiel**
   - garder la logique opérationnelle existante ;
   - éventuellement clarifier les conditions d’usage du fallback créatif ;
   - ne pas déplacer de logique constitutionnelle ici.

---

## Arbitrages explicitement rejetés

### REJ_01 — Remonter toute la hiérarchie de signaux dans la Constitution
Rejeté, car cela ferait dériver la Constitution vers une couche trop opérationnelle alors que le Référentiel contient déjà ce matériau. :contentReference[oaicite:7]{index=7}

### REJ_02 — Supprimer le `creative fallback`
Rejeté à ce stade, car le fallback est déjà borné par invariant (`×1`) ; le problème porte davantage sur son binding et sa lisibilité que sur sa simple existence. :contentReference[oaicite:8]{index=8}

### REJ_03 — Déplacer les seuils de patch trigger dans la Constitution
Rejeté, car la Constitution doit gouverner l’admissibilité et les invariants de patch, non les seuils opérationnels eux-mêmes. :contentReference[oaicite:9]{index=9}

---

## Cadre de synthèse pour la phase 3

La synthèse de patch devra suivre ce cap :

- **Patch minimaliste**
  - priorité au LINK ;
  - éviter tout déplacement massif d’objets entre Core.

- **Patch de fermeture**
  - supprimer les dépendances implicites critiques ;
  - expliciter les chaînes d’autorité inter-Core.

- **Patch compatible release**
  - aucun changement direct dans `current/` ;
  - tout ajout doit rester ré-inflatable et auditable dans les validations ultérieures. :contentReference[oaicite:10]{index=10}

---

## Arbitrage global

**Décision globale**
- Le système n’appelle pas une refonte.
- Il appelle un **patch de fermeture inter-Core**, principalement sur le LINK, avec un éventuel micro-renfort Constitution sur la gestion explicite des états inconnus.

**Impact attendu**
- réduction nette des ambiguïtés moteur ;
- meilleure gouvernance de patch ;
- meilleure préparabilité de la release.