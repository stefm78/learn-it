# tmp

Répertoire temporaire du repo.

## Usage prévu

- y déposer des fichiers patch générés ponctuellement ;
- y conserver des scripts ou rapports de travail transitoires ;
- télécharger, tester ou appliquer localement des artefacts non canoniques ;
- servir de zone de passage pendant une discussion IA / humain.

## Convention

- contenu non canonique ;
- pas destiné à structurer durablement le repo ;
- peut être vidé, remplacé ou régénéré à tout moment ;
- les fichiers importants doivent être promus vers `docs/`, `docs/patcher/shared/`, `docs/pipelines/...` ou un autre emplacement canonique avant d'être considérés comme faisant partie du pipeline.

## Mode opératoire pour les mises à jour du repo avec scripts jetables

Ce mode opératoire décrit la façon de travailler avec une IA lorsqu'une modification du repo doit être préparée, appliquée, vérifiée et synchronisée.

### Principe général

L'IA ne doit pas prétendre avoir modifié le repo directement si elle ne l'a pas fait.

Quand une modification est nécessaire, l'IA fournit soit :

1. un script Python jetable à télécharger dans le dossier local `Downloads` ;
2. une commande Git Bash directe ;
3. un fichier complet à créer ou remplacer.

L'utilisateur exécute les scripts depuis la racine du repo `learn-it`, vérifie le diff, commit/push, puis répond `sync` dans la discussion.

Au `sync`, l'IA doit relire les fichiers concernés sur GitHub et vérifier que le contenu correspond bien à l'état attendu.

### Convention locale pour les scripts jetables

Les scripts jetables fournis par l'IA sont généralement téléchargés dans :

```bash
/c/Users/Stef/Downloads/
```

Ils sont exécutés depuis la racine du repo :

```bash
python /c/Users/Stef/Downloads/<script>.py
```

ou, si nécessaire sous Windows :

```bash
py /c/Users/Stef/Downloads/<script>.py
```

### Exigences pour les scripts jetables

Les scripts jetables doivent autant que possible :

- être idempotents ;
- modifier uniquement les fichiers annoncés ;
- afficher les commandes de vérification à exécuter ensuite ;
- échouer clairement si un fichier attendu est absent ou si l'état du repo n'est pas celui prévu ;
- produire des rapports déterministes quand ils installent, testent ou valident une mécanique ;
- ne jamais modifier `policy.yaml`, `decisions.yaml`, le catalogue généré ou les scores sans gate explicite.

### Vérification après exécution

Après un script, l'utilisateur exécute typiquement :

```bash
python -m py_compile <script_installé_si_applicable>

git diff -- <fichiers_modifiés>
```

Puis commit/push :

```bash
git add <fichiers_modifiés>
git commit -m "<message explicite>"
git pull --rebase
git push
```

Ensuite l'utilisateur répond :

```text
sync
```

### Comportement attendu de l'IA au `sync`

Au `sync`, l'IA doit :

- relire les fichiers concernés sur GitHub ;
- vérifier que le contenu correspond à l'état attendu ;
- signaler explicitement les écarts ou corrections nécessaires ;
- ne pas avancer à l'étape suivante si un rapport attendu est absent, incohérent ou en échec.

### Règle sur les scripts déterministes du pipeline

Les scripts du repo ne doivent pas être simulés.

Si un stage ou une phase demande un script déterministe, il doit être réellement exécuté.

Si l'IA ne peut pas l'exécuter elle-même, elle doit fournir les commandes exactes à l'utilisateur.

Un rapport `PASS`, `BLOCKED`, `PENDING_HUMAN_ARBITRATION`, `PASS_READY_TO_PATCH`, etc. doit provenir d'un vrai script exécuté, pas d'une déduction narrative.

### Règle spécifique PHASE_16

Ne pas modifier `policy.yaml` ou `decisions.yaml` tant que :

```text
docs/pipelines/constitution/reports/constitution_neighbor_ids_arbitration_validation.yaml
```

n'est pas en :

```yaml
status: PASS_READY_TO_PATCH
```

Le patcher :

```text
docs/patcher/shared/apply_constitution_neighbor_ids_arbitration.py
```

doit rester en dry-run ou `BLOCKED` tant que l'arbitrage est incomplet.

L'écriture réelle de `decisions.yaml` n'est autorisée qu'avec :

```bash
python docs/patcher/shared/apply_constitution_neighbor_ids_arbitration.py \
  --apply \
  --report docs/pipelines/constitution/reports/constitution_neighbor_ids_decisions_patch_report.yaml
```

et seulement après validation `PASS_READY_TO_PATCH`.

### Séparation des étapes

Ne jamais mélanger dans une même opération :

- installation d'un mécanisme générique ;
- arbitrage humain ;
- application canonique dans `policy.yaml` ou `decisions.yaml`.

Ces étapes doivent rester séparées, vérifiées, commitées et synchronisées indépendamment.
