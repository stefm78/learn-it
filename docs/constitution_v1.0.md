# Constitution conceptuelle – Learn-it (v1.0)

> **Note de version** : La v1.0 intègre (a) le nouveau **Principe 0 — Calibrage initial**, (b) 9 modifications issues de l'analyse critique approfondie de la v0.9, et (c) les mises à jour du Glossaire et du cycle ADDIE en découlant. Les ajouts et modifications par rapport à la v0.9 sont signalés par `[v1.0]`.

---

## Principes fondamentaux

### Principe 0 — Calibrage initial de l'apprenant `[v1.0]`

Avant l'entrée dans le parcours personnalisé, le système conduit une **phase de calibrage initiale** poursuivant deux objectifs distincts et complémentaires.

**(a) Calibrage épistémique** : estimer la position de l'apprenant dans le graphe de connaissances via un diagnostic adaptatif court (≤ 10 items, configurable par univers). Le résultat initialise l'état du graphe pour cet apprenant, en distinguant les prérequis confirmés maîtrisés, les concepts en doute et les lacunes probables. En l'absence de calibrage épistémique, le système part d'une hypothèse conservatrice (position initiale basse) et délègue à l'apprenant la possibilité de débloquer manuellement des nœuds du graphe qu'il estime déjà maîtrisés.

Pour les concepts déclarés déjà maîtrisés lors du calibrage et confirmés par le pré-test, le MSC peut être initialisé directement à l'état *Maîtrise d'entraînement* (composantes P + R + A présumées atteintes) — mais avec la composante T non encore validée, ce qui génère automatiquement une mission de transfert prioritaire lors des premières sessions.

**(b) Calibrage métacognitif** : estimer le profil de calibration de l'apprenant (auto-efficacité perçue vs performance réelle) en intégrant une **prédiction de performance** dans le pré-test lui-même — avant chaque item ou groupe d'items, l'apprenant prédit s'il va réussir. La comparaison entre prédictions et résultats réels initialise la composante Calibration de l'état apprenant composite (P5). Ce mécanisme constitue la première instance explicite de la boucle métacognitive avant/pendant/après (P9) — le calibrage est ainsi pédagogiquement productif en lui-même, et pas seulement informatif pour le système.

La phase de calibrage est conçue pour être **courte, engageante et immédiatement utile** à l'apprenant : le système lui restitue une première cartographie visuelle de ses connaissances dès la fin du calibrage. Elle ne repose sur aucune typologie de "styles d'apprentissage" empiriquement invalidée (VARK, etc.). Le calibrage est **révisable** : l'apprenant peut contester une inférence initiale et le système permet une correction facile des états mal estimés lors des premières sessions. Toutes les inférences issues du calibrage initial sont traitées avec une **confiance réduite** et renforcées ou révisées en priorité par les données comportementales des premières sessions — elles ne constituent jamais un état figé.

---

### Principe 1 — Primat de la maîtrise des compétences d'examen

Le jeu est conçu d'abord pour garantir la maîtrise des compétences réellement évaluées (telles qu'elles apparaissent dans les objectifs du cours et les annales), puis pour être engageant. Les activités de jeu doivent pouvoir se mapper à des tâches d'examen (résolution de problèmes, modélisation, explication, interprétation de données). L'introduction des tâches complexes de type annale se fait de manière progressive (scaffolding), en contrôlant la charge cognitive : on commence par des versions simplifiées avant de monter vers des sujets multi-étapes. Chaque mission importante précise explicitement sa pertinence par rapport à l'examen (composante Relevance du modèle ARCS) et s'appuie, autant que possible, sur des **exemples concrets** avant de généraliser vers des formes plus abstraites.

Les objectifs d'apprentissage associés à chaque mission sont caractérisés par leur **niveau cognitif cible** selon la taxonomie révisée de Bloom (mémoriser, comprendre, appliquer, analyser, évaluer, créer). La progression de l'étudiant vise une montée en niveaux cognitifs, et non la seule consolidation des niveaux bas.

Le graphe de connaissances est construit à partir des supports de cours et des annales, mais aussi confronté à la structure disciplinaire du domaine, afin d'éviter un rétrécissement du curriculum aux seuls formats d'évaluation. L'**Indice de Confiance du Corpus (ICC)**, calculé à partir du nombre d'annales disponibles, de leur ancienneté et de leur diversité de formats, est déclaré explicitement en phase Analyse et conditionne la stratégie de construction du graphe :

- **ICC fort** (annales complètes) : graphe calibré normalement sur la fréquence des concepts en annales.
- **ICC partiel** (annales incomplètes) : les fréquences sont pondérées et complétées par la structure disciplinaire de référence.
- **ICC absent** (aucune annale fournie) : fallback sur taxonomie Bloom et corpus disciplinaire de référence (référentiel officiel, syllabus, manuels du domaine).

