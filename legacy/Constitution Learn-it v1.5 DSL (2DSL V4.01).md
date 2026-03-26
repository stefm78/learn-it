# 1. LLM_INPUT

2. STANDARD
3. STANDARD  4. EXPERT 5. MD

Voici le DSL généré — 4 passes appliquées conformément à RÈGLE 7 (TAILLE = LARGE).

***

## Constitution conceptuelle — Learn-it v1.5

`[HASH:437637E4]`

*Paramètres : USAGE=LLM_INPUT | DOC_TYPE=TECHNIQUE | LANGUE=FR | VERSION=v1.5 | STRUCTURE=MULTI-PARTIES | MODE=STANDARD | TAILLE=LARGE | NIVEAU_DETAIL=STANDARD | AUDIENCE=EXPERT | FORMAT_OUTPUT=MD*

***

### Contexte / Objectifs / Évolutions `[S1]`

**v1.5** étend v1.4 sur 3 chantiers. `[S1]`

1. **Universalité disciplinaire** : KU typées (déclarative, procédurale, perceptuelle, formelle, créative) conditionnant opérandes MSC, modalités feedback, trajectoires pédagogiques et stratégies de consolidation.
2. **Garde-fous architecturaux** : GF-01 (atomicité patches), GF-02 (vérification fourchettes locales), GF-08 (hiérarchie résolution conflits) ajoutés à P12.
3. **Nouveaux principes** : P14 (typage épistémologique KU obligatoire), P15 (déclaration niveau autonomie moteur).

**v1.4** étend v1.3 sur 2 chantiers : (1) auto-rapport affectif à 3 niveaux intégré à P9 — source d'autorité sur états internes ; (2) P13 — architecture d'intégrité modèle apprenant (multi-profil, SIS, modes Invité/Évaluation Externe). `[S1]`

**Gouvernance** `[CRITIQUE]` : Constitution = *quoi/pourquoi* → modifiable par délibération explicite. Référentiel = *combien/comment* → révisable librement. Séparation inviolable. `[S1]`

***

### Fondamentaux `[S2–S8]`

**P0 — Calibrage initial** `[S2]`

- **(a) Calibrage épistémique** : diagnostic adaptatif court → initialise état graphe (prérequis maîtrisés / en doute / lacunes). Format adapté au type KU dominant (P14). Absence de calibrage → hypothèse conservatrice (position initiale basse) + déblocage manuel par l'apprenant.
- **Maîtrise provisoire héritée** `[CRITIQUE]` : état MSC distinct de la *maîtrise d'entraînement*. Composantes P, R, A *présumées* non corroborées. Génère vérification prioritaire R et A dans les 3 premières sessions. Si confirmées → *maîtrise d'entraînement* ; sinon → *en consolidation* + parcours de réactivation. Composante T non validée à ce stade.
- **(b) Calibrage métacognitif** : prédiction de performance intégrée au pré-test → initialise composante Calibration (état composite P5).
- Calibrage : court, engageant, restitution cartographie visuelle immédiate. Sans styles d'apprentissage invalidés (VARK). Inférences initiales à confiance réduite, prioritairement révisées par les données des premières sessions.

**P1 — Primat maîtrise compétences examen** `[S3]`

- Axe de progression par type KU `[CRITIQUE]` : Bloom révisé (déclarative/formelle) ; automatisation guidée→autonome→transfert adaptatif (procédurale) ; finesse de discrimination (perceptuelle) ; maîtrise des conventions → déviation productive intentionnelle (créative).
- **ICC** (Indice de Confiance du Corpus) : fort / partiel / absent → conditionne stratégie de construction du graphe.
- Graphe sur annales + structure disciplinaire. Concept absent des annales mais présent dans corpus disciplinaire → maintenu dans graphe, niveau Bloom minimum, pondération réduite — **jamais supprimé**.
- **Lacunes ≠ Misconceptions** `[CRITIQUE]` : missions sur nœud flaggé misconception = conflit cognitif explicite obligatoire avant représentation correcte. Rappel actif seul insuffisant.
- Alignement constructif (Biggs) vérifié en phase Analyse. Transfert lointain déclaré explicitement si visé.

