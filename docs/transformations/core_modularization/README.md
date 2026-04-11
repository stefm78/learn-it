# Transformation — modularisation des Core et adaptation des pipelines

## Objet

Ce répertoire porte le pilotage minimal de la transformation visant à :
- rendre les artefacts canonique plus maniables sans diminuer la rigueur ;
- introduire un régime **sources modulaires -> bundle canonique compilé -> projections dérivées validées** ;
- faire évoluer les pipelines `constitution` et `platform_factory` pour qu'ils puissent traiter des **sous-ensembles bornés** ;
- préparer un mode de travail plus parallèle entre IA, sans perdre la cohérence canonique globale.

## Branche de travail

- Branche dédiée : `feat/core-modularization-bootstrap`
- Point de départ : baseline `main` active au moment de l'initialisation de cette transformation.

## Point d'entrée unique pour reprise

Toute IA ou tout opérateur qui reprend ce chantier doit lire dans cet ordre :
1. `docs/transformations/core_modularization/README.md`
2. `docs/transformations/core_modularization/ROADMAP.md`
3. `docs/transformations/core_modularization/STATUS.yaml`
4. `docs/transformations/core_modularization/WORKLOG.md`

Ce répertoire doit suffire à comprendre :
- où en est le chantier ;
- ce qui a été décidé ;
- ce qui reste à faire ;
- la prochaine action utile et sûre.

## Artefacts de pilotage

- `ROADMAP.md` : vision d'ensemble, phases, livrables, critères de sortie.
- `STATUS.yaml` : état machine-readable du chantier.
- `WORKLOG.md` : journal append-only de continuité/handover.

## Principes de transformation

1. **Le canon publié reste unique** tant que la nouvelle chaîne de compilation n'est pas fiabilisée.
2. **Aucune baisse de rigueur** : modularisation ne signifie pas relâchement de la validation.
3. **Les pipelines actuels restent la référence opérationnelle** tant qu'un nouveau régime n'est pas explicitement validé.
4. **Le parallélisme porte sur les scopes de travail**, pas sur la vérité canonique finale.
5. **La promotion reste centralisée** : une seule vue active promue à la fois.
6. **Toute reprise doit s'appuyer sur le repo, pas sur un contexte implicite de conversation.**

## Règles minimales de continuité

À chaque étape significative, mettre à jour :
- `STATUS.yaml` pour l'état courant ;
- `WORKLOG.md` avec une entrée datée, concise et factuelle.

Ne pas disperser l'état du chantier dans des messages ad hoc ou des notes non référencées.

## Strict nécessaire posé par ce bootstrap

Ce bootstrap ne fait volontairement pas encore :
- la refonte complète des pipelines ;
- la modularisation effective des Core ;
- l'implémentation des validateurs et compileurs.

Il pose seulement le socle minimal de pilotage pour rendre la transformation :
- traçable ;
- reprenable ;
- découpable ;
- gouvernable par plusieurs IA successives.

## Prochaine cible immédiate

Première itération attendue après ce bootstrap :
- définir le **modèle cible minimal** des sources modulaires ;
- définir les **artefacts de scope** nécessaires aux pipelines (`scope_manifest`, `impact_bundle`, `integration_gate`) ;
- décider le **niveau minimal de changement** à apporter d'abord au pipeline `constitution` avant d'étendre à `platform_factory`.
