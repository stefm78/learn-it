# Feuille de route conceptuelle – Learn-it (v0.6)

Ce document décrit ce qu’il reste à faire sur le plan conceptuel pour le projet Learn-it, ainsi que la manière de reprendre le travail dans une nouvelle conversation sans dépendre de l’historique du chat.

## 1. Point de départ

Les éléments déjà formalisés et versionnés dans le dépôt sont :

- `docs/constitution_v0.md` (v0.6) :
  - 9 principes fondamentaux du jeu d’apprentissage, déjà ajustés pour intégrer explicitement :
    - des contraintes de **charge cognitive** (Cognitive Load Theory, difficultés désirables, multimédia sobre),
    - des contraintes de **motivation de qualité** (Self‑Determination Theory, modèle ARCS : autonomie, compétence, lien, Attention/Relevance/Confidence/Satisfaction),
    - des exigences de **métacognition et d’auto‑régulation** (structure avant/pendant/après, décisions actives de l’étudiant, prompts de planification, monitoring et réflexion),
    - l’intégration explicite des **stratégies d’apprentissage fondées sur la preuve** (rappel actif, espacement, interleaving, élaboration, double codage, exemples concrets) dans les principes 1, 3, 4, 5 et 9,
    - des garde‑fous pour la **personnalisation et les systèmes adaptatifs** (adaptation ouverte, pas de plafonds de difficulté durs, décisions explicables, possibilité d’override humain).
  - Liste des grands cadres théoriques à confronter (cognition/charge, motivation, métacognition/SRL, stratégies fondées sur la preuve, adaptatif/IA, ingénierie pédagogique).

Ce fichier constitue la "constitution conceptuelle" de base sur laquelle s’appuie toute la suite.

## 2. Objectif de la phase actuelle

Construire une **constitution conceptuelle robuste au regard de la recherche académique**, en confrontant systématiquement les 9 principes aux principaux cadres théoriques pertinents, puis en ajustant si nécessaire.

À la fin de cette phase, nous voulons :
- Une version `constitution_v1.x` où chaque principe :
  - est clairement formulé,
  - est mis en relation explicite avec les cadres théoriques,
  - inclut, si besoin, des garde‑fous ou limites d’application.

## 3. Cadres théoriques à passer en revue

Nous avons identifié au moins six blocs à traiter :

1. **Cognition et charge mentale**  
   - Cognitive Load Theory (CLT).  
   - Desirable Difficulties.  
   - Théorie de l’apprentissage multimédia (Mayer).

2. **Motivation et engagement**  
   - Self‑Determination Theory (SDT).  
   - Modèle ARCS.  
   - Autres théories de la motivation de la réussite / valeur‑attente.

3. **Métacognition et auto‑régulation**  
   - Modèles de Self‑Regulated Learning (SRL).  
   - Recommandations EEF sur la métacognition.

4. **Stratégies d’apprentissage fondées sur la preuve**  
   - Rappel actif, espacement, interleaving, élaboration, double codage, exemples concrets.

5. **Personnalisation et systèmes adaptatifs**  
   - Cadres pour adaptive learning, IA éducative, risques de biais, d’iniquité et d’opacité.

6. **Modèles d’ingénierie pédagogique**  
   - ADDIE, Merrill’s First Principles, taxonomie de Bloom révisée, autres modèles de design.

## 4. Méthode de travail pour chaque cadre

Pour chaque bloc théorique (1 à 6) :

1. **Rappel synthétique** du cadre en quelques lignes (sans entrer dans le détail encyclopédique).
2. **Analyse de compatibilité** avec les 9 principes :
   - Principe(s) clairement alignés avec ce cadre.
   - Points de tension ou risques potentiels.
3. **Ajustements proposés** :
   - Reformulation éventuelle d’un principe.
   - Ajout de garde‑fous (par exemple : limiter la difficulté dans certains cas, encadrer l’usage de récompenses, etc.).
4. **Trace écrite** :
   - Ajouter une sous‑section dans `constitution_v0.md` ou un nouveau fichier `constitution_notes_<cadre>.md` récapitulant cette confrontation.

## 5. État d’avancement par cadre

- **Bloc 1 – Cognition et charge mentale** :
  - Statut : INTÉGRÉ DANS LA CONSTITUTION (v0.2+).  
  - Travail réalisé : contraintes liées à la charge intrinsèque/extrinsèque, scaffolding des tâches complexes, sobriété graphique, contrôle de la complexité par session.

- **Bloc 2 – Motivation et engagement** :
  - Statut : INTÉGRÉ DANS LA CONSTITUTION (v0.3+).  
  - Travail réalisé : prise en compte explicite des besoins d’autonomie, de compétence et de lien (SDT), et des composantes Attention/Relevance/Confidence/Satisfaction (ARCS) dans les principes (chemin recommandé mais non rigide, succès significatifs réguliers, explication de la pertinence des missions, récompenses complémentaires à la motivation intrinsèque, dimension sociale prudente).

