[1] INPUT CORE
    Constitution / Référentiel / LINK

[2] CHALLENGE
    Prompt: Challenge_constitution.md
    Sortie: Audit structuré

[3] ARBITRAGE
    Humain ou prompt d’arbitrage
    Sortie: Liste des corrections retenues

[4] PATCH SYNTHESIS
    Prompt: Make05CorePatch.md
    Sortie: PATCH_SET YAML canonique

[5] PRECHECK
    Patcher en mode dry-run / atomic
    Sortie: Rapport d’applicabilité

[6] APPLY
    apply_learnit_core_patch.py
    Sortie: fichiers modifiés + backups

[7] VALIDATION
    Prompt: Make02CoreValidation.md
    Sortie: PASS / FAIL + anomalies

[8] OPTIONAL REPAIR LOOP
    Si FAIL → nouveau patch ciblé

[9] RELEASE
    Renommage version / commit / tag