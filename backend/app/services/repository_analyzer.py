from pathlib import Path

from app.models.FileMetadata import FileMetadata
from app.models.RepositoryMetadata import RepositoryMetadata

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

PRIORITY_FILES = [
    "README.md",
    "README.rst",
    "README.txt",
    "pyproject.toml",
    "requirements.txt",
    "package.json",
    "main.py",
    "app.py",
    "server.py",
    "Dockerfile",
]

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

class RepositoryAnalyzer:

    # DETECTS THE LANGUAGE OF THE FILE 
    def detect_language(self, repo_path: Path) -> str:
        for item in repo_path.iterdir():
            if item.name in LANGUAGE_FILES:
                return LANGUAGE_FILES[item.name]
        return "Unknown"

    # RETURNS THE INFORMATION ABOUT THE REPO
    def analyze(self, repo_path: Path) -> dict:
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
    def directory_exists(self, repo_path: Path, dirname: str):
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

    # FINDS THE IMPORTANT FILES IN THE REPO
    def get_priority_files(self, repo_path: Path) -> list[Path]:
        priority_files = []

        for filename in PRIORITY_FILES:
            file = self.get_file(repo_path, filename)

            if file:
                priority_files.append(file)

        return priority_files

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
