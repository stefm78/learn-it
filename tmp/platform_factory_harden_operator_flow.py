#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parents[1]

FILES: dict[str, str] = {
    "docs/pipelines/platform_factory/pipeline.md": dedent(
        """\
        # Platform Factory Pipeline

        ## Purpose

        This pipeline governs the `platform_factory` layer.
        It does not instantiate a domain application.
        It governs:
        - the prescriptive architecture of the Platform Factory,
        - the recognized current state of the Platform Factory,
        - the rules for validated derived execution projections,
        - the generic minimum contract of a produced application.

        It keeps the same overall spirit as the `constitution` pipeline:
        - explicit stages,
        - challenge and arbitrage,
        - patching,
        - validation,
        - release materialization,
        - optional promotion,
        - cleanup and archive.

        ---

        ## Governed artifacts

        Primary governed artifacts:
        - `docs/cores/current/platform_factory_architecture.yaml`
        - `docs/cores/current/platform_factory_state.yaml`

        Related reference inputs:
        - `docs/cores/current/constitution.yaml`
        - `docs/cores/current/referentiel.yaml`
        - `docs/cores/current/link.yaml`
        - `docs/architecture/Platform_Factory_Plan.md`

        Non-governed by this pipeline:
        - one specific instantiated application,
        - domain-specific learning content,
        - learner runtime state,
        - the future application instantiation pipeline itself.

        ---

        ## Operating doctrine

        ### Rule 1 — No duplication of normative authority
        The pipeline must not rewrite the Constitution, the Référentiel or the LINK indirectly.
        It may only:
        - reference them,
        - bind to them,
        - derive validated execution projections from them,
        - operationalize them for factory-level concerns.

        ### Rule 2 — Separation of prescriptive and constatative artifacts
        - `platform_factory_architecture.yaml` is prescriptive.
        - `platform_factory_state.yaml` is constatative.

        These two roles must remain separate throughout the pipeline.

        ### Rule 3 — Released baseline posture
        The current `platform_factory` artifacts are considered a released baseline.
        A new pipeline run does not start with a discovery audit of an unknown object.
        It starts by challenging the released baseline and deciding whether corrections are required.

        ### Rule 4 — Derived execution projections must remain strictly conformant
        A `validated_derived_execution_projection` may be the only artifact given to an IA for a bounded task, but only if it is validated as strictly conformant to the applicable canon.

        ### Rule 5 — Multi-IA readiness is a first-rank design constraint
        The pipeline must preserve or improve the ability of the Platform Factory to support bounded, parallel work by multiple IAs.

        ### Rule 6 — Release and promotion are distinct acts
        Release materialization and promotion to `docs/cores/current/` must remain explicitly separated.
        A validated patched state is not yet the promoted current state until a dedicated promotion stage completes.

        ---

        ## Stage map

        ### STAGE_01_CHALLENGE

        - Inputs:
          - current `platform_factory` artifacts
          - canonical foundation
          - optional focus note in `inputs/`
        - Prompt:
          - `docs/prompts/shared/Challenge_platform_factory.md`
        - Output:
          - `work/01_challenge/challenge_report_##.md`

        ### STAGE_02_FACTORY_ARBITRAGE

        - Inputs:
          - challenge reports from `work/01_challenge/`
          - optional human arbitrage notes
        - Prompt:
          - `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
        - Rule:
          - every `challenge_report*.md` present in `work/01_challenge/` must be considered during arbitrage
          - multiple parallel arbitrage proposals may be produced under `work/02_arbitrage/platform_factory_arbitrage_<ID>.md`
          - the arbitrage must consolidate retained, rejected, deferred and out-of-scope findings into a single decision record
          - the canonical output of the stage remains `work/02_arbitrage/platform_factory_arbitrage.md`
        - Outputs:
          - `work/02_arbitrage/platform_factory_arbitrage_<ID>.md`
          - `work/02_arbitrage/platform_factory_arbitrage.md`

        ### STAGE_03_FACTORY_PATCH_SYNTHESIS

        - Inputs:
          - current governed artifacts
          - challenge reports
          - arbitrage
        - Prompt:
          - `docs/prompts/shared/Make22PlatformFactoryPatch.md`
        - Output:
          - `work/03_patch/platform_factory_patchset.yaml`

        ### STAGE_04_FACTORY_PATCH_VALIDATION

        - Inputs:
          - `work/03_patch/platform_factory_patchset.yaml`
          - `work/02_arbitrage/platform_factory_arbitrage.md`
        - Prompt:
          - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`
        - Companion prompt:
          - `docs/prompts/shared/Make23PlatformFactoryValidation.md`
        - Outputs:
          - `work/04_patch_validation/platform_factory_patch_validation.yaml`
          - `reports/platform_factory_patch_validation_report.md`

        ### STAGE_05_FACTORY_APPLY

        - Inputs:
          - validated patchset
        - Prompt:
          - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`
        - Outputs:
          - `work/05_apply/patched/platform_factory_architecture.yaml`
          - `work/05_apply/patched/platform_factory_state.yaml`
          - `reports/platform_factory_execution_report.yaml`

        ### STAGE_06_FACTORY_CORE_VALIDATION

        - Inputs:
          - patched `platform_factory` artifacts from `work/05_apply/patched/`
        - Prompt:
          - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`
        - Companion prompt:
          - `docs/prompts/shared/Make23PlatformFactoryValidation.md`
        - Outputs:
          - `work/06_core_validation/platform_factory_core_validation.yaml`
          - `reports/platform_factory_core_validation_report.md`

        ### STAGE_07_FACTORY_RELEASE_MATERIALIZATION

        - Prompt:
          - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
        - Spec détaillée :
          - `docs/pipelines/platform_factory/STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
        - Rule:
          - `STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md` is the canonical specification for Stage 07

        ### STAGE_08_FACTORY_PROMOTE_CURRENT

        - Prompt:
          - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`
        - Spec détaillée :
          - `docs/pipelines/platform_factory/STAGE_08_FACTORY_PROMOTE_CURRENT.md`
        - Rule:
          - `STAGE_08_FACTORY_PROMOTE_CURRENT.md` is the canonical specification for Stage 08

        ### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE

        - Inputs:
          - promotion outputs
          - release outputs
        - Prompt:
          - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`
        - Outputs:
          - `reports/platform_factory_closeout_report.yaml`
          - `outputs/platform_factory_summary.md`

        ---

        ## Minimal write zones

        Expected write zones for this pipeline:
        - `docs/pipelines/platform_factory/work/`
        - `docs/pipelines/platform_factory/reports/`
        - `docs/pipelines/platform_factory/outputs/`
        - `docs/pipelines/platform_factory/archive/`

        Primary target artifacts:
        - `docs/cores/current/platform_factory_architecture.yaml`
        - `docs/cores/current/platform_factory_state.yaml`

        ---

        ## Prompt assets

        Expected shared prompt family:
        - `docs/prompts/shared/Challenge_platform_factory.md`
        - `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
        - `docs/prompts/shared/Make22PlatformFactoryPatch.md`
        - `docs/prompts/shared/Make23PlatformFactoryValidation.md`

        Stage-specific launch prompts:
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`

        Prompt usage companion:
        - `docs/pipelines/platform_factory/PROMPT_USAGE.md`

        Operator guidance companion:
        - `docs/pipelines/platform_factory/OPERATOR_RUNBOOK.md`

        ---

        ## Validation expectations

        At minimum, the pipeline must preserve:
        - separation between architecture and state,
        - strict fidelity requirements for validated derived execution projections,
        - explicit dependence on Constitution/Référentiel/LINK,
        - minimum produced-application contract integrity,
        - multi-IA parallel readiness constraints.

        ---

        ## Success criteria

        - No stage may be skipped
        - A new run starts from challenge of the released baseline, not from a discovery audit
        - No file in `docs/cores/current/` may be modified directly before explicit promotion
        - Any patch application must occur in a sandbox root under `work/05_apply/`
        - Any release materialization should happen before promotion
        - Promotion to `current/` must remain explicit and occur in a dedicated stage
        - Any successful promotion should be followed by an explicit archive-and-reset closeout stage

        ---

        ## Current V0 posture

        This pipeline skeleton is intentionally V0.
        It is sufficient to begin challenge and iterative hardening.
        It is not yet a fully tooled execution framework.
        """
    ),
    "docs/pipelines/platform_factory/PROMPT_USAGE.md": dedent(
        """\
        # Platform Factory — Prompt usage

        Ce document complète `pipeline.md` en indiquant quel prompt utiliser à chaque étape du pipeline `platform_factory`.

        Il ne remplace pas le pipeline.
        Il en précise le mode opératoire côté IA.

        ---

        ## Vue d'ensemble

        Prompts disponibles :
        - `docs/prompts/shared/Challenge_platform_factory.md`
        - `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
        - `docs/prompts/shared/Make22PlatformFactoryPatch.md`
        - `docs/prompts/shared/Make23PlatformFactoryValidation.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`

        Companion opérateur :
        - `docs/pipelines/platform_factory/OPERATOR_RUNBOOK.md`

        ---

        ## Mapping recommandé par stage

        ### STAGE_01_CHALLENGE
        Prompt principal :
        - `docs/prompts/shared/Challenge_platform_factory.md`

        But :
        - challenger la baseline release actuelle de la factory ;
        - identifier faiblesses, ambiguïtés, contradictions, trous de contrat ou dérives ;
        - préparer les findings pour arbitrage.

        ---

        ### STAGE_02_FACTORY_ARBITRAGE
        Prompt principal :
        - `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`

        Input attendu :
        - un ou plusieurs challenge reports ;
        - éventuellement des arbitrages humains complémentaires.

        ---

        ### STAGE_03_FACTORY_PATCH_SYNTHESIS
        Prompt principal :
        - `docs/prompts/shared/Make22PlatformFactoryPatch.md`

        But :
        - préparer la synthèse de patch en gardant la séparation architecture / state.

        ---

        ### STAGE_04_FACTORY_PATCH_VALIDATION
        Prompt principal :
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`

        Prompt compagnon :
        - `docs/prompts/shared/Make23PlatformFactoryValidation.md`

        But :
        - exécuter la validation pré-apply ;
        - produire le YAML automatique de validation ;
        - produire le report markdown humain cohérent avec ce YAML.

        ---

        ### STAGE_05_FACTORY_APPLY
        Prompt principal :
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`

        But :
        - préparer la sandbox ;
        - exécuter le dry-run puis l’apply réel ;
        - matérialiser les artefacts patchés et le report d’exécution.

        ---

        ### STAGE_06_FACTORY_CORE_VALIDATION
        Prompt principal :
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`

        Prompt compagnon :
        - `docs/prompts/shared/Make23PlatformFactoryValidation.md`

        But :
        - exécuter la validation post-apply ;
        - produire le YAML automatique de validation ;
        - produire le report markdown humain cohérent avec ce YAML.

        ---

        ### STAGE_07_FACTORY_RELEASE_MATERIALIZATION
        Prompt principal :
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`

        But :
        - calculer le release plan déterministe ;
        - ne matérialiser une release que si `release_required: true` ;
        - produire le report de matérialisation et les release notes.

        ---

        ### STAGE_08_FACTORY_PROMOTE_CURRENT
        Prompt principal :
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`

        But :
        - promouvoir la release matérialisée vers `docs/cores/current/` ;
        - produire le report de promotion ;
        - rester idempotent si la release est déjà current.

        ---

        ### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE
        Prompt principal :
        - `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`

        But :
        - exécuter le closeout déterministe du run ;
        - archiver `work/`, `reports/` et `outputs/` ;
        - produire `platform_factory_closeout_report.yaml` et `platform_factory_summary.md` ;
        - réinitialiser `work/` pour le prochain cycle.

        ---

        ## Mode opératoire recommandé pour une IA sans contexte

        1. Lire d’abord `docs/pipelines/platform_factory/pipeline.md`.
        2. Lire ensuite ce document.
        3. Lire ensuite le prompt principal du stage visé.
        4. Si le stage implique un script déterministe, donner d’abord la commande exacte à exécuter, sans simuler le résultat.
        5. Après exécution humaine de la commande, relire le YAML ou le report réellement produit, puis annoncer seulement :
           - les chemins écrits ;
           - le statut ;
           - la suite immédiate.

        Pour les Stages 01 à 03, il n’y a pas de commande shell obligatoire : l’IA doit écrire directement le livrable dans le repo, ou fournir un contenu prêt à déposer exactement au bon chemin.

        ---

        ## Règle d'usage

        Le point d'entrée normal d'un run `platform_factory` est le challenge de la baseline release active.
        Le pipeline ne prévoit pas de stage d'audit initial ni de stage de scan séparé dans son flux nominal.
        La release materialization reste distincte de la promotion, comme dans les autres pipelines de gouvernance du repo.

        ---

        ## Posture V0

        Ce mapping est volontairement simple.
        Il est suffisant pour lancer des premiers cycles cohérents de gouvernance `platform_factory`.
        Il pourra être raffiné après quelques runs réels.
        """
    ),
    "docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md": dedent(
        """\
        # LAUNCH PROMPT — STAGE_07_FACTORY_RELEASE_MATERIALIZATION

        Tu travailles dans le repo local `learn-it`.

        ## Mission

        Exécuter le `STAGE_07_FACTORY_RELEASE_MATERIALIZATION` du pipeline :
        - `docs/pipelines/platform_factory/pipeline.md`
        - spécification détaillée :
          - `docs/pipelines/platform_factory/STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`

        ## Sous-étapes obligatoires

        - `07A_FACTORY_RELEASE_CLASSIFICATION`
        - `07B_FACTORY_RELEASE_MATERIALIZATION`

        ## Inputs obligatoires

        Artefacts patchés validés :
        - `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml`
        - `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml`

        Validation et exécution amont :
        - `docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml`
        - `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml`

        État courant de référence :
        - `docs/cores/current/platform_factory_architecture.yaml`
        - `docs/cores/current/platform_factory_state.yaml`

        Scripts dédiés :
        - `docs/patcher/shared/build_platform_factory_release_plan.py`
        - `docs/patcher/shared/materialize_platform_factory_release.py`

        ## Préconditions obligatoires

        - `docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml` doit être en `status: PASS`.
        - Les artefacts patchés de `work/05_apply/patched/` doivent exister réellement.
        - Le report d’exécution Stage 05 doit exister réellement.
        - Ne pas simuler une release plan ou une release matérialisée si les scripts n’ont pas tourné.

        ## Contexte d’exécution obligatoire

        - Le calcul de release doit être déterministe.
        - L’IA peut commenter ou relire le résultat, mais ne doit pas remplacer le calcul par une estimation libre.
        - `docs/cores/current/` ne doit jamais être modifié à ce stage.
        - Le résultat attendu doit être écrit dans le repo, dans les chemins de sortie imposés ci-dessous.
        - Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.

        ## Règle anti-simulation obligatoire

        - Ne jamais simuler le résultat d’un script déterministe.
        - Ne jamais annoncer un `release_required`, `change_depth`, `release_id`, `release_path` ou `status` comme si les scripts avaient été exécutés si ce n’est pas le cas.
        - Ne jamais prétendre qu’une release immuable existe sous `docs/cores/releases/` si elle n’a pas été réellement matérialisée.
        - Si une commande doit être exécutée par l’humain ou dans un autre contexte d’exécution, cela doit être dit explicitement dans le chat.
        - Dans ce cas, il faut donner clairement la ou les commandes exactes à exécuter.
        - Toute lecture complémentaire doit être présentée comme préparatoire ou conditionnelle, jamais comme un résultat déjà constaté des scripts.

        ## Fichiers de sortie obligatoires

        Sorties de `07A_FACTORY_RELEASE_CLASSIFICATION` :
        - `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`

        Sorties de `07B_FACTORY_RELEASE_MATERIALIZATION` :
        - `docs/cores/releases/<release_id>/platform_factory_architecture.yaml`
        - `docs/cores/releases/<release_id>/platform_factory_state.yaml`
        - `docs/cores/releases/<release_id>/manifest.yaml`
        - `docs/pipelines/platform_factory/outputs/platform_factory_release_candidate_notes.md`
        - `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`

        ## Étapes d’exécution obligatoires

        ### 1. Préparer le répertoire de travail release

        Exécuter :

        ```bash
        mkdir -p ./docs/pipelines/platform_factory/work/07_release
        mkdir -p ./docs/pipelines/platform_factory/outputs
        ```

        ### 2. Exécuter 07A_FACTORY_RELEASE_CLASSIFICATION

        Exécuter :

        ```bash
        python docs/patcher/shared/build_platform_factory_release_plan.py \
          ./docs/pipelines/platform_factory/work/05_apply/patched \
          ./docs/cores/current \
          ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml \
          ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml
        ```

        ### 3. Vérifier le release plan

        - Lire `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
        - Vérifier explicitement la racine `RELEASE_PLAN` :
          - `status`
          - `release_required`
          - `change_depth`
          - `release_bundle.release_id`
          - `release_bundle.release_path`
          - `release_bundle.promotion_candidate`
        - Si `RELEASE_PLAN.status` n’est pas `PASS`, arrêter ici.
        - Si `RELEASE_PLAN.release_required` vaut `false`, arrêter ici sans lancer 07B.
        - Dans ce cas, ne pas créer de release sous `docs/cores/releases/` et ne pas passer au Stage 08.

        ### 4. Exécuter 07B_FACTORY_RELEASE_MATERIALIZATION

        Seulement si le release plan est exploitable et si `RELEASE_PLAN.release_required: true`, exécuter :

        ```bash
        python docs/patcher/shared/materialize_platform_factory_release.py \
          ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
          ./docs/pipelines/platform_factory/work/05_apply/patched \
          ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
          ./docs/pipelines/platform_factory/outputs/platform_factory_release_candidate_notes.md
        ```

        ### 5. Vérifier le report de matérialisation

        - Lire `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`
        - Vérifier explicitement la racine `PLATFORM_FACTORY_RELEASE_MATERIALIZATION` :
          - `status`
          - `release_required`
          - `release_id`
          - `release_path`
          - `files_written`
        - Si `PLATFORM_FACTORY_RELEASE_MATERIALIZATION.status` n’est pas `PASS`, le stage ne franchit pas 07.
        - Ne pas passer à la promotion tant que la matérialisation n’est pas proprement fermée.

        ## Si une commande doit être exécutée par l’humain dans le chat

        Avant toute interprétation du résultat, dire explicitement :
        - qu’il s’agit d’une commande déterministe à exécuter ;
        - que le résultat automatique n’est pas encore disponible ;
        - que tout statut de release reste non confirmé tant que les fichiers de sortie n’ont pas été réellement produits.

        ## Contraintes

        - Ne pas modifier `docs/cores/current/` à ce stage.
        - Ne pas inventer un `release_id` à la place du script.
        - Ne pas créer de release immuable si `RELEASE_PLAN.release_required: false`.
        - Ne pas remplacer les scripts dédiés par une interprétation libre.
        - Le livrable attendu est constitué des fichiers écrits dans le repo. Le retour chat doit être très succinct.

        ## Résultat terminal attendu

        À la fin de l’exécution, si les scripts ont bien été exécutés et les artefacts bien écrits, afficher uniquement :
        1. les chemins exacts des artefacts écrits
        2. le statut final du release plan et du report de matérialisation : PASS | WARN | FAIL
        3. un résumé ultra-court
        """
    ),
    "docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md": dedent(
        """\
        # LAUNCH PROMPT — STAGE_08_FACTORY_PROMOTE_CURRENT

        Tu travailles dans le repo local `learn-it`.

        ## Mission

        Exécuter le `STAGE_08_FACTORY_PROMOTE_CURRENT` du pipeline :
        - `docs/pipelines/platform_factory/pipeline.md`
        - spécification détaillée :
          - `docs/pipelines/platform_factory/STAGE_08_FACTORY_PROMOTE_CURRENT.md`

        ## Inputs obligatoires

        Plan et report Stage 07 :
        - `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
        - `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`

        Release matérialisée :
        - `docs/cores/releases/<release_id>/platform_factory_architecture.yaml`
        - `docs/cores/releases/<release_id>/platform_factory_state.yaml`
        - `docs/cores/releases/<release_id>/manifest.yaml`

        État courant éventuel :
        - `docs/cores/current/platform_factory_architecture.yaml`
        - `docs/cores/current/platform_factory_state.yaml`

        Script dédié :
        - `docs/patcher/shared/promote_platform_factory_current.py`

        ## Préconditions obligatoires

        - `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml` doit être en `status: PASS`.
        - `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml` doit être en `status: PASS`.
        - La release ciblée doit exister physiquement sous `docs/cores/releases/<release_id>/`.
        - Le manifest de release doit être présent et lisible.
        - Ne pas promouvoir depuis `work/05_apply/patched/`.
        - Ne pas simuler une promotion si le script n’a pas tourné.

        ## Contexte d’exécution obligatoire

        - `docs/cores/releases/` est la source de vérité des releases publiées.
        - `docs/cores/current/` est uniquement la vue active de la release promue.
        - Ce stage ne doit modifier que `docs/cores/current/` et le report de promotion.
        - Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.
        - La promotion doit rester idempotente.
        - Il ne faut pas modifier `docs/cores/current/manifest.yaml` par défaut à ce stade V0.

        ## Règle anti-simulation obligatoire

        - Ne jamais simuler le résultat d’un script déterministe.
        - Ne jamais annoncer qu’une release a été promue si le script n’a pas réellement tourné.
        - Ne jamais annoncer un `promotion_mode`, un `release_id` promu ou un `status` comme si la promotion avait été constatée si ce n’est pas le cas.
        - Si une commande doit être exécutée par l’humain ou dans un autre contexte d’exécution, cela doit être dit explicitement dans le chat.
        - Dans ce cas, il faut donner clairement la commande exacte à exécuter.
        - Toute lecture complémentaire doit être présentée comme préparatoire ou conditionnelle, jamais comme le résultat réel du script.

        ## Fichiers de sortie obligatoires

        - `docs/cores/current/platform_factory_architecture.yaml`
        - `docs/cores/current/platform_factory_state.yaml`
        - `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`

        ## Étape d’exécution obligatoire

        Exécuter :

        ```bash
        python docs/patcher/shared/promote_platform_factory_current.py \
          ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml
        ```

        ## Vérification obligatoire après exécution

        - Lire `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`
        - Vérifier explicitement la racine `PROMOTION_REPORT` :
          - `status`
          - `release_id`
          - `source_release_path`
          - `promotion_mode`
          - `files_promoted`
        - Si `PROMOTION_REPORT.status` n’est pas en `PASS`, le stage ne franchit pas 08.
        - Si `PROMOTION_REPORT.promotion_mode: already_current`, considérer la promotion comme idempotente et valide.

        ## Si une commande doit être exécutée par l’humain dans le chat

        Avant toute interprétation du résultat, dire explicitement :
        - qu’il s’agit d’une commande déterministe à exécuter ;
        - que le résultat automatique n’est pas encore disponible ;
        - que tout statut de promotion reste non confirmé tant que le report YAML n’a pas été réellement produit.

        ## Contraintes

        - Ne pas promouvoir depuis `work/05_apply/patched/`.
        - Ne pas réécrire la logique des artefacts pendant la promotion.
        - Ne pas modifier `docs/cores/releases/<release_id>/`.
        - Ne pas modifier `docs/cores/current/manifest.yaml` par défaut dans ce Stage 08 V0.
        - Ne pas remplacer le script dédié par une interprétation libre.
        - Le livrable attendu est constitué des fichiers écrits dans le repo. Le retour chat doit être très succinct.

        ## Résultat terminal attendu

        À la fin de l’exécution, si le script a bien été exécuté et les artefacts bien écrits, afficher uniquement :
        1. les chemins exacts des artefacts écrits
        2. le statut final du report de promotion : PASS | WARN | FAIL
        3. un résumé ultra-court
        """
    ),
    "docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md": dedent(
        """\
        # LAUNCH PROMPT — STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE

        Tu travailles dans le repo local `learn-it`.

        ## Mission

        Exécuter le `STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE` du pipeline :
        - `docs/pipelines/platform_factory/pipeline.md`

        Le but de ce stage est de clôturer proprement un run déjà promu, d’archiver son état d’exécution, de produire le report final de closeout, de produire le résumé final, puis de réinitialiser `work/` pour un prochain run.

        ## Inputs obligatoires

        Promotion réussie :
        - `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`

        Traçabilité release :
        - `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
        - `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`

        Script dédié :
        - `docs/patcher/shared/closeout_platform_factory_run.py`

        ## Préconditions obligatoires

        - `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml` doit être en `status: PASS`.
        - `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml` doit être en `status: PASS`.
        - `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml` doit être en `status: PASS`.
        - Le `promotion_mode` doit être compatible avec un closeout post-promotion (`applied` ou `already_current`).
        - La release promue doit exister réellement sous `docs/cores/releases/<release_id>/`.
        - Le manifest de release doit être présent.
        - Ne pas simuler un closeout si le script n’a pas tourné.

        ## Contexte d’exécution obligatoire

        - Le Stage 09 clôture explicitement le run terminé.
        - Il archive le run sous `docs/pipelines/platform_factory/archive/<release_id>/`.
        - Il archive :
          - `docs/pipelines/platform_factory/work/`
          - `docs/pipelines/platform_factory/reports/`
          - `docs/pipelines/platform_factory/outputs/`
        - Il recrée ensuite `docs/pipelines/platform_factory/work/` vide, prêt pour une nouvelle exécution.
        - Il réécrit ensuite le report final de closeout et le résumé final dans les emplacements actifs du pipeline.
        - Il ne modifie ni la release immuable sous `docs/cores/releases/`, ni la promotion déjà en place sous `docs/cores/current/`.
        - Il ne faut pas considérer qu’une réponse dans le chat suffit à accomplir la tâche.

        ## Règle anti-simulation obligatoire

        - Ne jamais simuler le résultat d’un script déterministe.
        - Ne jamais annoncer qu’un run est clôturé et archivé si le script n’a pas réellement tourné.
        - Ne jamais prétendre que `work/` a été réinitialisé si ce n’est pas réellement le cas.
        - Si une commande doit être exécutée par l’humain ou dans un autre contexte d’exécution, cela doit être dit explicitement dans le chat.
        - Dans ce cas, il faut donner clairement la commande exacte à exécuter.
        - Toute lecture complémentaire doit être présentée comme préparatoire ou conditionnelle, jamais comme le résultat réel du script.

        ## Fichiers et répertoires de sortie obligatoires

        Sorties actives attendues après exécution :
        - `docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml`
        - `docs/pipelines/platform_factory/outputs/platform_factory_summary.md`
        - `docs/pipelines/platform_factory/work/` recréé vide

        Archive attendue :
        - `docs/pipelines/platform_factory/archive/<release_id>/`

        ## Étape d’exécution obligatoire

        Exécuter :

        ```bash
        python docs/patcher/shared/closeout_platform_factory_run.py \
          ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml \
          ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml \
          ./docs/pipelines/platform_factory/outputs/platform_factory_summary.md \
          ./docs/pipelines/platform_factory/archive
        ```

        ## Vérification obligatoire après exécution

        Lire :
        - `docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml`
        - `docs/pipelines/platform_factory/outputs/platform_factory_summary.md`

        Vérifier explicitement dans la racine YAML `PLATFORM_FACTORY_CLOSEOUT_REPORT` :
        - `status`
        - `release_id`
        - `source_release_path`
        - `promotion_mode`
        - `manifest_path`
        - `archive_path`
        - `archived_paths`
        - `work_reset`
        - `run_closed`

        Vérifier aussi :
        - que `docs/pipelines/platform_factory/work/` existe bien encore après exécution ;
        - qu’il est recréé vide ;
        - que `docs/pipelines/platform_factory/archive/<release_id>/` existe réellement.

        Si le report n’est pas en `status: PASS`, le pipeline ne peut pas être considéré comme proprement clôturé.

        ## Si une commande doit être exécutée par l’humain dans le chat

        Avant toute interprétation du résultat, dire explicitement :
        - qu’il s’agit d’une commande déterministe à exécuter ;
        - que le résultat automatique n’est pas encore disponible ;
        - que tout statut de closeout reste non confirmé tant que le report YAML n’a pas été réellement produit.

        ## Contraintes

        - Ne pas recalculer de contenu métier dans ce Stage 09.
        - Ne pas modifier `docs/cores/releases/`.
        - Ne pas modifier `docs/cores/current/`.
        - Ne pas remplacer le script dédié par une interprétation libre.
        - Ne pas considérer les copies archivées comme un substitut du report final actif.
        - Le livrable attendu est constitué des fichiers et répertoires écrits dans le repo. Le retour chat doit être très succinct.

        ## Résultat terminal attendu

        À la fin de l’exécution, si le script a bien été exécuté et les artefacts bien écrits, afficher uniquement :
        1. les chemins exacts des artefacts écrits ;
        2. le statut final du report de closeout : PASS | WARN | FAIL ;
        3. un résumé ultra-court.
        """
    ),
    "docs/pipelines/platform_factory/OPERATOR_RUNBOOK.md": dedent(
        """\
        # Platform Factory — Operator runbook

        Ce document sert de companion opérateur pour une IA sans contexte historique du repo.

        Il ne remplace ni `pipeline.md`, ni les launch prompts.
        Il donne le chemin le plus court pour faire avancer le pipeline proprement, en donnant au bon moment la commande exacte à exécuter, puis en relisant le report effectivement produit.

        ---

        ## Règle cardinale

        Ne jamais simuler le résultat d’un script déterministe.

        Pour tout stage scripté :
        1. lire le prompt du stage ;
        2. donner la commande exacte ;
        3. attendre l’exécution humaine ;
        4. relire le YAML ou le report réellement écrit ;
        5. annoncer seulement le statut constaté et la suite immédiate.

        ---

        ## Ordre minimal de lecture pour une IA sans contexte

        1. `docs/pipelines/platform_factory/pipeline.md`
        2. `docs/pipelines/platform_factory/PROMPT_USAGE.md`
        3. le prompt principal du stage en cours
        4. les fichiers d’entrée réellement présents dans `work/`, `reports/`, `outputs/` ou `docs/cores/current/`

        ---

        ## Format de réponse recommandé

        ### Cas A — stage sans script obligatoire

        Répondre de manière courte avec :
        - le chemin du fichier à écrire ;
        - soit le contenu complet prêt à déposer ;
        - soit un patch / remplacement exact si l’IA ne peut pas écrire directement.

        ### Cas B — stage avec script déterministe

        Répondre sous cette forme :

        ```text
        Commande déterministe à exécuter
        ```

        puis un unique bloc bash, puis une seule phrase demandant de coller la sortie du terminal ou de confirmer le fichier YAML produit.

        Après exécution, répondre seulement avec :
        1. chemins écrits ;
        2. statut ;
        3. suite immédiate.

        ---

        ## Mapping rapide par stage

        ### STAGE_01_CHALLENGE
        - Prompt : `docs/prompts/shared/Challenge_platform_factory.md`
        - Sortie attendue : `docs/pipelines/platform_factory/work/01_challenge/challenge_report_<ID>.md`
        - Commande shell : aucune obligatoire

        ### STAGE_02_FACTORY_ARBITRAGE
        - Prompt : `docs/prompts/shared/Make21PlatformFactoryArbitrage.md`
        - Sortie attendue : `docs/pipelines/platform_factory/work/02_arbitrage/platform_factory_arbitrage.md`
        - Commande shell : aucune obligatoire

        ### STAGE_03_FACTORY_PATCH_SYNTHESIS
        - Prompt : `docs/prompts/shared/Make22PlatformFactoryPatch.md`
        - Sortie attendue : `docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml`
        - Commande shell : aucune obligatoire

        ### STAGE_04_FACTORY_PATCH_VALIDATION
        - Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_04_FACTORY_PATCH_VALIDATION.md`
        - YAML attendu : `docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml`
        - Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_patch_validation_report.md`
        - Commande :

        ```bash
        mkdir -p ./docs/pipelines/platform_factory/work/04_patch_validation
        python docs/patcher/shared/validate_platform_factory_patchset.py \
          ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \
          > ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml
        ```

        ### STAGE_05_FACTORY_APPLY
        - Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_05_FACTORY_APPLY.md`
        - Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml`
        - Artefacts patchés attendus :
          - `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml`
          - `docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml`
        - Commandes :

        ```bash
        mkdir -p ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current
        cp ./docs/cores/current/platform_factory_architecture.yaml ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_architecture.yaml
        cp ./docs/cores/current/platform_factory_state.yaml ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_state.yaml
        python docs/patcher/shared/apply_platform_factory_patchset.py \
          ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \
          ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml \
          ./docs/pipelines/platform_factory/work/05_apply/sandbox \
          true \
          ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml
        ```

        Puis, seulement si le dry-run est `PASS` :

        ```bash
        python docs/patcher/shared/apply_platform_factory_patchset.py \
          ./docs/pipelines/platform_factory/work/03_patch/platform_factory_patchset.yaml \
          ./docs/pipelines/platform_factory/work/04_patch_validation/platform_factory_patch_validation.yaml \
          ./docs/pipelines/platform_factory/work/05_apply/sandbox \
          false \
          ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml
        mkdir -p ./docs/pipelines/platform_factory/work/05_apply/patched
        cp ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_architecture.yaml ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml
        cp ./docs/pipelines/platform_factory/work/05_apply/sandbox/docs/cores/current/platform_factory_state.yaml ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml
        ```

        ### STAGE_06_FACTORY_CORE_VALIDATION
        - Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_06_FACTORY_CORE_VALIDATION.md`
        - YAML attendu : `docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml`
        - Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_core_validation_report.md`
        - Commande :

        ```bash
        mkdir -p ./docs/pipelines/platform_factory/work/06_core_validation
        python docs/patcher/shared/validate_platform_factory_core.py \
          ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_architecture.yaml \
          ./docs/pipelines/platform_factory/work/05_apply/patched/platform_factory_state.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml \
          > ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml
        ```

        ### STAGE_07_FACTORY_RELEASE_MATERIALIZATION
        - Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_07_FACTORY_RELEASE_MATERIALIZATION.md`
        - Plan attendu : `docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml`
        - Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml`
        - Commandes :

        ```bash
        mkdir -p ./docs/pipelines/platform_factory/work/07_release
        mkdir -p ./docs/pipelines/platform_factory/outputs
        python docs/patcher/shared/build_platform_factory_release_plan.py \
          ./docs/pipelines/platform_factory/work/05_apply/patched \
          ./docs/cores/current \
          ./docs/pipelines/platform_factory/work/06_core_validation/platform_factory_core_validation.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_execution_report.yaml \
          ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml
        ```

        Puis, seulement si `RELEASE_PLAN.status: PASS` et `RELEASE_PLAN.release_required: true` :

        ```bash
        python docs/patcher/shared/materialize_platform_factory_release.py \
          ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
          ./docs/pipelines/platform_factory/work/05_apply/patched \
          ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
          ./docs/pipelines/platform_factory/outputs/platform_factory_release_candidate_notes.md
        ```

        ### STAGE_08_FACTORY_PROMOTE_CURRENT
        - Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_08_FACTORY_PROMOTE_CURRENT.md`
        - Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml`
        - Commande :

        ```bash
        python docs/patcher/shared/promote_platform_factory_current.py \
          ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml
        ```

        ### STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE
        - Prompt : `docs/pipelines/platform_factory/LAUNCH_PROMPT_STAGE_09_FACTORY_CLOSEOUT_AND_ARCHIVE.md`
        - Report attendu : `docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml`
        - Summary attendu : `docs/pipelines/platform_factory/outputs/platform_factory_summary.md`
        - Commande :

        ```bash
        python docs/patcher/shared/closeout_platform_factory_run.py \
          ./docs/pipelines/platform_factory/reports/platform_factory_promotion_report.yaml \
          ./docs/pipelines/platform_factory/work/07_release/platform_factory_release_plan.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_release_materialization_report.yaml \
          ./docs/pipelines/platform_factory/reports/platform_factory_closeout_report.yaml \
          ./docs/pipelines/platform_factory/outputs/platform_factory_summary.md \
          ./docs/pipelines/platform_factory/archive
        ```

        ---

        ## Discipline de sortie minimale

        Pour les stages 04 à 09, l’IA ne doit pas noyer l’utilisateur.

        Après exécution d’une commande, la sortie attendue côté chat doit tenir en trois éléments :
        1. chemins écrits ;
        2. statut lu dans le YAML ou report produit ;
        3. prochaine action immédiate.
        """
    ),
}


def main() -> None:
    for rel_path, content in FILES.items():
        path = REPO_ROOT / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        normalized = content.rstrip() + "\n"
        path.write_text(normalized, encoding="utf-8")
        print(f"UPDATED {rel_path}")
    print("DONE")


if __name__ == "__main__":
    main()