Dans tous les cas, tout concept présent dans le corpus disciplinaire de référence mais absent ou rare dans les annales est maintenu dans le graphe avec un niveau cognitif Bloom minimum *comprendre* et un coefficient de pondération réduit — il n'est jamais supprimé. Une distinction explicite est maintenue entre *concepts fréquents en annales* et *concepts fondamentaux du domaine*, les deux étant nécessaires mais avec des pondérations différentes.

`[v1.0]` Le graphe de connaissances distingue, pour les concepts à fort potentiel de représentation erronée identifié dans le corpus disciplinaire, les **lacunes** (compétence non encore développée) des **misconceptions** (représentation incorrecte fermement ancrée). Les missions ciblant un concept à misconception connue incluent une phase explicite de **conflit cognitif** (confrontation à un cas que la représentation erronée ne peut expliquer) avant de proposer la représentation correcte. Le simple rappel actif ou le scaffolding ne constituent pas des réponses suffisantes à une misconception identifiée. Ce flag *misconception* est optionnel par univers au MVP et requis dès la v1.1 pour tout domaine à fort taux de représentations erronées documentées.

Chaque univers vérifie l'**alignement constructif** (Biggs) dès la phase Analyse : cohérence entre objectifs Bloom, activités de jeu et formes d'évaluation. Tout désalignement détecté entre ces trois dimensions est signalé comme un défaut de design à corriger avant la phase Développement.

---

### Principe 2 — Moteur générique basé sur un graphe de connaissances

Le cœur du système est un moteur générique, indépendant du domaine, qui manipule des concepts, des relations de prérequis et des types de tâches. Chaque cours ou document est représenté comme un graphe orienté de connaissances, sur lequel le jeu instancie des cartes, puzzles, missions et "boss". Le graphe sert explicitement à gérer la charge intrinsèque : tant que certains prérequis ne sont pas maîtrisés, le système évite de proposer des puzzles qui combinent trop de concepts simultanément.

Les décisions adaptatives (quels contenus, dans quel ordre) doivent rester **explicables** : le système communique à l'étudiant, sur demande, les raisons principales de chaque recommandation de parcours, en distinguant les raisons liées aux prérequis manquants, aux lacunes observées, et aux contraintes temporelles. Cette explicabilité est fournie *sur demande explicite de l'étudiant* et, de manière non sollicitée, *uniquement aux moments de transition entre sessions* — jamais en milieu de tâche active, afin d'éviter d'augmenter la charge extrinsèque au moment où la capacité de traitement cognitif est engagée.

Le **fading** des aides est planifié dans le graphe : une fois un concept maîtrisé, le système programme des occurrences sans guidage, même hors contexte d'examen, afin de prévenir la dépendance à l'assistance. La maîtrise n'est considérée comme robuste que lorsqu'elle satisfait l'ensemble du Mastery Score Composite (MSC) défini en Glossaire ; en particulier, le fading des aides est déclenché lorsque la composante **A** (Autonomie) du MSC progresse — et non lorsque la précision seule est élevée.

`[v1.0]` Le fading des aides est planifié selon le rythme de progression du MSC, mais n'impose aucun plancher de guidage minimum : un apprenant dont la composante A progresse rapidement peut demander à tout moment une réduction immédiate du guidage sur un concept donné, sans attendre le seuil planifié. À l'inverse, lorsqu'un guidage fourni génère de la résistance comportementale (ignorance systématique des aides, accélération des réponses malgré les indices), le système traite ce signal comme un indicateur possible de **surqualification** (effet d'inversion de l'expertise, Kalyuga) et propose une réduction proactive du guidage. Dans ce cas, la charge extrinsèque engendrée par un guidage superflu est prioritairement réduite avant d'augmenter la difficulté intrinsèque.

`[v1.0]` Le design vise également à favoriser activement la **formation de schémas** (charge germinale) via des activités qui demandent à l'apprenant de générer, organiser ou expliquer — et pas seulement de répondre. Les missions mobilisant l'auto-explication, la cartographie conceptuelle, l'élaboration de liens entre notions ou l'enseignement fictif (*feigned teaching*) participent à cet objectif et sont distinguées des missions de rappel actif pur dans le graphe de design. La réduction de la charge extrinsèque est une condition nécessaire mais non suffisante : un design efficace favorise simultanément la schématisation active.

---

### Principe 3 — Temporalité et mémoire comme mécanismes centraux

La dynamique du jeu intègre explicitement la courbe de l'oubli : chaque concept possède un niveau de stabilité mémorielle qui évolue dans le temps. La répétition espacée et le rappel actif sont intégrés au cœur du gameplay (retours planifiés, anomalies, quêtes de réactivation), et non ajoutés comme un module annexe. L'usage des difficultés dites "désirables" est calibré : une difficulté n'est légitime que si elle augmente la consolidation ou le transfert sans dépasser durablement les capacités de traitement et d'autorégulation de l'étudiant. Lorsqu'une difficulté cesse d'être productive, le système revient provisoirement à la démonstration, au guidage et aux exemples travaillés avant de réaugmenter l'exigence.

