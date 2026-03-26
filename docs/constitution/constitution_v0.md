# Constitution conceptuelle – Learn-it (v0.9)

> **Note de version** : La v0.9 intègre 12 arbitrages validés issus de l'analyse critique approfondie de la v0.8. Les modifications sont signalées par `[v0.9]` dans le texte.

---

## Principes fondamentaux

1. **Primat de la maîtrise des compétences d'examen**

Le jeu est conçu d'abord pour garantir la maîtrise des compétences réellement évaluées (telles qu'elles apparaissent dans les objectifs du cours et les annales), puis pour être engageant. Les activités de jeu doivent pouvoir se mapper à des tâches d'examen (résolution de problèmes, modélisation, explication, interprétation de données). L'introduction des tâches complexes de type annale se fait de manière progressive (scaffolding), en contrôlant la charge cognitive : on commence par des versions simplifiées avant de monter vers des sujets multi‑étapes. Chaque mission importante précise explicitement sa pertinence par rapport à l'examen (composante Relevance du modèle ARCS) et s'appuie, autant que possible, sur des **exemples concrets** avant de généraliser vers des formes plus abstraites.

Les objectifs d'apprentissage associés à chaque mission sont caractérisés par leur **niveau cognitif cible** selon la taxonomie révisée de Bloom (mémoriser, comprendre, appliquer, analyser, évaluer, créer). La progression de l'étudiant vise une montée en niveaux cognitifs, et non la seule consolidation des niveaux bas.

Le graphe de connaissances est construit à partir des supports de cours et des annales, mais aussi confronté à la structure disciplinaire du domaine, afin d'éviter un rétrécissement du curriculum aux seuls formats d'évaluation. **[v0.9]** La qualité du corpus source est évaluée via un **Indice de Confiance du Corpus (ICC)**, calculé à partir du nombre d'annales disponibles, de leur ancienneté et de leur diversité de formats. La phase Analyse du cycle ADDIE exige de déclarer explicitement l'ICC avant de finaliser le graphe :

- **ICC fort** (annales complètes) : graphe calibré normalement sur la fréquence des concepts en annales.

- **ICC partiel** (annales incomplètes) : les fréquences sont pondérées et complétées par la structure disciplinaire de référence.

- **ICC absent** (aucune annale fournie) : fallback sur taxonomie Bloom et corpus disciplinaire de référence (référentiel officiel, syllabus, manuels du domaine).

Dans tous les cas, tout concept présent dans le corpus disciplinaire de référence mais absent ou rare dans les annales est maintenu dans le graphe avec un niveau cognitif Bloom minimum *comprendre* et un coefficient de pondération réduit — il n'est jamais supprimé. Une distinction explicite est maintenue entre *concepts fréquents en annales* et *concepts fondamentaux du domaine*, les deux étant nécessaires mais avec des pondérations différentes.

**[v0.9]** Chaque univers vérifie l'**alignement constructif** (Biggs) dès la phase Analyse : cohérence entre objectifs Bloom, activités de jeu et formes d'évaluation. Tout désalignement détecté entre ces trois dimensions est signalé comme un défaut de design à corriger avant la phase Développement.

1. **Moteur générique basé sur un graphe de connaissances**

Le cœur du système est un moteur générique, indépendant du domaine, qui manipule des concepts, des relations de prérequis et des types de tâches. Chaque cours ou document est représenté comme un graphe orienté de connaissances, sur lequel le jeu instancie des cartes, puzzles, missions et "boss". Le graphe sert explicitement à gérer la charge intrinsèque : tant que certains prérequis ne sont pas maîtrisés, le système évite de proposer des puzzles qui combinent trop de concepts simultanément.

Les décisions adaptatives (quels contenus, dans quel ordre) doivent rester **explicables** : le système communique à l'étudiant, sur demande, les raisons principales de chaque recommandation de parcours, en distinguant les raisons liées aux prérequis manquants, aux lacunes observées, et aux contraintes temporelles. **[v0.9]** Cette explicabilité est fournie *sur demande explicite de l'étudiant* et, de manière non sollicitée, *uniquement aux moments de transition entre sessions* — jamais en milieu de tâche active, afin d'éviter d'augmenter la charge extrinsèque au moment où la capacité de traitement cognitif est engagée.

