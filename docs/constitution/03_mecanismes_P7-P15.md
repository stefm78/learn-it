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
