// src/app/service/ExperiencesService.ts
// Gère les appels API pour les expériences professionnelles
// Pourquoi: centralise les requêtes vers /api/experiences/
// Relevant: BaseService, IExperience, resume.ts

import { inject, Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { IExperience } from "../shared/models/IExperiences";
import { BaseService } from "../shared/base/Baseservice";

@Injectable({
  providedIn: 'root'
})
export class ExperienceService {
  private baseService = inject(BaseService);

  // Récupère une expérience par son id
  getById(id: number): Observable<IExperience> {
    return this.baseService.get<IExperience>(`experiences/${id}`);
  }

  // Récupère toutes les expériences
  getAll(): Observable<IExperience[]> {
    return this.baseService.get<IExperience[]>('experiences');
  }

  // Récupère les expériences d'un utilisateur
  getByUtilisateur(utilisateurId: number): Observable<IExperience[]> {
    return this.baseService.get<IExperience[]>(`experiences?utilisateur=${utilisateurId}`);
  }
}