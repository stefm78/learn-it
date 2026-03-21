# Constitution conceptuelle – Learn-it (v1.4)

> **Note de version** : La v1.4 intègre deux chantiers d'approfondissement issus de l'analyse critique de la v1.3. **(1) Auto-rapport de l'état psychologique** : les proxys comportementaux de P5 sont nécessaires mais épistémologiquement insuffisants — ils capturent du comportement, pas de l'expérience. La v1.4 introduit un système d'auto-rapport à trois niveaux intégré à P9, qui devient la source de signal d'autorité sur les états affectifs et les régimes d'activation. P5 est amendé pour refléter la hiérarchie de confiance et pour distinguer confusion productive, frustration et anxiété — trois états aux proxys comportementaux similaires mais aux interventions opposées. **(2) Intégrité du modèle apprenant** : l'hyper-personnalisation suppose que toutes les sessions sont conduites par le bon apprenant. Cette hypothèse n'est ni triviale ni automatiquement vraie. La v1.4 introduit un nouveau Principe 13 posant l'architecture d'intégrité en couches : multi-profil (réponse primaire aux usages légitimes multi-personne), Score d'Intégrité de Session (réponse statistique à la substitution), modes explicites (Invité et Évaluation Externe), et vérification déclarative périodique. Ces mécanismes protègent le modèle sans surveillance comportementale ni présomption de mauvaise foi. Le contenu des principes non modifiés est inchangé par rapport à la v1.3.

> **Principe de gouvernance des deux documents** : La constitution est modifiée par délibération explicite lorsqu'un principe s'avère inadapté ou incomplet. Le Référentiel est révisé librement à partir des données terrain, sans toucher à la constitution. Un élément appartient à la constitution s'il répond à la question *"quoi et pourquoi"*. Il appartient au Référentiel s'il répond à la question *"combien et comment"*.

---

## Principes fondamentaux

### Principe 0 — Calibrage initial de l'apprenant

Avant l'entrée dans le parcours personnalisé, le système conduit une **phase de calibrage initiale** poursuivant deux objectifs distincts et complémentaires.

**(a) Calibrage épistémique** : estimer la position de l'apprenant dans le graphe de connaissances via un diagnostic adaptatif court. Le résultat initialise l'état du graphe pour cet apprenant, en distinguant les prérequis confirmés maîtrisés, les concepts en doute et les lacunes probables. En l'absence de calibrage épistémique, le système part d'une **hypothèse conservatrice** (position initiale basse) et délègue à l'apprenant la possibilité de débloquer manuellement des nœuds du graphe qu'il estime déjà maîtrisés.

Pour les concepts déclarés déjà maîtrisés lors du calibrage et confirmés par le pré-test, le MSC est initialisé à l'état **maîtrise provisoire héritée** — état distinct de la *maîtrise d'entraînement* — dans lequel les composantes P, R et A sont *présumées* mais non encore corroborées par des observations en usage. Un pré-test évalue la performance actuelle ; il ne valide pas la robustesse temporelle (composante R) ni l'autonomie sans aide répétée (composante A). La maîtrise provisoire héritée génère automatiquement une vérification prioritaire de R et A lors des trois premières sessions : si ces composantes sont confirmées, le concept passe en *maîtrise d'entraînement* ; sinon, il repasse en état *en consolidation* avec un parcours de réactivation. La composante T n'est pas validée dans cet état initial, ce qui génère une mission de transfert prioritaire.

**(b) Calibrage métacognitif** : estimer le profil de calibration de l'apprenant (auto-efficacité perçue vs performance réelle) en intégrant une **prédiction de performance** dans le pré-test lui-même. La comparaison entre prédictions et résultats réels initialise la composante Calibration de l'état apprenant composite (P5). Ce mécanisme constitue la première instance explicite de la boucle métacognitive avant/pendant/après (P9).

La phase de calibrage est conçue pour être **courte, engageante et immédiatement utile** à l'apprenant : le système lui restitue une première cartographie visuelle de ses connaissances dès la fin du calibrage. Elle ne repose sur aucune typologie de "styles d'apprentissage" empiriquement invalidée (VARK, etc.). Le calibrage est **révisable** : l'apprenant peut contester une inférence initiale et le système permet une correction facile des états mal estimés lors des premières sessions. Toutes les inférences issues du calibrage initial sont traitées avec une **confiance réduite** et renforcées ou révisées en priorité par les données comportementales des premières sessions — elles ne constituent jamais un état figé.

---

### Principe 1 — Primat de la maîtrise des compétences d'examen

