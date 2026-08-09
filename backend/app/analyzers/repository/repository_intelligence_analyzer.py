from pathlib import Path

from app.models.repository.RepositoryContext import RepositoryContext
from app.models.repository.RepositoryIntelligence import RepositoryIntelligence
from app.analyzers.repository.constants import ENTRY_POINT_FILES, NON_PRIMARY
from app.analyzers.repository.repository_analyzer import RepositoryAnalyzer
from app.analyzers.technology.technology_detector import TechnologyDetector
from app.analyzers.repository.entry_point_detector import EntryPointDetector

class RepositoryIntelligenceAnalyzer:

    def __init__(
        self, 
        repository_analyzer: RepositoryAnalyzer, 
        technology_detector: TechnologyDetector,
        entry_point_detector: EntryPointDetector
    ):
        self.repository_analyzer = repository_analyzer
        self.technology_detector = technology_detector
        self.entry_point_detector = entry_point_detector

    def analyze(self, context: RepositoryContext) -> RepositoryIntelligence:
        intelligence = RepositoryIntelligence()
        languages = self.repository_analyzer.detect_languages(context.repository_root)
        intelligence.languages = languages
        intelligence.primary_language = self.determine_primary_language(intelligence.languages)

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

        intelligence.package_manager = self.detect_package_manager(context.repository_root)

        intelligence.entry_points = self.entry_point_detector.detect(context)

        return intelligence

    def detect_package_manager(self, repository_root: Path):
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
            if (repository_root / file).exists():
                return manager

        return None

    def determine_primary_language(self, languages: list[str]):

        for language in languages:
            if language not in NON_PRIMARY:
                return language
        return languages[0] if languages else "Unknown"