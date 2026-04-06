# Platform Factory Release Candidate Notes

## Release

- **Release ID** : `PLATFORM_FACTORY_RELEASE_2026_04_06_R01`
- **Date** : 2026-04-06
- **Change depth** : `minor` (0.1.0 → 0.2.0)
- **Promotion candidate** : `true`

## Artefacts

| Rôle | Version source | Version release |
|---|---|---|
| `platform_factory_architecture` | 0.1.0 | 0.2.0 |
| `platform_factory_state` | 0.1.0 | 0.2.0 |

## Changements couverts

Issus des décisions d'arbitrage PFARB-DEC-01, 02, 03, 06 (patchset V0) :

- **PFARB-DEC-01** : Formalisation du contrat de projection dérivée validée dans `contracts.execution_projection_contract`
- **PFARB-DEC-02** : Renforcement des `generated_projection_rules.minimum_requirements` (8 items)
- **PFARB-DEC-03** : Renforcement des `build_and_packaging_rules` avec exigences de snapshot manifest-ready
- **PFARB-DEC-06** : Enrichissement de `capabilities_absent`, `derived_projection_conformity_status` et `produced_application_contract_status` dans le state

## Éléments exclus (différés ou rejetés)

- PFARB-DEC-04 (différé) : schema fin du manifest
- PFARB-DEC-05 (différé) : emplacement des projections
- PFARB-DEC-07 (rejeté) : hors scope V0

## Statut

`RELEASE_CANDIDATE` — prête pour promotion Stage 08.

`docs/cores/current/` non modifié à ce stage.
