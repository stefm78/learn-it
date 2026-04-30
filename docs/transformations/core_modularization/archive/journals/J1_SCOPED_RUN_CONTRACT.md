# J1 — contrat minimal d'un run borné

## Objet

Ce document définit le **strict nécessaire** pour permettre à un pipeline de gouvernance existant d'exécuter un run sur un **sous-ensemble borné** sans refonte complète immédiate.

Le but n'est pas encore de rendre toute la chaîne totalement modulaire.
Le but est de définir le plus petit contrat stable permettant :
- un challenge ciblé ;
- un arbitrage ciblé ;
- un patch ciblé ;
- une validation locale ;
- puis une réintégration contrôlée dans une validation globale.

---

## Principe général

Un run borné repose sur trois artefacts complémentaires :

1. `scope_manifest`
   - définit **ce que le run a le droit de traiter** ;
   - borne les artefacts, modules, IDs, opérations autorisées et exclusions.

2. `impact_bundle`
   - définit **ce que le run doit relire autour de son scope** ;
   - inclut la zone modifiée et son voisinage logique minimal.

3. `integration_gate`
   - définit **ce qui doit être rejoué globalement** avant release/promotion ;
   - évite qu'un succès local soit confondu avec une cohérence canonique globale acquise.

---

## Positionnement par rapport aux pipelines existants

Le run borné ne remplace pas immédiatement les pipelines `constitution` et `platform_factory`.

Il introduit un régime intermédiaire :
- mêmes pipelines de base ;
- mêmes familles de prompts ;
- mêmes étapes globales ;
- mais avec un **contexte d'exécution borné** et un **gate global explicite**.

Autrement dit :
- on ne duplique pas les pipelines ;
- on ne multiplie pas les prompts par sous-ensemble ;
- on ajoute un contrat de périmètre.

---

## Artefact 1 — `scope_manifest`

### Rôle

Déclarer le périmètre autorisé du run.

### Questions auxquelles il répond

- Quel pipeline est concerné ?
- Quel est le scope fonctionnel exact ?
- Quels fichiers sont dans le périmètre modifiable ?
- Quels modules ou blocs internes sont dans le périmètre ?
- Quels IDs sont dans le périmètre ?
- Quelles opérations sont autorisées ?
- Quelles zones sont explicitement hors scope ?
- Quel niveau d'impact hors scope est toléré ?

### Règle clé

Un run borné ne peut **ni écrire ni arbitrer silencieusement** hors du périmètre déclaré.
S'il détecte un impact hors scope, il doit :
- soit le signaler ;
- soit demander un élargissement explicite du scope ;
- soit le différer.

---

## Artefact 2 — `impact_bundle`

### Rôle

Assembler le **voisinage logique minimal** à relire pour travailler de manière sûre.

### Pourquoi il est nécessaire

Un scope trop étroit rend le travail local dangereux.
Il faut relire non seulement le sous-ensemble visé, mais aussi :
- ses dépendances amont ;
- ses dépendances aval ;
- les invariants transverses affectés ;
- les autres artefacts canoniques liés ;
- éventuellement l'arbitrage ou l'état de pipeline précédent utile.

### Contenu attendu

Le `impact_bundle` ne définit pas ce qui est **modifiable**.
Il définit ce qui est **à relire** pour éviter les modifications aveugles.

Il peut donc contenir :
- fichiers sources dans le scope ;
- fichiers liés hors scope ;
- blocs ou IDs reliés ;
- invariants transverses concernés ;
- dépendances croisées ;
- liste des points de vigilance.

---

## Artefact 3 — `integration_gate`

### Rôle

Empêcher la confusion entre :
- un succès local ;
- et une cohérence globale effectivement revalidée.

### Principe

Tout run borné peut réussir localement.
Mais avant release/promotion, il faut expliciter :
- quels contrôles globaux doivent être rejoués ;
- quels risques d'assemblage existent ;
- quels conflits potentiels doivent être exclus ;
- quel niveau de validation globale est requis.

### Effet attendu

Le `integration_gate` bloque toute promotion implicite d'un patch local tant que :
- la recompilation canonique complète n'est pas rejouée ;
- les références croisées ne sont pas revalidées ;
- les invariants globaux ne sont pas revalidés ;
- les collisions avec d'autres travaux parallèles ne sont pas évaluées.

---

## Règles minimales de gouvernance

### R1 — Le `scope_manifest` gouverne le droit d'action
Ce qui n'est pas dans le scope n'est pas implicitement modifiable.

### R2 — Le `impact_bundle` gouverne le devoir de lecture
Ce qui est relié logiquement peut devoir être lu, même si ce n'est pas modifiable.

### R3 — Le `integration_gate` gouverne le droit d'intégration
Ce qui a été localement validé n'est pas automatiquement intégrable.

### R4 — Aucun run borné ne peut promouvoir seul `current/`
La promotion reste un acte global centralisé.

### R5 — Le parallélisme porte sur les runs locaux, pas sur la vérité canonique finale
Plusieurs runs bornés peuvent coexister ; une seule intégration active peut être promue.

---

## Contrat minimal d'exécution

Un pipeline scope-aware doit pouvoir fonctionner selon la séquence suivante :

1. Lire le pipeline nominal existant.
2. Lire le `scope_manifest`.
3. Lire le `impact_bundle`.
4. Exécuter challenge / arbitrage / patch / validation locale dans ce périmètre.
5. Produire les livrables locaux usuels.
6. Passer par le `integration_gate` avant toute release/promotion.

---

## Premier usage recommandé

Premier terrain d'application recommandé :
- `constitution`
- sur un sous-ensemble borné simple et fortement identifiable
- sans déplacer encore physiquement les sources canoniques.

Ce premier pilote doit servir à valider :
- la clarté du `scope_manifest` ;
- la suffisance du `impact_bundle` ;
- la nécessité réelle du `integration_gate`.

---

## Livrables associés à J1

- `docs/transformations/core_modularization/templates/scope_manifest.template.yaml`
- `docs/transformations/core_modularization/templates/impact_bundle.template.yaml`
- `docs/transformations/core_modularization/templates/integration_gate.template.yaml`
- `docs/transformations/core_modularization/J1_CONSTITUTION_PIPELINE_MINIMAL_DELTA.md`

---

## Décision structurante de J1

Le chantier adopte la règle suivante :

**on ajoute un contrat de scope aux pipelines existants avant de chercher à construire un nouveau méta-pipeline.**

C'est le changement le plus sobre, le plus robuste, et le plus compatible avec le repo actuel.
