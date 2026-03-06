// src/app/service/ContactsService.ts
// Gère les appels API pour les messages de contact
// Pourquoi: permet d'envoyer un message via le formulaire vers /api/contacts/
// Relevant: BaseService, IContact, contact.ts

import { inject, Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { IContact } from '../shared/models/IContact';
import { BaseService } from "../shared/base/Baseservice";

@Injectable({
  providedIn: 'root'
})
export class ContactService {
  private baseService = inject(BaseService);

  // Récupère un contact par son id
  getById(id: number): Observable<IContact> {
    return this.baseService.get<IContact>(`contacts/${id}`);
  }

  // Récupère tous les contacts
  getAll(): Observable<IContact[]> {
    return this.baseService.get<IContact[]>('contacts');
  }

  // Envoie un nouveau message de contact
  saveContact(contact: Omit<IContact, 'id' | 'est_lu' | 'date_envoi'>): Observable<IContact> {
    return this.baseService.save<IContact>('contacts', contact);
  }
}
