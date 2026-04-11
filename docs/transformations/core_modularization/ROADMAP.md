# Roadmap — transformation modularisation des Core

## But

Faire évoluer le repo depuis un régime principalement monolithique de Core gouvernés vers un régime plus maniable :

- **sources modulaires gouvernées** ;
- **bundle canonique compilé** ;
- **projections dérivées validées** ;
- **pipelines scope-aware** capables de travailler sur des sous-ensembles bornés ;
- **intégration globale centralisée** avant release et promotion.

---

## Phases

| Phase | Intitulé | Statut initial | Livrables attendus | Critère de sortie |
|---|---|---:|---|---|
| P0 | Bootstrap du chantier | DONE | branche dédiée, README, roadmap, status, worklog | chantier reprenable sans contexte implicite |
| P1 | Modèle cible documentaire | TODO | structure cible des sources modulaires, règles de compilation, frontières canon / projection | design cible validé à haut niveau |
| P2 | Artefacts de scope pipeline | TODO | `scope_manifest`, `impact_bundle`, `integration_gate` | contrat minimal des runs bornés défini |
| P3 | Adaptation pipeline Constitution | TODO | pipeline `constitution` capable de traiter un scope borné tout en gardant une validation globale | premier cycle de challenge borné exécutable |
| P4 | Adaptation pipeline Platform Factory | TODO | pipeline `platform_factory` scope-aware sur ses artefacts gouvernés | premier cycle factory borné exécutable |
| P5 | Matérialisation/compilation canonique | TODO | outillage de compilation déterministe et contrôles croisés | bundle canonique recompilable et vérifiable |
| P6 | Intégration globale et pilote | TODO | gate d'intégration, test sur un vrai sous-ensemble, règles de promotion maintenues | premier pilote complet validé |

---

## Séquence recommandée

### P0 — Bootstrap du chantier
Déjà posé par ce commit initial.

### P1 — Modèle cible documentaire
À définir explicitement :
- où vivent les **sources modulaires** ;
- quels artefacts restent publiés dans `docs/cores/current/` ;
- ce qui est **canonique**, **constatif**, **dérivé**, **opératoire** ;
- quelle granularité modulaire est retenue au départ.

Livrables recommandés :
- note d'architecture de transformation ;
- première proposition d'arborescence cible ;
- règles de nommage et d'assemblage.

### P2 — Artefacts de scope pipeline
Définir le strict nécessaire pour qu'un run local soit borné et traçable.

Livrables minimaux :
- `scope_manifest` : périmètre autorisé du run ;
- `impact_bundle` : zone modifiée + voisinage logique ;
- `integration_gate` : contrôles globaux à rejouer avant release/promotion.

### P3 — Adaptation pipeline Constitution
Faire évoluer le pipeline `constitution` sans le casser.

Approche recommandée :
- ne pas dupliquer le pipeline ;
- rendre le pipeline capable de recevoir un scope explicite ;
- conserver les stages existants autant que possible ;
- ajouter un contrôle d'intégration globale avant release.

### P4 — Adaptation pipeline Platform Factory
Même logique que pour `constitution`, en gardant la séparation :
- artefact prescriptif ;
- artefact constatif.

Attention particulière :
- ne pas casser la doctrine déjà posée sur les `validated_derived_execution_projections` ;
- garder l'alignement avec la contrainte multi-IA.

### P5 — Matérialisation/compilation canonique
Poser le mécanisme permettant de :
- lire les sources modulaires ;
- vérifier unicité des IDs, dépendances, références ;
- produire le bundle canonique compilé ;
- calculer une empreinte stable ;
- préparer des projections dérivées régénérables.

### P6 — Intégration globale et pilote
Choisir un premier sous-ensemble réel, puis exécuter :
- challenge borné ;
- arbitrage borné ;
- patch borné ;
- validation locale ;
- intégration globale ;
- release/promotion selon règles existantes.

---

## Garde-fous

1. **Ne pas multiplier les pipelines sans nécessité.**
   Le principe directeur est : même pipeline, scopes différents.

2. **Ne pas multiplier les prompts sans changement de nature du travail.**
   Le principe directeur est : même famille de prompts, contexte de scope injecté.

3. **Ne pas ouvrir le parallélisme jusqu'à la promotion finale.**
   Le parallélisme est autorisé pour les travaux locaux ; la promotion reste centralisée.

4. **Ne pas basculer trop tôt vers une modularisation effective.**
   D'abord le design cible et le protocole de contrôle, ensuite le déplacement des artefacts.

5. **Conserver une voie de repli.**
   Tant que le nouveau régime n'est pas validé, les artefacts actuels et les pipelines actuels restent exploitables.

---

## Définition du “strict nécessaire”

Pour cette transformation, le strict nécessaire n'est pas une refonte totale.
C'est l'ensemble minimal permettant de sécuriser la suite :

- un suivi explicite ;
- une feuille de route ;
- un état machine-readable ;
- un journal de reprise ;
- un premier modèle cible ;
- un premier contrat de scope ;
- une première adaptation de pipeline sans explosion de complexité.

---

## Premier jalon recommandé

Le premier jalon utile et réaliste est :

**J1 — définir puis valider le contrat minimal d'un run borné**

Contenu de J1 :
- structure du `scope_manifest` ;
- structure du `impact_bundle` ;
- structure du `integration_gate` ;
- liste des changements minimaux à apporter au pipeline `constitution`.

Tant que ce jalon n'est pas posé, le reste du chantier restera conceptuel.
