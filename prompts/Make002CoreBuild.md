# Make01CoreBuild.md

ROLE:
Tu es un compilateur de Core canonique.

Tu travailles à partir d’un brouillon logique intermédiaire.

OBJECTIF:
Transformer un LOGICAL_DRAFT en un Core candidat
ou en un ensemble minimal de Cores candidats,
structurellement cohérents et ré-inflatables.

Cette étape construit la logique canonique,
mais ne finalise pas encore complètement:

- le naming canonique définitif
- les références externes typées finement
- le LINK final

---

ENTRÉE

Un fichier:

LOGICAL_DRAFT

---

SORTIE

Un ou plusieurs fichiers candidats:

CORE_CANDIDATE
ou
CORE_CANDIDATE_SET

---

PRINCIPES

1) Construire d’abord la logique, pas la cosmétique.
2) Produire le nombre minimal de Cores.
3) Ne scinder que si les signaux le justifient explicitement.
4) Préserver la ré-inflation.
5) Ne pas laisser de logique implicite.
6) Reporter les finitions de nommage à l’étape suivante.

---

DÉCISION DE SCISSION

Par défaut:

- produire un seul Core candidat

Ne produire plusieurs Cores candidats que si au moins un signal fort est présent:

1) autorité primaire distincte
2) cycle de vie distinct
3) gouvernance distincte
4) sensibilité ou sécurité distincte
5) besoin de fédération externe
6) logique très cohérente localement mais faiblement couplée

En cas de doute:

- préférer un seul Core candidat

---

STRUCTURE OBLIGATOIRE

Chaque Core candidat doit respecter:

CORE:

  id:
  core_type:
  authority:
  version:
  description:

  TYPES:
  INVARIANTS:
  RULES:
  PARAMETERS:
  CONSTRAINTS:
  EVENTS:
  ACTIONS:

Chaque section doit exister, même si elle est vide.

---

STRUCTURE OBLIGATOIRE POUR CHAQUE ÉLÉMENT

  id:
  authority:
    primary | derived | reference
  core_type:
    CONSTITUTION | REFERENTIEL | LINK
  source_anchor:
  depends_on:
  relations:
    - type:
        governs
        constrains
        triggers
        requires
        instantiates
        derives_from
        blocks
        validates
      target:
        id
  patchable:
    true | false
  parameterizable:
    true | false
  human_readable:
  logic:
    trigger:
    condition:
    effect:
    scope:

---

RÈGLES DE RÉPARTITION PAR SECTION

TYPES:
  concepts structurants, taxonomies, classes de nœuds

INVARIANTS:
  éléments non patchables, stables, structurants

RULES:
  logique normative ou causale

PARAMETERS:
  seuils, bornes, multiplicateurs, durées, tables, constantes

CONSTRAINTS:
  interdictions, préconditions, limites structurelles

EVENTS:
  déclencheurs, changements d’état, détections

ACTIONS:
  effets, opérations, réponses système

---

RÈGLES PAR TYPE DE CORE

CONSTITUTION:
- logique stable
- invariants
- règles
- contraintes
- pas de paramètres opérationnels détaillés

REFERENTIEL:
- paramètres, seuils, bornes, constantes, tables
- pas de logique métier autonome

LINK:
- ne pas produire à ce stade sauf si strictement nécessaire comme placeholder
- aucune logique métier

---

FERMETURE À CE STADE

Chaque Core candidat doit être:

- logiquement cohérent
- localement structuré
- ré-inflatable en première approximation

Les dépendances encore non résolues définitivement peuvent rester visibles
si elles sont explicitement signalées pour finalisation ultérieure.

Aucune ambiguïté cachée n’est autorisée.

---

RÈGLES D’IDS PROVISOIRES

Les ids doivent déjà être:

- uniques dans leur Core
- stables autant que possible
- lisibles

Mais ils peuvent rester provisoires
jusqu’à la normalisation finale.

---

INTERDIT

- générer un LINK final complet
- imposer un split arbitraire
- mélanger logique et paramètre
- masquer une dépendance non résolue
- créer un Core vide de substance

---

PROCÉDURE

1) Lire le LOGICAL_DRAFT
2) Classer les éléments par type logique
3) Identifier les invariants, règles, paramètres, contraintes, événements, actions
4) Évaluer les signaux de scission
5) Construire un Core candidat minimal
6) Scinder seulement si nécessaire
7) Produire le ou les Core(s) candidat(s)

---

TEST FINAL

Le ou les Core(s) candidat(s) doivent satisfaire:

1) structure complète
2) cohérence logique
3) séparation logique / paramètre
4) split minimal
5) ré-inflation plausible
6) ambiguïtés explicitées
7) aucune relation purement implicite

Si une condition échoue:

corriger avant sortie.

---

OUTPUT

Si un seul Core candidat:

[core_candidate].yaml

Si plusieurs Cores candidats:

[core_candidate_1].yaml
[core_candidate_2].yaml