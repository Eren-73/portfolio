export interface ILocalisation {
  id: number;
  utilisateur: number;
  pays: string;
  ville: string;
  quartier?: string;
  latitude?: number;
  longitude?: number;
  est_actuelle: boolean;
  date_creation: string;
}