import re
from pathlib import Path

from app.models.repository.FileMetadata import FileMetadata
from app.models.repository.RepositoryMetadata import RepositoryMetadata

EXTENSION_LANGUAGE = {
    ".py": "Python",
    ".java": "Java",
    ".ts": "TypeScript",
    ".js": "JavaScript",
    ".tsx": "React",
    ".jsx": "React",
    ".go": "Go",
    ".rs": "Rust",
    ".cpp": "C++",
    ".c": "C"
}

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

LANGUAGE_FILES = {
    "requirements.txt": "Python",
    "pyproject.toml": "Python",
    "package.json": "JavaScript/TypeScript",
    "pom.xml": "Java",
    "build.gradle": "Java/Kotlin",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
}

IGNORE_DIRECTORIES = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".idea",
    ".vscode",
    ".next",
    ".angular",
    "target",
    "out"
}

IGNORE_FILES = {
    ".env.example",
    ".DS_Store",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock"
}

FRAMEWORKS = {
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "@angular/core": "Angular",
    "react": "React",
    "vue": "Vue.js",
    "next": "Next.js",
    "express": "Express.js",
    "spring-boot": "Spring Boot",
    "gin": "Gin",
    "fiber": "Fiber",
    "actix-web": "Actix Web",
    "rocket": "Rocket"
}

DOCUMENTATION_FILES = {
    "README.md",
    "README.rst",
    "README.txt",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
}

DOCUMENTATION_EXTENSIONS = {
    ".md",
    ".txt",
}

CONFIGURATION_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "tsconfig.json",
    "angular.json",
    "vite.config.ts",
    "vite.config.js",
    "next.config.js",
    "next.config.ts",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "Cargo.toml",
}

DEPENDENCY_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "Cargo.toml",
}

ENTRY_POINT_FILES = {
    "main.py",
    "app.py",
    "server.py",
}

class RepositoryAnalyzer:

    # DETECTS THE LANGUAGE OF THE FILE 
    def detect_language(self, repo_path: Path) -> str:
        for item in repo_path.iterdir():
            if item.name in LANGUAGE_FILES:
                return LANGUAGE_FILES[item.name]
        return "Unknown"

    # RETURNS THE INFORMATION ABOUT THE REPO
    def analyze(self, repo_path: Path) -> RepositoryMetadata:
        return RepositoryMetadata(
            repository_name = repo_path.name,
            language = self.detect_language(repo_path),
            has_readme = self.detect_readme(repo_path),
            has_license = self.detect_license(repo_path),
            dockerized = self.detect_docker(repo_path),
            has_tests = self.detect_tests(repo_path)
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

    # DETECTS THE FRAMEWORK USED
    def detect_framework(self, repo_path: Path) -> str:
        for file in self.get_files(repo_path, DEPENDENCY_FILES):
            content = self.read_file(file).lower()
            words = re.findall(r"[A-Za-z0-9@._/-]+", content.lower())

            for keyword, framework in FRAMEWORKS.items():
                if keyword in words:
                    return framework

        return "Unknown"

    # RETURNS THE DEPENDENCIES USED IN THE REPOSITORY
    def find_dependencies(self, repo_path: Path) -> list[str]:
        dependencies = set()

        for file in self.get_files(repo_path, DEPENDENCY_FILES):
            content = self.read_file(file)

            for line in content.splitlines():
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                package = (line.split("==")[0].split(">=")[0].split("<=")[0].strip())
                dependencies.add(package)
        return sorted(dependencies)

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
