import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AnalyzeRepositoryRequest } from '../models/AnalyzeRepositoryRequest';

@Injectable({
  providedIn: 'root',
})
export class RepositoryService {
  constructor(private http: HttpClient) {}

  private readonly API_URL = 'http://localhost:8000';

  analyzeRepository(githubUrl: string): Observable<any> {
    const request: AnalyzeRepositoryRequest = {
        github_url: githubUrl
    }
    return this.http.post(`${this.API_URL}/agents/analyze-repository`, request);
  }
}
