from pathlib import Path

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

    ".env.example"
]

class RepositoryAnalyzer:

    # DETECTS THE LANGUAGE OF THE FILE 
    def detect_language(self, repo_path: Path):
        for item in repo_path.iterdir():
            if item.name in LANGUAGE_FILES:
                return LANGUAGE_FILES[item.name]
        return "Unknown"

    # RETURNS THE INFORMATION ABOUT THE REPO
    def analyze(self, repo_path: Path):
        return {
            "repository_name": repo_path.name,
            "language": self.detect_language(repo_path),
            "has_readme": self.detect_readme(repo_path),
            "has_license": self.detect_license(repo_path),
            "dockerized": self.detect_docker(repo_path),
            "has_tests": self.detect_tests(repo_path)
        }

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
    def get_file(self, repo_path: Path, filename: str):
        file = repo_path / filename

        if file.is_file():
            return file
        return None

    # FINDS THE IMPORTANT FILES IN THE REPO
    def get_priority_files(self, repo_path: Path):
        priority_files = []

        for filename in PRIORITY_FILES:
            file = self.get_file(repo_path, filename)

            if file:
                priority_files.append(file)

        return priority_files

    # GETS THE FILES IN THE REPO, STORES AND RETURNS THEM
    def get_all_files(self, repo_path: Path):
        files = []

        for item in repo_path.iterdir():

            if item.is_file():
                files.append(item)
            elif item.is_dir():
                files.extend(self.get_all_files(item))

        return files


repository_analyzer = RepositoryAnalyzer()