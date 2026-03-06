// src/app/service/UsersService.ts
// Gère les appels API pour les données utilisateur (profil, portfolio)
// Pourquoi: centralise les requêtes vers /api/utilisateurs/
// Relevant: BaseService, IUser, about.ts, introduction.ts

import { inject, Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { IUser } from "../shared/models/IUsers";
import { BaseService } from "../shared/base/Baseservice";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private baseService = inject(BaseService);

  // Récupère un utilisateur par son id
  getById(id: number): Observable<IUser> {
    return this.baseService.get<IUser>(`utilisateurs/${id}`);
  }

  // Récupère la liste de tous les utilisateurs
  getAll(): Observable<IUser[]> {
    return this.baseService.get<IUser[]>('utilisateurs');
  }

  // Récupère le portfolio complet (projets + expériences + services + réseaux)
  getPortfolioComplet(id: number): Observable<any> {
    return this.baseService.get<any>(`utilisateurs/${id}/portfolio_complet`);
  }
}
