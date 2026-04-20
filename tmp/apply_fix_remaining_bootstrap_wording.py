from pathlib import Path

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"[ERREUR] Bloc introuvable pour {label}")
    return text.replace(old, new, 1)

# -------------------------------------------------------------------
# 1) PIPELINE_MODEL.yaml
# -------------------------------------------------------------------
p = Path("docs/pipelines/constitution/PIPELINE_MODEL.yaml")
text = p.read_text(encoding="utf-8")

text = replace_once(
    text,
    "    - consume run_context first when present\n",
    "    - consume run_context first when present only after explicit run selection or when run_id is already known\n",
    "PIPELINE_MODEL external_orchestration responsibility",
)

text = replace_once(
    text,
    "    orchestration_scope: pipeline_or_single_run\n",
    "    orchestration_scope: run_or_pipeline\n",
    "PIPELINE_MODEL STAGE_08 orchestration_scope harmonization",
)

p.write_text(text, encoding="utf-8")
print("OK: PIPELINE_MODEL.yaml corrigé")

# -------------------------------------------------------------------
# 2) STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml
# -------------------------------------------------------------------
p = Path("docs/pipelines/constitution/stages/STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml")
text = p.read_text(encoding="utf-8")

text = replace_once(
    text,
    """  justification: >-
    Ce stage clôt un run déjà promu. Le modèle doit vérifier que les artefacts
    de promotion sont cohérents, que le closeout scripté a bien été exécuté,
    et que le run est prêt à sortir proprement du cycle actif sans ambiguïté.
""",
    """  justification: >-
    Ce stage clôt un cycle opératoire déjà promu, soit au niveau d'un run,
    soit au niveau pipeline-level. Le modèle doit vérifier que les artefacts
    de promotion sont cohérents, que le closeout scripté a bien été exécuté,
    et que la clôture est propre et sans ambiguïté dans le mode courant.
""",
    "STAGE_09 model_requirements justification",
)

text = replace_once(
    text,
    """  tracking_closure_rule: >-
    Le closeout scripté ne ferme pas à lui seul le tracking du run. Après un
    PASS du stage, l'humain doit exécuter update_run_tracking.py pour passer le
    run à status=closed et vider next_stage. Le stage n'est complètement
    convergent qu'une fois cette fermeture de tracking effectuée.
""",
    """  tracking_closure_rule: >-
    En bounded_local_run, le closeout scripté ne ferme pas à lui seul le tracking
    du run. Après un PASS du stage, l'humain doit exécuter update_run_tracking.py
    pour passer le run à status=closed et vider next_stage. En modes
    parallel_consolidation, nominal_global et bounded_transition, aucun tracking
    run-level supplémentaire n'est requis : le stage est convergent dès que les
    artefacts pipeline-level de closeout sont validés.
""",
    "STAGE_09 tracking_closure_rule",
)

text = replace_once(
    text,
    """  description: >-
    Si le script n'a pas été exécuté réellement, l'humain doit lancer la
    commande émise puis relancer l'IA sur ce stage. Une fois la clôture validée,
    le tracking du run doit encore être fermé explicitement via
    update_run_tracking.py.
""",
    """  description: >-
    Si le script n'a pas été exécuté réellement, l'humain doit lancer la
    commande émise puis relancer l'IA sur ce stage. En bounded_local_run,
    une fois la clôture validée, le tracking du run doit encore être fermé
    explicitement via update_run_tracking.py. En modes pipeline-level,
    aucune fermeture de tracking run-level supplémentaire n'est requise.
""",
    "STAGE_09 human_actions_required description",
)

text = replace_once(
    text,
    """  on_pass:
    next_stage: ENTRY_RESOLUTION
    precondition: human must confirm update_run_tracking.py execution
""",
    """  on_pass:
    next_stage: ENTRY_RESOLUTION
    precondition: >-
      En bounded_local_run, human must confirm update_run_tracking.py execution.
      En parallel_consolidation, nominal_global et bounded_transition,
      aucun tracking run-level supplémentaire n'est requis.
""",
    "STAGE_09 allowed_transitions on_pass precondition",
)

p.write_text(text, encoding="utf-8")
print("OK: STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml corrigé")

print("\\nTerminé.")
print("Fichiers modifiés :")
print("- docs/pipelines/constitution/PIPELINE_MODEL.yaml")
print("- docs/pipelines/constitution/stages/STAGE_09_CLOSEOUT_AND_ARCHIVE.skill.yaml")