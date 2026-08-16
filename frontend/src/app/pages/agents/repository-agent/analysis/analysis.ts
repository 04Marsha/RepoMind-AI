import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AnalysisStateService } from '../../../../services/AnalysisStateService';

@Component({
  selector: 'app-analysis',
  imports: [],
  templateUrl: './analysis.html',
  styleUrls: ['./analysis.css', './analysis.media.css'],
})
export class Analysis implements OnInit {
  constructor(private router: Router, private analysisStateService: AnalysisStateService) {}
  
  analysisResult: any;

  ngOnInit() {
    this.analysisResult = this.analysisStateService.analysisResult;
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

  getValue(value: any, fallback = 'N/A'): any {
    return value !== null &&
      value !== undefined &&
      value !== '' &&
      !(typeof value === 'number' && isNaN(value))
      ? value
      : fallback;
  }

  newAnalysis(): void {
    this.router.navigate(['agents/repository-agent']);
  }
}
