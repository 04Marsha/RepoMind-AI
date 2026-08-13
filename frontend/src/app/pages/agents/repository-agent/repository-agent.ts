import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RepositoryService } from '../../../services/RepositoryService';
import { DecimalPipe } from '@angular/common';
import { Router } from '@angular/router';
import { AnalysisStateService } from '../../../services/AnalysisStateService';
import { Loader } from '../../../components/loader/loader';

@Component({
  selector: 'app-repository-agent',
  imports: [FormsModule, Loader],
  templateUrl: './repository-agent.html',
  styleUrl: './repository-agent.css',
})
export class RepositoryAgent {
  loading = false;
  githubUrl = '';
  analysisResult: any = null;

  constructor(private repositoryService: RepositoryService, private router: Router, private analysisStateService: AnalysisStateService) {}

  analyze(): void {
    this.loading = true;
    if (!this.githubUrl.trim()) return;

    this.repositoryService.analyzeRepository(this.githubUrl).subscribe({
      next: (response) => {
        this.analysisStateService.analysisResult = response;
        this.router.navigate(['/agents/repository-agent/analysis'])
        this.loading = false;
      },
      error: (error) => {
        console.error(error);
        this.loading = false;
      },
    });
  }
}
