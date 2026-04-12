# Core validation report — bounded run `learner_state`

Run ID: `CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01`
Stage: `STAGE_06_CORE_VALIDATION`
Mode: `bounded_local_run`

## Résumé

Validation locale du scope : `PASS`
Validation globale canonique : `NON CLEARED`

Le patch appliqué dans le run borné reste cohérent avec le périmètre `learner_state` et avec la séparation Constitution / Référentiel / LINK. Le succès observé ici est un succès local de validation du scope, pas une autorisation implicite de release ou de promotion.

## Vérifications effectuées

- présence des trois snapshots patchés sous `work/05_apply/patched/`
- effet de patch conforme à l’arbitrage Stage 02
- aucune dérive latérale visible dans le Référentiel
- aucune dérive latérale visible dans le LINK
- séparation Constitution / Référentiel / LINK préservée
- aucune modification hors du fichier en scope autorisé
- aucune régression locale évidente sur les dépendances ou bindings relus dans le voisinage logique

## Constat principal

La seule modification effective du run est bien la clarification locale de `RULE_MULTI_AXIS_UNKNOWN_OR_UNOBSERVABLE_SAFE_ENTRY` dans la Constitution patchée.

Cette clarification :
- reste strictement dans le scope déclaré ;
- ne déplace pas de seuil référentiel dans la Constitution ;
- ne résout pas le sujet AR-N1 / AR-N3, qui reste explicitement hors patch courant et doit conserver ce statut.

## Limites assumées du Stage 06

Ce stage ne vaut pas clearance globale d’intégration.

Restent explicitement hors validation globale à ce stade :
- la relecture canonique complète des Core actifs ;
- la revalidation croisée exhaustive des références inter-Core ;
- la revalidation globale des invariants ;
- la vérification de collisions éventuelles avec d’autres runs parallèles ;
- toute décision de release ou de promotion.

## Conclusion

Le Stage 06 peut être considéré comme `PASS` au niveau **local scope validation**.

L’`integration_gate` doit toutefois rester **bloqué** pour toute suite de type release/promotion tant que les contrôles globaux demandés par le run n’ont pas été explicitement rejoués.