La planification temporelle vise explicitement à combiner **espacement** et **rappel actif**, plutôt qu'à s'appuyer sur de simples relectures passives. L'**interleaving** est appliqué en priorité sous sa forme de **variation de types de problèmes** (interleaving de catégories), dont l'effet sur la discrimination et le transfert est le plus robuste empiriquement. L'interleaving de contenus distincts est introduit plus progressivement, après une première phase de bloc homogène sur chaque contenu nouveau. La bascule vers l'interleaving de contenus est conditionnée à l'atteinte simultanée des composantes **P** (Précision) et **A** (Autonomie) du MSC sur chaque contenu concerné. Valeur de référence par défaut : ≥ 2 réussites consécutives sans aide sur ≥ 3 tâches distinctes du niveau Bloom cible — ce seuil est configurable par univers.

`[v1.0]` L'interleaving par catégories est soumis à une contrainte de **couverture équilibrée** : lors de chaque cycle d'interleaving, le système veille à ce qu'aucun item d'une catégorie ne soit systématiquement moins pratiqué que les autres items de cette même catégorie. Un déséquilibre de couverture documenté entre items d'une même catégorie (un item non présenté depuis ≥ 2× le délai moyen des autres) déclenche une rééquilibration prioritaire. Ce garde-fou prévient l'effet d'interférence du rappel actif (*retrieval-induced forgetting*, Anderson et al.) par lequel la pratique intensive de certains items peut inhiber le rappel des items connexes moins pratiqués.

`[v1.0]` L'exposition préalable à l'échec avant instruction directe (*productive failure*, Kapur) peut améliorer la compréhension profonde pour certains types de problèmes et certains profils d'apprenants. Cette stratégie est considérée comme incompatible avec les contraintes de gestion du temps jusqu'à l'examen pour le MVP, et n'est pas intégrée au moteur par défaut. Tout univers souhaitant l'intégrer doit le déclarer explicitement dans sa documentation de design et définir les conditions d'apprenant et de concept pour lesquelles elle est activée.

Après une interruption d'activité supérieure au seuil de robustesse temporelle (seuil_R, configurable par univers), le système déclenche une **session de reprise** avant de reprendre le parcours planifié : diagnostic léger (3 à 5 tâches de rappel sur les concepts récemment maîtrisés), bilan de l'état du graphe et recalcul du chemin vers l'échéance. Les concepts dont la composante R du MSC est dégradée repassent en état *en consolidation* avec un parcours de réactivation court — et non en état *nouveau*.

---

### Principe 4 — Planification vers une date cible

L'étudiant indique une date d'examen (et éventuellement un niveau visé). Le système planifie et réajuste un chemin d'apprentissage pour maximiser la probabilité d'atteindre un niveau de maîtrise suffisant à cette échéance, en tenant compte du temps disponible et de la difficulté des contenus. La planification intègre des contraintes de charge : chaque session limite le nombre d'éléments nouveaux en interaction et découpe les thèmes intrinsèquement complexes en sous-blocs digestes.

La représentation de l'échéance est conçue pour être **mobilisatrice et non anxiogène** : le système présente la progression accomplie et le chemin restant de manière équilibrée, sans surexposer la distance à l'objectif. La planification n'est pas imposée de manière rigide : le système propose un chemin recommandé mais laisse des marges de choix (ordre de certains modules, types de missions) afin de soutenir le besoin d'autonomie et d'entraîner la capacité de planification de l'étudiant. Ce chemin combine de manière explicite des phases de **découverte**, des blocs de **rappel actif espacés**, et des sessions **interleavées** où anciens et nouveaux contenus sont travaillés conjointement.

---

### Principe 5 — Hyper-personnalisation du parcours

Le parcours n'est pas uniforme. La difficulté, le rythme d'introduction de nouveaux concepts, le choix des missions et la répartition entre découverte, rappel et entraînement "type annale" sont adaptés en continu aux performances, au profil et aux objectifs de l'étudiant. Cette personnalisation vise explicitement à maintenir la charge cognitive dans une zone gérable (ni sous-stimulation, ni surcharge) et à réduire la charge extrinsèque inutile.

La personnalisation est pilotée par un **modèle d'état apprenant composite**, défini par deux axes orthogonaux :

