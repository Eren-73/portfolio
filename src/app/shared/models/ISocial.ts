export interface ISocial {
  id: number;
  utilisateur: number;
  nom_plateforme: 'GITHUB' | 'LINKEDIN' | 'TWITTER' | 'FACEBOOK' | 'INSTAGRAM' | 'PORTFOLIO' | 'AUTRE';
  lien: string;
  date_creation: string;
}
