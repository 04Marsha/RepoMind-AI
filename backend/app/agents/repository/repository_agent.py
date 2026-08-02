from pathlib import Path

from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.models.repository.RepositoryOverview import RepositoryOverview

class RepositoryAgent:

    def __init__(self, repository_analyzer: RepositoryAnalyzer):
        self.repository_analyzer = repository_analyzer

    # GETS THE OVERVIEW FOR THE REPO
    def get_repository_overview(self, repo_path: Path) -> RepositoryOverview:
        metadata = self.repository_analyzer.analyze(repo_path)

        return RepositoryOverview(
            repository_name=metadata.repository_name,
            primary_language=metadata.language,
            framework=self.repository_analyzer.detect_framework(repo_path),
            total_files=self.repository_analyzer.count_files(repo_path),
            total_directories=self.repository_analyzer.count_directories(repo_path),
            source_files=self.repository_analyzer.count_source_files(repo_path),
            documentation_files=self.repository_analyzer.count_documentation_files(repo_path),
            configuration_files=self.repository_analyzer.count_configuration_files(repo_path),
            has_readme=metadata.has_readme,
            has_license=metadata.has_license,
            has_tests=metadata.has_tests,
            dockerized=metadata.dockerized,
            dependencies=self.repository_analyzer.find_dependencies(repo_path)
        )

    