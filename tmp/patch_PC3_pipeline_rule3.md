# Patch PC-3 — pipeline.md Rule 3

## Fichier cible
`docs/pipelines/platform_factory/pipeline.md`

## Section concernée
`## Operating doctrine > ### Rule 3 — Released baseline posture`

## Texte actuel

```
### Rule 3 — Released baseline posture
The current `platform_factory` artifacts are considered a released baseline.
A new pipeline run does not start with a discovery audit of an unknown object.
It starts by challenging the released baseline and deciding whether corrections are required.
```

## Texte de remplacement

```
### Rule 3 — Released baseline posture
The current `platform_factory` artifacts are considered a governed working baseline.
They are not yet officially manifest-integrated.
Manifest integration is completed explicitly at STAGE_08 of each formal release cycle,
and constitutes the exit condition for PF_BLOCKER_CURRENT_MANIFEST_SCHEMA_LIMITATION.
A new pipeline run does not start with a discovery audit of an unknown object.
It starts by challenging the released baseline and deciding whether corrections are required.
```

## Justification
Arbitrage PC-3 — 2026-04-10.
Aligne la doctrine pipeline avec la réalité de gouvernance : les artefacts factory sont
dans `docs/cores/current/` mais ne sont pas encore intégrés au manifest officiel.
La mise à jour manifest est un acte explicite de STAGE_08, pas un effet de bord implicite.

## Statut
Prêt pour application dans `docs/pipelines/platform_factory/pipeline.md`.
À appliquer avant le prochain cycle de challenge.
