// src/environments/environment.prod.ts
// Configuration de l'environnement de production (Vercel + Railway)
// Pourquoi: remplace environment.ts lors du build Angular pour la prod
// Relevant: BaseService.ts, environment.ts, angular.json

export const environment = {
  production: true,
  // ⚠️ À METTRE À JOUR après le déploiement Railway
  // Exemple: 'https://portfolio-api-production.up.railway.app/api'
  apiUrl: 'https://VOTRE_URL_RAILWAY.up.railway.app/api',
  mediaUrl: 'https://VOTRE_URL_RAILWAY.up.railway.app',
};
