// src/app/home/components/resume/resume.ts
// Section "Résumé/Parcours" — affiche formations, expériences et compétences depuis l'API
// Pourquoi: tout est éditable depuis l'admin Django sans toucher au code
// Relevant: ExperienceService, ServicesService, UserService, resume.html

import { Component, OnInit, signal, computed, ChangeDetectionStrategy } from '@angular/core';
import { inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExperienceService } from '../../../service/ExperiencesService';
import { ServicesService } from '../../../service/ServicesService';
import { UserService } from '../../../service/UsersService';
import { IExperience } from '../../../shared/models/IExperiences';
import { IService } from '../../../shared/models/IServices';
import { IUser } from '../../../shared/models/IUsers';

@Component({
  selector: 'app-resume',
  imports: [CommonModule],
  templateUrl: './resume.html',
  styleUrl: './resume.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Resume implements OnInit {
  private experienceService = inject(ExperienceService);
  private servicesService = inject(ServicesService);
  private userService = inject(UserService);

  readonly USER_ID = 2;

  user = signal<IUser | null>(null);
  experiences = signal<IExperience[]>([]);
  services = signal<IService[]>([]);
  loading = signal(true);

  // Compteur interne : loading=false quand les 3 requêtes sont terminées
  private loaded = 0;
  private done() { if (++this.loaded >= 3) this.loading.set(false); }

  // Sépare automatiquement formations et expériences professionnelles
  formations = computed(() =>
    this.experiences().filter(e => e.type_contrat === 'FORMATION')
  );

  expPro = computed(() =>
    this.experiences().filter(e => e.type_contrat !== 'FORMATION')
  );

  // Extrait tous les outils uniques depuis les services (ex: "Django,Python" -> tags)
  outils = computed(() => {
    const set = new Set<string>();
    this.services().forEach(s => {
      if (s.outils) {
        s.outils.split(',').map(o => o.trim()).filter(Boolean).forEach(o => set.add(o));
      }
    });
    return Array.from(set);
  });

  // URL du CV : préfère le fichier uploadé, sinon le lien externe
  cvUrl = computed(() => {
    const u = this.user();
    if (!u) return null;
    if (u.fichier_cv) return 'http://localhost:8000' + (u.fichier_cv.startsWith('/') ? u.fichier_cv : '/' + u.fichier_cv);
    if (u.lien_cv) return u.lien_cv;
    return null;
  });

  ngOnInit(): void {
    this.userService.getById(this.USER_ID).subscribe({
      next: (data) => { this.user.set(data); this.done(); },
      error: () => this.done()
    });

    this.experienceService.getByUtilisateur(this.USER_ID).subscribe({
      next: (data) => {
        const list = (data as any).results ?? data;
        this.experiences.set(Array.isArray(list) ? list : []);
        this.done();
      },
      error: () => this.done()
    });

    this.servicesService.getByUtilisateur(this.USER_ID).subscribe({
      next: (data) => {
        const list = (data as any).results ?? data;
        this.services.set(Array.isArray(list) ? list : []);
        this.done();
      },
      error: () => this.done()
    });
  }

  // Formate une période de dates en texte lisible
  formatPeriode(exp: IExperience): string {
    const debut = new Date(exp.date_debut).getFullYear();
    if (exp.est_en_cours) return debut + ' - Présent';
    if (exp.date_fin) return debut + ' - ' + new Date(exp.date_fin).getFullYear();
    return String(debut);
  }
}
