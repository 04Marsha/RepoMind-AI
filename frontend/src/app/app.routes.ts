import { Routes } from '@angular/router';
import { LandingPage } from './pages/landing-page/landing-page';
import { Agents } from './pages/agents/agents';

export const routes: Routes = [
    {
        path: '',
        component: LandingPage
    },
    {
        path: 'agents',
        component: Agents,
    },
];
