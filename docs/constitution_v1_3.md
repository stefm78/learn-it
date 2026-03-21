# Constitution conceptuelle – Learn-it (v1.3)

> **Note de version** : La v1.3 intègre les recommandations issues de quatre analyses critiques indépendantes de la v1.2 au regard des cadres théoriques (CLT, SDT, SRL, stratégies fondées sur la preuve, ingénierie pédagogique) et de la contrainte d'architecture sans IA continue. Les modifications portent sur huit points : (1) reformulation de P0 introduisant l'état *maîtrise provisoire héritée* ; (2) ancrage de P3 sur un algorithme d'espacement explicite (renvoi DA-4) ; (3) reformulation de P5 remplaçant les labels psychologiques de l'axe émotionnel par des régimes observables décisionnels ; (4) reformulation de P9 distinguant internalisation et évitement des routines métacognitives, et posant les états affectifs comme régimes opérationnels et non comme diagnostics ; (5) reformulation de P10 clarifiant le régime nominal du feedback (templates paramétriques) ; (6) ajout d'un protocole de validation du graphe produit par la chaîne IA de conception dans la phase Analyse du cycle ADDIE ; (7) nouveau Principe 11 érigeant la séparation des couches (conception / moteur autonome / patchs) en principe cardinal ; (8) nouveau Principe 12 définissant les contraintes des patchs IA. Le contenu des principes non modifiés est inchangé par rapport à la v1.2.

> **Principe de gouvernance des deux documents** : La constitution est modifiée par délibération explicite lorsqu'un principe s'avère inadapté ou incomplet. Le Référentiel est révisé librement à partir des données terrain, sans toucher à la constitution. Un élément appartient à la constitution s'il répond à la question *"quoi et pourquoi"*. Il appartient au Référentiel s'il répond à la question *"combien et comment"*.

---

## Principes fondamentaux

### Principe 0 — Calibrage initial de l'apprenant

Avant l'entrée dans le parcours personnalisé, le système conduit une **phase de calibrage initiale** poursuivant deux objectifs distincts et complémentaires.

**(a) Calibrage épistémique** : estimer la position de l'apprenant dans le graphe de connaissances via un diagnostic adaptatif court. Le résultat initialise l'état du graphe pour cet apprenant, en distinguant les prérequis confirmés maîtrisés, les concepts en doute et les lacunes probables. En l'absence de calibrage épistémique, le système part d'une **hypothèse conservatrice** (position initiale basse) et délègue à l'apprenant la possibilité de débloquer manuellement des nœuds du graphe qu'il estime déjà maîtrisés.

Pour les concepts déclarés déjà maîtrisés lors du calibrage et confirmés par le pré-test, le MSC est initialisé à l'état **maîtrise provisoire héritée** — état distinct de la *maîtrise d'entraînement* — dans lequel les composantes P, R et A sont *présumées* mais non encore corroborées par des observations en usage. Un pré-test évalue la performance actuelle ; il ne valide pas la robustesse temporelle (composante R) ni l'autonomie sans aide répétée (composante A). La maîtrise provisoire héritée génère automatiquement une vérification prioritaire de R et A lors des trois premières sessions : si ces composantes sont confirmées, le concept passe en *maîtrise d'entraînement* ; sinon, il repasse en état *en consolidation* avec un parcours de réactivation. La composante T n'est pas validée dans cet état initial, ce qui génère une mission de transfert prioritaire.

**(b) Calibrage métacognitif** : estimer le profil de calibration de l'apprenant (auto-efficacité perçue vs performance réelle) en intégrant une **prédiction de performance** dans le pré-test lui-même. La comparaison entre prédictions et résultats réels initialise la composante Calibration de l'état apprenant composite (P5). Ce mécanisme constitue la première instance explicite de la boucle métacognitive avant/pendant/après (P9) — le calibrage est ainsi pédagogiquement productif en lui-même, et pas seulement informatif pour le système.

La phase de calibrage est conçue pour être **courte, engageante et immédiatement utile** à l'apprenant : le système lui restitue une première cartographie visuelle de ses connaissances dès la fin du calibrage. Elle ne repose sur aucune typologie de "styles d'apprentissage" empiriquement invalidée (VARK, etc.). Le calibrage est **révisable** : l'apprenant peut contester une inférence initiale et le système permet une correction facile des états mal estimés lors des premières sessions. Toutes les inférences issues du calibrage initial sont traitées avec une **confiance réduite** et renforcées ou révisées en priorité par les données comportementales des premières sessions — elles ne constituent jamais un état figé.

---

### Principe 1 — Primat de la maîtrise des compétences d'examen

Le jeu est conçu d'abord pour garantir la maîtrise des compétences réellement évaluées (telles qu'elles apparaissent dans les objectifs du cours et les annales), puis pour être engageant. Les activités de jeu doivent pouvoir se mapper à des tâches d'examen (résolution de problèmes, modélisation, explication, interprétation de données). L'introduction des tâches complexes de type annale se fait de manière progressive (scaffolding), en contrôlant la charge cognitive : on commence par des versions simplifiées avant de monter vers des sujets multi-étapes. Chaque mission importante précise explicitement sa pertinence par rapport à l'examen (composante Relevance du modèle ARCS) et s'appuie, autant que possible, sur des **exemples concrets** avant de généraliser vers des formes plus abstraites.

Les objectifs d'apprentissage associés à chaque mission sont caractérisés par leur **niveau cognitif cible** selon la taxonomie révisée de Bloom (mémoriser, comprendre, appliquer, analyser, évaluer, créer). La progression de l'étudiant vise une montée en niveaux cognitifs, et non la seule consolidation des niveaux bas.

Le graphe de connaissances est construit à partir des supports de cours et des annales, mais aussi confronté à la structure disciplinaire du domaine, afin d'éviter un rétrécissement du curriculum aux seuls formats d'évaluation. L'**Indice de Confiance du Corpus (ICC)**, calculé à partir du nombre d'annales disponibles, de leur ancienneté et de leur diversité de formats, est déclaré explicitement en phase Analyse et conditionne la stratégie de construction du graphe :

