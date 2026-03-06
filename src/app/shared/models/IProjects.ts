export interface IProject {
  id: number;
  utilisateur: number;
  utilisateur_nom?: string;
  titre: string;
  resume: string;
  image?: string;
  lien: string;
  date_creation: string;
  date_modification: string;
}
