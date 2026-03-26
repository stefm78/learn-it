# Feuille de route conceptuelle – Learn-it (v0.7)

Ce document décrit ce qu'il reste à faire sur le plan conceptuel pour le projet Learn-it, ainsi que la manière de reprendre le travail dans une nouvelle conversation sans dépendre de l'historique du chat.

## 1. Point de départ

Les éléments déjà formalisés et versionnés dans le dépôt sont :

- `docs/constitution_v0.md` (v0.8) :
  - 10 principes fondamentaux du jeu d'apprentissage, intégrant :
    - des contraintes de **charge cognitive** (Cognitive Load Theory, difficultés désirables calibrées, multimédia sobre, principe de cohérence Mayer, redondance évitée),
    - des contraintes de **motivation de qualité** (Self‑Determination Theory, modèle ARCS, self-efficacy Bandura unifié avec Confidence ARCS, transition motivation extrinsèque → intrinsèque),
    - des exigences de **métacognition et d'auto‑régulation** (structure avant/pendant/après, dosage métacognitif scaffoldé, modélisation explicite des stratégies, dimension affective légère),
    - l'intégration explicite des **stratégies d'apprentissage fondées sur la preuve** (rappel actif, espacement, interleaving différencié catégories/contenus, élaboration, double codage non redondant, exemples concrets, fading des aides),
    - des garde‑fous pour la **personnalisation et les systèmes adaptatifs** (adaptation ouverte, fading planifié, décisions explicables et proactives, surveillance des écarts entre profils, validité des inférences confrontée à des mesures externes),
    - un **cycle de design pédagogique** complet (ADDIE enrichi des First Principles de Merrill, ancrage Bloom révisé dès la phase Analyse, Merrill comme contrainte systématique),
    - un **Principe 10** dédié à la qualité du feedback et au modèle implicite de la compétence.
  - Cadres théoriques de référence listés en fin de document (incluant Pekrun, Bandura, alignement constructif Biggs).

Ce fichier constitue la "constitution conceptuelle" de base sur laquelle s'appuie toute la suite.

## 2. Objectif de la phase actuelle

Consolider la constitution v0.8 en une **version v1.0 stable**, apte à servir de référence durable pour le design des univers d'apprentissage.

À la fin de cette phase, nous voulons :

- Une version `constitution_v1.0` où chaque principe :
  - est clairement formulé,
  - est mis en relation explicite avec les cadres théoriques,
  - inclut les garde‑fous nécessaires,
  - a été validé par au moins une lecture critique externe.

## 3. État d'avancement par cadre théorique

- **Bloc 1 – Cognition et charge mentale** :
  - Statut : INTÉGRÉ (v0.2+, raffiné en v0.8 — cohérence Mayer, fading, difficultés désirables calibrées).
- **Bloc 2 – Motivation et engagement** :
  - Statut : INTÉGRÉ (v0.3+, raffiné en v0.8 — transition extrinsèque/intrinsèque, self-efficacy/ARCS Confidence unifiés).
- **Bloc 3 – Métacognition et auto‑régulation** :
  - Statut : INTÉGRÉ (v0.4+, raffiné en v0.8 — dosage métacognitif scaffoldé, modélisation explicite, dimension affective).
- **Bloc 4 – Stratégies d'apprentissage fondées sur la preuve** :
  - Statut : INTÉGRÉ (v0.5+, raffiné en v0.8 — distinction interleaving catégories/contenus, fading, double codage non redondant).
- **Bloc 5 – Personnalisation et systèmes adaptatifs** :
  - Statut : INTÉGRÉ (v0.6+, raffiné en v0.8 — validité des inférences, surveillance des écarts profils, explicabilité proactive).
- **Bloc 6 – Modèles d'ingénierie pédagogique** :
  - Statut : INTÉGRÉ (v0.7+, raffiné en v0.8 — ancrage Bloom révisé dans P1 et phase Analyse, Merrill comme contrainte systématique, alignement constructif Biggs, P10 feedback).
- **Bloc 7 – Émotions et apprentissage** :
  - Statut : INTÉGRÉ (v0.8 — dimension affective légère dans P9, représentation non anxiogène de l'échéance dans P4, Pekrun référencé).

## 4. Prochaines actions pour atteindre v1.0

1. **Relecture de cohérence globale** — Vérifier qu'aucun principe ne contredit un autre et que les 10 principes forment un ensemble cohérent et sans redondance.
2. **Opérationnalisation** — Pour chaque principe, identifier 1 à 3 indicateurs concrets permettant de vérifier qu'il est respecté dans un univers de jeu produit.
3. **Test sur un premier univers pilote** — Appliquer le cycle de design pédagogique à un cours pilote et confronter la constitution à la réalité de production.
4. **Incrémenter vers v1.0** — Intégrer les ajustements issus du test pilote et stabiliser la version.

## 5. Comment reprendre le travail dans une nouvelle conversation

Dans une nouvelle session sans contexte, pour continuer ce travail conceptuel :

1. **Rappeler le projet et les fichiers clés**
  - Indiquer que le projet s'appelle *Learn-it*.
  - Pointer vers `docs/constitution_v0.md` comme base (actuellement v0.8).
  - Pointer vers ce document `docs/roadmap_conceptuelle.md` comme guide d'avancement.
2. **Spécifier l'étape en cours**
Par exemple :
  - « Nous travaillons à la consolidation vers v1.0 : relecture de cohérence, opérationnalisation des principes, test pilote. »
3. **Demander un travail ciblé**
Exemple de prompt :
  - « Lis `docs/constitution_v0.md` et `docs/roadmap_conceptuelle.md` dans mon repo `stefm78/learn-it`. Nous visons la v1.0. Fais une relecture de cohérence des 10 principes et propose les ajustements nécessaires. »
4. **Mettre à jour les fichiers**
  - Intégrer les résultats dans `constitution_v0.md` (v0.9, v1.0, etc.).
  - Mettre à jour cette roadmap (statut des blocs, prochaine étape).
  - Incrémenter la version au passage en v1.0 quand la stabilisation est atteinte.