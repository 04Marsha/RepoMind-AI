from pathlib import Path

from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.models.repository.RepositoryOverview import RepositoryOverview
from app.analyzers.repository.repository_intelligence_analyzer import RepositoryIntelligenceAnalyzer
from app.discovery.project_discovery import ProjectDiscovery
from app.analyzers.structure.structure_analyzer import StructureAnalyzer
from app.analyzers.architecture.architecture_analyzer import ArchitectureAnalyzer
from app.analyzers.api.api_endpoint_analyzer import ApiEndpointAnalyzer
from app.analyzers.database.database_analyzer import DatabaseAnalyzer
from app.analyzers.metrics.metrics_analyzer import MetricsAnalyzer
from app.models.agents.repository_agent_model import RepositoryAgentModel

class RepositoryAgent:

    def __init__(self, 
        repository_analyzer: RepositoryAnalyzer, 
        repository_intelligence_analyzer: RepositoryIntelligenceAnalyzer, 
        project_discovery :ProjectDiscovery,
        structure_analyzer = StructureAnalyzer,
        metrics_analyzer = MetricsAnalyzer,
        architecture_analyzer = ArchitectureAnalyzer,
        api_endpoint_analyzer = ApiEndpointAnalyzer,
        database_analyzer = DatabaseAnalyzer,
    ):
        self.repository_analyzer = repository_analyzer
        self.repository_intelligence_analyzer = repository_intelligence_analyzer
        self.project_discovery = project_discovery
        self.structure_analyzer = structure_analyzer
        self.metrics_analyzer = metrics_analyzer
        self.architecture_analyzer = architecture_analyzer
        self.api_endpoint_analyzer = api_endpoint_analyzer
        self.database_analyzer = database_analyzer

    # GETS THE OVERVIEW FOR THE REPO
    def get_repository_overview(self, repo_path: Path) -> RepositoryOverview:
        context = context = self.project_discovery.discover(repo_path)

        metadata = self.repository_analyzer.analyze(context)
        intelligence=self.repository_intelligence_analyzer.analyze(context)

        return RepositoryOverview(
            repository_name=metadata.repository_name,
            primary_language=intelligence.primary_language,
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

    # COMBINES ALL THE INFO FROM THE ANALYZERS
    def analyze_repository(self, repo_path: Path) -> RepositoryAgentModel:
        context = self.project_discovery.discover(repo_path)

        return RepositoryAgentModel(
            overview=self.get_repository_overview(repo_path),
            intelligence=self.repository_intelligence_analyzer.analyze(context),
            structure=self.structure_analyzer.analyze(context),
            metrics=self.metrics_analyzer.analyze(context),
            architecture=self.architecture_analyzer.analyze(context),
            api_analysis=self.api_endpoint_analyzer.analyze(context),
            database=self.database_analyzer.analyze(context)
        )