- **Axe 1 — Calibration** (compétence perçue vs réelle) : *bien calibré* (auto-efficacité ≈ performance), *surestimateur* (auto-efficacité > performance), *sous-estimateur* (auto-efficacité < performance). Cet axe est initialisé par le calibrage métacognitif (P0) et mis à jour en continu.
- **Axe 2 — Activation émotionnelle** (Pekrun, Control-Value Theory) : *zone productive* (enthousiasme, engagement modéré), *zone anxiogène* (anxiété élevée, signaux d'abandon), *zone ennui/désinvestissement* (sous-stimulation).

Ces deux axes génèrent une matrice 3×3 de 9 états, chacun associé à une politique adaptative distincte (difficulté, type de tâche, feedback, message). Pour le MVP, les 5 états prioritaires sont : bien calibré/productif, surestimateur/productif, sous-estimateur/productif, bien calibré/anxiogène, bien calibré/ennui. La matrice complète constitue la cible v2.0.

Ce modèle composite remplace une hiérarchie fixe de signaux : il n'impose pas de priorité absolue entre performance, auto-efficacité et signaux affectifs, mais définit le régime approprié selon l'état réel détecté. Un étudiant en état de *flow* (performance élevée, engagement maximal) n'est pas interrompu par des ajustements adaptatifs même si des signaux secondaires déclenchent des alertes.

`[v1.0]` **Validité inférentielle** : toute règle d'inférence comportement → état apprenant (anxiété, ennui, flow, surcharge) doit être considérée comme une hypothèse à valider empiriquement, et non comme une connaissance établie. Pour chaque univers, la phase Analyse documente les signaux comportementaux retenus comme proxys d'état et les conditions dans lesquelles cette inférence a été validée ou est seulement supposée. Tout univers déployé sans validation empirique des inférences affectives doit déclarer explicitement ce statut dans sa documentation de design. La détection de l'état de flow en particulier — dont les proxys comportementaux peuvent coïncider avec l'exécution automatique sans engagement profond — doit spécifier ses critères de distinction dans la documentation.

`[v1.0]` **Équité algorithmique** : la surveillance des écarts systématiques de recommandations entre profils d'apprenants est opérationnalisée comme suit. Les profils surveillés sont définis *a priori* dans la documentation de chaque univers : a minima, le niveau initial estimé (via calibrage P0) et la régularité d'usage. Pour tout attribut protégé pertinent dans le contexte d'usage (niveau scolaire, langue principale, contexte d'accès), les métriques d'équité retenues (par ex., taux de maîtrise MSC atteint, temps moyen jusqu'au MSC, taux d'abandon) sont documentées et comparées entre groupes. Un écart systématique supérieur au seuil défini par univers déclenche une révision du modèle adaptatif — et pas seulement un signalement. Cette surveillance est activée dès le MVP pour les attributs a minima (niveau initial, régularité), et étendue aux attributs protégés complets en v2.0.

La personnalisation surveille également les **écarts systématiques de recommandations entre profils d'apprenants** et signale toute disparité notable nécessitant une révision du modèle. L'adaptation reste **ouverte** : le système recommande un niveau de difficulté "sûr" mais permet à l'étudiant de choisir des défis plus ambitieux. Aucun plafond de difficulté n'est imposé de manière définitive : les protections passent par le scaffolding (indices, décomposition) et des messages d'avertissement, pas par le blocage de contenus.

---

### Principe 6 — Transition progressive vers la "feuille blanche"

Le jeu propose plusieurs modes qui rapprochent progressivement l'expérience ludique du format réel de l'examen (problèmes longs, réponses libres, usage de papier/whiteboard). L'objectif est que les compétences développées dans le jeu se transfèrent sans rupture au contexte d'évaluation (annales, copie papier, épreuve en conditions réelles), en augmentant progressivement la complexité et en réduisant les aides pour ne pas provoquer de surcharge brutale.

Le transfert visé est prioritairement un **transfert proche** vers les conditions d'évaluation réelles. Cependant, une partie des missions d'intégration propose des contextes applicatifs légèrement décalés du format d'examen, afin de tester la robustesse de la compréhension au-delà de la simple familiarité au format. Les modes "simulation d'examen" doivent être ressentis comme des défis atteignables, avec des critères de réussite clairs, pour renforcer le sentiment de compétence. La progression vers les modes sans aide correspond à la montée de la composante **A** (Autonomie) du MSC.

---

### Principe 7 — Adaptation à l'environnement d'usage

