# ARBITRAGE — Constitution Pipeline STAGE_02_ARBITRAGE

<!-- pipeline: constitution -->
<!-- stage: STAGE_02_ARBITRAGE -->
<!-- date: 2026-04-01 -->
<!-- status: consolidated_decision_record -->

## Résumé exécutif

Cet arbitrage consolide les rapports `arbitrage_*.md` disponibles dans `docs/pipelines/constitution/work/01_challenge/`, avec prise en compte complémentaire de `challenge_NemoTron.md`, `challenge_NemoTron_bis.md` et de l'analyse de cohérence complémentaire figurant dans `tmp/Claude.md`.

Le corpus est globalement convergent sur un noyau dur de problèmes structurels :
- états moteur indéfinis
- dépendances inter-Core implicites
- événements référencés mais non déclarés
- cycles d'escalade non fermés
- frontière Constitution / Référentiel / LINK insuffisamment explicitée sur certains points

### Synthèse des décisions

- `corriger_maintenant` : trous structurels, chaînes incomplètes, états indéfinis, ambiguïtés runtime/offline, garde-fous minimaux de sécurité
- `reporter` : sujets réels mais non critiques pour fermer le moteur dans ce run, ou demandant un cycle de conception dédié
- `rejeter` : faux problèmes, préférences éditoriales, ou remises en cause d'un choix pédagogique déjà assumé
- `hors_perimetre` : gouvernance documentaire large ou sujets non destinés à être traités par le patch de ce run

### Décisions humaines déjà tranchées

- HUM-01 — Versioning inter-Core complet : **B**
- HUM-02 — `post-mastery revocation` : **B**
- HUM-03 — Référence fantôme `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED` : **B**
- HUM-04 — Priorité du régime de détresse : **A**
- HUM-05 — Gamification probatoire : **A**

### Arbitrages complémentaires tranchés

- SUP-01 — Détresse d'activation persistante : **A**
- SUP-02 — Notification externe en cas de divergence : **A**
- SUP-03 — Priorité entre escalades concurrentes : **A**
- SUP-04 — AR-N3 : **A**

---

## Périmètre consolidé

### Fichiers d'arbitrage considérés
- `arbitrage_ClaudeWoThink.md`
- `arbitrage_perplexity.md`
- `arbitrage_Perplexity_Sonnet46.md`
- `arbitrage_GPTwoThink.md`
- `arbitrage_Perplexity_SonnetThink.md`

### Fichiers challenge pris en compte en complément
- `challenge_NemoTron.md`
- `challenge_NemoTron_bis.md`

### Analyse complémentaire de cohérence
- `tmp/Claude.md`

### Règle d'arbitrage appliquée
- la convergence inter-rapports prime sur la sévérité isolée
- un point peut être retenu même avec faible convergence s'il casse clairement une chaîne fonctionnelle ou crée un état moteur interdit / indéfini
- tout point exigeant un choix de doctrine plus large qu'un patch minimal a été isolé puis tranché explicitement ou reporté

---

## Corrections à faire maintenant

### ARB-01 — Binding LINK manquant pour la divergence MSC / perception
**Décision :** `corriger_maintenant`

**Constat consolidé :** `EVENT_MSC_PERCEPTION_DIVERGENCE_DETECTED` dépend de `PARAM_REFERENTIEL_MSC_PERCEPTION_DIVERGENCE_THRESHOLD`, mais le binding explicite côté LINK est manquant ou insuffisant.

**Conséquence patch :**
- ajouter un `TYPE_BINDING` explicite dans le LINK entre l'EVENT et le PARAM référentiel concerné

**Justification :**
Sans ce binding, la résolution de la chaîne d'autorité est implicite. Ce point doit être rendu structurellement résoluble et audit-able.

---

### ARB-02 — Fallback constitutionnel si le Référentiel manque, est invalide ou incompatible
**Décision :** `corriger_maintenant`

**Constat consolidé :** plusieurs règles ou événements constitutionnels dépendent de seuils délégués au Référentiel sans comportement explicite si le Référentiel est absent, invalide ou non compatible.

**Conséquence patch :**
- ajouter un invariant ou une règle de précondition déclarant qu'aucune évaluation de seuil délégué ne peut être faite sans Référentiel valide
- prévoir un comportement conservateur explicite ou un blocage explicite de déploiement

**Justification :**
Il faut supprimer l'entre-deux où le moteur n'est ni clairement bloqué ni clairement en mode conservateur.

---

### ARB-03 — Cas multi-axes `unknown` sans comportement composite explicite
**Décision :** `corriger_maintenant`

**Constat consolidé :** la gestion d'un axe `unknown` existe, mais pas celle de plusieurs axes `unknown` simultanés.

**Conséquence patch :**
- ajouter un invariant ou une règle explicite de réponse conservatrice maximale quand plusieurs axes sont simultanément `unknown`

**Justification :**
C'est un trou de comportement moteur et non une simple préférence de modélisation.

---

### ARB-04 — `INV_MSC_AND_STRICT` : composante non calculable
**Décision :** `corriger_maintenant`

