// src/environments/environment.prod.ts
// Configuration de l'environnement de production (Vercel + Railway)
// Pourquoi: remplace environment.ts lors du build Angular pour la prod
// Relevant: BaseService.ts, environment.ts, angular.json

export const environment = {
  production: true,
  apiUrl: 'https://portfolio-production-0ae3.up.railway.app/api',
  mediaUrl: 'https://portfolio-production-0ae3.up.railway.app',
};