Le **fading** des aides est planifié dans le graphe : une fois un concept maîtrisé, le système programme des occurrences sans guidage, même hors contexte d'examen, afin de prévenir la dépendance à l'assistance. **[v0.9]** La maîtrise n'est considérée comme robuste que lorsqu'elle satisfait l'ensemble du Mastery Score Composite (MSC) défini en Glossaire ; en particulier, le fading des aides est déclenché lorsque la composante **A** (Autonomie) du MSC progresse — et non lorsque la précision seule est élevée.

1. **Temporalité et mémoire comme mécanismes centraux**

La dynamique du jeu intègre explicitement la courbe de l'oubli : chaque concept possède un niveau de stabilité mémorielle qui évolue dans le temps. La répétition espacée et le rappel actif sont intégrés au cœur du gameplay (retours planifiés, anomalies, quêtes de réactivation), et non ajoutés comme un module annexe. L'usage des difficultés dites "désirables" est calibré : une difficulté n'est légitime que si elle augmente la consolidation ou le transfert sans dépasser durablement les capacités de traitement et d'autorégulation de l'étudiant. Lorsqu'une difficulté cesse d'être productive, le système revient provisoirement à la démonstration, au guidage et aux exemples travaillés avant de réaugmenter l'exigence.

La planification temporelle vise explicitement à combiner **espacement** et **rappel actif**, plutôt qu'à s'appuyer sur de simples relectures passives. L'**interleaving** est appliqué en priorité sous sa forme de **variation de types de problèmes** (interleaving de catégories), dont l'effet sur la discrimination et le transfert est le plus robuste empiriquement. L'interleaving de contenus distincts est introduit plus progressivement, après une première phase de bloc homogène sur chaque contenu nouveau. **[v0.9]** La bascule vers l'interleaving de contenus est conditionnée à l'atteinte simultanée des composantes **P** (Précision) et **A** (Autonomie) du MSC sur chaque contenu concerné. Valeur de référence par défaut : ≥ 2 réussites consécutives sans aide sur ≥ 3 tâches distinctes du niveau Bloom cible — ce seuil est configurable par univers.

**[v0.9]** Après une interruption d'activité supérieure au seuil de robustesse temporelle (seuil_R, configurable par univers), le système déclenche une **session de reprise** avant de reprendre le parcours planifié : diagnostic léger (3 à 5 tâches de rappel sur les concepts récemment maîtrisés), bilan de l'état du graphe et recalcul du chemin vers l'échéance. Les concepts dont la composante R du MSC est dégradée repassent en état *en consolidation* avec un parcours de réactivation court — et non en état *nouveau*.

1. **Planification vers une date cible**

L'étudiant indique une date d'examen (et éventuellement un niveau visé). Le système planifie et réajuste un chemin d'apprentissage pour maximiser la probabilité d'atteindre un niveau de maîtrise suffisant à cette échéance, en tenant compte du temps disponible et de la difficulté des contenus. La planification intègre des contraintes de charge : chaque session limite le nombre d'éléments nouveaux en interaction et découpe les thèmes intrinsèquement complexes en sous‑blocs digestes.

La représentation de l'échéance est conçue pour être **mobilisatrice et non anxiogène** : le système présente la progression accomplie et le chemin restant de manière équilibrée, sans surexposer la distance à l'objectif. La planification n'est pas imposée de manière rigide : le système propose un chemin recommandé mais laisse des marges de choix (ordre de certains modules, types de missions) afin de soutenir le besoin d'autonomie et d'entraîner la capacité de planification de l'étudiant. Ce chemin combine de manière explicite des phases de **découverte**, des blocs de **rappel actif espacés**, et des sessions **interleavées** où anciens et nouveaux contenus sont travaillés conjointement.

1. **Hyper‑personnalisation du parcours**

Le parcours n'est pas uniforme. La difficulté, le rythme d'introduction de nouveaux concepts, le choix des missions et la répartition entre découverte, rappel et entraînement "type annale" sont adaptés en continu aux performances, au profil et aux objectifs de l'étudiant. Cette personnalisation vise explicitement à maintenir la charge cognitive dans une zone gérable (ni sous‑stimulation, ni surcharge) et à réduire la charge extrinsèque inutile.

**[v0.9]** La personnalisation est pilotée par un **modèle d'état apprenant composite**, défini par deux axes orthogonaux :

- **Axe 1 — Calibration** (compétence perçue vs réelle) : *bien calibré* (auto-efficacité ≈ performance), *surestimateur* (auto-efficacité > performance), *sous-estimateur* (auto-efficacité < performance).

