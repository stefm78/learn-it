DSL2Human v1.0 {
  
  // Meta-gouvernance
  gouvernance {
    regle_revision: "quoi_pourquoi | combien_comment"
    hierarchie_conflits: [
      "fidelite_absolute_P1 > extension_logique_P2",
      "structure_DSL_P3 > exhaustivite_P4",
      "hierarchie_conservee_P5 > clarite_narrative_P6"
    ]
  }
  
  // Typage transformation
  types_transformation: {
    DSL_compact: {axe:"structure_hierarchique", cible:"markdown_natif", ratio:"10-20x"}
    principe: {format:"300-500mots", structure:"argument_justification_exemple_limites"}
    regle: {format:"paragraphe_explicatif", garde_fou:"evidence"}
    metriques: {format:"tableau_comparatif"}
  }
  
  // Pipeline analyse obligatoire (P0)
  analyse_DSL: {
    etapes: [
      "structure_hierarchique",
      "concepts_cles", 
      "relations_dependencies",
      "ton_implicite"
    ]
    cible: "carte_sementique_complete"
  }
  
  // Règles transformation strictes (P1-P6)
  principes: {
    
    P1_fidelite: {
      regle: "aucune_information_absente_DSL"
      mecanisme: "inference_logique_coherente_uniquement"
      garde_fou: "GF01_verification_traçabilité"
    }
    
    P2_hierarchie: {
      mapping: "niveau_DSL → header_markdown"
      niveaux: ["#", "##", "###", "####"]
    }
    
    P3_exhaustivite: {
      cible: "chaque_element_DSL → explication_complete"
      profondeur: "200-500mots_par_principe_majeur"
    }
    
    P4_clarte: {
      definitions: "premiere_occurrence"
      sequence: "general → particulier → limites"
      exemples: "obligatoires_concrets"
    }
    
    P5_structure_sortie: {
      sections_obligatoires: [
        "TITRE_v[VERSION]",
        "Note_version_Contexte", 
        "Sections_DSL_principales",
        "Glossaire_Referentiel",
        "Seuils_critiques"
      ]
    }
    
    P6_formatage: {
      tableaux: "typages_metriques_hierarchies_seuils"
      listes_numerotees: "sequences_priorites_workflows"
      listes_puces: "caracteristiques_garde_fous_cas"
      emphasis: "⚠️_garde_fous_critiques"
    }
    
    P7_ton_style: {
      registre: "argumentatif_technique"
      syntaxe: "phrases_actives_transitions_fluid"
      vocabulaire: "precise_domaine_DSL"
    }
    
    P8_livrables: {
      format: "markdown_complet_autonome"
      contraintes: [
        "aucun_commentaire_meta",
        "aucun_resume_introductif", 
        "aucune_mention_processus"
      ]
    }
  }
  
  // Garde-fous architecturaux
  garde_fous: {
    GF01_verification: "traçabilité_element_DSL → paragraphe_sortie"
    GF02_structure: "respect_hierarchie_DSL_ou_rejet"
    GF03_hallucination: "aucune_info_absente_DSL"
  }
  
  // Métriques qualité
  metriques: {
    ratio_expansion: {min: "10x", cible: "15-20x"}
    couverture: "100%_elements_DSL"
    coherence: "ton_domaine_DSL"
  }
  
  // Glossaire critique
  glossaire: {
    DSL: "Domain Specific Language compact structuré"
    KU_transformation: "unités: principe|regle|metrique|seuil"
    GF: "garde_fou architectural critique"
  }
  
  // Paramètres critiques
  seuils: {
    fidelite: {min: "100%_couverture_DSL"}
    volume: {min: "10x_DSL_original"}
    structure: {validite: "100%_hierarchie_conservee"}
  }
}
