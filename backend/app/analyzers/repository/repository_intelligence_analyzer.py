from pathlib import Path

from app.models.repository.RepositoryContext import RepositoryContext
from app.models.repository.RepositoryIntelligence import RepositoryIntelligence
from app.analyzers.repository.constants import ENTRY_POINT_FILES
from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.analyzers.technology.technology_detector import TechnologyDetector

class RepositoryIntelligenceAnalyzer:

    def __init__(self, repository_analyzer: RepositoryAnalyzer, technology_detector: TechnologyDetector):
        self.repository_analyzer = repository_analyzer
        self.technology_detector = technology_detector

    def analyze(self, context: RepositoryContext) -> RepositoryIntelligence:
        intelligence = RepositoryIntelligence()
        intelligence.language = self.repository_analyzer.detect_language(context.project_root)

        technologies = self.technology_detector.detect(context)

        for tech in technologies:
            match tech.category:
                case "frontend_framework":
                    intelligence.frontend_frameworks.append(tech.name)
                case "backend_framework":
                    intelligence.backend_frameworks.append(tech.name)
                case "database":
                    intelligence.databases.append(tech.name)
                case "vector_database":
                    intelligence.vector_databases.append(tech.name)
                case "orm":
                    intelligence.orms.append(tech.name)
                case "testing":
                    intelligence.testing_frameworks.append(tech.name)
                case "build_tool":
                    intelligence.build_tools.append(tech.name)

        intelligence.package_manager = self.detect_package_manager(context.project_root)

        entry_points = []

        for file in context.project_root.rglob("*"):
            if file.name in ENTRY_POINT_FILES:
                entry_points.append(str(file.relative_to(context.project_root)))
        intelligence.entry_points = entry_points

        return intelligence

    def detect_package_manager(self, project_root: Path):
        mapping = {
            "requirements.txt": "pip",
            "pyproject.toml": "pip",
            "package.json": "npm",
            "Cargo.toml": "Cargo",
            "go.mod": "Go Modules",
            "pom.xml": "Maven",
            "build.gradle": "Gradle",
            "Gemfile": "Bundler",
            "composer.json": "Composer"
        }

        for file, manager in mapping.items():
            if (project_root / file).exists():
                return manager

        return None