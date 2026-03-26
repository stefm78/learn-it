# Passage 2 — Promotion Status

## Objective

Passage 2 visait à :
- promouvoir des copies synchronisées des Core dans une zone canonique ;
- sortir de la dépendance aux pointeurs legacy ;
- promouvoir le patcher partagé v4 ;
- préparer une release/promotion traçable par patch.

## Done

- framework de pipelines posé dans `docs/`
- `docs/cores/current/` créé et désormais promu en copies canoniques
- `docs/cores/releases/` alimenté avec :
  - `constitution_v1_7.yaml`
  - `referentiel_v0_6.yaml`
  - `link_v1_7__v0_6.yaml`
- `docs/patcher/shared/apply_patch.py` synchronisé avec le moteur v4
- `docs/patcher/shared/validate_patchset.py` synchronisé avec le validateur v4
- couche `Release Patch DSL` ajoutée pour les promotions de repo

## Remaining legacy

- `docs/Current_Constitution/` reste conservé comme historique/compatibilité
- `docs/make_constitution/` reste legacy tant qu’une migration explicite n’est pas décidée

## Result

Le Passage 2C est finalisé fonctionnellement :
- les Core courants sont canoniques ;
- les outils partagés sont alignés ;
- la promotion future de `current/` passe par release patch.
