# Learn-it 🎓

> Moteur d'apprentissage adaptatif basé sur une architecture constitutionnelle formelle.

---

## Vue d'ensemble

**Learn-it** est un système d'apprentissage adaptatif gouverné par une **Constitution** et un **Référentiel** séparés. La Constitution définit *le quoi et le pourquoi* (types, invariants, règles, contraintes), tandis que le Référentiel borne *le combien et le comment* (seuils, paramètres, valeurs par défaut).

Le moteur fonctionne **100 % en local** pendant l'usage apprenant : aucun appel réseau en temps réel, aucune génération de contenu à la volée.

---

## Architecture

```
learn-it/
├── docs/
│   └── Current_Constitution/
│       ├── Learn-it_Constitution_v1_7.yaml        # Constitution canonique (TYPES, INVARIANTS, RULES…)
│       ├── Learn-it_referentiel_defaults_v0_6.yaml # Référentiel des seuils et paramètres
│       └── Learnit__link_core.yaml                # Liens inter-Core
└── prompts/                                       # Prompts opérationnels
```

---

## Concepts clés

### Knowledge Unit (KU)
Unité atomique du graphe de connaissances. **Toute KU doit être typée** (déclarative, procédurale, perceptuelle, créative…). Un type absent déclenche un mode de sécurité et interdit l'adaptation fine.

### Knowledge Graph
Graphe orienté **acyclique** de KU reliées par des arêtes de dépendance explicites. La propagation d'incertitude est limitée à **un saut** : toute rétrogradation secondaire constitue un nouvel événement indépendant.

### Modèle de Maîtrise (MSC)
Agrégation **AND stricte** sur trois composantes :
| Composante | Signification |
|------------|---------------|
| **P** | Précision |
| **R** | Robustesse temporelle |
| **A** | Autonomie |

La composante **T** (transférabilité) est séparée de la maîtrise de base et ne peut jamais en être un prérequis.

### Modèle d'état apprenant
Trois axes observés en continu :
- **Calibration** — décalage auto-rapport / performance
- **Activation** — régime productif, détresse ou sous-défi (gouverné par AR-N1)
- **Valeur-Coût (VC)** — perçue en fin de session via AR-N2 (optionnel)

### Auto-rapports (AR)
| Niveau | Moment | Rôle |
|--------|--------|------|
| AR-N1 | Événementiel runtime | Distinction confusion / frustration / anxiété |
| AR-N2 | Fin de session | VC, difficulté perçue, intention de retour |
| AR-N3 | Périodique | Bilan calibration dérivé AEQ |

En absence d'AR-N1, le système adopte une **réponse conservatrice** (scaffolding léger réversible, sans pénalisation).

---

## Invariants fondamentaux

- 🔒 **Séparation Constitution / Référentiel** inviolable
- 🔒 **Moteur 100 % local** en usage apprenant
- 🔒 **Aucune génération de contenu** à la volée
- 🔒 **Graphe acyclique** obligatoire
- 🔒 **Propagation graphe limitée à 1 saut**
- 🔒 **Logique AND du MSC** non patchable
- 🔒 **Bloom ≥ 4 interdit** sans contexte authentique déclaré
- 🔒 **Pas de biométrie** ni de surveillance hors session
- 🔒 **Pas de déploiement Assisté** sans infrastructure tutorale

---

## Système de Patch

Les patches sont **occasionnels, bornés et atomiques**. Ils doivent être :
1. **Générés et validés hors session** (QA pédagogique préalable)
2. **Déterministes** dans leur validation locale (aucun critère sémantique ou interprétatif en local)
3. **Rollbackés intégralement** en cas d'échec partiel

Une dérive persistante non corrigeable par patch doit être **escaladée** vers la chaîne d'analyse hors session.

> ⚠️ La philosophie adaptative, la logique AND du MSC et la règle de propagation graphe sont **non patchables**.

---

## Niveaux d'autonomie moteur

| Mode | Description |
|------|-------------|
| **Autonome** | Moteur décide seul |
| **Hybride recommandé** | Suggestions humaines non bloquantes |
| **Hybride bloquant** | Validation humaine requise |
| **Assisté** | Infrastructure tutorale obligatoire |

---

## Versions

| Artefact | Version actuelle |
|----------|------------------|
| Constitution | v1.7 |
| Référentiel | v0.6 |

---

## Licence

*À définir.*
