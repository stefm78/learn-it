# LAUNCH PROMPT — STAGE_06_FACTORY_CORE_VALIDATION

Tu travailles dans le repo local `learn-it`.

## Mission

Exécuter le `STAGE_06_FACTORY_CORE_VALIDATION` du pipeline :
- `docs/pipelines/platform_factory/pipeline.md`

## Mode de validation attendu

- Mode attendu : `POST_APPLY_CORE_VALIDATION`
- Il s’agit ici de valider le couple d’artefacts patchés après application.
- Il ne s’agit pas de revalider le patchset pré-apply.

## Inputs obligatoires

Artefacts patchés à valider :
- `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml`
- `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml`

Traçabilité du run amont :
- `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`
- `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`
- `docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml`

Artefacts courants de comparaison si nécessaire :
- `docs/cores/current/platform_factory_architecture.yaml`
- `docs/cores/current/platform_factory_state.yaml`

Socle canonique de contrôle :
- `docs/cores/current/constitution.yaml`
- `docs/cores/current/referentiel.yaml`
- `docs/cores/current/link.yaml`

Contexte d’exécution :
- `docs/pipelines/platform_factory/pipeline.md`
- `docs/prompts/shared/Make23PlatformFactoryValidation.md`
- éventuellement une note de focalisation validation dans `docs/pipelines/platform_factory/inputs/`

## Préconditions obligatoires

- `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml` doit exister.
- Les deux artefacts patchés sous `work/05_apply/patched/` doivent exister réellement.
- Si les artefacts patchés n’existent pas, ne pas simuler leur contenu.
- Si le report d’exécution n’existe pas ou est incohérent, le signaler explicitement.

## Contexte d’exécution obligatoire

- Les artefacts patchés sont l’objet principal de validation.
- Le résultat attendu doit être écrit dans le repo, dans les fichiers de sortie imposés ci-dessous.
- Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.
- Le but est de décider si l’état patché peut franchir le Stage 06 et servir de base au Stage 07.
- Ne pas réouvrir l’arbitrage.
- Ne pas transformer cette validation en nouveau challenge.
- Ne pas compenser une ambiguïté ou une absence d’artefact par une réécriture implicite.

## Règle anti-simulation obligatoire

- Ne jamais simuler le contenu des artefacts patchés.
- Ne jamais annoncer un `PASS`, `WARN` ou `FAIL` comme si les fichiers patchés avaient été relus si ce n’est pas le cas.
- Ne jamais prétendre qu’un artefact patché existe s’il n’existe pas réellement dans le repo.
- Si des fichiers requis manquent, il faut le dire explicitement dans le chat et dans le report.
- Toute conclusion doit être présentée comme conditionnelle si les inputs effectifs ne sont pas tous présents.

## Fichiers de sortie obligatoires

Écrire exactement les fichiers suivants dans le repo :
- `docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml`
- `docs/pipelines/platform_factory/reports/platform_factory_core_validation_report.md`

## Ordre de lecture obligatoire

1. `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml`
2. `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml`
3. `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml`
4. `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`
5. `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`
6. `docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml`
7. `docs/cores/current/constitution.yaml`
8. `docs/cores/current/referentiel.yaml`
9. `docs/cores/current/link.yaml`
10. `docs/cores/current/platform_factory_architecture.yaml`
11. `docs/cores/current/platform_factory_state.yaml`
12. `docs/pipelines/platform_factory/pipeline.md`
13. `docs/prompts/shared/Make23PlatformFactoryValidation.md`
14. éventuellement la note de focalisation validation

## Objectif exact

Valider que le couple patché :
- est cohérent comme couple architecture/state
- reste compatible avec le socle canonique
- préserve la séparation prescriptif / constatif
- ne surdéclare pas la maturité V0
- garde un contrat minimal d’application produite exploitable
- garde des règles de projections dérivées strictement gouvernables
- reste compatible avec la readiness multi-IA
- est suffisamment stable et gouvernable pour passer au Stage 07

## Vérifications obligatoires

La validation doit au minimum couvrir :
- adéquation au mode POST_APPLY
- fidélité à l’arbitrage et au patchset effectivement appliqué
- séparation architecture / state
- cohérence interne et cohérence croisée
- compatibilité avec Constitution / Référentiel / LINK
- cohérence du contrat minimal d’application produite
- gouvernabilité des projections dérivées
- maintien de la posture multi-IA
- stabilité et gouvernabilité de l’état patché
- anomalies, warnings et sévérité

## Contraintes

- Être explicite sur : `PASS`, `WARN`, `FAIL`.
- Ne pas produire un nouveau patch complet ici.
- Ne pas écrire une simple analyse chat à la place des livrables attendus.
- Ne pas inventer des inputs ou des conclusions non supportées.
- Ne pas réouvrir les arbitrages déjà fermés.
- Le livrable attendu est constitué des fichiers écrits dans le repo. Le retour chat doit être très succinct.

## Structure attendue du YAML de validation

Le fichier :
- `docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml`

Doit contenir au minimum :
- un statut global
- la qualification du contexte de validation
- les vérifications par axe
- les anomalies bloquantes
- les warnings
- la décision de passage de stage
- les conditions éventuelles avant Stage 07

Pour chaque point important, expliciter si possible :
- Validation Item ID
- Axe concerné
- Statut : PASS | WARN | FAIL
- Élément concerné
- Nature du problème ou de la conformité
- Impact
- Justification
- Action attendue avant passage de stage si applicable

## Structure attendue du report markdown

Le fichier :
- `docs/pipelines/platform_factory/reports/platform_factory_core_validation_report.md`

Doit être une lecture humaine cohérente du YAML de validation, avec au minimum :
- Résumé exécutif
- Qualification du contexte de validation
- Décision globale
- Vérifications par axe
- Anomalies bloquantes
- Warnings
- Conditions éventuelles avant Stage 07

## Résultat terminal attendu

À la fin de l’exécution, si les fichiers requis ont bien été relus et les livrables bien écrits, afficher uniquement :
1. les chemins exacts des fichiers écrits
2. le statut global : PASS | WARN | FAIL
3. un résumé ultra-court
