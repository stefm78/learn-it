# Pilot 01 — Constitution bounded run on `learner_state`

## Objet

Ce document cadre le premier pilote réel du mode borné introduit dans le pipeline `constitution`.

Le pilote vise à tester un run local borné sur un sous-ensemble lisible de la Constitution, sans toucher encore à la structure physique des artefacts canoniques.

## Scope retenu

Identifiant de scope :
- `CONSTITUTION_BOUNDARY_PILOT_01_LEARNER_STATE`

Artefacts d'entrée :
- `docs/pipelines/constitution/inputs/scope_manifest.yaml`
- `docs/pipelines/constitution/inputs/impact_bundle.yaml`
- `docs/pipelines/constitution/inputs/integration_gate.yaml`

## Sous-ensemble visé

Le pilote cible principalement :
- `TYPE_LEARNER_STATE_MODEL`
- les axes d'état apprenant ;
- les auto-reports AR-N1 / AR-N2 / AR-N3 ;
- la logique de conservatisme quand l'observabilité est insuffisante ;
- la frontière entre `unknown`, détresse et escalade.

## Pourquoi ce scope

Ce scope a été retenu car il est :
- assez petit pour être manipulable dans un premier run borné ;
- assez relié pour révéler les effets de bord ;
- déjà suffisamment structuré pour tester les règles `in_scope`, `out_of_scope_but_relevant` et `needs_scope_extension`.

## Objectifs de validation du pilote

Le pilote doit permettre de vérifier :

1. que le challenge borné reste utile et substantiel ;
2. qu'il ne dérive pas silencieusement hors scope ;
3. que les dépendances au Référentiel sont correctement signalées ;
4. que l'arbitrage distingue bien :
   - ce qui est corrigeable maintenant ;
   - ce qui est pertinent mais hors scope ;
   - ce qui nécessite extension de scope ;
5. que le `integration_gate` empêche toute lecture abusive d'un succès local comme succès global.

## Résultat attendu du pilote

Un pilote réussi n'implique pas forcément qu'un patch soit produit.

Le pilote est considéré comme utile si l'un des cas suivants se produit :
- un challenge borné de qualité est produit ;
- un arbitrage borné clair est produit ;
- un patch borné sûr est produit ;
- ou une décision explicite de `no_patch / scope_extension_needed` est justifiée proprement.

## Séquence recommandée

1. Lire `docs/pipelines/constitution/pipeline.md`.
2. Lire `docs/prompts/shared/Challenge_constitution.md`.
3. Lire `docs/prompts/shared/Make04ConstitutionArbitrage.md`.
4. Lire les trois fichiers d'entrée du pilote dans `docs/pipelines/constitution/inputs/`.
5. Exécuter le Stage 01 en mode borné.
6. Exécuter le Stage 02 en mode borné.
7. Décider ensuite si un Stage 03 patch borné est justifié.

## Garde-fous

- Ne pas élargir le scope implicitement pendant le pilote.
- Ne pas convertir une dépendance référentielle en correction constitutionnelle silencieuse.
- Ne pas traiter le pilote comme une refonte globale de `learner_state`.
- Ne pas promouvoir quoi que ce soit à partir de ce pilote sans revalidation globale explicite.

## Décision de continuité

Après ce pilote, la prochaine décision structurante devra être l'une des suivantes :
- `bounded_run_viable_as_is`
- `bounded_run_viable_with_prompt_adjustment`
- `bounded_run_viable_with_pipeline_adjustment`
- `bounded_run_not_yet_viable`

Le but du pilote est donc autant méthodologique que documentaire.