**Constat consolidé :** en première session ou sans historique suffisant, une composante du MSC peut être non calculable ; l'état résultant n'est pas tranché proprement.

**Conséquence patch :**
- ajouter une règle explicite du type : composante non calculable ⇒ maîtrise `deferred`
- ne pas la faire tomber implicitement à `false`

**Justification :**
Le cas existe nécessairement pour un nouvel apprenant.

---

### ARB-05 — Acyclicité du graphe à revalider après patch
**Décision :** `corriger_maintenant`

**Constat consolidé :** l'acyclicité est couverte au chargement initial, mais pas explicitement après patch incrémental du graphe.

**Conséquence patch :**
- étendre le trigger existant, ou ajouter un invariant dédié de revalidation post-patch

**Justification :**
Un patch ne doit pas pouvoir réintroduire silencieusement un cycle.

---

### ARB-06 — Flag `misconception` non autorisé en runtime
**Décision :** `corriger_maintenant`

**Constat consolidé :** le flag `misconception` est utilisé dans les règles, mais son mode d'attribution n'est pas assez borné ; il faut exclure toute inférence implicite en runtime.

**Conséquence patch :**
- préciser explicitement que ce flag est posé en conception ou hors session seulement

**Justification :**
Cela protège la frontière entre design offline et exécution locale.

---

### ARB-07 — Composante T : cycle de vie minimal à fermer
**Décision :** `corriger_maintenant`

**Constat consolidé :** T est déclarée mais pas suffisamment gouvernée dans son cycle de vie : absence de déclencheur, d'état explicite si jamais non évaluée, ou d'événement de retard d'évaluation.

**Conséquence patch :**
- ajouter `EVENT_T_EVALUATION_OVERDUE`
- ajouter une rule minimale de scheduling ou de signalement

**Justification :**
La composante existe ; son cycle de vie minimal doit donc être fermé.

---

### ARB-08 — `EVENT_CONSERVATIVE_SCAFFOLDING_ESCALATION` manquant
**Décision :** `corriger_maintenant`

**Constat consolidé :** le Référentiel y fait référence, mais l'événement n'est pas formellement déclaré.

**Conséquence patch :**
- déclarer l'événement dans la bonne couche, ici le Référentiel

**Justification :**
Une chaîne d'escalade ne peut pas fonctionner si l'événement déclencheur n'existe pas.

---

### ARB-09 — `EVENT_SYSTEMIC_INVESTIGATION_AUTO_OPENED` manquant
**Décision :** `corriger_maintenant`

**Constat consolidé :** l'événement est appelé par la logique référentielle, mais n'existe pas comme entité déclarée.

**Conséquence patch :**
- déclarer l'événement
- le relier correctement à la logique d'investigation systémique

**Justification :**
Tant qu'il manque, la chaîne d'investigation est ouverte mais non exécutable.

---

### ARB-10 — Investigation systémique : cycle d'entrée / sortie inachevé
**Décision :** `corriger_maintenant`

**Constat consolidé :** l'investigation systémique a une entrée partielle, mais pas de sortie claire, pas de clôture, pas de borne temporelle ni de résolution suffisamment formalisée.

**Conséquence patch :**
- ajouter un événement ou une rule de clôture
- ajouter une borne ou une fenêtre maximale

**Justification :**
Il ne faut pas créer un mode moteur dont on ne sait pas sortir proprement.

---

### ARB-11 — Détresse d'activation persistante sans escalade explicite
**Décision :** `corriger_maintenant`

**Constat consolidé :** la divergence de perception dispose d'une escalade, mais la détresse d'activation persistante peut rester indéfiniment en mode conservateur sans escalade explicite.

**Conséquence patch :**
- ajouter une règle d'escalade symétrique à l'existant quand la détresse d'activation persiste sur N sessions
- paramétrer N dans le Référentiel

**Justification :**
L'asymétrie est mauvaise pour l'apprenant et inutilement incohérente du point de vue de la gouvernance pédagogique.

---

### ARB-12 — Notification externe de divergence : hors session uniquement
**Décision :** `corriger_maintenant`

**Constat consolidé :** une notification externe déclenchée pendant une session active entrerait en conflit avec le principe de runtime local only.

**Conséquence patch :**
- préciser explicitement que la notification externe éventuelle ne peut partir qu'hors session

**Justification :**
La correction est minime, sûre et lève un conflit structurel potentiel.

---

### ARB-13 — Priorité entre escalades concurrentes
**Décision :** `corriger_maintenant`

**Constat consolidé :** plusieurs mécanismes d'escalade peuvent théoriquement se présenter en concurrence sans ordre explicite.

**Conséquence patch :**
- ajouter une table de priorité explicite :
  1. investigation systémique
  2. divergence de perception
  3. signaux de motivation

**Justification :**
Cela évite des implémentations divergentes et garde la sécurité pédagogique au sommet.

---

### ARB-14 — Hiérarchie des régimes adaptatifs : garde-fou constitutionnel minimal sur la détresse
**Décision :** `corriger_maintenant`

**Constat consolidé :** la résolution de conflits entre régimes ne doit pas pouvoir rétrograder implicitement la priorité de la détresse par simple patch Référentiel.