- **Axe 2 — Activation émotionnelle** (Pekrun, Control-Value Theory) : *zone productive* (enthousiasme, engagement modéré), *zone anxiogène* (anxiété élevée, signaux d'abandon), *zone ennui/désinvestissement* (sous-stimulation).

Ces deux axes génèrent une matrice 3×3 de 9 états, chacun associé à une politique adaptative distincte (difficulté, type de tâche, feedback, message). Pour le MVP, les 5 états prioritaires sont : bien calibré/productif, surestimateur/productif, sous-estimateur/productif, bien calibré/anxiogène, bien calibré/ennui. La matrice complète constitue la cible v2.0.

Ce modèle composite remplace une hiérarchie fixe de signaux : il n'impose pas de priorité absolue entre performance, auto-efficacité et signaux affectifs, mais définit le régime approprié selon l'état réel détecté. Un étudiant en état de *flow* (performance élevée, engagement maximal) n'est pas interrompu par des ajustements adaptatifs même si des signaux secondaires déclenchent des alertes.

La personnalisation surveille également les **écarts systématiques de recommandations entre profils d'apprenants** et signale toute disparité notable nécessitant une révision du modèle. L'adaptation reste **ouverte** : le système recommande un niveau de difficulté "sûr" mais permet à l'étudiant de choisir des défis plus ambitieux. Aucun plafond de difficulté n'est imposé de manière définitive : les protections passent par le scaffolding (indices, décomposition) et des messages d'avertissement, pas par le blocage de contenus.

1. **Transition progressive vers la "feuille blanche"**

Le jeu propose plusieurs modes qui rapprochent progressivement l'expérience ludique du format réel de l'examen (problèmes longs, réponses libres, usage de papier/whiteboard). L'objectif est que les compétences développées dans le jeu se transfèrent sans rupture au contexte d'évaluation (annales, copie papier, épreuve en conditions réelles), en augmentant progressivement la complexité et en réduisant les aides pour ne pas provoquer de surcharge brutale.

Le transfert visé est prioritairement un **transfert proche** vers les conditions d'évaluation réelles. Cependant, une partie des missions d'intégration propose des contextes applicatifs légèrement décalés du format d'examen, afin de tester la robustesse de la compréhension au-delà de la simple familiarité au format. Les modes "simulation d'examen" doivent être ressentis comme des défis atteignables, avec des critères de réussite clairs, pour renforcer le sentiment de compétence. La progression vers les modes sans aide correspond à la montée de la composante **A** (Autonomie) du MSC.

1. **Adaptation à l'environnement d'usage**

Le système s'adapte aux contraintes contextuelles de l'étudiant (transport, bureau, bibliothèque, temps court/long). Différents modes (micro‑sessions de rappel, entraînements longs, simulations d'examen) sont proposés, tout en restant alignés sur la même trajectoire globale d'apprentissage. Les modes courts privilégient des tâches à faible charge (peu d'éléments en interaction), tandis que les modes longs peuvent accueillir des problèmes plus complexes avec un guidage adéquat. Lorsque c'est pertinent, certains modes peuvent encourager l'usage de supports physiques (papier, whiteboard) pour préparer la transition vers la feuille blanche.

**[v0.9]** Le système intègre un modèle de **fatigue cognitive intra-session** : les missions impliquant une forte charge intrinsèque (boss, problèmes multi-étapes, tâches de niveau Bloom *analyser* ou supérieur) sont positionnées en début ou milieu de session. Au-delà d'un seuil de durée de travail actif (configurable, valeur de référence : 25 minutes), le système bascule automatiquement vers des formats à faible charge (rappel guidé, reconnaissance, révision d'exemples travaillés) plutôt que vers des tâches de production ou d'analyse. Ce seuil est signalé à l'étudiant de manière non anxiogène.

1. **Gamification éthique centrée sur l'effort cognitif**

Les mécaniques d'engagement (récompenses, progression, défis) servent en priorité l'effort intellectuel et la maîtrise des compétences, et non la simple rétention d'attention. Un mécanisme d'engagement qui améliore la persistance à court terme mais dégrade la qualité du traitement cognitif, l'autonomie perçue ou la compréhension à long terme doit être considéré comme contraire à la constitution. Les récompenses extrinsèques sont utilisées préférentiellement en phase d'amorçage et progressivement retirées au profit du sentiment de compétence et de progrès intrinsèque, afin de soutenir l'intériorisation de la motivation (SDT : régulation identifiée puis intégrée).

**[v0.9]** Les éléments visuels et interactifs sont soumis à deux régimes distincts selon leur nature :

- **(a) Éléments multimédia pédagogiques** (contenus, explications, feedbacks) : principe de cohérence de Mayer strict — seuls les éléments qui contribuent directement à la compréhension sont inclus, la redondance entre modalités est évitée, et la charge extrinsèque est minimisée.

- **(b) Éléments de gamification** (animations de récompense, badges, effets visuels) : test de non-nuisance — l'élément est acceptable s'il ne dégrade ni la motivation intrinsèque (SDT) ni l'effort cognitif productif. Le critère n'est pas la redondance Mayer (une animation de récompense est par nature redondante avec le contenu) mais l'absence d'effet négatif mesurable sur l'apprentissage ou l'autonomie.

Les récompenses sont reliées de façon significative au contenu appris, et les systèmes de points/bonus évitent de nuire à la motivation intrinsèque.

1. **Développement de la métacognition, de l'auto‑régulation et du lien social**

Le jeu aide l'étudiant à apprendre à apprendre : calibrer sa confiance, planifier, monitorer et évaluer son propre apprentissage. Il met en regard perception de maîtrise et données réelles, explicite les raisons pédagogiques des mécaniques (rappel, espacement, interleaving) et propose des moments de réflexion sur les stratégies utilisées. Concrètement, le jeu structure la plupart des activités en trois temps :

- **Avant la tâche** : clarification du but, éventuellement choix entre plusieurs priorités ou types de missions, et brève anticipation de la difficulté (forethought).

- **Pendant la tâche** : incitations ponctuelles à estimer sa confiance ou à vérifier sa compréhension (monitoring), sans interrompre excessivement le flux de jeu.

- **Après la tâche** : synthèse des erreurs, comparaison entre confiance déclarée et performance réelle, invitation à identifier ce qui a le mieux aidé ou ce qui sera changé la prochaine fois (self‑reflection). Certains prompts de réflexion encouragent explicitement l'**élaboration** (faire des liens avec d'autres notions, trouver des exemples) et l'usage de **double codage** (verbal + visuel) lorsque les deux représentations sont complémentaires et non redondantes.

**[v0.9]** Les invitations métacognitives avant/pendant/après **varient en format** (question ouverte, choix entre 2–3 options, prédiction chiffrée, complétion de phrase) et ne sont pas systématiques à chaque micro-tâche. La variabilité est planifiée pour maintenir un effet de surprise cognitif et prévenir la réponse automatique sans engagement réel. Les formats les plus guidés (choix fermés, exemples de réponse) sont réservés aux apprenants novices ou en forte charge cognitive.

L'**intensité des prompts métacognitifs est elle-même scaffoldée** : pour les apprenants novices ou en situation de forte charge cognitive, les invitations à la réflexion sont plus guidées et moins fréquentes, puis progressivement retirées à mesure que l'étudiant internalise ces routines. Les stratégies métacognitives (planification, monitoring, réflexion) font l'objet d'une **modélisation explicite** avant d'être demandées de manière autonome.

Le système intègre une **dimension affective** : il adapte son discours et sa difficulté en réponse aux signaux comportementaux d'anxiété ou de frustration détectés (abandon précoce, taux d'erreur inhabituel, refus de missions). **[v0.9]** L'ennui et la sous-stimulation sont traités comme des signaux d'alarme **symétriques** à l'anxiété (Pekrun, Control-Value Theory) : une sous-stimulation détectée — signaux comportementaux d'engagement minimal, performance anormalement haute sans effort apparent, accélération des réponses — déclenche une réponse adaptative équivalente à une surcharge : augmentation de la difficulté, changement de type de tâche ou introduction d'une nouvelle contrainte. Ni l'anxiété ni l'ennui ne sont nommés cliniquement dans les messages.

