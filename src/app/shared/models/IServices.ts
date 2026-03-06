export interface IService {
  id: number;
  utilisateur: number;
  nom: string;
  detail: string;
  type_service: string;
  outils: string;
  niveau: number;  // 0-100, affiché comme barre de progression
  est_disponible: boolean;
  date_creation: string;
}