- **ICC fort** (annales complètes) : graphe calibré normalement sur la fréquence des concepts en annales.
- **ICC partiel** (annales incomplètes) : les fréquences sont pondérées et complétées par la structure disciplinaire de référence.
- **ICC absent** (aucune annale fournie) : fallback sur taxonomie Bloom et corpus disciplinaire de référence (référentiel officiel, syllabus, manuels du domaine).

Dans tous les cas, tout concept présent dans le corpus disciplinaire de référence mais absent ou rare dans les annales est maintenu dans le graphe avec un niveau cognitif Bloom minimum et un coefficient de pondération réduit — il n'est **jamais supprimé**. Une distinction explicite est maintenue entre *concepts fréquents en annales* et *concepts fondamentaux du domaine*, les deux étant nécessaires mais avec des pondérations différentes.

Le graphe de connaissances distingue, pour les concepts à fort potentiel de représentation erronée identifié dans le corpus disciplinaire, les **lacunes** (compétence non encore développée) des **misconceptions** (représentation incorrecte fermement ancrée). Les missions ciblant un concept à misconception connue incluent une phase explicite de **conflit cognitif** (confrontation à un cas que la représentation erronée ne peut expliquer) avant de proposer la représentation correcte. Le simple rappel actif ou le scaffolding ne constituent pas des réponses suffisantes à une misconception identifiée.

Chaque univers vérifie l'**alignement constructif** (Biggs) dès la phase Analyse : cohérence entre objectifs Bloom, activités de jeu et formes d'évaluation. Tout désalignement détecté entre ces trois dimensions est signalé comme un défaut de design à corriger avant la phase Développement.

Tout univers dont les objectifs dépassent la seule réussite à l'examen déclare explicitement un **objectif de transfert lointain** en phase Analyse. En son absence, l'univers est documenté comme *à portée examen uniquement* — ce statut est visible dans sa documentation de design et ne constitue pas un défaut, mais une déclaration explicite de périmètre. Toute allégation de transfert au-delà du jeu ou du format d'entraînement doit être adossée à une mesure externe dédiée, explicitement prévue dans le design de l'univers.

---

### Principe 2 — Moteur générique basé sur un graphe de connaissances

Le cœur du système est un moteur générique, indépendant du domaine, qui manipule des concepts, des relations de prérequis et des types de tâches. Chaque cours ou document est représenté comme un graphe orienté de connaissances, sur lequel le jeu instancie des cartes, puzzles, missions et "boss". Le graphe sert explicitement à gérer la charge intrinsèque : tant que certains prérequis ne sont pas maîtrisés, le système évite de proposer des puzzles qui combinent simultanément un trop grand nombre de concepts non consolidés.

Les décisions adaptatives (quels contenus, dans quel ordre) doivent rester **explicables** : le système communique à l'étudiant, sur demande, les raisons principales de chaque recommandation de parcours, en distinguant les raisons liées aux prérequis manquants, aux lacunes observées, et aux contraintes temporelles. Cette explicabilité est fournie *sur demande explicite de l'étudiant* et, de manière non sollicitée, *uniquement aux moments de transition entre sessions* — jamais en milieu de tâche active, afin d'éviter d'augmenter la charge extrinsèque au moment où la capacité de traitement cognitif est engagée.

Le **fading** des aides est planifié dans le graphe : une fois un concept maîtrisé, le système programme des occurrences sans guidage, même hors contexte d'examen, afin de prévenir la dépendance à l'assistance. Le fading est déclenché par la progression de la composante **A** (Autonomie) du MSC — et non lorsque la précision seule est élevée. Un apprenant dont la composante A progresse rapidement peut demander à tout moment une réduction immédiate du guidage sur un concept donné. Lorsqu'un guidage fourni génère de la résistance comportementale (ignorance systématique des aides, accélération des réponses malgré les indices), le système traite ce signal comme un indicateur possible de **surqualification** (effet d'inversion de l'expertise, Kalyuga) et propose une réduction proactive du guidage. La charge extrinsèque engendrée par un guidage superflu est prioritairement réduite avant d'augmenter la difficulté intrinsèque.

Le design vise à favoriser activement la **formation de schémas** (charge germinale) via des activités qui demandent à l'apprenant de générer, organiser ou expliquer — et pas seulement de répondre. Les missions mobilisant l'auto-explication, la cartographie conceptuelle, l'élaboration de liens entre notions ou l'enseignement fictif (*feigned teaching*) sont distinguées des missions de rappel actif pur dans le graphe de design. La réduction de la charge extrinsèque est une condition nécessaire mais non suffisante : un design efficace favorise simultanément la schématisation active.

