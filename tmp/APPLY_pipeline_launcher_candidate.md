# Apply — pipeline launcher candidate

Le launcher candidat unique est désormais :
- `tmp/pipeline_launcher.py`

## 1. Utiliser le launcher candidat

```bash
python ./tmp/pipeline_launcher.py --repo-root . --pipeline constitution --branch feat/core-modularization-bootstrap
```

## 2. Nettoyer les anciennes versions expérimentales

```bash
rm -f \
  ./tmp/pipeline_launcher_bootstrap.py \
  ./tmp/pipeline_launcher_bootstrap_v2.py \
  ./tmp/pipeline_launcher_bootstrap_v3.py \
  ./tmp/pipeline_launcher_bootstrap_v4.py \
  ./tmp/pipeline_launcher_bootstrap_v5.py \
  ./tmp/pipeline_launcher_bootstrap_v6.py
```

## 3. Vérifier l'état du repo

```bash
git status --short
```

## 4. Étape suivante recommandée

Quand le comportement du launcher candidat est jugé stable :
- le promouvoir hors de `tmp/`
- idéalement vers `docs/patcher/shared/`
- puis le brancher à un flux de lancement de pipeline plus canonique
