import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RepositoryService } from '../../../services/RepositoryService';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-repository-agent',
  imports: [FormsModule, DecimalPipe],
  templateUrl: './repository-agent.html',
  styleUrl: './repository-agent.css',
})
export class RepositoryAgent {
  loading = false;
  githubUrl = '';
  analysisResult: any = null;

  constructor(private repositoryService: RepositoryService) {}

  analyze(): void {
    if (!this.githubUrl.trim()) return;

    this.repositoryService.analyzeRepository(this.githubUrl).subscribe({
      next: (response) => {
        this.analysisResult = response;
        this.loading = false;
      },
      error: (error) => {
        console.error(error);
        this.loading = false;
      },
    });
  }

  getScoreColor(score: number): string {
    if (score >= 95) return '#2563eb';
    if (score >= 85) return '#10b981';
    if (score >= 75) return '#22c55e';
    if (score >= 65) return '#84cc16';
    if (score >= 55) return '#eab308';
    if (score >= 45) return '#f59e0b';
    if (score >= 35) return '#f97316';
    return '#ef4444';
  }

  hasData(value: any): boolean {
    if (value === null || value === undefined) {
      return false;
    }

    if (Array.isArray(value)) {
      return value.length > 0;
    }

    if (typeof value === 'string') {
      return value.trim().length > 0;
    }

    return true;
  }

  newAnalysis(): void {
    this.analysisResult = null;
    this.githubUrl = '';
  }
}
