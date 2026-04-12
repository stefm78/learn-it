# J3 — reconstruction canonique à partir de résultats bornés intégrés

## Objet

J2 a clarifié la prochaine marche de modularisation côté lecture :
réduire la surface de lecture effective des runs bornés.

Mais la modularisation ne sera réellement robuste que si elle devient **bidirectionnelle** :

1. **décomposition** du canon vers des scopes et des runs bornés ;
2. **reconstruction** du canon à partir de résultats locaux intégrés et validés.

Ce document définit donc le prochain incrément structurel :

**la mécanique déterministe de reconstruction des fichiers Core canoniques à partir de résultats de pipeline bornés, après intégration globale explicite.**

---

## Problème exact

Tant que les pipelines bornés ne servent qu'à :
- challenger localement ;
- arbitrer localement ;
- patcher localement ;
- valider localement ;

sans mécanisme explicite de reconstruction canonique, la modularisation reste incomplète.

On dispose alors :
- d'une meilleure gouvernance locale ;
- d'un meilleur parallélisme ;
- d'une meilleure focalisation ;

mais pas encore d'une **chaîne complète et déterministe de retour vers le canon publié**.

---

## Décision structurante

La transformation adopte la règle suivante :

**les résultats bruts de pipeline ne reconstruisent jamais directement les Core canoniques.**

La reconstruction canonique doit consommer :
- uniquement des artefacts structurés ;
- déjà validés localement ;
- explicitement intégrés dans une décision globale ;
- sérialisables de manière stable.

Autrement dit :
- pas de reconstruction directe à partir d'un challenge report ;
- pas de reconstruction directe à partir d'un arbitrage narratif ;
- pas de reconstruction directe à partir d'un texte libre produit par une IA.

---

## Chaîne cible

### A. Canon publié
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

### B. Décomposition / travail borné
- catalogue de scopes ;
- runs bornés ;
- challenge / arbitrage / patch / validation locale.

### C. Résultats locaux normalisés
Les pipelines produisent des résultats locaux, mais ceux-ci doivent être traduits en une forme intégrable.

### D. Intégration globale
Une étape explicite décide quels résultats locaux entrent dans l'état intégré.

### E. Reconstruction canonique
Un mécanisme déterministe reconstruit les fichiers Core canoniques complets.

---

## Distinction structurante

Il faut désormais séparer quatre niveaux.

### 1. Traces de travail de pipeline
Exemples :
- `challenge_report*.md`
- `arbitrage.md`
- rapports de validation
- reports de stage

Ces artefacts sont utiles pour le raisonnement, l'audit et la traçabilité.
Ils ne doivent pas être les entrées directes du reconstructeur canonique.

### 2. Deltas locaux structurés
Exemples :
- patchset validé ;
- décision `no_patch` ;
- demande d'extension de scope ;
- classification d'impact hors scope ;
- validation locale de cohérence.

Ces artefacts commencent à être exploitables par une intégration globale.

### 3. Résultat intégré global
C'est la forme canonique que le reconstructeur doit consommer.

Elle doit exprimer de manière stable :
- ce qui est accepté ;
- ce qui est rejeté ;
- ce qui est différé ;
- ce qui modifie effectivement les Core ;
- ce qui reste bloqué par gate.

### 4. Canon reconstruit
Sortie déterministe :
- Core complets ;
- ordre stable ;
- références stables ;
- fingerprint stable.

---

## Entrée autorisée du reconstructeur

La reconstruction canonique ne doit pas consommer directement les artefacts narratifs.

Elle doit consommer un artefact explicite du type :
- `integrated_scoped_changeset`
- ou équivalent

Cet artefact doit au minimum porter :
- la version/fingerprint du canon source ;
- la liste des runs considérés ;
- la liste des changements retenus ;
- les collisions résolues ;
- les changements exclus ;
- les invariants à rejouer ;
- le statut d'intégration global.

---

## Reconstruction déterministe

