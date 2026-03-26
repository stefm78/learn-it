# Passage 2 — Promotion Status

## Objective

Passage 2 vise à :
- promouvoir des copies synchronisées des Core dans une zone canonique ;
- sortir de la dépendance aux pointeurs legacy ;
- promouvoir le vrai patcher partagé ;
- préparer la synchronisation finale des versions internes via le pipeline `release`.

## Done in this passage

- framework de pipelines posé dans `docs/`
- `docs/cores/current/` créé
- `docs/cores/releases/` créé
- copie promue synchronisée de la Constitution ajoutée dans `docs/cores/releases/constitution_v1_7.yaml`
- PR de restructuration ouverte

## Still legacy or provisional

- `docs/Current_Constitution/` reste la source legacy active
- `docs/cores/current/*.yaml` restent des pointeurs descriptifs
- `docs/patcher/shared/apply_patch.py` reste un wrapper provisoire vers le patcher legacy
- les versions internes actives des Core legacy restent encore désynchronisées (`v1.6` / `v0.5` visibles dans les métadonnées internes)

## Next target

1. promouvoir `referentiel_v0_6.yaml`
2. promouvoir `link_v1_7__v0_6.yaml`
3. promouvoir le patcher v4 complet dans `docs/patcher/shared/`
4. basculer `docs/cores/current/*.yaml` de pointeurs vers copies canoniques
5. utiliser le pipeline `release` pour synchroniser les versions internes et les aliases `current/`

## Rule

Tant que le pipeline `release` n'a pas promu les artefacts, un pipeline d'exécution doit considérer `docs/cores/current/*.yaml` comme des pointeurs et non comme des copies canoniques finalisées.