**Les décisions adaptatives du moteur en phase d'usage reposent exclusivement sur des règles déterministes** (conditions sur les composantes du MSC, l'état apprenant composite et les paramètres du référentiel) et des **modèles statistiques légers exécutables localement** (BKT, modèles d'oubli paramétriques, régressions simples sur fenêtres glissantes). Toute règle d'inférence comportement → état apprenant doit être spécifiable comme condition booléenne ou calcul sur des métriques comportementales discrètes documentées dans le référentiel. Si une inférence ne peut pas être formalisée ainsi, elle est exclue du moteur et documentée comme candidat à un patch IA occasionnel (P12).

---

### Principe 3 — Temporalité et mémoire comme mécanismes centraux

La dynamique du jeu intègre explicitement la courbe de l'oubli : chaque concept possède un niveau de stabilité mémorielle qui évolue dans le temps. La répétition espacée et le rappel actif sont intégrés au cœur du gameplay (retours planifiés, anomalies, quêtes de réactivation), et non ajoutés comme un module annexe. L'usage des difficultés dites "désirables" est calibré : une difficulté n'est légitime que si elle augmente la consolidation ou le transfert sans dépasser durablement les capacités de traitement et d'autorégulation de l'étudiant. Lorsqu'une difficulté cesse d'être productive, le système revient provisoirement à la démonstration, au guidage et aux exemples travaillés avant de réaugmenter l'exigence.

La planification temporelle des révisions repose sur un **algorithme d'espacement local explicitement choisi**, documenté en DA-4 du Référentiel de defaults. Cet algorithme est déterministe, exécutable localement sans dépendance à un service externe, et paramétré par les composantes P et R du MSC. Le moteur autonome ne dépend jamais d'un calcul de déclin mémoriel réalisé côté serveur. Un patch peut ajuster les paramètres de l'algorithme (intervalles, facteur de facilité) mais ne se substitue pas à l'algorithme lui-même. La composante R du MSC sert de garde-fou : un concept non encore validé sur la composante R ne peut pas être déclaré maîtrisé, indépendamment de la valeur de P.

La planification combine de manière explicite des phases de **découverte**, des blocs de **rappel actif espacés**, et des sessions **interleavées** où anciens et nouveaux contenus sont travaillés conjointement. L'**espacement** et le **rappel actif** sont prioritaires et constituent le cœur mécanique du moteur. L'**interleaving** est introduit comme mécanisme conditionnel de discrimination et de transfert — non comme principe universel — et est activé lorsque la stabilité minimale du contenu est atteinte.

L'**interleaving** est appliqué en priorité sous sa forme de **variation de types de problèmes** (interleaving de catégories), dont l'effet sur la discrimination et le transfert est le plus robuste empiriquement. L'interleaving de contenus distincts est introduit plus progressivement, après une première phase de bloc homogène sur chaque contenu nouveau. La bascule vers l'interleaving de contenus est conditionnée à l'atteinte simultanée des composantes **P** (Précision) et **A** (Autonomie) du MSC sur chaque contenu concerné — et non de R, car l'interleaving lui-même constitue un test de R en conditions réelles.

L'interleaving par catégories est soumis à une contrainte de **couverture équilibrée** : lors de chaque cycle d'interleaving, le système veille à ce qu'aucun item d'une catégorie ne soit systématiquement moins pratiqué que les autres items de cette même catégorie. Un déséquilibre de couverture documenté déclenche une rééquilibration prioritaire. Ce garde-fou prévient l'effet d'interférence du rappel actif (*retrieval-induced forgetting*, Anderson et al.) par lequel la pratique intensive de certains items peut inhiber le rappel des items connexes moins pratiqués.

L'exposition préalable à l'échec avant instruction directe (*productive failure*, Kapur) n'est pas intégrée au moteur par défaut. Tout univers souhaitant l'intégrer doit le déclarer explicitement dans sa documentation de design et définir les conditions d'apprenant et de concept pour lesquelles elle est activée.

Après une interruption d'activité supérieure au seuil de robustesse temporelle, le système déclenche une **session de reprise** avant de reprendre le parcours planifié : diagnostic léger sur les concepts récemment maîtrisés, bilan de l'état du graphe et recalcul du chemin vers l'échéance. Les concepts dont la composante R du MSC est dégradée repassent en état *en consolidation* avec un parcours de réactivation — et non en état *nouveau*.

---

### Principe 4 — Planification vers une date cible

L'étudiant indique une date d'examen (et éventuellement un niveau visé). Le système planifie et réajuste un chemin d'apprentissage pour maximiser la probabilité d'atteindre un niveau de maîtrise suffisant à cette échéance, en tenant compte du temps disponible et de la difficulté des contenus. La planification intègre des contraintes de charge : chaque session limite le nombre d'éléments nouveaux en interaction et découpe les thèmes intrinsèquement complexes en sous-blocs digestes.

La représentation de l'échéance est conçue pour être **mobilisatrice et non anxiogène** : le système présente la progression accomplie et le chemin restant de manière équilibrée, sans surexposer la distance à l'objectif. La planification n'est pas imposée de manière rigide : le système propose un chemin recommandé mais laisse des marges de choix (ordre de certains modules, types de missions) afin de soutenir le besoin d'autonomie et d'entraîner la capacité de planification de l'étudiant. Ce chemin combine de manière explicite des phases de **découverte**, des blocs de **rappel actif espacés**, et des sessions **interleavées** où anciens et nouveaux contenus sont travaillés conjointement.

---

### Principe 5 — Hyper-personnalisation du parcours

Le parcours n'est pas uniforme. La difficulté, le rythme d'introduction de nouveaux concepts, le choix des missions et la répartition entre découverte, rappel et entraînement "type annale" sont adaptés en continu aux performances, au profil et aux objectifs de l'étudiant. Cette personnalisation vise explicitement à maintenir la charge cognitive dans une zone gérable (ni sous-stimulation, ni surcharge) et à réduire la charge extrinsèque inutile.

La personnalisation est pilotée par un **modèle d'état apprenant composite**, défini par deux axes orthogonaux :

- **Axe 1 — Calibration** (compétence perçue vs réelle) : *bien calibré* (auto-efficacité ≈ performance), *surestimateur* (auto-efficacité > performance), *sous-estimateur* (auto-efficacité < performance). Cet axe est initialisé par le calibrage métacognitif (P0) et mis à jour en continu. Il est inféré à partir de l'écart mesurable entre prédictions déclarées et performances réelles — signal déterministe, précis, ne requérant aucun modèle probabiliste complexe.

- **Axe 2 — Régime d'activation** : *régime productif* (engagement soutenu, performance stable), *régime de détresse* (signaux de surcharge ou d'anxiété), *régime de sous-défi* (signaux de désengagement ou d'ennui). Cet axe **n'est pas un diagnostic psychologique** : il est estimé par un ensemble de **règles déterministes appliquées à des proxys comportementaux mesurables localement**, documentés pour chaque univers en phase Analyse. Les proxys de référence sont : taux d'erreur sur fenêtre glissante de N tentatives, ratio d'abandon intra-mission vs inter-mission, fréquence des demandes d'aide, temps de réponse relatif à la médiane personnelle, et auto-déclaration simplifiée en fin de session. Les seuils opérationnels de ces proxys sont définis dans le Référentiel. En l'absence de validation empirique des règles d'inférence pour un univers donné, le moteur opère avec une **version dégradée robuste à trois régimes** (détresse / neutre / sous-défi), définie dans le Référentiel. La version complète à neuf états est une cible de couverture conditionnée à la validation empirique des règles d'inférence sur données terrain.

Ces deux axes génèrent une matrice d'états, chacun associé à une politique adaptative distincte (difficulté, type de tâche, feedback, message). Ce modèle composite ne définit pas de hiérarchie fixe entre signaux. Un apprenant en régime *productif* n'est pas interrompu par des ajustements adaptatifs même si des signaux secondaires déclenchent des alertes. Lorsque plusieurs interprétations d'un même signal restent plausibles, le moteur **privilégie la réponse la moins intrusive ou sollicite un auto-rapport bref** — il n'agit pas sur la base d'une inférence ambiguë seule.

**Validité inférentielle** : toute règle d'inférence comportement → état apprenant est une hypothèse à valider empiriquement, et non une connaissance établie. La phase Analyse documente les signaux comportementaux retenus, les seuils associés, et le statut de validation de chaque règle (validée empiriquement / supposée / à valider en pilote). Un état inféré avec une confiance insuffisante ne déclenche que des adaptations conservatrices et réversibles. Aucune adaptation à fort impact sur la difficulté, le guidage ou le parcours n'est autorisée en dessous d'un niveau de confiance minimal défini dans le Référentiel.

**Équité algorithmique** : les profils d'apprenants surveillés pour détecter des écarts systématiques de recommandations sont définis *a priori* dans la documentation de chaque univers. Pour tout attribut protégé pertinent dans le contexte d'usage, les métriques d'équité retenues sont documentées et comparées entre groupes. Un écart systématique supérieur au seuil défini déclenche une révision du modèle adaptatif — et pas seulement un signalement.

L'adaptation reste **ouverte** : le système recommande un niveau de difficulté "sûr" mais permet à l'étudiant de choisir des défis plus ambitieux. Aucun plafond de difficulté n'est imposé de manière définitive : les protections passent par le scaffolding (indices, décomposition) et des messages d'avertissement, pas par le blocage de contenus.

La personnalisation intègre la **qualité motivationnelle de l'engagement** comme dimension distincte de la quantité d'usage : un engagement soutenu par motivation intrinsèque (sessions volontaires prolongées, retours spontanés après complétion) est distingué d'un engagement entretenu par des mécaniques de récompense extrinsèque. Cette distinction est opérationnalisée par des signaux comportementaux observables (abandons, sessions volontaires, temps actif vs passif) et constitue une estimation de profil comportemental — non une lecture directe d'un état motivationnel profond. Elle ne peut justifier que des ajustements doux, jamais une fermeture d'options ou une interprétation psychologique forte.

---

### Principe 6 — Transition progressive vers la "feuille blanche"

Le jeu propose plusieurs modes qui rapprochent progressivement l'expérience ludique du format réel de l'examen (problèmes longs, réponses libres, usage de papier/whiteboard). L'objectif est que les compétences développées dans le jeu se transfèrent sans rupture au contexte d'évaluation (annales, copie papier, épreuve en conditions réelles), en augmentant progressivement la complexité et en réduisant les aides pour ne pas provoquer de surcharge brutale.

Le transfert visé est prioritairement un **transfert proche** vers les conditions d'évaluation réelles. Cependant, une partie des missions d'intégration propose des contextes applicatifs légèrement décalés du format d'examen, afin de tester la robustesse de la compréhension au-delà de la simple familiarité au format. Les modes "simulation d'examen" doivent être ressentis comme des défis atteignables, avec des critères de réussite clairs, pour renforcer le sentiment de compétence. La progression vers les modes sans aide correspond à la montée de la composante **A** (Autonomie) du MSC.

---

### Principe 7 — Adaptation à l'environnement d'usage

Le système s'adapte aux contraintes contextuelles de l'étudiant (transport, bureau, bibliothèque, temps court/long). Différents modes (micro-sessions de rappel, entraînements longs, simulations d'examen) sont proposés, tout en restant alignés sur la même trajectoire globale d'apprentissage. Les modes courts privilégient des tâches à faible charge (peu d'éléments en interaction), tandis que les modes longs peuvent accueillir des problèmes plus complexes avec un guidage adéquat. Lorsque c'est pertinent, certains modes peuvent encourager l'usage de supports physiques (papier, whiteboard) pour préparer la transition vers la feuille blanche.

Le système intègre un modèle de **fatigue cognitive intra-session** : les missions impliquant une forte charge intrinsèque (boss, problèmes multi-étapes, tâches de niveau Bloom *analyser* ou supérieur) sont positionnées en début ou milieu de session. Le seuil de bascule vers des formats à faible charge est défini dans le Référentiel (P7-1) et piloté par un **proxy de charge pondéré par type de tâche** (DA-2) : chaque type de tâche est annoté d'un poids de charge intrinsèque estimée dans le graphe de design, et le budget cognitif consommé en session est calculé comme somme pondérée des tâches complétées. Le proxy temporel reste le garde-fou de dernier ressort. Ce seuil est signalé à l'étudiant de manière non anxiogène.

Le système reconnaît et préserve la valeur des **sessions de travail continu et soutenu**, nécessaires à la formation de schémas complexes que la micro-fragmentation seule ne peut produire. La flexibilité contextuelle ne doit pas se faire au détriment de l'accès aux formats longs : les modes de session profonde sont protégés contre la surfragmentation et proposés activement lorsque l'état apprenant et le type de contenu le justifient.

---

### Principe 8 — Gamification éthique centrée sur l'effort cognitif

Les mécaniques d'engagement (récompenses, progression, défis) servent en priorité l'effort intellectuel et la maîtrise des compétences, et non la simple rétention d'attention. Un mécanisme d'engagement qui améliore la persistance à court terme mais dégrade la qualité du traitement cognitif, l'autonomie perçue ou la compréhension à long terme est contraire à la constitution. Les récompenses extrinsèques sont utilisées préférentiellement en phase d'amorçage et progressivement retirées au profit du sentiment de compétence et de progrès intrinsèque, afin de soutenir l'intériorisation de la motivation (SDT : régulation identifiée puis intégrée).

Les éléments visuels et interactifs sont soumis à deux régimes distincts selon leur nature :

- **(a) Éléments multimédia pédagogiques** (contenus, explications, feedbacks) : principe de cohérence de Mayer strict — seuls les éléments qui contribuent directement à la compréhension sont inclus, la redondance entre modalités est évitée, et la charge extrinsèque est minimisée.

- **(b) Éléments de gamification** (animations de récompense, badges, effets visuels) : **test de non-nuisance** — l'élément est acceptable s'il ne dégrade ni la motivation intrinsèque (SDT) ni l'effort cognitif productif. Le critère n'est pas la redondance Mayer mais l'absence d'effet négatif mesurable sur l'apprentissage ou l'autonomie. Tant que ce test n'a pas été vérifié en phase Évaluation, l'élément est en **période probatoire** et son déploiement à large échelle est suspendu.

À l'issue de toute mission majeure (boss, simulation d'examen, premier passage d'un concept en état MSC complet), le système propose un moment structuré de **clôture motivationnelle** : restitution synthétique de ce qui a été accompli, comparaison avec le niveau de départ, et message ancré sur la compétence acquise plutôt que sur la récompense. Cette clôture cible la consolidation de la valeur perçue de l'effort (ARCS — Satisfaction, SDT — compétence) et est distincte du feedback pédagogique (P10).

Les récompenses sont reliées de façon significative au contenu appris, et les systèmes de points/bonus évitent de nuire à la motivation intrinsèque.

---

### Principe 9 — Développement de la métacognition, de l'auto-régulation et du lien social

Le jeu aide l'étudiant à apprendre à apprendre : calibrer sa confiance, planifier, monitorer et évaluer son propre apprentissage. Il met en regard perception de maîtrise et données réelles, explicite les raisons pédagogiques des mécaniques (rappel, espacement, interleaving) et propose des moments de réflexion sur les stratégies utilisées. Les activités sont structurées en trois temps :

- **Avant la tâche** : clarification du but, éventuellement choix entre plusieurs priorités ou types de missions, et brève anticipation de la difficulté (forethought). La clarification du but intègre un garde-fou sur la **représentation de la tâche** : le système vérifie, par une formulation explicite de l'objectif et un bref écho de compréhension attendu, que l'apprenant s'est fixé le même but que celui prévu par le design. Un étudiant qui se fixerait un but de surface (terminer la mission, obtenir la récompense) au lieu d'un but d'apprentissage compromet l'ensemble de la boucle SRL. Ce garde-fou est particulièrement actif lors des premières occurrences de chaque nouveau type de mission.
- **Pendant la tâche** : incitations ponctuelles à estimer sa confiance ou à vérifier sa compréhension (monitoring), sans interrompre excessivement le flux de jeu.
- **Après la tâche** : synthèse des erreurs, comparaison entre confiance déclarée et performance réelle, invitation à identifier ce qui a le mieux aidé ou ce qui sera changé la prochaine fois (self-reflection). Certains prompts de réflexion encouragent explicitement l'**élaboration** (faire des liens avec d'autres notions, trouver des exemples) et l'usage de **double codage** (verbal + visuel) lorsque les deux représentations sont complémentaires et non redondantes.

Les invitations métacognitives **varient en format** (question ouverte, choix entre options, prédiction chiffrée, complétion de phrase) et obéissent à un **principe de frugalité** : elles ne sont pas systématiques à chaque micro-tâche, sont concentrées aux moments de transition et sur les tâches à enjeu, et évitent d'engendrer une hausse de charge extrinsèque ou des réponses automatiques sans engagement réel.

L'**intensité des prompts métacognitifs est elle-même scaffoldée** : pour les apprenants novices ou en situation de forte charge cognitive, les invitations à la réflexion sont plus guidées et moins fréquentes, puis progressivement retirées à mesure que l'étudiant internalise ces routines. Les stratégies métacognitives font l'objet d'une **modélisation explicite** avant d'être demandées de manière autonome.

Le système distingue un apprenant qui **internalise** les routines métacognitives (réduction planifiée de la fréquence des prompts au fil des sessions) d'un apprenant qui les **évite** (réponses automatiques sans engagement réel, temps inférieur au seuil sur les écrans de réflexion, taux d'erreur post-prompt inchangé). L'évitement métacognitif est traité comme un signal d'alarme équivalent à un signal de surcharge : il déclenche un retour à des prompts plus guidés et plus courts, et non une suppression des prompts. Un apprenant en évitement persistant est un candidat à un patch paramétrique (P12).

Le système intègre une **dimension affective opérationnelle** : il adapte sa difficulté et ses messages en réponse aux régimes observables détectés (axe 2, P5). Ces **états affectifs utilisés par le moteur sont des régimes opérationnels de régulation, et non des diagnostics psychologiques** : le système agit sur des signaux tels que *surcharge probable*, *sous-défi probable*, *désengagement probable*, sans prétendre diagnostiquer cliniquement un état émotionnel. Lorsque plusieurs interprétations d'un même signal restent plausibles, le moteur privilégie l'intervention la moins intrusive. L'ennui et la sous-stimulation sont traités comme des signaux d'alarme symétriques à l'anxiété (Pekrun). Ni l'anxiété ni l'ennui ne sont nommés cliniquement dans les messages.

Le système distingue l'**abandon par détresse** (taux d'erreur élevé, signaux de surcharge, abandon précoce) de l'**abandon par désengagement rationnel** face à une tâche perçue comme peu pertinente (performance correcte mais refus répété, accélération sans erreur, signaux de sous-défi sans difficulté excessive). Le premier justifie un ajustement de difficulté ou un retour au guidage ; le second appelle une **re-négociation explicite des objectifs** avec l'apprenant.

