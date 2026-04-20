#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


TARGET = Path("docs/patcher/shared/reconcile_run.py")
BACKUP = Path("tmp/reconcile_run.py.bak_before_literal_newline_repair")


def detect_newline(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    if "\r" in text:
        return "\r"
    return "\n"


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def restore_newlines(text: str, newline: str) -> str:
    return text.replace("\n", newline)


def repair_literal_newline_corruption(text: str) -> str:
    text = normalize_newlines(text)

    # Cas cassé explicite vu dans le fichier:
    #   import fnmatch\n
    text = text.replace("import fnmatch\\n\n", "import fnmatch\n")
    text = text.replace("import fnmatch\\n", "import fnmatch\n")

    repaired_lines = []
    for line in text.split("\n"):
        # Certaines lignes sont littéralement "\n"
        if line == r"\n":
            repaired_lines.append("")
            continue

        # D'autres commencent par un ou plusieurs préfixes littéraux "\n"
        while line.startswith(r"\n"):
            line = line[2:]

        repaired_lines.append(line)

    repaired = "\n".join(repaired_lines)

    # Normalisation légère des triples sauts de ligne excessifs éventuellement introduits
    while "\n\n\n\n" in repaired:
        repaired = repaired.replace("\n\n\n\n", "\n\n\n")

    return repaired


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Missing target file: {TARGET}")

    raw = TARGET.read_text(encoding="utf-8")
    newline = detect_newline(raw)

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_text(raw, encoding="utf-8")

    repaired = repair_literal_newline_corruption(raw)

    TARGET.write_text(restore_newlines(repaired, newline), encoding="utf-8")

    print(f"Backup written to: {BACKUP}")
    print(f"Repaired: {TARGET}")

    repaired_check = TARGET.read_text(encoding="utf-8")
    remaining_literal_prefix_lines = sum(
        1
        for line in normalize_newlines(repaired_check).split("\n")
        if line.startswith(r"\n") or line == r"\n"
    )
    print(f"Remaining suspicious literal-\\\\n line prefixes: {remaining_literal_prefix_lines}")


if __name__ == "__main__":
    main()