Le système s'adapte aux contraintes contextuelles de l'étudiant (transport, bureau, bibliothèque, temps court/long). Différents modes (micro-sessions de rappel, entraînements longs, simulations d'examen) sont proposés, tout en restant alignés sur la même trajectoire globale d'apprentissage. Les modes courts privilégient des tâches à faible charge (peu d'éléments en interaction), tandis que les modes longs peuvent accueillir des problèmes plus complexes avec un guidage adéquat. Lorsque c'est pertinent, certains modes peuvent encourager l'usage de supports physiques (papier, whiteboard) pour préparer la transition vers la feuille blanche.

Le système intègre un modèle de **fatigue cognitive intra-session** : les missions impliquant une forte charge intrinsèque (boss, problèmes multi-étapes, tâches de niveau Bloom *analyser* ou supérieur) sont positionnées en début ou milieu de session. Au-delà d'un seuil de durée de travail actif (configurable, valeur de référence : 25 minutes), le système bascule automatiquement vers des formats à faible charge (rappel guidé, reconnaissance, révision d'exemples travaillés) plutôt que vers des tâches de production ou d'analyse. Ce seuil est signalé à l'étudiant de manière non anxiogène.

---

### Principe 8 — Gamification éthique centrée sur l'effort cognitif

Les mécaniques d'engagement (récompenses, progression, défis) servent en priorité l'effort intellectuel et la maîtrise des compétences, et non la simple rétention d'attention. Un mécanisme d'engagement qui améliore la persistance à court terme mais dégrade la qualité du traitement cognitif, l'autonomie perçue ou la compréhension à long terme doit être considéré comme contraire à la constitution. Les récompenses extrinsèques sont utilisées préférentiellement en phase d'amorçage et progressivement retirées au profit du sentiment de compétence et de progrès intrinsèque, afin de soutenir l'intériorisation de la motivation (SDT : régulation identifiée puis intégrée).

Les éléments visuels et interactifs sont soumis à deux régimes distincts selon leur nature :

- **(a) Éléments multimédia pédagogiques** (contenus, explications, feedbacks) : principe de cohérence de Mayer strict — seuls les éléments qui contribuent directement à la compréhension sont inclus, la redondance entre modalités est évitée, et la charge extrinsèque est minimisée.
- **(b) Éléments de gamification** (animations de récompense, badges, effets visuels) : **test de non-nuisance** — l'élément est acceptable s'il ne dégrade ni la motivation intrinsèque (SDT) ni l'effort cognitif productif. Le critère n'est pas la redondance Mayer (une animation de récompense est par nature redondante avec le contenu) mais l'absence d'effet négatif mesurable sur l'apprentissage ou l'autonomie.

`[v1.0]` Le test de non-nuisance exige, lors de la phase Évaluation, la vérification d'au moins l'un des indicateurs suivants : absence de dégradation du MSC moyen sur les sessions contenant l'élément par rapport aux sessions sans l'élément ; absence de corrélation positive entre l'exposition à l'élément et la réduction de la composante A du MSC ; absence de corrélation positive entre l'exposition et l'abandon des missions complexes. Tant que cet indicateur n'a pas été vérifié, l'élément est considéré comme **en période probatoire** et son déploiement à large échelle est suspendu.

Les récompenses sont reliées de façon significative au contenu appris, et les systèmes de points/bonus évitent de nuire à la motivation intrinsèque.

---

### Principe 9 — Développement de la métacognition, de l'auto-régulation et du lien social

Le jeu aide l'étudiant à apprendre à apprendre : calibrer sa confiance, planifier, monitorer et évaluer son propre apprentissage. Il met en regard perception de maîtrise et données réelles, explicite les raisons pédagogiques des mécaniques (rappel, espacement, interleaving) et propose des moments de réflexion sur les stratégies utilisées. Concrètement, le jeu structure la plupart des activités en trois temps :

- **Avant la tâche** : clarification du but, éventuellement choix entre plusieurs priorités ou types de missions, et brève anticipation de la difficulté (forethought).
- **Pendant la tâche** : incitations ponctuelles à estimer sa confiance ou à vérifier sa compréhension (monitoring), sans interrompre excessivement le flux de jeu.
- **Après la tâche** : synthèse des erreurs, comparaison entre confiance déclarée et performance réelle, invitation à identifier ce qui a le mieux aidé ou ce qui sera changé la prochaine fois (self-reflection). Certains prompts de réflexion encouragent explicitement l'**élaboration** (faire des liens avec d'autres notions, trouver des exemples) et l'usage de **double codage** (verbal + visuel) lorsque les deux représentations sont complémentaires et non redondantes.

Les invitations métacognitives avant/pendant/après **varient en format** (question ouverte, choix entre 2–3 options, prédiction chiffrée, complétion de phrase) et ne sont pas systématiques à chaque micro-tâche. La variabilité est planifiée pour maintenir un effet de surprise cognitif et prévenir la réponse automatique sans engagement réel. Les formats les plus guidés (choix fermés, exemples de réponse) sont réservés aux apprenants novices ou en forte charge cognitive.

L'**intensité des prompts métacognitifs est elle-même scaffoldée** : pour les apprenants novices ou en situation de forte charge cognitive, les invitations à la réflexion sont plus guidées et moins fréquentes, puis progressivement retirées à mesure que l'étudiant internalise ces routines. Les stratégies métacognitives (planification, monitoring, réflexion) font l'objet d'une **modélisation explicite** avant d'être demandées de manière autonome.

