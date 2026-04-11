# Worklog — transformation modularisation des Core

## Règle d'usage

Ce journal est append-only.
Chaque entrée doit rester courte, factuelle, datée, et permettre une reprise sans contexte de conversation.

Format recommandé :
- Date
- Auteur ou mode (`human`, `ai`, `human+ai`)
- Changement effectué
- Décision prise
- Prochaine action utile

---

## 2026-04-11 — bootstrap initial

- Mode : `human+ai`
- Branche créée : `feat/core-modularization-bootstrap`
- Artefacts ajoutés :
  - `docs/transformations/core_modularization/README.md`
  - `docs/transformations/core_modularization/ROADMAP.md`
  - `docs/transformations/core_modularization/STATUS.yaml`
  - `docs/transformations/core_modularization/WORKLOG.md`

### Décisions prises

1. La transformation doit être pilotée depuis le repo, pas depuis le contexte implicite d'une conversation.
2. Le repo ne doit pas exploser en nombre de pipelines ni de prompts.
3. La cible est un régime :
   - sources modulaires gouvernées,
   - bundle canonique compilé,
   - projections dérivées validées,
   - pipelines capables de traiter des scopes bornés,
   - intégration globale centralisée avant promotion.
4. Le strict nécessaire posé à ce stade est un socle de continuité et de pilotage, pas une refonte technique immédiate.

### État constaté

- Le chantier est amorcé mais aucun contrat de scope n'est encore matérialisé.
- Aucun pipeline n'a encore été rendu scope-aware.
- Aucun artefact canonique n'a encore été modularisé effectivement.

### Prochaine action utile

Définir le premier jalon J1 :
- `scope_manifest`
- `impact_bundle`
- `integration_gate`

Puis déterminer le delta minimal à apporter au pipeline `constitution` pour supporter un premier run borné.
