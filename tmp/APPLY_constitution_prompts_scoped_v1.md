# Apply — scoped constitution prompts v1

Depuis la racine du repo, remplacer les prompts existants par les versions préparées dans `tmp/` :

```bash
cp ./tmp/Challenge_constitution_scoped_v1.md ./docs/prompts/shared/Challenge_constitution.md
cp ./tmp/Make04ConstitutionArbitrage_scoped_v1.md ./docs/prompts/shared/Make04ConstitutionArbitrage.md
```

Puis vérifier le diff :

```bash
git diff -- docs/prompts/shared/Challenge_constitution.md docs/prompts/shared/Make04ConstitutionArbitrage.md
```

Objectif de ce remplacement :
- rendre les prompts compatibles avec le mode nominal global ;
- ajouter un mode borné piloté par `scope_manifest` et `impact_bundle` ;
- rendre explicite la gestion des constats `in_scope`, `out_of_scope_but_relevant` et `needs_scope_extension` ;
- empêcher qu'un arbitrage ou un challenge borné dérive silencieusement hors périmètre.

Après application du remplacement, la prochaine action recommandée est :
- synchroniser `STATUS.yaml` et `WORKLOG.md` avec l'avancement réel ;
- préparer un premier pilote borné sur un sous-ensemble simple de la Constitution.