La dimension sociale est introduite via une **exposition progressive et réversible** : après un seuil d'usage établi (défini dans le Référentiel), le système propose activement une fonctionnalité sociale concrète et non intrusive, avec option de désactivation simple et permanente. Les missions d'**apprentissage par les pairs** (confrontation d'erreurs, enseignement mutuel, co-résolution) sont distinguées des effets motivationnels du lien social. Cette dimension est optionnelle par univers ; sa présence doit être explicitement justifiée, ou son absence motivée, dans la documentation de design.

---

### Principe 10 — Qualité du feedback et modèle implicite de la compétence

Le feedback généré par le moteur autonome porte en priorité sur le **processus** (stratégies utilisées, erreurs procédurales, pistes de révision) et sur l'**autorégulation** (comment l'étudiant pourrait ajuster son approche), plutôt que sur la personne ou les aptitudes. Les messages de réussite soulignent l'effort, la stratégie et la progression, afin de renforcer une conception malléable de la compétence. Tout feedback évaluatif global ("tu maîtrises ce chapitre") est accompagné d'une indication de son niveau de fiabilité et des conditions dans lesquelles cette inférence a été établie.

Le feedback produit par le moteur autonome en phase d'usage repose sur des **templates paramétriques** — ensemble fini de formats de feedback définis en phase Développement par la chaîne IA de conception, indexés sur le type d'erreur, le niveau Bloom de la tâche et l'état MSC du concept. Ces templates constituent le **régime nominal du moteur**. Tout feedback supposant une contextualisation linguistique fine au-delà du template (explication d'une erreur raisonnée inédite, reformulation personnalisée de la stratégie) dépasse la capacité du moteur autonome et constitue un candidat au régime de patch (P12). Cette contrainte est déclarée en phase Analyse : la richesse et la couverture des templates de feedback sont un livrable obligatoire de la chaîne IA de conception, conditionné à la diversité des types d'erreurs documentés dans le graphe.

