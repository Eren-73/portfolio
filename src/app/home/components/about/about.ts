// src/app/home/components/about/about.ts
// Section "À propos" — affiche les infos du profil utilisateur depuis l'API
// Pourquoi: connecte les données dynamiques Django au template about.html
// Relevant: UsersService, SocialService, IUser, ISocial, about.html

import { Component, OnInit, signal, ChangeDetectionStrategy } from '@angular/core';
import { inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from '../../../service/UsersService';
import { SocialService } from '../../../service/SocialService';
import { IUser } from '../../../shared/models/IUsers';
import { ISocial } from '../../../shared/models/ISocial';

@Component({
  selector: 'app-about',
  imports: [CommonModule],
  templateUrl: './about.html',
  styleUrl: './about.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class About implements OnInit {
  private userService = inject(UserService);
  private socialService = inject(SocialService);

  // ID de l'utilisateur du portfolio (Traore Husseni = 2)
  readonly USER_ID = 2;

  user = signal<IUser | null>(null);
  socials = signal<ISocial[]>([]);
  loading = signal(true);
  error = signal(false);

  // Mappe le nom de la plateforme vers l'icône Font Awesome
  readonly iconMap: Record<string, string> = {
    GITHUB: 'fab fa-github',
    LINKEDIN: 'fab fa-linkedin-in',
    TWITTER: 'fab fa-twitter',
    FACEBOOK: 'fab fa-facebook-f',
    INSTAGRAM: 'fab fa-instagram',
    PORTFOLIO: 'fas fa-globe',
    AUTRE: 'fas fa-link'
  };

  getIcon(plateforme: string): string {
    return this.iconMap[plateforme] ?? 'fas fa-link';
  }

  // Construit l'URL complète de l'image (gère les chemins relatifs et absolus)
  getPhotoUrl(path: string): string {
    if (path.startsWith('http')) return path;
    const clean = path.startsWith('/') ? path : '/' + path;
    return 'http://localhost:8000' + clean;
  }

  ngOnInit(): void {
    this.userService.getById(this.USER_ID).subscribe({
      next: (data) => {
        this.user.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      }
    });

    // Charge les réseaux sociaux séparément
    this.socialService.getByUtilisateur(this.USER_ID).subscribe({
      next: (data) => {
        const list = (data as any).results ?? data;
        this.socials.set(Array.isArray(list) ? list : []);
      },
      error: () => {} // silencieux, pas bloquant
    });
  }
}

