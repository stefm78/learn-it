# Constitution conceptuelle – Learn-it (v0.2)

## Principes fondamentaux

1. **Primat de la maîtrise des compétences d’examen**  
   Le jeu est conçu d’abord pour garantir la maîtrise des compétences réellement évaluées (telles qu’elles apparaissent dans les objectifs du cours et les annales), puis pour être engageant. Les activités de jeu doivent pouvoir se mapper à des tâches d’examen (résolution de problèmes, modélisation, explication, interprétation de données). L’introduction des tâches complexes de type annale se fait de manière progressive (scaffolding), en contrôlant la charge cognitive : on commence par des versions simplifiées avant de monter vers des sujets multi‑étapes.

2. **Moteur générique basé sur un graphe de connaissances**  
   Le cœur du système est un moteur générique, indépendant du domaine, qui manipule des concepts, des relations de prérequis et des types de tâches. Chaque cours ou document est représenté comme un graphe orienté de connaissances, sur lequel le jeu instancie des cartes, puzzles, missions et “boss”. Le graphe sert explicitement à gérer la charge intrinsèque : tant que certains prérequis ne sont pas maîtrisés, le système évite de proposer des puzzles qui combinent trop de concepts simultanément.

3. **Temporalité et mémoire comme mécanismes centraux**  
   La dynamique du jeu intègre explicitement la courbe de l’oubli : chaque concept possède un niveau de stabilité mémorielle qui évolue dans le temps. La répétition espacée et le rappel actif sont intégrés au cœur du gameplay (retours planifiés, anomalies, quêtes de réactivation), et non ajoutés comme un module annexe. L’usage des difficultés dites “désirables” est calibré : pour un contenu nouveau ou très complexe, le système commence par des explications guidées et des exemples travaillés avant de demander un rappel autonome intensif.

4. **Planification vers une date cible**  
   L’étudiant indique une date d’examen (et éventuellement un niveau visé). Le système planifie et réajuste un chemin d’apprentissage pour maximiser la probabilité d’atteindre un niveau de maîtrise suffisant à cette échéance, en tenant compte du temps disponible et de la difficulté des contenus. La planification intègre des contraintes de charge : chaque session limite le nombre d’éléments nouveaux en interaction et découpe les thèmes intrinsèquement complexes en sous‑blocs digestes.

5. **Hyper‑personnalisation du parcours**  
   Le parcours n’est pas uniforme. La difficulté, le rythme d’introduction de nouveaux concepts, le choix des missions et la répartition entre découverte, rappel et entraînement “type annale” sont adaptés en continu aux performances, au profil et aux objectifs de l’étudiant. Cette personnalisation vise explicitement à maintenir la charge cognitive dans une zone gérable (ni sous‑stimulation, ni surcharge) et à réduire la charge extrinsèque inutile.

6. **Transition progressive vers la “feuille blanche”**  
   Le jeu propose plusieurs modes qui rapprochent progressivement l’expérience ludique du format réel de l’examen (problèmes longs, réponses libres, usage de papier/whiteboard). L’objectif est que les compétences développées dans le jeu se transfèrent sans rupture au contexte d’évaluation (annales, copie papier, épreuve en conditions réelles), en augmentant progressivement la complexité et en réduisant les aides pour ne pas provoquer de surcharge brutale.

7. **Adaptation à l’environnement d’usage**  
   Le système s’adapte aux contraintes contextuelles de l’étudiant (transport, bureau, bibliothèque, temps court/long). Différents modes (micro‑sessions de rappel, entraînements longs, simulations d’examen) sont proposés, tout en restant alignés sur la même trajectoire globale d’apprentissage. Les modes courts privilégient des tâches à faible charge (peu d’éléments en interaction), tandis que les modes longs peuvent accueillir des problèmes plus complexes avec un guidage adéquat.

8. **Gamification éthique centrée sur l’effort cognitif**  
   Les mécaniques d’engagement (récompenses, progression, défis) servent en priorité l’effort intellectuel et la maîtrise des compétences, et non la simple rétention d’attention. Les récompenses sont reliées de façon significative au contenu appris, et les systèmes de points/bonus évitent de nuire à la motivation intrinsèque. Les éléments visuels et interactifs liés à la gamification sont conçus pour minimiser la charge extrinsèque : sobriété graphique, absence d’animations inutiles, signalisation claire de l’information pertinente.

9. **Développement de la métacognition et de l’auto‑régulation**  
   Le jeu aide l’étudiant à apprendre à apprendre : calibrer sa confiance, planifier, monitorer et évaluer son propre apprentissage. Il met en regard perception de maîtrise et données réelles, explicite les raisons pédagogiques des mécaniques (rappel, espacement, interleaving) et propose des moments de réflexion sur les stratégies utilisées.

## Cadres théoriques à confronter (liste de travail)

Les principes ci‑dessus devront être confrontés, critiqués et ajustés à la lumière de plusieurs cadres théoriques majeurs, notamment :

- Cognition et charge mentale : Cognitive Load Theory, Desirable Difficulties, théorie de l’apprentissage multimédia.
- Motivation et engagement : Self‑Determination Theory, ARCS, théories de la motivation de la réussite et de la valeur-attente.
- Métacognition et auto‑régulation : modèles de Self‑Regulated Learning (Pintrich, Winne & Hadwin, modèles modernes de SRL), recommandations EEF sur la métacognition.
- Stratégies d’apprentissage fondées sur la preuve : rappel actif, répétition espacée, interleaving, élaboration, double codage, exemples concrets.
- Personnalisation et systèmes adaptatifs : cadres pour adaptive learning et systèmes d’apprentissage pilotés par l’IA.
- Modèles d’ingénierie pédagogique : ADDIE, Merrill’s First Principles, taxonomie de Bloom révisée, autres modèles d’instruction.
