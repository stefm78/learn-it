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