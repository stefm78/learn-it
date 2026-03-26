# Pipeline Core — Input / Output / Contrôles

## Objectif

Ce pipeline sert à faire évoluer des Core YAML de manière contrôlée, traçable, patchable et validable.

Il sépare explicitement :
- l'analyse,
- la décision,
- la synthèse de patch,
- la validation du patch,
- l'application,
- la validation des Core patchés,
- la release.

---

## Vue d'ensemble

```text
[1] Core source
    Input  : Constitution.yaml, Referentiel.yaml, Link.yaml
    Output : base de travail versionnée

[2] Challenge
    Input  : 3 Core + prompt de challenge
    Output : audit structuré

[3] Arbitrage
    Input  : audit structuré
    Output : liste de corrections retenues / rejetées

[4] Synthesis patch
    Input  : 3 Core + audit + arbitrage + prompt patch
    Output : patchset.yaml

[5] Validation patch
    Input  : patchset.yaml + spec Patch DSL
    Output : rapport PASS / FAIL patch-level

[6] Dry-run technique
    Input  : patchset.yaml + Core source + patcher
    Output : rapport d'applicabilité, sans écriture

[7] Apply réel
    Input  : patchset.yaml validé + Core source + patcher
    Output : Core patchés + backups + rapport d'exécution

[8] Validation Core
    Input  : Core patchés + prompt de validation
    Output : rapport PASS / FAIL structurel et logique

[9] Release
    Input  : Core patchés validés + prompt release
    Output : plan de release, bump de version, synchronisation inter-Core
```

---

## Étape 1 — Core source

### Input
- `Constitution_*.yaml`
- `referentiel_*.yaml`
- `link_*.yaml`

### Output
- 3 Core de référence à analyser et patcher

### Contraintes
- fichiers YAML valides
- structure Core reconnue
- versions internes lisibles

### Contrôles
- chargement YAML possible
- présence des sections attendues
- `core_type` cohérent avec le fichier

---

## Étape 2 — Challenge

### Input
- les 3 Core source
- `Challenge_constitution.md`

### Traitement
- audit adversarial
- détection de tensions, contradictions, angles morts, états indéfinis, risques moteur

### Output
- rapport d'audit structuré

### Format de sortie attendu
- texte structuré
- tableaux possibles
- scénarios adversariaux possibles
- recommandations possibles

### Important
Cette étape **n'écrit pas de patch**.
Elle produit un diagnostic.

---

## Étape 3 — Arbitrage

### Input
- rapport d'audit

### Traitement
- décision sur les corrections à retenir
- tri entre :
  - à intégrer
  - à reformuler
  - à rejeter
  - à reporter

### Output
- liste de corrections retenues
- liste des corrections rejetées
- éventuelles priorités d'intégration

### Format conseillé
- liste structurée par Core cible : Constitution / Référentiel / LINK

### Important
Cette étape fixe le périmètre du patch.

---

## Étape 4 — Synthesis patch

### Input
- les 3 Core source
- rapport d'audit
- arbitrage
- `Make05CorePatch_Lot4.md`
- spec `Patch_DSL_v4.md`

### Traitement
- transformation des corrections retenues en patch canonique
- choix des opérations de patch
- minimisation des modifications

### Output
- `patchset.yaml`

### Format de sortie obligatoire
- un unique `PATCH_SET` YAML valide

### Opérations disponibles en v4
- `assert`
- `append`
- `replace`
- `replace_field`
- `remove`
- `rename`
- `append_field_list`
- `remove_field_list_item`
- `move`
- `ensure_exists`
- `ensure_absent`
- `assert_meta`
- `replace_meta_field`
- `rewrite_references`
- `replace_text`
- `note`
- `no_change`

### Contrôles conceptuels
- la correction doit être patchable
- la correction doit viser le bon Core
- pas de logique métier autonome dans le LINK
- pas de doublons d'id

---

## Étape 5 — Validation patch

### Input
- `patchset.yaml`
- `Patch_DSL_v4.md`
- `Make06PatchValidation.md`
- `validate_patchset_v4.py`

### Traitement
- validation formelle du patchset
- vérification des opérations supportées
- vérification de la structure minimale
- détection d'incohérences évidentes

### Output
- rapport PASS / FAIL patch-level

### Contrôles typiques
- `patch_dsl_version` présent
- `atomic` déclaré
- opérations supportées uniquement
- champs obligatoires présents
- sections valides
- cibles correctement décrites

### Important
Cette étape valide **le patch**, pas encore les Core patchés.

---

