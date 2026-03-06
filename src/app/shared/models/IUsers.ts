export interface IUser {
  id: number;
  nom: string;
  prenom: string;
  photo_profil?: string;
  description: string;
  age: number;
  email: string;
  lien_cv?: string;      // URL externe (Google Drive, etc.)
  fichier_cv?: string;   // Fichier uploadé depuis l'admin
  telephone: string;
  date_creation: string;
  date_modification: string;
}