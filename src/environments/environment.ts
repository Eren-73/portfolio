// src/environments/environment.ts
// Configuration de l'environnement de développement local
// Pourquoi: centralise l'URL de l'API pour dev vs prod sans toucher au code
// Relevant: BaseService.ts, environment.prod.ts

export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  mediaUrl: 'http://localhost:8000',
};
