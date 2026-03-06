// src/app/service/SocialService.ts
// Gère les appels API pour les réseaux sociaux
// Pourquoi: centralise les requêtes vers /api/reseaux-sociaux/
// Relevant: BaseService, ISocial, about.ts

import { inject, Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { BaseService } from "../shared/base/Baseservice";
import { ISocial } from "../shared/models/ISocial";

@Injectable({
  providedIn: 'root'
})
export class SocialService {
  private baseService = inject(BaseService);

  // Récupère les réseaux sociaux d'un utilisateur
  getByUtilisateur(utilisateurId: number): Observable<ISocial[]> {
    return this.baseService.get<ISocial[]>(`reseaux-sociaux?utilisateur=${utilisateurId}`);
  }

  // Récupère tous les réseaux actifs
  getAll(): Observable<ISocial[]> {
    return this.baseService.get<ISocial[]>('reseaux-sociaux');
  }
}