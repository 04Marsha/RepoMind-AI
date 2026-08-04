from pathlib import Path

from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.models.repository.RepositoryOverview import RepositoryOverview
from app.models.repository.RepositoryContext import RepositoryContext
from app.analyzers.repository.repository_intelligence_analyzer import RepositoryIntelligenceAnalyzer
from app.discovery.project_discovery import ProjectDiscovery

class RepositoryAgent:

    def __init__(self, repository_analyzer: RepositoryAnalyzer, repository_intelligence_analyzer: RepositoryIntelligenceAnalyzer, project_discovery :ProjectDiscovery):
        self.repository_analyzer = repository_analyzer
        self.repository_intelligence_analyzer = repository_intelligence_analyzer
        self.project_discovery = project_discovery

    # GETS THE OVERVIEW FOR THE REPO
    def get_repository_overview(self, repo_path: Path) -> RepositoryOverview:
        context = context = self.project_discovery.discover(repo_path)

        metadata = self.repository_analyzer.analyze(context)
        intelligence=self.repository_intelligence_analyzer.analyze(context)

        return RepositoryOverview(
            repository_name=metadata.repository_name,
            primary_language=metadata.primary_language,
            languages=metadata.languages,
            framework=(intelligence.backend_frameworks + intelligence.frontend_frameworks),
            total_files=self.repository_analyzer.count_files(context.project_root),
            total_directories=self.repository_analyzer.count_directories(repo_path),
            source_files=self.repository_analyzer.count_source_files(repo_path),
            documentation_files=self.repository_analyzer.count_documentation_files(repo_path),
            configuration_files=self.repository_analyzer.count_configuration_files(context.project_root),
            has_readme=metadata.has_readme,
            has_license=metadata.has_license,
            has_tests=metadata.has_tests,
            dockerized=metadata.dockerized,
            dependencies=self.repository_analyzer.find_dependencies(context.project_root)
        )

    