`[v1.0]` La clarification du but de tâche (phase *avant*) intègre un garde-fou sur la **représentation de la tâche** : le système vérifie, par une formulation explicite de l'objectif et un bref écho de compréhension attendu, que l'apprenant s'est fixé le même but que celui prévu par le design. Un étudiant qui se fixerait un but de surface (terminer la mission, obtenir la récompense) au lieu d'un but d'apprentissage (comprendre le concept, réussir sans aide) compromet l'ensemble de la boucle SRL. Ce garde-fou est particulièrement actif lors des premières occurrences de chaque nouveau type de mission.

Le système intègre une **dimension affective** : il adapte son discours et sa difficulté en réponse aux signaux comportementaux d'anxiété ou de frustration détectés (abandon précoce, taux d'erreur inhabituel, refus de missions). L'ennui et la sous-stimulation sont traités comme des signaux d'alarme **symétriques** à l'anxiété (Pekrun, Control-Value Theory) : une sous-stimulation détectée — signaux comportementaux d'engagement minimal, performance anormalement haute sans effort apparent, accélération des réponses — déclenche une réponse adaptative équivalente à une surcharge : augmentation de la difficulté, changement de type de tâche ou introduction d'une nouvelle contrainte. Ni l'anxiété ni l'ennui ne sont nommés cliniquement dans les messages.

Dans la mesure du possible, le système intègre une dimension de lien (classement coopératif, défis partagés) afin de soutenir le besoin de *relatedness* sans générer de comparaison sociale malsaine. La dimension sociale est introduite via une **exposition progressive et réversible** : après un seuil d'usage établi (valeur de référence : 5 sessions complétées), le système propose activement une fonctionnalité sociale concrète et non intrusive, avec option de désactivation simple et permanente à tout moment.

`[v1.0]` Au-delà du besoin d'appartenance (SDT), certaines missions peuvent intégrer une dimension d'**apprentissage par les pairs** (confrontation d'erreurs, enseignement mutuel, co-résolution), dont les effets sur la compréhension profonde et la métacognition sont distincts des effets motivationnels du lien social. Ces missions sont designées pour activer la Zone Proximale de Développement (Vygotsky) : elles proposent des tâches légèrement au-delà du niveau de maîtrise individuelle actuel, dans un cadre où l'interaction avec un pair constitue l'aide principale. Cette dimension est **optionnelle par univers** et non requise au MVP ; sa présence doit être explicitement justifiée, ou son absence motivée, dans la documentation de design.

---

### Principe 10 — Qualité du feedback et modèle implicite de la compétence

Le feedback généré par le système porte en priorité sur le **processus** (stratégies utilisées, erreurs procédurales, pistes de révision) et sur l'**autorégulation** (comment l'étudiant pourrait ajuster son approche), plutôt que sur la personne ou les aptitudes. Les messages de réussite soulignent l'effort, la stratégie et la progression, afin de renforcer une conception malléable de la compétence. Tout feedback évaluatif global ("tu maîtrises ce chapitre") est accompagné d'une indication de son niveau de fiabilité et des conditions dans lesquelles cette inférence a été établie.

---

## Cycle de design pédagogique

Le design des univers d'apprentissage dans Learn-it suit un cycle explicite, inspiré des modèles d'ingénierie pédagogique (notamment ADDIE) et des First Principles of Instruction de Merrill :

### 1. Analyse

Identifier les objectifs d'apprentissage et les compétences d'examen associées, extraire les concepts et relations clés à partir des supports (cours, exercices, annales) et construire le graphe de connaissances correspondant. Pour chaque objectif, les verbes d'action sont positionnés dans la **taxonomie de Bloom révisée** (mémoriser, comprendre, appliquer, analyser, évaluer, créer), afin de garantir que les missions de jeu couvrent les niveaux cognitifs visés par le cours et non seulement les niveaux les plus facilement gamifiables.

L'**ICC** (Indice de Confiance du Corpus) est déclaré explicitement à cette phase et conditionne la stratégie de construction du graphe (voir P1). L'**alignement constructif** (Biggs) est vérifié : cohérence entre objectifs, activités et formes d'évaluation.

`[v1.0]` La phase Analyse définit également : (a) les **signaux comportementaux** retenus comme proxys d'états apprenants (anxiété, ennui, flow, surcharge) et leur statut de validation empirique ; (b) les **profils d'apprenants** surveillés pour l'équité algorithmique et les métriques d'équité associées ; (c) les concepts à **flag misconception** dans le graphe, le cas échéant.

Tout univers d'apprentissage doit expliciter les compétences visées, leur position dans une progression de complexité, les tâches authentiques de référence, les niveaux cognitifs sollicités, les formes de guidage prévues, les preuves attendues de maîtrise (référencées au MSC) et les conditions de révision après usage.

