import { Routes } from '@angular/router';
import { LandingPage } from './pages/landing-page/landing-page';
import { Agents } from './pages/agents/agents';
import { RepositoryAgent } from './pages/agents/repository-agent/repository-agent';

export const routes: Routes = [
    {
        path: '',
        component: LandingPage
    },
    {
        path: 'agents',
        component: Agents,
    },
    {
        path: 'agents/repository-agent',
        loadComponent: () => 
            import('./pages/agents/repository-agent/repository-agent')
        .then(m => m.RepositoryAgent)
    }
];
