// src/app/service/ServicesService.ts
// Gère les appels API pour les services proposés
// Pourquoi: centralise les requêtes vers /api/services/
// Relevant: BaseService, IService, services.ts

import { inject, Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { IService } from "../shared/models/IServices";
import { BaseService } from "../shared/base/Baseservice";

@Injectable({
  providedIn: 'root'
})
export class ServicesService {
  private baseService = inject(BaseService);

  // Récupère un service par son id
  getById(id: number): Observable<IService> {
    return this.baseService.get<IService>(`services/${id}`);
  }

  // Récupère tous les services
  getAll(): Observable<IService[]> {
    return this.baseService.get<IService[]>('services');
  }

  // Récupère les services d'un utilisateur
  getByUtilisateur(utilisateurId: number): Observable<IService[]> {
    return this.baseService.get<IService[]>(`services?utilisateur=${utilisateurId}`);
  }
}