### 2. Design

Pour chaque objectif et partie du graphe, définir des problèmes authentiques et une trajectoire d'apprentissage de type **activation → démonstration → application → intégration**, en les traduisant en types de missions, puzzles, cartes et "boss" alignés avec les 10 principes. La trajectoire activation → démonstration → application → intégration constitue une **contrainte systématique de design**, et non une simple inspiration : chaque univers doit couvrir ces quatre phases pour chaque objectif cible.

`[v1.0]` La phase Design précise également : (a) les missions de type **conflit cognitif** pour chaque concept flaggé *misconception* ; (b) les missions de type **génératif** (auto-explication, cartographie, enseignement fictif) distinctes des missions de rappel actif pur ; (c) la décision d'inclure ou d'exclure la *productive failure* et, si incluse, les conditions d'activation.

### 3. Développement

Produire les contenus jouables (énoncés, interfaces, feedbacks, paramètres adaptatifs) en respectant les contraintes de charge cognitive, de motivation, de métacognition, de stratégies fondées sur la preuve et d'éthique de la personnalisation.

### 4. Implémentation

`[v1.0]` Déployer l'univers d'apprentissage auprès des étudiants, configurer les paramètres d'adaptation et les liens avec l'environnement réel (calendrier d'examen, modes d'usage). Les éléments de gamification non encore soumis au test de non-nuisance sont déployés en **mode probatoire** : leur collecte de données est activée dès cette phase pour permettre la vérification lors de la phase Évaluation.

### 5. Évaluation et révision

Recueillir des données sur la maîtrise réelle des objectifs (performances aux missions clés, simulations d'examen, résultats d'évaluation externe) et sur l'expérience des utilisateurs, puis ajuster le graphe, les missions et les paramètres adaptatifs.

Le déclencheur de révision du modèle d'inférence est défini en termes d'**écarts longitudinaux intra-individuels** :

- **Écart ponctuel** : maîtrise estimée par le système supérieure à la performance réelle lors d'une simulation d'examen → signalement immédiat et ajustement du modèle pour les concepts concernés.
- **Biais systématique** : sur ≥ 3 évaluations consécutives, le système surestime ou sous-estime de manière cohérente (écart médian > 20%) → révision du modèle d'inférence pour ce concept ou ce type de tâche.
- **Dérive hors-jeu** : performance en simulation stable mais résultats réels (examen intermédiaire, devoir rendu) systématiquement inférieurs → revoir le paramètre de transfert du graphe. Ce troisième cas porte spécifiquement sur la composante **T** (Transférabilité) du MSC.

`[v1.0]` La phase Évaluation inclut systématiquement : (a) la **vérification du test de non-nuisance** pour tout élément de gamification en période probatoire ; (b) la **vérification des métriques d'équité** définies en phase Analyse, avec déclenchement d'une révision si les écarts dépassent les seuils définis ; (c) la **confrontation des règles d'inférence comportement → état** aux données observées, avec mise à jour du statut de validation dans la documentation.

Ce mécanisme est valide pour un usage individuel comme collectif. Pour un usage en cohorte, un écart > 15% sur ≥ 10 apprenants peut déclencher une révision du modèle commun. Ce cycle est itératif : les univers peuvent être révisés régulièrement pour rester cohérents avec la constitution et les retours du terrain.

---

## Cadres théoriques de référence

Les principes ci-dessus ont été confrontés, critiqués et ajustés à la lumière des cadres théoriques suivants :

- **Cognition et charge mentale** : Cognitive Load Theory (Sweller, van Merriënboer) — charge intrinsèque, extrinsèque et germinale ; effet d'inversion de l'expertise (Kalyuga) ; Desirable Difficulties (Bjork) ; *retrieval-induced forgetting* (Anderson et al.) ; théorie de l'apprentissage multimédia (Mayer — 12 principes dont cohérence, segmentation, redondance) ; *productive failure* (Kapur).

- **Motivation et engagement** : Self-Determination Theory (Deci & Ryan), modèle ARCS (Keller), théories de la motivation de la réussite et de la valeur-attente.

- **Métacognition et auto-régulation** : modèles de Self-Regulated Learning (Zimmerman ; Winne & Hadwin — task definition, boucles COPES), recommandations EEF sur la métacognition, self-efficacy (Bandura).

- **Émotions et apprentissage** : Control-Value Theory (Pekrun) — anxiété de test, ennui, enthousiasme comme régulateurs de la cognition et de la motivation.

- **Stratégies d'apprentissage fondées sur la preuve** : rappel actif, répétition espacée, interleaving (catégories et contenus), élaboration, double codage, exemples concrets, worked examples et fading (Sweller, van Merriënboer) ; apprentissage génératif (Fiorella & Mayer).

