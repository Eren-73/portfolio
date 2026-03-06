
export interface IContact {
  id: number;
  utilisateur: number;
  nom_complet: string;
  email: string;
  objet: string;
  message: string;
  est_lu: boolean;
  date_envoi: string;
}