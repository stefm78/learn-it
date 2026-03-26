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
