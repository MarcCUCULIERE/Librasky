import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, from } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';
import { Whisky, WhiskyCreateUpdate, WhiskyExport } from '../models/whisky.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class WhiskyService {
  private apiUrl = `${environment.apiUrl}/api/whiskies`;

  constructor(private http: HttpClient) {}

  getWhiskies(skip: number = 0, limit: number = 100): Observable<Whisky[]> {
    return this.http.get<Whisky[]>(`${this.apiUrl}?skip=${skip}&limit=${limit}`);
  }

  getWhisky(id: number): Observable<Whisky> {
    return this.http.get<Whisky>(`${this.apiUrl}/${id}`);
  }

  async processImage(image: File | string | undefined): Promise<string | undefined> {
    if (!image) return undefined;
    if (typeof image === 'string') return image;
    return await this.convertFileToBase64(image);
  }

  createWhisky(whisky: WhiskyCreateUpdate): Observable<Whisky> {
    return from(this.processImage(whisky.image)).pipe(
      switchMap(processedImage => {
        const whiskyData = {
          ...whisky,
          image: processedImage ? processedImage.split(',')[1] : undefined
        };
        return this.http.post<Whisky>(this.apiUrl, whiskyData);
      })
    );
  }

  updateWhisky(id: number, whisky: Partial<WhiskyCreateUpdate>): Observable<Whisky> {
    return from(this.processImage(whisky.image)).pipe(
      switchMap(processedImage => {
        const whiskyData = {
          ...whisky,
          image: processedImage ? processedImage.split(',')[1] : undefined,
          // Formatez la date au format ISO
          purchase_date: whisky.purchase_date ? this.formatDate(whisky.purchase_date) : undefined
        };
        return this.http.put<Whisky>(`${this.apiUrl}/${id}`, whiskyData);
      })
    );
  }

  deleteWhisky(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  exportWhiskies(): Observable<WhiskyExport> {
    return this.http.get<WhiskyExport>(`${this.apiUrl}/export`);
  }

  importWhiskies(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/import`, formData);
  }

  private async convertFileToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = error => reject(error);
    });
  }

  // Ajoutez cette méthode helper pour formater la date
  private formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
  }
}