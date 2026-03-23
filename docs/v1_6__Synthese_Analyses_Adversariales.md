# Synthèse des analyses adversariales — Learn-it v1.6
## Éléments à intégrer dans Constitution v1.6 et Référentiel v0.5

`[SOURCE : 4 analyses expertes indépendantes (Perplexity ×3, ChatGPT-4o ×1)]`
`[CIBLES : Constitution_Learn-it_v1_6_DSL.md → v1.7 | referentiel_defaults_v0_5_DSL.md → v0.6]`

---

## Lecture de la synthèse

Chaque point indique :
- **Cible** : Constitution (C) ou Référentiel (R)
- **Consensus** : nombre d'analyses convergentes sur ce point (1–4)
- **Type** : Contradiction · Complétude · Gouvernance · Implémentabilité
- **Priorité** : 🔴 Critique (bloque moteur) · 🟠 Élevée (dégrade silencieusement) · 🟡 Modérée (edge case)

---

## BLOC 1 — Corrections urgentes (contradictions détectées)

### C-1 · Rétrogradation par échec diagnostique vs invariant P17 `[T4/T6 — 3 analyses]`

**Cible** : Constitution P17 + Référentiel §S19 · **Priorité** 🔴 · **Contradiction**

**Problème** : DOC-B §S19 déclare « Si échec [à la tâche diagnostique] → KU dépendante rétrogradée à son tour ». Cette rétrogradation peut elle-même déclencher une propagation sur les dépendances de la KU dépendante, créant une cascade transitive non bornée en violation directe de l'invariant P17 (« 1 saut maximum »).

**Correction Constitution P17** : Ajouter : « La rétrogradation déclenchée par un échec à une tâche diagnostique de propagation constitue un *nouvel événement de rétrogradation indépendant*, soumis aux mêmes règles P17 (1 saut, état interdit si règle absente). Elle ne prolonge pas la propagation courante. »

**Correction Référentiel §S19** : Remplacer « Si échec → KU dépendante rétrogradée » par : « Si échec → flag `rétrogradation-secondaire` sur KU dépendante → nouveau cycle P17 autonome déclenché lors de la session suivante. »

---

### C-2 · Contradiction rétrogradation P16 vs condition révocation §S2 `[T6 — 2 analyses]`

**Cible** : Référentiel §S2 · **Priorité** 🔴 · **Contradiction**

