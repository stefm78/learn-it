# Legacy paths preserved

Ces chemins sont conservés pour compatibilité et archivage :

- `docs/Current_Constitution/`
- `docs/constitution/`
- `docs/referentiel/`
- `docs/make_constitution/`
- `prompts/`

## Règle

- Ne pas supprimer brutalement ces chemins tant que les nouveaux alias canoniques ne sont pas validés.
- Les nouveaux pipelines doivent pointer vers `docs/cores/current/`, `docs/prompts/shared/`, `docs/patcher/shared/` et `docs/specs/patch-dsl/current.md`.
- Toute migration ou suppression future doit passer par le pipeline `migration` ou `release`.