- **Bloc 3 – Métacognition et auto‑régulation** :  
  - Statut : INTÉGRÉ DANS LA CONSTITUTION (v0.4+).  
  - Travail réalisé : principe 9 enrichi pour inclure une structuration explicite des activités en trois phases (avant/pendant/après), avec des prompts de planification, de monitoring et de réflexion, et un rôle actif laissé à l’étudiant dans les décisions de parcours.

- **Bloc 4 – Stratégies d’apprentissage fondées sur la preuve** :  
  - Statut : INTÉGRÉ DANS LA CONSTITUTION (v0.5+).  
  - Travail réalisé : intégration explicite des stratégies de rappel actif, espacement, interleaving, élaboration, double codage et exemples concrets dans plusieurs principes (1, 3, 4, 5, 9), de façon à ce qu’elles soient au cœur du gameplay et de la planification.

- **Bloc 5 – Personnalisation et systèmes adaptatifs** :  
  - Statut : INTÉGRÉ DANS LA CONSTITUTION (v0.6).  
  - Travail réalisé : garde‑fous sur la personnalisation (adaptation ouverte, absence de plafonds de difficulté imposés, décisions explicables, possibilité de dépassement par l’étudiant, override possible par l’enseignant/tuteur).

- **Bloc 6 – Modèles d’ingénierie pédagogique** :  
  - Statut : EN ATTENTE.

## 6. Ordre de traitement proposé (mis à jour)

1. **Cognition et charge mentale (CLT, Desirable Difficulties, multimédia)**  
   → Intégré dans v0.2, pourra être raffiné au besoin.

2. **Motivation et engagement (SDT, ARCS)**  
   → Intégré dans v0.3, pourra être raffiné au besoin.

3. **Métacognition et auto‑régulation (SRL)**  
   → Intégré dans v0.4, pourra être raffiné au besoin.

4. **Stratégies d’apprentissage fondées sur la preuve**  
   → Intégré dans v0.5, pourra être raffiné au besoin.

5. **Personnalisation et systèmes adaptatifs**  
   → Intégré dans v0.6, pourra être raffiné au besoin.

6. **Modèles d’ingénierie pédagogique**  
   → Prochaine analyse à mener, pour relier la constitution à un processus de design réutilisable (comment un cours devient un univers jouable).

## 7. Comment reprendre le travail dans une nouvelle conversation

Dans une nouvelle session sans contexte, pour continuer ce travail conceptuel :

1. **Rappeler le projet et les fichiers clés**  
   - Indiquer que le projet s’appelle *Learn-it*.  
   - Pointer vers `docs/constitution_v0.md` comme base (actuellement v0.6).  
   - Pointer vers ce document `docs/roadmap_conceptuelle.md` comme guide d’avancement.

2. **Spécifier l’étape en cours**  
   Par exemple :
   - « Nous en sommes à confronter les principes au bloc 6 – Modèles d’ingénierie pédagogique (ADDIE, Merrill, Bloom révisé, etc.). »

3. **Demander un travail ciblé**  
   Exemple de prompt :
   - « Lis `docs/constitution_v0.md` et `docs/roadmap_conceptuelle.md` dans mon repo `stefm78/learn-it`. Nous en sommes au bloc 6 (Modèles d’ingénierie pédagogique). Analyse les 9 principes à la lumière de ces modèles et propose les ajustements nécessaires pour qu’ils soient opérationnalisables dans un processus de design de cours. »

4. **Mettre à jour les fichiers**  
   - Intégrer les résultats dans `constitution_v0.md` (v0.7, v0.8, etc.) ou dans un nouveau fichier de notes.  
   - Mettre à jour cette roadmap (statut des blocs, prochaine étape).  
   - Incrémenter la version (par ex. `constitution_v1.0` quand le tour des cadres est terminé).

## 8. Prochaines actions concrètes

À court terme :

1. Poursuivre l’analyse du **bloc 6 – Modèles d’ingénierie pédagogique**.
2. Proposer des ajustements aux principes et, si besoin, ajouter une section spécifique pour :
   - décrire comment un cours ou un chapitres est transformé en univers jouable (analyse, design, développement, implémentation, évaluation),
   - articuler les principes avec un cycle de type ADDIE et les First Principles de Merrill (problèmes authentiques, activation, démonstration, application, intégration),
   - préciser à quel moment de ce cycle interviennent les décisions adaptatives et les stratégies fondées sur la preuve.
3. Mettre à jour `docs/constitution_v0.md` en conséquence (version v0.7).
