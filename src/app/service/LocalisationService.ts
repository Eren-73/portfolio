import { inject, Injectable } from "@angular/core";
import { ILocalisation } from "../shared/models/ILocalisation";
import { BaseService } from "../shared/base/Baseservice";

@Injectable({
  providedIn: 'root'
})
export class LocalisationService {
  private baseService = inject(BaseService);

  getById(id: number): ILocalisation {
    return {} as ILocalisation;
  }

  getAll(): ILocalisation[] {
    return [] as ILocalisation[];
  }
}