# CoreNamingPolicy.md

ROLE:
Tu es un normalisateur d’identifiants logiques.

OBJECTIF:
Définir une convention canonique de nommage
pour garantir l’unicité, la lisibilité machine
et la stabilité structurelle des ids
dans tout système de Core.

---

PRINCIPES

1) Un id doit être reconnaissable sans contexte.
2) Un id doit être déterministe.
3) Un id doit être stable dans le temps.
4) Un id ne doit jamais être ambigu.
5) Un id doit être compatible multi-Core.

---

FORMAT GÉNÉRAL

<TYPE>_<OBJECT>[_QUALIFIER]

Exemples:

TYPE_USER
INV_LAYER_SEPARATION
RULE_PATCH_VALIDATION
PARAM_MAX_RETRY
EVENT_PATCH_REQUEST
ACTION_APPLY_PATCH

---

PRÉFIXES AUTORISÉS

TYPE
INV
RULE
PARAM
CONST
EVENT
ACTION
REF
LINK
CORE

---

RÈGLES

Les identifiants doivent:

- être en majuscules
- utiliser "_" comme séparateur
- ne contenir aucun espace
- ne contenir aucun caractère spécial
- être uniques dans le système
- être déterministes

---

IDENTIFIANTS DE CORE

Format obligatoire:

<ROLE>_CORE

Exemples:

CONSTITUTION_CORE
REFERENTIEL_CORE
LINK_CORE
SECURITY_CORE
GOVERNANCE_CORE

---

IDENTIFIANTS DE LINK

Format obligatoire:

LINK_<SOURCE_CORE>_<TARGET_CORE>

Exemples:

LINK_CONSTITUTION_REFERENTIEL
LINK_SECURITY_EXECUTION
LINK_GOVERNANCE_INFRASTRUCTURE

---

IDENTIFIANTS DE RÉFÉRENCE

Format obligatoire:

REF_<TYPE>_<OBJECT>

Exemples:

REF_RULE_PATCH_OPERATION
REF_EVENT_PRIORITY_VERIFICATION
REF_ACTION_HIGH_LEVEL_TASK
REF_INV_MSC_MODEL

---

INTERDIT

- minuscules
- espaces
- accents
- caractères spéciaux
- préfixes non définis
- noms ambigus
- REF_* non typé

---

STABILITÉ

Un identifiant ne doit pas changer sans justification structurelle.

Le changement d’un identifiant doit être traité
comme une modification structurelle du système.

---

OUTPUT

Une convention de nommage canonique applicable
à tous les Core(s), LINK(s), Module(s), Core Light(s)
et références externes.