**Problème** : P16 (Constitution) impose une rétrogradation dès qu'une composante MSC est en défaillance. Le Référentiel §S2 définit la révocation sur condition conjonctive (≥ 2 échecs ET délai ≥ seuil_R). Ces deux mécanismes sont confondus alors qu'ils couvrent deux situations distinctes : la **rétrogradation courante** (pendant la phase d'apprentissage) et la **révocation post-maîtrise**. Le moteur ne dispose d'aucune règle pour distinguer les deux cas, créant un comportement non déterministe sur les KU en frontière de seuil P.

**Correction Référentiel §S2** : Créer deux sous-sections explicites :
- `Rétrogradation courante` (P16) : toute composante P, R ou A chute sous seuil → MSC passe à « en consolidation » immédiatement.
- `Révocation post-maîtrise` (deg) : ≥ 2 échecs consécutifs ET délai ≥ seuil_R → perte de maîtrise déclarée. `deg` = condition de révocation, NON composante MSC.

---

### C-3 · Condition interleaving incomplète `[T3 — 3 analyses]`

**Cible** : Référentiel §S3 section 2 · **Priorité** 🔴 · **Contradiction**

**Problème** : Constitution P3 déclare « interleaving contenus après atteinte simultanée P+A ». Le Référentiel §S3 section 2 ne conditionne l'interleaving qu'à « ≥ 2 réussites consécutives ET ≥ 3 tâches distinctes » — condition sur P uniquement, sans A. Un apprenant peut déclencher l'interleaving sans avoir atteint A, en violation du principe constitutionnel.

**Correction Référentiel §S3-2** :
```
Condition d'activation interleaving (contenus) :
≥ 2 réussites consécutives (P)
ET ≥ 3 tâches distinctes
ET composante A ≥ seuil_A sur les KU concernées [AJOUTÉ]

Condition d'activation interleaving (catégories — prioritaire) :
inchangée (P seul suffisant)

Garde-fou supplémentaire [AJOUTÉ] :
Suspendre interleaving si MSC agrégé des KU interleaved < 50% → risque surcharge extrinsèque (Renkl & Atkinson, 2003).
```

---

### C-4 · QA pédagogique patch non déterministe localement `[T1/AXE4 — 2 analyses]`

**Cible** : Constitution P12 + Référentiel §S6 · **Priorité** 🔴 · **Implémentabilité**

**Problème** : GF-02 exige une vérification « locale + déterministe ». Constitution P12 liste une « liste de contrôle qualité pédagogique ». Référentiel §S6 fusionne dans une seule condition de rejet : `paramètres ∈ bornes ET impact_scope calculable ET liste QA satisfaite`. Or la QA pédagogique (alignement Biggs, P10, P19) est une évaluation sémantique non déterministe localement — sa fusion dans GF-02 est une violation de la contrainte déterministe du moteur local.

**Correction Constitution P12** : Distinguer deux niveaux de rejet :
- **Rejet automatique local (GF-02)** : paramètres hors bornes · impact_scope incalculable · type KU absent · attribut obligatoire manquant. Ces critères sont **entièrement déterministes**.
- **Validation QA pédagogique (chaîne serveur)** : critères Biggs, P10, P19 — exécutée avant soumission du patch, hors session. **Non fusionnable avec GF-02.**

**Correction Référentiel §S6** : Rétablir deux conditions séparées dans la vérification locale.

---

## BLOC 2 — Complétude du moteur (états indéfinis)

### C-5 · Acyclicité du graphe non imposée `[EI-3 — 3 analyses]`

**Cible** : Constitution P2 ou P17 · **Priorité** 🔴 · **Complétude**

**Problème** : P17 propage sur arcs sortants directs. Un graphe avec cycles (KU-A → KU-B → KU-A) produit une boucle de marquage mutuel permanente sans résolution. P2 ne déclare pas les cycles comme état interdit. ADDIE-0 valide la « cohérence des arêtes » mais sans interdiction explicite des cycles.

**Correction Constitution P2** : Ajouter : « Le graphe KU est un **DAG (Directed Acyclic Graph)**. Tout cycle détecté lors de la validation ADDIE-0 = état interdit → déploiement bloqué. »

**Correction Constitution P17** : Ajouter règle de résolution de cycle détecté en usage (si graphe corrompu post-déploiement) : « En cas de cycle résiduel détecté : la KU avec le MSC le plus bas est traitée en priorité ; les KU du cycle restant sont gelées (pas de nouvelles missions) jusqu'à résolution par patch. »

---

### C-6 · KU sans type déclaré — comportement moteur indéfini `[EI-1 — 4 analyses]`

**Cible** : Constitution P14 + P12 · **Priorité** 🔴 · **Complétude**

**Problème** : P14 déclare le typage obligatoire mais ne définit pas le comportement moteur si le type est absent en production. Constitution dit « inadéquation silencieuse » — sans état de fallback ni blocage.

**Correction Constitution P14** : Ajouter : « KU avec type absent ou non validé en production = `ku-type-manquant` → mode Hybride bloquant minimum + suspension missions Bloom ≥ 3 jusqu'à validation humaine. »

**Correction Constitution P12** : Ajouter « type KU déclaré et valide » à la liste de contrôle qualité patch comme **critère de rejet automatique local** (GF-02).

---

### C-7 · Comportement moteur durant investigation systémique `[Scénario 3 — 2 analyses]`

**Cible** : Référentiel §S19 · **Priorité** 🟠 · **Complétude**

**Problème** : Le signal d'alerte (> 20% KU simultanément marquées) déclenche une « investigation systémique » dont le comportement moteur pendant la durée n'est pas défini. L'apprenant reçoit-il des sessions normales ? Est-il bloqué ?

**Correction Référentiel §S19** : Ajouter :
```
Comportement moteur durant investigation systémique :
- Mode : missions sur KU non marquées uniquement (mode minimal)
- Délai maximum investigation : 2 sessions avant escalade human_checkpoint obligatoire
- Si délai dépassé sans résolution : passage en mode Hybride bloquant global
```

---

### C-8 · Plancher poids proxy absent `[EI-2 — 3 analyses]`

**Cible** : Référentiel (nouvelle section) + Constitution P9 · **Priorité** 🟠 · **Complétude**

**Problème** : P9 déclare « accumulation discordances AR-N1/proxys → poids proxy révisé à la baisse » sans borne inférieure. Le proxy peut atteindre poids ≈ 0, rendant le moteur aveugle aux signaux comportementaux objectifs. Chez les apprenants avec biais de désirabilité sociale, l'AR prime sur des données biaisées — dégradation silencieuse auto-renforçante.

**Correction Référentiel** (section DA-proxys ou §S3) :
```
Poids proxy minimum : 0.2 — non patchable [CRITIQUE]
Signal de révision : si poids proxy < 0.3 ET indice calibration AR-N3 bas → restauration temporaire poids proxy à 0.4 (1 cycle de 10 sessions)
```

**Correction Constitution P9** : Ajouter : « Le poids accordé aux proxys comportementaux ne peut être réduit en dessous d'un plancher défini par le Référentiel, indépendamment du nombre de discordances cumulées. »

---

### C-9 · Patch rejeté + dérive persistante `[EI-6 — 3 analyses]`

**Cible** : Constitution P12 · **Priorité** 🟠 · **Complétude**

**Problème** : Si un patch est rejeté (GF-02) mais que la dérive qui l'a déclenché persiste au-delà de la fréquence de patch (1/14 j), aucune règle ne force une ré-évaluation. Le moteur peut rester en état de dérive non traitée indéfiniment.

**Correction Constitution P12** : Ajouter : « Si un patch est rejeté ET que le déclencheur qui l'a initié reste actif lors du cycle suivant → **escalade obligatoire** : (a) réexamen du patch avec paramétrage révisé, ou (b) signalement human_checkpoint. Aucune dérive active ne peut dépasser 2 cycles consécutifs sans intervention. »

---

### C-10 · Axe VC activé, item AR-N2 VC structurellement absent `[EI-5 — 2 analyses]`

**Cible** : Référentiel §S16 · **Priorité** 🟠 · **Complétude**

**Problème** : Si l'axe VC est activé mais que l'item VC est systématiquement absent (AR-N2 déjà à 3 items, substitution non applicable), l'axe devient fonctionnellement mort sans déclaration explicite. Règle de désactivation absente.

**Correction Référentiel §S16** : Ajouter :
```
Désactivation automatique axe VC :
Si item VC structurellement absent (AR-N2 saturé sans substitution possible) sur ≥ N sessions → flag `vc-non-observable` → axe VC traité comme absent jusqu'à prochain patch.
Fourchette N : 3–7 sessions (même fourchette que VC persistance).
Désactivation explicite : par patch uniquement.
```

---

## BLOC 3 — Gouvernance Constitution / Référentiel

### C-11 · Règle d'arbitrage AR-N2 VC vs intention session `[T2 — 4 analyses]`

**Cible** : Constitution P9 · **Priorité** 🟠 · **Gouvernance**

**Problème** : Constitution mentionne ≤ 3 items AR-N2 + item VC si axe activé + item intention. Total potentiel = 5 items. Référentiel résout partiellement par substitution conditionnelle (« si VC axe prioritaire déclaré ») — mais le cas VC activé + non prioritaire crée un total de 4 items sans règle. La règle d'arbitrage est une règle invariante de construction du sondage : elle appartient à la Constitution.

**Correction Constitution P9** : Ajouter règle constitutionnelle : « Si l'axe VC est activé ET le total AR-N2 dépasse 3 items, l'item VC remplace **systématiquement** l'item 'intention retour'. L'item intention session et l'item VC sont mutuellement exclusifs dans AR-N2. Indépendamment du statut de priorité déclaré. »

**Correction Référentiel §S3-6** : Supprimer la condition « si VC est axe prioritaire déclaré » — remplacer par la règle constitutionnelle simplifiée.

---

### C-12 · Seuil de vérification maîtrise provisoire héritée `[G6 — 1 analyse]`

**Cible** : Constitution P0 → Référentiel · **Priorité** 🟡 · **Gouvernance**

**Problème** : Constitution P0 dit « vérification prioritaire R et A dans les 3 premières sessions » — seuil opérationnel constitutionnalisé alors qu'il devrait être ajustable selon la densité du graphe et la durée des sessions. De plus, « 3 sessions » ne distingue pas 3 sessions en 3 jours vs 3 sessions en 3 semaines : R ne peut pas être validée en 3 jours.

**Correction Constitution P0** : Remplacer « dans les 3 premières sessions » par « dans les N_vérification_héritée sessions initiales (seuil Référentiel) ET dans un délai calendaire minimum (seuil Référentiel). »

**Correction Référentiel** (nouvelle entrée §S5 + §S3) :
```
N_vérification_héritée : 3 sessions (fourchette 2–5) [AJOUTÉ]
Délai calendaire minimum validation maîtrise héritée : 7 jours (fourchette 5–14 j) [AJOUTÉ]
Justification : R (seuil_R ≥ 3 j) ne peut être validée si les 3 sessions se déroulent en < 3 jours.
```

---

### C-13 · Délai planification propagation potentiellement contournable `[AXE5 — 2 analyses]`

**Cible** : Constitution P17 · **Priorité** 🟡 · **Gouvernance**

**Problème** : Le délai de planification (0–3 sessions, Référentiel §S19) est patchable. Sur un graphe à forte vélocité, 3 sessions de délai peut représenter 3+ semaines — rendant l'invariant 1-saut inopérant. La borne haute interagit avec le principe constitutionnel.

**Correction Constitution P17** : Ajouter : « Le délai de planification de la vérification prioritaire est borné à un maximum de 1 session. Cette borne est un invariant constitutionnel — non modifiable par le Référentiel ni par patch. »

**Correction Référentiel §S19** : Réduire la borne haute de la fourchette à 1 session. Supprimer la mention 0–3 sessions.

---

### C-14 · KU créative + niveau Autonome — combinaison non viable `[Scénario 3 — 2 analyses]`

**Cible** : Constitution P15 · **Priorité** 🟠 · **Complétude**

**Problème** : KU créative couche ≥ 2 en mode Autonome = feedback non formalisable localement (rubrique multi-critères nécessite lecture compréhensive) + matrice couverture feedback non obligatoire + human_checkpoint interdit. Le système est architecturalement aveugle sur le feedback créatif en mode Autonome.

**Correction Constitution P15** : Ajouter : « KU créative de couche ≥ 2 → niveau Autonome interdit. Mode Hybride recommandé minimum obligatoire. »

---

### C-15 · Artefacts générés par patch — définition temporelle absente `[AXE4 — 1 analyse]`

**Cible** : Constitution P11/P12 · **Priorité** 🟡 · **Implémentabilité**

**Problème** : Constitution P11 interdit la génération à la volée, mais P12 autorise les patchs à générer des missions et templates feedback (artefacts). Si le serveur de patch est appelé pendant une session, la limite « zéro LLM continu » devient floue.

**Correction Constitution P12** : Ajouter : « Les artefacts générés par patch (missions, templates feedback) sont produits **hors session**, intégrés dans le moteur local avant la session suivante. Tout appel serveur pendant une session apprenant est interdit. »

---

## BLOC 4 — Nouvelles sections Référentiel à créer

### R-1 · DA-2 — Budget cognitif par type KU `[G3/AXE4 — 3 analyses]`

**Cible** : Référentiel (nouvelle section, après §S4) · **Priorité** 🟠

**Problème** : DA-2 est nommé dans la Constitution (P7) comme mécanisme de prévention surcharge, mais n'existe pas comme table opérationnelle dans le Référentiel. Le proxy temporel 25 min est un garde-fou de dernier recours non différencié par type KU.

**Contenu à créer** :
```
### Section DA-2 — Budget cognitif session par type KU [AJOUTÉ]

| Type KU | Unité de coût | Coût référence | Plafond session |
|---------|--------------|----------------|-----------------|
| Déclarative | item QCM/rappel | 1 | 20 items |
| Formelle | tâche raisonnement | 3 | 7 tâches |
| Procédurale | séquence d'exécution | 5 | 4 séquences |
| Perceptuelle | item classification | 0.5 | 30 items |
| Créative | production contrainte | 8 | 2 productions |

Règle moteur : somme des coûts session ≤ plafond global = 25 min équivalent.
Signal de révision : données terrain sur ≥ 3 univers déployés.
[CRITIQUE — paramètre opérationnel de P7]
```

---

### R-2 · Proxys comportementaux minimaux Axe 2 `[G4/AXE4 — 3 analyses]`

**Cible** : Référentiel (nouvelle section) · **Priorité** 🔴

**Problème** : Le cœur du mécanisme Axe 2 (Régime d'activation) repose sur des proxys laissés entièrement à la phase Analyse sans cadre minimal commun. Le moteur générique n'a aucune règle garantie pour l'Axe 2 hors AR-N1.

**Contenu à créer** :
```
### Section — Proxys comportementaux minimaux garantis (Axe 2) [AJOUTÉ]

Format requis pour tout proxy valide :
(a) Signal observable mesurable (ex. : temps_réponse > 2× médiane)
(b) Seuil numérique déclaré
(c) Statut empirique : validé / hypothèse / invalide
Règle : proxy statut=invalide → exclu du moteur automatiquement.

Proxys minimaux garantis par le Référentiel (indépendants de la phase Analyse) :

| Signal | Seuil référence | Régime suggéré | Fourchette |
|--------|----------------|----------------|------------|
| Temps réponse / tâche | > 2× médiane cohorte | Détresse ou confusion | 1.5×–3× |
| Taux erreurs / session | > 60% | Détresse ou sous-maîtrise | 50%–70% |
| Taux abandon tâche | > 40% session | Détresse ou sous-défi | 30%–50% |
| Temps réflexion | < 30% médiane | Évitement métacognitif | 20%–40% |

Poids proxy minimum : 0.2 — non patchable [CRITIQUE]
Condition changement régime : ≥ 2 proxys franchissent leur seuil.
Clarification [AJOUTÉ] : un AR-N1 isolé est suffisant pour changer de régime, indépendamment des proxys. Les proxys s'appliquent en l'absence d'AR-N1.
```

---

### R-3 · AR-N3 — Fréquence et règle moteur `[G1/AXE3 — 3 analyses]`

**Cible** : Référentiel (nouvelle section) · **Priorité** 🟠

**Problème** : Le mécanisme de détection des biais AR-N1 (désirabilité sociale, profil AR-réfractaire dissimulé) repose sur AR-N3. Sans fréquence ni règle moteur définie, AR-N3 peut ne jamais être déclenché ou ses résultats ignorés.

**Contenu à créer** :
```
### Section — AR-N3 (bilan tendances) [AJOUTÉ]

Fréquence de référence : 1 bilan / 10 sessions
Fourchette : 1/5 sessions ≤ fréq ≤ 1/20 sessions

Seuil indice calibration AR bas :
Discordances AR-N1 / proxys > 40% des sessions sur la fenêtre AR-N3 → indice calibration AR = bas

Règle moteur associée [AJOUTÉ — paramètre orphelin résolu] :
Indice calibration AR bas → réduction temporaire poids AR-N1 de 20% sur 1 cycle AR-N3.
Proxys restaurés à poids_proxy_minimum + 0.2 pendant ce cycle.
Non patchable (protection contre sur-réduction double).

Signal de révision : données terrain dès cohorte ≥ 30 apprenants.
```

---

### R-4 · Contexte authentique P19 — format et contrôle `[G3/T4 — 2 analyses]`

**Cible** : Référentiel (nouvelle section §20) · **Priorité** 🟠

**Problème** : P19 interdit Bloom ≥ 4 en l'absence de contexte authentique, mais le Référentiel ne définit ni le format de ce livrable, ni la condition de validation, ni le contrôle minimal de couverture Bloom.

**Contenu à créer** :
```
### Section 20 — Contexte authentique (paramètres opérationnels P19) [AJOUTÉ]

Attributs obligatoires du livrable contexte authentique :
- domaine : [string — secteur/discipline]
- situation_problème : [string ≤ 150 mots]
- niveau_bloom_cible : [entier 4–6]
- KU_concernées : [liste d'identifiants KU]

Validation : livrable présent ET attributs complets → P19 satisfait.
Contrôle moteur : vérification locale sur attributs (déterministe).

Couverture missions Bloom ≥ 4 [AJOUTÉ] :
Si contexte authentique déclaré pour une KU → ≥ 1 mission Bloom ≥ 4 obligatoire pour cette KU en phase Design.
KU sans mission Bloom ≥ 4 malgré contexte déclaré → flag `bloom-coverage-manquante` → composante T non calculable pour cette KU.

Contexte partiel (certaines KU avec, d'autres sans) [AJOUTÉ] :
Plafonnement Bloom ≥ 4 s'applique **par KU** — non globalement à l'univers.
```

---

### R-5 · Seuil confiance typage KU et comportement de fallback `[AXE5 — 2 analyses]`

**Cible** : Référentiel §S3 (Format calibrage par KU) · **Priorité** 🟠

**Problème** : Le seuil de confiance en dessous duquel la validation humaine est obligatoire n'est défini ni dans la Constitution ni dans le Référentiel.

**Ajout §S3** :
```
Seuil confiance typage KU :
Valeur référence : 0.85 (fourchette 0.75–0.95)
< seuil → validation humaine obligatoire avant déploiement
= absent ou non calculé → comportement C-6 (Hybride bloquant + flag)
```

---

### R-6 · Fourchette multiplicateur R créatif `[Scénario 2/AXE5 — 2 analyses]`

**Cible** : Référentiel §S3-3 · **Priorité** 🟠

**Problème** : R créatif = ×1 fallback sans fourchette définie. GF-02 rejette tout paramètre hors fourchette — une fourchette vide rend tout patch invalide (ou toute valeur valide). Sur cohortes créatives avec taux de révocation élevé, le moteur est paralysé.

**Correction §S3-3** :
```
Multiplicateur R créatif : ×1 (fallback)
Fourchette : ×1 ≤ R_créatif ≤ ×2 [AJOUTÉ]
Signal de révision : N ≥ 30 KU créatives complétées (inchangé)
             OU taux révocation MSC créatif > 40% sur cohorte partielle ≥ 15 apprenants [AJOUTÉ]
```

---

### R-7 · Fourchette fréquence patch `[AXE5 — 1 analyse]`

**Cible** : Référentiel §S5 · **Priorité** 🟡

**Problème** : La fréquence patch 1/14 j n'a pas de fourchette définie. Une réduction à 1/7 j modifierait l'esprit constitutionnel « patchs occasionnels » sans violer formellement un paramètre balisé.

**Ajout §S5** :
```
Fréquence patch : 1 / 14 jours (référence)
Fourchette : 1/7 j ≤ fréq_patch ≤ 1/30 j [AJOUTÉ]
```

**Ajout Constitution S1 (Gouvernance)** : « Occasionnel = maximum 1/7 j. »

---

## BLOC 5 — Risques théoriques (sans blocage moteur immédiat)

Ces points ne créent pas d'état indéfini mais dégradent la fidélité pédagogique :

| # | Point | Cadre théorique | Correction suggérée | Cible | Priorité |
|---|-------|-----------------|---------------------|-------|----------|
| T-1 | Timeout confusion productive absent | D'Mello & Graesser (2012) : confusion bascule en frustration après délai | Ajouter en Référentiel : `timeout_confusion_productive` (ref 3 tâches sans résolution → bascule scaffolding) | R §S3 | 🟡 |
| T-2 | Fenêtre maximale détection VC non documentée | Wigfield & Eccles (2000) : VC prédicteur abandon précoce | Documenter en §S16 : avec fréq AR-N2 minimale (1/3 sessions), détection VC peut atteindre 21 sessions — alerter si délai théorique > 14 sessions | R §S16 | 🟡 |
| T-3 | Interleaving perceptuel + multiplicateur ×0.5 non coordonnés | Kornell & Bjork (2008) | Ajouter règle : multiplicateur ×0.5 perceptuel → fréquence interleaving ajustée proportionnellement | R §S3 | 🟡 |
| T-4 | Indice ARCS-Confidence non relié aux déclencheurs | Keller (ARCS) | Ajouter en Référentiel : sous-estimateur chronique (Axe 1) → déclencheur patch motivationnel distinct des adaptations MSC | R §tables | 🟡 |
| T-5 | Type de tâche non pondéré dans calcul P | PFA — Pavlik et al. (2009) | Ajouter note constitutionnelle : « La diversité des modalités de tâches (rappel libre, reconnaissance, production) contribue à la validité de P — la phase Design doit inclure ≥ 2 modalités distinctes par KU » | C P1 | 🟡 |
| T-6 | Détresse masquée par bonne performance (P élevé, A faible) | Kalyuga (effet inversion expertise) | Ajouter règle Référentiel : P ≥ seuil_P ET A faible persistant > 5 sessions → human_checkpoint diagnostic obligatoire (non pénalisant) | R §tables déclencheurs | 🟠 |

---

## Récapitulatif — Tableau des priorités

| Rang | ID | Description courte | Cible | Type | Priorité |
|------|----|--------------------|-------|------|----------|
| 1 | C-1 | Rétrogradation cascade P17 vs §S19 | C+R | Contradiction | 🔴 |
| 2 | C-4 | QA pédagogique patch — non déterministe | C+R | Implémentabilité | 🔴 |
| 3 | C-5 | Graphe acyclique non imposé | C | Complétude | 🔴 |
| 4 | C-2 | Rétrogradation courante vs révocation post-maîtrise | R | Contradiction | 🔴 |
| 5 | C-3 | Condition interleaving — A absente | R | Contradiction | 🔴 |
| 6 | C-6 | KU sans type — comportement indéfini | C+P12 | Complétude | 🔴 |
| 7 | R-2 | Proxys minimaux Axe 2 absents | R | Complétude | 🔴 |
| 8 | C-11 | Règle AR-N2 VC vs intention — à constitutionnaliser | C | Gouvernance | 🟠 |
| 9 | C-8 | Plancher poids proxy absent | R | Complétude | 🟠 |
| 10 | C-9 | Patch rejeté + dérive persistante sans escalade | C | Complétude | 🟠 |
| 11 | C-14 | KU créative couche ≥ 2 + mode Autonome interdit | C | Complétude | 🟠 |
| 12 | R-3 | AR-N3 sans fréquence ni règle moteur | R | Complétude | 🟠 |
| 13 | C-7 | Comportement durant investigation systémique | R | Complétude | 🟠 |
| 14 | R-4 | Contexte authentique P19 sans paramètre Référentiel | R | Trou couverture | 🟠 |
| 15 | R-6 | Fourchette R créatif absente | R | Gouvernance | 🟠 |
| 16 | C-12 | Seuil vérification héritée à déplacer vers Référentiel | C→R | Gouvernance | 🟡 |
| 17 | C-13 | Délai propagation contournable par patch | C | Gouvernance | 🟡 |
| 18 | R-1 | DA-2 absent du Référentiel | R | Trou couverture | 🟡 |
| 19 | R-5 | Seuil confiance typage KU non défini | R | Trou couverture | 🟡 |
| 20 | C-15 | Artefacts patch — hors session non formalisé | C | Implémentabilité | 🟡 |

---

## Note sur la version cible

Les corrections de rang 1–7 (🔴) sont des **prérequis pour la cohérence déterministe du moteur** et doivent être intégrées avant tout déploiement production.

Les corrections de rang 8–15 (🟠) sont des **améliorations de robustesse** intégrables en v1.7/v0.6.

Les corrections de rang 16–20 (🟡) et les risques théoriques du Bloc 5 sont des **raffinements pédagogiques** déléguables à une révision ultérieure ou à la phase Analyse par déploiement.

---

`[SYNTHÈSE GÉNÉRÉE PAR CLAUDE — CONSOLIDATION DE 4 ANALYSES ADVERSARIALES]`
`[SOURCES : Perplexity (3 passes) + ChatGPT-4o (1 passe) sur Constitution v1.6 + Référentiel v0.5]`
`[HASH SOURCE CONSTITUTION : C4D9A3F2 | HASH SOURCE RÉFÉRENTIEL : B_E7B2D841]`
