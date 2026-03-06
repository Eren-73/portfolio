export interface IExperience {
  id: number;
  utilisateur: number;
  utilisateur_nom?: string;
  role: string;
  entreprise: string;
  description: string;
  type_contrat: 'CDI' | 'CDD' | 'STAGE' | 'FREELANCE' | 'ALTERNANCE' | 'FORMATION';
  date_debut: string;
  date_fin?: string;
  est_en_cours: boolean;
  duree?: number;
  date_creation: string;
}