---

### Principe 11 — Séparation des couches : conception, moteur autonome, patchs

Learn-it distingue trois couches fonctionnelles aux responsabilités strictement séparées. Aucune de ces couches ne peut être implicitement substituée à une autre dans la formulation des principes ou dans l'implémentation.

**(a) Couche conception** (chaîne IA, hors phase d'usage) : construction du graphe de connaissances, génération des missions et de leurs variantes, paramétrage initial du référentiel, production des assets pédagogiques (missions de conflit cognitif, missions génératives, modélisation métacognitive, templates de feedback). C'est la couche qui exerce l'intelligence générative : elle produit les artefacts paramétriques que le moteur exécutera.

**(b) Couche moteur autonome** (local, en phase d'usage) : toutes les décisions adaptatives session par session, pilotées par des règles déterministes et des modèles statistiques légers sur les données d'état apprenant. Le moteur **ne génère aucun contenu** : il sélectionne, séquence et paramètre des artefacts produits en couche conception. Aucune décision du moteur ne peut dépendre d'un appel réseau en temps réel. Tout ce qui peut être décidé de manière fiable par règles expertes et statistiques légères doit être décidé localement.

**(c) Couche patch** (serveur, occasionnel) : correction documentée des dérives que le moteur autonome ne peut corriger par simple reparamétrage courant. Un patch génère ou révise des artefacts paramétriques (sous-parcours, variantes de missions, ajustements de seuils dans les fourchettes du référentiel, templates de feedback supplémentaires) téléchargeables et intégrés localement. Le patch ne remplace pas le moteur : il met à jour les artefacts que le moteur exécute. Les contraintes des patchs sont définies en P12.

Cette séparation est **inviolable en conception** : tout mécanisme qui suppose de générer du contenu en phase d'usage appartient à la couche patch, pas au moteur autonome. Tout mécanisme du moteur qui supposerait un appel réseau continu signale une dépendance IA implicite à corriger.

---

### Principe 12 — Patchs paramétriques : déclencheurs, périmètre et garde-fous

Un patch est déclenché lorsqu'une **métrique de dérive documentée** franchit son seuil défini dans le Référentiel. Le moteur surveille en continu ces métriques et reste en contrôle entre les patchs : les patchs sont occasionnels, non continus. Les déclencheurs de référence sont ceux définis dans le Référentiel (ADDIE-1, ADDIE-2 et métriques de dérive complémentaires).

**Périmètre autorisé d'un patch** : ajustement de paramètres du Référentiel dans les fourchettes autorisées, ajout ou révision de sous-parcours, ajout de variantes de missions ou de templates de feedback, révision des poids du graphe local sur une zone problématique, ajustement du mapping entre régimes observables et politiques adaptatives. Un patch peut aussi activer la version étendue à neuf états de la matrice apprenant (P5) si les données terrain le justifient.

**Périmètre interdit d'un patch** : un patch ne peut pas redéfinir les composantes ou seuils du MSC au-delà des fourchettes constitutionnelles, modifier la philosophie d'adaptation (P5, P8), introduire un nouveau mécanisme d'inférence psychologique sans statut probatoire, ni élargir silencieusement le périmètre des inférences sur l'apprenant. Un patch ne peut pas introduire un principe nouveau : seule une délibération constitutionnelle le peut.

**Attributs obligatoires de tout patch** : le patch est *paramétrique* (jamais conversationnel continu), *traçable* (justifié par un signal explicite et versionné), *borné* (périmètre des paramètres modifiés déclaré), *réversible* (condition de rollback définie si le patch dégrade les métriques cibles), et *transparent* (l'apprenant est informé qu'une mise à jour de son parcours a été générée et peut en consulter les raisons principales sur demande).

La **conformité constitutionnelle du patch est vérifiée** avant déploiement : un patch contrevenant à P5 (équité), P8 (non-nuisance gamification) ou P9 (autonomie apprenant) est rejeté. Cette vérification est réalisée par un ensemble de règles de validation documentées dans le Référentiel.

---

## Cycle de design pédagogique

Le design des univers d'apprentissage dans Learn-it suit un cycle explicite, inspiré des modèles d'ingénierie pédagogique (notamment ADDIE) et des First Principles of Instruction de Merrill :

### 1. Analyse

Identifier les objectifs d'apprentissage et les compétences d'examen associées, extraire les concepts et relations clés à partir des supports (cours, exercices, annales) et construire le graphe de connaissances correspondant. Pour chaque objectif, les verbes d'action sont positionnés dans la **taxonomie de Bloom révisée** (mémoriser, comprendre, appliquer, analyser, évaluer, créer).

L'**ICC** est déclaré explicitement à cette phase et conditionne la stratégie de construction du graphe (voir P1). L'**alignement constructif** (Biggs) est vérifié : cohérence entre objectifs, activités et formes d'évaluation.

La phase Analyse définit également : (a) les **signaux comportementaux** retenus comme proxys d'états apprenants et leur statut de validation empirique (validée / supposée / à valider en pilote) ; (b) les **profils d'apprenants** surveillés pour l'équité algorithmique et les métriques d'équité associées ; (c) les concepts à **flag misconception** dans le graphe, le cas échéant ; (d) la déclaration de l'objectif de **transfert lointain** ou du statut *à portée examen uniquement* ; (e) la décision d'inclure ou d'exclure la *productive failure* et, si incluse, les conditions d'activation.

**Validation du graphe produit par la chaîne IA de conception** : avant tout déploiement, le graphe fait l'objet d'un **protocole de validation de qualité** couvrant au minimum : (i) couverture des objectifs Bloom déclarés (chaque objectif est représenté par au moins un nœud au niveau cognitif cible) ; (ii) cohérence des arêtes de prérequis (absence de cycles, arêtes justifiées dans la documentation) ; (iii) présence des flags misconception documentés dans le corpus disciplinaire de référence ; (iv) couverture des types de missions requis (conflit cognitif, missions génératives, templates de feedback) pour chaque nœud. Tout graphe ne satisfaisant pas ces critères minimaux est marqué comme **graphe en attente de validation** et déployé uniquement en mode pilote restreint. La constitution ne délègue pas la responsabilité de la qualité pédagogique à la chaîne IA : elle en fait un critère de gouvernance explicite du cycle ADDIE.

Tout univers d'apprentissage doit expliciter les compétences visées, leur position dans une progression de complexité, les tâches authentiques de référence, les niveaux cognitifs sollicités, les formes de guidage prévues, les preuves attendues de maîtrise (référencées au MSC) et les conditions de révision après usage.

### 2. Design

Pour chaque objectif et partie du graphe, définir des problèmes authentiques et une trajectoire d'apprentissage de type **activation → démonstration → application → intégration**, en les traduisant en types de missions, puzzles, cartes et "boss" alignés avec les 12 principes. Cette trajectoire constitue une **contrainte systématique de design**, et non une simple inspiration : chaque univers doit couvrir ces quatre phases pour chaque objectif cible.

La phase Design précise également : (a) les missions de type **conflit cognitif** pour chaque concept flaggé *misconception* ; (b) les missions de type **génératif** (auto-explication, cartographie, enseignement fictif) distinctes des missions de rappel actif pur ; (c) la décision d'inclure ou d'exclure la *productive failure* et, si incluse, les conditions d'activation ; (d) les **templates de feedback** couvrant les types d'erreurs documentés par nœud et par niveau Bloom.

### 3. Développement

Produire les contenus jouables (énoncés, interfaces, feedbacks, paramètres adaptatifs) en respectant les contraintes de charge cognitive, de motivation, de métacognition, de stratégies fondées sur la preuve et d'éthique de la personnalisation.

### 4. Implémentation

Déployer l'univers d'apprentissage auprès des étudiants, configurer les paramètres d'adaptation et les liens avec l'environnement réel (calendrier d'examen, modes d'usage). Les éléments de gamification non encore soumis au test de non-nuisance sont déployés en **mode probatoire** : leur collecte de données est activée dès cette phase pour permettre la vérification lors de la phase Évaluation.

### 5. Évaluation et révision

Recueillir des données sur la maîtrise réelle des objectifs (performances aux missions clés, simulations d'examen, résultats d'évaluation externe) et sur l'expérience des utilisateurs, puis ajuster le graphe, les missions et les paramètres adaptatifs.

Le déclencheur de révision du modèle d'inférence est défini en termes d'**écarts longitudinaux intra-individuels** :

- **Écart ponctuel** : maîtrise estimée par le système supérieure à la performance réelle lors d'une simulation d'examen → signalement immédiat et ajustement du modèle pour les concepts concernés.
- **Biais systématique** : le système surestime ou sous-estime de manière cohérente sur plusieurs évaluations consécutives → révision du modèle d'inférence pour ce concept ou ce type de tâche.
- **Dérive hors-jeu** : performance en simulation stable mais résultats réels systématiquement inférieurs → revoir le paramètre de transfert du graphe (composante **T** du MSC).

La phase Évaluation inclut systématiquement : (a) la **vérification du test de non-nuisance** pour tout élément de gamification en période probatoire ; (b) la **vérification des métriques d'équité** définies en phase Analyse, avec déclenchement d'une révision si les écarts dépassent les seuils définis ; (c) la **confrontation des règles d'inférence comportement → état** aux données observées, avec mise à jour du statut de validation dans la documentation ; (d) la **vérification d'efficience** : le temps médian d'apprentissage jusqu'au MSC par nœud est comparé à la valeur cible documentée en phase Analyse — un écart supérieur au double de cette valeur déclenche une révision structurelle du graphe distincte de la révision paramétrique.

Ce cycle est itératif : les univers peuvent être révisés régulièrement pour rester cohérents avec la constitution et les retours du terrain.

---

## Cadres théoriques de référence

Les principes ci-dessus ont été confrontés, critiqués et ajustés à la lumière des cadres théoriques suivants :

- **Cognition et charge mentale** : Cognitive Load Theory (Sweller, van Merriënboer) — charge intrinsèque, extrinsèque et germinale ; effet d'inversion de l'expertise (Kalyuga) ; Desirable Difficulties (Bjork) ; *retrieval-induced forgetting* (Anderson et al.) ; théorie de l'apprentissage multimédia (Mayer — 12 principes dont cohérence, segmentation, redondance) ; *productive failure* (Kapur).

- **Motivation et engagement** : Self-Determination Theory (Deci & Ryan), modèle ARCS (Keller), théories de la motivation de la réussite et de la valeur-attente (Eccles & Wigfield).

- **Métacognition et auto-régulation** : modèles de Self-Regulated Learning (Zimmerman ; Winne & Hadwin — task definition, boucles COPES), recommandations EEF sur la métacognition, self-efficacy (Bandura).

- **Émotions et apprentissage** : Control-Value Theory (Pekrun) — anxiété de test, ennui, enthousiasme comme régulateurs de la cognition et de la motivation.

- **Stratégies d'apprentissage fondées sur la preuve** : rappel actif, répétition espacée, interleaving (catégories et contenus), élaboration, double codage, exemples concrets, worked examples et fading (Sweller, van Merriënboer) ; apprentissage génératif (Fiorella & Mayer) ; elaborative interrogation (Dunlosky et al.).

- **Apprentissage social et constructivisme** : Zone Proximale de Développement (Vygotsky), apprentissage par les pairs, enseignement mutuel.

- **Misconceptions et changement conceptuel** : conflit cognitif, réfutation explicite (Posner et al., Chi).

- **Personnalisation et systèmes adaptatifs** : cadres pour adaptive learning et systèmes d'apprentissage pilotés par l'IA, modèles de l'apprenant (BKT, PFA), garde-fous en matière de biais, d'équité et de transparence, mastery learning (Bloom).

- **Modèles d'ingénierie pédagogique** : ADDIE, Merrill's First Principles, taxonomie de Bloom révisée, alignement constructif (Biggs), assessment for learning (Black & Wiliam).

---

## Glossaire

### Mastery Score Composite (MSC)

La maîtrise d'un concept est définie par un vecteur à quatre composantes, toutes requises simultanément pour déclarer une **maîtrise robuste**. Le MSC est toujours instancié à un niveau Bloom cible — il n'existe pas de maîtrise absolue d'un concept, seulement une maîtrise à un niveau cognitif donné.

```
MSC(concept, niveau Bloom) = (P, R, A, T)
```

| Composante | Définition |
|---|---|
| **P — Précision** | Taux de réussite sur les N dernières occurrences au niveau Bloom cible |
| **R — Robustesse temporelle** | Au moins une réussite après un délai ≥ D sans stimulation du concept |
| **A — Autonomie** | Au moins M réussites sans aide ni indice d'aucune sorte |
| **T — Transférabilité** | Voir définition étendue ci-dessous |

Les seuils opérationnels (N, D, M) sont définis dans le Référentiel de defaults.

**Composante T — Transférabilité**

Au moins une réussite sur un format *structurellement différent* de l'entraînement principal (transfert intra-jeu). Pour les univers disposant d'une mesure externe (simulation hors-jeu, devoir rendu, examen intermédiaire), au moins une réussite sur cette mesure externe est requise pour valider le transfert hors-jeu.

En l'absence de mesure externe disponible, la Transférabilité intra-jeu suffit pour déclarer la *maîtrise robuste*, mais une **note de risque T** est inscrite dans le modèle de l'apprenant, signalant que le transfert hors-jeu n'a pas été vérifié. La phase Évaluation doit prévoir systématiquement au moins une mesure externe de transfert.

**États de maîtrise** :

- **Maîtrise provisoire héritée** : état initialisé par le calibrage (P0) pour les concepts confirmés en pré-test. P est présumée ; R et A sont non encore corroborées par des observations en usage. Génère une vérification prioritaire de R et A lors des trois premières sessions. Inférieure à la maîtrise d'entraînement jusqu'à confirmation.
- **Maîtrise d'entraînement** : P + R + A atteints, T non encore atteint. Suffisante pour progresser dans le graphe, insuffisante pour clore définitivement un concept et désactiver les rappels espacés.
- **Maîtrise robuste** : P + R + A + T atteints (T intra-jeu au minimum, T hors-jeu si mesure disponible). Le concept peut être marqué comme consolidé.

**Règles d'exception** :

- **Dégradation post-maîtrise** : une maîtrise déclarée peut être révoquée si l'étudiant échoue sur plusieurs occurrences consécutives après une absence ≥ seuil_R. Le concept repasse en état *en consolidation* avec un parcours de réactivation — et non en état *nouveau*.
- **Niveau Bloom différencié** : un concept peut être maîtrisé au niveau *comprendre* mais pas au niveau *analyser*. Le MSC est toujours associé à un niveau Bloom cible.

**Liens avec les principes** :

- P0 (calibrage) : maîtrise provisoire héritée pour les concepts confirmés en pré-test, avec vérification prioritaire R et A.
- P2 (fading) : déclenché par la progression de la composante A.
- P3 (interleaving) : bascule conditionnée à P + A atteints.
- P6 (feuille blanche) : progression vers les modes sans aide = montée de A.
- ADDIE (révision) : l'écart longitudinal à détecter porte prioritairement sur T.

---

### Indice de Confiance du Corpus (ICC)

Métadonnée obligatoire déclarée en phase Analyse, calculée à partir du nombre d'annales disponibles, de leur ancienneté et de leur diversité de formats. Conditionne la stratégie de construction du graphe (voir P1). Valeurs : **fort** / **partiel** / **absent**.

---

### État apprenant composite

Modèle à deux axes (calibration × régime d'activation) générant une matrice d'états avec politiques adaptatives associées (voir P5). L'axe calibration est inféré à partir de l'écart prédiction/performance (signal déterministe). L'axe régime d'activation est estimé par proxys comportementaux explicites. Initialisé par le calibrage métacognitif (P0). La liste des états implémentés en priorité et la cible de couverture complète sont définies dans le Référentiel de defaults.

---

### Flag Misconception

Attribut d'un nœud du graphe de connaissances signalant qu'une représentation erronée fermement ancrée est documentée pour ce concept dans le corpus disciplinaire de référence. Déclenche l'obligation d'une mission de type *conflit cognitif* en phase Design. Le périmètre d'obligation par univers est défini dans le Référentiel de defaults.

---

### Période probatoire (gamification)

Statut d'un élément de gamification déployé en Implémentation mais dont le test de non-nuisance n'a pas encore été vérifié en phase Évaluation. En période probatoire, l'élément est actif mais sa collecte de données est obligatoire et son déploiement à large échelle est suspendu jusqu'à vérification.

---

*Constitution v1.3 — intègre les recommandations des analyses critiques de la v1.2. Contenu conceptuel des principes non modifiés inchangé par rapport à la v1.2. À lire conjointement avec le Référentiel de defaults pédagogiques v0.2.*
