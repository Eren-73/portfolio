// src/app/home/components/portfolio/portfolio.ts
// Section "Portfolio" — affiche les projets depuis l'API Django
// Pourquoi: charge dynamiquement les projets de l'utilisateur
// Relevant: ProjectService, IProject, portfolio.html

import { Component, OnInit, signal, ChangeDetectionStrategy } from '@angular/core';
import { inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProjectService } from '../../../service/ProjectsService';
import { IProject } from '../../../shared/models/IProjects';

@Component({
  selector: 'app-portfolio',
  imports: [CommonModule],
  templateUrl: './portfolio.html',
  styleUrl: './portfolio.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Portfolio implements OnInit {
  private projectService = inject(ProjectService);

  readonly USER_ID = 2;

  projects = signal<IProject[]>([]);
  loading = signal(true);
  error = signal(false);

  ngOnInit(): void {
    this.projectService.getByUtilisateur(this.USER_ID).subscribe({
      next: (data) => {
        // L'API retourne {count, results: [...]} en mode paginé
        const list = (data as any).results ?? data;
        this.projects.set(Array.isArray(list) ? list : []);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      }
    });
  }

  // Construit l'URL complète de l'image (gère chemins relatifs et absolus)
  getImageUrl(path: string): string {
    if (path.startsWith('http')) return path;
    const clean = path.startsWith('/') ? path : '/' + path;
    return 'http://localhost:8000' + clean;
  }
}

