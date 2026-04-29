from __future__ import annotations

MATURITY_AXES_COUNT = 6
MATURITY_MAX_SCORE = 24
MATURITY_LEVELS: list[tuple[str, int, int]] = [
    ("L4_strong", 21, 24),
    ("L3_operational", 17, 20),
    ("L2_usable_with_care", 13, 16),
    ("L1_fragile", 9, 12),
    ("L0_experimental", 0, 8),
]
MATURITY_MINIMUM_LEVEL = "L2_usable_with_care"
MATURITY_GATED_LEVELS = {"L0_experimental", "L1_fragile"}


def maturity_pct(score: int) -> str:
    return f"{round(score * 100 / MATURITY_MAX_SCORE)}%"


def maturity_level_from_score(score: int) -> str:
    for level_key, lo, hi in MATURITY_LEVELS:
        if lo <= score <= hi:
            return level_key
    return "L0_experimental"
