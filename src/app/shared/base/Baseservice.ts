// src/app/shared/base/Baseservice.ts
// Service de base qui centralise tous les appels HTTP vers l'API Django
// Pourquoi: évite de répéter l'URL et la logique HTTP dans chaque service
// Relevant: UsersService, ProjectsService, ContactsService, ...

import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BaseService {
  private http = inject(HttpClient);
  // URL de base de l'API Django — différente selon dev ou prod
  private readonly apiUrl = environment.apiUrl;

  // GET — récupère des données (liste ou objet unique)
  // Gère les query params proprement: "experiences?utilisateur=2" → "/api/experiences/?utilisateur=2"
  get<T>(endpoint: string): Observable<T> {
    const [path, query] = endpoint.split('?');
    const url = query
      ? `${this.apiUrl}/${path}/?${query}`
      : `${this.apiUrl}/${path}/`;
    return this.http.get<T>(url);
  }

  // POST — crée une nouvelle ressource
  save<T>(endpoint: string, data: unknown): Observable<T> {
    return this.http.post<T>(`${this.apiUrl}/${endpoint}/`, data);
  }

  // PUT — remplace une ressource existante en entier
  update<T>(endpoint: string, data: unknown): Observable<T> {
    return this.http.put<T>(`${this.apiUrl}/${endpoint}/`, data);
  }

  // PATCH — modifie partiellement une ressource
  patch<T>(endpoint: string, data: unknown): Observable<T> {
    return this.http.patch<T>(`${this.apiUrl}/${endpoint}/`, data);
  }

  // DELETE — supprime une ressource
  delete(endpoint: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${endpoint}/`);
  }
}
