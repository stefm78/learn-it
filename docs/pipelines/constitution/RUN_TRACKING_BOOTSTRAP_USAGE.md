# Constitution — first use of `update_run_tracking.py`

## Objet

Ce document précise **quand** et **comment** utiliser une première fois le script `docs/patcher/shared/update_run_tracking.py` pour simplifier le démarrage d'un run.

---

## Réponse courte

Oui.

Une première utilisation du script est utile **juste après la décision d'entrée** :
- une fois qu'on a décidé de **continuer un run existant** ou **ouvrir un nouveau run** ;
- avant de charger le contexte profond du stage ;
- avant de produire les artefacts métier du stage.

Cela permet de matérialiser proprement :
- que le run a bien été sélectionné ;
- quel stage devient actif ;
- que le suivi de `runs/index.yaml` est cohérent ;
- qu'une autre IA peut reprendre immédiatement sans réinterpréter le point d'entrée.

---

## Quand le faire

### Cas A — reprise d'un run existant
Faire un appel de bootstrap juste après avoir résolu :
- `resume_existing_run`

But :
- marquer explicitement le stage repris comme `in_progress` ;
- matérialiser que la décision d'entrée est levée.

### Cas B — création d'un nouveau run
Faire un appel de bootstrap juste après :
- création du `run_manifest.yaml`
- matérialisation des inputs du run

But :
- déclarer le premier stage actif ;
- initialiser proprement le tracking.

---

## Commande recommandée — reprise d'un run existant

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id CONSTITUTION_RUN_2026_04_11_LEARNER_STATE_R01 \
  --stage-id STAGE_01_CHALLENGE \
  --stage-status in_progress \
  --run-status active \
  --next-stage STAGE_01_CHALLENGE \
  --scope-status confirmed_for_bounded_run \
  --summary "Entry decision resolved; resuming existing learner_state run at Stage 01"
```

---

## Commande recommandée — nouveau run

```bash
python docs/patcher/shared/update_run_tracking.py \
  --pipeline constitution \
  --run-id <NEW_RUN_ID> \
  --stage-id STAGE_01_CHALLENGE \
  --stage-status in_progress \
  --run-status active \
  --next-stage STAGE_01_CHALLENGE \
  --scope-status draft \
  --summary "Entry decision resolved; new run opened and Stage 01 started"
```

---

## Pourquoi c'est utile

Sans ce premier appel :
- le run peut exister mais rester ambigu dans l'index ;
- une autre IA peut devoir re-résoudre l'entrée ;
- le passage de `bootstrap_open` à `active` peut rester implicite.

Avec ce premier appel :
- le point d'entrée est acté ;
- le stage courant est visible ;
- la reprise devient plus simple et plus déterministe.

---

## Limite

Ce bootstrap tracking ne remplace pas la vraie clôture de stage.

Il sert à :
- **déclarer le stage comme commencé**.

Puis, à la fin du stage, il faut toujours exécuter un second appel avec :
- `stage-status done` ou `blocked` ou `failed`
- et le `next-stage` réel.

---

## Décision de design

Pour `constitution`, il est recommandé d'utiliser `update_run_tracking.py` une première fois au moment où la décision d'entrée est levée, afin de transformer une résolution implicite en état de run explicite et traçable.
