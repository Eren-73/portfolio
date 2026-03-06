// src/app/home/components/contact/contact.ts
// Formulaire de contact — envoie un message à l'API Django
// Pourquoi: permet aux visiteurs d'envoyer un vrai message via /api/contacts/
// Relevant: ContactService, IContact, contact.html

import { Component, signal, ChangeDetectionStrategy } from '@angular/core';
import { inject } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { ContactService } from '../../../service/ContactsService';

@Component({
  selector: 'app-contact',
  imports: [ReactiveFormsModule],
  templateUrl: './contact.html',
  styleUrl: './contact.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Contact {
  private contactService = inject(ContactService);
  private fb = inject(FormBuilder);

  // ID de l'utilisateur destinataire (Traore Husseni = 2)
  readonly USER_ID = 2;

  sending = signal(false);
  success = signal(false);
  error = signal(false);

  form = this.fb.group({
    nom_complet: ['', [Validators.required, Validators.minLength(2)]],
    email: ['', [Validators.required, Validators.email]],
    objet: ['', [Validators.required, Validators.minLength(3)]],
    message: ['', [Validators.required, Validators.minLength(10)]]
  });

  onSubmit(): void {
    if (this.form.invalid) return;

    this.sending.set(true);
    this.success.set(false);
    this.error.set(false);

    const payload = {
      utilisateur: this.USER_ID,
      ...this.form.value
    } as any;

    this.contactService.saveContact(payload).subscribe({
      next: () => {
        this.sending.set(false);
        this.success.set(true);
        this.form.reset();
      },
      error: () => {
        this.sending.set(false);
        this.error.set(true);
      }
    });
  }
}