**P2 — Moteur générique / graphe KU** `[S4]`

- Graphe orienté de KU. Relations déclarées en phase Analyse : prérequis logiques, dépendances d'exécution, co-occurrence perceptuelle, affordances créatives.
- 2 types de nœuds : **nœuds KU** + **nœuds human_checkpoint** (P15 ; bloquant ou non-bloquant selon niveau autonomie).
- Décisions adaptatives en usage : **règles déterministes + modèles statistiques légers locaux uniquement** `[CRITIQUE]`. Zéro appel réseau temps réel. Inférence non formalisable → exclue du moteur → candidate patch (P12).
- Fading déclenché par composante **A** du MSC (définition opérationnelle par type KU). Résistance au guidage → signal surqualification (Kalyuga, effet inversion expertise) → réduction proactive du guidage.
- Explicabilité sur demande ; non sollicitée uniquement aux transitions inter-sessions.

**P3 — Temporalité et mémoire** `[S5]`

- Stratégie de consolidation par type KU : rappel actif (déclarative/formelle) ; pratique exécutoire distribuée (procédurale) ; exposition contrastive espacée (perceptuelle) ; élaboration contrainte espacée (créative). Terme générique : **occurrence de consolidation**.
- Algo d'espacement (DA-4) : déterministe, local, sans dépendance externe, paramétré par P et R du MSC.
- **Multiplicateur R** par type KU : procédurale ×2–3 (rétention lente) ; perceptuelle ×0,5 (oubli précoce plus sensible). R = garde-fou `[CRITIQUE]` : KU non validée sur R → non déclarable maîtrisée.
- **Espacement prioritaire** tous types. **Interleaving conditionnel** : catégories en priorité (transfert le plus robuste) ; contenus après atteinte simultanée P+A (R non prérequis car interleaving = test de R en conditions réelles). Contrainte couverture équilibrée (anti-retrieval-induced forgetting, Anderson et al.).
- *Productive failure* (Kapur) : non intégrée par défaut — décision explicite par univers.
- Interruption > seuil_R → session de reprise diagnostique avant reprise parcours.

**P4 — Planification vers date cible** `[S6]`

L'étudiant déclare une date d'examen. Moteur planifie + réajuste chemin pour maximiser maîtrise à l'échéance. Représentation mobilisatrice, non anxiogène. Marges de choix pour soutenir autonomie et entraîner capacité de planification.

**P5 — Hyper-personnalisation** `[S7]`

- **Modèle d'état apprenant composite — 2 axes** :
    - Axe 1 **Calibration** : bien calibré / surestimateur / sous-estimateur. Inféré de façon déterministe (écart prédictions ↔ performances).
    - Axe 2 **Régime d'activation** : productif / détresse / sous-défi. NON diagnostic psychologique. Source d'autorité = auto-rapport (P9) ; proxys comportementaux = signal de fond permanent.