Le jeu est conçu d'abord pour garantir la maîtrise des compétences réellement évaluées (telles qu'elles apparaissent dans les objectifs du cours et les annales), puis pour être engageant. Les activités de jeu doivent pouvoir se mapper à des tâches d'examen (résolution de problèmes, modélisation, explication, interprétation de données). L'introduction des tâches complexes de type annale se fait de manière progressive (scaffolding), en contrôlant la charge cognitive : on commence par des versions simplifiées avant de monter vers des sujets multi-étapes. Chaque mission importante précise explicitement sa pertinence par rapport à l'examen (composante Relevance du modèle ARCS) et s'appuie, autant que possible, sur des **exemples concrets** avant de généraliser vers des formes plus abstraites.

Les objectifs d'apprentissage associés à chaque mission sont caractérisés par leur **niveau cognitif cible** selon la taxonomie révisée de Bloom (mémoriser, comprendre, appliquer, analyser, évaluer, créer). La progression de l'étudiant vise une montée en niveaux cognitifs, et non la seule consolidation des niveaux bas.

Le graphe de connaissances est construit à partir des supports de cours et des annales, mais aussi confronté à la structure disciplinaire du domaine, afin d'éviter un rétrécissement du curriculum aux seuls formats d'évaluation. L'**Indice de Confiance du Corpus (ICC)**, calculé à partir du nombre d'annales disponibles, de leur ancienneté et de leur diversité de formats, est déclaré explicitement en phase Analyse et conditionne la stratégie de construction du graphe :

- **ICC fort** (annales complètes) : graphe calibré normalement sur la fréquence des concepts en annales.
- **ICC partiel** (annales incomplètes) : les fréquences sont pondérées et complétées par la structure disciplinaire de référence.
- **ICC absent** (aucune annale fournie) : fallback sur taxonomie Bloom et corpus disciplinaire de référence.

Dans tous les cas, tout concept présent dans le corpus disciplinaire de référence mais absent ou rare dans les annales est maintenu dans le graphe avec un niveau cognitif Bloom minimum et un coefficient de pondération réduit — il n'est **jamais supprimé**. Une distinction explicite est maintenue entre *concepts fréquents en annales* et *concepts fondamentaux du domaine*.

Le graphe de connaissances distingue les **lacunes** (compétence non encore développée) des **misconceptions** (représentation incorrecte fermement ancrée). Les missions ciblant un concept à misconception connue incluent une phase explicite de **conflit cognitif** avant de proposer la représentation correcte. Le simple rappel actif ou le scaffolding ne constituent pas des réponses suffisantes à une misconception identifiée.

Chaque univers vérifie l'**alignement constructif** (Biggs) dès la phase Analyse. Tout univers dont les objectifs dépassent la seule réussite à l'examen déclare explicitement un **objectif de transfert lointain** en phase Analyse. Toute allégation de transfert au-delà du jeu ou du format d'entraînement doit être adossée à une mesure externe dédiée.

---

### Principe 2 — Moteur générique basé sur un graphe de connaissances

Le cœur du système est un moteur générique, indépendant du domaine, qui manipule des concepts, des relations de prérequis et des types de tâches. Chaque cours ou document est représenté comme un graphe orienté de connaissances, sur lequel le jeu instancie des cartes, puzzles, missions et "boss". Le graphe sert explicitement à gérer la charge intrinsèque : tant que certains prérequis ne sont pas maîtrisés, le système évite de proposer des puzzles qui combinent simultanément un trop grand nombre de concepts non consolidés.

Les décisions adaptatives doivent rester **explicables** : le système communique à l'étudiant, sur demande, les raisons principales de chaque recommandation de parcours. Cette explicabilité est fournie *sur demande explicite* et, de manière non sollicitée, *uniquement aux moments de transition entre sessions*.

Le **fading** des aides est déclenché par la progression de la composante **A** du MSC. Lorsqu'un guidage fourni génère de la résistance comportementale (ignorance systématique des aides, accélération des réponses malgré les indices), le système traite ce signal comme un indicateur possible de **surqualification** (effet d'inversion de l'expertise, Kalyuga) et propose une réduction proactive du guidage.

Le design vise à favoriser activement la **formation de schémas** via des activités génératives (auto-explication, cartographie conceptuelle, élaboration, enseignement fictif), distinguées des missions de rappel actif pur dans le graphe de design.

**Les décisions adaptatives du moteur en phase d'usage reposent exclusivement sur des règles déterministes** et des **modèles statistiques légers exécutables localement**. Toute règle d'inférence comportement → état apprenant doit être spécifiable comme condition booléenne ou calcul sur des métriques documentées dans le référentiel. Si une inférence ne peut pas être formalisée ainsi, elle est exclue du moteur et documentée comme candidat à un patch (P12).

---

### Principe 3 — Temporalité et mémoire comme mécanismes centraux

La dynamique du jeu intègre explicitement la courbe de l'oubli : chaque concept possède un niveau de stabilité mémorielle qui évolue dans le temps. La répétition espacée et le rappel actif sont intégrés au cœur du gameplay, et non ajoutés comme un module annexe.

