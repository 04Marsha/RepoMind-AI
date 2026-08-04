TECHNOLOGIES = [
    {
        "name": "FastAPI",
        "type": "backend_framework",
        "keywords": ["fastapi"],
        "package_files": ["requirements.txt", "pyproject.toml"]
    },
    {
        "name": "Flask",
        "type": "backend_framework",
        "keywords": ["flask"],
        "package_files": ["requirements.txt", "pyproject.toml"]
    },
    {
        "name": "Angular",
        "type": "frontend_framework",
        "keywords": ["@angular/core"],
        "package_files": ["package.json"]
    },
    {
        "name": "React",
        "type": "frontend_framework",
        "keywords": ["react"],
        "package_files": ["package.json"]
    },
]

ENTRY_POINT_FILES = {

    # Python
    "main.py",
    "app.py",
    "server.py",

    # Node
    "index.js",
    "app.js",
    "server.js",

    "index.ts",
    "app.ts",
    "server.ts",

    # Java
    "Application.java",

    # Go
    "main.go",

    # Rust
    "main.rs"
}

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

DOCUMENTATION_FILES = {
    "README.md",
    "README.rst",
    "README.txt",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
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