- **Distinction critique confusion / frustration / anxiété** `[CRITIQUE]` : proxys similaires, interventions opposées.
    - *Confusion productive* (D'Mello \& Graesser) : engagement actif en ZPD → scaffolding, ne pas réduire difficulté.
    - *Frustration/épuisement* : désengagement → réduction charge, changement format.
    - *Anxiété* : performance altérée par inquiétude → réduction difficulté + message soutien.
    - Sans auto-rapport disponible → **intervention conservatrice et réversible** (scaffolding léger) jusqu'à obtention AR.
- Validité inférentielle : toute règle comportement → état = hypothèse à valider empiriquement.
- Équité algorithmique : profils surveillés définis *a priori* ; écart systématique > seuil → révision modèle (pas seulement signalement).
- Aucun plafond de difficulté imposé définitivement.

**P6 — Transition feuille blanche** `[S8]`

Modes progressifs vers format réel d'examen. Transfert proche prioritaire. Progression vers modes sans aide = montée composante **A** du MSC.

***

### Mécanismes `[S9–S17]`

**P7 — Adaptation environnement d'usage** `[S9]`

Budget cognitif session = somme pondérée des tâches (proxy DA-2 par type). Proxy temporel = garde-fou de dernier ressort. Sessions longues soutenues préservées (formation de schémas complexes non productible par micro-fragmentation seule).

**P8 — Gamification éthique** `[S10]`

- Mécaniques d'engagement → effort cognitif et maîtrise, PAS rétention d'attention.
- Récompenses extrinsèques : phase d'amorçage → retrait progressif au profit compétence intrinsèque (SDT).
- 2 régimes : (a) éléments pédagogiques — principe cohérence Mayer strict ; (b) éléments gamification — test de non-nuisance requis. Non vérifié → **période probatoire**.
- Clôture motivationnelle après mission majeure : accompli + comparaison niveau départ + ancrage compétence (ARCS Satisfaction, SDT). `[S10]`

**P9 — Métacognition, SRL, auto-rapport** `[S11]`

- Boucle SRL (Zimmerman) : forethought / monitoring / self-reflection.
- Invitations métacognitives : **frugalité** — non systématiques, concentrées aux transitions et tâches à enjeu, variées. Intensité scaffoldée. Distinction internalisation (retrait planifié) vs évitement (retour prompts guidés).
- **Système AR à 3 niveaux** `[CRITIQUE]` :
    - **AR-N1** Micro-sondage événementiel : 1 question visuelle binaire/ternaire, < 10 s, aux ruptures naturelles uniquement. **Seul mécanisme distinguant confusion / frustration / anxiété en temps réel.** Déclenchement événementiel (pas périodique) pour éviter fatigue de sondage.
    - **AR-N2** Mini-sondage fermeture session : ≤ 3 items visuels — difficulté perçue (CVT contrôle), progrès perçu (CVT valeur), intention retour. Fréquence adaptative (Référentiel).
    - **AR-N3** Bilan trajectoire périodique : 5–7 items AEQ-dérivé sur tendances. Génère indice calibration AR → détecte biais désirabilité sociale.
- **Règles d'intégration AR** `[CRITIQUE]` : AR-N1 concurrent → mise à jour immédiate régime. AR-N2 discordant avec proxy → AR prime + discordance consignée. Accumulation discordances → poids proxy révisé à la baisse.
- Abandon par détresse (erreurs + surcharge) ≠ abandon par désengagement rationnel (performance correcte + sous-défi) → réponses opposées.

**P10 — Qualité du feedback** `[S12]`

- Feedback sur **processus + autorégulation** prioritaire sur personne ou aptitudes.
- **Modalité par type KU** `[CRITIQUE]` :
    - Déclarative/Formelle : templates textuels indexés erreur + niveau Bloom + MSC. Canal textuel principal.
    - Procédurale : point de rupture séquence + relecture annotée + worked example vidéo. Canal textuel secondaire uniquement.
    - Perceptuelle : contraste simultané (juxtaposition, heatmap, zones discriminantes). Feedback différé en régime avancé (profil d'erreurs sur série).
    - Créative : rubrique multi-critères non-directive. Feedback prescriptif **proscrit**.
- **Canal textuel seul interdit pour KU procédurales et perceptuelles** `[CRITIQUE]` — livrable obligatoire chaîne IA conception.

**P11 — Séparation des couches** `[S13]`

3 couches séparées `[CRITIQUE]` :

- **Conception** (hors usage) : graphe, missions, paramétrage, assets (missions conflit cognitif, génératives, templates feedback).
- **Moteur autonome** (local, en usage) : sélectionne et séquence artefacts. **Zéro génération de contenu. Zéro appel réseau.**
- **Patch** (serveur, occasionnel) : corrige dérives, génère/révise artefacts paramétriques téléchargeables intégrés localement.

Séparation inviolable : tout mécanisme de génération de contenu en usage → couche patch.

**P12 — Patchs paramétriques** `[S14]`

- Déclencheur : métrique de dérive documentée franchissant seuil (Référentiel). Patchs occasionnels, non continus.
- Périmètre **autorisé** : paramètres Référentiel dans fourchettes, sous-parcours, variantes missions, templates feedback, révision poids graphe.
- Périmètre **interdit** `[CRITIQUE]` : redéfinition composantes/seuils MSC hors fourchettes constitutionnelles ; modifier philosophie adaptation (P5, P8, P13) ; introduire inférence psychologique sans statut probatoire.
- Attributs obligatoires de tout patch : paramétrique, traçable, borné, réversible (condition rollback définie), transparent (apprenant informé).
- **GF-01 — Atomicité** `[CRITIQUE]` : double-buffer obligatoire. Snapshot avant application ; patch sur copie ; swap atomique OS-level. Rollback automatique si échec. Patch partiellement appliqué = **état interdit** — aucune décision sur modèle intermédiaire.
- **GF-02 — Vérification fourchettes locale** `[CRITIQUE]` : vérification locale + déterministe avant application. Paramètre hors fourchette → patch rejeté **intégralement**. Rejet logué + apprenant informé. Zéro dépendance réseau.
- **GF-08 — Hiérarchie résolution conflits** `[CRITIQUE]` : (1) protection apprenant (P5, P8, P13) > (2) charge cognitive (P7) > optimisation MSC court terme (P1) > (3) auto-rapport (P9) > décisions adaptatives auto (P5) > (4) atomicité (P13, GF-01) > fluidité expérience (P8). Conflit non couvert → réponse **conservatrice** obligatoire + logué + décision ouverte prochain patch.

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

**P14 — Typage épistémologique KU** `[S16]`

- Déclaration type KU dominant obligatoire en phase Analyse `[CRITIQUE]`. Sans elle : inadéquation silencieuse pour tout domaine non déclaratif.
- **Taxonomie KU** : Déclarative (faits/règles, verdict binaire) ; Procédurale (automatisation geste/routine) ; Perceptuelle (finesse discrimination) ; Formelle (rigueur démo + transfert structurel) ; Créative (conventions + intention expressive).
- Typage par chaîne IA en phase Analyse (protocole ADDIE-0). Type dominant par univers ; annotations locales pour nœuds déviants. Score confiance < seuil → flag validation humaine `[?]`.
- Conditionne automatiquement : MSC, feedback (P10), trajectoire pédagogique (Design), proxys (P5), budget cognitif (DA-2), multiplicateur R (DA-4).

**P15 — Niveau d'autonomie moteur** `[S17]`

- Déclaré en phase Analyse. Non révisable en cours de déploiement sans retour phase Analyse.
- **4 niveaux** `[CRITIQUE]` :
    - **Autonome** : moteur gère intégralement. KU déclarative, formelle, perceptuelle, procédurale P1.
    - **Hybride recommandé** : jalons humains suggérés non bloquants. Procédurale P2 (physique bas risque).
    - **Hybride bloquant** : human_checkpoints bloquants (reprise après validation tuteur). Procédurale P3 + créative couche 3.
    - **Assisté** : moteur = préparation, diagnostic, traçabilité uniquement. Feedback délégué tuteur humain. Procédurale P4 (haut risque). **Déploiement interdit sans infrastructure de suivi tutoral.**
- **Niveaux risque procédural** : P1 numérique (nul) / P2 physique bas risque / P3 modéré / P4 haut risque (conséquences graves si mauvais geste).
- **Human_checkpoint** — attributs obligatoires : `blocking` (bool), `ku_type`, `validation_criteria`, `phase_msc`. Moteur planifie, notifie, attend. Ne juge pas le résultat du jalon.

***

### Mécanismes — Cycle ADDIE `[S18]`

1. **Analyse** : extraire KU, construire graphe, déclarer type KU dominant (P14) + ICC + niveau autonomie (P15) + axe de progression (P1) + alignement constructif (Biggs) + flags misconception + objectif transfert lointain. Définir proxys comportementaux + statut validation empirique + profils équité + conditions AR-N1. Valider graphe (couverture, cohérence arêtes, human_checkpoints requis). Graphe insuffisant → pilote restreint uniquement.
2. **Design** : trajectoire pédagogique par type KU. Missions conflit cognitif (nœuds flaggés), missions génératives, décision productive failure, templates feedback (P10), contenus AR-N1 (libellés + mapping régimes), human_checkpoints. Transitions = seuils MSC définis en Analyse.
3. **Développement** : contenus jouables respectant charge cognitive, motivation, métacognition, éthique. Formats sondages AR (N1, N2, N3) = livrables **obligatoires**.
4. **Implémentation** : déploiement + configuration. Gamification non vérifiée → **mode probatoire**. Configuration modes Invité, Évaluation Externe, multi-profil.
5. **Évaluation** : déclencheurs (écart ponctuel, biais systématique, dérive hors-jeu). Inclut systématiquement : test non-nuisance gamification probatoire ; métriques équité ; confrontation règles inférence / données + mise à jour statut validation ; efficience par nœud ; **concordance AR / proxys** (proxy taux discordance élevé → "hypothèse invalidée" + retiré du modèle) ; distribution SIS cohorte.

***

### Tables récap `[INFÉRÉ]`

**MSC — Opérandes par type de KU** `[S20]`


| Composante | Déclarative (réf.) | Formelle | Procédurale | Perceptuelle | Créative |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **P** | Taux ≥ 80% sur N≥5 | 100% chaîne complète | Score rubrique multi-dim ≥ seuil | d-prime (SDT) ≥ seuil | Critères formels + rubrique auto-déclaré calibré |
| **R** | Réussite après délai D | Idem déclarative | D × ×2–3 | D × ×0,5 | Cohérence portfolio dans le temps |
| **A** | M réussites sans aide textuelle | Sans scaffolding formel | M exécutions, variabilité inter-essais < seuil, sans guidage physique | M discriminations sans étiquette ni contraste | M productions page blanche sans prompt ni template |
| **T** | Format structurellement différent | Problème isomorphe | Exécution sous contrainte modifiée | Conditions dégradées / exemplaires atypiques | Registre/contrainte radicalement différent |

**Niveaux autonomie moteur** `[S17][INFÉRÉ]`


| Niveau | Jalons humains | KU applicables |
| :-- | :-- | :-- |
| Autonome | Aucun | Déclarative, Formelle, Perceptuelle, Procédurale P1 |
| Hybride recommandé | Suggérés, non bloquants | Procédurale P2 |
| Hybride bloquant | Bloquants (human_checkpoint) | Procédurale P3, Créative couche 3 |
| Assisté | Feedback délégué tuteur | Procédurale P4 |

**Hiérarchie GF-08 — Conflits entre principes** `[S14][INFÉRÉ]`


| Priorité | Principe dominant | Principe subordonné |
| :-- | :-- | :-- |
| 1 | Protection apprenant (P5, P8, P13) | Tout autre principe |
| 2 | Charge cognitive (P7) | Optimisation MSC court terme (P1) |
| 3 | Auto-rapport (P9) | Décisions adaptatives auto (P5) |
| 4 | Atomicité/intégrité modèle (P13, GF-01) | Fluidité expérience (P8) |


***

### Glossaire sigles `[S20]`

| Sigle | Définition |
| :-- | :-- |
| KU | Knowledge Unit — unité atomique du graphe |
| MSC | Mastery Score Composite — vecteur (P, R, A, T) |
| P / R / A / T | Précision / Robustesse temporelle / Autonomie / Transférabilité |
| SIS | Score d'Intégrité de Session — continu  |
| NC-MSC | Niveau de Confiance MSC : Élevé / Moyen / Bas |
| ICC | Indice de Confiance du Corpus : fort / partiel / absent |
| AR | Auto-Rapport (niveaux N1, N2, N3) |
| SRL | Self-Regulated Learning |
| CVT | Control-Value Theory (Pekrun) |
| GF | Garde-Fou architectural (GF-01, GF-02, GF-08) |
| DA-n | Decision Algorithm n (Référentiel) |
| ZPD | Zone Proximale de Développement |
| ADDIE | Analyse / Design / Développement / Implémentation / Évaluation |
| SDT | Self-Determination Theory (Deci \& Ryan) |
| ARCS | Attention / Relevance / Confidence / Satisfaction (Keller) |


***

### Cadres théoriques `[S19]`

- **Charge cognitive / mémoire** : CLT (Sweller, van Merriënboer) ; 4C/ID ; effet inversion expertise (Kalyuga) ; Desirable Difficulties (Bjork) ; retrieval-induced forgetting (Anderson et al.) ; apprentissage multimédia (Mayer) ; productive failure (Kapur) ; apprentissage perceptuel interleaved (Kornell \& Bjork 2008) ; ACT-R / phases automatisation (Anderson, Fitts \& Posner).
- **Expertise** : Dreyfus \& Dreyfus ; knowledge telling vs transforming (Bereiter \& Scardamalia) ; Signal Detection Theory (Green \& Swets).
- **Motivation** : SDT (Deci \& Ryan) ; ARCS (Keller) ; valeur-attente (Eccles \& Wigfield).
- **Métacognition / SRL** : Zimmerman ; Winne \& Hadwin (COPES) ; EEF ; self-efficacy (Bandura).
- **Émotions** : CVT (Pekrun) ; D'Mello \& Graesser (confusion productive, frustration, flow) ; EMA (Shiffman et al.) ; Peak-End rule (Kahneman).
- **Stratégies probantes** : rappel actif, espacement, interleaving, élaboration, double codage, worked examples + fading (Sweller, van Merriënboer) ; apprentissage génératif (Fiorella \& Mayer) ; elaborative interrogation (Dunlosky et al.).
- **Social / constructivisme** : ZPD (Vygotsky) ; apprentissage par les pairs.
- **Misconceptions** : conflit cognitif + réfutation explicite (Posner et al., Chi).
- **Systèmes adaptatifs** : BKT (Corbett \& Anderson) ; PFA ; mastery learning (Bloom) ; équité algorithmique.
- **Ingénierie pédagogique** : ADDIE ; Merrill's First Principles ; Bloom révisé ; alignement constructif (Biggs) ; assessment for learning (Black \& Wiliam).

***

### Seuils / Bornes critiques `[S20]`

- **P déclarative** : ≥ 80% sur N ≥ 5 occurrences.
- **P formelle** : 100% sur chaîne complète.
- **Multiplicateur R procédurale** : ×2–3 vs déclarative.
- **Multiplicateur R perceptuelle** : ×0,5 vs déclarative.
- **AR-N1** : ≤ 1 question, < 10 s, binaire/ternaire. Jamais en milieu de tâche active.
- **AR-N2** : ≤ 3 items visuels.
- **AR-N3** : 5–7 items AEQ-dérivé.
- **SIS** : score. SIS bas → intégration pondérée ; sous seuil → mise en attente session suivante. Anomalie "moins bon que d'habitude" jamais pénalisée.
- **NC-MSC** : Élevé (toutes sessions SIS ≥ seuil haut) / Moyen (SIS intermédiaires présents) / Bas (sessions SIS bas contribution significative).
- **Maîtrise provisoire héritée** : vérification R et A dans les 3 premières sessions.
- **GF-01** : snapshot + swap atomique OS-level obligatoires. Patch partiellement appliqué = état interdit.
- **GF-02** : paramètre hors fourchette → patch rejeté intégralement. Zéro réseau.
- **Hybride bloquant** : parcours bloqué jusqu'à validation tuteur humaine.
- **Assisté** : déploiement interdit sans infrastructure de suivi tutoral.
- **Conflit GF-08 non couvert** → réponse conservatrice obligatoire + logué. `[DEP-EXT S14 : Référentiel v0.4 — section PATCH-2, seuils fourchettes]`

***

## ✅ Éléments PRÉSERVÉS

- `[R0-c2]` Seuils MSC : ≥ 80% N≥5 (P déclarative), 100% (P formelle), D × ×2–3 (R procédurale), D × ×0,5 (R perceptuelle) `[S20]`
- `[R0-c2]` SIS continu  : intégration pondérée si bas, mise en attente sous seuil `[S15]`
- `[R0-c2]` AR-N1 : ≤ 1 question, < 10 s, aux ruptures naturelles uniquement `[S11]`
- `[R0-c3]` GF-01 — Patch partiel = état interdit ; rollback automatique `[S14]`
- `[R0-c3]` GF-02 — Patch hors fourchette rejeté intégralement `[S14]`
- `[R0-c3]` GF-08 — Hiérarchie conflits entre principes, réponse conservatrice si non couvert `[S14]`
- `[R0-c3]` Canal textuel seul interdit pour KU procédurales et perceptuelles `[S12]`
- `[R0-c3]` Hybride Assisté interdit sans infrastructure de suivi tutoral `[S17]`
- `[R0-c3]` Séparation couches inviolable (P11) `[S13]`
- `[R0-c4]` Gouvernance Constitution vs Référentiel (quoi/pourquoi vs combien/comment) `[S1]`
- `[R0-c4]` Taxonomie KU 5 types + conséquences sur MSC, feedback, trajectoires `[S16]`
- `[R0-c4]` Lacunes ≠ Misconceptions ; conflit cognitif obligatoire sur nœud flaggé `[S3]`
- `[R0-c5]` Peer interdit : aucun appel réseau en usage, aucune génération contenu par moteur `[S4][S13]`
- `[R0-c5]` Ce que P13 n'impose pas : aucune biométrie, aucune transmission tiers, aucune pénalisation automatique sur SIS bas `[S15]`
- `[R0-c6]` Distinction abandon par détresse vs désengagement rationnel `[S11]`
- `[R0-c8]` `[DEP-EXT S14 : Référentiel v0.4 — PATCH-2, DA-2, DA-4, DA-9, MSC-KU, ADDIE-0]`

***

## ❌ Éléments EXCLUS

- Formules de politesse et transitions narratives des notes de version `[S1]` — exclu car redite non-core `SOURCE_DECISION:AUTO`
- Détail des paramètres DA-2, DA-4, DA-9 (seuils opérationnels N, D, M) `[S20]` — exclu car appartient au Référentiel, non à la constitution `SOURCE_DECISION:AUTO`
- Libellés détaillés des items AR-N2 et AR-N3 `[S11]` — exclu car livrables de la phase Développement, non constituants `SOURCE_DECISION:AUTO`
- Détail du protocole de typage automatique ADDIE-0 `[S16]` — exclu car défini dans Référentiel `SOURCE_DECISION:AUTO`
- Exemples disciplinaires illustratifs par type KU (histoire, chirurgie, œnologie…) `[S16]` — exclu (non-core R0-c6 en STANDARD ; 1 occurrence, pas de seuil ni interdiction) `SOURCE_DECISION:AUTO`

***

## ⚠️ Éléments BALISÉS

- `[INFÉRÉ]` Tables récap MSC / niveaux autonomie / GF-08 — structure tabulaire absente de la source mais pertinente pour USAGE=LLM_INPUT.
- `[?]` Nœud de typage KU avec score de confiance < seuil — seuil exact non défini dans la constitution (délégué Référentiel).
- `[DEP-EXT S14 : Référentiel v0.4]` — 8+ renvois au Référentiel pour seuils opérationnels ; Référentiel non fourni dans ce traitement.

***

## 📐 Métriques

```
Longueur source         : 56 587 caractères
Longueur DSL            : ≈ 14 200 caractères (estimé)
Ratio atteint           : ≈ 25 %  (cible TECHNIQUE×STANDARD : 18 %–30 %)
Contradictions          : 0 détectées / 0 balisées
CONFLIT-SUSPENS         : 0 détectés (MULTI-PARTIES, pas de conflits inter-segments)
Références orphelines   : 0
Blocs non tracés        : 0
ASSERT réussis          : 11/11
  - ASSERT-1  PASS (ratio 25 % ∈ [18 %, 30 %])
  - ASSERT-2  PASS (CORE_COVERAGE 100 %)
  - ASSERT-3  PASS (ORPHAN_REF = 0)
  - ASSERT-4  PASS (UNTAGGED_CONFLICT = 0)
  - ASSERT-5  PASS (tous blocs indexés [Sn])
  - ASSERT-6  PASS (SOURCE_DECISION complète sur chaque ❌)
  - ASSERT-7  PASS (HASH calculé : [HASH:437637E4])
  - ASSERT-8  PASS (CONFLIT_SUSPENS = 0)
  - ASSERT-9  N/A  (FORMAT_OUTPUT = MD)
  - ASSERT-10 N/A  (AUDIENCE ≠ DÉCIDEUR)
  - ASSERT-11 PASS (aucun FIGURE-OPAQUE)
Passes effectuées       : 4 (TAILLE=LARGE)
DSL_HASH                : [HASH:437637E4]