Dans la mesure du possible, le système intègre une dimension de lien (classement coopératif, défis partagés) afin de soutenir le besoin de *relatedness* sans générer de comparaison sociale malsaine. **[v0.9]** La dimension sociale est introduite via une **exposition progressive et réversible** : après un seuil d'usage établi (valeur de référence : 5 sessions complétées), le système propose activement une fonctionnalité sociale concrète et non intrusive, avec option de désactivation simple et permanente à tout moment. L'étudiant n'est pas obligé d'activer activement une option pour bénéficier d'un lien social adapté, mais peut s'en désengager sans friction.

1. **Qualité du feedback et modèle implicite de la compétence**

Le feedback généré par le système porte en priorité sur le **processus** (stratégies utilisées, erreurs procédurales, pistes de révision) et sur l'**autorégulation** (comment l'étudiant pourrait ajuster son approche), plutôt que sur la personne ou les aptitudes. Les messages de réussite soulignent l'effort, la stratégie et la progression, afin de renforcer une conception malléable de la compétence. Tout feedback évaluatif global ("tu maîtrises ce chapitre") est accompagné d'une indication de son niveau de fiabilité et des conditions dans lesquelles cette inférence a été établie.

---

## Cycle de design pédagogique

Le design des univers d'apprentissage dans Learn-it suit un cycle explicite, inspiré des modèles d'ingénierie pédagogique (notamment ADDIE) et des First Principles of Instruction de Merrill :

