DISCOVERY_SCORES = {
    # Strong indicators
    "requirements.txt": 100,
    "pyproject.toml": 100,
    "package.json": 100,
    "pom.xml": 100,
    "build.gradle": 100,
    "go.mod": 100,
    "Cargo.toml": 100,
    "pubspec.yaml": 100,

    # Weak indicators
    "main.py": 20,
    "app.py": 20,
    "server.py": 20,

    "Dockerfile": 10,
    "README.md": 5,
}

STRONG_PROJECT_FILES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "Cargo.toml",
    "pubspec.yaml",
}