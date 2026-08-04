import json
from pathlib import Path

from app.models.repository.FileMetadata import FileMetadata
from app.models.repository.RepositoryMetadata import RepositoryMetadata
from app.models.repository.RepositoryContext import RepositoryContext
from app.analyzers.repository.constants import (
    EXTENSION_LANGUAGE,
    IGNORE_DIRECTORIES, 
    IGNORE_FILES,
    DOCUMENTATION_FILES,
    CONFIGURATION_FILES
    )
from app.analyzers.dependency.dependency_parser import DependencyParser
from collections import Counter

ALLOWED_EXTENSIONS = set(EXTENSION_LANGUAGE.keys())
ALLOWED_EXTENSIONS.update({
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".toml",
    ".sql"
})

class RepositoryAnalyzer:

    def __init__(self, dependency_parser: DependencyParser):
        self.dependency_parser = dependency_parser

    # DETECTS THE LANGUAGE OF THE FILE 
    def detect_language(self, repo_path: Path) -> str:
        languages = self.detect_languages(repo_path)

        if languages:
            return languages[0]
        return "Unknown"

    def detect_languages(self, repo_path: Path) -> list[str]:
        language_counter = Counter()

        for file in self.get_source_files(repo_path):
            language = self.detect_file_language(file)

            if language != "Unknown":
                language_counter[language] += 1
        return [language for language, _ in language_counter.most_common()]

    # RETURNS THE INFORMATION ABOUT THE REPO
    def analyze(self, context: RepositoryContext) -> RepositoryMetadata:
        languages = self.detect_languages(context.project_root)
        return RepositoryMetadata(
            repository_name=context.repository_name,
            primary_language=languages[0],
            languages=languages,
            has_readme=self.detect_readme(context.project_root),
            has_license=self.detect_license(context.project_root),
            dockerized=self.detect_docker(context.project_root),
            has_tests=self.detect_tests(context.project_root),
        )

    # CHECKS IF THE FILE EXISTS
    def file_exists(self, repo_path: Path, filename: str) -> bool:
        return (repo_path / filename).is_file()

    # CHECKS IF A DIRECTORY/FOLDER EXISTS
    def directory_exists(self, repo_path: Path, dirname: str) -> bool:
        return (repo_path / dirname).is_dir()

    # CHECKS IF A README FILE EXISTS
    def detect_readme(self, repo_path: Path) -> bool:
        return self.file_exists(repo_path, "README.md")

    # CHECKS IF LICENSE EXISTS
    def detect_license(self, repo_path: Path) -> bool:
        return self.file_exists(repo_path, "LICENSE")

    # CHECKS IN DOCKER FILE EXISTS
    def detect_docker(self, repo_path: Path) -> bool:
        return self.file_exists(repo_path, "Dockerfile")

    # CHECKS IF TEST OR TESTS FOLDER EXISTS
    def detect_tests(self, repo_path: Path) -> bool:
        return (
            self.directory_exists(repo_path, "test")
            or self.directory_exists(repo_path, "tests")
        )

    # CHECKS IF THE FILE EXISTS IN THE REPO
    def get_file(self, repo_path: Path, filename: str) -> Path | None:
        file = repo_path / filename

        if file.is_file():
            return file
        return None

    # RETURNS THE FILES
    def get_files(self, repo_path: Path, filenames: set[str]) -> list[Path]:
        files = []
        for filename in filenames:
            file = self.get_file(repo_path, filename)
            if file:
                files.append(file)

        return files

    # GETS THE FILES IN THE REPO, STORES AND RETURNS THEM
    def get_all_files(self, repo_path: Path) -> list[Path]:
        files = []

        for item in repo_path.iterdir():

            if item.is_file():
                if item.name not in IGNORE_FILES and item.suffix in ALLOWED_EXTENSIONS:
                    files.append(item)
            elif item.is_dir():
                if item.name not in IGNORE_DIRECTORIES:
                    files.extend(self.get_all_files(item))

        return files

    # BUILDS METADATA FOR EVERY FILE IN THE REPO
    def index_repository(self, repo_path: Path) -> list[FileMetadata]:
        files = self.get_all_files(repo_path)

        index = []

        for file in files:
            content = self.read_file(file)

            if not content:
                continue

            metadata = FileMetadata(
                path = str(file.relative_to(repo_path)),
                extension = file.suffix,
                language = self.detect_file_language(file),
                size = file.stat().st_size,
                content = content
            )

            index.append(metadata)

        return index

    # DETECTS FILE LANGUAGE
    def detect_file_language(self, file: Path) -> str:
        return EXTENSION_LANGUAGE.get(file.suffix, "Unknown")

    # READS FILE
    def read_file(self, file: Path) -> str:
        try:
            return file.read_text(encoding="utf-8")
        except Exception:
            return ""

    # COUNTS THE TOTAL NUMBER OF FILES
    def count_files(self, repo_path: Path) -> int:
        return len(self.get_all_files(repo_path))

    # COUNTS THE TOTAL NUMBER OF DIRECTORIES
    def count_directories(self, repo_path: Path) -> int:
        count = 0

        for item in repo_path.iterdir():
            if item.is_dir() and item.name not in IGNORE_DIRECTORIES:
                count += 1
                count += self.count_directories(item)
        return count

    # RETURNS ALL SOURCE FILES
    def get_source_files(self, repo_path: Path) -> list[Path]:
        files = self.get_all_files(repo_path)

        return [
            file for file in files if file.suffix in EXTENSION_LANGUAGE
        ]

    # COUNTS SOURCE FILES
    def count_source_files(self, repo_path: Path) -> int:
        return len(self.get_source_files(repo_path))

    # RETURNS THE DEPENDENCIES USED IN THE REPOSITORY
    def find_dependencies(self, repo_path: Path) -> list[str]:
        return self.dependency_parser.parse(repo_path)

    # RETURNS ALL DOCUMENTATION FILES
    def get_documentation_files(self, repo_path: Path) -> list[Path]:
        return self.get_files(repo_path, DOCUMENTATION_FILES)

    # COUNTS ALL DOCUMENTATION FILES
    def count_documentation_files(self, repo_path: Path) -> int:
        return len(self.get_documentation_files(repo_path))

    # RETURNS ALL CONFIGURATION FILES
    def get_configuration_files(self, repo_path: Path) -> list[Path]:
        return self.get_files(repo_path, CONFIGURATION_FILES)

    # COUNTS ALL CONFIGURATION FILES
    def count_configuration_files(self, repo_path: Path) -> int:
        return len(self.get_configuration_files(repo_path))