- **Apprentissage social et constructivisme** : Zone Proximale de Développement (Vygotsky), apprentissage par les pairs, enseignement mutuel.

- **Misconceptions et changement conceptuel** : conflit cognitif, réfutation explicite (Posner et al., Chi).

- **Personnalisation et systèmes adaptatifs** : cadres pour adaptive learning et systèmes d'apprentissage pilotés par l'IA, modèles de l'apprenant (BKT, PFA), garde-fous en matière de biais, d'équité et de transparence, mastery learning (Bloom).

- **Modèles d'ingénierie pédagogique** : ADDIE, Merrill's First Principles, taxonomie de Bloom révisée, alignement constructif (Biggs), assessment for learning (Black & Wiliam).

---

## Glossaire

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
| **T — Transférabilité** | Voir définition étendue ci-dessous | Voir ci-dessous |

**`[v1.0]` Composante T — Transférabilité (définition étendue)**

Au moins une réussite sur un format *structurellement différent* de l'entraînement principal (transfert intra-jeu). Pour les univers disposant d'une mesure externe (simulation hors-jeu, devoir rendu, examen intermédiaire), au moins une réussite sur cette mesure externe est requise pour valider le transfert hors-jeu.

En l'absence de mesure externe disponible, la Transférabilité intra-jeu suffit pour déclarer la *maîtrise robuste*, mais une **note de risque T** est inscrite dans le modèle de l'apprenant, signalant que le transfert hors-jeu n'a pas été vérifié. La phase Évaluation du cycle ADDIE doit prévoir systématiquement au moins une mesure externe de transfert. La dérive hors-jeu détectée en phase Évaluation porte spécifiquement sur cette composante.

**États de maîtrise** :

- **Maîtrise d'entraînement** : P + R + A atteints, T non encore atteint. Suffisante pour progresser dans le graphe, insuffisante pour clore définitivement un concept et désactiver les rappels espacés.
- **Maîtrise robuste** : P + R + A + T atteints (T intra-jeu au minimum, T hors-jeu si mesure disponible). Le concept peut être marqué comme consolidé.

**Règles d'exception** :

- **Dégradation post-maîtrise** : une maîtrise déclarée peut être révoquée si l'étudiant échoue sur 2 occurrences consécutives après une absence ≥ seuil_R. Le concept repasse en état *en consolidation* avec un parcours de réactivation — et non en état *nouveau*.
- **Niveau Bloom différencié** : un concept peut être maîtrisé au niveau *comprendre* mais pas au niveau *analyser*. Le MSC est toujours associé à un niveau Bloom cible — il n'existe pas de maîtrise absolue d'un concept, seulement une maîtrise à un niveau cognitif donné.

**Liens avec les principes** :

- P0 (calibrage) : pour les concepts confirmés en pré-test, le MSC est initialisé à Maîtrise d'entraînement (P + R + A présumés), T à valider.
- P2 (fading) : déclenché par la progression de la composante A.
- P3 (interleaving) : bascule conditionnée à P + A atteints.
- P6 (feuille blanche) : progression vers les modes sans aide = montée de A.
- ADDIE (révision) : l'écart longitudinal à détecter porte prioritairement sur T.

---

### Indice de Confiance du Corpus (ICC)

Métadonnée obligatoire déclarée en phase Analyse, calculée à partir du nombre d'annales disponibles, de leur ancienneté et de leur diversité de formats. Conditionne la stratégie de construction du graphe (voir P1). Valeurs : **fort** / **partiel** / **absent**.

---

### État apprenant composite

Modèle à deux axes (calibration × activation émotionnelle) générant une matrice 3×3 de 9 états avec politiques adaptatives associées (voir P5). Initialisé par le calibrage métacognitif (P0). MVP : 5 états prioritaires. Cible v2.0 : matrice complète.

---

### Flag Misconception `[v1.0]`

Attribut d'un nœud du graphe de connaissances signalant qu'une représentation erronée fermement ancrée est documentée pour ce concept dans le corpus disciplinaire de référence. Déclenche l'obligation d'une mission de type *conflit cognitif* en phase Design. Optionnel par univers au MVP, requis en v1.1 pour les domaines à fort taux de misconceptions documentées.

---

### Période probatoire (gamification) `[v1.0]`

Statut d'un élément de gamification déployé en Implémentation mais dont le test de non-nuisance n'a pas encore été vérifié en phase Évaluation. En période probatoire, l'élément est actif mais sa collecte de données est obligatoire et son déploiement à large échelle est suspendu jusqu'à vérification.

---

*Constitution v1.0 — intègre le Principe 0 (Calibrage initial) et les 9 modifications issues de l'analyse critique de la v0.9. Prochaine étape : test sur un univers pilote → v1.1.*
