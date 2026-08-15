import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AnalyzeRepositoryRequest } from '../models/AnalyzeRepositoryRequest';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class RepositoryService {
  constructor(private http: HttpClient) {}

  private readonly API_URL = environment.apiUrl;

  analyzeRepository(githubUrl: string): Observable<any> {
    const request: AnalyzeRepositoryRequest = {
        github_url: githubUrl
    }
    return this.http.post(`${this.API_URL}/agents/analyze-repository`, request);
  }
}