## Étape 6 — Dry-run technique

### Input
- `patchset.yaml`
- Core source
- `apply_learnit_core_patch_v4.py`

### Traitement
- application en mémoire uniquement
- aucune écriture disque
- simulation complète des opérations
- contrôle des références cassées
- contrôle des suppressions dangereuses

### Output
- journal d'applicabilité
- éventuellement rapport d'exécution YAML
- aucun fichier modifié

### Commande type
```bash
python ./apply_learnit_core_patch_v4.py ./patchset.yaml . true
```

### Rôle
Détecter les erreurs techniques avant écriture réelle.

---

## Étape 7 — Apply réel

### Input
- `patchset.yaml` validé
- Core source
- `apply_learnit_core_patch_v4.py`

### Traitement
- application atomique réelle
- création des backups
- écriture des fichiers patchés
- génération d'un rapport d'exécution si demandé

### Output
- Core patchés
- fichiers `.bak`
- rapport d'exécution optionnel

### Commande type
```bash
python ./apply_learnit_core_patch_v4.py ./patchset.yaml . false ./patch_execution_report.yaml
```

### Contrôles
- si une opération échoue, rien n'est écrit
- les références critiques sont revérifiées avant écriture

---

## Étape 8 — Validation Core

### Input
- Core patchés
- `Make02CoreValidation.md`

### Traitement
- validation structurelle
- validation logique locale
- validation des dépendances
- validation des relations
- validation de la connexité
- validation de la ré-inflation possible

### Output
- rapport PASS / FAIL Core-level

### Contrôles typiques
- aucune règle dupliquée
- aucune dépendance orpheline
- aucune relation implicite
- invariants non patchables
- logique non contradictoire
- `source_anchor` présent
- relations cohérentes
- graphe connexe
- ré-inflation possible

### Important
Ici on valide les **Core résultants**, pas le patch lui-même.

---

## Étape 9 — Release

### Input
- Core patchés validés
- `Make07CoreRelease.md`
- éventuellement rapport d'exécution et rapport de validation

### Traitement
- décision de bump de version
- synchronisation des versions internes
- mise à jour des références inter-Core
- alignement du LINK
- préparation du package de release

### Output
- plan de release
- versions cibles
- renommages nécessaires
- mises à jour de références
- notes de release

### Important
Cette étape est indispensable dès qu'un patch modifie :
- les versions internes,
- les noms de Core,
- les références `REF_CORE_*`,
- les références `LINK_REF_CORE_*`.

---

## Artifacts produits par le pipeline

### Artifacts d'entrée
- `Constitution_*.yaml`
- `referentiel_*.yaml`
- `link_*.yaml`

### Artifacts analytiques
- rapport de challenge
- arbitrage

### Artifacts de patch
- `patchset.yaml`
- rapport de validation de patch
- rapport de dry-run

### Artifacts d'exécution
- Core patchés
- backups `.bak`
- rapport d'exécution YAML

### Artifacts de validation
- rapport de validation Core

### Artifacts de release
- plan de release
- note de version

---

## Distinction fondamentale des sorties

### Challenge
Produit un **diagnostic**.

### Patch
Produit un **artefact d'édition**.

### Validation patch
Produit un **jugement sur la forme et la sécurité du patch**.

### Validation Core
Produit un **jugement sur l'état logique du résultat**.

### Release
Produit un **plan de synchronisation et de versionnement**.

---

## Commandes minimales du pipeline

```bash
# 1. validation formelle du patch
python ./validate_patchset_v4.py ./patchset.yaml

# 2. dry-run
python ./apply_learnit_core_patch_v4.py ./patchset.yaml . true

# 3. apply réel
python ./apply_learnit_core_patch_v4.py ./patchset.yaml . false ./patch_execution_report.yaml
```

Puis :
- validation Core avec `Make02CoreValidation.md`
- release avec `Make07CoreRelease.md`

---

## Pipeline canonique résumé

```text
Core YAML
  -> Challenge_constitution.md
  -> Audit
  -> Arbitrage
  -> Make05CorePatch_Lot4.md
  -> patchset.yaml
  -> validate_patchset_v4.py
  -> dry-run patcher
  -> apply réel
  -> Make02CoreValidation.md
  -> Make07CoreRelease.md
```

---

## Règle d'or

Un pipeline sain doit toujours séparer :
- ce qui **observe**,
- ce qui **décide**,
- ce qui **écrit**,
- ce qui **vérifie**,
- ce qui **publie**.

C'est cette séparation qui rend les Core manipulables par IA sans perdre la gouvernance.
