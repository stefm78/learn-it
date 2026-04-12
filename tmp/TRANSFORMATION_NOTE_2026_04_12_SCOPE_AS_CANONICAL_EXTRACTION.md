# Transformation note — 2026-04-12 — Scope as canonical extraction

## Contexte

Cette note capture un point architectural important de la transformation `core_modularization`, afin de permettre une reprise fiable par une autre IA sans dépendre du contexte implicite d'une conversation.

## Décision clarifiée

Les scopes du pipeline `constitution` doivent être compris comme des **extractions gouvernées** ou **vues dérivées** des fichiers canoniques, et non comme de nouvelles sources autonomes.

En particulier :
- les fichiers canoniques restent :
  - `docs/cores/current/constitution.yaml`
  - `docs/cores/current/referentiel.yaml`
  - `docs/cores/current/link.yaml`
- les fichiers sous `docs/pipelines/constitution/scope_catalog/scope_definitions/` décrivent des sous-ensembles logiques dérivés de ces sources ;
- les runs bornés consomment ces scopes dérivés, mais ne remplacent pas l'autorité canonique des Core.

## Interprétation correcte de `source_artifacts`

Le champ `source_artifacts` doit être lu d'abord comme une **provenance** :
- il documente les sources canoniques utilisées pour dériver le scope ;
- il n'implique pas nécessairement qu'une IA doive relire intégralement tous ces fichiers à chaque exécution ;
- il reste acceptable que `source_artifacts` référence les trois Core complets tant qu'on parle de provenance et non de payload de lecture minimal.

## Problème encore ouvert

Le vrai sujet non résolu est la **réduction effective de la surface de lecture**.

Aujourd'hui, une partie importante du modèle reste encore trop `files-first` :
- `target.files` pointe encore souvent vers un Core complet ;
- `default_neighbors_to_read.files` pointe encore vers `referentiel.yaml` et `link.yaml` complets ;
- donc la gouvernance du scope progresse plus vite que la réduction réelle du coût de contexte.

Conclusion :
- le modèle actuel améliore déjà le **droit d'action** et la **focalisation logique** ;
- mais il ne réduit pas encore suffisamment le **payload documentaire réellement à lire**.

## Conséquence architecturale

La prochaine étape de transformation ne doit pas d'abord consister à modifier `source_artifacts`.

La vraie cible est de passer progressivement vers un modèle où les scopes deviennent **ids-first** ou **projection-first**, par exemple via :
- `target.ids` comme unité primaire de lecture ;
- `logical_neighbors_to_read.ids` comme voisinage minimal ;
- des projections minimales dérivées ;
- ou des bundles d'extraits ciblés stables et traçables.

## Guardrails

1. Les scopes restent dérivés du canon ; ils ne deviennent pas une seconde source de vérité.
2. Toute évolution significative des Core canoniques doit conduire à une revalidation ou régénération des scopes concernés.
3. Le chantier principal de modularisation ne doit pas confondre :
   - **provenance canonique**
   - **périmètre d'écriture autorisé**
   - **payload de lecture minimal**
4. Le fait qu'un scope référence encore des fichiers complets n'invalide pas le modèle ; cela montre seulement que la transformation est encore intermédiaire.

## Impact sur le suivi de transformation

Cette clarification doit être considérée comme un complément explicite au point déjà identifié dans la transformation :
- les scopes ont déjà réduit la gouvernance ;
- la réduction effective de contexte reste à traiter comme chantier d'architecture à part entière.

## Prochaine action utile

Quand le chantier pipeline sera stabilisé côté opératoire, faire évoluer le catalogue de scopes et/ou le contrat de run pour introduire un niveau de lecture plus fin que `files`, sans casser la traçabilité vers les sources canoniques.
