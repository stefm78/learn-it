# Feuille de route conceptuelle – Learn-it (v0.1)

Ce document décrit ce qu’il reste à faire sur le plan conceptuel pour le projet Learn-it, ainsi que la manière de reprendre le travail dans une nouvelle conversation sans dépendre de l’historique du chat.

## 1. Point de départ

Les éléments déjà formalisés et versionnés dans le dépôt sont :

- `docs/constitution_v0.md` :
  - 9 principes fondamentaux du jeu d’apprentissage.
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
   - Cadres pour adaptive learning, IA éducative, risques de biais.

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

## 5. Ordre de traitement proposé

Pour garder une progression logique :

1. **Cognition et charge mentale (CLT, Desirable Difficulties, multimédia)**  
   → Valider que les mécaniques de difficulté progressive, de puzzles et d’UI ne surchargent pas la mémoire de travail.

2. **Motivation et engagement (SDT, ARCS)**  
   → S’assurer que la gamification reste alignée avec l’autonomie, la compétence perçue et le sens.

3. **Métacognition et auto‑régulation (SRL)**  
   → Consolider le principe 9 et les mécanismes de réflexion sur l’apprentissage.

4. **Stratégies d’apprentissage fondées sur la preuve**  
   → Vérifier que les mécaniques centrales (temps, rappels, types de tâches) exploitent bien les stratégies les plus robustes.

5. **Personnalisation et systèmes adaptatifs**  
   → Encadrer l’hyper‑personnalisation (équité, transparence, pas de plafonds implicites).

6. **Modèles d’ingénierie pédagogique**  
   → Relier la constitution à un processus de design réutilisable (comment un cours devient un univers jouable).

Cet ordre peut être ajusté, mais il fournit un cadre clair pour avancer par "chapitres".

## 6. Comment reprendre le travail dans une nouvelle conversation

Dans une nouvelle session sans contexte, pour continuer ce travail conceptuel :

1. **Rappeler le projet et les fichiers clés**  
   - Indiquer que le projet s’appelle *Learn-it*.  
   - Pointer vers le fichier `docs/constitution_v0.md` comme base.  
   - Pointer vers ce document `docs/roadmap_conceptuelle.md` comme guide d’avancement.

2. **Spécifier l’étape en cours**  
   Par exemple :
   - « Nous en sommes à confronter les principes à la Cognitive Load Theory. »  
   - ou « Nous passons au bloc Motivation / Self‑Determination Theory. »

3. **Demander un travail ciblé**  
   Exemple de prompt :
   - « Lis `docs/constitution_v0.md` et `docs/roadmap_conceptuelle.md` dans mon repo `stefm78/learn-it`. Nous en sommes à l’étape 1 (Cognitive Load Theory). Analyse les 9 principes à la lumière de la CLT et propose les ajustements nécessaires. »

4. **Mettre à jour les fichiers**  
   - Intégrer les résultats dans `constitution_v0.md` ou dans un nouveau fichier de notes.  
   - Incrémenter éventuellement la version (par ex. `constitution_v0.2.md`, puis `v1.0` quand le tour des cadres est terminé).

## 7. Prochaines actions concrètes

À court terme :

1. Relire et, si besoin, ajuster `docs/constitution_v0.md` à la main.  
2. Démarrer l’analyse du **bloc 1 – Cognition et charge mentale**, en créant :
   - soit une sous‑section dans `constitution_v0.md`,  
   - soit un fichier `docs/constitution_notes_cognition.md`.

Ce document pourra évoluer (v0.2, v1.0, etc.) au fur et à mesure que la démarche se précise.