## Sections ajoutées [S16–S19] `[AJOUTÉ]`

### Section 16 — Valeur-Coût perçue (VC) `[AJOUTÉ]` `[CRITIQUE]`

Définition :

Axe 3 optionnel du modèle apprenant (P5, P18 Constitution v1.6).
Source d'inférence unique : item AR-N2 VC — aucun proxy comportemental autorisé.

États VC :

- VC-Élevée : utilité perçue > coût perçu
- VC-Neutre
- VC-Basse : coût perçu > utilité perçue

Seuil persistance déclencheur patch relevance :

≥ 4 sessions consécutives VC-Basse

Fourchette :

3 ≤ N ≤ 7 sessions

Justification fourchette :

< 3 sessions = signal trop bruit ; > 7 sessions = dérive trop longue sans intervention.

Cible patch :

révision présentation enjeux, missions contextualisation, lien contexte authentique (P19)
**non** ajustement difficulté.

Signal de révision paramètre :

patch relevance sans amélioration VC après 2 cycles → escalade vers révision Phase Analyse
(vérifier adéquation contexte authentique déclaré).

Règles d'intégration moteur :

- VC Basse isolée (< seuil persistance) : aucune action moteur
- VC Basse persistante : flag `vc-bas-persistant` → déclencheur patch uniquement
- VC inconnue (item non renseigné) : aucune inférence autorisée — axe traité comme absent

`[CRITIQUE]`

---

### Section 17 — Profil AR-réfractaire `[AJOUTÉ]` `[CRITIQUE]`

Définition :

Apprenant dont le taux de réponse AR-N1 est systématiquement bas
sur une fenêtre de sessions consécutives.

Seuil de détection :

≥ 5 sessions consécutives sans AR-N1 obtenu

Fourchette :

3 ≤ N ≤ 8 sessions

Justification fourchette :

< 3 sessions = variation normale ; > 8 sessions = dérive trop longue sans réponse.

Conséquence moteur :

Flag `profil-ar-refractaire` → déclencheur patch révision mode sollicitation.

Cible patch :

- révision format AR-N1 (ex. : réduire à 1 icône tap vs texte)
- révision déclencheur (ex. : fin de session vs rupture intra-session)
- **jamais** : augmenter fréquence ou rendre AR-N1 bloquant

Règle conservatrice renforcée :

Tant que profil AR-réfractaire actif ET patch non encore appliqué :
moteur applique scaffolding léger réversible sur toutes décisions Axe 2 (régime activation).
Ce comportement est un **invariant constitutionnel** (P5 Constitution v1.6), pas un mode dégradé.

Signal de révision paramètre :

Après 2 patchs révision sollicitation sans amélioration taux AR-N1 :
considérer niveau autonomie moteur insuffisant → escalade P15 (révision phase Analyse).

`[CRITIQUE]`

---

### Section 18 — Couverture feedback (paramètres opérationnels) `[AJOUTÉ]`

*(Complément de la garde-fou §S4 — couverture matrice feedback)*

Métriques de suivi par univers :

| Métrique | Valeur référence | Fourchette | Signal révision |
|----------|-----------------|------------|-----------------|
| Taux couverture à production | ≥ 70% | 60%–90% | < 60% → pilote restreint |
| Taux hors-taxonomie déclencheur patch | > 15% / 10 sessions | 10%–25% | > seuil sur 3 patchs → revoir taxonomie Design |
| Délai enrichissement après flag | ≤ 1 cycle patch (14 j) | 7–30 j | > 30 j sans patch → alert investigation |

KU concernées : Formelle, Procédurale uniquement.
KU Déclarative : couverture souhaitable mais non obligatoire (patterns d'erreurs bornés).
KU Perceptuelle, Créative : feedback différé ou rubrique — non indexable par taxonomie d'erreurs → exempt.

---

### Section 19 — Propagation graphe (paramètres opérationnels) `[AJOUTÉ]`

*(Implémentation de P17 Constitution v1.6)*

Profondeur propagation :

1 saut de dépendance (arcs sortants directs uniquement)

Ce paramètre est un **invariant constitutionnel** (P17) — non modifiable par patch.

Délai planification vérification prioritaire :

≤ prochaine session disponible de l'apprenant

Fourchette :

0 ≤ délai ≤ 3 sessions

Format tâche diagnostique déclenchée :

Identique au format calibrage par type KU (table §S3).
Durée : version courte (50% de la durée calibrage standard).

Condition de levée du marquage :

Tâche diagnostique réussie (seuil P de référence, 1 occurrence suffit).
Si échec → KU dépendante rétrogradée à son tour (`en consolidation`).

Signal d'alerte :

> 20% des KU du graphe simultanément marquées « vérification prioritaire »
→ investigation systémique (probable révocation MSC en cascade — vérifier intégrité session SIS).