Le reconstructeur canonique doit pouvoir :

1. lire le canon source gouverné ;
2. lire l'artefact d'intégration structuré ;
3. appliquer les changements retenus dans un ordre stable ;
4. régénérer les fichiers Core complets ;
5. recalculer les références et fingerprints attendus ;
6. produire un résultat strictement reproductible à entrée égale.

---

## Invariants de round-trip

La mécanique aller-retour doit respecter au minimum :

1. **pas de perte silencieuse d'IDs**
2. **pas de duplication silencieuse d'IDs**
3. **pas de dérive silencieuse de références**
4. **ordre stable de sérialisation**
5. **sortie identique si aucun changement logique retenu**
6. **reconstruction identique pour les mêmes entrées intégrées**
7. **traçabilité du canon source et du canon reconstruit**

---

## Rôle de l'intégration globale

La reconstruction ne doit pas contourner le `integration_gate`.

Au contraire, elle doit arriver **après** :
- relecture globale des invariants ;
- validation des références croisées ;
- résolution des collisions entre runs ;
- arbitrage explicite sur les extensions de scope ;
- décision d'intégration.

Donc la séquence correcte est :

1. succès local du run ;
2. gate global ;
3. artefact intégré ;
4. reconstruction canonique.

---

## Lien avec les runs bornés

Un run borné peut produire :
- un patch valide ;
- un patch localement accepté ;
- un `no_patch` utile ;
- une alerte `needs_scope_extension` ;
- un constat de collision potentielle.

Mais aucun de ces résultats ne doit être interprété seul comme un ordre implicite de modification du canon.

Le run fournit une contribution ;
l'intégration globale décide ;
le reconstructeur matérialise.

---

## Strict nécessaire recommandé

J3 ne doit pas introduire immédiatement un compilateur complet de production.

Le strict nécessaire est :

1. **documenter le contrat de reconstruction canonique** ;
2. **définir un artefact intermédiaire structuré** consommable par un reconstructeur ;
3. **définir les invariants de round-trip** ;
4. **préparer un futur script déterministe** de reconstruction ;
5. **garder la promotion explicite et centralisée**.

---

## Proposition de séquence d'implémentation

### Étape 1 — niveau transformation
Documenter J3 et définir le template de l'artefact intégré.

### Étape 2 — niveau validation
Définir les checks minimaux du reconstructeur :
- source fingerprint attendu ;
- runs intégrés autorisés ;
- collisions résolues ;
- invariants globaux rejoués.

### Étape 3 — niveau outillage
Créer un script déterministe capable de :
- prendre un canon source + un `integrated_scoped_changeset` ;
- reconstruire les Core complets ;
- produire un fingerprint et un rapport.

### Étape 4 — niveau pipeline
Brancher cette reconstruction dans le chemin release/promotion, sans casser les garde-fous existants.

---

## Bénéfices attendus

1. Modularisation réellement bidirectionnelle.
2. Meilleure sûreté du retour vers le canon.
3. Rejouabilité de la chaîne complète.
4. Réduction du risque qu'une IA réécrive le canon de manière ad hoc.
5. Préparation d'une future compilation canonique déterministe.

---

## Garde-fous

1. Le reconstructeur ne consomme pas de texte libre comme entrée primaire.
2. Le canon reconstruit reste une sortie déterministe, pas une synthèse narrative.
3. La reconstruction arrive après intégration globale, jamais à la place de celle-ci.
4. La promotion de `current/` reste un acte explicite.
5. Les traces de pipeline restent auditables mais séparées des artefacts d'intégration.

---

## Décision structurante de J3

Le chantier adopte la règle suivante :

**la modularisation doit devenir bidirectionnelle : extraction déterministe du canon vers des unités de travail bornées, puis reconstruction déterministe du canon à partir de résultats intégrés et validés.**

C'est cette mécanique aller-retour gouvernée qui permettra de faire de la modularisation autre chose qu'un simple mode local de travail.
