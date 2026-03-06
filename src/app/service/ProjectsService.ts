// src/app/service/ProjectsService.ts
// Gère les appels API pour les projets du portfolio
// Pourquoi: centralise les requêtes vers /api/projets/
// Relevant: BaseService, IProject, portfolio.ts

import { inject, Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { IProject } from "../shared/models/IProjects";
import { BaseService } from "../shared/base/Baseservice";

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private baseService = inject(BaseService);

  // Récupère un projet par son id
  getById(id: number): Observable<IProject> {
    return this.baseService.get<IProject>(`projets/${id}`);
  }

  // Récupère tous les projets
  getAll(): Observable<IProject[]> {
    return this.baseService.get<IProject[]>('projets');
  }

  // Récupère les projets d'un utilisateur spécifique
  getByUtilisateur(utilisateurId: number): Observable<IProject[]> {
    return this.baseService.get<IProject[]>(`projets?utilisateur=${utilisateurId}`);
  }
}