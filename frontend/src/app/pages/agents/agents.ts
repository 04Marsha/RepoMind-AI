import { Component } from '@angular/core';

export interface Agent {
  phase: string;
  title: string;
  description: string;
  icon: string;
  link: string;
}

@Component({
  selector: 'app-agents',
  imports: [],
  templateUrl: './agents.html',
  styleUrl: './agents.css',
})
export class Agents {
  agents: Agent[] = [
    {
      phase: 'AGENT 01',
      title: 'Repository Agent',
      description: 'Analyzes repository structure, technologies, dependencies, and code organization.',
      icon: 'repository_agent.png',
      link: '/repository-agent',
    },
    // {
    //   phase: 'AGENT 02',
    //   title: 'Documentation Agent',
    //   description: 'Generates clear documentation, READMEs, and developer guides from code.',
    //   icon: 'repository_agent.png',
    //   link: '/repository-agent',
    // },
    // {
    //   phase: 'AGENT 03',
    //   title: 'Code Search Agent',
    //   description: 'Finds relevant files, functions, classes, and code snippets across the repository.',
    //   icon: 'repository_agent.png',
    //   link: '/repository-agent',
    // },
    // {
    //   phase: 'AGENT 04',
    //   title: 'Security Agent',
    //   description: 'Detects potential vulnerabilities, insecure patterns, and security risks.',
    //   icon: 'repository_agent.png',
    //   link: '/repository-agent',
    // },
    // {
    //   phase: 'AGENT 05',
    //   title: 'DSA Mentor Agent',
    //   description: 'Explains algorithms, data structures, and coding concepts used in the codebase.',
    //   icon: 'repository_agent.png',
    //   link: '/repository-agent',
    // },
    // {
    //   phase: 'AGENT 06',
    //   title: 'Test Generator Agent',
    //   description: 'Creates unit tests, integration tests, and testing recommendations.',
    //   icon: 'repository_agent.png',
    //   link: '/repository-agent',
    // },
    // {
    //   phase: 'AGENT 07',
    //   title: 'Refactoring Agent',
    //   description: 'Recommends cleaner, more maintainable, and scalable code improvements.',
    //   icon: 'repository_agent.png',
    //   link: '/repository-agent',
    // },
    // {
    //   phase: 'AGENT 08',
    //   title: 'Bug Finder Agent',
    //   description: 'Locates potential bugs, logic errors, and edge-case failures.',
    //   icon: 'repository_agent.png',
    //   link: '/repository-agent',
    // },
    // {
    //   phase: 'AGENT 09',
    //   title: 'Orchestrator Agent',
    //   description: 'Coordinates all agents.',
    //   icon: 'repository_agent.png',
    //   link: '/repository-agent',
    // },
  ];
}