La planification temporelle des révisions repose sur un **algorithme d'espacement local explicitement choisi**, documenté en DA-4 du Référentiel. Cet algorithme est déterministe, exécutable localement sans dépendance à un service externe, et paramétré par les composantes P et R du MSC. La composante R du MSC sert de garde-fou : un concept non encore validé sur R ne peut pas être déclaré maîtrisé, indépendamment de P.

L'**espacement** et le **rappel actif** sont prioritaires. L'**interleaving** est conditionnel : interleaving de catégories en priorité (effet transfert le plus robuste), interleaving de contenus uniquement après atteinte simultanée de P et A sur chaque contenu — R n'est pas un prérequis à cette bascule, car l'interleaving lui-même constitue un test de R en conditions réelles.

L'interleaving par catégories est soumis à une contrainte de **couverture équilibrée** prévenant le *retrieval-induced forgetting* (Anderson et al.). La *productive failure* (Kapur) n'est pas intégrée par défaut : son inclusion est une décision explicite par univers.

Après une interruption supérieure au seuil de robustesse temporelle, le système déclenche une **session de reprise** diagnostique avant de reprendre le parcours planifié.

---

### Principe 4 — Planification vers une date cible

L'étudiant indique une date d'examen. Le système planifie et réajuste un chemin d'apprentissage pour maximiser la probabilité d'atteindre la maîtrise à cette échéance, en tenant compte du temps disponible et de la difficulté des contenus. La représentation de l'échéance est conçue pour être **mobilisatrice et non anxiogène**. La planification n'est pas rigide : le système laisse des marges de choix afin de soutenir l'autonomie et d'entraîner la capacité de planification de l'étudiant.

---

### Principe 5 — Hyper-personnalisation du parcours

Le parcours est adapté en continu aux performances, au profil et aux objectifs de l'étudiant. La personnalisation vise à maintenir la charge cognitive dans une zone gérable et à réduire la charge extrinsèque inutile.

La personnalisation est pilotée par un **modèle d'état apprenant composite**, défini par deux axes :

- **Axe 1 — Calibration** : *bien calibré* / *surestimateur* / *sous-estimateur*. Inféré de façon déterministe à partir de l'écart mesurable entre prédictions déclarées et performances réelles — signal ne requérant aucun modèle probabiliste complexe.

- **Axe 2 — Régime d'activation** : *productif* / *détresse* / *sous-défi*. Cet axe n'est **pas un diagnostic psychologique**. Il est estimé par une **hiérarchie de sources de signal** ordonnées par fiabilité décroissante, définie dans le Référentiel et détaillée dans P9. Les proxys comportementaux seuls (P5-4 du Référentiel) constituent la source de base, active en permanence. Ils sont complétés et, le cas échéant, corrigés par l'auto-rapport de l'apprenant (P9), qui constitue la source d'autorité sur les états internes.

