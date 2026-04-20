from pathlib import Path

path = Path("docs/patcher/shared/closeout_pipeline_run.py")
text = path.read_text(encoding="utf-8")

old = '        help="Path to arbitrage report (default: docs/pipelines/constitution/work/arbitrage.md)",\n'
new = '        help="Path to arbitrage report (default: <work-root>/arbitrage.md)",\n'

if old not in text:
    raise SystemExit("Ligne help --arbitrage-path introuvable")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("OK")