## Tables récapitulatives [INFÉRÉ]

### Déclencheurs de patch IA `[MODIFIÉ §tables v0.4 vs v0.5]`

| Déclencheur | Seuil | Cible patch |
|-------------|-------|-------------|
| Écart performance | > 20% | paramètres, sous-parcours |
| Biais cohorte | > 15% | révision modèle inférence |
| Révocation MSC | > 30% | recalibration seuils, missions |
| Oscillation concept | ≥ 3 cycles | missions conflit cognitif, graphe |
| Écart équité | dépassement seuil | révision modèle |
| Sessions SIS faibles | > 20% | vérification intégrité |
| Erreurs hors-taxonomie `[AJOUTÉ]` | > 15% sur 10 sessions | enrichissement matrice feedback |
| VC Bas persistant `[AJOUTÉ]` | ≥ 4 sessions consécutives (fourchette 3–7) | révision relevance / contexte authentique |
| Profil AR-réfractaire `[AJOUTÉ]` | ≥ 5 sessions sans AR-N1 (fourchette 3–8) | révision mode sollicitation AR |

`[IMPACT-CRITIQUE]`

---

### Périmètre autorisé des patchs `[MODIFIÉ §tables v0.4 vs v0.5]`

Autorisé :

- ajustement paramètres dans fourchettes
- ajout missions
- recalibration seuils
- enrichissement matrice couverture feedback `[AJOUTÉ]`
- révision mode sollicitation AR-N1 (profil AR-réfractaire) `[AJOUTÉ]`
- révision présentation contexte authentique / relevance (VC Bas) `[AJOUTÉ]`

Interdit :

- modifier composantes MSC
- changer philosophie adaptative
- restructurer graphe principal
- modifier logique d'agrégation AND (P16 Constitution — invariant constitutionnel) `[AJOUTÉ]` `[CRITIQUE]`
- modifier règle de propagation graphe 1-saut (P17 Constitution) `[AJOUTÉ]` `[CRITIQUE]`
- modifier liste de contrôle qualité pédagogique patch (P12 Constitution) `[AJOUTÉ]` `[CRITIQUE]`

`[CRITIQUE]`
