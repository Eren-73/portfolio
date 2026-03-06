// src/app/home/components/introduction/introduction.ts
// Section hero/introduction — affiche le nom et la photo de l'utilisateur depuis l'API
// Pourquoi: permet de changer le nom/photo affichés sur la page d'accueil depuis l'admin Django
// Relevant: UserService, IUser, introduction.html, about.ts

import { Component, OnInit, signal, ChangeDetectionStrategy } from '@angular/core';
import { inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from '../../../service/UsersService';
import { IUser } from '../../../shared/models/IUsers';

@Component({
  selector: 'app-introduction',
  imports: [CommonModule],
  templateUrl: './introduction.html',
  styleUrl: './introduction.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Introduction implements OnInit {
  private userService = inject(UserService);

  readonly USER_ID = 2;

  user = signal<IUser | null>(null);

  ngOnInit(): void {
    this.userService.getById(this.USER_ID).subscribe({
      next: (data) => this.user.set(data),
      error: () => {} // silencieux — garde le fallback statique
    });
  }

  // Construit l'URL complète de la photo (gère les chemins relatifs et absolus)
  getPhotoUrl(path: string): string {
    if (path.startsWith('http')) return path;
    const clean = path.startsWith('/') ? path : '/' + path;
    return 'http://localhost:8000' + clean;
  }
}
