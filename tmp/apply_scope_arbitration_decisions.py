#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ARBITRATION_PATH = Path("tmp/scope_lab/scope_redesign_arbitration.yaml")
SUMMARY_PATH = Path("tmp/scope_lab/scope_redesign_arbitration_summary.md")


DECISIONS = {
    "MACRO_001_REFERENTIEL_LINK_UNOWNED_CLASSIFICATION": {
        "arbitration_status": "accepted",
        "selected_option": "declare_referentiel_and_link_as_read_only_external_cores",
        "rationale": (
            "Les IDs referentiel/link ne doivent pas être forcés artificiellement dans les scopes Constitution. "
            "Ils constituent des surfaces de référence et de liaison inter-core, lues par les runs constitution "
            "mais non possédées par eux, sauf décision explicite."
        ),
        "canonicalization_action": (
            "Introduire une politique explicite de classification des IDs referentiel/link : external_read_only_core "
            "pour les IDs lus mais non possédés par la Constitution, shared/global seulement si nécessaire, et ownership "
            "par un scope constitution uniquement lorsqu'il existe une responsabilité de gouvernance réelle. Le validateur "
            "de bijection devra distinguer les IDs constitution-owned des IDs external_read_only."
        ),
    },
    "MACRO_006_SCOPE_BOUNDARY_REVIEW": {
        "arbitration_status": "accepted",
        "selected_option": "redesign_patch_lifecycle_first",
        "rationale": (
            "Les cinq scopes actuels montrent des signaux de revue, mais une refonte globale serait trop risquée. "
            "patch_lifecycle est le meilleur stress-test car il combine un cœur structurel clair avec des frontières "
            "difficiles autour des déclencheurs, du learner_state et des signaux runtime."
        ),
        "canonicalization_action": (
            "Utiliser patch_lifecycle comme premier scope pilote pour valider la méthode graph-based. Les autres scopes "
            "restent temporairement inchangés, avec leurs anomalies conservées comme backlog d'arbitrage."
        ),
    },
    "MACRO_002_PATCH_LIFECYCLE_CORE_STRUCTURE": {
        "arbitration_status": "accepted",
        "selected_option": "name_as_patch_structure_subcluster",
        "rationale": (
            "Le graphe montre un cœur patch_lifecycle très cohérent autour de TYPE_PATCH_ARTIFACT, "
            "TYPE_PATCH_IMPACT_SCOPE, TYPE_PATCH_QUALITY_GATE, rollback, validation locale et rejet des patches invalides. "
            "Ce bloc ne doit pas être séparé immédiatement en scope autonome, mais il doit être nommé comme sous-grappe "
            "diagnostique stable."
        ),
        "canonicalization_action": (
            "Conserver ces IDs dans patch_lifecycle. Ajouter une classification ou note de sous-grappe nommée "
            "patch_structure_and_quality dans les artefacts de Scope Lab, puis éventuellement dans la policy de scoping "
            "si la méthode est validée."
        ),
    },
    "MACRO_003_PATCH_TRIGGER_BOUNDARY": {
        "arbitration_status": "accepted",
        "selected_option": "keep_triggers_in_patch_lifecycle_with_neighbors",
        "rationale": (
            "Les déclencheurs de patch sont proches de learner_state dans le graphe, mais ils représentent des décisions "
            "gouvernées de cycle de vie du patch : déclencher un patch de relevance, déclencher une sollicitation AR, "
            "ou escalader une dérive persistante. Leur ownership doit donc rester dans patch_lifecycle, tandis que les "
            "signaux d'état apprenant doivent être lus comme neighbors explicites."
        ),
        "canonicalization_action": (
            "Conserver les règles/événements/actions de déclenchement dans patch_lifecycle. Déclarer explicitement les IDs "
            "learner_state nécessaires comme neighbors. Créer si besoin une sous-grappe diagnostique patch_trigger_governance."
        ),
    },
}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def main() -> int:
    doc = load_yaml(ARBITRATION_PATH)
    root = doc["scope_redesign_arbitration"]

    for macro in root.get("macro_decisions", []):
        macro_id = macro.get("macro_decision_id")
        if macro_id in DECISIONS:
            macro["status"] = "arbitrated"
            macro["human_decision"] = DECISIONS[macro_id]

    accepted = []
    pending = []

    for macro in root.get("macro_decisions", []):
        decision = macro.get("human_decision", {})
        if decision.get("arbitration_status") == "accepted":
            accepted.append(macro)
        else:
            pending.append(macro)

    root["status"] = "PARTIALLY_ARBITRATED"
    root["summary"]["accepted_macro_decision_count"] = len(accepted)
    root["summary"]["pending_macro_decision_count"] = len(pending)

    ARBITRATION_PATH.write_text(dump_yaml(doc), encoding="utf-8")

    lines = [
        "# Scope redesign arbitration summary",
        "",
        "Status: PARTIALLY_ARBITRATED",
        "",
        "## Accepted macro-decisions",
        "",
    ]

    for macro in accepted:
        decision = macro["human_decision"]
        lines.extend(
            [
                f"### {macro['macro_decision_id']}",
                "",
                f"- Title: {macro['title']}",
                f"- Selected option: `{decision['selected_option']}`",
                f"- Canonicalization action: {decision['canonicalization_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Pending macro-decisions",
            "",
        ]
    )

    for macro in pending:
        lines.append(f"- {macro['macro_decision_id']} — {macro['title']}")

    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"updated: {ARBITRATION_PATH}")
    print(f"written: {SUMMARY_PATH}")
    print(f"accepted={len(accepted)} pending={len(pending)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