**Conséquence patch :**
- ajouter un garde-fou constitutionnel minimal protégeant la priorité du régime de détresse

**Justification :**
Décision humaine validée : la détresse doit rester structurellement prioritaire.

---

### ARB-15 — Gamification probatoire sans fermeture
**Décision :** `corriger_maintenant`

**Constat consolidé :** le mode probatoire peut rester ouvert sans durée maximale ni sortie explicite.

**Conséquence patch :**
- ajouter un paramètre de durée maximale dans le Référentiel
- ajouter un événement ou une règle de sortie du mode probatoire

**Justification :**
Décision humaine validée : par cohérence structurelle, cette boucle ouverte doit être fermée dans ce run.

---

## Points reportés

### REP-01 — AR-N3 insuffisamment explicité
**Décision :** `reporter`

**Motif :** sujet réel mais moins critique que les chaînes cassées.

**Décision de couche déjà tranchée :**
- la consommation de N3 est **référentielle**, pas constitutionnelle

**Conséquence de gouvernance :**
- à reprendre dans un prochain cycle avec explicitation propre côté Référentiel et, si nécessaire, ajustement du LINK

---

### REP-02 — Charge cognitive cumulée des sollicitations AR
**Décision :** `reporter`

**Motif :** vrai sujet d'ergonomie et de calibrage pédagogique, mais pas nécessaire pour fermer le moteur dans ce run.

**Conséquence de gouvernance :**
- à reprendre dans un cycle dédié à la calibration AR

---

### REP-03 — Décroissance temporelle explicite de R
**Décision :** `reporter`

**Motif :** sujet important à terme, mais il engage davantage la doctrine pédagogique qu'une fermeture structurelle immédiate.

**Statut explicite :**
- risque pédagogique accepté temporairement
- non traité dans ce run

**Conséquence de gouvernance :**
- à reprendre dans un cycle dédié avec choix explicite sur la décroissance, les paramètres, les bornes et les effets runtime

---

## Rejets et hors périmètre

### REJ-01 — Remise en cause générale du plafonnement Bloom
**Décision :** `rejeter`

**Motif :** relève d'un choix pédagogique assumé et non d'un défaut structurel du système.

---

### HP-01 — Normalisation immédiate des `source_anchor`
**Décision :** `hors_perimetre`

**Motif :** sujet de gouvernance documentaire, pas une lacune moteur immédiate.

---

### HP-02 — Versioning inter-Core complet et mécanisme général de release coordonnée
**Décision :** `hors_perimetre`

**Motif :** décision humaine tranchée en B. Les 3 fichiers Core évoluent conjointement dans le cadre opérationnel actuel. Aucun mécanisme global supplémentaire n'est ajouté dans ce run.

---

### HP-03 — Création d'un nouveau concept constitutionnel autonome de `post-mastery revocation`
**Décision :** `hors_perimetre`

**Motif :** décision humaine tranchée en B.

**Consigne de cohérence :**
- ne pas créer de nouveau concept constitutionnel autonome dans ce run
- reformuler la logique référentielle concernée comme cas particulier d'un concept déjà reconnu, si correction nécessaire

---

### HP-04 — Création d'une nouvelle règle constitutionnelle `RULE_VC_AXIS_DEACTIVATION_AUTHORIZED`
**Décision :** `hors_perimetre`

**Motif :** décision humaine tranchée en B.

**Consigne de cohérence :**
- corriger le Référentiel pour pointer vers un élément existant ou retirer la référence fantôme
- ne pas enrichir inutilement la Constitution pour satisfaire une référence erronée

---

## Décisions de couche déjà tranchées

- AR-N3 : couche **référentielle**
- versioning inter-Core complet : **hors patch de ce run**
- `post-mastery revocation` : **ne pas créer comme concept constitutionnel autonome dans ce run**
- priorité du régime de détresse : **protégée constitutionnellement à titre minimal**
- gamification probatoire : **corriger dans ce run**

---

## Contraintes de synthèse pour STAGE_03_PATCH_SYNTHESIS

1. Préférer les ajouts additifs aux refontes.
2. Ne pas introduire de nouveau concept constitutionnel si un recadrage référentiel suffit.
3. Ne pas rouvrir dans ce patch la gouvernance large du versioning inter-Core.
4. Conserver strictement la séparation Constitution / Référentiel / LINK.
5. Toute nouvelle règle d'escalade externe doit être explicitement hors session.
6. Toute priorité inter-régimes ou inter-escalades ajoutée doit rester minimale et orientée sécurité pédagogique.
7. Les reports REP-01 à REP-03 doivent rester visibles comme backlog de gouvernance assumé, non comme oubli.

---

## Décision de transmission au STAGE_03_PATCH_SYNTHESIS

Transmettre au patch :
- ARB-01 à ARB-15

Ne pas transmettre au patch :
- REP-01 à REP-03
- REJ-01
- HP-01 à HP-04

Le patch de ce run doit viser :
- fermeture des chaînes cassées
- suppression des états indéfinis
- clarification runtime/offline
- protection minimale des priorités de sécurité
- sans relancer un chantier de doctrine ou de gouvernance plus large que nécessaire
