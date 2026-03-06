// src/app/app.config.ts
// Configuration globale de l'application Angular
// Pourquoi: point d'entrée des providers (HttpClient, Router...)
// Relevant: app.routes.ts, shared/base/Baseservice.ts

import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient()   // Nécessaire pour que HttpClient fonctionne dans les services
  ]
};
