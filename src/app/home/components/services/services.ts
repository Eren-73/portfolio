// src/app/home/components/services/services.ts
// Section "Services" — affiche les services depuis l'API Django
// Pourquoi: charge dynamiquement les compétences/services de l'utilisateur
// Relevant: ServicesService, IService, services.html

import { Component, OnInit, signal, ChangeDetectionStrategy } from '@angular/core';
import { inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServicesService } from '../../../service/ServicesService';
import { IService } from '../../../shared/models/IServices';

@Component({
  selector: 'app-services',
  imports: [CommonModule],
  templateUrl: './services.html',
  styleUrl: './services.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class Services implements OnInit {
  private servicesService = inject(ServicesService);

  readonly USER_ID = 2;

  services = signal<IService[]>([]);
  loading = signal(true);

  // Icone par type de service
  readonly iconMap: Record<string, string> = {
    DEV_WEB: 'mbri-sites',
    DEV_MOBILE: 'mbri-smartphone',
    DEV_BACKEND: 'mbri-database',
    DEV_FRONTEND: 'mbri-code',
    API: 'mbri-cloud',
    CONSULTING: 'mbri-setting2',
    FORMATION: 'mbri-layers',
    MAINTENANCE: 'mbri-setting2',
    AUTRE: 'mbri-code'
  };

  getIcon(type: string): string {
    return this.iconMap[type] ?? 'mbri-code';
  }

  ngOnInit(): void {
    this.servicesService.getByUtilisateur(this.USER_ID).subscribe({
      next: (data) => {
        const list = (data as any).results ?? data;
        this.services.set(Array.isArray(list) ? list : []);
        this.loading.set(false);
      },
      error: () => {
        // En cas d'erreur, on garde la liste vide → affiche le contenu statique
        this.loading.set(false);
      }
    });
  }
}