**Distinction critique — confusion, frustration, anxiété** : la constitution reconnaît explicitement que ces trois états partagent des proxys comportementaux similaires (taux d'erreur élevé, engagement réduit) mais appellent des interventions opposées :
- **Confusion productive** (D'Mello & Graesser) : l'apprenant est en difficulté mais cognitivement engagé, cherche activement ; l'erreur résulte d'une tâche dans la zone proximale de développement. *Intervention : scaffolding, ne pas réduire la difficulté.*
- **Frustration/épuisement** : l'apprenant a cessé d'essayer activement ; les erreurs résultent d'un désengagement. *Intervention : réduction de charge, changement de format.*
- **Anxiété** : l'apprenant cherche de l'aide, la performance est altérée par l'inquiétude plutôt que par l'absence de connaissance. *Intervention : réduction de la difficulté + message de soutien.*

Les proxys comportementaux ne peuvent pas distinguer ces trois états de façon fiable. Seul l'auto-rapport événementiel (Tier 1, P9) le peut. Lorsque les proxys signalent un régime de détresse et qu'aucun auto-rapport n'est disponible pour affiner, le moteur applique une **intervention conservatrice et réversible** (scaffolding léger), sans réduire brutalement la difficulté ni changer de format, jusqu'à obtention d'une donnée auto-déclarée.

**Validité inférentielle** : toute règle d'inférence comportement → état apprenant est une hypothèse à valider empiriquement. La phase Analyse documente les proxys retenus, leurs seuils, et leur statut de validation. Un état inféré avec une confiance insuffisante ne déclenche que des adaptations conservatrices et réversibles.

**Équité algorithmique** : les profils d'apprenants surveillés pour détecter des écarts systématiques de recommandations sont définis *a priori*. Un écart systématique supérieur au seuil défini déclenche une révision du modèle adaptatif — et pas seulement un signalement.

L'adaptation reste **ouverte** : aucun plafond de difficulté n'est imposé définitivement.

La personnalisation intègre la **qualité motivationnelle de l'engagement** comme dimension distincte de la quantité d'usage. Elle constitue une estimation de profil comportemental — non une lecture directe d'un état motivationnel profond — et ne peut justifier que des ajustements doux.

---

### Principe 6 — Transition progressive vers la "feuille blanche"

Le jeu propose plusieurs modes rapprochant progressivement l'expérience du format réel de l'examen. Le transfert visé est prioritairement un **transfert proche** vers les conditions d'évaluation réelles. La progression vers les modes sans aide correspond à la montée de la composante **A** du MSC.

---

### Principe 7 — Adaptation à l'environnement d'usage

Le système s'adapte aux contraintes contextuelles de l'étudiant. Les modes courts privilégient des tâches à faible charge, les modes longs accueillent des problèmes plus complexes avec guidage adéquat.

Le système intègre un modèle de **fatigue cognitive intra-session** piloté par un **proxy de charge pondéré par type de tâche** (DA-2) : budget cognitif de session = somme pondérée des tâches complétées. Le proxy temporel reste le garde-fou de dernier ressort.

Le système préserve la valeur des **sessions de travail continu et soutenu**, nécessaires à la formation de schémas complexes que la micro-fragmentation seule ne peut produire.

---

### Principe 8 — Gamification éthique centrée sur l'effort cognitif

Les mécaniques d'engagement servent en priorité l'effort intellectuel et la maîtrise, et non la rétention d'attention. Les récompenses extrinsèques sont utilisées préférentiellement en phase d'amorçage et progressivement retirées au profit du sentiment de compétence intrinsèque (SDT).

Deux régimes distincts : **(a)** éléments pédagogiques — principe de cohérence Mayer strict ; **(b)** éléments de gamification — test de non-nuisance (absence d'effet négatif mesurable sur l'apprentissage ou l'autonomie). Tout élément non encore vérifié est en **période probatoire**.

À l'issue de toute mission majeure, le système propose un moment structuré de **clôture motivationnelle** : restitution de ce qui a été accompli, comparaison avec le niveau de départ, message ancré sur la compétence acquise (ARCS Satisfaction, SDT compétence).

---

### Principe 9 — Développement de la métacognition, de l'auto-régulation, du lien social et de l'auto-rapport affectif

Le jeu aide l'étudiant à apprendre à apprendre : calibrer sa confiance, planifier, monitorer et évaluer son propre apprentissage. Les activités sont structurées en trois temps (forethought / monitoring / self-reflection selon Zimmerman).

**Boucle SRL :**
- **Avant la tâche** : clarification du but, anticipation de la difficulté (forethought). Garde-fou sur la **représentation de la tâche** : vérification que l'apprenant s'est fixé un but d'apprentissage et non un but de surface. Particulièrement actif lors des premières occurrences de chaque nouveau type de mission.
- **Pendant la tâche** : incitations ponctuelles à estimer sa confiance (monitoring), sans interrompre excessivement le flux.
- **Après la tâche** : synthèse des erreurs, comparaison confiance / performance réelle, invitation à l'élaboration et au double codage lorsque pertinents (self-reflection).

Les invitations métacognitives obéissent à un **principe de frugalité** : non systématiques, concentrées aux moments de transition et tâches à enjeu, variées en format pour prévenir la réponse automatique.

L'intensité des prompts est scaffoldée : plus guidés pour les novices, progressivement retirés à mesure de l'internalisation. Le système distingue un apprenant qui **internalise** (réduction planifiée des prompts) d'un apprenant qui les **évite** (réponses automatiques, temps sous seuil, taux d'erreur post-prompt inchangé). L'évitement est traité comme un signal d'alarme déclenchant un retour à des prompts plus guidés.

**Système d'auto-rapport à trois niveaux (AR) :**

L'auto-rapport est la **source d'autorité** sur les états affectifs et les régimes d'activation. Les proxys comportementaux (P5) constituent le signal de fond permanent ; l'auto-rapport les complète, les valide, et les corrige quand ils sont discordants. La hiérarchie de confiance est définie dans le Référentiel.

**(AR-Niveau 1) — Micro-sondage événementiel** : déclenché par des événements d'apprentissage à haute valeur émotionnelle, en cours de session, aux seuls points de rupture naturelle (jamais en milieu de tâche active). Maximum 1 question, format visuel binaire ou ternaire, < 10 secondes. Ce niveau est l'**unique mécanisme constitutionnel permettant de distinguer confusion productive, frustration et anxiété en temps réel** — distinction que les proxys seuls ne peuvent pas faire. Son déclenchement est événementiel (et non périodique) pour éviter la réactivité d'évaluation et la fatigue de sondage. Les conditions de déclenchement sont définies dans le Référentiel.

**(AR-Niveau 2) — Mini-sondage de fermeture** : affiché à la clôture d'une session, selon une fréquence adaptative définie dans le Référentiel (ni systématique, ni rare). Maximum 3 items visuels, couvrant trois dimensions : difficulté perçue (appraisal de contrôle), sentiment de progrès (appraisal de valeur), intention de retour (comportement anticipé). Ces dimensions correspondent aux deux axes de la Control-Value Theory (Pekrun) et permettent de valider ou corriger la lecture de régime de la session par les proxys comportementaux.

**(AR-Niveau 3) — Bilan de trajectoire périodique** : indépendant des sessions, déclenché sur une base temporelle définie dans le Référentiel. 5 à 7 items, format AEQ-dérivé, portant sur des **tendances** et non sur des états ponctuels. Génère un **indice de calibration de l'auto-rapport** détectant un biais de désirabilité sociale (apprenant déclarant systématiquement des états positifs sans corrélation avec la performance) — signal d'alarme réduisant le poids accordé aux auto-rapports de cet apprenant dans le modèle.

**Règles d'intégration de l'auto-rapport dans le modèle :**
- Auto-rapport AR-Niveau 1 concurrent à un événement → priorité maximale sur les proxys ; le régime d'activation est mis à jour immédiatement.
- Auto-rapport AR-Niveau 2 discordant avec la lecture proxy de la session → auto-rapport prime ; la discordance est consignée.
- Accumulation de discordances sur un même proxy → le poids du proxy pour cet apprenant est révisé à la baisse. Les détails de cette recalibration sont définis dans le Référentiel.

**Dimension affective opérationnelle :**
Les états affectifs utilisés par le moteur sont des **régimes opérationnels de régulation, non des diagnostics psychologiques**. Lorsqu'aucune donnée AR n'est disponible pour affiner, le moteur applique une réponse conservatrice. Ni l'anxiété ni l'ennui ne sont nommés cliniquement dans les messages.

Le système distingue l'**abandon par détresse** (taux d'erreur élevé, surcharge) de l'**abandon par désengagement rationnel** (performance correcte, refus répété, signaux de sous-défi). Le premier justifie un retour au guidage ; le second appelle une re-négociation explicite des objectifs.

**Dimension sociale :**
Introduction progressive et réversible après un seuil d'usage défini dans le Référentiel. Les missions d'apprentissage par les pairs (confrontation d'erreurs, enseignement mutuel, co-résolution) sont distinguées des effets motivationnels du lien social. Dimension optionnelle par univers, avec justification obligatoire dans la documentation de design.

---

### Principe 10 — Qualité du feedback et modèle implicite de la compétence

Le feedback porte en priorité sur le **processus** (stratégies, erreurs procédurales, pistes de révision) et sur l'**autorégulation**, plutôt que sur la personne ou les aptitudes. Tout feedback évaluatif global est accompagné d'une indication de son niveau de fiabilité.

Le feedback produit par le moteur autonome repose sur des **templates paramétriques** définis en phase Développement, indexés sur le type d'erreur, le niveau Bloom et l'état MSC. Tout feedback supposant une contextualisation linguistique fine au-delà du template est un candidat au patch (P12). La richesse des templates est un livrable obligatoire de la chaîne IA de conception.

---

### Principe 11 — Séparation des couches : conception, moteur autonome, patchs

Learn-it distingue trois couches aux responsabilités strictement séparées :

**(a) Couche conception** (chaîne IA, hors usage) : construction du graphe, génération des missions, paramétrage initial du référentiel, production des assets (missions de conflit cognitif, missions génératives, modélisation métacognitive, templates de feedback). La couche conception produit les artefacts paramétriques que le moteur exécutera.

**(b) Couche moteur autonome** (local, en usage) : toutes les décisions adaptatives session par session, par règles déterministes et modèles statistiques légers. Le moteur **ne génère aucun contenu** : il sélectionne et séquence des artefacts produits en couche conception. Aucune décision ne peut dépendre d'un appel réseau en temps réel.

**(c) Couche patch** (serveur, occasionnel) : correction documentée des dérives que le moteur ne peut corriger par simple reparamétrage. Un patch génère ou révise des artefacts paramétriques téléchargeables et intégrés localement. Les contraintes des patchs sont définies en P12.

Cette séparation est inviolable : tout mécanisme supposant de générer du contenu en phase d'usage appartient à la couche patch.

---

### Principe 12 — Patchs paramétriques : déclencheurs, périmètre et garde-fous

Un patch est déclenché par une **métrique de dérive documentée** franchissant son seuil (défini dans le Référentiel). Les patchs sont occasionnels, non continus. Le moteur reste en contrôle entre les patchs.

**Périmètre autorisé** : ajustement de paramètres du Référentiel dans les fourchettes autorisées, sous-parcours, variantes de missions, templates de feedback supplémentaires, révision des poids du graphe local, ajustement du mapping régimes → politiques.

**Périmètre interdit** : redéfinir les composantes ou seuils du MSC hors fourchettes constitutionnelles, modifier la philosophie d'adaptation (P5, P8, P13), introduire un mécanisme d'inférence psychologique sans statut probatoire, élargir silencieusement le périmètre des inférences sur l'apprenant.

**Attributs obligatoires** : paramétrique, traçable, borné, réversible (avec condition de rollback définie), transparent (l'apprenant est informé et peut consulter les raisons). La conformité constitutionnelle est vérifiée avant déploiement.

---

### Principe 13 — Intégrité du modèle apprenant

**Fondement.** L'hyper-personnalisation de Learn-it suppose que le modèle apprenant représente fidèlement UN apprenant spécifique. Toute session conduite par une autre personne — même avec la meilleure intention — pollue ce modèle et dégrade la validité de toutes les décisions adaptatives ultérieures, en particulier l'espacement, le fading et le calcul du MSC. L'intégrité du modèle est une **condition de validité de P5**, non une option.

**Philosophie.** Le système protège l'intégrité du modèle sans surveillance comportementale intrusive ni présomption de mauvaise foi. Il fournit des outils positifs (multi-profil, mode invité) qui rendent les usages légitimes multi-personne naturels et sans friction. La détection statistique (SIS) est une protection secondaire, non le mécanisme principal.

**Architecture d'intégrité en couches :**

**(a) Multi-profil** : réponse primaire aux situations de partage légitime (famille, enseignant, démonstration). Chaque personne susceptible d'utiliser le dispositif dispose de son propre profil nommé, avec son propre modèle complet (MSC, baseline comportementale, état apprenant composite). La sélection de profil au démarrage est la seule mesure nécessaire pour la grande majorité des situations de partage. Learn-it est conçu pour un usage individuel ; le multi-profil est l'outil architectural qui rend cet usage individuel praticable sur un dispositif partagé.

**(b) Mode Invité** : pour les usages de démonstration, exploration ou test par un tiers, le profil principal peut être mis en mode Invité. En mode Invité, la session se déroule normalement mais **aucune donnée n'est écrite dans le modèle**. Ce mode est disponible sans friction depuis l'écran de démarrage, visuellement distinct pendant toute la session, et non limité en durée mais signalé après un délai défini dans le Référentiel.

**(c) Mode Évaluation Externe** : pour les sessions administrées dans un contexte formel (examen blanc, évaluation par l'enseignant), les données sont enregistrées mais **taguées comme évaluation externe**. Elles alimentent uniquement la composante **T** (Transférabilité) du MSC — qui requiert précisément une réussite sur un format ou contexte différent de l'entraînement — sans modifier P, R ou A. Ce mode permet d'intégrer proprement les évaluations institutionnelles dans le modèle sans perturber la dynamique d'apprentissage.

**(d) Score d'Intégrité de Session (SIS)** : mécanisme statistique de protection résiduelle pour les situations où le multi-profil n'a pas été utilisé. Le SIS est un score continu [0, 1] calculé pour chaque session à partir de l'écart entre le profil comportemental de la session et la baseline personnelle de l'apprenant, selon des indicateurs définis dans le Référentiel. Un SIS faible n'invalide pas automatiquement une session : il conduit à une **intégration pondérée** dans le MSC et, sous un seuil défini dans le Référentiel, à une **mise en attente de confirmation** par la session suivante. Le SIS distingue les anomalies dans le sens "trop bon" (signe potentiel de substitution) des anomalies dans le sens "moins bon que d'habitude" (variation d'état intra-individuelle légitime, jamais pénalisée).

**(e) Vérification déclarative périodique** : à intervalles définis dans le Référentiel, le système pose une question neutre et non accusatoire à l'apprenant : les sessions récentes ont-elles bien été conduites par lui ? Si la réponse est négative, un mécanisme simple permet de marquer les sessions concernées comme non comptabilisées, avec recalcul du MSC. Ce mécanisme repose sur la bonne foi de l'apprenant et est présenté comme une aide à la fiabilité du modèle, jamais comme un contrôle.

**(f) Niveau de Confiance MSC** : chaque composante du MSC est associée à un niveau de confiance dérivé de l'historique SIS des sessions qui ont contribué à sa validation. Un niveau de confiance faible conduit le moteur à traiter cette composante comme *provisoire* et à programmer des vérifications supplémentaires avant d'en tirer des décisions adaptatives importantes. Les seuils et la mécanique de calcul sont définis dans le Référentiel.

**Ce que le principe 13 n'impose pas** : aucune identification biométrique, aucune surveillance des comportements hors session, aucune transmission de données à des tiers sans consentement explicite, aucune pénalisation automatique d'une session sur la seule base d'un SIS bas. L'apprenant reste toujours maître de la décision finale sur la comptabilisation de ses sessions.

---

## Cycle de design pédagogique

### 1. Analyse

Identifier les objectifs d'apprentissage, extraire les concepts, construire le graphe. Positionner chaque objectif dans la taxonomie de Bloom révisée. Déclarer l'ICC. Vérifier l'alignement constructif (Biggs).

La phase Analyse définit : (a) les **signaux comportementaux** retenus comme proxys d'états apprenants, leur statut de validation empirique, et les conditions de déclenchement des auto-rapports AR-Niveau 1 spécifiques à l'univers ; (b) les **profils d'apprenants** surveillés pour l'équité algorithmique ; (c) les concepts à **flag misconception** ; (d) la déclaration de l'objectif de **transfert lointain** ou du statut *à portée examen uniquement* ; (e) la décision d'inclure ou d'exclure la *productive failure*.

**Validation du graphe** : protocole de validation de qualité couvrant couverture Bloom, cohérence des arêtes, flags misconception, couverture des types de missions et formats de récupération. Tout graphe insuffisant est déployé uniquement en mode pilote restreint.

### 2. Design

Trajectoire **activation → démonstration → application → intégration** pour chaque objectif. La phase Design précise : missions de conflit cognitif (par nœud flaggé), missions génératives distinctes du rappel pur, décision sur la productive failure, templates de feedback par type d'erreur et niveau Bloom, et **contenus des auto-rapports AR-Niveau 1** (libellés des questions, options de réponse, mapping des réponses vers les régimes de régulation).

### 3. Développement

Produire les contenus jouables en respectant les contraintes de charge cognitive, motivation, métacognition, stratégies fondées sur la preuve et éthique de la personnalisation. Les **formats des sondages AR** (Niveau 1, 2 et 3) sont des livrables de cette phase.

### 4. Implémentation

Déployer l'univers, configurer les paramètres. Éléments de gamification non vérifiés → **mode probatoire**. Configurer les modes d'usage (Invité, Évaluation Externe) et les paramètres de multi-profil.

### 5. Évaluation et révision

Recueillir des données sur la maîtrise réelle et l'expérience. Déclencheurs de révision :

- **Écart ponctuel** : maîtrise estimée > performance réelle lors d'une simulation → ajustement immédiat.
- **Biais systématique** : sur-/sous-estimation cohérente sur plusieurs évaluations → révision du modèle d'inférence.
- **Dérive hors-jeu** : simulation stable, résultats réels inférieurs → revoir la composante T.

La phase Évaluation inclut systématiquement : (a) test de non-nuisance des éléments en période probatoire ; (b) vérification des métriques d'équité ; (c) confrontation des règles d'inférence aux données, mise à jour du statut de validation ; (d) vérification d'efficience par nœud (temps médian vs cible) ; (e) **analyse de la concordance auto-rapport / proxys comportementaux** pour chaque proxy documenté en phase Analyse — tout proxy à taux de discordance élevé avec les auto-rapports est reclassé comme "hypothèse invalidée" et retiré du modèle de cet univers ; (f) **analyse de la distribution SIS** pour identifier d'éventuelles dérives systématiques d'intégrité à l'échelle de la cohorte.

---

## Cadres théoriques de référence

- **Cognition et charge mentale** : Cognitive Load Theory (Sweller, van Merriënboer) ; effet d'inversion de l'expertise (Kalyuga) ; Desirable Difficulties (Bjork) ; *retrieval-induced forgetting* (Anderson et al.) ; apprentissage multimédia (Mayer) ; *productive failure* (Kapur).
- **Motivation et engagement** : Self-Determination Theory (Deci & Ryan) ; modèle ARCS (Keller) ; valeur-attente (Eccles & Wigfield).
- **Métacognition et auto-régulation** : Self-Regulated Learning (Zimmerman ; Winne & Hadwin — COPES) ; recommandations EEF ; self-efficacy (Bandura).
- **Émotions et apprentissage** : Control-Value Theory (Pekrun) ; affects pendant l'apprentissage (D'Mello & Graesser — confusion productive, frustration, flow) ; Ecological Momentary Assessment (Shiffman et al.) ; Peak-End rule (Kahneman).
- **Stratégies fondées sur la preuve** : rappel actif, espacement, interleaving, élaboration, double codage, worked examples et fading (Sweller, van Merriënboer) ; apprentissage génératif (Fiorella & Mayer) ; elaborative interrogation (Dunlosky et al.).
- **Apprentissage social et constructivisme** : ZPD (Vygotsky) ; apprentissage par les pairs.
- **Misconceptions et changement conceptuel** : conflit cognitif, réfutation explicite (Posner et al., Chi).
- **Personnalisation et systèmes adaptatifs** : BKT (Corbett & Anderson) ; PFA ; mastery learning (Bloom) ; équité algorithmique ; intégrité des modèles apprenants.
- **Ingénierie pédagogique** : ADDIE ; Merrill's First Principles ; Bloom révisé ; alignement constructif (Biggs) ; assessment for learning (Black & Wiliam).

---

## Glossaire

### Mastery Score Composite (MSC)

Vecteur à quatre composantes, toutes requises simultanément pour déclarer une **maîtrise robuste**. Toujours instancié à un niveau Bloom cible.

```
MSC(concept, niveau Bloom) = (P, R, A, T)
```

| Composante | Définition |
|---|---|
| **P — Précision** | Taux de réussite sur les N dernières occurrences au niveau Bloom cible |
| **R — Robustesse temporelle** | Au moins une réussite après un délai ≥ D sans stimulation du concept |
| **A — Autonomie** | Au moins M réussites sans aide ni indice |
| **T — Transférabilité** | Au moins une réussite sur un format structurellement différent de l'entraînement principal |

Les seuils opérationnels (N, D, M) sont définis dans le Référentiel. Chaque composante du MSC est associée à un **Niveau de Confiance MSC** dérivé du SIS des sessions contribuantes.

**États de maîtrise** :
- **Maîtrise provisoire héritée** : initialisée par le calibrage P0 pour les concepts confirmés en pré-test. P présumée ; R et A non encore corroborées. Génère une vérification prioritaire dans les 3 premières sessions.
- **Maîtrise d'entraînement** : P + R + A atteints, T non encore atteint.
- **Maîtrise robuste** : P + R + A + T atteints.

**Règles d'exception** :
- **Dégradation post-maîtrise** : révocation si ≥ 2 échecs consécutifs après absence ≥ seuil_R → passage en *en consolidation* (pas en *nouveau*).
- **Niveau Bloom différencié** : le MSC est toujours associé à un niveau Bloom cible.

---

### Score d'Intégrité de Session (SIS)

Score continu [0, 1] calculé pour chaque session, mesurant la proximité du profil comportemental de la session avec la baseline comportementale personnelle de l'apprenant. Un SIS proche de 1 indique un profil cohérent avec l'historique. Un SIS bas indique une anomalie — qui peut résulter d'une substitution, d'un état intra-individuel inhabituel, ou d'une progression réelle exceptionnelle. Le SIS **n'invalide jamais automatiquement** une session : il conditionne son mode d'intégration dans le MSC. Les paramètres de calcul et les seuils d'intégration sont définis dans le Référentiel.

---

### Niveau de Confiance MSC (NC-MSC)

Métadonnée associée à chaque composante du MSC, dérivée du SIS des sessions qui ont contribué à sa validation. Valeurs : **Élevé** (toutes sessions contribuantes avec SIS ≥ seuil haut) / **Moyen** (présence de sessions avec SIS intermédiaire) / **Bas** (une ou plusieurs sessions avec SIS bas ont contribué significativement). Un NC-MSC Bas conduit le moteur à traiter la composante comme provisoire et à programmer des vérifications supplémentaires. Paramètres définis dans le Référentiel.

---

### Mode Invité

Mode de session dans lequel aucune donnée n'est écrite dans le modèle apprenant à l'issue de la session. Conçu pour les usages de démonstration, exploration ou test par un tiers. Accessible sans friction depuis l'écran de démarrage. Visuellement distinct pendant toute la session. Non limitant pour le contenu affiché — la session se déroule normalement. Paramètres (signalement après délai, indicateurs visuels) définis dans le Référentiel.

---

### Mode Évaluation Externe

Mode de session dans lequel les données sont enregistrées mais taguées comme évaluation externe, excluant toute mise à jour de P, R et A. Alimente uniquement la composante T du MSC (transfert hors contexte d'entraînement). Conçu pour les évaluations formelles administrées par un enseignant ou une institution. Paramètres définis dans le Référentiel.

---

### Indice de Confiance du Corpus (ICC)

Métadonnée obligatoire déclarée en phase Analyse. Valeurs : **fort** / **partiel** / **absent**. Conditionne la stratégie de construction du graphe (P1).

---

### État apprenant composite

Modèle à deux axes (calibration × régime d'activation) avec politiques adaptatives associées (P5). L'axe calibration est inféré de façon déterministe. L'axe régime d'activation combine proxys comportementaux et auto-rapport selon une hiérarchie de confiance définie dans le Référentiel. Initialisé par le calibrage métacognitif (P0).

---

### Flag Misconception

Attribut d'un nœud du graphe signalant une représentation erronée documentée. Déclenche l'obligation d'une mission de conflit cognitif en phase Design.

---

### Période probatoire (gamification)

Statut d'un élément de gamification déployé mais dont le test de non-nuisance n'a pas encore été vérifié. Collecte de données obligatoire ; déploiement à large échelle suspendu.

---

*Constitution v1.4 — intègre les chantiers d'auto-rapport affectif (P9 amendé, P5 amendé) et d'intégrité du modèle apprenant (nouveau P13, glossaire étendu). À lire conjointement avec le Référentiel de defaults pédagogiques v0.3.*