1. **Analyse**

Identifier les objectifs d'apprentissage et les compétences d'examen associées, extraire les concepts et relations clés à partir des supports (cours, exercices, annales) et construire le graphe de connaissances correspondant. Pour chaque objectif, les verbes d'action sont positionnés dans la **taxonomie de Bloom révisée** (mémoriser, comprendre, appliquer, analyser, évaluer, créer), afin de garantir que les missions de jeu couvrent les niveaux cognitifs visés par le cours et non seulement les niveaux les plus facilement gamifiables.

**[v0.9]** L'ICC (Indice de Confiance du Corpus) est déclaré explicitement à cette phase et conditionne la stratégie de construction du graphe (voir P1). L'alignement constructif (Biggs) est vérifié : cohérence entre objectifs, activités et formes d'évaluation.

Tout univers d'apprentissage doit expliciter les compétences visées, leur position dans une progression de complexité, les tâches authentiques de référence, les niveaux cognitifs sollicités, les formes de guidage prévues, les preuves attendues de maîtrise (référencées au MSC) et les conditions de révision après usage.

1. **Design**

Pour chaque objectif et partie du graphe, définir des problèmes authentiques et une trajectoire d'apprentissage de type activation → démonstration → application → intégration, en les traduisant en types de missions, puzzles, cartes et "boss" alignés avec les 10 principes. La trajectoire activation → démonstration → application → intégration constitue une **contrainte systématique de design**, et non une simple inspiration : chaque univers doit couvrir ces quatre phases pour chaque objectif cible.

1. **Développement**

Produire les contenus jouables (énoncés, interfaces, feedbacks, paramètres adaptatifs) en respectant les contraintes de charge cognitive, de motivation, de métacognition, de stratégies fondées sur la preuve et d'éthique de la personnalisation.

1. **Implémentation**

Déployer l'univers d'apprentissage auprès des étudiants, configurer les paramètres d'adaptation et les liens avec l'environnement réel (calendrier d'examen, modes d'usage).

1. **Évaluation et révision**

Recueillir des données sur la maîtrise réelle des objectifs (performances aux missions clés, simulations d'examen, résultats d'évaluation externe) et sur l'expérience des utilisateurs, puis ajuster le graphe, les missions et les paramètres adaptatifs.

**[v0.9]** Le déclencheur de révision du modèle d'inférence est défini en termes d'**écarts longitudinaux intra-individuels** :

- **Écart ponctuel** : maîtrise estimée par le système supérieure à la performance réelle lors d'une simulation d'examen → signalement immédiat et ajustement du modèle pour les concepts concernés.

- **Biais systématique** : sur ≥ 3 évaluations consécutives, le système surestime ou sous-estime de manière cohérente (écart médian > 20%) → révision du modèle d'inférence pour ce concept ou ce type de tâche.

- **Dérive hors-jeu** : performance en simulation stable mais résultats réels (examen intermédiaire, devoir rendu) systématiquement inférieurs → revoir le paramètre de transfert du graphe (la maîtrise en jeu ne se transfère pas suffisamment hors-jeu). Ce troisième cas porte spécifiquement sur la composante **T** (Transférabilité) du MSC.

Ce mécanisme est valide pour un usage individuel comme collectif. Pour un usage en cohorte, un écart > 15% sur ≥ 10 apprenants peut déclencher une révision du modèle commun. Ce cycle est itératif : les univers peuvent être révisés régulièrement pour rester cohérents avec la constitution et les retours du terrain.

---

## Cadres théoriques de référence

Les principes ci‑dessus ont été confrontés, critiqués et ajustés à la lumière des cadres théoriques suivants :

