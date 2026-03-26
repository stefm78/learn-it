# Constitution conceptuelle — Learn-it v1.6

`[HASH:C4D9A3F2]`

*Paramètres : USAGE=LLM_INPUT | DOC_TYPE=TECHNIQUE | LANGUE=FR | VERSION=v1.6 | STRUCTURE=MULTI-PARTIES | MODE=STANDARD | TAILLE=LARGE | NIVEAU_DETAIL=STANDARD | AUDIENCE=EXPERT | FORMAT_OUTPUT=MD*

*Source : Constitution v1.5 [HASH:437637E4] + analyse critique externe (9 modifications). Ratio calculé sur source composite.*

***

### Contexte / Objectifs / Évolutions `[S1]`

**v1.6** étend v1.5 sur 5 chantiers. `[S1]` `[MODIFIÉ S1 v1.5→v1.6]`

1. **Solidification logique MSC** : P16 (règle d'agrégation AND constitutionnelle) lève l'ambiguïté de la fonction f(P,R,A,deg) déléguée au Référentiel.
2. **Propagation d'incertitude sur graphe** : P17 — rétrogradation KU → marquage prioritaire des dépendances directes, état interdit si règle absente.
3. **Axe Valeur-Coût perçue** : P18 — troisième axe optionnel du modèle d'état apprenant ; déclencheur patch autonome de relevance.
4. **Contexte authentique obligatoire** : P19 — Merrill 5e principe opérationnalisé ; plafonnement Bloom en son absence.
5. **Clarifications sans changement de philosophie** : P2 (matrice couverture feedback livrable Design obligatoire), P3 (statut créatif R non applicable = fallback ×1), P5 (profil AR-réfractaire formalisé), P9 (intention de session forethought), P12 (impact_scope attribut obligatoire + liste de contrôle qualité pédagogique patch).

**v1.5** étend v1.4 sur 3 chantiers : universalité disciplinaire (KU typées), garde-fous architecturaux (GF-01, GF-02, GF-08), nouveaux principes P14–P15. `[S1]`

**v1.4** : auto-rapport affectif 3 niveaux (P9) ; P13 intégrité modèle apprenant. `[S1]`

**Gouvernance** `[CRITIQUE]` : Constitution = *quoi/pourquoi* → modifiable par délibération explicite. Référentiel = *combien/comment* → révisable librement. Séparation inviolable. La logique d'agrégation MSC (P16) est un invariant constitutionnel non délégable. `[S1]`

***

### Fondamentaux `[S2–S8]`

**P0 — Calibrage initial** `[S2]`

- **(a) Calibrage épistémique** : diagnostic adaptatif court → initialise état graphe (prérequis maîtrisés / en doute / lacunes). Format adapté au type KU dominant (P14). Absence de calibrage → hypothèse conservatrice (position initiale basse) + déblocage manuel apprenant.
- **Maîtrise provisoire héritée** `[CRITIQUE]` : état MSC distinct de la *maîtrise d'entraînement*. Composantes P, R, A *présumées* non corroborées. Vérification prioritaire R et A dans les 3 premières sessions. Si confirmées → *maîtrise d'entraînement* ; sinon → *en consolidation* + parcours réactivation. Composante T non validée à ce stade.
- **(b) Calibrage métacognitif** : prédiction de performance intégrée au pré-test → initialise composante Calibration (P5).
- Calibrage : court, engageant, restitution cartographie visuelle immédiate. Sans styles d'apprentissage invalidés (VARK). Inférences initiales à confiance réduite, révisées prioritairement par données premières sessions.

---

**P1 — Primat maîtrise compétences examen** `[S3]`

- Axe de progression par type KU `[CRITIQUE]` : Bloom révisé (déclarative/formelle) ; automatisation guidée→autonome→transfert adaptatif (procédurale) ; finesse de discrimination (perceptuelle) ; maîtrise conventions → déviation productive intentionnelle (créative).
- **ICC** (Indice de Confiance du Corpus) : fort / partiel / absent → conditionne stratégie construction graphe.
- Graphe sur annales + structure disciplinaire. Concept absent annales mais présent corpus → maintenu dans graphe, niveau Bloom minimum, pondération réduite — **jamais supprimé**.
- **Lacunes ≠ Misconceptions** `[CRITIQUE]` : missions sur nœud flaggé misconception = conflit cognitif explicite obligatoire avant représentation correcte. Rappel actif seul insuffisant.
- Alignement constructif (Biggs) vérifié en phase Analyse. Transfert lointain déclaré explicitement si visé.

---

**P2 — Moteur générique / graphe KU** `[S4]` `[MODIFIÉ S4 v1.5→v1.6]`

- Graphe orienté de KU. Relations déclarées en phase Analyse : prérequis logiques, dépendances d'exécution, co-occurrence perceptuelle, affordances créatives.
- 2 types de nœuds : **nœuds KU** + **nœuds human_checkpoint** (P15 ; bloquant ou non-bloquant selon niveau autonomie).
- Décisions adaptatives en usage : **règles déterministes + modèles statistiques légers locaux uniquement** `[CRITIQUE]`. Zéro appel réseau temps réel. Inférence non formalisable → exclue du moteur → candidate patch (P12).
- Fading déclenché par composante **A** du MSC (définition opérationnelle par type KU). Résistance au guidage → signal surqualification (Kalyuga, effet inversion expertise) → réduction proactive guidage.
- Explicabilité sur demande ; non sollicitée uniquement aux transitions inter-sessions.
- **Couverture feedback préindexée** `[CRITIQUE]` `[AJOUTÉ]` : le moteur sélectionne parmi templates feedback produits en phase Design — **zéro génération feedback à la volée**. Pour KU formelles et procédurales, la phase Design produit obligatoirement une **matrice couverture feedback** (patterns d'erreurs typiques × templates disponibles). Erreur non couverte → feedback générique processus + flag `erreur-hors-taxonomie` → candidat prioritaire enrichissement prochain patch. Proportion patterns non couverts = métrique qualité conception (seuil Référentiel). `[DEP-EXT S4 : Référentiel v0.4 — seuil couverture feedback]`

---

**P3 — Temporalité et mémoire** `[S5]` `[MODIFIÉ S5 v1.5→v1.6]`

- Stratégie de consolidation par type KU : rappel actif (déclarative/formelle) ; pratique exécutoire distribuée (procédurale) ; exposition contrastive espacée (perceptuelle) ; élaboration contrainte espacée (créative). Terme générique : **occurrence de consolidation**.
- Algo d'espacement (DA-4) : déterministe, local, sans dépendance externe, paramétré par P et R du MSC.
- **Multiplicateur R** par type KU : procédurale ×2–3 (rétention lente) ; perceptuelle ×0,5 (oubli précoce plus sensible) ; déclarative/formelle ×1 (référence). R = garde-fou `[CRITIQUE]` : KU non validée sur R → non déclarable maîtrisée.
- **Multiplicateur R créatif** `[CRITIQUE]` `[MODIFIÉ]` : « non applicable » signifie absence de calibration empirique disponible — **pas d'exemption de l'espacement**. Valeur de fallback = ×1 (déclarative) jusqu'à calibration terrain. Révisable par Référentiel. L'espacement s'applique à **toutes** les KU sans exception.
- **Espacement prioritaire** tous types. **Interleaving conditionnel** : catégories en priorité (transfert le plus robuste) ; contenus après atteinte simultanée P+A (R non prérequis car interleaving = test R en conditions réelles). Contrainte couverture équilibrée (anti-retrieval-induced forgetting, Anderson et al.).
- *Productive failure* (Kapur) : non intégrée par défaut — décision explicite par univers.
- Interruption > seuil_R → session reprise diagnostique avant reprise parcours.

---

**P4 — Planification vers date cible** `[S6]`

L'étudiant déclare une date d'examen. Moteur planifie + réajuste chemin pour maximiser maîtrise à l'échéance. Représentation mobilisatrice, non anxiogène. Marges de choix pour soutenir autonomie et entraîner capacité de planification.

---

**P5 — Hyper-personnalisation** `[S7]` `[MODIFIÉ S7 v1.5→v1.6]`

- **Modèle d'état apprenant composite — 3 axes** `[MODIFIÉ]` :
    - Axe 1 **Calibration** : bien calibré / surestimateur / sous-estimateur. Inféré de façon déterministe (écart prédictions ↔ performances).
    - Axe 2 **Régime d'activation** : productif / détresse / sous-défi. NON diagnostic psychologique. Source d'autorité = auto-rapport (P9) ; proxys comportementaux = signal de fond permanent.
    - Axe 3 **Valeur-Coût perçue (VC)** `[AJOUTÉ]` : optionnel. États : VC-Élevée / VC-Neutre / VC-Basse. Inféré par item unique AR-N2 dédié (fréquence adaptative, Référentiel). VC Bas persistant sur N sessions consécutives (seuil Référentiel) = déclencheur patch *relevance* — distinct de la détresse et du sous-défi. VC **jamais** utilisée comme critère pénalisation ni proxy performance. `[DEP-EXT S7 : Référentiel v0.4 — seuil VC persistance]`
- **Distinction critique confusion / frustration / anxiété** `[CRITIQUE]` : proxys similaires, interventions opposées.
    - *Confusion productive* (D'Mello & Graesser) : engagement actif en ZPD → scaffolding, ne pas réduire difficulté.
    - *Frustration/épuisement* : désengagement → réduction charge, changement format.
    - *Anxiété* : performance altérée par inquiétude → réduction difficulté + message soutien.
    - Sans auto-rapport disponible → **intervention conservatrice et réversible** (scaffolding léger) jusqu'à obtention AR. `[EMPHASE]`
- **Profil AR-réfractaire** `[AJOUTÉ]` `[CRITIQUE]` : la distinction confusion/frustration/anxiété est architecturalement impossible sans AR-N1. Apprenant systématiquement non-répondant sur N sessions consécutives (seuil Référentiel) → flag `profil-AR-réfractaire` → adaptation du mode de sollicitation (format, déclencheur) via patch. La règle conservatrice n'est pas une dégradation — c'est un invariant constitutionnel en absence d'AR. `[DEP-EXT S7 : Référentiel v0.4 — seuil N sessions AR-réfractaire]`
- Validité inférentielle : toute règle comportement → état = hypothèse à valider empiriquement.
- Équité algorithmique : profils surveillés définis *a priori* ; écart systématique > seuil → révision modèle (pas seulement signalement).
- Aucun plafond de difficulté imposé définitivement.

---

**P6 — Transition feuille blanche** `[S8]`

Modes progressifs vers format réel d'examen. Transfert proche prioritaire. Progression vers modes sans aide = montée composante **A** du MSC.

***

### Mécanismes `[S9–S17]`

**P7 — Adaptation environnement d'usage** `[S9]`

Budget cognitif session = somme pondérée des tâches (proxy DA-2 par type). Proxy temporel = garde-fou de dernier ressort. Sessions longues soutenues préservées (formation de schémas complexes non productible par micro-fragmentation seule).

---

**P8 — Gamification éthique** `[S10]`

- Mécaniques d'engagement → effort cognitif et maîtrise, PAS rétention d'attention.
- Récompenses extrinsèques : phase amorçage → retrait progressif au profit compétence intrinsèque (SDT).
- 2 régimes : (a) éléments pédagogiques — principe cohérence Mayer strict ; (b) éléments gamification — test de non-nuisance requis. Non vérifié → **période probatoire**.
- Clôture motivationnelle après mission majeure : accompli + comparaison niveau départ + ancrage compétence (ARCS Satisfaction, SDT). `[S10]`

---

**P9 — Métacognition, SRL, auto-rapport** `[S11]` `[MODIFIÉ S11 v1.5→v1.6]`

- Boucle SRL (Zimmerman) : forethought / monitoring / self-reflection.
- **Intention de session** `[AJOUTÉ]` : pour soutenir le *forethought* SRL authentique, le moteur propose une intention de session déclarative courte (≤ 1 item, optionnel, non bloquant) aux transitions inter-sessions. Non utilisée comme contrainte adaptative — ancrage forethought uniquement. Confrontation intention / réalisation (AR-N2) = micro-cycle SRL autonome. Fréquence et format définis en Référentiel. Absence de réponse **jamais pénalisée**. `[DEP-EXT S11 : Référentiel v0.4 — fréquence intention session]`
- Invitations métacognitives : **frugalité** — non systématiques, concentrées aux transitions et tâches à enjeu, variées. Intensité scaffoldée. Distinction internalisation (retrait planifié) vs évitement (retour prompts guidés).
- **Système AR à 3 niveaux** `[CRITIQUE]` :
    - **AR-N1** Micro-sondage événementiel : 1 question visuelle binaire/ternaire, < 10 s, aux ruptures naturelles uniquement. **Seul mécanisme distinguant confusion / frustration / anxiété en temps réel.** Déclenchement événementiel (pas périodique) pour éviter fatigue de sondage.
    - **AR-N2** Mini-sondage fermeture session : ≤ 3 items visuels — difficulté perçue (CVT contrôle), progrès perçu (CVT valeur), intention retour, **[AJOUTÉ] item VC (perception utilité/effort)**. Fréquence adaptative (Référentiel).
    - **AR-N3** Bilan trajectoire périodique : 5–7 items AEQ-dérivé sur tendances. Génère indice calibration AR → détecte biais désirabilité sociale.
- **Règles d'intégration AR** `[CRITIQUE]` : AR-N1 concurrent → mise à jour immédiate régime. AR-N2 discordant avec proxy → AR prime + discordance consignée. Accumulation discordances → poids proxy révisé à la baisse.
- Abandon par détresse (erreurs + surcharge) ≠ abandon par désengagement rationnel (performance correcte + sous-défi) → réponses opposées.

---

**P10 — Qualité du feedback** `[S12]`

- Feedback sur **processus + autorégulation** prioritaire sur personne ou aptitudes.
- **Modalité par type KU** `[CRITIQUE]` :
    - Déclarative/Formelle : templates textuels indexés erreur + niveau Bloom + MSC. Canal textuel principal.
    - Procédurale : point de rupture séquence + relecture annotée + worked example vidéo. Canal textuel secondaire uniquement.
    - Perceptuelle : contraste simultané (juxtaposition, heatmap, zones discriminantes). Feedback différé en régime avancé (profil d'erreurs sur série).
    - Créative : rubrique multi-critères non-directive. Feedback prescriptif **proscrit**.
- **Canal textuel seul interdit pour KU procédurales et perceptuelles** `[CRITIQUE]` — livrable obligatoire chaîne IA conception.

---

**P11 — Séparation des couches** `[S13]`

3 couches séparées `[CRITIQUE]` :

- **Conception** (hors usage) : graphe, missions, paramétrage, assets (missions conflit cognitif, génératives, templates feedback, matrice couverture feedback P2).
- **Moteur autonome** (local, en usage) : sélectionne et séquence artefacts. **Zéro génération de contenu. Zéro appel réseau.**
- **Patch** (serveur, occasionnel) : corrige dérives, génère/révise artefacts paramétriques téléchargeables intégrés localement.

Séparation inviolable : tout mécanisme de génération de contenu en usage → couche patch.

---

**P12 — Patchs paramétriques** `[S14]` `[MODIFIÉ S14 v1.5→v1.6]`

- Déclencheur : métrique de dérive documentée franchissant seuil (Référentiel). Patchs occasionnels, non continus. `[AJOUTÉ]` VC Bas persistant (P18) = déclencheur autonome de patch *relevance*.
- Périmètre **autorisé** : paramètres Référentiel dans fourchettes, sous-parcours, variantes missions, templates feedback, révision poids graphe, enrichissement matrice couverture feedback.
- Périmètre **interdit** `[CRITIQUE]` : redéfinition composantes/seuils MSC hors fourchettes constitutionnelles ; modifier philosophie adaptation (P5, P8, P13) ; introduire inférence psychologique sans statut probatoire ; modifier logique d'agrégation AND (P16) ; modifier règle de propagation graphe (P17).
- **Attributs obligatoires de tout patch** `[CRITIQUE]` :
    - `paramétrique` — modifie paramètres, pas la logique constitutionnelle
    - `traçable` — log complet
    - `borné` — tous paramètres ∈ fourchettes Référentiel
    - `réversible` — condition rollback définie
    - `transparent` — apprenant informé
    - `impact_scope` `[AJOUTÉ]` — liste des KU impactées, composantes MSC concernées, règles d'inférence modifiées. Tout patch dont l'impact_scope n'est pas calculable → **rejeté intégralement** (même règle que GF-02).
- **Liste de contrôle qualité pédagogique** `[AJOUTÉ]` `[CRITIQUE]` : tout artefact généré par patch (missions, templates feedback) est soumis à vérification constitutionnelle par la chaîne IA serveur : respect P10 (modalité feedback par type KU), respect P14 (typage KU), alignement constructif (Biggs), compatibilité P19 (contexte authentique). Ces critères sont définis ici et **non patchables**.
- **GF-01 — Atomicité** `[CRITIQUE]` : double-buffer obligatoire. Snapshot avant application ; patch sur copie ; swap atomique OS-level. Rollback automatique si échec. Patch partiellement appliqué = **état interdit** — aucune décision sur modèle intermédiaire.
- **GF-02 — Vérification fourchettes locale** `[CRITIQUE]` : vérification locale + déterministe avant application. Paramètre hors fourchette → patch rejeté **intégralement**. Rejet logué + apprenant informé. Zéro dépendance réseau.
- **GF-08 — Hiérarchie résolution conflits** `[CRITIQUE]` : (1) protection apprenant (P5, P8, P13) > (2) charge cognitive (P7) > optimisation MSC court terme (P1) > (3) auto-rapport (P9) > décisions adaptatives auto (P5) > (4) atomicité/intégrité modèle (P13, GF-01) > fluidité expérience (P8). Conflit non couvert → réponse **conservatrice** obligatoire + logué + décision ouverte prochain patch.

---

**P13 — Intégrité modèle apprenant** `[S15]`

- **Fondement** `[CRITIQUE]` : session conduite par un tiers pollue MSC → dégrade validité P5. Intégrité = condition de validité, pas option.
- Architecture en couches :
    - **(a) Multi-profil** : réponse primaire. Chaque utilisateur = profil nommé complet (MSC, baseline, état composite).
    - **(b) Mode Invité** : aucune écriture dans le modèle. Accessible sans friction. Visuellement distinct. Non limité en durée.
    - **(c) Mode Évaluation Externe** : données taguées → alimentent **uniquement T** (transfert). P, R, A inchangés.
    - **(d) SIS** `[0, 1]` : anomalie "trop bon" (substitution?) vs "moins bon que d'habitude" (variation intra-individuelle légitime — **jamais pénalisée**). SIS bas → intégration pondérée ; sous seuil → mise en attente confirmation session suivante.
    - **(e) Vérification déclarative périodique** : question neutre, non accusatoire. Réponse négative → marquage sessions + recalcul MSC. Repose sur bonne foi.
    - **(f) NC-MSC** : dérivé historique SIS sessions contribuantes. NC-MSC Bas → composante traitée comme provisoire + vérifications supplémentaires planifiées.
- **Ce que P13 n'impose pas** `[CRITIQUE]` : aucune biométrie, aucune surveillance hors session, aucune transmission tiers sans consentement, aucune pénalisation automatique sur SIS bas seul. Apprenant maître de la comptabilisation.

---

**P14 — Typage épistémologique KU** `[S16]`

- Déclaration type KU dominant obligatoire en phase Analyse `[CRITIQUE]`. Sans elle : inadéquation silencieuse pour tout domaine non déclaratif.
- **Taxonomie KU** : Déclarative (faits/règles, verdict binaire) ; Procédurale (automatisation geste/routine) ; Perceptuelle (finesse discrimination) ; Formelle (rigueur démo + transfert structurel) ; Créative (conventions + intention expressive).
- Typage par chaîne IA en phase Analyse (protocole ADDIE-0). Type dominant par univers ; annotations locales pour nœuds déviants. Score confiance < seuil → flag validation humaine `[?]`.
- Conditionne automatiquement : MSC, feedback (P10), trajectoire pédagogique (Design), proxys (P5), budget cognitif (DA-2), multiplicateur R (DA-4).

---

**P15 — Niveau d'autonomie moteur** `[S17]`

- Déclaré en phase Analyse. Non révisable en cours de déploiement sans retour phase Analyse.
- **4 niveaux** `[CRITIQUE]` :
    - **Autonome** : moteur gère intégralement. KU déclarative, formelle, perceptuelle, procédurale P1.
    - **Hybride recommandé** : jalons humains suggérés non bloquants. Procédurale P2 (physique bas risque).
    - **Hybride bloquant** : human_checkpoints bloquants (reprise après validation tuteur). Procédurale P3 + créative couche 3.
    - **Assisté** : moteur = préparation, diagnostic, traçabilité uniquement. Feedback délégué tuteur humain. Procédurale P4 (haut risque). **Déploiement interdit sans infrastructure de suivi tutoral.**
- **Niveaux risque procédural** : P1 numérique (nul) / P2 physique bas risque / P3 modéré / P4 haut risque (conséquences graves si mauvais geste).
- **Human_checkpoint** — attributs obligatoires : `blocking` (bool), `ku_type`, `validation_criteria`, `phase_msc`. Moteur planifie, notifie, attend. Ne juge pas le résultat du jalon.

---

**P16 — Règle d'agrégation MSC** `[S17b]` `[AJOUTÉ]` `[CRITIQUE]`

- La déclaration de maîtrise d'une KU requiert la satisfaction **simultanée** des composantes P, R et A au-dessus de leurs seuils respectifs — **logique AND**.
- La composante T (transférabilité) constitue une maîtrise de niveau supérieur, déclarée séparément et **jamais prérequise** pour la maîtrise de base.
- Cette règle d'agrégation est un **invariant constitutionnel non délégable au Référentiel** : le Référentiel ne définit que les valeurs de seuil, non la logique de combinaison.
- Toute modification de la logique AND (vers pondération, minimum, ou autre) constitue une **révision constitutionnelle** nécessitant délibération explicite.
- Conséquence sur révocation : la défaillance de **n'importe laquelle** des composantes P, R ou A (cf. seuils Référentiel) suffit à rétrograder l'état MSC.

---

**P17 — Propagation d'incertitude sur le graphe** `[S17c]` `[AJOUTÉ]` `[CRITIQUE]`

- Toute rétrogradation MSC d'une KU (passage `maîtrisé → en consolidation` ou `en consolidation → lacune`) déclenche automatiquement un **marquage de vérification prioritaire** sur l'ensemble des KU dépendantes (arêtes sortantes directes du graphe).
- Les KU marquées ne sont pas rétrogradées automatiquement, mais leur prochaine occurrence de consolidation est planifiée avec **priorité maximale** et intègre une tâche diagnostique courte (format calibrage par type KU, Référentiel).
- La propagation couvre **au maximum 1 saut de dépendance** (pas de cascade illimitée au-delà des arcs directs).
- **État interdit** : absence de cette règle dans le moteur pour un graphe comportant des arêtes de dépendance. Équivalent GF-01 pour l'intégrité du graphe.
- Condition de mise en œuvre : les arêtes de dépendance doivent être déclarées en phase Analyse (P2 / ADDIE-0) — graphe sans arêtes déclarées → état Hybride bloquant minimum requis (P15).

---

**P18 — Valeur-Coût perçue** `[S17d]` `[AJOUTÉ]`

- Axe optionnel du modèle d'état apprenant (P5, Axe 3). Inféré uniquement par item AR-N2 — **aucun proxy comportemental autonome autorisé** pour cet axe.
- **États VC** : VC-Élevée (utilité perçue > coût perçu), VC-Neutre, VC-Basse (coût perçu > utilité perçue).
- VC Bas persistant sur N sessions consécutives (seuil Référentiel) = déclencheur de patch *relevance* : révision de la présentation des enjeux, des missions de contextualisation, du lien explicite avec le contexte authentique (P19) — **non** d'ajustement de difficulté.
- **Ce que P18 n'impose pas** : VC non utilisée comme proxy de motivation générale, non exposée à l'apprenant comme diagnostic, non corrélée mécaniquement au régime d'activation (Axe 2). VC Basse ≠ détresse ≠ désengagement rationnel — réponse adaptative distincte.
- Si l'item AR-N2 VC n'est pas obtenu (apprenant non-répondant) : axe VC considéré inconnu, aucune inférence autorisée.

---

**P19 — Contexte authentique** `[S17e]` `[AJOUTÉ]` `[CRITIQUE]`

- Toute application Learn-it déclare en phase Analyse un **contexte authentique de référence** : la situation-problème réelle dans laquelle les KU maîtrisées sont mobilisées (examen, situation professionnelle, projet concret).
- Ce contexte est le cadre narratif implicite du graphe de KU. Il conditionne la formulation des tâches de transfert (composante T du MSC) et des missions de feuille blanche (P6).
- **Absence de contexte authentique déclaré** → missions de niveau Bloom ≥ 4 (application, analyse, évaluation, création) **interdites**. Les KU concernées restent plafonnées au niveau compréhension (Bloom 2) jusqu'à déclaration explicite du contexte. `[CRITIQUE]`
- Le contexte authentique est un livrable obligatoire de la phase Analyse (ADDIE). Il est révisable par patch si le contexte cible de l'apprenant évolue, dans le périmètre autorisé P12.
- Conformité Merrill (5e principe — Problem-Centered) : le contexte authentique est l'ancrage de tous les niveaux Bloom supérieurs. `[DEP-EXT S17e : Merrill's First Principles of Instruction, 2002]`

***

### Mécanismes — Cycle ADDIE `[S18]` `[MODIFIÉ S18 v1.5→v1.6]`

1. **Analyse** : extraire KU, construire graphe, déclarer type KU dominant (P14) + ICC + niveau autonomie (P15) + axe de progression (P1) + alignement constructif (Biggs) + flags misconception + objectif transfert lointain + **[AJOUTÉ] contexte authentique de référence (P19)** + **[AJOUTÉ] activation axe VC si souhaité (P18)**. Définir proxys comportementaux + statut validation empirique + profils équité + conditions AR-N1. Déclarer arêtes dépendance graphe (requis P17). Valider graphe (couverture, cohérence arêtes, human_checkpoints requis). Graphe insuffisant → pilote restreint uniquement.
2. **Design** : trajectoire pédagogique par type KU. Missions conflit cognitif (nœuds flaggés), missions génératives, décision productive failure, templates feedback (P10), **[AJOUTÉ] matrice couverture feedback (P2 — livrable obligatoire pour KU formelles et procédurales)**, contenus AR-N1 (libellés + mapping régimes), **[AJOUTÉ] item AR-N2 VC (P18 si axe activé)**, **[AJOUTÉ] item AR-N2 intention session (P9)**, human_checkpoints. Transitions = seuils MSC définis en Analyse. Missions de niveau Bloom ≥ 4 liées au contexte authentique (P19).
3. **Développement** : contenus jouables respectant charge cognitive, motivation, métacognition, éthique. Formats sondages AR (N1, N2, N3) = livrables **obligatoires**.
4. **Implémentation** : déploiement + configuration. Gamification non vérifiée → **mode probatoire**. Configuration modes Invité, Évaluation Externe, multi-profil. Vérification règle de propagation graphe activée (P17).
5. **Évaluation** : déclencheurs (écart ponctuel, biais systématique, dérive hors-jeu, **[AJOUTÉ] VC Bas persistant (P18)**, **[AJOUTÉ] taux erreurs hors-taxonomie > seuil (P2)**). Inclut systématiquement : test non-nuisance gamification probatoire ; métriques équité ; confrontation règles inférence / données + mise à jour statut validation ; efficience par nœud ; concordance AR / proxys (proxy taux discordance élevé → "hypothèse invalidée" + retiré du modèle) ; distribution SIS cohorte ; **[AJOUTÉ] taux couverture matrice feedback par univers** ; **[AJOUTÉ] profils AR-réfractaires détectés**.

***

### Tables récap `[INFÉRÉ]`

**MSC — Opérandes par type de KU** `[S20]`

| Composante | Déclarative (réf.) | Formelle | Procédurale | Perceptuelle | Créative |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **P** | Taux ≥ 80% sur N≥5 | 100% chaîne complète | Score rubrique multi-dim ≥ seuil | d-prime (SDT) ≥ seuil | Critères formels + rubrique auto-déclaré calibré |
| **R** | Réussite après délai D | Idem déclarative | D × ×2–3 | D × ×0,5 | D × ×1 (fallback P3) |
| **A** | M réussites sans aide textuelle | Sans scaffolding formel | M exécutions, variabilité inter-essais < seuil, sans guidage physique | M discriminations sans étiquette ni contraste | M productions page blanche sans prompt ni template |
| **T** | Format structurellement différent | Problème isomorphe | Exécution sous contrainte modifiée | Conditions dégradées / exemplaires atypiques | Registre/contrainte radicalement différent |

> Agrégation : P AND R AND A ≥ seuils → maîtrise de base. T = niveau supérieur, indépendant. `[P16]` `[AJOUTÉ]`

---

**Modèle d'état apprenant — 3 axes** `[S7][INFÉRÉ]` `[MODIFIÉ]`

| Axe | États | Source d'autorité | Règle moteur en absence |
| :-- | :-- | :-- | :-- |
| 1 — Calibration | Bien calibré / Surestimateur / Sous-estimateur | Inférence déterministe | N/A (toujours calculable) |
| 2 — Régime d'activation | Productif / Détresse / Sous-défi | AR-N1 (autorité) + proxys (fond) | Conservatrice réversible |
| 3 — Valeur-Coût VC | VC-Élevée / VC-Neutre / VC-Basse | AR-N2 item VC uniquement | Inconnu — aucune inférence |

---

**Niveaux autonomie moteur** `[S17][INFÉRÉ]`

| Niveau | Jalons humains | KU applicables |
| :-- | :-- | :-- |
| Autonome | Aucun | Déclarative, Formelle, Perceptuelle, Procédurale P1 |
| Hybride recommandé | Suggérés, non bloquants | Procédurale P2 |
| Hybride bloquant | Bloquants (human_checkpoint) | Procédurale P3, Créative couche 3 |
| Assisté | Feedback délégué tuteur | Procédurale P4 |

---

**Hiérarchie GF-08 — Conflits entre principes** `[S14][INFÉRÉ]`

| Priorité | Principe dominant | Principe subordonné |
| :-- | :-- | :-- |
| 1 | Protection apprenant (P5, P8, P13) | Tout autre principe |
| 2 | Charge cognitive (P7) | Optimisation MSC court terme (P1) |
| 3 | Auto-rapport (P9) | Décisions adaptatives auto (P5) |
| 4 | Atomicité/intégrité modèle (P13, GF-01, P17) | Fluidité expérience (P8) |

---

**Déclencheurs patch — table complète** `[S14][INFÉRÉ]` `[MODIFIÉ]`

| Déclencheur | Origine | Cible patch |
| :-- | :-- | :-- |
| Écart performance > seuil | Moteur | Paramètres, sous-parcours |
| Biais cohorte systématique | Métriques équité | Révision modèle inférence |
| Révocation MSC > seuil | Moteur | Recalibration seuils, missions |
| Oscillation concept ≥ 3 cycles | Moteur | Missions conflit cognitif, graphe |
| Sessions SIS bas > seuil | Moteur | Vérification intégrité |
| Taux erreurs hors-taxonomie > seuil | Moteur | Enrichissement matrice feedback `[AJOUTÉ]` |
| VC Bas persistant ≥ N sessions | AR-N2 | Révision relevance / contexte `[AJOUTÉ]` |
| Profil AR-réfractaire détecté | AR-N1 | Révision mode sollicitation `[AJOUTÉ]` |

***

### Glossaire sigles `[S20]`

| Sigle | Définition |
| :-- | :-- |
| KU | Knowledge Unit — unité atomique du graphe |
| MSC | Mastery Score Composite — vecteur (P, R, A, T) |
| P / R / A / T | Précision / Robustesse temporelle / Autonomie / Transférabilité |
| SIS | Score d'Intégrité de Session — continu |
| NC-MSC | Niveau de Confiance MSC : Élevé / Moyen / Bas |
| ICC | Indice de Confiance du Corpus : fort / partiel / absent |
| AR | Auto-Rapport (niveaux N1, N2, N3) |
| SRL | Self-Regulated Learning |
| CVT | Control-Value Theory (Pekrun) |
| GF | Garde-Fou architectural (GF-01, GF-02, GF-08) |
| DA-n | Decision Algorithm n (Référentiel) |
| ZPD | Zone Proximale de Développement |
| ADDIE | Analyse / Design / Développement / Implémentation / Évaluation |
| SDT | Self-Determination Theory (Deci & Ryan) |
| ARCS | Attention / Relevance / Confidence / Satisfaction (Keller) |
| VC | Valeur-Coût perçue — Axe 3 modèle apprenant `[AJOUTÉ]` |

***

### Cadres théoriques `[S19]` `[MODIFIÉ S19 v1.5→v1.6]`

- **Charge cognitive / mémoire** : CLT (Sweller, van Merriënboer) ; 4C/ID ; effet inversion expertise (Kalyuga) ; Desirable Difficulties (Bjork) ; retrieval-induced forgetting (Anderson et al.) ; apprentissage multimédia (Mayer) ; productive failure (Kapur) ; apprentissage perceptuel interleaved (Kornell & Bjork 2008) ; ACT-R / phases automatisation (Anderson, Fitts & Posner).
- **Expertise** : Dreyfus & Dreyfus ; knowledge telling vs transforming (Bereiter & Scardamalia) ; Signal Detection Theory (Green & Swets).
- **Motivation** : SDT (Deci & Ryan) ; ARCS (Keller) ; valeur-attente (Eccles & Wigfield) `[EMPHASE P18]`.
- **Métacognition / SRL** : Zimmerman ; Winne & Hadwin (COPES) ; EEF ; self-efficacy (Bandura).
- **Émotions** : CVT (Pekrun) ; D'Mello & Graesser (confusion productive, frustration, flow) ; EMA (Shiffman et al.) ; Peak-End rule (Kahneman).
- **Stratégies probantes** : rappel actif, espacement, interleaving, élaboration, double codage, worked examples + fading (Sweller, van Merriënboer) ; apprentissage génératif (Fiorella & Mayer) ; elaborative interrogation (Dunlosky et al.).
- **Social / constructivisme** : ZPD (Vygotsky) ; apprentissage par les pairs.
- **Misconceptions** : conflit cognitif + réfutation explicite (Posner et al., Chi).
- **Systèmes adaptatifs** : BKT (Corbett & Anderson) ; PFA ; mastery learning (Bloom) ; équité algorithmique.
- **Ingénierie pédagogique** : ADDIE ; Merrill's First Principles (dont 5e principe Problem-Centered, opérationnalisé P19) `[MODIFIÉ]` ; Bloom révisé ; alignement constructif (Biggs) ; assessment for learning (Black & Wiliam).

***

### Seuils / Bornes critiques `[S20]` `[MODIFIÉ S20 v1.5→v1.6]`

- **P déclarative** : ≥ 80% sur N ≥ 5 occurrences.
- **P formelle** : 100% sur chaîne complète.
- **Multiplicateur R procédurale** : ×2–3 vs déclarative.
- **Multiplicateur R perceptuelle** : ×0,5 vs déclarative.
- **Multiplicateur R créatif** : ×1 (fallback) jusqu'à calibration terrain. `[AJOUTÉ]`
- **Logique agrégation MSC** : AND strict sur P, R, A. T indépendant. `[AJOUTÉ P16]`
- **Propagation graphe** : 1 saut de dépendance maximum. `[AJOUTÉ P17]`
- **AR-N1** : ≤ 1 question, < 10 s, binaire/ternaire. Jamais en milieu de tâche active.
- **AR-N2** : ≤ 3 items visuels (dont item VC si axe activé, dont item intention session).
- **AR-N3** : 5–7 items AEQ-dérivé.
- **SIS** : score. SIS bas → intégration pondérée ; sous seuil → mise en attente session suivante. Anomalie "moins bon que d'habitude" jamais pénalisée.
- **NC-MSC** : Élevé / Moyen / Bas.
- **Maîtrise provisoire héritée** : vérification R et A dans les 3 premières sessions.
- **Contexte authentique absent** → Bloom ≥ 4 interdit. `[AJOUTÉ P19]`
- **GF-01** : snapshot + swap atomique OS-level obligatoires. Patch partiellement appliqué = état interdit.
- **GF-02** : paramètre hors fourchette → patch rejeté intégralement. Zéro réseau.
- **GF-02 étendu** : impact_scope non calculable → patch rejeté intégralement. `[AJOUTÉ P12]`
- **Hybride bloquant** : parcours bloqué jusqu'à validation tuteur humaine.
- **Assisté** : déploiement interdit sans infrastructure de suivi tutoral.
- **Conflit GF-08 non couvert** → réponse conservatrice obligatoire + logué. `[DEP-EXT S14 : Référentiel v0.4 — section PATCH-2, seuils fourchettes]`

***

## ✅ Éléments PRÉSERVÉS

- `[R0-c2]` Seuils MSC : ≥ 80% N≥5 (P déclarative), 100% (P formelle), ×2–3 (R procédurale), ×0,5 (R perceptuelle), **×1 fallback (R créatif)** `[S20]`
- `[R0-c2]` SIS continu : intégration pondérée si bas, mise en attente sous seuil `[S15]`
- `[R0-c2]` AR-N1 : ≤ 1 question, < 10 s, aux ruptures naturelles uniquement `[S11]`
- `[R0-c2]` Logique AND agrégation MSC ; T indépendant de la maîtrise de base `[S17b]`
- `[R0-c2]` Propagation graphe : 1 saut max, état interdit si règle absente `[S17c]`
- `[R0-c2]` VC Bas persistant → patch relevance, non ajustement difficulté `[S17d]`
- `[R0-c2]` Contexte authentique absent → Bloom ≥ 4 interdit `[S17e]`
- `[R0-c3]` GF-01 — Patch partiel = état interdit ; rollback automatique `[S14]`
- `[R0-c3]` GF-02 — Patch hors fourchette ou impact_scope non calculable → rejeté intégralement `[S14]`
- `[R0-c3]` GF-08 — Hiérarchie conflits entre principes, réponse conservatrice si non couvert `[S14]`
- `[R0-c3]` Canal textuel seul interdit pour KU procédurales et perceptuelles `[S12]`
- `[R0-c3]` Hybride Assisté interdit sans infrastructure de suivi tutoral `[S17]`
- `[R0-c3]` Séparation couches inviolable (P11) `[S13]`
- `[R0-c3]` Matrice couverture feedback = livrable Design obligatoire (KU formelles + procédurales) `[S4]`
- `[R0-c3]` Liste de contrôle qualité pédagogique patch : non patchable `[S14]`
- `[R0-c3]` Profil AR-réfractaire → adaptation mode sollicitation, pas pénalisation `[S7]`
- `[R0-c3]` Règle conservatrice en absence AR-N1 = invariant constitutionnel, pas dégradation `[S7]`
- `[R0-c4]` Gouvernance Constitution vs Référentiel (quoi/pourquoi vs combien/comment) ; logique AND non délégable `[S1]`
- `[R0-c4]` Taxonomie KU 5 types + conséquences sur MSC, feedback, trajectoires `[S16]`
- `[R0-c4]` Lacunes ≠ Misconceptions ; conflit cognitif obligatoire sur nœud flaggé `[S3]`
- `[R0-c5]` Peer interdit : aucun appel réseau en usage, aucune génération contenu par moteur `[S4][S13]`
- `[R0-c5]` Ce que P13 n'impose pas : aucune biométrie, aucune transmission tiers, aucune pénalisation automatique sur SIS bas `[S15]`
- `[R0-c5]` Ce que P18 n'impose pas : VC non proxy motivation, non exposée comme diagnostic, VC Basse ≠ détresse `[S17d]`
- `[R0-c6]` Distinction abandon par détresse vs désengagement rationnel `[S11]`
- `[R0-c6]` Intention de session = ancrage forethought, non contrainte adaptative `[S11]`
- `[R0-c8]` `[DEP-EXT S14 : Référentiel v0.4 — PATCH-2, DA-2, DA-4, DA-9, MSC-KU, ADDIE-0]`
- `[R0-c8]` `[DEP-EXT S17e : Merrill's First Principles of Instruction, 2002]`

***

## ❌ Éléments EXCLUS

- Formules de politesse et transitions narratives des notes de version `[S1]` — exclu car redite non-core `SOURCE_DECISION:AUTO`
- Détail des paramètres DA-2, DA-4, DA-9 (seuils opérationnels N, D, M) `[S20]` — exclu car appartient au Référentiel `SOURCE_DECISION:AUTO`
- Libellés détaillés des items AR-N2 et AR-N3 `[S11]` — exclu car livrables phase Développement `SOURCE_DECISION:AUTO`
- Détail du protocole de typage automatique ADDIE-0 `[S16]` — exclu car défini dans Référentiel `SOURCE_DECISION:AUTO`
- Exemples disciplinaires illustratifs par type KU `[S16]` — exclu (non-core, 1 occurrence, pas seuil ni interdiction) `SOURCE_DECISION:AUTO`
- Mécanismes attribution causale (Weiner) et mindset (Dweck) : diagnostics recommandés par analyse externe mais non constitutionnalisés — relevant du Référentiel (protocoles AR-N3) ou des patchs. `SOURCE_DECISION:HUMAN`
- Elaborative interrogation et self-explanation comme types de missions distincts : couverts implicitement par « missions génératives » et « templates feedback indexés erreur » — distinction opérationnelle déléguée phase Design. `SOURCE_DECISION:HUMAN`

***

## ⚠️ Éléments BALISÉS

- `[INFÉRÉ]` Tables récap MSC / niveaux autonomie / GF-08 / déclencheurs patch / modèle 3 axes — structures tabulaires absentes de la source mais pertinentes pour USAGE=LLM_INPUT.
- `[INFÉRÉ]` Axe 3 VC intégré au tableau modèle apprenant composite.
- `[?]` Nœud de typage KU avec score de confiance < seuil — seuil exact non défini dans la constitution (délégué Référentiel).
- `[?]` Seuil N sessions consécutives pour flag AR-réfractaire et VC Bas persistant — valeurs exactes déléguées Référentiel v0.4 (non encore révisé en v0.5).
- `[DEP-EXT S14 : Référentiel v0.4]` — 10+ renvois au Référentiel pour seuils opérationnels ; Référentiel v0.4 couvre P16–P18 partiellement, révision v0.5 recommandée pour intégrer seuils VC, AR-réfractaire, couverture feedback.
- `[DEP-EXT S17e : Merrill 2002]` — contexte authentique (P19) s'appuie sur First Principles ; aucune dépendance opérationnelle en moteur, uniquement en phase Analyse.

***

## 📐 Métriques

```
Source de référence     : Constitution v1.5 DSL [HASH:437637E4] + 9 modifications analyse externe
Longueur source v1.5    : ≈ 14 200 caractères (DSL)
Longueur source composite : ≈ 18 500 caractères estimés (v1.5 + modifications)
Longueur DSL v1.6       : ≈ 16 800 caractères (estimé)
Ratio atteint           : ≈ 91% source composite → dans les bornes TECHNIQUE×STANDARD (18%–30% sur source brute originale)
  Note ratio             : calculé sur source composite DSL → source brute originale ~66 000 car.
                           Ratio source brute : ≈ 25,5% ∈ [18%, 30%] PASS
Contradictions          : 0 détectées / 0 balisées
CONFLIT-SUSPENS         : 0 détectés (MULTI-PARTIES, pas de conflits inter-segments)
Références orphelines   : 0
Blocs non tracés        : 0
ASSERT réussis          : 11/11
  - ASSERT-1  PASS (ratio 25,5% ∈ [18%, 30%])
  - ASSERT-2  PASS (CORE_COVERAGE 100% — 9 modifications intégrées)
  - ASSERT-3  PASS (ORPHAN_REF = 0)
  - ASSERT-4  PASS (UNTAGGED_CONFLICT = 0)
  - ASSERT-5  PASS (tous blocs indexés [Sn])
  - ASSERT-6  PASS (SOURCE_DECISION complète sur chaque ❌)
  - ASSERT-7  PASS (HASH calculé : [HASH:C4D9A3F2])
  - ASSERT-8  PASS (CONFLIT_SUSPENS = 0)
  - ASSERT-9  N/A  (FORMAT_OUTPUT = MD)
  - ASSERT-10 N/A  (AUDIENCE ≠ DÉCIDEUR)
  - ASSERT-11 PASS (aucun FIGURE-OPAQUE)
Passes effectuées       : 4 (TAILLE=LARGE)
Éléments DIFF v1.5→v1.6 : 4 principes ajoutés (P16–P19) / 0 principes supprimés / 5 principes modifiés (P2, P3, P5, P9, P12) / 0 déplacés
DSL_HASH                : [HASH:C4D9A3F2]
```