- **Cognition et charge mentale** : Cognitive Load Theory (Sweller, van Merriënboer), Desirable Difficulties (Bjork), théorie de l'apprentissage multimédia (Mayer — 12 principes dont cohérence, segmentation, redondance).

- **Motivation et engagement** : Self‑Determination Theory (Deci & Ryan), modèle ARCS (Keller), théories de la motivation de la réussite et de la valeur-attente.

- **Métacognition et auto‑régulation** : modèles de Self‑Regulated Learning (Zimmerman, Winne & Hadwin), recommandations EEF sur la métacognition, self-efficacy (Bandura).

- **Émotions et apprentissage** : Control-Value Theory (Pekrun) — anxiété de test, ennui, enthousiasme comme régulateurs de la cognition et de la motivation.

- **Stratégies d'apprentissage fondées sur la preuve** : rappel actif, répétition espacée, interleaving (catégories et contenus), élaboration, double codage, exemples concrets, worked examples et fading (Sweller, van Merriënboer).

- **Personnalisation et systèmes adaptatifs** : cadres pour adaptive learning et systèmes d'apprentissage pilotés par l'IA, modèles de l'apprenant (BKT, PFA), garde‑fous en matière de biais, d'équité et de transparence, mastery learning (Bloom).

- **Modèles d'ingénierie pédagogique** : ADDIE, Merrill's First Principles, taxonomie de Bloom révisée, alignement constructif (Biggs).

---

## Glossaire [v0.9]

### Mastery Score Composite (MSC)

La maîtrise d'un concept est définie par un vecteur à quatre composantes, toutes requises simultanément pour déclarer une **maîtrise robuste** :

```

MSC(concept, niveau Bloom) = (P, R, A, T)

```

| Composante | Définition | Seuil de référence (configurable par univers) |

|---|---|---|

| **P — Précision** | Taux de réussite sur les N dernières occurrences au niveau Bloom cible | ≥ 80% sur N ≥ 5 occurrences |

| **R — Robustesse temporelle** | Au moins une réussite après un délai ≥ D jours sans stimulation du concept | D ≥ 3 jours (court terme), D ≥ 7 jours (moyen terme) |

| **A — Autonomie** | Au moins M réussites sans aide ni indice d'aucune sorte | M ≥ 3 occurrences |

| **T — Transférabilité** | Au moins une réussite sur une tâche de format différent de l'entraînement principal | ≥ 1 occurrence sur format décalé |

**États de maîtrise** :

- **Maîtrise d'entraînement** : P + R + A atteints, T non encore atteint. Suffisante pour progresser dans le graphe, insuffisante pour clore définitivement un concept et désactiver les rappels espacés.

- **Maîtrise robuste** : P + R + A + T atteints. Le concept peut être marqué comme consolidé.

**Règles d'exception** :

- **Dégradation post-maîtrise** : une maîtrise déclarée peut être révoquée si l'étudiant échoue sur 2 occurrences consécutives après une absence ≥ seuil_R. Le concept repasse en état *en consolidation* avec un parcours de réactivation — et non en état *nouveau*.

- **Niveau Bloom différencié** : un concept peut être maîtrisé au niveau *comprendre* mais pas au niveau *analyser*. Le MSC est toujours associé à un niveau Bloom cible — il n'existe pas de maîtrise absolue d'un concept, seulement une maîtrise à un niveau cognitif donné.

**Liens avec les principes** :

- P2 (fading) : déclenché par la progression de la composante A.

- P3 (interleaving) : bascule conditionnée à P + A atteints.

- P6 (feuille blanche) : progression vers les modes sans aide = montée de A.

- ADDIE (révision) : l'écart longitudinal à détecter porte prioritairement sur T.

### Indice de Confiance du Corpus (ICC)

Métadonnée obligatoire déclarée en phase Analyse, calculée à partir du nombre d'annales disponibles, de leur ancienneté et de leur diversité de formats. Conditionne la stratégie de construction du graphe (voir P1). Valeurs : fort / partiel / absent.

### État apprenant composite

Modèle à deux axes (calibration × activation émotionnelle) générant une matrice 3×3 de 9 états avec politiques adaptatives associées (voir P5). MVP : 5 états prioritaires. Cible v2.0 : matrice complète.

---

*Constitution v0.9 — intègre les arbitrages validés issus de l'analyse critique de la v0.8. Prochaine étape : test sur un univers pilote → v1.0.*